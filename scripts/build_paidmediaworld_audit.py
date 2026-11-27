import os
import json
import csv
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
import shutil

out_dir = r"website audit/paidmediaworld.com"
os.makedirs(out_dir, exist_ok=True)

# 1. Audit Data Payload
audit_data = {
    "client_name": "Paid Media World",
    "domain": "https://paidmediaworld.com/",
    "primary_service": "https://paidmediaworld.com/google-ads/",
    "core_offering": "Premier Performance Marketing Agency & Growth Hub (Google Ads, Meta Ads, GA4, AI Search)",
    "technology_stack": "Next.js (App Router / React) on Cloudflare CDN Edge",
    "audit_date": "October 17, 2026 (Empirically Verified via GSC & Crawl)",
    "domain_authority_summary": "GSC 16M: 205.9K Impr | 276 Clicks | CTR 0.13% | 131 Indexable Pages | 11 404s",
    "health_score": 39,
    "badge_text": "Performance Marketing Technical SEO & GSC Audit",
    "report_title": "TECHNICAL SEO & SEARCH CONSOLE AUDIT REPORT",
    "meta_items": [
        ("Target Website:", "https://paidmediaworld.com/"),
        ("Primary Service Focus:", "https://paidmediaworld.com/google-ads/"),
        ("Business Type & Market:", "Performance Marketing & Growth Agency | Global (US, India, UK, SG, AU)"),
        ("Technology Platform:", "Next.js (React / SSR) on Cloudflare Global Edge"),
        ("Audit Date:", "October 17, 2026"),
        ("Technical Health Rubric Score:", "39 / 100 (Internal Agency Diagnostic Rubric — Critical Remediation Required)")
    ],
    "executive_summary": [
        {
            "bold_prefix": "Executive Context: ",
            "text": "Paid Media World (paidmediaworld.com) is a high-authority performance marketing publication, agency, and growth resource specializing in advanced paid acquisition (Google Ads, Meta Ads, TikTok), tracking & attribution (GA4, BigQuery, Server-Side GTM), and conversion rate optimization. The platform is architected on modern Next.js hosted behind Cloudflare's CDN edge. While the site has accumulated substantial algorithmic trust and impressions in Google Search, it suffers from a catastrophic click-through rate (CTR) deficit, near-total absence of canonical tags, widespread SERP snippet truncation, raw HTML entities in title tags, and critical broken internal links."
        },
        {
            "bold_prefix": "Verified First-Party Google Search Console Baseline: ",
            "text": "First-party Google Search Console exports confirm substantial latent search demand paired with severe snippet underperformance. Over the last 16 months (Sept 2025 – Oct 2026), the site generated 205,940 impressions across 1,000+ commercial and technical queries, but secured only 276 total clicks—representing a dismal overall CTR of 0.13% (industry benchmark: 1.5%–4.0%). In the last 7 days alone, the site registered 3,238 impressions and only 3 clicks (CTR 0.09%). Crucially, the #1 impression asset ('Facebook Ads Cost in India...') captured 100,917 impressions at an average position of 6.5 (Page 1), yet yielded only 47 clicks (0.05% CTR) due to title truncation and unescaped HTML entities."
        },
        {
            "bold_prefix": "Screaming Frog Crawl & Live Technical Verification: ",
            "text": "The crawl evaluated 179 total URLs (131 Indexable, 48 Non-Indexable). Deep technical inspection revealed that 99.2% of indexable pages (130 of 131) completely lack canonical tags in their Next.js header output, 96.2% of page titles (126 of 131) exceed 60 characters / 561 pixels causing severe truncation in search results, 87.8% of meta descriptions exceed 155 characters, 23 page titles leak raw HTML entities ('&amp;#038;'), and 11 URLs return HTTP 404 Client Errors—including a broken Cloudflare email protection link with 238 internal inlinks and 6 strategic pillar guides."
        }
    ],
    "scorecard": [
        ["Crawlability & HTTP Hygiene", "10", "5 / 10", "Warning", "11 internal 404s (email protection link has 238 inlinks); 37 internal 301 hops."],
        ["Indexability & Canonicals", "10", "1 / 10", "Critical", "130 of 131 indexable URLs (99.2%) lack canonical tags in Next.js header output."],
        ["URL & Parameter Hygiene", "10", "4 / 10", "Warning", "12 parameter URLs (/contact-us/?service=*) indexed without canonical consolidation."],
        ["SERP Metadata & Snippets", "10", "2 / 10", "Critical", "96.2% of titles exceed 60 chars / 561 px; 87.8% descriptions > 155 chars; raw HTML."],
        ["Organic CTR & Monetization", "10", "2 / 10", "Critical", "205.9K GSC impressions yielding only 276 clicks (0.13% CTR); top page 0.05% CTR."],
        ["Heading Structure (H1/H2)", "10", "7 / 10", "Pass", "Clean single <h1> structure on all pages; but 72 <h1> tags exceed 70 characters."],
        ["Content Depth & Architecture", "10", "6 / 10", "Warning", "Average word count is strong (1,737 words); but 10 categories are thin listing stubs."],
        ["Structured Data (Schema)", "10", "6 / 10", "Warning", "LocalBusiness and TechArticle schema active; missing author sameAs and FAQs."],
        ["Media & Page Speed (CLS)", "10", "3 / 10", "Critical", "83.8% images > 100KB (93 assets); 92.8% missing dimensions causing layout shift."],
        ["Security & Server Headers", "10", "3 / 10", "Warning", "Cloudflare edge lacks HSTS, CSP, X-Frame-Options, nosniff, and Referrer-Policy."],
        ["DIAGNOSTIC RUBRIC SCORE", "100", "39 / 100", "Critical Remediation Required", "Ten 10-point categories derived strictly from GSC first-party data and crawl audit."]
    ],
    "issues": [
        {
            "title": "Severe Organic CTR Collapse Across 205,940 Search Impressions (Overall CTR 0.13%)",
            "severity": "Critical",
            "urls": "Site-wide (First-Party Google Search Console Performance Data)",
            "impact": "Over the last 16 months, the website earned 205,940 impressions in Google Search across high-intent performance marketing queries, but generated only 276 clicks—a catastrophic CTR of 0.13%. Most critically, the top asset ('/cost-of-facebook-ads-in-india-guide-benchmarks-for-leads-sales/') achieved 100,917 impressions on Page 1 (Average Position 6.5), but secured only 47 clicks (0.05% CTR). Lifting this single page to an industry-standard 2.5% CTR would generate 2,500+ clicks (a 53x traffic increase) on existing rankings without building a single new backlink."
        },
        {
            "title": "Complete Absence of Canonical Tags Across 99.2% of Indexable Pages",
            "severity": "Critical",
            "urls": "Site-wide (130 of 131 indexable URLs lack <link rel='canonical'>)",
            "impact": "Screaming Frog and live HTTP inspection confirm that 130 out of 131 indexable HTML pages completely omit canonical link elements. Next.js metadata templates in layout.tsx fail to declare 'alternates.canonical', leaving the entire site exposed to index fragmentation, duplicate parameter indexing, and search engine canonical confusion."
        },
        {
            "title": "Widespread Title Tag Truncation in Google Search Results (96.2% of All Titles)",
            "severity": "Critical",
            "urls": "126 of 131 indexable URLs exceed 60 characters / 561 pixels",
            "impact": "96.18% of all page titles on the website exceed Google's desktop and mobile display limits (561 pixels / ~60 characters). Titles reach up to 105 characters (e.g. 'Facebook Ads Cost in India: 2026 Benchmarks &#038; Pricing Guide | Paid Media World' at 85 chars / 723 px). Google truncates these titles mid-sentence with ellipses, hiding critical value propositions and destroying search snippet click-through rates."
        },
        {
            "title": "Broken Cloudflare Email Protection Link Generating 238 Internal 404 Client Errors",
            "severity": "Critical",
            "urls": "https://paidmediaworld.com/cdn-cgi/l/email-protection (Linked across 238 internal pages)",
            "impact": "Cloudflare's automated email obfuscation script endpoint (/cdn-cgi/l/email-protection) returns HTTP 404 Client Errors on the live site. Because this link is embedded in global footer and author templates, 238 internal pages continuously generate 404 errors for visitors and search engine crawlers, degrading crawl health and domain trust."
        },
        {
            "title": "6 High-Value Strategic Pillar Guides Linked Internally Returning 404 Errors",
            "severity": "Critical",
            "urls": "/the-ultimate-google-ads-guide-for-beginners-and-professionals-2026/, /predictive-profitability-ga4-customer-ltv-b2b-leadgen/, /what-is-performance-marketing-blueprint-scalable-growth/, /the-ultimate-meta-ads-guide-for-lead-generation-and-sales/, /meta-advantage-plus-shopping-campaigns-ecommerce-guide/, /category/seo/technical-seo/",
            "impact": "Six high-intent pillar guides and a category archive are actively linked from other published articles but return HTTP 404 Client Errors. These broken internal references waste internal PageRank, frustrate high-intent visitors, and produce dead-end crawl traps."
        },
        {
            "title": "Widespread Meta Description Truncation (87.8% of Indexable Pages)",
            "severity": "High",
            "urls": "115 of 131 indexable URLs exceed 155 characters / 985 pixels",
            "impact": "Nearly 88% of all meta descriptions exceed 155 characters, reaching up to 220 characters. Descriptions are cut off mid-thought in search snippets without presenting a compelling call to action, contributing directly to the site's 0.13% CTR collapse."
        },
        {
            "title": "Raw HTML Entities Leaking Directly Into Page Titles and Search Snippets",
            "severity": "High",
            "urls": "23 page titles site-wide (including top traffic assets)",
            "impact": "23 page titles output raw unescaped HTML entities such as '&amp;#038;' and '&#038;' directly in their <title> tags. For example, the top traffic asset displays 'Benchmarks &amp;#038; Pricing Guide' in Google SERPs and browser tabs, projecting an unpolished, broken technical impression."
        },
        {
            "title": "Indexation of 12 Duplicate Contact Parameter URLs (/contact-us/?service=*)",
            "severity": "High",
            "urls": "https://paidmediaworld.com/contact-us/?service=tracking, ...?service=cro-landing-pages, ...?service=b2b-saas-marketing (12 URLs)",
            "impact": "12 tracking parameter variations of the contact page are indexable, contain thin identical content (237 words), and completely lack canonical tags pointing back to the clean '/contact-us/' route. This pollutes the index and dilutes crawl equity."
        },
        {
            "title": "37 Internal 301 Redirect Hops Diluting Crawl Budget and Adding Latency",
            "severity": "High",
            "urls": "Site-wide (37 internal links pointing to redirected URLs)",
            "impact": "Internal navigation and contextual body links point to 37 retired URLs (such as old calculator routes and legacy guides) that trigger 301 redirects. This forces crawlers and users through avoidable redirect chains, adding latency and shedding link equity."
        },
        {
            "title": "Local Healthcare Agency Opportunity Wasted: Page 1 Rankings Yielding Zero Clicks",
            "severity": "High",
            "urls": "https://paidmediaworld.com/why-every-hospital-and-private-practice-in-kolkata-needs-a-specialized-healthcare-digital-marketing-agency/",
            "impact": "GSC data reveals this single page ranks in positions 7–10 on Page 1 for high-value local queries ('digital marketing services for diagnostic centre in kolkata' - Pos 7.1, 630 impr; 'digital marketing company for diagnostic centre' - Pos 9.2, 568 impr), capturing 4,745 total impressions but securing exactly 0 clicks (0.00% CTR) due to a 115-character untargeted title."
        },
        {
            "title": "Missing Explicit Image Dimensions on 92.8% of Assets Triggering Layout Shift (CLS)",
            "severity": "Medium",
            "urls": "103 of 111 images site-wide (including 100% of homepage images)",
            "impact": "Over 92% of images lack explicit HTML width and height attributes. Browsers cannot calculate aspect ratio layout boxes prior to image download, causing severe layout instability and inflating Cumulative Layout Shift (CLS) on mobile viewports."
        },
        {
            "title": "83.8% of Images Exceeding 100KB Served as Uncompressed Legacy Formats",
            "severity": "Medium",
            "urls": "93 images site-wide (PNG and JPG assets)",
            "impact": "83.78% of images exceed 100KB, with large full-width diagrams and screenshots served as uncompressed PNGs rather than modern WebP or AVIF formats. On the homepage, 100% of images are served as legacy PNG/JPG."
        },
        {
            "title": "10 Thin Category Archive Pages (< 300 Words) Lacking Topical Authority",
            "severity": "Medium",
            "urls": "/category/ai-marketing/ (115 words), /category/attribution/ (62 words), /category/ab-testing/ (66 words), /category/conversion-tracking/ (66 words), etc.",
            "impact": "10 category archives function purely as automated link lists with word counts between 62 and 292 words. They lack unique introductory copy, structured definitions, and custom meta descriptions, failing to rank for competitive category head-terms."
        },
        {
            "title": "72 <h1> Headings Exceeding 70 Characters Diluting Topical Relevance",
            "severity": "Medium",
            "urls": "72 of 131 indexable pages (54.96%)",
            "impact": "More than half of all primary page headings exceed 70 characters. Long, verbose <h1> tags dilute primary keyword weight and reduce semantic clarity for search engines and assistive screen readers."
        },
        {
            "title": "Cloudflare CDN Edge Lacks Essential HTTP Security Headers",
            "severity": "Medium",
            "urls": "Server-level (261 URLs flagged in Screaming Frog)",
            "impact": "The Cloudflare edge server omits Strict-Transport-Security (HSTS), Content-Security-Policy (CSP), X-Frame-Options (clickjacking protection), and X-Content-Type-Options: nosniff headers across 261 URLs."
        },
        {
            "title": "42 Duplicate <h2> Tags and 40 Non-Sequential Heading Hierarchy Warnings",
            "severity": "Medium",
            "urls": "42 pages with duplicate <h2>s; 40 pages with non-sequential headings",
            "impact": "Re-used sidebar callouts and footer widgets inject identical <h2> headings across 42 articles, while 40 pages skip heading levels (e.g. Jumping directly from <h1> to <h3>), disrupting the logical semantic outline."
        },
        {
            "title": "Missing Author E-E-A-T Credential Links in TechArticle Structured Data",
            "severity": "Medium",
            "urls": "https://paidmediaworld.com/* (Published Articles)",
            "impact": "While TechArticle schema is present on articles, author nodes omit 'sameAs' links to verified LinkedIn profiles, industry publications, or executive bios, missing a vital E-E-A-T trust signal for algorithmic evaluation."
        },
        {
            "title": "15 Duplicate Page Titles and 15 Duplicate Meta Descriptions",
            "severity": "Low",
            "urls": "15 URLs site-wide",
            "impact": "Overlapping category pages, pagination routes, and duplicate contact parameters share 15 identical titles and descriptions, creating minor internal keyword competition."
        },
        {
            "title": "25 Images With Overly Long, Keyword-Stuffed Alt Text Exceeding 100 Characters",
            "severity": "Low",
            "urls": "25 images site-wide (22.52%)",
            "impact": "Alt attributes on 25 images contain full paragraphs of text exceeding 100 characters, creating accessibility friction for screen readers and triggering search engine keyword-stuffing filters."
        },
        {
            "title": "Unnecessary URL Parameters Adding Noise to Crawl Budget",
            "severity": "Low",
            "urls": "12 parameter URLs site-wide",
            "impact": "Internal tracking parameters in navigation links generate duplicate crawl paths that consume bot resources."
        }
    ],
    "scope_of_improvement": [
        {
            "bold_prefix": "1. Search Snippet Optimization & CTR Recovery (The 50x Growth Lever): ",
            "text": "Rewriting titles and meta descriptions across the top 20 impression pages in GSC to fit strictly within 55–60 characters / 155 characters. Replacing generic phrases with compelling numerical benchmarks (e.g. 'Facebook Ads Cost in India: 2026 CPC & CPL Benchmarks') to capture immediate traffic from the 205,940 impressions currently earning a 0.13% CTR."
        },
        {
            "bold_prefix": "2. Next.js Canonical Architecture & Parameter Governance: ",
            "text": "Deploying self-referencing canonical tags site-wide via Next.js metadata ('alternates.canonical') across all 131 routes, and ensuring all 12 '/contact-us/?service=*' parameter URLs canonicalize strictly to the clean 'https://paidmediaworld.com/contact-us/' route."
        },
        {
            "bold_prefix": "3. Crawl Hygiene & 404 Broken Link Remediation: ",
            "text": "Fixing the Cloudflare email protection link in global footer/author templates to eliminate 238 internal 404 errors, 301-redirecting or restoring the 6 broken pillar guides, and updating internal links to bypass 37 301 redirect hops."
        },
        {
            "bold_prefix": "4. Media Modernization & Core Web Vitals (CLS/LCP): ",
            "text": "Adding explicit HTML width and height dimensions across all 103 images to resolve Cumulative Layout Shift (CLS), and converting 93 oversized PNG/JPG assets into modern, responsive WebP/AVIF images."
        },
        {
            "bold_prefix": "5. E-E-A-T Authority, Local SEO & Security Hardening: ",
            "text": "Enhancing TechArticle schema with author credentials and verified LinkedIn sameAs links, creating dedicated high-converting landing pages for Kolkata healthcare agency queries (currently ranking #7–#10 with 0 clicks), and deploying standard security headers via Cloudflare Transform Rules."
        }
    ],
    "immediate_fixations": [
        "Rewrite Snippet for #1 Traffic Asset (/cost-of-facebook-ads-in-india-...): Shorten title to 58 characters ('Facebook Ads Cost in India: 2026 Benchmarks (CPC, CPL, CPA)'), remove '&amp;#038;', and deploy a high-CTR 155-character meta description to immediately monetize 100,917 Page 1 impressions.",
        "Deploy Self-Referencing Canonical Tags in Next.js layout.tsx: Implement 'metadata.alternates.canonical' across all routes to resolve the 99.2% canonical void.",
        "Fix Broken Cloudflare Email Protection Link (238 Inlinks): Update global footer and author templates to remove or fix '/cdn-cgi/l/email-protection' and eliminate 238 internal 404 errors.",
        "301 Redirect or Restore 6 Broken Pillar Guides: Map the 6 broken 404 URLs (/the-ultimate-google-ads-guide-..., /predictive-profitability-..., etc.) to live resolving routes.",
        "Sanitize Raw HTML Entities in 23 Page Titles: Update Next.js title generation to decode entities and eliminate '&amp;#038;' and '&#038;' from search snippets.",
        "Self-Canonicalize the 12 Contact Parameter URLs: Set canonical tags on '/contact-us/?service=*' to point strictly to 'https://paidmediaworld.com/contact-us/'.",
        "Rewrite Titles for Kolkata Healthcare Agency Pages: Shorten and optimize titles for the diagnostic/hospital marketing pages ranking on Page 1 (Pos 7–10) to capture local lead volume.",
        "Update Internal Links to Bypass 37 301 Redirect Hops: Point internal links directly to their final destination URLs to preserve link equity and eliminate crawl latency.",
        "Add Explicit Width & Height Attributes to Images: Inject dimensions on the 103 image elements (including all 10 homepage images) to stabilize CLS.",
        "Deploy Security Headers via Cloudflare Transform Rules: Configure HSTS, X-Frame-Options, X-Content-Type-Options: nosniff, and Referrer-Policy at the Cloudflare edge."
    ],
    "roadmap": [
        {
            "phase": "Phase 1: Emergency CTR Recovery, Canonicals & 404 Remediation\n(Days 1–15)",
            "objectives": "Deploy Next.js canonical tags site-wide, rewrite titles and meta descriptions for top 20 GSC impression pages (especially #1 asset), fix Cloudflare email protection 404 (238 inlinks), redirect 6 broken pillar guides, sanitize HTML entities, and inject Cloudflare security headers.",
            "milestone": "100% canonical coverage; 0 internal 404 errors; entity bugs eliminated; immediate CTR inflection on top 100k impression asset"
        },
        {
            "phase": "Phase 2: On-Page Architecture, Media & Core Web Vitals\n(Days 16–45)",
            "objectives": "Shorten oversized titles (> 60 chars) across remaining 106 pages, add explicit image dimensions across 103 assets, convert 93 images to WebP, add unique 150+ word intro copy to 10 category hubs, and update internal links to remove 37 301 hops.",
            "milestone": "0 truncated titles in SERPs; passed Core Web Vitals CLS benchmark; streamlined crawl path"
        },
        {
            "phase": "Phase 3: E-E-A-T Schema Expansion & Pillar Content Strategy\n(Days 46–90)",
            "objectives": "Add comprehensive author authority credentials and sameAs links to TechArticle schema, deploy FAQPage schema across pillar guides, build dedicated local landing pages for Kolkata healthcare search clusters, and expand thin calculators.",
            "milestone": "Rich FAQ snippets active in SERPs; local healthcare lead generation active; enhanced topical authority"
        },
        {
            "phase": "Phase 4: Search Console Measurement & AI Search Optimization\n(Days 90+)",
            "objectives": "Track non-brand organic click growth in GSC (targeting overall CTR > 1.0%), monitor brand citations and entity recognition across AI search engines (ChatGPT, Perplexity, Google AI Overviews), and re-evaluate technical health rubric score.",
            "milestone": "5x–10x organic click growth from existing impression base; verified AI search citations"
        }
    ]
}

# 2. Save audit_data.json
json_path = os.path.join(out_dir, "audit_data.json")
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(audit_data, f, indent=2)
print(f"[+] Saved audit_data.json: {json_path}")

# 3. Create 04_issues_log.csv
issues_file = os.path.join(out_dir, "04_issues_log.csv")
with open(issues_file, 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(["Issue Title", "Severity", "Affected URLs", "Observed Defect & Impact"])
    for iss in audit_data["issues"]:
        w.writerow([iss["title"], iss["severity"], iss["urls"], iss["impact"]])
print(f"[+] Saved 04_issues_log.csv: {issues_file}")

# 4. Create 10_roadmap_30_60_90.md
rm_file = os.path.join(out_dir, "10_roadmap_30_60_90.md")
with open(rm_file, 'w', encoding='utf-8') as f:
    f.write("""# Paid Media World — 30-60-90 Day SEO & Organic Growth Roadmap

## Phase 1: Emergency CTR Recovery, Canonicals & 404 Remediation (Days 1–15)
- [ ] Deploy self-referencing canonical tags in Next.js `layout.tsx` (`metadata.alternates.canonical`) across all 131 routes.
- [ ] Rewrite snippet for #1 traffic asset (`/cost-of-facebook-ads-in-india-guide-benchmarks-for-leads-sales/`): title to < 60 chars, remove `&amp;#038;`, and craft a high-CTR 155-char meta description to monetize 100,917 Page 1 impressions.
- [ ] Rewrite titles and meta descriptions for the top 20 impression pages in GSC to stop SERP truncation.
- [ ] Fix broken Cloudflare email protection link (`/cdn-cgi/l/email-protection`) across 238 inlinks in global footer and author templates.
- [ ] 301-redirect or restore the 6 broken high-value pillar guides (`/the-ultimate-google-ads-guide-...`, `/predictive-profitability-...`, etc.).
- [ ] Sanitize raw HTML entities (`&amp;#038;` and `&#038;`) in Next.js title generation templates across 23 articles.
- [ ] Set canonical tags on the 12 `/contact-us/?service=*` parameter URLs to point strictly to `https://paidmediaworld.com/contact-us/`.
- [ ] Rewrite titles for Kolkata healthcare agency pages (ranking in positions 7–10 with 0 clicks) to capture local lead volume.
- [ ] Update internal navigation and body links to bypass 37 301 redirect hops.
- [ ] Deploy standard HTTP security headers (HSTS, CSP, X-Frame-Options, nosniff, Referrer-Policy) via Cloudflare Transform Rules.

## Phase 2: On-Page Architecture, Media & Core Web Vitals (Days 16–45)
- [ ] Shorten oversized titles (> 60 characters) across the remaining 106 indexable pages.
- [ ] Add explicit HTML width and height attributes across all 103 image elements (including all 10 homepage images) to stabilize CLS.
- [ ] Convert 93 oversized PNG and JPG images (> 100KB) to modern, responsive WebP/AVIF format.
- [ ] Add unique 150+ word introductory editorial copy and custom meta descriptions to all 10 thin category archive hubs.
- [ ] Refactor long `<h1>` headings exceeding 70 characters on 72 pages to sharpen topical keyword focus.
- [ ] Clean up heading outline structure across 40 pages with non-sequential heading hierarchy.

## Phase 3: E-E-A-T Schema Expansion & Pillar Content Strategy (Days 46–90)
- [ ] Upgrade TechArticle JSON-LD schema with author `sameAs` authority links to verified LinkedIn profiles, awards, and bios.
- [ ] Deploy Schema.org `FAQPage` JSON-LD markup on major pillar guides to capture enhanced SERP real estate.
- [ ] Build dedicated, conversion-optimized local landing pages for Kolkata healthcare and clinic PPC services.
- [ ] Expand thin interactive calculator tools with in-depth methodological explainers and industry benchmarks.

## Phase 4: Search Console Measurement & AI Search Optimization (Days 90+)
- [ ] Monitor Google Search Console performance data, evaluating organic click growth and tracking overall CTR recovery toward > 1.0%.
- [ ] Measure local organic lead inquiries generated from optimized Kolkata healthcare landing pages.
- [ ] Track brand citations, entity recognition, and accuracy across AI search engines (ChatGPT, Perplexity, Google AI Overviews).
- [ ] Re-evaluate internal technical health rubric score against the 39/100 baseline.
""")
print(f"[+] Saved 10_roadmap_30_60_90.md: {rm_file}")

# 5. Build Reports via Universal Engine
from generate_issue_only_report_engine import build_docx_report, build_pdf_report

docx_path = os.path.join(out_dir, "PaidMediaWorld_SEO_Audit_Report.docx")
build_docx_report(audit_data, docx_path)

pdf_path = os.path.join(out_dir, "PaidMediaWorld_SEO_Audit_Report.pdf")
build_pdf_report(audit_data, pdf_path)

# Mirror to root
shutil.copyfile(docx_path, "PaidMediaWorld_SEO_Audit_Report.docx")
shutil.copyfile(pdf_path, "PaidMediaWorld_SEO_Audit_Report.pdf")
print("[+] Mirrored reports to root successfully!")
