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

# 1. Prepare comprehensive audit_data payload
audit_data = {
    "client_name": "Label IT Solutions",
    "domain": "https://labelitsolutions.co.uk/",
    "primary_service": "https://labelitsolutions.co.uk/product-category/direct-thermal/",
    "core_offering": "UK Label Manufacturer — Direct Thermal, Thermal Transfer, Sheet Labels & Cores",
    "technology_stack": "WordPress (WooCommerce + Elementor) on Apache Web Server",
    "audit_date": "October 16, 2026 (Empirically Verified)",
    "domain_authority_summary": "Semrush AS 6 | Moz DA 2 | UK Keywords: 8 | Ref. Domains: 189 | Mobile PSI: 47/100 (LCP 16.5s)",
    "health_score": 36,
    "badge_text": "UK E-Commerce, WordPress SEO & Core Web Vitals Audit",
    "report_title": "TECHNICAL SEO & E-COMMERCE AUDIT REPORT",
    "meta_items": [
        ("Target Website:", "https://labelitsolutions.co.uk/"),
        ("Primary Product Focus:", "https://labelitsolutions.co.uk/product-category/direct-thermal/"),
        ("Business Type & Market:", "Label Manufacturer & B2B/DTC Supplier | Leicester, UK (Co. 15776706, VAT GB474015505)"),
        ("E-Commerce Platform:", "WordPress (WooCommerce 10.3.8 + Elementor 3.33.3) on Apache"),
        ("Audit Date:", "October 16, 2026"),
        ("Technical Health Rubric Score:", "36 / 100 (Internal Agency Diagnostic Rubric — Critical Remediation Required)")
    ],
    "executive_summary": [
        {
            "bold_prefix": "Executive Context: ",
            "text": "Label IT Solutions (labelitsolutions.co.uk), operated by Label It Ltd (Company Registration No. 15776706, VAT GB474015505, registered at 3 Sylvan Avenue, Leicester, LE5 3SN, United Kingdom), is an established UK manufacturer and converter of direct thermal roll labels, thermal transfer rolls, A4 sheet labels, integrated courier labels, cardboard cores, and printer consumables. The website operates on WordPress with WooCommerce and Elementor on an Apache server. While the commercial product catalog is substantial, the store currently suffers from near-zero organic search visibility in the UK, severe canonical and heading structure deficits, extensive taxonomy bloat, and an absence of structured e-commerce data."
        },
        {
            "bold_prefix": "Verified Tool Baseline (Semrush & Moz, Oct 15–16, 2026): ",
            "text": "Semrush Authority Score: 6 / 100 ('Low authority'). UK Organic Traffic: 3 visits/mo (Paid Traffic: 0). UK Organic Keywords: 8 (-20%). Worldwide Organic Keywords: 19 (-5%). 100% of organic traffic is driven solely by brand navigational queries ('labelit' - Pos 3, Vol 140; 'label it' - Pos 10, Vol 260), while commercial terms sit outside page 4 ('label it printer' - Pos 51; 'label solutions' - Pos 44). Inbound Links: 189 Referring Domains | 253 Backlinks. Moz Pro: Domain Authority 2 / 100, Brand Authority 1 / 100, Page Authority 22 / 100 (Dominant search theme: 'Custom Label Solutions'). AI Search Visibility: 0 worldwide and UK across ChatGPT, Google AI Overviews, Google AI Mode, and Gemini."
        },
        {
            "bold_prefix": "Google PageSpeed Insights & Core Web Vitals Lab Baseline (Oct 16, 2026): ",
            "text": "Official Google Lighthouse analysis confirms critical mobile performance bottlenecks: Mobile Performance Score: 47 / 100 (Red / Fail). Mobile Largest Contentful Paint (LCP) reaches an extreme 16.5 seconds (over 6x the Google 2.5s threshold), and First Contentful Paint (FCP) lags at 6.3 seconds. Total network payload is 4,912 KiB (~4.9 MB). Crucially, 3,769 KiB (~3.8 MB) of static assets lack browser cache lifetimes due to missing Apache mod_expires configuration, 1,060 ms of latency is driven by render-blocking resources, and 1,090 KiB of unused JavaScript and CSS (from Elementor, slider, and WooCommerce scripts) blocks the main thread for 2.9 seconds across 10 long tasks. Desktop performance achieves 70 / 100 with an FCP of 1.2s and an LCP of 3.1s."
        },
        {
            "bold_prefix": "Screaming Frog Crawl & Live Technical Verification: ",
            "text": "The crawl evaluated 214 total URLs: 201 returning HTTP 200, 11 returning HTTP 301 (internal links omitting trailing slashes), and 2 returning HTTP 404 (broken WooCommerce placeholder images). 200 URLs are indexable; 14 are non-indexable. Deep technical inspection revealed that 99.5% of pages (200 of 201) lack canonical tags entirely, 122 pages (60.7%) lack <h1> headings (including 100% of product category archives), 59 thin WooCommerce attribute archives are indexed, zero products contain @type: Product schema, no OpenGraph tags exist, and the homepage title is only 8 characters ('Label IT') with no meta description."
        }
    ],
    "scorecard": [
        ["Crawlability & Sitemaps", "10", "6 / 10", "Warning", "Default WP sitemap indexes empty taxonomies; internal links omit trailing slashes."],
        ["Indexability & Canonicals", "10", "1 / 10", "Critical", "Missing canonical tags on 200 of 201 URLs (99.5%); zero self-referencing canonicals."],
        ["Taxonomy & Index Hygiene", "10", "2 / 10", "Critical", "59 thin WooCommerce attribute archives indexed (/label-width/, /material/, etc.)."],
        ["Heading Structure (H1/H2)", "10", "2 / 10", "Critical", "122 pages missing <h1> tags (60.7%); 100% of category archives lack an <h1>."],
        ["Metadata & Snippet Quality", "10", "2 / 10", "Critical", "Homepage title only 8 chars; 131 pages missing meta descriptions; raw HTML in title."],
        ["Structured Data (Schema)", "10", "2 / 10", "Critical", "Zero @type: Product schema across all 71 products; only basic breadcrumb present."],
        ["Social & Graph Metadata", "10", "0 / 10", "Fail", "Zero OpenGraph (og:*) and zero Twitter Card tags deployed site-wide."],
        ["Product Page (PDP) Depth", "10", "3 / 10", "Critical", "Unique copy is only 13–22 words; description tabs missing; 0 customer reviews."],
        ["Media & Performance (CWV)", "10", "2 / 10", "Critical", "Mobile Score 47/100; LCP 16.5s; 4.9MB payload; 3.8MB un-cached; 1,060ms render delay."],
        ["Security & Server Hygiene", "10", "3 / 10", "Warning", "Apache server lacks HSTS, X-Frame-Options, CSP, nosniff, and Referrer-Policy."],
        ["DIAGNOSTIC RUBRIC SCORE", "100", "36 / 100", "Critical Remediation Required", "Full WordPress/WooCommerce Technical Overhaul & Mobile Speed Optimization Required"]
    ],
    "issues": [
        {
            "title": "Severe Mobile Core Web Vitals Failure: 16.5s LCP, 6.3s FCP, and 4.9 MB Network Payload",
            "severity": "Critical",
            "urls": "https://labelitsolutions.co.uk/ (Google PageSpeed Insights Mobile Run)",
            "impact": "Google PageSpeed Insights records a critical Mobile Performance Score of 47 / 100. Largest Contentful Paint (LCP) takes 16.5 seconds on simulated mobile connections (Google threshold: ≤ 2.5s), and First Contentful Paint (FCP) requires 6.3 seconds. The total page weight is 4,912 KiB (~4.9 MB), creating severe bounce rates for mobile purchasers and triggering Core Web Vitals ranking demotions."
        },
        {
            "title": "Unconfigured Browser Caching on Apache Web Server (3.8 MB Un-Cached Payload)",
            "severity": "Critical",
            "urls": "Site-wide (Apache Server Header Configuration)",
            "impact": "PageSpeed Insights flags 3,769 KiB (~3.8 MB) of static CSS, JS, and image assets lacking efficient cache lifetimes (Cache-Control: max-age or Expires). Returning visitors and multi-page B2B shoppers are forced to re-download the entire 4.9 MB payload on every navigation, multiplying server load and page load latency."
        },
        {
            "title": "Absence of Canonical Tags Across 99.5% of Pages",
            "severity": "Critical",
            "urls": "Site-wide (200 of 201 URLs lack <link rel='canonical'>)",
            "impact": "Screaming Frog and live HTTP header inspection confirm that 200 out of 201 HTML pages completely omit canonical link elements. The website possesses zero self-referencing canonical tags, exposing the site to severe duplicate content penalties across parameter URLs, trailing-slash variations, and HTTP/HTTPS variations."
        },
        {
            "title": "100% of Product Category Archives and 122 Total Pages Missing <h1> Headings",
            "severity": "Critical",
            "urls": "https://labelitsolutions.co.uk/product-category/* (17 categories) and 106 standard pages",
            "impact": "Screaming Frog flags 122 pages lacking an <h1> tag entirely (60.7% of indexable pages). Crucially, 100% of commercial WooCommerce product category archives (/direct-thermal/, /thermal-transfer/, /a4-sheet-labels/) lack an <h1> tag because the Elementor theme template hardcodes category titles inside <h2> tags, stripping primary topical signals from core landing pages."
        },
        {
            "title": "Complete Absence of @type: Product Structured Data Across All 71 Products",
            "severity": "Critical",
            "urls": "https://labelitsolutions.co.uk/product/* (All 71 products)",
            "impact": "Product detail pages output solely a basic BreadcrumbList JSON-LD block and completely omit Schema.org @type: Product, Offer, price, priceCurrency (GBP), availability, SKU, and review properties. This prevents all 71 products from attaining rich snippet pricing badges in Google SERPs and blocks automated Google Merchant Center synchronization."
        },
        {
            "title": "Index Bloat: 59 Thin WooCommerce Attribute Taxonomy Archives Indexed",
            "severity": "Critical",
            "urls": "https://labelitsolutions.co.uk/label-width/*, /label-length/*, /material/*, /printer-compatibility/*",
            "impact": "59 WooCommerce attribute archives (pa_label-width, pa_label-length, pa_material, pa_printer-compatibility) are currently indexable. These pages contain only automated duplicate product grids with zero unique descriptive copy (~128 words), fragmenting link equity, cannibalizing primary category rankings, and wasting search engine crawl budget."
        },
        {
            "title": "Minimal Homepage Title Tag (8 Characters) and Missing Meta Description",
            "severity": "Critical",
            "urls": "https://labelitsolutions.co.uk/",
            "impact": "The homepage <title> tag contains only 'Label IT' (8 characters, 71 pixels), completely failing to target primary commercial keywords ('Direct Thermal Labels UK', 'Thermal Transfer Rolls Manufacturer'). Additionally, the homepage has no meta description, leaving Google to extract arbitrary header text for search snippets."
        },
        {
            "title": "Render-Blocking Resource Latency and Unused Elementor/WooCommerce Code Bloat",
            "severity": "High",
            "urls": "https://labelitsolutions.co.uk/",
            "impact": "PageSpeed Insights identifies 1,060 ms of render-blocking requests delaying initial DOM rendering. Furthermore, 687 KiB of unused JavaScript and 403 KiB of unused CSS (totaling 1,090 KiB) from Elementor, Elementor Pro, and WooCommerce plugins load sitewide, tying up the browser main thread for 2.9 seconds across 10 long tasks."
        },
        {
            "title": "Raw HTML Tags Displaying in Page Title Search Snippets",
            "severity": "High",
            "urls": "https://labelitsolutions.co.uk/my-account/lost-password/",
            "impact": "The password reset page outputs raw, unescaped HTML styling within its <title> tag: 'Forgot Your <span style=\"color:#c50000;\">Password?</span> – Label IT'. This severe template defect renders broken code directly in browser tabs and search engine result pages."
        },
        {
            "title": "Widespread Missing Meta Descriptions (131 Pages / 65.2% Lacking Snippets)",
            "severity": "High",
            "urls": "131 URLs across product categories, policy pages, and taxonomy archives",
            "impact": "65.2% of the entire website lacks meta descriptions. This includes high-priority commercial hubs such as /product-category/direct-thermal/, /sheet-labels/, and /printer-accessories/, severely reducing organic click-through rates (CTR) on commercial SERP impressions."
        },
        {
            "title": "Thin Unique Product Descriptions (13–22 Words) With Missing Description Tabs",
            "severity": "High",
            "urls": "https://labelitsolutions.co.uk/product/* (Site-wide on PDPs)",
            "impact": "Product pages contain only a brief 13–22 word short description sentence. The standard WooCommerce product description tab is completely unconfigured or missing. Pages lack technical specifications, adhesive grades (permanent acrylic vs removable), liner backing types, roll winding directions, and core dimensions."
        },
        {
            "title": "107 Page Titles Under 30 Characters Failing to Target Commercial Queries",
            "severity": "High",
            "urls": "107 URLs site-wide (53.2% of indexable pages)",
            "impact": "Over 53% of all pages have truncated, minimal titles under 30 characters (e.g. 'Ribbon Ink – Label IT', 'Cores – Label IT', 'Printers – Label IT', 'Shop – Label IT'). This underutilizes available SERP real estate (up to 60 characters / 561 pixels) and prevents the site from capturing long-tail UK B2B queries."
        },
        {
            "title": "Internal Links Omit Trailing Slashes Triggering 11 Unnecessary 301 Redirect Hops",
            "severity": "High",
            "urls": "https://labelitsolutions.co.uk/blog, /contact-us, /about-us, /shop, /faq, /registration",
            "impact": "Internal navigation menus and text links point to non-trailing-slash URLs, causing 11 internal 301 redirect hops to their trailing-slash counterparts on every crawl. Furthermore, paginated category links (/page/1/) redirect to root categories, wasting crawl budget and adding avoidable latency."
        },
        {
            "title": "Broken 404 WooCommerce Placeholder Images Linked Internally",
            "severity": "High",
            "urls": "https://labelitsolutions.co.uk/wp-content/uploads/woocommerce-placeholder-300x300.png, ...380x380.png",
            "impact": "Screaming Frog flags 2 internal URLs returning HTTP 404 Client Errors. These missing WooCommerce placeholder images are actively linked across catalog templates where product imagery is absent, generating 404 errors for visitors and crawlers."
        },
        {
            "title": "Complete Absence of OpenGraph and Twitter Card Social Metadata",
            "severity": "Medium",
            "urls": "Site-wide (0 og:* and 0 twitter:* tags detected)",
            "impact": "The website has zero OpenGraph or Twitter Card meta tags installed. When links from the store are shared across B2B communications, LinkedIn, WhatsApp, or Twitter, they render without rich media previews, product images, or structured summaries."
        },
        {
            "title": "42 Images Exceeding 100KB and 22 Images Missing Descriptive Alt Text",
            "severity": "Medium",
            "urls": "Site-wide (42.9% of images > 100KB; 22.4% missing alt text)",
            "impact": "Screaming Frog flags 42 images exceeding 100KB (with unoptimized PNG assets), and 22 images missing alt text entirely. Crucially, the primary site logo (label-it-logo-scaled.webp) and main homepage hero banners (Frame-1707488208.png) lack alt text, hindering accessibility and image search indexing."
        },
        {
            "title": "Missing Explicit Image Dimensions on 15 Homepage Elements (CLS Risk)",
            "severity": "Medium",
            "urls": "https://labelitsolutions.co.uk/ (15 img elements lacking width/height attributes)",
            "impact": "15 images on the homepage lack explicit HTML width and height attributes. This prevents the browser layout engine from reserving image aspect ratio boxes prior to asset download, triggering layout instability and inflating Cumulative Layout Shift (CLS)."
        },
        {
            "title": "Uninstalled Dedicated WordPress SEO Plugin (Default WP Core Sitemap Active)",
            "severity": "Medium",
            "urls": "Site-wide (https://labelitsolutions.co.uk/wp-sitemap.xml)",
            "impact": "The site relies on the unconfigured WordPress 5.5+ core sitemap generator (/wp-sitemap.xml) rather than a robust SEO plugin (Rank Math, Yoast SEO). This leaves webmasters without the ability to manage indexation flags, set canonical overrides, or exclude junk attribute taxonomies."
        },
        {
            "title": "Complete Absence of Verified Customer Reviews and Social Proof Across All PDPs",
            "severity": "Medium",
            "urls": "https://labelitsolutions.co.uk/product/*",
            "impact": "Zero customer reviews or star ratings exist across all 71 products. The native WooCommerce review tab is unpopulated, and no third-party review integration (Trustpilot, Reviews.io, Judge.me) is active, severely limiting buyer trust for first-time UK B2B procurement purchasers."
        },
        {
            "title": "Apache Web Server Lacks Essential HTTP Security Headers",
            "severity": "Medium",
            "urls": "Server-level (478 URLs lacking security headers in Screaming Frog)",
            "impact": "The Apache web server omits Strict-Transport-Security (HSTS), Content-Security-Policy (CSP), X-Frame-Options (clickjacking protection), X-Content-Type-Options: nosniff, and Referrer-Policy headers. In Screaming Frog, 478 URLs are flagged for missing secure referrer headers."
        },
        {
            "title": "Failed Agentic Browsing Readiness (Score: 0 / 2 on Mobile)",
            "severity": "Low",
            "urls": "https://labelitsolutions.co.uk/ (Lighthouse Agentic Browsing Audit)",
            "impact": "PageSpeed Insights flags the website as scoring 0/2 on Agentic Browsing mobile capabilities due to missing explicit machine-readable metadata, un-annotated action targets, and rigid interactive elements that impede autonomous AI agent navigation and procurement bot traversal."
        },
        {
            "title": "Double-Escaped HTML Entities in Structured Data Breadcrumbs",
            "severity": "Low",
            "urls": "https://labelitsolutions.co.uk/product/*",
            "impact": "BreadcrumbList JSON-LD blocks output double-escaped entities in item names (e.g. 'Cardboard Cores &amp;#8211; 13mm Internal Diameter'), reflecting a theme sanitization bug that pollutes structured data consumed by search engines."
        }
    ],
    "scope_of_improvement": [
        {
            "bold_prefix": "1. Mobile Core Web Vitals & Server Performance: ",
            "text": "Remediating the 16.5s mobile LCP bottleneck by configuring Apache browser caching (mod_expires / Cache-Control) across 3.8 MB of static assets, deferring 1,060ms of render-blocking JavaScript, purging 1.1 MB of unused Elementor/WooCommerce CSS and JS, preloading the LCP hero image, and converting 42 oversized images to modern WebP."
        },
        {
            "bold_prefix": "2. Search Visibility & Canonical Governance: ",
            "text": "Deploying self-referencing canonical tags across 100% of URLs (200 HTML pages) via a dedicated WordPress SEO plugin, and setting 59 thin WooCommerce attribute archives (/label-width/, /material/, /printer-compatibility/) to 'noindex, follow' to eliminate index bloat and consolidate link equity."
        },
        {
            "bold_prefix": "3. On-Page Structure & Snippet Optimization: ",
            "text": "Refactoring category archive templates to promote category titles from <h2> to styled <h1> tags, optimizing the homepage title tag to target primary UK commercial keywords, fixing the raw HTML <span> error in the user account title, and writing compelling meta descriptions across all 17 product categories."
        },
        {
            "bold_prefix": "4. Structured Data & Google Merchant Center Integration: ",
            "text": "Implementing comprehensive Schema.org @type: Product JSON-LD markup (including price, currency GBP, availability, SKU, and brand) across all 71 products, and submitting an automated product feed to Google Merchant Center to capture high-converting Free Product Listings on the Google Shopping tab."
        },
        {
            "bold_prefix": "5. Product Page (PDP) Re-architecture & Trust: ",
            "text": "Expanding unique product copy from 15 words to 250+ words covering material specifications, adhesive grades (standard permanent vs freezer vs removable), roll core sizes (25mm/38mm/76mm), and printer compatibility matrices (Zebra, Citizen, Sato, Toshiba TEC). Integrating third-party customer reviews for B2B credibility."
        }
    ],
    "immediate_fixations": [
        "Enable Apache Browser Caching (mod_expires / Cache-Control): Immediately configure 1-year cache headers for static images, CSS, and JS to eliminate the 3,769 KiB un-cached asset penalty.",
        "Eliminate 1,060ms Render-Blocking Resource Delay: Defer and delay non-essential Elementor, slider, and WooCommerce scripts to unblock first contentful paint (FCP 6.3s).",
        "Preload and Optimize LCP Hero Asset: Preload the primary above-the-fold hero banner to drastically compress the 16.5s mobile Largest Contentful Paint.",
        "Deploy Self-Referencing Canonical Tags Site-Wide: Implement canonical link elements across all 200 indexable HTML pages to protect against duplicate content.",
        "Fix Category <h1> Heading Templates: Update the WooCommerce/Elementor category archive template to output category titles inside proper <h1> tags rather than <h2>.",
        "Rewrite Minimal Homepage Title Tag: Replace the 8-character '<title>Label IT</title>' with an optimized commercial title ('Label IT Solutions | UK Thermal Labels & Rolls Manufacturer') and deploy a 155-character meta description.",
        "Set 59 Thin Attribute Taxonomies to Noindex: Configure '/label-width/*', '/label-length/*', '/material/*', and '/printer-compatibility/*' to 'noindex, follow' to eliminate index bloat.",
        "Resolve Raw HTML <span> Bug in Lost Password Title: Remove unescaped HTML styling from the user account template title snippet.",
        "Correct Internal Links to Include Trailing Slashes: Update navigation and footer links for '/blog', '/contact-us', '/about-us', '/shop', and '/faq' to resolve 11 301 redirects.",
        "Eliminate Broken 404 Placeholder Images: Upload missing placeholder image assets ('woocommerce-placeholder-300x300.png' and '380x380.png') or remap missing catalog thumbnails."
    ],
    "roadmap": [
        {
            "phase": "Phase 1: Emergency Speed & Indexation Remediation\n(Days 1–15)",
            "objectives": "Configure Apache browser caching (mod_expires), defer 1,060ms render-blocking JS, preload LCP hero asset to drop mobile LCP from 16.5s, deploy self-referencing canonicals site-wide, fix category <h1> headings, apply noindex to 59 attribute archives, resolve raw HTML in title, fix internal trailing slashes, and replace 404 placeholder images.",
            "milestone": "Mobile LCP under 4.0s; 100% canonical coverage; valid category H1s deployed; 0 raw HTML bugs; 0 internal 404 errors"
        },
        {
            "phase": "Phase 2: Product Content & E-Commerce Trust Re-architecture\n(Days 16–45)",
            "objectives": "Expand PDP descriptions to 250+ words with material specs (adhesive types, core sizes, liner backing), build structured printer compatibility matrices (Zebra, Citizen, Sato, Toshiba), activate customer review integration, deploy Product JSON-LD schema, and configure OpenGraph tags.",
            "milestone": "Google Product Rich Snippets active; review social proof established; unique PDP content expanded"
        },
        {
            "phase": "Phase 3: Google Merchant Center & Commercial Authority\n(Days 46–90)",
            "objectives": "Deploy automated Google Merchant Center product feed for Free Google Shopping listings, build dedicated commercial landing pages for high-volume printer models ('Zebra 4x6 Thermal Labels', 'Direct Thermal Rolls UK'), and conduct a forensic backlink audit of the 189 referring domains.",
            "milestone": "Merchant Center product feed approved; targeted printer landing pages ranking; backlink quality verified"
        },
        {
            "phase": "Phase 4: Field Verification & Search Measurement Pass\n(Days 90+)",
            "objectives": "Integrate and monitor Google Search Console (GSC) for true UK search impressions, verify mobile Core Web Vitals (LCP < 2.5s, FCP < 1.8s) in field CrUX data, monitor AI search citations in ChatGPT and Google AI Overviews, and re-evaluate technical health rubric score.",
            "milestone": "Passed Core Web Vitals field metrics; verified GSC keyword traction; elevated organic revenue"
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
    f.write("""# Label IT Solutions — 30-60-90 Day SEO & E-Commerce Growth Roadmap (Revised With PageSpeed Insights)

## Phase 1: Emergency Speed & Indexation Remediation (Days 1–15)
- [ ] Configure Apache browser caching (`mod_expires` / `Cache-Control: max-age=31536000`) across 3.8 MB of static assets.
- [ ] Defer and delay non-critical Elementor, slider, and WooCommerce scripts to eliminate 1,060ms of render-blocking latency.
- [ ] Preload the LCP hero image asset and convert oversized PNG banners to modern WebP format to drop mobile LCP from 16.5s.
- [ ] Deploy self-referencing canonical tags across all 200 indexable HTML pages.
- [ ] Fix category archive templates by promoting category titles from `<h2>` to styled `<h1>` headings.
- [ ] Replace 8-character homepage title (`Label IT`) with an optimized commercial title and deploy a 155-character meta description.
- [ ] Apply `noindex, follow` directives to 59 thin WooCommerce attribute archives (`/label-width/*`, `/label-length/*`, `/material/*`, `/printer-compatibility/*`).
- [ ] Fix unescaped HTML `<span>` tag rendering in `/my-account/lost-password/` `<title>` snippet.
- [ ] Update internal navigation and footer links to include trailing slashes, eliminating 11 301 redirects.
- [ ] Resolve 2 internal 404 client errors on `woocommerce-placeholder-300x300.png` and `380x380.png`.
- [ ] Inject standard HTTP security headers (HSTS, CSP, X-Frame-Options, nosniff, Referrer-Policy) in Apache `.htaccess`.

## Phase 2: Product Content & E-Commerce Trust Re-architecture (Days 16–45)
- [ ] Expand unique product descriptions to 250+ words covering material specifications, adhesive grades (standard vs freezer vs removable), roll core sizes, and liner backing.
- [ ] Build structured Printer Compatibility Matrices (Zebra, Citizen, Sato, Toshiba TEC) on all relevant thermal roll PDPs.
- [ ] Activate verified customer review integration (Trustpilot, Reviews.io, or Judge.me) across all 71 products.
- [ ] Deploy Schema.org `@type: Product` JSON-LD schema with pricing, availability, currency (GBP), and SKU.
- [ ] Deploy complete OpenGraph (`og:*`) and Twitter Card metadata across the store.

## Phase 3: Google Merchant Center & Commercial Authority (Days 46–90)
- [ ] Deploy automated Google Merchant Center product feed to capture high-converting Free Product Listings on the Google Shopping tab.
- [ ] Build dedicated high-intent landing pages for top printer models ("Zebra 4x6 Shipping Labels", "Direct Thermal Rolls UK").
- [ ] Conduct forensic backlink audit of the 189 referring domains to identify low-quality or toxic links; prepare disavow file if necessary.
- [ ] Benchmark organic search performance against UK competitors (Label Planet, Priory Direct, Make Me A Label).

## Phase 4: Field Verification & Search Measurement Pass (Days 90+)
- [ ] Review Google Search Console (GSC) performance data for true UK search impressions, clicks, and indexed URLs.
- [ ] Re-test Core Web Vitals in PageSpeed Insights to verify passing field CrUX metrics (Mobile LCP < 2.5s, FCP < 1.8s, Score 85+).
- [ ] Track brand citations and technical accuracy across AI search platforms (ChatGPT, Perplexity, Google AI Overviews).
- [ ] Re-evaluate internal technical health rubric score.
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
print("[+] Mirrored updated reports to root successfully!")
