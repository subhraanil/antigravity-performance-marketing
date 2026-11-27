import csv
from collections import Counter

html_csv = r"C:\Users\test\Videos\Personal\data\Paid Media World\Paid Media World - internal_html.csv"

with open(html_csv, mode="r", encoding="utf-8-sig", errors="replace") as f:
    r = csv.DictReader(f)
    rows = list(r)

print(f"Total rows in internal_html.csv: {len(rows)}")

# Status codes
status_counts = Counter(r["Status Code"] for r in rows)
print("Status codes:", status_counts)

# Indexability
idx_counts = Counter(r["Indexability"] for r in rows)
print("Indexability:", idx_counts)

# 404 Client Errors
print("\n=== 404 CLIENT ERRORS (11 URLs) ===")
err_404 = [r for r in rows if r["Status Code"] == "404"]
for r in err_404:
    print(f"  {r['Address']} | Inlinks: {r.get('Inlinks', '')}")

# 301 Redirects
print("\n=== SAMPLE 301 REDIRECTS (37 URLs) ===")
red_301 = [r for r in rows if r["Status Code"] == "301"]
print(f"Total 301s: {len(red_301)}")
for r in red_301[:12]:
    print(f"  {r['Address']} -> {r.get('Redirect URL', '')}")

# URL Types
types = Counter()
for r in rows:
    url = r["Address"]
    if "/category/" in url:
        types["Category"] += 1
    elif "/tag/" in url:
        types["Tag"] += 1
    elif "/author/" in url:
        types["Author"] += 1
    elif "/page/" in url:
        types["Pagination"] += 1
    elif url == "https://paidmediaworld.com/":
        types["Homepage"] += 1
    else:
        # Check if blog post or static page
        types["Post/Page"] += 1

print("\nURL Types Breakdown:", types)
