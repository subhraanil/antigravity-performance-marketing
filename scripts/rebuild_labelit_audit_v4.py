import os
import json
import csv
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import shutil

out_dir = r"website audit/labelitsolutions.co.uk"
os.makedirs(out_dir, exist_ok=True)

# 1. Prepare fully reconciled audit_data payload
audit_data = {
    "client_name": "Label IT Solutions",
    "domain": "https://labelitsolutions.co.uk/",
    "primary_service": "https://labelitsolutions.co.uk/product-category/direct-thermal/",
    "core_offering": "UK Label Manufacturer — Direct Thermal, Thermal Transfer, Sheet Labels & Cores",
    "technology_stack": "WordPress 7.1.3 (WooCommerce 10.3.8 + Elementor 3.33.3) on Apache Web Server",
    "audit_date": "October 16, 2026 (Crawled & Lab-Tested)",
    "domain_authority_summary": "Semrush AS 6 | Moz DA 2 | UK Keywords: 8 | Ref. Domains: 189 | Mobile PSI: 47/100 (LCP 16.5s)",
    "health_score": 20,
    "badge_text": "UK E-Commerce, WordPress SEO & Technical Audit",
    "report_title": "TECHNICAL SEO & E-COMMERCE AUDIT REPORT",
    "meta_items": [
        ("Target Website:", "https://labelitsolutions.co.uk/"),
        ("Primary Product Focus:", "https://labelitsolutions.co.uk/product-category/direct-thermal/"),
        ("Business Type & Market:", "Label Manufacturer & B2B/DTC Supplier | Leicester, UK (Co. 15776706, VAT GB474015505)"),
        ("E-Commerce Platform:", "WordPress (WooCommerce 10.3.8 + Elementor 3.33.3) on Apache"),
        ("Audit Date:", "October 16, 2026"),
        ("Technical Health Rubric Score:", "20 / 100 (Internal Agency Diagnostic Rubric — Critical Remediation Required)")
    ],
    "executive_summary": [
        {
            "bold_prefix": "Executive Context: ",
            "text": "Label IT Solutions (labelitsolutions.co.uk), operated by Label It Ltd (Company Registration No. 15776706, VAT GB474015505, 3 Sylvan Avenue, Leicester, LE5 3SN, United Kingdom), manufactures direct thermal roll labels, thermal transfer rolls, A4 sheet labels, integrated courier labels, cardboard cores, and printer consumables. The store operates on WordPress with WooCommerce and Elementor on an Apache server. While the product catalog is commercially viable, the store registers negligible organic search visibility in the UK, suffers from severe canonical and heading structure deficits, extensive taxonomy index bloat, missing product schema, and severe mobile latency."
        },
        {
            "bold_prefix": "Verified Tool Baseline (Semrush & Moz, Oct 15–16, 2026): ",
            "text": "Semrush Authority Score: 6 / 100 ('Low authority'). UK Organic Traffic: 3 visits/mo (Paid Traffic: 0). UK Organic Keywords: 8 (-20%). Worldwide Organic Keywords: 19 (-5%). 100% of organic traffic is driven solely by brand navigational queries ('labelit' - Pos 3, Vol 140; 'label it' - Pos 10, Vol 260), while commercial terms sit outside page 4 ('label it printer' - Pos 51; 'label solutions' - Pos 44). Inbound Links: 189 Referring Domains | 253 Backlinks. Moz Pro: Domain Authority 2 / 100, Brand Authority 1 / 100, Page Authority 22 / 100 (Dominant search theme: 'Custom Label Solutions'). AI Search Visibility: 0 worldwide and UK across ChatGPT, Google AI Overviews, Google AI Mode, and Gemini."
        },
        {
            "bold_prefix": "Google PageSpeed Insights Lab Baseline (Oct 16, 2026): ",
            "text": "Lighthouse lab analysis identifies severe mobile performance bottlenecks: Mobile Performance Score: 47 / 100 (Red / Fail). Mobile Largest Contentful Paint (LCP) reaches 16.5 seconds (against the Google <= 2.5s threshold), and First Contentful Paint (FCP) lags at 6.3 seconds. Total network payload is 4,912 KiB (~4.9 MB). Crucially, 3,769 KiB (~3.8 MB) of static assets lack browser cache lifetimes due to missing Apache mod_expires configuration, 1,060 ms of latency is driven by render-blocking resources, and 1,090 KiB of unused JavaScript and CSS blocks the main thread for 2.9 seconds. Server HTML response time (TTFB) averages 1.77 seconds (1.48s–2.42s). Desktop performance achieves 70 / 100 (FCP 1.2s, LCP 3.1s)."
        },
        {
            "bold_prefix": "Screaming Frog Crawl Verification: ",
            "text": "The crawl evaluated 214 total URLs: 201 returning HTTP 200, 11 returning HTTP 301, and 2 returning HTTP 404. Exactly 200 URLs are indexable; 14 are non-indexable. Deep technical inspection revealed that 99.5% of pages (200 of 201) lack canonical tags entirely, 122 indexable pages lack <h1> headings (97 attribute archives, 17 category URLs, and 8 core pages), 97 thin WooCommerce attribute archives are indexed, 100% of products (71/71) lack @type: Product schema, no OpenGraph tags exist, and the homepage title is only 8 characters ('Label IT') with no meta description."
        }
    ],
    "scorecard": [
        ["Crawlability & Sitemaps", "10", "5 / 10", "Warning", "Default WP sitemap indexes empty taxonomies; 11 internal 301s (slashes & HTTP)."],
        ["Indexability & Canonicals", "10", "1 / 10", "Critical", "Missing canonical tags on 200 of 201 URLs (99.5%); zero self-referencing canonicals."],
        ["Taxonomy & Index Hygiene", "10", "1 / 10", "Critical", "97 thin WooCommerce attribute archives indexed across 10 taxonomies."],
        ["Heading Structure (H1/H2)", "10", "2 / 10", "Critical", "122 indexable pages missing <h1>; 100% of commercial categories use <h2> for titles."],
        ["Metadata & Snippet Quality", "10", "2 / 10", "Critical", "Homepage title only 8 chars; 131 pages missing meta descriptions; 54 duplicates."],
        ["Structured Data (Schema)", "10", "1 / 10", "Critical", "Zero @type: Product schema across all 71 products; only basic breadcrumb present."],
        ["Social & Graph Metadata", "10", "0 / 10", "Fail", "Zero OpenGraph (og:*) and zero Twitter Card tags deployed site-wide."],
        ["Product Page (PDP) Depth", "10", "3 / 10", "Critical", "No Description tab (71/71 products start with 'Additional info' H2); 0 reviews."],
        ["Speed & Core Web Vitals", "10", "2 / 10", "Critical", "Mobile Score 47/100; LCP 16.5s; Avg TTFB 1.77s; 4.9MB payload; 3.8MB un-cached."],
        ["Server Hygiene & Security", "10", "3 / 10", "Warning", "Apache server lacks HSTS/CSP/X-Frame-Options; 73 protocol-relative links."],
        ["DIAGNOSTIC RUBRIC SCORE", "100", "20 / 100", "Critical Remediation Required", "Ten 10-point categories derived strictly from crawl, lab speed, and live inspection."]
    ],
    "issues": [
        {
            "title": "Complete Absence of Canonical Tags Across 99.5% of Pages",
            "severity": "Critical",
            "urls": "Site-wide (200 of 201 URLs lack <link rel='canonical'>)",
            "impact": "200 out of 201 HTML pages omit canonical tags. The website possesses zero self-referencing canonical tags, creating index dilution and canonical confusion across parameter URLs, trailing-slash variations, and HTTP/HTTPS variations."
        },
        {
            "title": "Severe Mobile Core Web Vitals Failure: 16.5s LCP, 1.77s Avg TTFB, and 4.9 MB Payload",
            "severity": "Critical",
            "urls": "https://labelitsolutions.co.uk/ (Google PageSpeed Insights & Crawl TTFB)",
            "impact": "Lighthouse records a Mobile Performance Score of 47/100 with an extreme 16.5-second LCP and 6.3-second FCP. Screaming Frog confirms average server response time (TTFB) is 1.77s (1.48s–2.42s). The 4.9 MB payload creates severe mobile bounce rates and conversion friction."
        },
        {
            "title": "Index Bloat: 97 Thin WooCommerce Attribute Taxonomy Archives Indexed",
            "severity": "Critical",
            "urls": "/label-length/ (28), /label-width/ (23), /labels-per-roll/ (16), /labels-per-sheet/ (13), /material/ (4), /printer-compatibility/ (4), /core-diameter-mm/ (3), /sheet-size/ (2), /adhesive-type/ (2), /label-shape/ (2)",
            "impact": "97 attribute archive pages across 10 taxonomies are indexable. These pages contain only automated duplicate product grids with zero unique descriptive copy (~128 words), fragmenting link equity, cannibalizing primary category rankings, and wasting crawl budget."
        },
        {
            "title": "100% of Commercial Product Categories Missing <h1> Headings",
            "severity": "Critical",
            "urls": "https://labelitsolutions.co.uk/product-category/* (12 base categories + 5 paginated archives)",
            "impact": "All commercial category hubs (/direct-thermal/, /thermal-transfer/, /sheet-labels/, etc.) lack an <h1> tag because the Elementor theme template hardcodes category titles inside <h2> tags, stripping primary topical signals from core landing pages."
        },
        {
            "title": "Complete Absence of @type: Product Structured Data Across All 71 Products",
            "severity": "Critical",
            "urls": "https://labelitsolutions.co.uk/product/* (All 71 products)",
            "impact": "Product detail pages output solely a basic BreadcrumbList JSON-LD block and omit Schema.org @type: Product, Offer, price, priceCurrency (GBP), availability, and SKU properties. This deprives listings of Google rich snippets (pricing badges, stock availability) and requires supplemental feeds for Google Merchant Center."
        },
        {
            "title": "Unconfigured Browser Caching on Apache Web Server (3.8 MB Un-Cached Payload)",
            "severity": "Critical",
            "urls": "Site-wide (Apache Server Header Configuration)",
            "impact": "PageSpeed Insights flags 3,769 KiB (~3.8 MB) of static CSS, JS, and image assets lacking efficient cache lifetimes (Cache-Control: max-age or Expires). Returning visitors and multi-page B2B shoppers are forced to re-download the entire 4.9 MB payload on every navigation."
        },
        {
            "title": "Minimal Homepage Title Tag (8 Characters) and Missing Meta Description",
            "severity": "Critical",
            "urls": "https://labelitsolutions.co.uk/",
            "impact": "The homepage <title> tag contains only 'Label IT' (8 characters / 71 pixels), completely failing to target primary commercial keywords ('Direct Thermal Labels UK', 'Thermal Transfer Rolls Manufacturer'). Additionally, the homepage has no meta description."
        },
        {
            "title": "Unpopulated Description Tab Across 100% of Products (71/71 Display 'Additional info' H2)",
            "severity": "High",
            "urls": "https://labelitsolutions.co.uk/product/* (All 71 products)",
            "impact": "While total page word counts reach 315–712 words due to template boilerplate, 100% of products (71/71) display an 'Additional information' <h2> as their very first content heading. This confirms that the primary WooCommerce 'Description' tab is completely unmounted or empty, leaving listings without editorial specifications, adhesive grades, or liner details."
        },
        {
            "title": "Duplicate Commercial Category Cannibalization: /a4-sheet-labels/ vs /sheet-labels/a4-sheet-labels/",
            "severity": "High",
            "urls": "https://labelitsolutions.co.uk/product-category/a4-sheet-labels/, https://labelitsolutions.co.uk/product-category/sheet-labels/a4-sheet-labels/",
            "impact": "Two distinct URLs share identical '<title>A4 Sheet Labels – Label IT</title>', identical heading hierarchies, and identical 369-word product grids. This creates direct internal keyword cannibalization that splits internal and external link equity."
        },
        {
            "title": "Render-Blocking Resource Latency and Unused Elementor/WooCommerce Code Bloat",
            "severity": "High",
            "urls": "https://labelitsolutions.co.uk/",
            "impact": "PageSpeed Insights identifies 1,060 ms of render-blocking requests. Furthermore, 687 KiB of unused JavaScript and 403 KiB of unused CSS (1,090 KiB total) from Elementor, Elementor Pro, and WooCommerce plugins load sitewide, tying up the browser main thread for 2.9 seconds across 10 long tasks."
        },
        {
            "title": "Widespread Missing & Duplicate Meta Descriptions (131 Missing, 54 Duplicate)",
            "severity": "High",
            "urls": "131 URLs missing; 54 URLs sharing duplicate snippets (56 of 71 products share 19 unique snippets)",
            "impact": "65.2% of the site lacks meta descriptions, including all 12 commercial categories. Furthermore, 54 URLs share duplicate snippets, causing Google to ignore them in search snippets."
        },
        {
            "title": "107 Truncated Page Titles Under 30 Characters (91 Attribute Archives + 16 Core Pages)",
            "severity": "High",
            "urls": "107 URLs site-wide",
            "impact": "Over 53% of all pages have truncated titles under 30 characters. While 91 are attribute archives, 16 core commercial hubs (including the homepage, shop, and 12 categories) fail to target primary UK search queries."
        },
        {
            "title": "Complete Absence of OpenGraph and Twitter Card Social Metadata",
            "severity": "Medium",
            "urls": "Site-wide (0 og:* and 0 twitter:* tags detected)",
            "impact": "The store has zero OpenGraph or Twitter Card meta tags installed. Links shared on LinkedIn, WhatsApp, or Twitter produce no rich media previews, product images, or structured summaries."
        },
        {
            "title": "42 Images Exceeding 100KB and 22 Images Missing Descriptive Alt Text",
            "severity": "Medium",
            "urls": "Site-wide (42.9% of images > 100KB; 22.4% missing alt text)",
            "impact": "Screaming Frog flags 42 images exceeding 100KB and 22 images missing alt text entirely. Crucially, the primary site logo (label-it-logo-scaled.webp) and main homepage hero banners (Frame-1707488208.png) lack alt text."
        },
        {
            "title": "Missing Explicit Image Dimensions on 15 Homepage Elements (CLS Risk)",
            "severity": "Medium",
            "urls": "https://labelitsolutions.co.uk/ (15 img elements lacking width/height attributes)",
            "impact": "15 images on the homepage lack explicit HTML width and height attributes, preventing the browser layout engine from reserving aspect ratio boxes prior to asset download and triggering Cumulative Layout Shift (CLS)."
        },
        {
            "title": "Complete Absence of Verified Customer Reviews Across All 71 Products",
            "severity": "Medium",
            "urls": "https://labelitsolutions.co.uk/product/*",
            "impact": "Zero customer reviews or star ratings exist across all 71 products. The native WooCommerce review tab is unpopulated, and no third-party review integration (Trustpilot, Reviews.io, Judge.me) is active, limiting buyer trust for B2B procurement purchasers."
        },
        {
            "title": "Apache Web Server Lacks Essential HTTP Security Headers",
            "severity": "Medium",
            "urls": "Server-level (478 URLs lacking security headers in Screaming Frog)",
            "impact": "The Apache web server omits Strict-Transport-Security (HSTS), Content-Security-Policy (CSP), X-Frame-Options, X-Content-Type-Options: nosniff, and Referrer-Policy headers. In Screaming Frog, 478 URLs are flagged for missing secure referrer headers."
        },
        {
            "title": "73 Protocol-Relative Resource Links and 1 Internal Insecure HTTP Reference",
            "severity": "Low",
            "urls": "Site-wide (73 URLs load //... resources; 1 internal link to http://www.labelitsolutions.co.uk/)",
            "impact": "73 URLs reference resources using protocol-relative '//' URLs, and one internal navigation element points to the unencrypted HTTP domain, triggering an avoidable 301 redirect."
        },
        {
            "title": "Thin Educational Content Footprint (Only 3 Guides Averaging ~250 Words)",
            "severity": "Low",
            "urls": "https://labelitsolutions.co.uk/how-to-choose-the-right-label-adhesive-standard-freezer-removable/, etc.",
            "impact": "The entire blog consists of only 3 articles averaging 200–290 words. This provides insufficient topical depth to capture informational UK search intent."
        },
        {
            "title": "Quick-Wins / Housekeeping: Lost-Password Title, 404 Placeholders & Slashes",
            "severity": "Low",
            "urls": "/my-account/lost-password/ (raw HTML span), 2 broken placeholder images (300x300, 380x380), 6 trailing-slash 301s",
            "impact": "Minor housekeeping items: unescaped span tag in noindexed lost-password title, two 404 placeholder thumbnails, and 6 internal links omitting trailing slashes."
        }
    ],
    "scope_of_improvement": [
        {
            "bold_prefix": "1. Foundational SEO Architecture & Canonical Governance: ",
            "text": "Installing and configuring a dedicated SEO framework (Rank Math or Yoast SEO) as the primary enabler to inject self-referencing canonical tags across all 200 HTML pages, manage title/meta templates, output clean OpenGraph and Product schema, and apply 'noindex, follow' directives across all 97 thin attribute archives."
        },
        {
            "bold_prefix": "2. Server Speed Optimization & Core Web Vitals Remediation: ",
            "text": "Resolving the 16.5s mobile LCP bottleneck and 1.77s TTFB by deploying page-level server caching (WP Rocket / Redis), configuring Apache mod_expires cache headers across 3.8 MB of static assets, deferring 1,060ms of render-blocking JS, and preloading the primary LCP hero image."
        },
        {
            "bold_prefix": "3. Commercial Category Architecture (12 Base Hubs): ",
            "text": "Refactoring category archive templates to promote category titles from <h2> to styled <h1> tags, crafting unique meta descriptions and introductory copy for all 12 commercial categories, and consolidating the duplicate A4 sheet label category (/product-category/a4-sheet-labels/) with a 301 redirect."
        },
        {
            "bold_prefix": "4. Product Page (PDP) Re-architecture & Schema: ",
            "text": "Mounting and populating the primary WooCommerce Description tab across all 71 products with 250+ words of technical copy (adhesive formulations, core sizes, liner backings, and printer compatibility matrices), deploying Schema.org @type: Product JSON-LD, and integrating verified customer reviews."
        },
        {
            "bold_prefix": "5. Crawl Hygiene & Google Merchant Center Integration: ",
            "text": "Submitting a clean product feed to Google Merchant Center to capture high-converting Free Product Listings on the Google Shopping tab, updating internal trailing-slash links, replacing 404 placeholder images, and injecting standard security headers in the Apache .htaccess."
        }
    ],
    "immediate_fixations": [
        "Install & Configure Rank Math or Yoast SEO (Foundational Enabler): Deploy a dedicated SEO plugin on Day 1 to immediately inject canonical tags site-wide, generate XML sitemaps, output Product schema, and manage metadata templates.",
        "Set All 97 Thin Attribute Taxonomies to Noindex: Configure '/label-width/*', '/label-length/*', '/material/*', and the other 7 attribute taxonomies to 'noindex, follow' to eliminate index bloat.",
        "Deploy Page-Level Server Caching & Apache Browser Caching: Implement page caching to slash the 1.77s TTFB and configure mod_expires headers to eliminate the 3,769 KiB un-cached asset penalty.",
        "Eliminate 1,060ms Render-Blocking Resource Delay: Defer and delay non-essential Elementor, slider, and WooCommerce scripts to unblock First Contentful Paint.",
        "Preload and Optimize LCP Hero Asset: Preload the above-the-fold hero banner and convert oversized images to WebP to compress the 16.5s mobile LCP.",
        "Fix Category <h1> Heading Templates: Update the WooCommerce/Elementor category archive template to output category titles inside proper <h1> tags rather than <h2> across all 12 base categories.",
        "Rewrite Minimal Homepage Title Tag: Replace '<title>Label IT</title>' with an optimized commercial title ('Label IT Solutions | UK Thermal Labels & Rolls Manufacturer') and deploy a 155-character meta description.",
        "Consolidate Duplicate A4 Category With 301 Redirect: Redirect '/product-category/sheet-labels/a4-sheet-labels/' to '/product-category/a4-sheet-labels/'.",
        "Mount & Populate the Product Description Tab: Re-enable the primary WooCommerce Description tab to replace the 'Additional information' H2 fallback.",
        "Verify Search Console & GA4 Integration: Verify that Google Search Console (GSC) and GA4 are tracking correctly to establish a clean UK search impression baseline."
    ],
    "roadmap": [
        {
            "phase": "Phase 1: Foundational SEO, Speed & Indexing\n(Days 1–15)",
            "objectives": "Install Rank Math/Yoast SEO (enabling canonicals site-wide), verify GSC/GA4 tracking, apply noindex to all 97 attribute archives, configure Apache caching & page caching (targeting TTFB < 0.6s), defer render-blocking JS, preload LCP hero, fix 12 category <h1> headings, rewrite homepage title/meta description, and resolve duplicate A4 category.",
            "milestone": "100% canonical coverage; 97 archives noindexed; GSC baseline verified; mobile LCP under 4.0s; category H1s deployed"
        },
        {
            "phase": "Phase 2: Product Content, Schema & Google Merchant Center\n(Days 16–45)",
            "objectives": "Mount primary Description tab on all 71 PDPs with 250+ words of specs (adhesive types, core sizes, liner backing), deploy structured printer compatibility matrices (Zebra, Citizen, Sato, Toshiba), output Schema.org @type: Product JSON-LD, submit Google Merchant Center feed for Free Shopping listings, and deploy OpenGraph tags.",
            "milestone": "Google Product Rich Snippets active; Merchant Center feed approved; unique PDP content expanded; social previews active"
        },
        {
            "phase": "Phase 3: Category Expansion & Commercial Authority\n(Days 46–90)",
            "objectives": "Build dedicated high-intent landing pages for top printer models ('Zebra 4x6 Thermal Labels', 'Direct Thermal Rolls UK'), expand the 3 thin blog guides into comprehensive buyer guides, activate customer review integration (Trustpilot/Judge.me), and conduct a forensic backlink audit of the 189 referring domains.",
            "milestone": "Targeted printer landing pages ranking; customer review social proof established; backlink quality verified"
        },
        {
            "phase": "Phase 4: Search Console Measurement & Lab Speed Verification\n(Days 90+)",
            "objectives": "Review Google Search Console impression and click growth, evaluate Lighthouse lab performance scores (targeting Mobile 85+, LCP <= 2.5s, FCP <= 1.8s), monitor brand and product citations in AI search (ChatGPT, Perplexity, Google AI Overviews), and re-evaluate internal technical health rubric score.",
            "milestone": "Passing Lighthouse lab scores; measurable GSC non-brand impression growth; elevated technical rubric score"
        }
    ]
}

# 2. Save audit_data.json
json_path = os.path.join(out_dir, "audit_data.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(audit_data, f, indent=2)
print(f"[+] Saved updated audit_data.json: {json_path}")

# 3. Create 04_issues_log.csv
issues_file = os.path.join(out_dir, "04_issues_log.csv")
with open(issues_file, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(["Issue Title", "Severity", "Affected URLs", "Observed Defect & Impact"])
    for iss in audit_data["issues"]:
        w.writerow([iss["title"], iss["severity"], iss["urls"], iss["impact"]])
print(f"[+] Saved updated 04_issues_log.csv: {issues_file}")

# 4. Create 10_roadmap_30_60_90.md
rm_file = os.path.join(out_dir, "10_roadmap_30_60_90.md")
with open(rm_file, 'w', encoding='utf-8') as f:
    f.write("""# Label IT Solutions — 30-60-90 Day SEO & E-Commerce Growth Roadmap (Fully Reconciled v4)

## Phase 1: Foundational SEO, Speed & Indexing (Days 1–15)
- [ ] Install and configure Rank Math or Yoast SEO as the foundational enabler (injecting canonicals site-wide, managing metadata templates, and sitemaps).
- [ ] Verify that Google Search Console (GSC) and GA4 are set up properly to establish a clean UK search impression and indexing baseline.
- [ ] Apply `noindex, follow` directives to all 97 thin WooCommerce attribute archives across 10 taxonomies (`/label-width/*`, `/label-length/*`, `/labels-per-roll/*`, etc.) and remove them from the XML sitemap.
- [ ] Deploy page-level server caching (WP Rocket / Redis / LiteSpeed) to slash the 1.77s average TTFB toward < 0.6s.
- [ ] Configure Apache browser caching (`mod_expires` / `Cache-Control: max-age=31536000`) across 3.8 MB of static assets.
- [ ] Defer and delay non-critical Elementor, slider, and WooCommerce scripts to eliminate 1,060ms of render-blocking latency.
- [ ] Preload the LCP hero image asset and convert oversized PNG banners to modern WebP format to compress the 16.5s mobile LCP.
- [ ] Update WooCommerce/Elementor category archive templates to output category titles inside proper `<h1>` tags across all 12 commercial categories.
- [ ] Replace 8-character homepage title (`Label IT`) with an optimized commercial title and deploy a 155-character meta description.
- [ ] Consolidate duplicate A4 sheet label category by redirecting `/product-category/sheet-labels/a4-sheet-labels/` to `/product-category/a4-sheet-labels/`.
- [ ] Quick-wins: update internal trailing-slash links (6 301s), replace 404 placeholder images, and clean up lost-password title.

## Phase 2: Product Content, Schema & Google Merchant Center (Days 16–45)
- [ ] Mount and populate the primary WooCommerce Description tab on all 71 products with 250+ words of technical copy (adhesive formulations, core sizes, liner backing).
- [ ] Build structured Printer Compatibility Matrices (Zebra, Citizen, Sato, Toshiba TEC) on all relevant thermal roll PDPs.
- [ ] Deploy Schema.org `@type: Product` JSON-LD schema with pricing, availability, currency (GBP), and SKU.
- [ ] Set up automated Google Merchant Center product feed to capture high-converting Free Product Listings on the Google Shopping tab.
- [ ] Deploy complete OpenGraph (`og:*`) and Twitter Card metadata across the store.

## Phase 3: Category Expansion & Commercial Authority (Days 46–90)
- [ ] Build dedicated high-intent landing pages for top printer models ("Zebra 4x6 Shipping Labels", "Direct Thermal Rolls UK").
- [ ] Expand the 3 thin educational blog guides into comprehensive buyer guides.
- [ ] Activate verified customer review integration (Trustpilot, Reviews.io, or Judge.me) across all 71 products.
- [ ] Conduct forensic backlink audit of the 189 referring domains to identify low-quality or toxic links; prepare disavow file if necessary.
- [ ] Benchmark organic search performance against UK competitors (Label Planet, Priory Direct, Make Me A Label).

## Phase 4: Search Console Measurement & Lab Speed Verification (Days 90+)
- [ ] Review Google Search Console (GSC) performance data for true UK search impressions, clicks, and non-brand keyword rankings.
- [ ] Re-test Core Web Vitals in PageSpeed Insights to verify passing lab metrics (Mobile Score 85+, LCP <= 2.5s, FCP <= 1.8s).
- [ ] Track brand citations and technical accuracy across AI search platforms (ChatGPT, Perplexity, Google AI Overviews).
- [ ] Re-evaluate internal technical health rubric score against the 20/100 baseline.
""")
print(f"[+] Saved updated 10_roadmap_30_60_90.md: {rm_file}")

# 5. Build Reports via Universal Engine
from generate_issue_only_report_engine import build_docx_report, build_pdf_report

docx_path = os.path.join(out_dir, "LabelItSolutions_SEO_Audit_Report.docx")
build_docx_report(audit_data, docx_path)

pdf_path = os.path.join(out_dir, "LabelItSolutions_SEO_Audit_Report.pdf")
build_pdf_report(audit_data, pdf_path)

# Mirror to root
shutil.copyfile(docx_path, "LabelItSolutions_SEO_Audit_Report.docx")
shutil.copyfile(pdf_path, "LabelItSolutions_SEO_Audit_Report.pdf")
print("[+] Mirrored fully reconciled reports to root successfully!")
