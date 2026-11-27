import csv

p_html = r"website audit\victoryhcspl.com\internal_html.csv"
p_issues = r"website audit\victoryhcspl.com\issues_overview_report.csv"

print("=== INTERNAL_HTML.CSV ===")
with open(p_html, "r", encoding="utf-8", errors="ignore") as f:
    reader = csv.DictReader(f)
    rows = list(reader)
    print(f"Total rows: {len(rows)}")
    for i, r in enumerate(rows):
        # find address key
        addr_key = [k for k in r.keys() if "Address" in k][0]
        addr = r.get(addr_key)
        sc = r.get("Status Code")
        idx = r.get("Indexability")
        idx_stat = r.get("Indexability Status")
        title = (r.get("Title 1") or "")[:40]
        h1 = (r.get("H1-1") or "")[:40]
        meta = (r.get("Meta Description 1") or "")[:40]
        print(f"{i+1:2d}. [{sc}] ({idx}/{idx_stat}) {addr}")
        print(f"    Title: {title} | H1: {h1} | Meta: {meta}")

print("\n=== ISSUES_OVERVIEW_REPORT.CSV ===")
with open(p_issues, "r", encoding="utf-8", errors="ignore") as f:
    reader = csv.DictReader(f)
    for i, r in enumerate(reader):
        name_key = [k for k in r.keys() if "Issue Name" in k][0]
        name = r.get(name_key)
        itype = r.get("Issue Type")
        prio = r.get("Issue Priority")
        urls_count = r.get("URLs")
        pct = r.get("% of Total")
        print(f"{i+1:2d}. [{prio}] {name} ({itype}): {urls_count} URLs ({pct}%)")
