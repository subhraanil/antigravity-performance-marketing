import csv
import os

html_csv = r"website audit/labelitsolutions.co.uk - internal_html.csv"
out_dir = r"website audit/labelitsolutions.co.uk"

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
        
        if "/product/" in url:
            cat = "Product Detail Page"
        elif "/product-category/" in url:
            cat = "Product Category Archive"
        elif any(tax in url for tax in ["/label-width/", "/label-length/", "/material/", "/printer-compatibility/", "/adhesive/"]):
            cat = "WooCommerce Attribute Taxonomy"
        elif any(sys_p in url for sys_p in ["/cart/", "/checkout/", "/my-account/", "/login/", "/registration/", "/quotation/"]):
            cat = "System / Account"
        elif any(pol in url for pol in ["/privacy", "/terms", "/returns", "/about-us", "/contact-us", "/faq", "/shop", "/blog"]):
            cat = "Standard / Policy Page"
        elif url.endswith(".png"):
            cat = "Broken Image Asset"
        else:
            cat = "Article / Other"
            
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
