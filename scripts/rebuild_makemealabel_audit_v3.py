import os
import json
import csv
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from playwright.sync_api import sync_playwright

out_dir = r"website audit/makemealabel.com"
os.makedirs(out_dir, exist_ok=True)

audit_data = {
    "client_name": "Make Me A Label",
    "domain": "https://makemealabel.com/",
    "primary_service": "https://makemealabel.com/collections/direct-thermal-roll-labels-blank",
    "core_offering": "UK Label Manufacturer — Direct Thermal, Thermal Transfer & Custom Printed Roll Labels",
    "technology_stack": "Shopify (Dawn Theme) on Cloudflare CDN / Edge",
    "audit_date": "October 16, 2026 (Empirically Verified)",
    "domain_authority_summary": "Semrush AS 2 | UK Organic Keywords: 1 | Ref. Domains: 1.2K | UK AI Visibility: 14",
    "health_score": 42,
    "badge_text": "UK E-Commerce & Technical SEO Audit",
    "report_title": "TECHNICAL SEO & E-COMMERCE AUDIT REPORT",
    "meta_items": [
        ("Target Website:", "https://makemealabel.com/"),
        ("Primary Product Focus:", "https://makemealabel.com/collections/direct-thermal-roll-labels-blank"),
        ("Business Type & Market:", "Label Manufacturer & Direct-to-Consumer/B2B Supplier | Leicester, UK (Co. 13161985)"),
        ("E-Commerce Platform:", "Shopify (Dawn Theme) on Cloudflare Global Edge"),
        ("Audit Date:", "October 16, 2026"),
        ("Technical Health Rubric Score:", "42 / 100 (Internal Agency Diagnostic Rubric — Remediation Required)")
    ],
    "executive_summary": [
        {
            "bold_prefix": "Executive Context: ",
            "text": "Make Me A Label (makemealabel.com) is an online UK-based label manufacturing business located in Leicester (Company Registration No. 13161985, 3 Sylvan Avenue, LE5 3SN). The business manufactures and converts direct thermal roll labels, thermal transfer rolls, sheet labels, and custom printed packaging stickers for UK commercial, warehouse, and retail clients. While utilizing Shopify with Cloudflare edge caching, the store currently registers negligible organic search traffic in the UK and exhibits significant on-page technical defects, e-commerce conversion friction, and an unexamined backlink footprint."
        },
        {
            "bold_prefix": "Verified Tool Baseline (Semrush Oct 15, 2026): ",
            "text": "Authority Score: 2 / 100 ('Lacks organic traffic'). UK Organic Traffic: 0 visits/mo (Paid Traffic: 0). UK Organic Keywords: 1 (-50%). Worldwide Organic Keywords: 6. Inbound Links: 1,200 Referring Domains | 1,500 Backlinks. AI Search Visibility: 14 in the UK (with 4 mentions in ChatGPT and 0 cited pages); 0 AI Visibility Worldwide (with 1 cited page in Google AI Mode, 0 in ChatGPT/Gemini). Note: Third-party databases frequently undercount small B2B product catalogs; Google Search Console (GSC) must be integrated to inspect true UK search impression volume."
        },
        {
            "bold_prefix": "Screaming Frog Crawl & Live Technical Verification: ",
            "text": "The crawl evaluated 258 total URLs, identifying 58 HTML pages (27 Products, 7 Collections, 10 Blog URLs, 5 Policies, 4 Pages, and 5 System routes). Technical inspection identified severe URL slug/title dimensional mismatches (e.g. 58x60 slug delivering 58x40 product), eight key pages missing H1 tags entirely, a Shopify Liquid translation error appearing in paginated title tags, blog articles with mismatched commercial titles, 47 images missing alt text, and uncompressed PNG hero images up to 3.2 MB."
        }
    ],
    "scorecard": [
        ["Crawlability & Sitemaps", "10", "8 / 10", "Pass", "Valid Shopify XML sitemaps for products, collections, pages, and blogs."],
        ["Indexability & Canonicals", "10", "7 / 10", "Pass", "Self-referencing canonicals active; page 1 pagination properly canonicalized."],
        ["URL Architecture & Accuracy", "10", "2 / 10", "Critical", "Severe product slug vs title mismatches (e.g. 58x60 slug delivering 58x40)."],
        ["Heading Structure (H1/H2)", "10", "2 / 10", "Critical", "Missing H1s on 4 primary collections and 4 main landing pages (8 total)."],
        ["On-Page Metadata & Liquid", "10", "3 / 10", "Critical", "Liquid translation missing error in SERP titles; blog titles misaligned with posts."],
        ["Product Page (PDP) Depth", "10", "3 / 10", "Critical", "Unique copy ~15 words; empty apparel demo accordions active on PDPs."],
        ["Conversion UX & Pricing", "10", "4 / 10", "Warning", "Bundle savings uncalculated; quick-order table lacks primary Add to Cart CTA."],
        ["Structured Data (Schema)", "10", "3 / 10", "Warning", "Product schema omits SKU, GTIN, and reviews; no BreadcrumbList markup."],
        ["Media & Performance", "10", "4 / 10", "Warning", "47 images missing alt text; hero PNGs up to 3.2MB require WebP compression."],
        ["Backlink & Trust Profile", "10", "6 / 10", "Warning", "1.2K ref domains with AS 2 indicates low link quality; shipping policy lacks rates."],
        ["DIAGNOSTIC RUBRIC SCORE", "100", "42 / 100", "Remediation Required", "Shopify Theme Fixes, PDP Specs & Backlink Audit Required"]
    ],
    "issues": [
        {
            "title": "Product URL Slug and Heading Dimensional Mismatches",
            "severity": "Critical",
            "urls": "https://makemealabel.com/products/copy-of-58mm-x-60mm-direct-thermal-roll-labels, https://makemealabel.com/products/57mm-x-70mm-direct-thermal-roll-labels",
            "impact": "Multiple products possess severe discrepancies between their URL slugs and actual titles/H1s: the slug 'copy-of-58mm-x-60mm-...' displays a '58mm x 40mm' label, while '57mm-x-70mm-direct-thermal-roll-labels' displays a '57mm x 90mm' label (whereas the '-1' variant displays 57mm x 70mm). This risks sending buyers to incorrect label sizes, resulting in high return rates and eroded trust."
        },
        {
            "title": "Missing H1 Headings on Primary Collections and Core Landing Pages",
            "severity": "Critical",
            "urls": "https://makemealabel.com/collections/direct-thermal-roll-labels-blank, /thermal-transfer-roll-labels-blank, /custom-printed-labels, /frontpage, /pages/sheet-labels, /pages/roll-labels, /pages/about-us, /pages/contact",
            "impact": "Screaming Frog identifies 8 pages lacking an <h1> tag entirely. The 4 primary commercial collection pages and 4 key landing pages omit <h1>{{ collection.title }}</h1> or page titles, depriving search engines of primary topical signals for major commercial queries."
        },
        {
            "title": "Shopify Liquid Translation Bug Displaying in Search Snippet Titles",
            "severity": "Critical",
            "urls": "https://makemealabel.com/collections/all?page=2, https://makemealabel.com/blogs/news?page=2",
            "impact": "Paginated collection and blog pages output raw template missing text in their <title> tags: 'Products Translation missing: en.general.meta.page'. This configuration error displays directly in Google search snippets, depressing organic click-through rates."
        },
        {
            "title": "Homepage H1 Restricted to Header Logo Image With Zero Textual Heading",
            "severity": "High",
            "urls": "https://makemealabel.com/",
            "impact": "The homepage <h1> tag wraps solely the header logo <a><img></a> element with alt text 'Make me a Label'. The page completely lacks a keyword-optimized text heading, despite the title tag targeting 'Label Manufacturing Company in Leicester'."
        },
        {
            "title": "Apparel Theme Demo Accordions Displayed on Industrial Label PDPs",
            "severity": "High",
            "urls": "https://makemealabel.com/products/* (Site-wide on PDPs)",
            "impact": "Product detail pages display default Shopify Dawn apparel demo accordion headers ('Materials and care', 'Merchandising tips', 'Product features') that contain completely empty bodies, presenting an unfinished impression to B2B procurement managers."
        },
        {
            "title": "Brief Unique Product Description Copy (~15 Words)",
            "severity": "High",
            "urls": "https://makemealabel.com/products/* (All 27 products)",
            "impact": "While total page word count reaches 240–530 words due to theme, navigation, and drawer text, unique product description copy is limited to a single 15-word line. Pages lack technical specifications, adhesive grades (permanent vs removable), liner types, operating temperature ranges, and application use cases."
        },
        {
            "title": "B2B Tiered Bundle Savings Uncalculated and Misleadingly Labelled",
            "severity": "High",
            "urls": "https://makemealabel.com/products/*",
            "impact": "Tiered volume options exist (e.g. 100x152mm is £9.99 for 1 roll, £27.99 for 4 [~30% discount/roll], £119.99 for 24 [~50% discount/roll]), but prices are labelled as '£27.99/ea' in the quick-order table rather than per bundle, and percentage savings are never highlighted. Furthermore, tier increments are inconsistent across products (1/4/12/24 vs 3/8/16/32/64)."
        },
        {
            "title": "Quick-Order Table Lacks Standard Above-the-Fold 'Add to Cart' CTA",
            "severity": "High",
            "urls": "https://makemealabel.com/products/*",
            "impact": "The PDP replaces the conventional single 'Add to Cart' button with a multi-row quick-order list table requiring shoppers to use +/- buttons and locate a small 'View cart' link. This unconventional UX creates friction for single-roll buyers and suffers severe horizontal compression on mobile viewports."
        },
        {
            "title": "Blog Title Tags Misaligned With Article Content",
            "severity": "Medium",
            "urls": "https://makemealabel.com/blogs/news/*",
            "impact": "Multiple informational blog posts have commercial e-commerce title tags assigned. For example, 'The Science Behind Thermal Transfer Roll Labels! (How It Lasts?)' has the title 'Top Thermal Transfer Roll Labels Suppliers – Make Me a Label', creating an intent mismatch that limits ranking potential."
        },
        {
            "title": "Disproportionate Backlink Profile Indicating Low-Quality Inbound Links",
            "severity": "High",
            "urls": "Domain-level (Off-Page)",
            "impact": "Semrush records 1,200 referring domains and 1,500 backlinks against an Authority Score of only 2. This severe discrepancy strongly indicates that the vast majority of inbound links originate from low-quality scrapers, directory spam, or discounted networks. A link audit is required before investing in outreach."
        },
        {
            "title": "Oversized PNG Hero Assets and 47 Images Missing Alt Text",
            "severity": "Medium",
            "urls": "Site-wide (80 images > 100KB)",
            "impact": "Screaming Frog flags 47 images with missing alt text across product and collection templates. Additionally, 80 images exceed 100KB, with desktop hero PNG banners reaching up to 3,235 KB (3.2 MB), creating an avoidable Largest Contentful Paint (LCP) performance bottleneck on mobile networks."
        },
        {
            "title": "Incomplete Product Schema Markup (Missing SKU, GTIN, and Reviews)",
            "severity": "Medium",
            "urls": "https://makemealabel.com/products/*",
            "impact": "The @type: Product JSON-LD schema omits 'sku', 'gtin13/barcode', 'mpn', and review properties. This prevents listings from securing enhanced Google Shopping search results and Free Merchant Center listings."
        },
        {
            "title": "Missing UK B2B VAT Breakdown (ex-VAT vs inc-VAT)",
            "severity": "Medium",
            "urls": "Site-wide",
            "impact": "Product pages state only 'Tax included. Shipping calculated at checkout'. UK corporate purchasers (logistics, fulfillment centers, retail) require transparent '£X.XX ex. VAT / £Y.YY inc. VAT' pricing and visible VAT registration numbers on invoices."
        },
        {
            "title": "Missing Printer Compatibility Matrix on Thermal Roll PDPs",
            "severity": "Medium",
            "urls": "https://makemealabel.com/products/*",
            "impact": "Thermal roll listings omit compatible desktop and industrial printer models (Zebra ZD420/GK420d, Citizen CL-S521, TSC, Brother, Dymo 4XL), failing to capture high-intent commercial queries like 'Zebra compatible 4x6 thermal shipping labels'."
        },
        {
            "title": "Shipping Policy Formatted as Legal Disclaimers Lacking Delivery Information",
            "severity": "Low",
            "urls": "https://makemealabel.com/policies/shipping-policy",
            "impact": "The shipping policy consists of 404 words of legal liability disclaimers with zero delivery timescales, standard/express rates, free shipping thresholds, dispatch cut-off hours, or courier partner details (Royal Mail, DPD)."
        },
        {
            "title": "Absence of Verified Customer Reviews or Social Proof",
            "severity": "Medium",
            "urls": "Site-wide",
            "impact": "Zero customer reviews or star ratings exist across all 27 products. No review integration (e.g. Judge.me, Loox, Trustpilot) is installed, leaving the store without third-party validation."
        },
        {
            "title": "Metadata Hygiene: Missing Descriptions and Length Issues",
            "severity": "Low",
            "urls": "Site-wide (Screaming Frog Overview)",
            "impact": "Screaming Frog records 11 pages with missing meta descriptions, 3 duplicated descriptions, 6 page titles exceeding 60 characters / 561 pixels, and 12 titles below 30 characters."
        },
        {
            "title": "Pagination Sequence and Non-Indexable Warnings",
            "severity": "Low",
            "urls": "https://makemealabel.com/collections/all?page=1, https://makemealabel.com/blogs/news?page=1",
            "impact": "Screaming Frog flags 2 non-indexable pagination URLs and 2 pagination sequence warnings associated with canonicalized page 1 parameters."
        }
    ],
    "scope_of_improvement": [
        {
            "bold_prefix": "1. Search Visibility & First-Party Data Integration: ",
            "text": "Integrating Google Search Console (GSC) and GA4 to analyze true UK search impression data, indexed URL counts, and query performance, moving beyond third-party database estimates. Conducting structured keyword research against established UK competitors (Label Planet, Priory Direct, Cloud Labels)."
        },
        {
            "bold_prefix": "2. Technical Governance & URL Architecture: ",
            "text": "Correcting misleading product URL slugs (e.g. 58x60 slug delivering 58x40 labels) with 301 redirects, eliminating the Shopify Liquid translation missing error from title tags, and restoring proper <h1> elements across the 4 key collections and 4 main landing pages."
        },
        {
            "bold_prefix": "3. Product Page (PDP) Re-architecture: ",
            "text": "Expanding unique product copy to 250+ words covering material specifications, adhesive grades (permanent acrylic vs removable), operating temperature ranges, and a structured printer compatibility matrix (Zebra, Citizen, TSC, Brother, Dymo)."
        },
        {
            "bold_prefix": "4. E-Commerce Pricing Transparency & Conversion Optimization: ",
            "text": "Providing clear ex-VAT and inc-VAT dual pricing, correcting the '/ea' bundle label on quick-order tables, clearly communicating tiered savings (e.g. 'Save 30% — £7.00/roll for 4 rolls'), and providing a prominent primary 'Add to Cart' button above the fold."
        },
        {
            "bold_prefix": "5. Off-Page Hygiene & Google Shopping Expansion: ",
            "text": "Performing a forensic backlink audit to examine the 1,200 referring domains against Semrush Authority Score 2, preparing disavow submissions if toxic link footprints exist, and submitting a structured product feed to Google Merchant Center for Free Product Listings."
        }
    ],
    "immediate_fixations": [
        "Correct Product URL Slug Mismatches: Remap 'copy-of-58mm-x-60mm-...' (58x40 product) and '57mm-x-70mm-...' (57x90 product) to accurate slugs with 301 redirects.",
        "Resolve Shopify Liquid Translation Bug in Titles: Remove 'Translation missing: en.general.meta.page' appearing on paginated collection and blog pages.",
        "Deploy <h1> Headings on Collections and Landing Pages: Add styled <h1> headings across the 4 key collections and 4 landing pages (8 pages total).",
        "Replace Homepage Logo-Only <h1> With Text Heading: Move the logo out of the primary <h1> tag and introduce a descriptive text heading ('UK Manufacturer of Thermal Roll & Custom Printed Labels').",
        "Purge Empty Apparel Demo Accordions From PDPs: Remove the default Dawn theme demo sections ('Materials and care', 'Merchandising tips') from the product template.",
        "Add Prominent Primary 'Add to Cart' CTA Above the Fold: Provide a clear, standard purchase button alongside the B2B quick-order list table.",
        "Display Clear Tiered Bundle Savings: Clarify the quick-order table by showing bundle pricing, per-roll unit cost, and percentage discount.",
        "Compress Desktop Hero PNG Banners to WebP: Optimize the top 80 oversized images (with hero images reaching 3.2 MB) to improve mobile LCP.",
        "Add Missing Alt Text to 47 Images: Populate descriptive alt text across the 47 image instances flagged by Screaming Frog.",
        "Align Blog Post Titles With Content: Replace generic commercial 'Shop...' titles with topic-accurate titles matching the informational articles."
    ],
    "roadmap": [
        {
            "phase": "Phase 1: Emergency Technical & Theme Cleanup\n(Days 1–15)",
            "objectives": "Correct product URL slug mismatches with 301 redirects, fix Liquid translation bug in titles, restore 8 missing collection/landing H1s, purge empty apparel accordions, and compress oversized hero PNGs.",
            "milestone": "0 Liquid template bugs in SERPs; correct product slugs; valid collection H1s deployed"
        },
        {
            "phase": "Phase 2: E-Commerce Content & Conversion Architecture\n(Days 16–45)",
            "objectives": "Expand PDP descriptions to 250+ words with technical specs, add printer compatibility matrices (Zebra, Citizen, TSC), deploy ex-VAT/inc-VAT pricing, install customer review integration (Judge.me/Loox), and rewrite customer-facing shipping policy.",
            "milestone": "Google Product Rich Snippets active; review social proof established; shipping policy updated"
        },
        {
            "phase": "Phase 3: Backlink Audit & Google Merchant Center\n(Days 46–90)",
            "objectives": "Conduct forensic backlink audit of 1.2K referring domains (preparing disavow if necessary), deploy Google Merchant Center product feed for Free Shopping listings, build dedicated printer-model landing pages, and benchmark UK competitors (Label Planet, Priory Direct).",
            "milestone": "Merchant Center feed approved; backlink toxicity reviewed; targeted B2B landing pages live"
        },
        {
            "phase": "Phase 4: Field Verification & Measurement Pass\n(Days 90+)",
            "objectives": "Review first-party Google Search Console click and impression data, evaluate PageSpeed Insights field CrUX data for Core Web Vitals (LCP, INP, CLS), track AI search citations in ChatGPT/Perplexity, and re-evaluate technical health rubric.",
            "milestone": "GSC keyword traction verified; measured field performance; expanded commercial visibility"
        }
    ]
}

# 1. Save updated audit_data.json
json_path = os.path.join(out_dir, "audit_data.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(audit_data, f, indent=2)
print(f"[+] Updated audit_data.json saved: {json_path}")

# 2. Update 04_issues_log.csv
issues_file = os.path.join(out_dir, "04_issues_log.csv")
with open(issues_file, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(["Issue Title", "Severity", "Affected URLs", "Observed Defect & Impact"])
    for iss in audit_data["issues"]:
        w.writerow([iss["title"], iss["severity"], iss["urls"], iss["impact"]])
print(f"[+] Updated 04_issues_log.csv saved: {issues_file}")

# 3. Update 10_roadmap_30_60_90.md
rm_file = os.path.join(out_dir, "10_roadmap_30_60_90.md")
with open(rm_file, 'w', encoding='utf-8') as f:
    f.write("""# Make Me A Label — 30-60-90 Day SEO & E-Commerce Growth Roadmap (Revised)

## Phase 1: Emergency Technical & Theme Cleanup (Days 1–15)
- [ ] Correct product URL slug mismatches: 301 redirect `copy-of-58mm-x-60mm-...` (58x40 product) and `57mm-x-70mm-...` (57x90 product).
- [ ] Fix Liquid translation missing bug on paginated collection and blog pages (`en.general.meta.page`).
- [ ] Deploy styled `<h1>` headings across the 4 key commercial collections and 4 main landing pages (8 pages total).
- [ ] Move header logo out of homepage `<h1>` and introduce a descriptive text heading.
- [ ] Remove empty apparel demo accordions ("Materials and care", "Merchandising tips") from product template.
- [ ] Add prominent primary "Add to Cart" CTA above the fold alongside the quick-order list.
- [ ] Clarify tiered bundle pricing (displaying bundle total, per-roll unit cost, and percentage discount).
- [ ] Compress desktop hero PNG images (up to 3.2 MB) to modern WebP format.
- [ ] Add descriptive alt text across the 47 images flagged by Screaming Frog.
- [ ] Re-align blog title tags to reflect informational article topics rather than generic commercial strings.

## Phase 2: E-Commerce Content & Conversion Architecture (Days 16–45)
- [ ] Expand unique product descriptions to 250+ words covering material specifications, adhesive grades, core sizes, and liner types.
- [ ] Add a structured Printer Compatibility Matrix (Zebra, Citizen, TSC, Brother, Dymo) on all relevant thermal roll PDPs.
- [ ] Deploy dual pricing display showing clear ex-VAT and inc-VAT breakdowns and company VAT registration number.
- [ ] Install customer review integration (e.g. Judge.me or Loox) and solicit verified buyer feedback.
- [ ] Rewrite shipping policy to clearly present delivery timescales, courier partners (Royal Mail / DPD), cut-off hours, and rates.
- [ ] Complete Product JSON-LD schema by adding SKU, GTIN/EAN barcodes, offers, and breadcrumb navigation.

## Phase 3: Backlink Audit & Google Merchant Center (Days 46–90)
- [ ] Conduct forensic backlink audit to evaluate 1,200 referring domains against Authority Score 2; submit disavow file if toxic links are found.
- [ ] Set up Google Merchant Center product feed to capture high-converting Free Product Listings on the Google Shopping tab.
- [ ] Build dedicated high-intent landing pages for "Zebra 4x6 Shipping Labels" and "Royal Mail Thermal Labels".
- [ ] Benchmark organic search performance against UK competitors (Label Planet, Priory Direct, Cloud Labels).

## Phase 4: Field Verification & Measurement Pass (Days 90+)
- [ ] Review Google Search Console (GSC) performance data for true UK search impressions, clicks, and indexed URLs.
- [ ] Evaluate real-user Core Web Vitals (LCP, INP, CLS) in PageSpeed Insights once traffic data populates.
- [ ] Track brand citations and technical accuracy across AI search platforms (ChatGPT, Perplexity, Google AI Overviews).
- [ ] Re-evaluate internal technical health rubric score.
""")
print(f"[+] Updated 10_roadmap_30_60_90.md saved: {rm_file}")

# 4. Generate Reports
from generate_issue_only_report_engine import build_docx_report, build_pdf_report

docx_path = os.path.join(out_dir, "MakeMeALabel_SEO_Audit_Report.docx")
build_docx_report(audit_data, docx_path)

pdf_path = os.path.join(out_dir, "MakeMeALabel_SEO_Audit_Report.pdf")
build_pdf_report(audit_data, pdf_path)

# Mirror to root
import shutil
shutil.copyfile(docx_path, "MakeMeALabel_SEO_Audit_Report.docx")
shutil.copyfile(pdf_path, "MakeMeALabel_SEO_Audit_Report.pdf")
print("[+] Mirrored updated reports to root successfully!")
