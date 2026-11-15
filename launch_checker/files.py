"""Read the UTM tracker and the Salesforce campaign export; write a cleaned-up tracker."""
import csv
import re

from .checks import UTM_KEYS, build_url, suggest

# internal name -> accepted header labels (matched ignoring case, spaces and punctuation)
TRACKER_COLUMNS = {
    "campaign_name": ["Campaign Name", "Salesforce Campaign"],
    "channel": ["Channel"],
    "utm_source": ["utm_source", "UTM Source", "Source"],
    "utm_medium": ["utm_medium", "UTM Medium", "Medium"],
    "utm_campaign": ["utm_campaign", "UTM Campaign"],
    "utm_content": ["utm_content", "UTM Content", "Content"],
    "utm_term": ["utm_term", "UTM Term", "Term", "Keyword"],
    "destination_url": ["Destination URL", "Landing Page", "Landing Page URL"],
    "full_tagged_url": ["Full Tagged URL", "Tagged URL", "Final URL"],
    "launch_date": ["Launch Date", "Start Date"],
    "status": ["Status"],
}
SALESFORCE_COLUMNS = {
    "name": ["Campaign Name"],
    "parent": ["Parent Campaign", "Parent Campaign: Campaign Name", "Parent"],
    "type": ["Type", "Campaign Type"],
    "status": ["Status"],
}


def _key(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _read(path, columns):
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        headers = reader.fieldnames or []
        by_key = {_key(h): h for h in headers}
        mapping = {}
        for col, labels in columns.items():
            src = next((by_key[_key(l)] for l in [col] + labels if _key(l) in by_key), None)
            if src:
                mapping[col] = src
        rows = []
        for raw in reader:
            if not any((v or "").strip() for v in raw.values() if isinstance(v, str)):
                continue
            # Keep the raw destination URL so stray spaces can be caught.
            rows.append({col: (raw.get(src) or "") if col == "destination_url" else (raw.get(src) or "").strip()
                         for col, src in mapping.items()})
        return rows, mapping, headers


def read_tracker(path):
    rows, mapping, headers = _read(path, TRACKER_COLUMNS)
    missing = [c for c in ("utm_source", "utm_medium", "utm_campaign", "destination_url") if c not in mapping]
    return rows, mapping, headers, missing


def read_salesforce(path):
    rows, mapping, _ = _read(path, SALESFORCE_COLUMNS)
    if "name" not in mapping:
        raise ValueError(f"{path} has no 'Campaign Name' column.")
    return rows


def write_fixed(path_in, path_out, mapping):
    """Copy the tracker with format fixes: UTM values cleaned up, URLs trimmed, Full Tagged URL rebuilt.

    Only mechanical fixes. Wrong sources, mediums or duplicate content still need a person to decide.
    """
    with open(path_in, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        headers = list(reader.fieldnames)
        rows = [r for r in reader if any((v or "").strip() for v in r.values() if isinstance(v, str))]
    tagged_col = mapping.get("full_tagged_url") or "Full Tagged URL"
    if tagged_col not in headers:
        headers.append(tagged_col)
    changed = 0
    for r in rows:
        before = dict(r)
        params = {}
        for k in UTM_KEYS:
            src = mapping.get(k)
            if src and r.get(src):
                r[src] = suggest(r[src])
                params[k] = r[src]
        dest_col = mapping.get("destination_url")
        if dest_col and r.get(dest_col):
            r[dest_col] = r[dest_col].strip()
            r[tagged_col] = build_url(r[dest_col], params)
        changed += before != r
    with open(path_out, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=headers)
        w.writeheader()
        w.writerows(rows)
    return changed
