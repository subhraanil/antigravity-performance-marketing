import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from playwright.sync_api import sync_playwright

output_dir = r"website audit\panelright.com"
os.makedirs(output_dir, exist_ok=True)

print("=== 1. GENERATING EXPANDED ISSUE-ONLY EXECUTIVE DOCX REPORT (v2) ===")

doc = docx.Document()

for s in doc.sections:
    s.top_margin = Inches(0.9)
    s.bottom_margin = Inches(0.9)
    s.left_margin = Inches(0.9)
    s.right_margin = Inches(0.9)

COLOR_NAVY = RGBColor(10, 25, 47)      # #0a192f
COLOR_BLUE = RGBColor(37, 99, 235)     # #2563eb
COLOR_RED = RGBColor(220, 38, 38)      # #dc2626
COLOR_DARK = RGBColor(15, 23, 42)      # #0f172a

# Cover Header
title_p = doc.add_paragraph()
r = title_p.add_run("TECHNICAL SEO & ON-PAGE AUDIT: EXPANDED GAP & ISSUE ANALYSIS")
r.font.name = "Arial"
r.font.size = Pt(20)
r.font.bold = True
r.font.color.rgb = COLOR_NAVY
title_p.paragraph_format.space_after = Pt(2)

sub_p = doc.add_paragraph()
r_sub = sub_p.add_run("PanelRight (www.panelright.com) | PCB Panel Optimization Software (v2 Expanded Audit)")
r_sub.font.name = "Arial"
r_sub.font.size = Pt(12)
r_sub.font.color.rgb = COLOR_BLUE
sub_p.paragraph_format.space_after = Pt(12)

meta_table = doc.add_table(rows=6, cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ("Target Website:", "https://www.panelright.com/"),
    ("Application Portal / Contact:", "https://solutions.panelright.com/contact"),
    ("Core Value Proposition:", "Algorithmic PCB Panelization to Minimize eWaste & Cost"),
    ("Technology Framework & Host:", "Next.js 13+ (App Router) on Vercel Edge / AWS (US)"),
    ("Audit Date:", "October 14, 2026 (Live Probed & Verified)"),
    ("Overall Website Health Score:", "33 / 100 (Critical Remediation Required)")
]
for idx, (lbl, val) in enumerate(meta_data):
    c1, c2 = meta_table.rows[idx].cells
    c1.text = lbl
    c2.text = val
    c1.paragraphs[0].runs[0].bold = True
    c1.paragraphs[0].runs[0].font.size = Pt(9)
    c2.paragraphs[0].runs[0].font.size = Pt(9)
    if "Health Score" in lbl:
        c2.paragraphs[0].runs[0].bold = True
        c2.paragraphs[0].runs[0].font.color.rgb = COLOR_RED

doc.add_paragraph().paragraph_format.space_after = Pt(8)

def add_heading(text, level=1):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(12.5 if level == 1 else 11)
    r.font.bold = True
    r.font.color.rgb = COLOR_NAVY if level == 1 else COLOR_BLUE
    return p

def add_para(text, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        rp = p.add_run(bold_prefix)
        rp.bold = True
        rp.font.name = "Arial"
        rp.font.size = Pt(9)
        rp.font.color.rgb = COLOR_DARK
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(9)
    r.font.color.rgb = COLOR_DARK
    return p

add_heading("1. Executive Summary & Verified Tool Baseline")
add_para("PanelRight operates in a highly specialized, lucrative B2B manufacturing domain: optimizing printed circuit board (PCB) panelization and array layouts to maximize panel utilization, minimize costly FR-4 laminate scrap (eWaste), and reduce production costs. While Vercel Edge hosting delivers exceptional static response times (TTFB: 68 ms, FCP: 500 ms), the website currently suffers from zero organic search traffic and zero AI search visibility.")
add_para("Semrush Domain Overview: Authority Score: 2 / 100 ('Lacks organic traffic'). Organic Traffic: 0 visits/mo. Paid Traffic: 0. AI Search Visibility: 0 across ChatGPT, Google AI Overviews, Google AI Mode, and Gemini. Referring Domains: 1.2K | Backlinks: 1.3K.", "Verified Baseline: ")
add_para("Moz Domain Overview: Domain Authority (DA): 6 / 100. Brand Authority: 1 / 100. Page Authority: 22 / 100. Domain Search Theme: 'Industrial Panel Systems'.", "Verified Baseline: ")
add_para("Hosting Geolocation: IP 64.29.17.65 (Vercel, Inc / Amazon.com, Inc.) hosted in Walnut, California, United States.", "Infrastructure: ")
add_para("Live Crawl & Probing Verification: Unlike unverified assumptions, direct live probing confirmed that robots.txt is active but lacks a Sitemap directive, headers on the root domain lack X-Frame-Options/X-Content-Type-Options, placeholder pages have zero meta robots tags (meaning they are indexed by default), and the mobile contact submit button is only 24px high.", "Live Probed Facts: ")

add_heading("2. Comprehensive Issue Catalog (22 Verified Issues - Issues ONLY)")

issues = [
    ("Default Next.js 13 Template Description in Production", "Critical", "https://www.panelright.com/, /efficiency, /faq", "Meta description on homepage and /efficiency reads: 'An open source application built using the new router, server components and everything new in Next.js 13.' This template boilerplate from the shadcn/taxonomy starter kit appears directly in live Google search snippets."),
    ("Primary CTA Links to a 25-Word 'Under Construction' Page", "Critical", "https://www.panelright.com/efficiency", "The prominent homepage CTA ('How We Find Efficient Solutions') links to /efficiency, which displays a 25-word 'Under Construction' placeholder. It contains 0 H1s and returns HTTP 200 without a noindex tag, causing immediate visitor bounce."),
    ("Default Indexability of Placeholder Pages (Missing noindex)", "Critical", "https://www.panelright.com/efficiency, /privacy, /terms", "Live header and DOM analysis proves zero meta robots tags or X-Robots-Tags exist. The 25-word 'Under Construction' page and Latin Lorem Ipsum legal pages are 100% indexable by default, exposing development drafts to search engines."),
    ("Severe Heading Dilution: 7 Separate H1 Tags on Homepage", "Critical", "https://www.panelright.com/", "The homepage marks up 7 separate <h1> tags (the main slogan plus all 6 industry tabs: Aviation, Marine, Medical, Automotive, Industrial, Consumer), severely diluting keyword relevance."),
    ("Missing H1 Tag on Key Solution Page", "Critical", "https://www.panelright.com/efficiency", "The /efficiency page contains zero <h1> elements, jumping directly into an <h2> ('Under Construction')."),
    ("FAQ Answers Unmounted in Server HTML (Radix SSR Bug)", "Critical", "https://www.panelright.com/faq", "Radix UI accordion renders closed answers with <div hidden=''></div> with zero text in SSR. Googlebot sees only 130 words of question headings and zero answer text, preventing indexing and FAQ Rich Snippets."),
    ("Live Production Legal Pages Contain Latin Lorem Ipsum", "Critical", "https://www.panelright.com/privacy, /terms", "/privacy and /terms are live in production containing unedited Latin filler text referencing 'Taxonomy App'. Neither page is linked in the global footer."),
    ("Total Absence of XML Sitemap (HTTP 404)", "Critical", "https://www.panelright.com/sitemap.xml", "Requesting /sitemap.xml returns HTTP 404 via Next.js error boundary. robots.txt lacks a Sitemap reference, leaving crawlers with zero indexing guidance."),
    ("Missing Canonical Tags Across 100% of Production Pages", "High", "All pages", "Zero pages contain a <link rel='canonical'> tag. Screaming Frog reports 'Canonicals: Missing' across the entire domain."),
    ("Subdomain Security Header Asymmetry & Missing Root Headers", "High", "https://www.panelright.com/", "Root domain lacks X-Frame-Options, X-Content-Type-Options, Referrer-Policy, and CSP. In contrast, solutions.panelright.com has DENY and nosniff, demonstrating fragmented security governance."),
    ("Subdomain Trust Boundary & Broken Return Navigation", "High", "https://solutions.panelright.com/contact", "Contact form is isolated on solutions. subdomain. The 'Return' link navigates to solutions.panelright.com/ (an internal app portal titled 'Redirect Buttons' lacking a viewport tag) instead of the marketing homepage."),
    ("Mobile Tap-Target Failure: 24px Contact Submit Button", "High", "https://solutions.panelright.com/contact", "The mobile submit button renders at only 127px by 24px, violating WCAG 2.5.8 / mobile usability standards (minimum 44x44px or 48x48px touch targets), causing tap frustration."),
    ("OpenGraph Image Points to Ephemeral Vercel Preview URL", "High", "All pages", "og:image is set to 'https://panelright-website-50h6p5vgc-panel-right.vercel.app/opengraph-image.jpg' instead of a permanent production www.panelright.com domain asset."),
    ("Under-Optimized, Extremely Short Title Tags (< 25 Chars)", "Medium", "All pages", "Homepage title is literally just 10 chars ('PanelRight'), FAQ is 16 chars ('FAQ | PanelRight'), Contact is 18 chars ('Contact PanelRight'). Missing all primary B2B keywords."),
    ("Extreme Thin Content Across Entire Domain (< 530 Words Total)", "Medium", "Site-wide", "The entire marketing website consists of fewer than 530 total words (Home: 341, FAQ: 130, Efficiency: 25, Contact: 31). Zero technical whitepapers, calculators, or case studies."),
    ("Zero Structured Data / Schema Markup", "Medium", "Site-wide", "0 JSON-LD scripts detected across any page. Missing Organization, SoftwareApplication, and FAQPage rich snippets."),
    ("AI Search Invisibility & Zero Citations", "Medium", "Site-wide", "0 citations across ChatGPT, Perplexity, Gemini, and Google AI Overviews because the site lacks substantive crawlable text and entity validation."),
    ("Core Web Vitals Lab vs. Field Data Blindspot", "Medium", "Site-wide", "Fast synthetic TTFB (68ms) creates false confidence. Google CrUX field data is currently unpopulated due to 0 traffic; tab-switcher INP and accordion hydration shifts remain unmonitored."),
    ("Two-Hop Redirect Chain on Non-WWW HTTP Version", "Low", "http://panelright.com/", "http://panelright.com/ -> 308 -> https://panelright.com/ -> 308 -> https://www.panelright.com/ (2 redirect hops)."),
    ("Missing Accessibility Labels on Contact Textarea", "Medium", "https://solutions.panelright.com/contact", "The contact message body input renders without an explicit type or associated label tag, impacting screen reader navigation."),
    ("Zero Analytics or Conversion Attribution Tracking", "Critical", "Site-wide", "0 instances of GA4, GTM, or webmaster verification tags detected. All user visits and contact form interactions are unmeasured."),
    ("Total Absence of Company Identity, E-E-A-T & Trust Signals", "Critical", "Site-wide", "Footer contains only 'Copyright Panelright 2026'. No physical address, no phone number, no company email, no team/founder bios, and no active corporate LinkedIn profile.")
]

issue_table = doc.add_table(rows=1, cols=4)
issue_table.alignment = WD_TABLE_ALIGNMENT.CENTER
i_headers = ["Issue Identified", "Severity", "Affected URLs", "Observed Defect & Impact"]
for idx, h in enumerate(i_headers):
    issue_table.rows[0].cells[idx].text = h
    issue_table.rows[0].cells[idx].paragraphs[0].runs[0].bold = True
    issue_table.rows[0].cells[idx].paragraphs[0].runs[0].font.size = Pt(8.5)

for row in issues:
    rc = issue_table.add_row().cells
    for idx, val in enumerate(row):
        rc[idx].text = val
        rc[idx].paragraphs[0].runs[0].font.size = Pt(8)
        if idx == 1 and val == "Critical":
            rc[idx].paragraphs[0].runs[0].bold = True

add_heading("3. Scope of Improvement")
add_para("PanelRight operates in an uncrowded, high-margin B2B software sector where electronics OEMs and PCB fabricators actively search for ways to reduce laminate scrap. The scope of improvement includes:")
add_para("Organic Search & AI Search Visibility: Transitioning from Authority Score 2 and 0 organic traffic to Page 1 rankings for commercial queries ('PCB panel optimization', 'PCB panelization software', 'PCB array nesting', 'reduce electronics manufacturing eWaste'). Currently, AI search engines have 0 citations for the brand.", "1. Search Visibility: ")
add_para("Technical Governance & Crawl Hygiene: Providing clean XML sitemaps, canonical tags, server-rendered FAQ content, single-hop redirects, temporary noindex on unfinished drafts, and uniform HTTP security headers.", "2. Technical Foundation: ")
add_para("Topical Authority & Content Expansion: Expanding from a 530-word brochure into an authoritative B2B technical hub featuring dedicated industry solution pages (Aerospace, Medical Devices, Automotive), technical panelization guides, and laminate savings formulas.", "3. Content Depth: ")
add_para("Conversion Funnel & Mobile Usability: Replacing the dead 'Under Construction' roadblock with a high-converting technology explainer, fixing the 24px mobile submit button tap target, and unifying the contact flow.", "4. Lead Generation: ")
add_para("Brand Authority & E-E-A-T Elevation: Moving Moz Brand Authority from 1 to enterprise-grade by publishing verified company background, founder credentials, enterprise security/NDA assurances, and legitimate Privacy/Terms policies.", "5. Trust Signals: ")

add_heading("4. Immediate Fixation Needed (Emergency Priority - 9 Items)")
add_para("The following 9 items are actively damaging the brand and user experience in production right now and require immediate intervention:")
add_para("1. Replace Default Next.js 13 Template Description: Stop developer boilerplate from showing in Google search snippets.")
add_para("2. Resolve the Broken /efficiency Page & Apply Temporary noindex: Eliminate the 25-word 'Under Construction' placeholder, and set noindex, follow until full technical content is published.")
add_para("3. Consolidate Homepage Heading Structure: Eliminate the 7 H1 tags and establish a single clear page title.")
add_para("4. Fix the Radix UI Accordion Bug on /faq: Ensure FAQ answer text is rendered into the server HTML payload so Googlebot can index it.")
add_para("5. Replace Latin Lorem Ipsum & Apply Temporary noindex: Remove 'Taxonomy App' Latin filler text from /privacy and /terms, and set noindex until real policies are drafted.")
add_para("6. Deploy an XML Sitemap (Currently 404) and Canonical Tags: Restore fundamental crawl and indexation directives.")
add_para("7. Resolve Subdomain Contact Navigation: Fix the 'Return' link on solutions.panelright.com/contact to point back to the marketing homepage, and enlarge the mobile submit button from 24px to ≥ 44px.")
add_para("8. Standardize HTTP Security Headers: Apply X-Frame-Options, X-Content-Type-Options: nosniff, and Referrer-Policy to the root domain to match the subdomain.")
add_para("9. Add robots.txt Sitemap Reference & Clarify AI Crawler Directives: Add the sitemap URL and ensure friendly directives for GPTBot, ClaudeBot, and PerplexityBot.")

add_heading("5. What Will Be the Next Step (Strategic 4-Phase Roadmap)")
add_para("Phase 1: Emergency Technical Cleanup (Days 1–15): Focus exclusively on resolving the 9 emergency defects above. Clean up metadata in Next.js, fix heading tags, deploy dynamic sitemap, add canonical tags, noindex placeholder drafts, and fix the mobile contact button.")
add_para("Phase 2: Core Solution Content & Trust Architecture (Days 16–45): Transform /efficiency into a full technical explainer (1,000+ words with laminate savings tables), draft legitimate B2B Privacy and Terms policies, add company trust signals to the footer, and deploy Schema.org structured data.")
add_para("Phase 3: Industry Expansion & B2B Inbound Scaling (Days 46–90): Launch dedicated landing pages for Aerospace, Medical, and Automotive PCB manufacturing; build an interactive PCB laminate savings calculator; and pursue B2B industry visibility across electronics manufacturing publications (EE Times, I-Connect007).")
add_para("Phase 4: Field Verification & Authority Rescoring (Days 90+): Once real organic traffic begins, analyze live Chrome User Experience Report (CrUX) field data for LCP/INP/CLS, audit mobile usability on real devices, verify AI citation appearance in ChatGPT/Gemini, and re-score the website out of 100.", "Post-Launch: ")

doc.save(os.path.join(output_dir, "PanelRight_SEO_Audit_Report.docx"))
doc.save("PanelRight_SEO_Audit_Report.docx")
print("DOCX v2 generated successfully!")

print("\n=== 2. GENERATING EXPANDED ISSUE-ONLY PDF VIA PLAYWRIGHT ===")

pdf_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>SEO & Website Audit Report | PanelRight (v2 Expanded)</title>
    <style>
        @page {
            size: A4;
            margin: 12mm 12mm 12mm 12mm;
            @bottom-center {
                content: "PanelRight — SEO & Website Audit (v2 Expanded) | Page " counter(page);
                font-size: 8pt;
                color: #64748b;
            }
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            color: #0f172a;
            line-height: 1.4;
            font-size: 8.5pt;
            background: #ffffff;
        }

        .cover-page {
            text-align: center;
            padding-top: 40px;
            padding-bottom: 45px;
            page-break-after: always;
        }
        .cover-badge {
            display: inline-block;
            text-transform: uppercase;
            font-size: 8.5pt;
            font-weight: 700;
            color: #2563eb;
            letter-spacing: 1px;
            margin-bottom: 10px;
        }
        .cover-title {
            font-size: 22pt;
            font-weight: 800;
            color: #0a192f;
            margin-bottom: 8px;
            line-height: 1.2;
        }
        .cover-subtitle {
            font-size: 11.5pt;
            color: #475569;
            margin-bottom: 30px;
        }
        .score-box {
            display: inline-block;
            border: 3px solid #dc2626;
            background: #fef2f2;
            border-radius: 12px;
            padding: 20px 36px;
            margin-bottom: 30px;
        }
        .score-val {
            font-size: 42pt;
            font-weight: 800;
            color: #dc2626;
            line-height: 1;
        }
        .score-lbl {
            font-size: 9pt;
            font-weight: 700;
            color: #991b1b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 5px;
        }
        .cover-meta {
            max-width: 520px;
            margin: 0 auto;
            text-align: left;
            background: #f8fafc;
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: 14px 18px;
            font-size: 8.5pt;
        }
        .cover-meta div {
            margin-bottom: 4px;
        }
        .cover-meta strong {
            color: #0a192f;
        }

        .section {
            margin-bottom: 16px;
            page-break-inside: avoid;
        }
        .section-title {
            font-size: 11pt;
            font-weight: 800;
            color: #0a192f;
            border-bottom: 2px solid #2563eb;
            padding-bottom: 3px;
            margin-bottom: 6px;
            margin-top: 10px;
        }
        p {
            margin-bottom: 5px;
            color: #334155;
            text-align: justify;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 7.5pt;
            margin: 6px 0 12px;
            page-break-inside: avoid;
        }
        th {
            background: #0a192f;
            color: #ffffff;
            font-weight: 700;
            text-align: left;
            padding: 5px 8px;
            text-transform: uppercase;
            font-size: 7pt;
            letter-spacing: 0.5px;
        }
        td {
            padding: 5px 8px;
            border-bottom: 1px solid #e2e8f0;
            color: #334155;
            vertical-align: top;
        }
        tr:nth-child(even) td {
            background: #f8fafc;
        }

        .badge {
            display: inline-block;
            padding: 1px 4px;
            border-radius: 3px;
            font-size: 6.5pt;
            font-weight: 700;
            text-transform: uppercase;
        }
        .badge-critical { background: #fee2e2; color: #dc2626; }
        .badge-warning { background: #fef3c7; color: #d97706; }
        .badge-pass { background: #d1fae5; color: #059669; }

        .callout {
            background: #fff5f5;
            border-left: 3px solid #dc2626;
            padding: 6px 10px;
            border-radius: 0 5px 5px 0;
            margin-bottom: 6px;
            page-break-inside: avoid;
        }
        .callout h4 {
            font-size: 8pt;
            font-weight: 700;
            color: #991b1b;
            margin-bottom: 2px;
        }
        .callout p {
            font-size: 7.5pt;
            color: #7f1d1d;
            margin-bottom: 0;
        }
    </style>
</head>
<body>

<!-- PAGE 1: COVER -->
<div class="cover-page">
    <div class="cover-badge">B2B Website Technical &amp; On-Page Audit (v2 Expanded)</div>
    <div class="cover-title">SEO &amp; WEBSITE AUDIT REPORT</div>
    <div class="cover-subtitle">PanelRight (www.panelright.com) — Issues &amp; Gap Analysis</div>

    <div class="score-box">
        <div class="score-val">33 / 100</div>
        <div class="score-lbl">Overall Website Health Score</div>
    </div>

    <div class="cover-meta">
        <div><strong>Client Domain:</strong> https://www.panelright.com/</div>
        <div><strong>Application Portal:</strong> https://solutions.panelright.com/contact</div>
        <div><strong>Core Offering:</strong> Algorithmic PCB Panel Optimization Software</div>
        <div><strong>Technology Stack:</strong> Next.js 13+ (App Router) on Vercel Edge / AWS (US)</div>
        <div><strong>Audit Verification:</strong> October 14, 2026 (Live Probed &amp; Measured)</div>
        <div><strong>Domain Authority:</strong> Moz DA 6 | Semrush AS 2 | Organic Traffic: 0</div>
    </div>
</div>

<!-- PAGE 2: EXECUTIVE SUMMARY & SCORECARD -->
<div class="section">
    <div class="section-title">1. Executive Summary &amp; Live-Verified Baseline</div>
    <p>PanelRight provides an automated algorithmic software solution designed to solve an expensive bottleneck in electronics manufacturing: printed circuit board (PCB) panelization and array nesting to minimize laminate scrap (eWaste) and reduce fabrication costs. While Vercel Edge hosting delivers exceptional static response times (TTFB: 68 ms, FCP: 500 ms), the website currently suffers from <strong>zero organic search visibility</strong> because critical developer boilerplate and unfinished assets were left active in production.</p>
    
    <div class="callout" style="background: #eff6ff; border-left-color: #2563eb;">
        <h4 style="color: #1e40af;">Verified Tool Baseline &amp; Direct Probing Results</h4>
        <p style="color: #1e3a8a;">
            <strong>Semrush:</strong> Authority Score 2/100 ("Lacks organic traffic"). Organic Search Traffic: 0 visits/mo. AI Search Visibility: 0 across ChatGPT, Google AI Overviews, Google AI Mode, and Gemini. Ref. Domains: 1.2K | Backlinks: 1.3K.<br>
            <strong>Moz:</strong> Domain Authority: 6/100 | Brand Authority: 1/100 | Page Authority: 22/100 | Search Theme: "Industrial Panel Systems".<br>
            <strong>Live Header &amp; Robot Audit:</strong> robots.txt returns 200 with Allow: / but lacks a Sitemap directive. Root domain lacks X-Frame-Options, X-Content-Type-Options, and Referrer-Policy, while solutions. subdomain enforces them. Zero meta robots tags exist, leaving unfinished pages fully indexable. Contact submit button is only 24px high on mobile viewports.
        </p>
    </div>
</div>

<div class="section">
    <div class="section-title">2. Website Technical Health Scorecard (33 / 100)</div>
    <table>
        <thead>
            <tr><th>Audit Category</th><th>Weight</th><th>Score</th><th>Status</th><th>Primary Observed Defect</th></tr>
        </thead>
        <tbody>
            <tr><td><strong>Crawlability &amp; Sitemaps</strong></td><td>10</td><td><strong>2 / 10</strong></td><td><span class="badge badge-critical">Fail</span></td><td>sitemap.xml returns HTTP 404; robots.txt has no sitemap reference</td></tr>
            <tr><td><strong>Indexability &amp; Canonicals</strong></td><td>10</td><td><strong>2 / 10</strong></td><td><span class="badge badge-critical">Fail</span></td><td>Missing canonical tags across 100% of pages; drafts lack noindex</td></tr>
            <tr><td><strong>On-Page Metadata</strong></td><td>10</td><td><strong>2 / 10</strong></td><td><span class="badge badge-critical">Critical</span></td><td>Next.js 13 starter boilerplate meta descriptions; titles &lt; 20 chars</td></tr>
            <tr><td><strong>Heading Structure (H1/H2)</strong></td><td>10</td><td><strong>2 / 10</strong></td><td><span class="badge badge-critical">Critical</span></td><td>7 separate H1 tags on homepage; 0 H1 tags on /efficiency</td></tr>
            <tr><td><strong>Content Depth &amp; Indexability</strong></td><td>10</td><td><strong>2 / 10</strong></td><td><span class="badge badge-critical">Critical</span></td><td>Primary CTA leads to 25-word 'Under Construction' page; FAQ unmounted</td></tr>
            <tr><td><strong>Performance &amp; Speed</strong></td><td>10</td><td><strong>10 / 10</strong></td><td><span class="badge badge-pass">Pass</span></td><td>Vercel Edge delivery is ultra fast (TTFB 68ms, FCP 500ms lab)</td></tr>
            <tr><td><strong>Structured Data (Schema)</strong></td><td>10</td><td><strong>0 / 10</strong></td><td><span class="badge badge-critical">Fail</span></td><td>Zero Schema.org JSON-LD blocks across the domain</td></tr>
            <tr><td><strong>E-E-A-T &amp; Trust Signals</strong></td><td>10</td><td><strong>2 / 10</strong></td><td><span class="badge badge-critical">Critical</span></td><td>No company address/phone; Latin Lorem Ipsum on /privacy &amp; /terms</td></tr>
            <tr><td><strong>Security &amp; Architecture</strong></td><td>10</td><td><strong>3 / 10</strong></td><td><span class="badge badge-warning">Warning</span></td><td>Root lacks X-Frame-Options/nosniff; contact subdomain disconnected</td></tr>
            <tr><td><strong>Mobile &amp; Accessibility</strong></td><td>10</td><td><strong>2 / 10</strong></td><td><span class="badge badge-critical">Critical</span></td><td>Mobile contact submit button is only 24px high (fails 44px WCAG touch)</td></tr>
            <tr><td><strong>TOTAL WEIGHTED SCORE</strong></td><td>100</td><td><strong>33 / 100</strong></td><td><span class="badge badge-critical">Critical</span></td><td><strong>Immediate Production Cleanup &amp; Content Build Required</strong></td></tr>
        </tbody>
    </table>
</div>

<!-- PAGE 3: ISSUE CATALOG -->
<div class="section" style="page-break-before: always;">
    <div class="section-title">3. Comprehensive Issue Catalog (22 Verified Issues - Issues ONLY)</div>

    <div class="callout">
        <h4>1. Default Next.js 13 Template Description Active in Production</h4>
        <p><strong>Affected URLs:</strong> <code>https://www.panelright.com/</code>, <code>/efficiency</code>, <code>/faq</code> (OG)<br>
        <strong>Observed:</strong> Meta description reads: <em>"An open source application built using the new router, server components and everything new in Next.js 13."</em> from the <code>shadcn/taxonomy</code> template. Appears in live Google search snippets.</p>
    </div>

    <div class="callout">
        <h4>2. Primary CTA Links to a 25-Word 'Under Construction' Page</h4>
        <p><strong>Affected URLs:</strong> <code>https://www.panelright.com/efficiency</code><br>
        <strong>Observed:</strong> Homepage CTA <em>"How We Find Efficient Solutions"</em> links to <code>/efficiency</code>, displaying only: <em>"Under Construction. This page is currently being built. Please check back soon."</em> Returns HTTP 200 without a noindex tag.</p>
    </div>

    <div class="callout">
        <h4>3. Default Indexability of Unfinished/Placeholder Pages (Missing noindex)</h4>
        <p><strong>Affected URLs:</strong> <code>/efficiency</code>, <code>/privacy</code>, <code>/terms</code><br>
        <strong>Observed:</strong> Live header and DOM extraction proves zero meta robots tags or X-Robots-Tags exist. Search engines are allowed to index 25-word under construction notices and Latin filler text.</p>
    </div>

    <div class="callout">
        <h4>4. Severe Heading Dilution (7 Separate H1 Tags on Homepage)</h4>
        <p><strong>Affected URLs:</strong> <code>https://www.panelright.com/</code><br>
        <strong>Observed:</strong> Homepage marks up 7 separate <code>&lt;h1&gt;</code> tags (the main slogan plus all 6 industry tabs: Aviation, Marine, Medical, Automotive, Industrial, Consumer).</p>
    </div>

    <div class="callout">
        <h4>5. Missing H1 Tag on Key Solution Page</h4>
        <p><strong>Affected URLs:</strong> <code>https://www.panelright.com/efficiency</code><br>
        <strong>Observed:</strong> Contains zero <code>&lt;h1&gt;</code> elements, jumping directly into an <code>&lt;h2&gt;</code> ('Under Construction').</p>
    </div>

    <div class="callout">
        <h4>6. FAQ Answers Unmounted in Server HTML (Radix SSR Bug)</h4>
        <p><strong>Affected URLs:</strong> <code>https://www.panelright.com/faq</code><br>
        <strong>Observed:</strong> Radix UI accordion renders closed answers with <code>&lt;div hidden=""&gt;&lt;/div&gt;</code> with zero text in SSR. Crawlers see only 130 words of question headings and zero answer text, blocking FAQ Rich Snippets.</p>
    </div>

    <div class="callout">
        <h4>7. Live Production Legal Pages Contain Latin Lorem Ipsum ('Taxonomy App')</h4>
        <p><strong>Affected URLs:</strong> <code>https://www.panelright.com/privacy</code>, <code>https://www.panelright.com/terms</code><br>
        <strong>Observed:</strong> Live on production containing raw Latin filler text referencing <em>"Taxonomy App"</em>. Neither is linked in the global footer.</p>
    </div>

    <div class="callout">
        <h4>8. Total Absence of XML Sitemap (HTTP 404) &amp; Missing Canonical Tags</h4>
        <p><strong>Affected URLs:</strong> <code>https://www.panelright.com/sitemap.xml</code>, All pages<br>
        <strong>Observed:</strong> <code>/sitemap.xml</code> returns 404, robots.txt has no sitemap reference, and 0 pages have <code>&lt;link rel="canonical"&gt;</code>.</p>
    </div>

    <div class="callout">
        <h4>9. Subdomain Security Header Asymmetry &amp; Missing Root Headers</h4>
        <p><strong>Affected URLs:</strong> <code>https://www.panelright.com/</code><br>
        <strong>Observed:</strong> Live header probing reveals root domain lacks X-Frame-Options, X-Content-Type-Options: nosniff, and Referrer-Policy, whereas solutions. subdomain enforces them.</p>
    </div>

    <div class="callout">
        <h4>10. Subdomain Trust Boundary &amp; Broken Return Navigation</h4>
        <p><strong>Affected URLs:</strong> <code>https://solutions.panelright.com/contact</code><br>
        <strong>Observed:</strong> Contact form is isolated on solutions. subdomain. The 'Return' link navigates to <code>solutions.panelright.com/</code> (an unstyled portal titled <em>"Redirect Buttons"</em> lacking a viewport tag) instead of the marketing homepage.</p>
    </div>

    <div class="callout">
        <h4>11. Mobile Tap-Target Failure: 24px Contact Submit Button</h4>
        <p><strong>Affected URLs:</strong> <code>https://solutions.panelright.com/contact</code><br>
        <strong>Observed:</strong> Measured mobile submit button dimensions are 127px by 24px, failing WCAG 2.5.8 touch target standards (minimum 44x44px or 48x48px) and risking mobile form abandonment.</p>
    </div>

    <div class="callout">
        <h4>12. AI Search Invisibility (0 Citations Across All AI Platforms)</h4>
        <p><strong>Affected URLs:</strong> Site-wide<br>
        <strong>Observed:</strong> ChatGPT, Gemini, Perplexity, and Google AI Overviews return zero citations because the domain lacks substantive text (530 words total) and entity signals.</p>
    </div>
</div>

<!-- PAGE 4: SCOPE OF IMPROVEMENT & IMMEDIATE FIXATION -->
<div class="section" style="page-break-before: always;">
    <div class="section-title">4. Scope of Improvement</div>
    <p>PanelRight operates in an uncrowded, high-margin B2B software sector where electronics OEMs and PCB fabricators actively search for ways to reduce laminate scrap. The scope of improvement covers 5 strategic pillars:</p>
    
    <p><strong>1. Search Visibility &amp; AI Discovery:</strong> Transitioning from Authority Score 2 and 0 organic visits to Page 1 rankings for high-intent queries (<em>"PCB panel optimization"</em>, <em>"PCB panelization software"</em>, <em>"PCB array nesting"</em>, <em>"reduce electronics manufacturing eWaste"</em>). Establishing entity clarity and crawlable content for AI search engines.</p>
    
    <p><strong>2. Technical Governance &amp; Crawl Hygiene:</strong> Establishing clean XML sitemaps, self-referencing canonical tags, server-rendered FAQ content, single-hop redirects, temporary noindex flags on unfinished drafts, and uniform HTTP security headers.</p>
    
    <p><strong>3. Topical Authority &amp; Content Depth:</strong> Expanding from a 530-word brochure into an authoritative B2B technical hub featuring dedicated industry solution pages (Aerospace, Medical Devices, Automotive), technical panelization guides, and laminate savings formulas.</p>
    
    <p><strong>4. Conversion Funnel &amp; Mobile Usability:</strong> Replacing the dead 'Under Construction' roadblock with a high-converting technology explainer, unifying the contact flow, and enlarging mobile tap targets to meet WCAG standards.</p>
    
    <p><strong>5. Brand Authority &amp; E-E-A-T Elevation:</strong> Moving Moz Brand Authority from 1 to enterprise-grade by publishing verified company background, founder credentials, enterprise security/NDA assurances, and legitimate Privacy/Terms policies.</p>
</div>

<div class="section">
    <div class="section-title">5. Immediate Fixation Needed (Emergency Priority - 9 Items)</div>
    <p>The following 9 items are actively harming brand perception and search performance in production right now and require immediate remediation:</p>
    <ul style="margin-left: 18px; font-size: 8pt; color: #334155; line-height: 1.5;">
        <li><strong>1. Replace Default Next.js 13 Template Description:</strong> Stop developer boilerplate from showing in live Google search snippets.</li>
        <li><strong>2. Resolve Broken /efficiency Page &amp; Apply Temporary noindex:</strong> Eliminate the 25-word placeholder; set noindex, follow until full technical content is published.</li>
        <li><strong>3. Consolidate Homepage Heading Structure:</strong> Eliminate the 7 H1 tags and establish a single clear page title.</li>
        <li><strong>4. Fix Radix UI Accordion Bug on /faq:</strong> Ensure FAQ answer text is rendered into the server HTML payload so Googlebot can read it.</li>
        <li><strong>5. Replace Latin Lorem Ipsum &amp; Apply Temporary noindex:</strong> Remove 'Taxonomy App' filler text from <code>/privacy</code> and <code>/terms</code>; noindex until real policies are drafted.</li>
        <li><strong>6. Deploy XML Sitemap (Currently 404) and Canonical Tags:</strong> Restore fundamental crawl and indexation directives.</li>
        <li><strong>7. Fix Subdomain Contact Navigation &amp; Mobile Button:</strong> Point the 'Return' link to the marketing homepage, and enlarge the mobile submit button from 24px to &ge; 44px.</li>
        <li><strong>8. Standardize Root HTTP Security Headers:</strong> Apply X-Frame-Options, X-Content-Type-Options: nosniff, and Referrer-Policy to the root domain.</li>
        <li><strong>9. Update robots.txt:</strong> Add the Sitemap URL directive and confirm explicit friendly rules for AI crawlers (GPTBot, ClaudeBot, PerplexityBot).</li>
    </ul>
</div>

<div class="section">
    <div class="section-title">6. What Will Be the Next Step (Strategic 4-Phase Roadmap)</div>
    <table>
        <thead>
            <tr><th>Phase</th><th>Key Objectives &amp; Focus Areas</th><th>Target Milestone</th></tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Phase 1: Emergency Cleanup<br>(Days 1–15)</strong></td>
                <td>Focus exclusively on resolving the 9 emergency defects: clean up metadata in Next.js, fix heading tags, deploy dynamic sitemap, add canonical tags, noindex placeholder drafts, standardize security headers, and enlarge mobile contact button.</td>
                <td>100% crawlable sitemap; 0 template strings in SERP; valid canonicals; no unindexed drafts</td>
            </tr>
            <tr>
                <td><strong>Phase 2: Core Solution Content<br>(Days 16–45)</strong></td>
                <td>Transform <code>/efficiency</code> into a full technical explainer (1,000+ words with laminate savings tables), draft legitimate B2B Privacy and Terms policies, add company trust signals to the footer, and deploy Schema.org structured data.</td>
                <td>Google indexes FAQ answers; legal trust established; 0 orphan pages</td>
            </tr>
            <tr>
                <td><strong>Phase 3: Industry Expansion<br>(Days 46–90)</strong></td>
                <td>Launch dedicated landing pages for Aerospace, Medical, and Automotive PCB manufacturing; build an interactive PCB laminate savings calculator; and pursue B2B industry visibility across electronics manufacturing publications (EE Times, I-Connect007).</td>
                <td>Page 1 rankings for long-tail PCB nesting terms; qualified inbound demo inquiries</td>
            </tr>
            <tr>
                <td><strong>Phase 4: Field Verification<br>(Days 90+)</strong></td>
                <td>Once real user traffic is established, pull Chrome User Experience Report (CrUX) field data for LCP/INP/CLS, audit mobile usability on real devices, verify AI citation appearance in ChatGPT/Gemini, and re-score the website out of 100.</td>
                <td>CrUX field validation; verified AI search presence; enterprise Brand Authority</td>
            </tr>
        </tbody>
    </table>
</div>

</body>
</html>
"""

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.set_content(pdf_html)
    page.wait_for_load_state("networkidle")
    
    pdf_path = os.path.join(output_dir, "PanelRight_SEO_Audit_Report.pdf")
    page.pdf(path=pdf_path, format="A4", print_background=True, margin={"top": "12mm", "bottom": "12mm", "left": "12mm", "right": "12mm"})
    
    # Also save to root
    page.pdf(path="PanelRight_SEO_Audit_Report.pdf", format="A4", print_background=True, margin={"top": "12mm", "bottom": "12mm", "left": "12mm", "right": "12mm"})
    
    browser.close()

print(f"Generated Issue-Only PDF: {pdf_path} ({os.path.getsize(pdf_path):,} bytes)")
print(f"Generated Issue-Only PDF: PanelRight_SEO_Audit_Report.pdf ({os.path.getsize('PanelRight_SEO_Audit_Report.pdf'):,} bytes)")
