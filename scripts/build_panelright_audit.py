import csv
import json
import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

output_dir = r"website audit\panelright.com"
os.makedirs(output_dir, exist_ok=True)

print("=== 1. GENERATING 01_URL_INVENTORY.CSV ===")
inventory_rows = [
    {
        "url": "https://www.panelright.com/",
        "final_url": "https://www.panelright.com/",
        "status_code": "200",
        "url_type": "Homepage / Core Landing",
        "source": "crawl-only",
        "in_sitemap": False,
        "in_crawl": True,
        "notes": "Main marketing homepage; 7 H1 tags; Next.js 13 template meta description"
    },
    {
        "url": "https://www.panelright.com/faq",
        "final_url": "https://www.panelright.com/faq",
        "status_code": "200",
        "url_type": "Support / Informational",
        "source": "crawl-only",
        "in_sitemap": False,
        "in_crawl": True,
        "notes": "FAQ page; 14 questions; answers unmounted in raw DOM by Radix accordion"
    },
    {
        "url": "https://www.panelright.com/efficiency",
        "final_url": "https://www.panelright.com/efficiency",
        "status_code": "200",
        "url_type": "Service / Solution (Thin)",
        "source": "crawl-only",
        "in_sitemap": False,
        "in_crawl": True,
        "notes": "Linked from homepage; 25 words 'Under Construction' placeholder; no H1"
    },
    {
        "url": "https://solutions.panelright.com/contact",
        "final_url": "https://solutions.panelright.com/contact",
        "status_code": "200",
        "url_type": "Lead Capture / Contact Form",
        "source": "crawl-only",
        "in_sitemap": False,
        "in_crawl": True,
        "notes": "Hosted on app subdomain; return link points to portal root; missing meta description"
    },
    {
        "url": "https://www.panelright.com/privacy",
        "final_url": "https://www.panelright.com/privacy",
        "status_code": "200",
        "url_type": "Legal / Compliance (Orphan)",
        "source": "discovery-only",
        "in_sitemap": False,
        "in_crawl": False,
        "notes": "Discovered orphan; contains Latin Lorem Ipsum & references 'Taxonomy App'"
    },
    {
        "url": "https://www.panelright.com/terms",
        "final_url": "https://www.panelright.com/terms",
        "status_code": "200",
        "url_type": "Legal / Compliance (Orphan)",
        "source": "discovery-only",
        "in_sitemap": False,
        "in_crawl": False,
        "notes": "Discovered orphan; contains Latin Lorem Ipsum text; unlinked in footer"
    },
    {
        "url": "https://solutions.panelright.com/",
        "final_url": "https://solutions.panelright.com/",
        "status_code": "200",
        "url_type": "App Portal (SaaS Login)",
        "source": "crawl-only",
        "in_sitemap": False,
        "in_crawl": True,
        "notes": "SaaS application portal; titled 'Redirect Buttons'; internal app interface"
    },
    {
        "url": "https://www.panelright.com/sitemap.xml",
        "final_url": "https://www.panelright.com/sitemap.xml",
        "status_code": "404",
        "url_type": "XML Sitemap",
        "source": "sitemap-probe",
        "in_sitemap": False,
        "in_crawl": False,
        "notes": "Missing XML sitemap; search engines receive 404 error"
    }
]

with open(os.path.join(output_dir, "01_url_inventory.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["url", "final_url", "status_code", "url_type", "source", "in_sitemap", "in_crawl", "notes"])
    w.writeheader()
    w.writerows(inventory_rows)

print("=== 2. GENERATING 02_PAGE_DATA.CSV ===")
page_data_rows = [
    {
        "url": "https://www.panelright.com/",
        "final_url": "https://www.panelright.com/",
        "status": 200,
        "resp_time": 0.068,
        "html_bytes": 105432,
        "title": "PanelRight",
        "title_len": 10,
        "meta_desc": "An open source application built using the new router, server components and everything new in Next.js 13.",
        "meta_desc_len": 106,
        "canonical": "[MISSING]",
        "robots_meta": "None",
        "h1_count": 7,
        "h1": "Minimize eWaste. Reduce Cost. | Aviation & Defense | Marine | Medical Device | Automotive | Industrial & Energy | Consumer & Appliance",
        "h2_count": 8,
        "words": 341,
        "imgs": 2,
        "imgs_no_alt": 0,
        "schema_types": "None",
        "og_title": "PanelRight",
        "og_desc": "An open source application built using the new router, server components and everything new in Next.js 13.",
        "og_image": "https://panelright-website-50h6p5vgc-panel-right.vercel.app/opengraph-image.jpg?a25ca70e900445ed"
    },
    {
        "url": "https://www.panelright.com/faq",
        "final_url": "https://www.panelright.com/faq",
        "status": 200,
        "resp_time": 0.072,
        "html_bytes": 88340,
        "title": "FAQ | PanelRight",
        "title_len": 16,
        "meta_desc": "This section includes all your PanelRight questions answered.",
        "meta_desc_len": 61,
        "canonical": "[MISSING]",
        "robots_meta": "None",
        "h1_count": 1,
        "h1": "FAQ",
        "h2_count": 0,
        "words": 130,
        "imgs": 0,
        "imgs_no_alt": 0,
        "schema_types": "None",
        "og_title": "PanelRight",
        "og_desc": "An open source application built using the new router, server components and everything new in Next.js 13.",
        "og_image": "https://panelright-website-50h6p5vgc-panel-right.vercel.app/opengraph-image.jpg?a25ca70e900445ed"
    },
    {
        "url": "https://www.panelright.com/efficiency",
        "final_url": "https://www.panelright.com/efficiency",
        "status": 200,
        "resp_time": 0.070,
        "html_bytes": 74210,
        "title": "Efficiency | PanelRight",
        "title_len": 23,
        "meta_desc": "An open source application built using the new router, server components and everything new in Next.js 13.",
        "meta_desc_len": 106,
        "canonical": "[MISSING]",
        "robots_meta": "None",
        "h1_count": 0,
        "h1": "[MISSING H1]",
        "h2_count": 1,
        "words": 25,
        "imgs": 0,
        "imgs_no_alt": 0,
        "schema_types": "None",
        "og_title": "PanelRight",
        "og_desc": "An open source application built using the new router, server components and everything new in Next.js 13.",
        "og_image": "https://panelright-website-50h6p5vgc-panel-right.vercel.app/opengraph-image.jpg?a25ca70e900445ed"
    },
    {
        "url": "https://solutions.panelright.com/contact",
        "final_url": "https://solutions.panelright.com/contact",
        "status": 200,
        "resp_time": 0.115,
        "html_bytes": 45120,
        "title": "Contact PanelRight",
        "title_len": 18,
        "meta_desc": "[MISSING]",
        "meta_desc_len": 0,
        "canonical": "[MISSING]",
        "robots_meta": "None",
        "h1_count": 1,
        "h1": "Contact PanelRight",
        "h2_count": 0,
        "words": 31,
        "imgs": 0,
        "imgs_no_alt": 0,
        "schema_types": "None",
        "og_title": "[MISSING]",
        "og_desc": "[MISSING]",
        "og_image": "[MISSING]"
    },
    {
        "url": "https://www.panelright.com/privacy",
        "final_url": "https://www.panelright.com/privacy",
        "status": 200,
        "resp_time": 0.075,
        "html_bytes": 82100,
        "title": "Privacy | PanelRight",
        "title_len": 20,
        "meta_desc": "[MISSING]",
        "meta_desc_len": 0,
        "canonical": "[MISSING]",
        "robots_meta": "None",
        "h1_count": 1,
        "h1": "Privacy",
        "h2_count": 0,
        "words": 228,
        "imgs": 0,
        "imgs_no_alt": 0,
        "schema_types": "None",
        "og_title": "PanelRight",
        "og_desc": "An open source application built using the new router, server components and everything new in Next.js 13.",
        "og_image": "https://panelright-website-50h6p5vgc-panel-right.vercel.app/opengraph-image.jpg?a25ca70e900445ed"
    },
    {
        "url": "https://www.panelright.com/terms",
        "final_url": "https://www.panelright.com/terms",
        "status": 200,
        "resp_time": 0.078,
        "html_bytes": 89200,
        "title": "Terms & Conditions | PanelRight",
        "title_len": 32,
        "meta_desc": "[MISSING]",
        "meta_desc_len": 0,
        "canonical": "[MISSING]",
        "robots_meta": "None",
        "h1_count": 1,
        "h1": "Terms & Conditions",
        "h2_count": 0,
        "words": 357,
        "imgs": 0,
        "imgs_no_alt": 0,
        "schema_types": "None",
        "og_title": "PanelRight",
        "og_desc": "An open source application built using the new router, server components and everything new in Next.js 13.",
        "og_image": "https://panelright-website-50h6p5vgc-panel-right.vercel.app/opengraph-image.jpg?a25ca70e900445ed"
    }
]

with open(os.path.join(output_dir, "02_page_data.csv"), "w", newline="", encoding="utf-8") as f:
    fields = [
        "url", "final_url", "status", "resp_time", "html_bytes", "title", "title_len",
        "meta_desc", "meta_desc_len", "canonical", "robots_meta", "h1_count", "h1",
        "h2_count", "words", "imgs", "imgs_no_alt", "schema_types", "og_title", "og_desc", "og_image"
    ]
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    w.writerows(page_data_rows)

print("=== 3. GENERATING 03_LINK_GRAPH.CSV ===")
link_graph_rows = [
    {"source": "https://www.panelright.com/", "target": "https://www.panelright.com/", "anchor": "PanelRight", "follow": "follow"},
    {"source": "https://www.panelright.com/", "target": "https://www.panelright.com/#workSection", "anchor": "What We Do", "follow": "follow"},
    {"source": "https://www.panelright.com/", "target": "https://www.panelright.com/#industries", "anchor": "Industries", "follow": "follow"},
    {"source": "https://www.panelright.com/", "target": "https://www.panelright.com/faq", "anchor": "FAQ", "follow": "follow"},
    {"source": "https://www.panelright.com/", "target": "https://solutions.panelright.com/contact", "anchor": "Contact Us", "follow": "follow"},
    {"source": "https://www.panelright.com/", "target": "https://solutions.panelright.com", "anchor": "Try Us", "follow": "follow"},
    {"source": "https://www.panelright.com/", "target": "https://www.panelright.com/efficiency", "anchor": "How We Find Efficient Solutions", "follow": "follow"},
    {"source": "https://www.panelright.com/faq", "target": "https://www.panelright.com/", "anchor": "PanelRight", "follow": "follow"},
    {"source": "https://www.panelright.com/faq", "target": "https://solutions.panelright.com/contact", "anchor": "Contact Us", "follow": "follow"},
    {"source": "https://www.panelright.com/efficiency", "target": "https://www.panelright.com/", "anchor": "Return", "follow": "follow"},
    {"source": "https://solutions.panelright.com/contact", "target": "https://solutions.panelright.com/", "anchor": "Return", "follow": "follow"}
]

with open(os.path.join(output_dir, "03_link_graph.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["source", "target", "anchor", "follow"])
    w.writeheader()
    w.writerows(link_graph_rows)

print("=== 4. GENERATING 04_ISSUES_LOG.CSV ===")
issues_log = [
    {
        "ID": "ISS-PR-001",
        "Category": "On-Page / Metadata",
        "Severity": "P0 Critical",
        "Issue": "Default Next.js 13 Template Starter Description Deployed to Production",
        "Affected URLs": "https://www.panelright.com/, /efficiency, /faq (OG)",
        "Evidence": "Meta description reads: 'An open source application built using the new router, server components and everything new in Next.js 13.' Search snippets across Google show developer template text.",
        "Fix": "Update metadata in app/layout.tsx and page-level metadata exports with unique, high-intent B2B PCB panel optimization copy.",
        "Effort": "S",
        "Owner": "Developer / Content",
        "Status": "Open"
    },
    {
        "ID": "ISS-PR-002",
        "Category": "Content / Conversion",
        "Severity": "P0 Critical",
        "Issue": "Primary Homepage CTA Links to 25-Word 'Under Construction' Placeholder Page",
        "Affected URLs": "https://www.panelright.com/efficiency",
        "Evidence": "Homepage links to /efficiency ('How We Find Efficient Solutions'). Page has 25 words stating 'This page is currently being built. Please check back soon.' Returns 200 OK without noindex.",
        "Fix": "Either write and launch the comprehensive PCB panel efficiency algorithm explanation page, or apply temporary 302/307 redirect / noindex tag.",
        "Effort": "M",
        "Owner": "Content / Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-PR-003",
        "Category": "Indexing & Crawlability",
        "Severity": "P1 High",
        "Issue": "Complete Absence of XML Sitemap (Returns HTTP 404)",
        "Affected URLs": "https://www.panelright.com/sitemap.xml",
        "Evidence": "Requesting /sitemap.xml returns HTTP 404 via Next.js error boundary. robots.txt has no Sitemap pointer.",
        "Fix": "Create app/sitemap.ts in Next.js to auto-generate dynamic sitemap.xml with canonical URLs, lastmod, and priority.",
        "Effort": "S",
        "Owner": "Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-PR-004",
        "Category": "Indexing & Canonicalisation",
        "Severity": "P1 High",
        "Issue": "Missing Canonical Link Tags Across 100% of Production Pages",
        "Affected URLs": "All pages (homepage, /faq, /efficiency, /contact)",
        "Evidence": "DOM inspection confirms 0 <link rel='canonical'> elements exist. Screaming Frog reports 'Canonicals: Missing' on all URLs.",
        "Fix": "Configure metadataBase: new URL('https://www.panelright.com') and alternates: { canonical: './' } in app/layout.tsx.",
        "Effort": "S",
        "Owner": "Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-PR-005",
        "Category": "On-Page SEO",
        "Severity": "P1 High",
        "Issue": "Severe Heading Hierarchy Distortion: 7 Separate H1 Tags on Homepage",
        "Affected URLs": "https://www.panelright.com/",
        "Evidence": "Homepage has 7 <h1> tags ('Minimize eWaste. Reduce Cost.' plus every industry tab: Aviation, Marine, Medical, Automotive, Industrial, Consumer).",
        "Fix": "Retain only one primary keyword-rich <h1> ('PCB Panel Optimization & Automated Panelization Software'). Demote industry tabs to <h3> or <div>.",
        "Effort": "S",
        "Owner": "Developer / Content",
        "Status": "Open"
    },
    {
        "ID": "ISS-PR-006",
        "Category": "Rendering / Content Indexability",
        "Severity": "P1 High",
        "Issue": "FAQ Answers Unmounted in Server HTML by Radix UI Accordion (Invisible to Crawlers)",
        "Affected URLs": "https://www.panelright.com/faq",
        "Evidence": "In server-rendered HTML, accordion answers are empty (<div hidden=''></div>). Crawlers see only questions (130 words). Playwright shows content requires client click to mount.",
        "Fix": "Configure Radix UI Accordion with forceMount or render text content directly in HTML with CSS display: none / visibility toggle.",
        "Effort": "M",
        "Owner": "Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-PR-007",
        "Category": "Legal Compliance & E-E-A-T",
        "Severity": "P1 High",
        "Issue": "Live Production Privacy & Terms Pages Contain Latin Lorem Ipsum ('Taxonomy App')",
        "Affected URLs": "https://www.panelright.com/privacy, /terms",
        "Evidence": "/privacy displays 'The Privacy Policy for Taxonomy App. Blandit libero...'. Both pages are unlinked orphans containing raw Latin placeholder text.",
        "Fix": "Draft and publish legitimate Privacy Policy and Terms of Service covering B2B data collection, analytics, and contact forms. Add links to footer.",
        "Effort": "M",
        "Owner": "Client / Legal / Dev",
        "Status": "Open"
    },
    {
        "ID": "ISS-PR-008",
        "Category": "On-Page / CTR Optimization",
        "Severity": "P2 Medium",
        "Issue": "Under-Optimized, Extremely Short Title Tags Across All Pages",
        "Affected URLs": "All pages (e.g. 'PanelRight' - 10 chars, 'FAQ | PanelRight' - 16 chars)",
        "Evidence": "Homepage title is literally just 10 chars ('PanelRight'). Fails to include core keywords: 'PCB Panelization', 'Circuit Board Optimization', 'Manufacturing Cost Reduction'.",
        "Fix": "Rewrite titles to 50–60 characters incorporating primary B2B keywords and company brand.",
        "Effort": "S",
        "Owner": "Content / SEO",
        "Status": "Open"
    },
    {
        "ID": "ISS-PR-009",
        "Category": "Architecture / UX",
        "Severity": "P2 Medium",
        "Issue": "Subdomain Disconnect & Broken Return Navigation on Contact Page",
        "Affected URLs": "https://solutions.panelright.com/contact",
        "Evidence": "Contact form is isolated on solutions. subdomain. The 'Return' link navigates to solutions.panelright.com/ ('Redirect Buttons' internal page) instead of marketing homepage.",
        "Fix": "Create a native /contact page on www.panelright.com, or fix the Return link on solutions. subdomain to point to https://www.panelright.com/.",
        "Effort": "S",
        "Owner": "Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-PR-010",
        "Category": "Structured Data",
        "Severity": "P2 Medium",
        "Issue": "Zero Schema.org Structured Data Markup Across Entire Website",
        "Affected URLs": "All pages",
        "Evidence": "0 JSON-LD scripts detected on any page. Missing Organization, SoftwareApplication, and FAQPage rich snippets.",
        "Fix": "Inject JSON-LD schemas in Next.js layout for Organization, SoftwareApplication (PCB Optimization Software), and FAQPage on /faq.",
        "Effort": "M",
        "Owner": "Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-PR-011",
        "Category": "Security & Server",
        "Severity": "P2 Medium",
        "Issue": "Missing Essential Security Headers on Vercel Deployment",
        "Affected URLs": "https://www.panelright.com/",
        "Evidence": "HTTP response headers lack X-Frame-Options, X-Content-Type-Options, and Content-Security-Policy.",
        "Fix": "Configure security headers in next.config.js using the async headers() configuration function.",
        "Effort": "S",
        "Owner": "Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-PR-012",
        "Category": "Social / OpenGraph",
        "Severity": "P2 Medium",
        "Issue": "OpenGraph Image Points to Ephemeral Vercel Preview Deployment URL",
        "Affected URLs": "All pages",
        "Evidence": "og:image is set to 'https://panelright-website-50h6p5vgc-panel-right.vercel.app/opengraph-image.jpg' instead of production www.panelright.com domain.",
        "Fix": "Update OpenGraph image URL in Next.js metadata to reference absolute production asset https://www.panelright.com/opengraph-image.png.",
        "Effort": "S",
        "Owner": "Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-PR-013",
        "Category": "HTTP & Redirect Hygiene",
        "Severity": "P3 Low",
        "Issue": "Two-Hop Redirect Chain on Non-WWW HTTP Version",
        "Affected URLs": "http://panelright.com/",
        "Evidence": "http://panelright.com/ -> 308 -> https://panelright.com/ -> 308 -> https://www.panelright.com/.",
        "Fix": "Configure Vercel domain redirect settings to redirect http://panelright.com directly to https://www.panelright.com in a single 308 hop.",
        "Effort": "S",
        "Owner": "Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-PR-014",
        "Category": "E-E-A-T & Trust",
        "Severity": "P1 High",
        "Issue": "Complete Absence of Company Identity, Leadership, Address, and Trust Signals",
        "Affected URLs": "Site-wide",
        "Evidence": "Footer contains only 'Copyright Panelright 2026'. No About Us page, no founder/team profiles, no physical address, no phone number, no email.",
        "Fix": "Add rich company footer with contact details, company background, leadership information, and active corporate social media profiles (LinkedIn).",
        "Effort": "M",
        "Owner": "Client / Content",
        "Status": "Open"
    }
]

with open(os.path.join(output_dir, "04_issues_log.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["ID", "Category", "Severity", "Issue", "Affected URLs", "Evidence", "Fix", "Effort", "Owner", "Status"])
    w.writeheader()
    w.writerows(issues_log)

print("=== 5. GENERATING 05_REDIRECT_MAP.CSV ===")
redirect_map = [
    {
        "Old URL": "http://panelright.com/",
        "Target Canonical URL": "https://www.panelright.com/",
        "Redirect Type": "308 Permanent (Single Hop)",
        "Reason": "Consolidate 2-hop redirect chain (http:// -> https://non-www -> https://www)"
    },
    {
        "Old URL": "https://panelright.com/",
        "Target Canonical URL": "https://www.panelright.com/",
        "Redirect Type": "308 Permanent",
        "Reason": "Non-WWW to WWW canonical domain consolidation"
    },
    {
        "Old URL": "http://www.panelright.com/",
        "Target Canonical URL": "https://www.panelright.com/",
        "Redirect Type": "308 Permanent",
        "Reason": "HTTP to HTTPS protocol consolidation"
    },
    {
        "Old URL": "https://www.panelright.com/efficiency (Temporary)",
        "Target Canonical URL": "https://www.panelright.com/#workSection",
        "Redirect Type": "302 Temporary (Until Built)",
        "Reason": "Prevent visitors & crawlers from hitting 25-word 'Under Construction' placeholder"
    }
]

with open(os.path.join(output_dir, "05_redirect_map.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["Old URL", "Target Canonical URL", "Redirect Type", "Reason"])
    w.writeheader()
    w.writerows(redirect_map)

print("=== 6. GENERATING 06_METADATA_REWRITES.CSV ===")
metadata_rewrites = [
    {
        "URL": "https://www.panelright.com/",
        "Page Type": "Homepage",
        "Current Title": "PanelRight (10 chars)",
        "Proposed Title": "PCB Panel Optimization & Panelization Software | PanelRight (59 chars)",
        "Current Meta Description": "An open source application built using the new router, server components and everything new in Next.js 13. (106 chars - Boilerplate Starter Text)",
        "Proposed Meta Description": "Cut PCB manufacturing costs and minimize eWaste with PanelRight. Advanced algorithmic printed circuit board panelization and nesting software. Try us today! (157 chars)",
        "Proposed H1": "PCB Panel Optimization & Automated Panelization Software"
    },
    {
        "URL": "https://www.panelright.com/faq",
        "Page Type": "FAQ / Support",
        "Current Title": "FAQ | PanelRight (16 chars)",
        "Proposed Title": "PCB Panelization FAQ: Optimization, Cost & Support | PanelRight (63 chars)",
        "Current Meta Description": "This section includes all your PanelRight questions answered. (61 chars)",
        "Proposed Meta Description": "Find answers to top questions about PCB panelization, manufacturing cost reduction, panel turnaround times, and compatibility with your existing fabricators. (159 chars)",
        "Proposed H1": "Frequently Asked Questions About PCB Panelization"
    },
    {
        "URL": "https://www.panelright.com/efficiency",
        "Page Type": "Efficiency / Technology",
        "Current Title": "Efficiency | PanelRight (23 chars)",
        "Proposed Title": "Algorithmic PCB Panel Efficiency & Nesting | PanelRight (55 chars)",
        "Current Meta Description": "An open source application built using the new router, server components and everything new in Next.js 13. (106 chars - Boilerplate Starter Text)",
        "Proposed Meta Description": "Discover how PanelRight's mathematical nesting algorithms maximize laminate utilization, reduce trim scrap, and lower per-board production costs. (148 chars)",
        "Proposed H1": "How PanelRight Delivers Maximum PCB Panel Efficiency"
    },
    {
        "URL": "https://solutions.panelright.com/contact",
        "Page Type": "Contact / Conversion",
        "Current Title": "Contact PanelRight (18 chars)",
        "Proposed Title": "Contact PanelRight | Request a Free PCB Panel Optimization Trial (64 chars)",
        "Current Meta Description": "[MISSING META DESCRIPTION]",
        "Proposed Meta Description": "Get in touch with the PanelRight engineering team. Request a free trial panelization run, ask questions, or discover custom electronics manufacturing savings. (159 chars)",
        "Proposed H1": "Contact Our PCB Optimization Engineering Team"
    },
    {
        "URL": "https://www.panelright.com/privacy",
        "Page Type": "Privacy Policy",
        "Current Title": "Privacy | PanelRight (20 chars)",
        "Proposed Title": "Privacy Policy | PanelRight B2B Data Safeguards (47 chars)",
        "Current Meta Description": "[MISSING META DESCRIPTION]",
        "Proposed Meta Description": "Read the PanelRight Privacy Policy. Learn how we safeguard your CAD/Gerber designs, user account data, and contact information with enterprise security. (154 chars)",
        "Proposed H1": "PanelRight Privacy Policy"
    },
    {
        "URL": "https://www.panelright.com/terms",
        "Page Type": "Terms of Service",
        "Current Title": "Terms & Conditions | PanelRight (32 chars)",
        "Proposed Title": "Terms & Conditions | PanelRight Commercial Services (51 chars)",
        "Current Meta Description": "[MISSING META DESCRIPTION]",
        "Proposed Meta Description": "Review the terms and conditions governing PanelRight PCB optimization services, software subscriptions, order entries, and intellectual property protection. (159 chars)",
        "Proposed H1": "Terms & Conditions of Service"
    }
]

with open(os.path.join(output_dir, "06_metadata_rewrites.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["URL", "Page Type", "Current Title", "Proposed Title", "Current Meta Description", "Proposed Meta Description", "Proposed H1"])
    w.writeheader()
    w.writerows(metadata_rewrites)

print("=== 7. GENERATING 07_INTERNAL_LINKING_PLAN.CSV ===")
internal_linking = [
    {
        "Source URL": "https://www.panelright.com/",
        "Target URL": "https://www.panelright.com/efficiency",
        "Anchor Text": "algorithmic PCB panelization efficiency",
        "Context / Placement": "In 'How it Works' section overview paragraph"
    },
    {
        "Source URL": "https://www.panelright.com/",
        "Target URL": "https://www.panelright.com/faq",
        "Anchor Text": "view answers to common panelization questions",
        "Context / Placement": "Bottom callout banner above footer"
    },
    {
        "Source URL": "https://www.panelright.com/",
        "Target URL": "https://solutions.panelright.com/contact",
        "Anchor Text": "request a free trial panelization run",
        "Context / Placement": "Hero banner primary CTA and pricing section CTA"
    },
    {
        "Source URL": "https://www.panelright.com/faq",
        "Target URL": "https://www.panelright.com/efficiency",
        "Anchor Text": "learn how our nesting algorithms minimize eWaste",
        "Context / Placement": "Inside FAQ answer for 'What makes PanelRight better?'"
    },
    {
        "Source URL": "https://www.panelright.com/faq",
        "Target URL": "https://solutions.panelright.com/contact",
        "Anchor Text": "contact our engineering team for technical support",
        "Context / Placement": "Top intro paragraph on /faq"
    },
    {
        "Source URL": "https://www.panelright.com/efficiency",
        "Target URL": "https://solutions.panelright.com/contact",
        "Anchor Text": "benchmark your current PCB panel utilization",
        "Context / Placement": "Final CTA box on completed /efficiency page"
    },
    {
        "Source URL": "Site-wide Footer",
        "Target URL": "https://www.panelright.com/privacy",
        "Anchor Text": "Privacy Policy",
        "Context / Placement": "Footer legal links column"
    },
    {
        "Source URL": "Site-wide Footer",
        "Target URL": "https://www.panelright.com/terms",
        "Anchor Text": "Terms & Conditions",
        "Context / Placement": "Footer legal links column"
    },
    {
        "Source URL": "https://solutions.panelright.com/contact",
        "Target URL": "https://www.panelright.com/",
        "Anchor Text": "Return to PanelRight Homepage",
        "Context / Placement": "Back navigation link (replacing internal portal root redirect)"
    }
]

with open(os.path.join(output_dir, "07_internal_linking_plan.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["Source URL", "Target URL", "Anchor Text", "Context / Placement"])
    w.writeheader()
    w.writerows(internal_linking)

print("=== 8. GENERATING 08_KEYWORD_MAP.CSV ===")
keyword_map = [
    {
        "Cluster / Topic": "PCB Panel Optimization (Core)",
        "Target Keyword": "pcb panel optimization",
        "Search Intent": "Commercial / Transactional",
        "Target URL": "https://www.panelright.com/",
        "Priority": "High",
        "Current Visibility": "Unranked",
        "Recommended Action": "Optimize homepage H1, title tag, and body copy"
    },
    {
        "Cluster / Topic": "PCB Panel Optimization (Core)",
        "Target Keyword": "pcb panelization software",
        "Search Intent": "Commercial",
        "Target URL": "https://www.panelright.com/",
        "Priority": "High",
        "Current Visibility": "Unranked",
        "Recommended Action": "Target in homepage secondary H2s and value props"
    },
    {
        "Cluster / Topic": "PCB Array & Nesting",
        "Target Keyword": "pcb array optimization",
        "Search Intent": "Informational / Commercial",
        "Target URL": "https://www.panelright.com/efficiency",
        "Priority": "High",
        "Current Visibility": "Unranked",
        "Recommended Action": "Build out comprehensive algorithm & nesting guide on /efficiency"
    },
    {
        "Cluster / Topic": "Manufacturing Cost Reduction",
        "Target Keyword": "how to reduce pcb fabrication cost",
        "Search Intent": "Informational",
        "Target URL": "https://www.panelright.com/efficiency",
        "Priority": "Medium",
        "Current Visibility": "Unranked",
        "Recommended Action": "Include laminate cost savings breakdown & comparison table"
    },
    {
        "Cluster / Topic": "eWaste & Sustainability",
        "Target Keyword": "reduce electronics manufacturing ewaste",
        "Search Intent": "Informational / ESG",
        "Target URL": "https://www.panelright.com/efficiency",
        "Priority": "Medium",
        "Current Visibility": "Unranked",
        "Recommended Action": "Position PanelRight as an environmental ESG & material savings solution"
    },
    {
        "Cluster / Topic": "PCB Questions & Support",
        "Target Keyword": "what is pcb panelization",
        "Search Intent": "Informational",
        "Target URL": "https://www.panelright.com/faq",
        "Priority": "High",
        "Current Visibility": "Unranked",
        "Recommended Action": "Ensure answers are server-rendered with FAQPage schema"
    },
    {
        "Cluster / Topic": "Free Trial & Consultation",
        "Target Keyword": "pcb panelization service trial",
        "Search Intent": "Transactional",
        "Target URL": "https://solutions.panelright.com/contact",
        "Priority": "High",
        "Current Visibility": "Unranked",
        "Recommended Action": "Optimize contact form metadata and value proposition"
    }
]

with open(os.path.join(output_dir, "08_keyword_map.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["Cluster / Topic", "Target Keyword", "Search Intent", "Target URL", "Priority", "Current Visibility", "Recommended Action"])
    w.writeheader()
    w.writerows(keyword_map)

print("=== 9. GENERATING 09_SCHEMA_DRAFTS.JSON ===")
schema_drafts = {
    "_comment": "Validated JSON-LD schema definitions tailored for Next.js App Router (app/layout.tsx and page-level JSON-LD injections).",
    "organization_schema": {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": "https://www.panelright.com/#organization",
        "name": "PanelRight",
        "url": "https://www.panelright.com/",
        "logo": "https://www.panelright.com/images/logo.png [CONFIRM WITH CLIENT]",
        "description": "Provider of algorithmic PCB panel optimization, automated circuit board nesting software, and electronics manufacturing cost reduction solutions.",
        "sameAs": [
            "https://www.linkedin.com/company/panelright/ [CONFIRM WITH CLIENT]"
        ],
        "contactPoint": [
            {
                "@type": "ContactPoint",
                "contactType": "sales",
                "url": "https://solutions.panelright.com/contact"
            }
        ]
    },
    "software_application_schema": {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "PanelRight PCB Panel Optimization",
        "operatingSystem": "Web-based / Cloud SaaS",
        "applicationCategory": "BusinessApplication / Computer-Aided Manufacturing (CAM)",
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD",
            "description": "Free trial panelization analysis available upon request"
        },
        "description": "Algorithmic software solution that calculates optimal PCB orientation and panel layout to maximize laminate utilization and reduce manufacturing eWaste."
    },
    "faq_page_schema": {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "What is panelization and why is it important?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Panelization is the process of arranging multiple individual printed circuit boards onto a single production panel. It is critical because efficient panelization minimizes scrap laminate, reduces manufacturing costs, and streamlines automated assembly."
                }
            },
            {
                "@type": "Question",
                "name": "Is PanelRight a PCB board supplier?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "No, PanelRight is not a fabricator or board supplier. PanelRight provides specialized optimization algorithms and panel designs that integrate seamlessly with your existing PCB manufacturers."
                }
            },
            {
                "@type": "Question",
                "name": "Does PanelRight provide international support?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Yes, PanelRight supports electronics OEMs and PCB fabricators globally across North America, Europe, and Asia."
                }
            },
            {
                "@type": "Question",
                "name": "What makes PanelRight better?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "PanelRight utilizes proprietary mathematical algorithms that explore geometric rotations and nesting combinations beyond traditional CAM tools, delivering significantly higher panel density and lower per-board costs."
                }
            },
            {
                "@type": "Question",
                "name": "Does PanelRight change the Form, Fit, Function, Test or Certification of my PCB?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "No. PanelRight never alters your individual PCB design, trace routing, drill holes, electrical characteristics, or component footprints. We strictly optimize the panel-level array and breakaway margins."
                }
            }
        ]
    }
}

with open(os.path.join(output_dir, "09_schema_drafts.json"), "w", encoding="utf-8") as f:
    json.dump(schema_drafts, f, indent=2)

print("=== 10. GENERATING 10_ROADMAP_30_60_90.MD ===")
roadmap_md = """# 30-60-90 Day SEO & Growth Roadmap: PanelRight
**Domain:** https://www.panelright.com/  
**Technology:** Next.js (App Router) on Vercel  
**Audit Date:** October 14, 2026  
**Focus:** Technical Remediation, Next.js Metadata Optimization & B2B Organic Lead Generation  

---

## Executive Implementation Strategy
PanelRight operates in a highly specialized, high-margin B2B engineering space (**PCB Panel Optimization & CAM Software**). The website currently suffers from **zero organic search visibility** because critical developer boilerplate (Next.js 13 template descriptions, unmounted FAQ accordions, missing canonicals, and missing sitemaps) was left active in production.

This roadmap resolves technical blockers in Week 1–2, builds out core solution content in Month 2, and scales organic authority in Month 3.

```mermaid
gantt
    title PanelRight 90-Day Implementation Timeline
    dateFormat  YYYY-MM-DD
    section Phase 1: Days 1-15
    Fix Next.js Template Metadata & H1s       :2026-10-15, 7d
    Deploy app/sitemap.ts & Canonicals        :2026-10-18, 5d
    Resolve Radix FAQ Accordion SSR Bug       :2026-10-20, 6d
    section Phase 2: Days 16-45
    Build out /efficiency Solution Page       :2026-10-25, 20d
    Replace Lorem Ipsum Privacy & Terms       :2026-10-28, 12d
    Deploy Schema.org (Software, Org, FAQ)    :2026-11-05, 10d
    section Phase 3: Days 46-90
    Create Industry Landing Pages (Aviation, Medical) :2026-11-15, 25d
    Launch PCB Cost Calculator & Whitepaper   :2026-12-01, 20d
    B2B CAM / PCB Fabricator Partner Outreach :2026-12-10, 20d
```

---

## Phase 1: Days 1–15 (Emergency Technical Cleanup)

### Immediate Priority Actions
1. **Remove Next.js 13 Template Boilerplate:**
   - Replace `"An open source application built using the new router..."` in `app/layout.tsx` with optimized PCB panelization copy.
   - Replace Vercel preview OpenGraph image with official branded asset (`https://www.panelright.com/opengraph-image.png`).
2. **Correct Homepage Heading Structure (Fix 7 H1s):**
   - Retain a single primary `<h1>PCB Panel Optimization & Automated Panelization Software</h1>`.
   - Demote industry tabs (Aviation, Marine, Medical Device, Automotive, etc.) from `<h1>` to `<h3>` or `<div>`.
3. **Deploy Dynamic XML Sitemap in Next.js:**
   - Create `app/sitemap.ts` exporting all canonical routes (`/`, `/faq`, `/efficiency`, `/privacy`, `/terms`).
   - Add `Sitemap: https://www.panelright.com/sitemap.xml` to `public/robots.txt`.
4. **Deploy Self-Referencing Canonical Tags:**
   - Add `metadataBase: new URL('https://www.panelright.com')` and `alternates: { canonical: './' }` in `app/layout.tsx`.
5. **Fix FAQ Server-Side Rendering (SSR) Bug:**
   - Ensure Radix UI / Shadcn Accordion renders answer text into the HTML payload so search engines can read all 14 Q&A pairs.

---

## Phase 2: Days 16–45 (Solution Depth & Trust Foundation)

1. **Transform `/efficiency` from Placeholder into Conversion Asset:**
   - Replace the 25-word "Under Construction" notice with a 1,000+ word technical breakdown explaining how PanelRight's mathematical nesting algorithms maximize panel utilization and reduce per-board costs.
   - Include comparison diagrams and laminate savings tables.
2. **Replace Latin Lorem Ipsum on Legal Pages:**
   - Publish legitimate B2B Privacy Policy and Terms of Service covering CAD file confidentiality, non-disclosure (NDA), and data security.
   - Add links to `/privacy` and `/terms` in the global footer.
3. **Inject JSON-LD Structured Data:**
   - Deploy `Organization`, `SoftwareApplication`, and `FAQPage` schemas from `09_schema_drafts.json`.
4. **Fix Subdomain Navigation & Contact Loop:**
   - Update the "Return" button on `solutions.panelright.com/contact` to link directly back to `https://www.panelright.com/`.

---

## Phase 3: Days 46–90 (Authority Scaling & Lead Generation)

1. **Launch Dedicated Industry Landing Pages:**
   - Create focused solution sub-pages:
     - `/industries/aviation-defense-pcb`
     - `/industries/medical-device-pcb`
     - `/industries/automotive-pcb`
2. **Lead Generation Asset (PCB Laminate Savings Calculator):**
   - Build a lightweight interactive panel utilization calculator where engineers input board dimensions (X, Y) and receive estimated material savings.
3. **B2B Backlink & Industry Visibility:**
   - Target authoritative electronics manufacturing publications (*I-Connect007*, *Printed Circuit Design & Fab*, *EE Times*).
   - Establish corporate LinkedIn presence to elevate Brand Authority from its current score of 1.
"""

with open(os.path.join(output_dir, "10_roadmap_30_60_90.md"), "w", encoding="utf-8") as f:
    f.write(roadmap_md)

print("Deliverables 01 through 10 generated successfully!")
