"""Rules for B2B paid media tracking links. Standard library only.

The rules follow tracking/utm-naming-convention.md and tracking/salesforce-campaign-hierarchy.md.
"""
import csv
import re
from datetime import datetime
from pathlib import Path
from urllib.parse import urlsplit, parse_qsl, urlencode, urlunsplit

RULES_FILE = Path(__file__).resolve().parent.parent / "rules" / "sources.csv"

UTM_KEYS = ["utm_source", "utm_medium", "utm_campaign", "utm_content", "utm_term"]
VALUE_PATTERN = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
# {year}-{quarter or half}-{program}[-{asset}], e.g. 2026-q3-abm-tech-sector
CAMPAIGN_PATTERN = re.compile(r"^(20\d{2})-(q[1-4]|h[12])-[a-z0-9]+(-[a-z0-9]+)*$")
# Mediums where each ad or creative needs its own utm_content
CONTENT_NEEDED = {"paid-social", "display"}

ERROR, WARN, NOTE = "ERROR", "WARN", "NOTE"


def load_rules(path=RULES_FILE):
    """{source: {medium: salesforce_type}} from rules/sources.csv."""
    rules = {}
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            rules.setdefault(r["utm_source"].strip(), {})[r["allowed_utm_medium"].strip()] = r["salesforce_campaign_type"].strip()
    return rules


def suggest(value):
    """The cleaned-up version of a UTM value: lowercase, hyphens, no special characters."""
    v = value.strip().lower()
    v = re.sub(r"[\s_/.]+", "-", v)
    v = re.sub(r"[^a-z0-9-]", "", v)
    return re.sub(r"-{2,}", "-", v).strip("-")


def build_url(destination, params):
    """Add UTM parameters to a destination URL, keeping any query it already has."""
    parts = urlsplit(destination.strip())
    query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if not k.startswith("utm_")]
    query += [(k, params[k]) for k in UTM_KEYS if params.get(k)]
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query, safe="-"), parts.fragment))


def _period_of(date_text):
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
        try:
            d = datetime.strptime(date_text.strip(), fmt)
            return d.year, (d.month - 1) // 3 + 1
        except ValueError:
            pass
    return None


def check_values(params, rules):
    """Checks on the five UTM values alone. Returns a list of (level, field, message)."""
    out = []
    source, medium, campaign = params.get("utm_source", ""), params.get("utm_medium", ""), params.get("utm_campaign", "")
    for key in ("utm_source", "utm_medium", "utm_campaign"):
        if not params.get(key, "").strip():
            out.append((ERROR, key, "missing. Every paid link needs source, medium and campaign."))
    for key in UTM_KEYS:
        v = params.get(key, "")
        if v and not VALUE_PATTERN.match(v):
            out.append((ERROR, key, f"'{v}' breaks the format (lowercase, hyphens only). Use '{suggest(v)}'."))
    if source and VALUE_PATTERN.match(source):
        if source not in rules:
            close = [s for s in rules if s[:4] == source[:4]]
            hint = f" Did you mean '{close[0]}'?" if close else " Add it to rules/sources.csv if it's a new partner."
            out.append((ERROR, "utm_source", f"'{source}' is not on the shared source list.{hint}"))
        elif medium and VALUE_PATTERN.match(medium) and medium not in rules[source]:
            allowed = ", ".join(rules[source])
            out.append((ERROR, "utm_medium", f"'{medium}' doesn't go with source '{source}'. Allowed: {allowed}."))
    if campaign and VALUE_PATTERN.match(campaign) and not CAMPAIGN_PATTERN.match(campaign):
        out.append((WARN, "utm_campaign", f"'{campaign}' doesn't follow year-period-program (e.g. 2026-q3-abm-tech-sector)."))
    if medium in CONTENT_NEEDED and not params.get("utm_content"):
        out.append((WARN, "utm_content", f"missing. On {medium} each ad needs its own utm_content, or you can't tell creatives apart."))
    if params.get("utm_term") and medium != "paid-search":
        out.append((WARN, "utm_term", "is only for paid search keywords. Leave it blank here."))
    return out


def check_tracker(rows, rules, salesforce=None):
    """Check every row of a UTM tracker. Returns (results per row, notes for the whole file)."""
    results = []
    seen_urls, seen_content = {}, {}
    sf_by_name = {c["name"].lower(): c for c in salesforce} if salesforce is not None else None
    for i, row in enumerate(rows):
        issues = []
        params = {k: row.get(k, "").strip() for k in UTM_KEYS}
        issues += check_values(params, rules)
        dest = row.get("destination_url", "")
        tagged = row.get("full_tagged_url", "").strip()
        expected = build_url(dest, params) if dest.strip() else ""

        # Destination URL
        if not dest.strip():
            issues.append((ERROR, "Destination URL", "missing."))
        else:
            if dest != dest.strip():
                issues.append((ERROR, "Destination URL", "has a space before or after it, which can break the link."))
            d = urlsplit(dest.strip())
            if d.scheme != "https":
                issues.append((ERROR, "Destination URL", "should start with https://."))
            if any(k.startswith("utm_") for k, _ in parse_qsl(d.query)):
                issues.append((ERROR, "Destination URL", "already has UTM parameters. Use the clean page URL."))

        # Full tagged URL must match the columns
        if not tagged:
            issues.append((ERROR, "Full Tagged URL", f"missing. It should be: {expected}" if expected else "missing."))
        elif expected:
            t, e = urlsplit(tagged), urlsplit(expected)
            t_utm = {k: v for k, v in parse_qsl(t.query) if k.startswith("utm_")}
            e_utm = {k: v for k, v in parse_qsl(e.query) if k.startswith("utm_")}
            if (t.netloc, t.path) != (e.netloc, e.path):
                issues.append((ERROR, "Full Tagged URL", "goes to a different page than the Destination URL."))
            if t_utm != e_utm:
                diffs = [f"{k}: link has '{t_utm.get(k, '')}', columns say '{e_utm.get(k, '')}'"
                         for k in UTM_KEYS if t_utm.get(k, "") != e_utm.get(k, "")]
                issues.append((ERROR, "Full Tagged URL", "doesn't match the columns (" + "; ".join(diffs) + ")."))
            dup_content = (params["utm_source"], params["utm_campaign"], params["utm_content"]) in seen_content
            if (tagged in seen_urls and not dup_content
                    and rows[seen_urls[tagged]].get("campaign_name") != row.get("campaign_name")):
                issues.append((ERROR, "Full Tagged URL", f"same link as row {seen_urls[tagged] + 2}, a different ad. "
                                                         "Give each ad its own utm_content."))
            seen_urls.setdefault(tagged, i)

        # Two ads in one campaign with the same utm_content
        key = (params["utm_source"], params["utm_campaign"], params["utm_content"])
        if params["utm_content"] and key in seen_content and seen_content[key][1] != row.get("campaign_name"):
            issues.append((ERROR, "utm_content", f"'{params['utm_content']}' is also used by row {seen_content[key][0] + 2} "
                                                 "in the same campaign. Test versions need different values."))
        seen_content.setdefault(key, (i, row.get("campaign_name")))

        # Campaign period vs. launch date
        launch = row.get("launch_date", "").strip()
        m = CAMPAIGN_PATTERN.match(params["utm_campaign"])
        if not launch:
            issues.append((WARN, "Launch Date", "missing."))
        elif m and _period_of(launch):
            year, quarter = _period_of(launch)
            period = m.group(2)
            ok_period = (period == f"q{quarter}") or (period == f"h{1 if quarter <= 2 else 2}")
            if int(m.group(1)) != year or not ok_period:
                issues.append((WARN, "utm_campaign", f"says {m.group(1)}-{period} but the launch date {launch} is {year}-q{quarter}."))

        # Salesforce campaign
        if sf_by_name is not None:
            name = row.get("campaign_name", "").strip()
            sf = sf_by_name.get(name.lower())
            if not name:
                issues.append((ERROR, "Campaign Name", "missing, so leads can't be matched to a Salesforce campaign."))
            elif sf is None:
                issues.append((ERROR, "Salesforce", f"no campaign named '{name}'. Create it before launch, or leads won't be credited."))
            else:
                if not sf.get("parent"):
                    issues.append((WARN, "Salesforce", f"'{name}' has no parent campaign, so it won't roll up to the program."))
                want = rules.get(params["utm_source"], {}).get(params["utm_medium"])
                if want and sf.get("type") and sf["type"].lower() != want.lower():
                    issues.append((WARN, "Salesforce", f"campaign type is '{sf['type']}'; for {params['utm_medium']} it should be '{want}'."))
                if sf.get("status", "").lower() in ("completed", "aborted"):
                    issues.append((WARN, "Salesforce", f"campaign status is '{sf['status']}'. Set it to Planned or Active."))
        results.append({"row": i + 2, "name": row.get("campaign_name", ""), "issues": issues, "expected_url": expected})

    notes = []
    if any(r.get("utm_source", "").strip().lower() == "google" and r.get("utm_medium", "").strip().lower() == "paid-search" for r in rows):
        notes.append("Google Search links: turn on auto-tagging in Google Ads and capture the GCLID in a hidden form field, "
                     "so MQLs and SQLs can be sent back to Google (see tracking/google-ads-to-salesforce.md).")
    if salesforce is None:
        notes.append("Salesforce campaigns not checked. Add --salesforce <campaigns.csv> to confirm every campaign exists "
                     "and rolls up to a parent.")
    return results, notes
