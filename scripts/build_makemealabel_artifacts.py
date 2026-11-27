import csv
import json
import os
import re

out_dir = r"website audit/makemealabel.com"
sf_internal = os.path.join(out_dir, "internal_all.csv")

print("=== BUILDING AUDIT ARTIFACTS FOR MAKEMEALABEL.COM ===")

# 1. Load Screaming Frog Data
html_rows = []
all_rows = []

with open(sf_internal, 'r', encoding='utf-8-sig', errors='ignore') as f:
    reader = csv.DictReader(f)
    for r in reader:
        all_rows.append(r)
        if "text/html" in r.get("Content Type", ""):
            html_rows.append(r)

print(f"Total rows in crawl: {len(all_rows)}")
print(f"Total HTML pages: {len(html_rows)}")

# 01_url_inventory.csv
inv_file = os.path.join(out_dir, "01_url_inventory.csv")
with open(inv_file, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(["Address", "Content Type", "Status Code", "Status", "Indexability", "Indexability Status", "Word Count", "Type"])
    for r in html_rows:
        u = r.get("Address", "")
        ptype = "Product" if "/products/" in u else ("Collection" if "/collections/" in u else ("Blog" if "/blogs/" in u else ("Policy" if "/policies/" in u else ("Page" if "/pages/" in u else "Other"))))
        w.writerow([u, r.get("Content Type", ""), r.get("Status Code", ""), r.get("Status", ""), r.get("Indexability", ""), r.get("Indexability Status", ""), r.get("Word Count", ""), ptype])

print(f"[+] Created {inv_file}")

# 02_page_data.csv
pdata_file = os.path.join(out_dir, "02_page_data.csv")
with open(pdata_file, 'w', newline='', encoding='utf-8') as f:
    fields = [
        "Address", "Type", "Status Code", "Indexability", "Title", "Title Length",
        "Meta Description", "Meta Desc Length", "H1", "H1 Length", "H2 Count",
        "Word Count", "Canonical", "Response Time (s)", "Size (Bytes)"
    ]
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for r in html_rows:
        u = r.get("Address", "")
        ptype = "Product" if "/products/" in u else ("Collection" if "/collections/" in u else ("Blog" if "/blogs/" in u else ("Policy" if "/policies/" in u else ("Page" if "/pages/" in u else "Other"))))
        w.writerow({
            "Address": u,
            "Type": ptype,
            "Status Code": r.get("Status Code", ""),
            "Indexability": r.get("Indexability", ""),
            "Title": r.get("Title 1", ""),
            "Title Length": r.get("Title 1 Length", ""),
            "Meta Description": r.get("Meta Description 1", ""),
            "Meta Desc Length": r.get("Meta Description 1 Length", ""),
            "H1": r.get("H1-1", ""),
            "H1 Length": r.get("H1-1 Length", ""),
            "H2 Count": r.get("H2-1 Length", ""),
            "Word Count": r.get("Word Count", ""),
            "Canonical": r.get("Canonical Link Element 1", ""),
            "Response Time (s)": r.get("Response Time", ""),
            "Size (Bytes)": r.get("Size (Bytes)", "")
        })

print(f"[+] Created {pdata_file}")

# 04_issues_log.csv
issues_file = os.path.join(out_dir, "04_issues_log.csv")
issues_data = [
    ("Homepage H1 Wraps Logo Image With Zero Text Heading", "Critical", "https://makemealabel.com/", "Homepage H1 contains only <a><img></a>. Completely lacks keyword-focused text H1 for label manufacturing."),
    ("Primary Collection Pages Have Zero H1 Headings", "Critical", "https://makemealabel.com/collections/*", "All major category collections (/direct-thermal-roll-labels-blank, /thermal-transfer-roll-labels-blank, /custom-printed-labels) have 0 H1 elements."),
    ("Shopify Liquid Translation Missing Bug in SERP Titles", "Critical", "https://makemealabel.com/collections/all?page=2, /blogs/news?page=2", "Liquid template bug prints 'Translation missing: en.general.meta.page' directly into page title tags, appearing in Google search snippets."),
    ("Apparel Demo Placeholders on Industrial Label Product Pages", "Critical", "https://makemealabel.com/products/*", "PDPs display empty Shopify Dawn apparel theme accordion headers ('Materials and care', 'Merchandising tips', 'Product features') with 0 text inside."),
    ("Critically Thin Product Descriptions (< 20 Words)", "Critical", "https://makemealabel.com/products/*", "Product detail pages contain a single 15-word sentence with zero technical specs, adhesive type, temperature rating, or application guidelines."),
    ("E-Commerce PDP Usability Friction: No Standard 'Add to Cart' CTA", "High", "https://makemealabel.com/products/*", "PDP replaces standard Buy button with B2B quick-order list table requiring +/- clicks and subtle 'View cart' links, causing conversion abandonment."),
    ("Missing UK B2B VAT Pricing Breakdown", "High", "Site-wide", "B2B customers cannot see ex-VAT / inc-VAT price breakdown or company VAT number. Label rolls are purchased by businesses requiring tax receipts."),
    ("Missing Volume Discount / Bulk Pricing Visual Tables", "High", "https://makemealabel.com/products/*", "No tier discount badges or savings breakdown tables (e.g. Save 15% on 4+ rolls, Save 25% on 12+ rolls) to incentivize higher AOV."),
    ("Zero Customer Reviews or Star Ratings Across Entire Store", "High", "Site-wide", "No review widget (Judge.me, Loox, Trustpilot) installed; zero social proof or testimonials to build transactional confidence."),
    ("Incomplete Product Schema Markup (Missing SKU, GTIN, Barcode)", "High", "https://makemealabel.com/products/*", "Product JSON-LD lacks SKU, GTIN/EAN, and AggregateRating, disqualifying listings from Google Shopping rich results and Merchant Center."),
    ("Zero Breadcrumb Navigation & BreadcrumbList Schema on PDPs", "Medium", "https://makemealabel.com/products/*", "PDPs lack clickable hierarchical breadcrumbs (Home > Roll Labels > Direct Thermal) and BreadcrumbList schema."),
    ("Oversized Images Up to 3.2 MB & 167 Images Missing Alt Text", "High", "Site-wide", "80 images exceed 100KB, with banner PNGs reaching 3,235 KB. 167 image instances have missing or empty alt text."),
    ("Customer-Hostile Shipping Policy Lacking Rates, Times & Couriers", "Medium", "https://makemealabel.com/policies/shipping-policy", "Shipping policy is 100% legal liability disclaimers with zero delivery times, delivery fees, free delivery thresholds, or courier names."),
    ("Missing Printer Compatibility Matrix on Product Detail Pages", "High", "https://makemealabel.com/products/*", "Thermal roll products omit compatible printer models (Zebra, Citizen, TSC, Brother), missing out on high-intent printer search queries."),
    ("Typo in Core Product Titles and URLs ('100m' & Feet Symbol '4'')", "Medium", "https://makemealabel.com/products/100mm-x-100m-4-by-4-direct-thermal-roll-labels", "Title and slug contain '100m' (meters) instead of '100mm', and use '4'' by 4''' (feet) instead of inches (4\" x 4\")."),
    ("Missing Security Headers on Production Edge", "Medium", "Site-wide", "Missing Referrer-Policy and uniform Content-Security-Policy across resources."),
    ("Zero AI-Search Optimization & Low Entity Authority", "Medium", "Site-wide", "Semrush shows 0 AI citations worldwide and AS 2. Lack of technical tabular specifications and entity signals prevents AI search engines from referencing the store."),
    ("Mobile Quick-Order Table Usability Squeeze", "Medium", "https://makemealabel.com/products/*", "Quick-order list table is heavily compressed on mobile viewports; no sticky Add to Cart bar exists on mobile scroll.")
]

with open(issues_file, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(["Issue Title", "Severity", "Affected URLs", "Observed Defect & Impact"])
    w.writerows(issues_data)

print(f"[+] Created {issues_file}")

# 08_keyword_map.csv
kw_file = os.path.join(out_dir, "08_keyword_map.csv")
kw_data = [
    ("Direct Thermal Roll Labels", "direct thermal labels, direct thermal roll labels uk, 4x6 thermal labels, thermal shipping labels", "https://makemealabel.com/collections/direct-thermal-roll-labels-blank", "Commercial / Transactional"),
    ("Thermal Transfer Labels", "thermal transfer roll labels, thermal transfer labels uk, barcode ribbon labels, thermal transfer printable labels", "https://makemealabel.com/collections/thermal-transfer-roll-labels-blank", "Commercial / Transactional"),
    ("Custom Printed Labels", "custom printed labels uk, personalized roll labels, custom product stickers leicester, branded packaging labels", "https://makemealabel.com/collections/custom-printed-labels", "Commercial / Transactional"),
    ("A4 Sheet Labels", "a4 sheet labels, printable a4 sticky labels, laser inkjet address labels a4, blank sheet stickers uk", "https://makemealabel.com/pages/sheet-labels", "Commercial / Transactional"),
    ("Zebra Compatible 4x6 Shipping Labels", "zebra 4x6 thermal labels, 100mm x 150mm shipping labels, royal mail thermal labels, courier 4x6 label rolls", "https://makemealabel.com/products/100mm-x-152mm-6-by-4-direct-thermal-roll-labels", "Transactional / B2B"),
    ("Label Manufacturing Leicester UK", "label manufacturer leicester, label printing company uk, roll label supplier midlands, custom stickers leicester", "https://makemealabel.com/", "Local & Commercial")
]

with open(kw_file, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(["Target Cluster", "Target Keywords (UK Market)", "Target URL", "Search Intent"])
    w.writerows(kw_data)

print(f"[+] Created {kw_file}")

# 10_roadmap_30_60_90.md
rm_file = os.path.join(out_dir, "10_roadmap_30_60_90.md")
with open(rm_file, 'w', encoding='utf-8') as f:
    f.write("""# Make Me A Label — 30-60-90 Day SEO & E-Commerce Growth Roadmap

## Phase 1: Emergency Technical & PDP Cleanup (Days 1–15)
- [ ] Fix Liquid translation missing bug on paginated collection and blog pages (`en.general.meta.page`).
- [ ] Add explicit text `<h1>` to homepage and all primary collection pages (`/collections/*`).
- [ ] Remove empty clothing theme demo accordions ("Materials and care", "Merchandising tips") from PDPs.
- [ ] Add high-converting primary "Add to Cart" button above the fold on all product pages alongside the quick-order list.
- [ ] Correct title and URL typos (change `100m` to `100mm`, replace feet marks `4'` with inches `4"`).
- [ ] Add explicit ex-VAT and inc-VAT pricing indicators across all product pages.
- [ ] Compress top 80 oversized PNG images to optimized WebP/JPEG format (reducing file sizes by 75-85%).

## Phase 2: E-Commerce Content & Conversion Architecture (Days 16–45)
- [ ] Expand product descriptions to 250+ words with technical specs (core diameter, adhesive type, temperature range, liner).
- [ ] Add a Printer Compatibility Matrix (Zebra, Citizen, TSC, Brother, Dymo) to all relevant thermal roll PDPs.
- [ ] Install customer review app (e.g. Judge.me or Loox) and solicit verified B2B buyer reviews.
- [ ] Re-write customer-friendly UK Shipping Policy detailing dispatch cut-offs (e.g. "Order by 2pm for same-day dispatch"), delivery fees, and courier partners (DPD / Royal Mail).
- [ ] Deploy complete Product Schema (`@type: Product`) with SKU, GTIN/EAN barcodes, offers, and breadcrumb navigation.
- [ ] Add visual bulk pricing / volume tier discount tables showing cost-per-roll savings.

## Phase 3: Category Expansion & B2B Commercial Scaling (Days 46–90)
- [ ] Build dedicated high-intent landing pages for "Zebra Compatible Shipping Labels" and "Royal Mail 4x6 Thermal Labels".
- [ ] Launch an interactive "Label Finder" tool (select by printer brand, size, or material).
- [ ] Pursue B2B industry citations and local Leicester business directory listings (Yell, Scoot, UK Small Business directories).
- [ ] Deploy FAQPage and LocalBusiness schema markup for Leicester manufacturing facility.

## Phase 4: Field Verification & Conversion Rescoring (Days 90+)
- [ ] Analyze Chrome User Experience Report (CrUX) field performance for LCP, INP, and CLS under live user traffic.
- [ ] Review Google Merchant Center approval status for rich product snippets.
- [ ] Re-score domain health score out of 100 and evaluate UK organic search rankings.
""")

print(f"[+] Created {rm_file}")
print("Audit artifacts created successfully!")
