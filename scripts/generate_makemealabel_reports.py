import os
import json
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from playwright.sync_api import sync_playwright

output_dir = r"website audit/makemealabel.com"
os.makedirs(output_dir, exist_ok=True)

audit_data = {
    "client_name": "Make Me A Label",
    "domain": "https://makemealabel.com/",
    "primary_service": "https://makemealabel.com/collections/direct-thermal-roll-labels-blank",
    "core_offering": "UK Label Manufacturer — Direct Thermal & Thermal Transfer Roll Labels",
    "technology_stack": "Shopify (Dawn Theme) on Cloudflare Edge",
    "audit_date": "October 16, 2026 (Live Probed & Verified)",
    "domain_authority_summary": "Semrush AS 2 | Organic Traffic: 0 | UK AI Visibility: 14",
    "health_score": 36,
    "badge_text": "UK E-Commerce & Technical SEO Audit",
    "report_title": "TECHNICAL SEO & E-COMMERCE AUDIT REPORT",
    "meta_items": [
        ("Target Website:", "https://makemealabel.com/"),
        ("Primary Product Collection:", "https://makemealabel.com/collections/direct-thermal-roll-labels-blank"),
        ("Core Business & Target Market:", "Custom Label Manufacturer & Supplier | United Kingdom (Leicester, UK)"),
        ("Technology Stack & Platform:", "Shopify (Dawn Theme) on Cloudflare CDN / Edge"),
        ("Audit Verification Date:", "October 16, 2026 (Live Probed & Verified)"),
        ("Overall Website Health Score:", "36 / 100 (Critical Remediation Required)")
    ],
    "executive_summary": [
        {
            "bold_prefix": "Executive Context: ",
            "text": "Make Me A Label (makemealabel.com) operates as a specialized UK label manufacturer based in Leicester (Company No. 13161985), producing direct thermal roll labels, thermal transfer rolls, and custom sheet labels for UK businesses. Despite high commercial intent for thermal shipping labels, barcode labels, and courier roll packaging across the UK logistics and retail sectors, the store currently registers zero organic search visits per month and suffers from severe e-commerce usability and on-page technical bottlenecks."
        },
        {
            "bold_prefix": "Verified Baseline (Semrush Oct 15, 2026): ",
            "text": "Authority Score: 2 / 100 ('Lacks organic traffic'). UK Organic Traffic: 0 visits/mo (Paid Traffic: 0). UK Organic Keywords: 1 (-50%). Worldwide Organic Keywords: 6. Referring Domains: 1.2K | Backlinks: 1.5K. AI Search Visibility: 14 in the UK (4 mentions on ChatGPT; 0 citations on Google AI Overviews, AI Mode, and Gemini) and 0 Worldwide."
        },
        {
            "bold_prefix": "Screaming Frog & Live Probed Facts: ",
            "text": "Screaming Frog crawled 258 total URLs, identifying 58 HTML pages (27 Products, 7 Collections, 10 Blogs, 5 Policies, 4 Pages, 5 System/Other). Direct live DOM and HTTP inspection revealed that 100% of collection pages lack H1 tags, homepage H1 wraps only an image logo, paginated titles print a live Shopify Liquid error ('Translation missing: en.general.meta.page'), product pages have empty apparel demo accordions, descriptions are under 20 words, product schema lacks SKU/GTIN, and images reach up to 3.2 MB."
        }
    ],
    "scorecard": [
        ["Crawlability & Sitemaps", "10", "8 / 10", "Pass", "Valid Shopify multi-sitemaps (products, collections, pages, blogs)"],
        ["Indexability & Canonicals", "10", "7 / 10", "Pass", "Self-referencing canonicals present; paginated page 1 canonicalised"],
        ["Heading Structure (H1/H2)", "10", "1 / 10", "Critical", "0 H1s on all collection pages; Homepage H1 wraps logo image only"],
        ["On-Page Metadata & Liquid", "10", "2 / 10", "Critical", "'Translation missing: en.general.meta.page' bug active in SERP titles"],
        ["Product Page (PDP) Depth", "10", "2 / 10", "Critical", "Thin 15-word descriptions; empty apparel demo accordions active"],
        ["E-Commerce Conversion UX", "10", "3 / 10", "Critical", "Quick-order list lacks standard primary Add to Cart CTA; no bulk tables"],
        ["UK B2B Pricing & VAT", "10", "2 / 10", "Critical", "No ex-VAT / inc-VAT breakdown or VAT registration number shown"],
        ["Structured Data (Schema)", "10", "3 / 10", "Warning", "Product schema lacks SKU, GTIN, MPN, and reviews; no Breadcrumbs"],
        ["Image Optimization & Media", "10", "2 / 10", "Critical", "80 images > 100KB (up to 3.2MB PNGs); 167 images missing alt text"],
        ["Trust, Reviews & E-E-A-T", "10", "4 / 10", "Warning", "0 customer reviews; shipping policy has only legal disclaimers"],
        ["TOTAL WEIGHTED SCORE", "100", "36 / 100", "Critical", "Immediate Shopify Theme Cleanup & PDP Re-architecture Required"]
    ],
    "issues": [
        {
            "title": "Homepage H1 Wraps Header Logo Image With Zero Textual Heading",
            "severity": "Critical",
            "urls": "https://makemealabel.com/",
            "impact": "The homepage <h1> tag contains exclusively an <a><img></a> wrapper with alt text 'Make me a Label'. The page completely lacks a keyword-focused text H1, despite the title tag targeting 'Label Manufacturing Company in Leicester'."
        },
        {
            "title": "Primary Category & Collection Pages Contain Zero H1 Headings",
            "severity": "Critical",
            "urls": "https://makemealabel.com/collections/direct-thermal-roll-labels-blank, /collections/thermal-transfer-roll-labels-blank, /collections/custom-printed-labels, /collections/frontpage",
            "impact": "All primary commercial collection pages have 0 H1 tags in the DOM. A Shopify Liquid theme defect omits <h1>{{ collection.title }}</h1>, severely depressing category rankings for high-intent queries like 'direct thermal roll labels uk'."
        },
        {
            "title": "Shopify Liquid Translation Bug Outputting Error Text in Search Titles",
            "severity": "Critical",
            "urls": "https://makemealabel.com/collections/all?page=2, https://makemealabel.com/blogs/news?page=2",
            "impact": "Page title tags output raw Liquid template error: 'Products Translation missing: en.general.meta.page'. This amateur defect displays directly in Google search snippets, destroying click-through rates."
        },
        {
            "title": "Apparel Demo Placeholders Active on Industrial Label Product Pages",
            "severity": "Critical",
            "urls": "https://makemealabel.com/products/* (Site-wide on PDPs)",
            "impact": "Product detail pages display default Shopify Dawn apparel demo accordion headers ('Materials and care', 'Merchandising tips', 'Product features') that contain completely empty text bodies, creating an unprofessional impression for B2B procurement managers."
        },
        {
            "title": "Critically Thin Product Descriptions (< 20 Words Total)",
            "severity": "Critical",
            "urls": "https://makemealabel.com/products/* (All 27 products)",
            "impact": "Product descriptions consist of a single 15-word sentence (e.g. '100mm x 152mm (6' by 4') Direct Thermal Labels - 500 Labels per roll - 38mm core - Perforated'). Completely lacks material specs, adhesive rating, liner type, temperature range, and application use cases."
        },
        {
            "title": "E-Commerce PDP Friction: B2B Quick-Order List Lacks Standard 'Add to Cart' CTA",
            "severity": "High",
            "urls": "https://makemealabel.com/products/*",
            "impact": "The store replaces the standard primary 'Add to Cart' or 'Buy Now' button with a multi-row quick-order list table requiring shoppers to click +/- icons and hunt for a small 'View cart' link. On mobile viewports, this causes extreme layout squeeze and high checkout drop-off."
        },
        {
            "title": "Missing UK B2B VAT Breakdown (ex-VAT vs inc-VAT)",
            "severity": "High",
            "urls": "Site-wide",
            "impact": "Prices state only 'Tax included. Shipping calculated at checkout'. B2B label buyers (logistics, fulfillment centers, retail) require transparent '£X.XX ex. VAT / £Y.YY inc. VAT' pricing and visible VAT registration numbers on PDPs."
        },
        {
            "title": "Missing Volume Discount / Bulk Tier Savings Tables",
            "severity": "High",
            "urls": "https://makemealabel.com/products/*",
            "impact": "While 1, 4, 12, and 24 roll options exist in the order list, there is no visual volume tier discount table (e.g. 'Save 15% on 4+ rolls, Save 25% on 12+ rolls') to incentivize higher average order value (AOV)."
        },
        {
            "title": "Zero Customer Reviews or Star Ratings Across Entire Store",
            "severity": "High",
            "urls": "Site-wide",
            "impact": "Zero reviews or ratings exist across all 27 products. No review widget (Judge.me, Loox, Trustpilot) is installed, leaving the store without social proof or buyer confidence signals."
        },
        {
            "title": "Incomplete Product Schema Markup (Missing SKU, GTIN, Barcode)",
            "severity": "High",
            "urls": "https://makemealabel.com/products/*",
            "impact": "The @type: Product JSON-LD schema completely omits 'sku', 'gtin13/barcode', 'mpn', 'aggregateRating', and 'review'. This disqualifies products from Google Shopping enhanced listings and Merchant Center rich results."
        },
        {
            "title": "Zero Breadcrumbs Navigation or BreadcrumbList Schema on PDPs",
            "severity": "Medium",
            "urls": "https://makemealabel.com/products/*",
            "impact": "PDPs lack clickable breadcrumbs (e.g. Home > Roll Labels > Direct Thermal > 100x152mm) and BreadcrumbList schema, degrading internal link equity and user category navigation."
        },
        {
            "title": "Severe Image Bloat Up to 3.2 MB & 167 Images Missing Alt Text",
            "severity": "High",
            "urls": "Site-wide (80 images > 100KB)",
            "impact": "80 images exceed 100KB, with hero banners reaching 3,235 KB (3.2 MB) uncompressed PNG. 167 image instances lack alt text, severely throttling mobile page speed (LCP) and accessibility."
        },
        {
            "title": "Customer-Hostile Shipping Policy Lacking Rates, Times & Couriers",
            "severity": "Medium",
            "urls": "https://makemealabel.com/policies/shipping-policy",
            "impact": "The shipping policy page consists of 404 words of legal liability disclaimers with zero delivery times, delivery fees, free delivery thresholds, or courier partners (Royal Mail / DPD / Evri)."
        },
        {
            "title": "Missing Printer Compatibility Matrix on Thermal Roll PDPs",
            "severity": "High",
            "urls": "https://makemealabel.com/products/*",
            "impact": "Thermal roll products omit compatible printer models (Zebra ZD420/GK420d, Citizen CL-S521, TSC, Brother, Dymo), failing to capture high-intent commercial queries like 'Zebra compatible 4x6 thermal labels'."
        },
        {
            "title": "Typographical Errors in Product Titles and URL Slugs ('100m' & Feet Marks '4'')",
            "severity": "Medium",
            "urls": "https://makemealabel.com/products/100mm-x-100m-4-by-4-direct-thermal-roll-labels",
            "impact": "Product URL and title mislabel '100mm' as '100m' (meters) and use feet marks '4' by 4'' instead of inches (4\" x 4\"), appearing unvetted in search snippets."
        },
        {
            "title": "Missing Security Headers on Production Edge",
            "severity": "Medium",
            "urls": "Site-wide",
            "impact": "HTTP response headers lack Referrer-Policy and permissions policy, failing best-practice browser privacy safeguards."
        },
        {
            "title": "AI Search Citation Blindspot (0 Citations Worldwide)",
            "severity": "Medium",
            "urls": "Site-wide",
            "impact": "Semrush records 0 AI search visibility worldwide and 14 in the UK. The lack of structured technical specifications and entity verification prevents AI engines (Perplexity, Gemini, Google AI Overviews) from citing the brand."
        },
        {
            "title": "Mobile UX Friction: Compressed B2B Table & No Sticky Add to Cart",
            "severity": "Medium",
            "urls": "https://makemealabel.com/products/*",
            "impact": "On mobile screens (390px), the quick-order list table is horizontally squeezed, requiring multi-level vertical scrolling with no sticky CTA on scroll."
        }
    ],
    "scope_of_improvement": [
        {
            "bold_prefix": "1. Search Visibility & AI Discovery: ",
            "text": "Transitioning from Authority Score 2 and 0 organic visits to Page 1 UK rankings for high-intent B2B terms ('direct thermal roll labels uk', 'zebra 4x6 shipping labels', 'thermal transfer labels supplier', 'custom roll labels leicester'). Establishing structured technical specs so AI engines (ChatGPT, Gemini, Perplexity) cite Make Me A Label as a premier UK label converter."
        },
        {
            "bold_prefix": "2. Technical Governance & E-Commerce Crawl Hygiene: ",
            "text": "Fixing the Shopify Liquid translation missing error in SERP title tags, restoring missing <h1> headers across all collection pages, and deploying complete Schema.org Product, Offer, and BreadcrumbList markup."
        },
        {
            "bold_prefix": "3. Topical Authority & Product Detail Page Depth: ",
            "text": "Expanding thin 15-word product pages into comprehensive 250+ word technical listings featuring adhesive grades (permanent vs removable), operating temperature ranges, core sizes (25mm / 38mm / 76mm), and explicit printer compatibility lists (Zebra, Citizen, TSC, Brother, Dymo)."
        },
        {
            "bold_prefix": "4. E-Commerce Conversion Funnel & Mobile Usability: ",
            "text": "Replacing the confusing standalone quick-order list with a dual interface: a prominent primary 'Add to Cart' button above the fold for standard shoppers, paired with an optional bulk volume order table showing tiered percentage savings (e.g. Save 15% on 4+ rolls). Adding a mobile sticky Add to Cart bar."
        },
        {
            "bold_prefix": "5. Brand Authority & UK B2B E-E-A-T: ",
            "text": "Displaying clear UK VAT pricing ('ex. VAT / inc. VAT') and VAT registration details, transforming the shipping policy into a customer-centric delivery guide (listing cut-off times, next-day courier options, and free delivery thresholds), and installing a verified customer reviews app."
        }
    ],
    "immediate_fixations": [
        "Resolve Shopify Liquid Translation Bug in Title Tags: Eliminate 'Translation missing: en.general.meta.page' appearing across paginated collections and blogs.",
        "Restore Missing <h1> Headings on All Collection Pages: Ensure {{ collection.title }} renders as a prominent, styled <h1> on all category landing pages.",
        "Replace Homepage Logo <h1> With a Textual Heading: Move the logo out of the sole <h1> tag and introduce a clear keyword-optimized heading ('UK Manufacturer of Thermal Roll & Custom Printed Labels').",
        "Purge Empty Apparel Demo Accordions From All PDPs: Remove the default Shopify Dawn demo sections ('Materials and care', 'Merchandising tips') from the product template.",
        "Add a Primary 'Add to Cart' CTA Above the Fold: Provide a clear, prominent single-item purchase button alongside the B2B multi-roll quick-order table.",
        "Compress 80 Oversized PNG Banner Images: Convert multi-megabyte PNGs (up to 3.2 MB) into optimized WebP/JPEG format to immediately recover mobile load speed (LCP).",
        "Add Missing Alt Text to 167 Images: Populate descriptive keyword-rich alt text across all product thumbnails and collection banners.",
        "Correct Title and URL Typo ('100m' -> '100mm'): Fix the mislabelled 100mm x 100mm product title and create a clean 301 redirect.",
        "Deploy ex-VAT and inc-VAT Price Transparency: Display clear tax breakdowns on product detail pages and cart templates to satisfy UK B2B procurement standards."
    ],
    "roadmap": [
        {
            "phase": "Phase 1: Emergency Technical & Theme Cleanup\n(Days 1–15)",
            "objectives": "Resolve the 9 emergency defects: fix Liquid translation bug in title tags, add collection H1s, purge empty apparel accordions, add primary Add to Cart CTA, compress oversized 3.2MB images, and add alt text.",
            "milestone": "0 Liquid template bugs in SERPs; valid collection H1s; sub-2s mobile LCP"
        },
        {
            "phase": "Phase 2: E-Commerce Content & Conversion Architecture\n(Days 16–45)",
            "objectives": "Expand PDP descriptions to 250+ words with technical specs, add printer compatibility matrices (Zebra, Citizen, TSC), install verified customer review app (Judge.me/Loox), deploy complete Product/Offer JSON-LD, and rewrite customer-facing shipping policy.",
            "milestone": "Google Product Rich Snippets active; customer review social proof established"
        },
        {
            "phase": "Phase 3: B2B Expansion & Category Authority\n(Days 46–90)",
            "objectives": "Build high-intent landing pages for 'Zebra 4x6 Shipping Labels' and 'Royal Mail Thermal Labels', launch an interactive 'Label Finder' tool, display volume tier discount tables, and secure local Leicester / UK manufacturing directory citations.",
            "milestone": "First Page 1 rankings for commercial UK label queries; +35% increase in B2B AOV"
        },
        {
            "phase": "Phase 4: Field Verification & Authority Rescoring\n(Days 90+)",
            "objectives": "Pull live Chrome User Experience Report (CrUX) field data for Core Web Vitals (LCP, INP, CLS), verify rich product snippet performance in Google Merchant Center, monitor AI search citations in ChatGPT/Perplexity, and re-score store health out of 100.",
            "milestone": "Passing Core Web Vitals field data; verified multi-platform AI search citations"
        }
    ]
}

# Save audit_data.json
json_path = os.path.join(output_dir, "audit_data.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(audit_data, f, indent=2)
print(f"[+] Saved audit_data.json: {json_path}")

# Build DOCX
print("\n=== GENERATING EXECUTIVE DOCX REPORT ===")
from generate_issue_only_report_engine import build_docx_report, build_pdf_report

docx_path = os.path.join(output_dir, "MakeMeALabel_SEO_Audit_Report.docx")
build_docx_report(audit_data, docx_path)

# Build PDF
print("\n=== GENERATING EXECUTIVE PDF REPORT VIA PLAYWRIGHT ===")
pdf_path = os.path.join(output_dir, "MakeMeALabel_SEO_Audit_Report.pdf")
build_pdf_report(audit_data, pdf_path)

# Mirror to root
root_docx = "MakeMeALabel_SEO_Audit_Report.docx"
root_pdf = "MakeMeALabel_SEO_Audit_Report.pdf"
import shutil
shutil.copyfile(docx_path, root_docx)
shutil.copyfile(pdf_path, root_pdf)
print(f"[+] Mirrored reports to workspace root: {root_docx}, {root_pdf}")
