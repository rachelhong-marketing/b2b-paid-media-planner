"""Command line: build, check, rules."""
import argparse
from pathlib import Path

from . import checks, files


def main(argv=None):
    ap = argparse.ArgumentParser(prog="launch_checker",
                                 description="Build and check B2B paid media tracking links before launch.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    b = sub.add_parser("build", help="build one tagged link")
    b.add_argument("--url", required=True, help="landing page, e.g. https://yoursite.com/guide")
    b.add_argument("--source", required=True)
    b.add_argument("--medium", required=True)
    b.add_argument("--campaign", required=True)
    b.add_argument("--content", default="")
    b.add_argument("--term", default="")

    c = sub.add_parser("check", help="check a UTM tracker CSV before launch")
    c.add_argument("tracker")
    c.add_argument("--salesforce", help="Salesforce campaigns export (CSV) to check campaigns exist and roll up")
    c.add_argument("--fixed", help="also write a copy with format fixes and rebuilt links to this CSV")

    sub.add_parser("rules", help="show the allowed sources and mediums")
    a = ap.parse_args(argv)
    rules = checks.load_rules()

    if a.cmd == "rules":
        print(f"{'utm_source':<22}{'utm_medium':<22}Salesforce campaign type")
        for src, mediums in rules.items():
            for med, sf_type in mediums.items():
                print(f"{src:<22}{med:<22}{sf_type}")
        print("\nEdit rules/sources.csv to add your own partners.")
        return 0

    if a.cmd == "build":
        params = {"utm_source": a.source, "utm_medium": a.medium, "utm_campaign": a.campaign,
                  "utm_content": a.content, "utm_term": a.term}
        issues = checks.check_values(params, rules)
        for level, field, msg in issues:
            print(f"{level:<6}{field}: {msg}")
        if any(level == checks.ERROR for level, _, _ in issues):
            print("\nNot built. Fix the errors above first.")
            return 1
        print(checks.build_url(a.url, params))
        return 0

    path = Path(a.tracker)
    if not path.exists():
        print(f"File not found: {path}")
        return 2
    rows, mapping, _headers, missing = files.read_tracker(path)
    if missing:
        print("The tracker is missing these columns: " + ", ".join(missing))
        print("See templates/utm-tracker-template.csv for the expected columns.")
        return 2
    salesforce = files.read_salesforce(a.salesforce) if a.salesforce else None
    results, notes = checks.check_tracker(rows, rules, salesforce)

    ready = [r for r in results if not any(i[0] == checks.ERROR for i in r["issues"])]
    clean = [r for r in ready if not r["issues"]]
    print(f"Launch check: {path.name}\n")
    print(f"Ready to launch: {len(ready)} of {len(results)} links "
          f"({len(clean)} with no issues, {len(ready) - len(clean)} with warnings only)\n")
    for r in results:
        if not r["issues"]:
            continue
        errors = sum(1 for i in r["issues"] if i[0] == checks.ERROR)
        verdict = "FIX BEFORE LAUNCH" if errors else "OK TO LAUNCH, CHECK WARNINGS"
        print(f"Row {r['row']}: {r['name'] or '(no campaign name)'}  [{verdict}]")
        for level, field, msg in r["issues"]:
            print(f"  {level:<6}{field}: {msg}")
        print()
    for n in notes:
        print(f"NOTE  {n}")
    if a.fixed:
        changed = files.write_fixed(path, a.fixed, mapping)
        print(f"\nSaved {a.fixed}: format fixes and rebuilt links on {changed} row(s). "
              "Wrong sources, mediums and duplicate content still need a decision.")
    return 0 if len(ready) == len(results) else 1
