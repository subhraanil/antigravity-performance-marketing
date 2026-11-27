import csv
import os

html_csv = r"C:\Users\test\Videos\Personal\data\Paid Media World\Paid Media World - internal_html.csv"
out_dir = r"website audit/paidmediaworld.com"

with open(html_csv, mode="r", encoding="utf-8-sig", errors="replace") as f:
    r = csv.DictReader(f)
    rows = list(r)

# 1. 01_url_inventory.csv
inv_file = os.path.join(out_dir, "01_url_inventory.csv")
with open(inv_file, mode="w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["Address", "Content Type", "Status Code", "Indexability", "Page Category", "Word Count"])
    for row in rows:
        url = row.get("Address", "")
        ctype = row.get("Content Type", "")
        status = row.get("Status Code", "")
        idx = row.get("Indexability", "")
        wc = row.get("Word Count", "")
        
        if url == "https://paidmediaworld.com/":
            cat = "Homepage"
        elif "/category/" in url:
            cat = "Category Archive"
        elif "/tools/" in url or "calculator" in url or "wordcounter" in url:
            cat = "Interactive Tool / Calculator"
        elif "?service=" in url:
            cat = "Parameter Route"
        elif status == "404":
            cat = "Broken Link / 404 Error"
        elif status == "301":
            cat = "Redirect Hop / 301"
        elif any(p in url for p in ["/contact-us", "/about-us", "/privacy-policy", "/terms-of-service", "/free-audit"]):
            cat = "Core Business / Policy Page"
        else:
            cat = "Educational Guide / Article"
            
        w.writerow([url, ctype, status, idx, cat, wc])

print(f"[+] Saved 01_url_inventory.csv ({len(rows)} URLs)")

# 2. 02_page_data.csv
pg_file = os.path.join(out_dir, "02_page_data.csv")
with open(pg_file, mode="w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    headers = [
        "Address", "Status Code", "Indexability", "Title", "Title Length",
        "Meta Description", "Meta Description Length", "H1-1", "H1-2",
        "Canonical URL", "Word Count", "Inlinks", "Outlinks"
    ]
    w.writerow(headers)
    for row in rows:
        w.writerow([
            row.get("Address", ""),
            row.get("Status Code", ""),
            row.get("Indexability", ""),
            row.get("Title 1", ""),
            row.get("Title 1 Length", ""),
            row.get("Meta Description 1", ""),
            row.get("Meta Description 1 Length", ""),
            row.get("H1-1", ""),
            row.get("H1-2", ""),
            row.get("Canonical Link Element 1", ""),
            row.get("Word Count", ""),
            row.get("Inlinks", ""),
            row.get("Outlinks", "")
        ])

print(f"[+] Saved 02_page_data.csv ({len(rows)} rows)")
