import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

output_dir = r"website audit\panelright.com"

print("=== GENERATING SEO_AUDIT_REPORT.MD FOR PANELRIGHT ===")

report_md = """# Technical SEO & On-Page Website Audit Report
**Client Website:** https://www.panelright.com/  
**Application Portal / Contact:** https://solutions.panelright.com/contact  
**Core Offering:** PCB (Printed Circuit Board) Panel Optimization & Automated Panelization Software  
**Target Market:** Global B2B (Electronics OEMs, PCB Fabricators, Contract Manufacturers)  
**Technology Stack:** Next.js 13+ (App Router), React, Tailwind CSS, Radix UI on Vercel / AWS  
**Audit Date:** October 14, 2026  
**Overall Website Health Score:** **33 / 100 (Critical Remediation Required)**  

---

## 1. Executive Summary

### 1.1 Overview & Core Business Context
PanelRight (`www.panelright.com`) provides a high-value, specialized B2B algorithmic software solution designed to solve one of the most expensive bottlenecks in electronics manufacturing: **Printed Circuit Board (PCB) panelization and array optimization**. By mathematically optimizing the nesting, orientation, and spacing of circuit boards on master fabrication panels, PanelRight enables manufacturers to **minimize expensive FR-4 / laminate eWaste and cut per-board fabrication costs**.

Despite operating in a highly lucrative B2B niche with strong technical hosting fundamentals (**Next.js on Vercel delivering an ultra-fast TTFB of 68 ms**), the website currently suffers from **zero organic search visibility** (Semrush Organic Traffic: **0**, AI Search Visibility: **0**, Moz Brand Authority: **1**).

This organic invisibility is directly driven by **critical developer boilerplate and unfinished assets left active in production**:

```mermaid
pie title Technical Health Score Breakdown (Total 33/100)
    "Performance & Speed (18/20)" : 18
    "Crawlability & Indexing (3/20)" : 3
    "On-Page & Metadata (4/20)" : 4
    "Content & E-E-A-T (4/20)" : 4
    "Conversion, Tracking & Legal (4/20)" : 4
```

### 1.2 Baseline Search & Domain Authority Metrics (Verified Tools)
- **Semrush (Oct 13, 2026):**
  - **Authority Score:** 2 / 100 ("Lacks organic traffic")
  - **Organic Search Traffic:** 0 visits / month
  - **Paid Search Traffic:** 0
  - **Referring Domains:** 1.2K | **Backlinks:** 1.3K
  - **AI Search Visibility:** 0 across ChatGPT, Google AI Overviews, Google AI Mode, and Gemini (0 mentions, 0 cited pages)
- **Moz Domain Overview (Oct 2026):**
  - **Domain Search Theme:** Industrial Panel Systems
  - **Domain Authority (DA):** 6 / 100
  - **Brand Authority:** 1 / 100
  - **Page Authority (PA):** 22 / 100
- **Hosting Infrastructure & Geolocation:**
  - **IP Address:** `64.29.17.65` (Vercel, Inc / Amazon.com, Inc.)
  - **Server Location:** Walnut, California, United States

### 1.3 Overall Health Score Breakdown

| Audit Category | Max Weight | Score | Status | Primary Observed Defect |
|---|---|---|---|---|
| **Crawlability & Sitemaps** | 10 | **2 / 10** | **Fail** | `sitemap.xml` is 404; no sitemap pointer in `robots.txt` |
| **Indexability & Canonicalisation** | 10 | **2 / 10** | **Fail** | Missing `<link rel="canonical">` across 100% of pages |
| **On-Page Metadata** | 10 | **2 / 10** | **Critical** | Default Next.js 13 starter boilerplate meta descriptions in production |
| **Heading Structure (H1/H2)** | 10 | **2 / 10** | **Critical** | 7 separate H1 tags on homepage; 0 H1 tags on `/efficiency` |
| **Content Depth & Indexability** | 10 | **2 / 10** | **Critical** | Primary CTA links to 25-word "Under Construction" page; FAQ answers unmounted |
| **Performance & Core Web Vitals** | 10 | **10 / 10** | **Pass** | Exceptional static speed via Vercel Edge (TTFB 68ms, FCP 500ms) |
| **Mobile & Rendering Parity** | 10 | **8 / 10** | **Pass** | Clean responsive layout; but Radix accordion unmounts answers from server DOM |
| **Structured Data (Schema.org)** | 10 | **0 / 10** | **Fail** | Zero Schema.org JSON-LD blocks across the entire domain |
| **E-E-A-T & Trust Signals** | 10 | **2 / 10** | **Critical** | Zero team/founder info; unlinked `/privacy` & `/terms` contain Latin Lorem Ipsum |
| **Security & Architecture** | 10 | **3 / 10** | **Warning** | Missing X-Frame-Options/CSP on root; fragmented subdomain contact flow |
| **TOTAL WEIGHTED SCORE** | **100** | **33 / 100** | **Critical** | **Immediate Next.js Production Cleanup Required** |

---

## 2. Top Critical Findings (The "Smoking Guns")

### Finding 1: Default Next.js 13 Template Description Active in Production
- **Observed:** On the homepage (`/`) and the efficiency page (`/efficiency`), the HTML meta description reads:
  > *"An open source application built using the new router, server components and everything new in Next.js 13."*
- **Evidence:** This exact string is the default boilerplate description from the open-source `shadcn/taxonomy` Next.js 13 template repository.
- **Impact:** Search engine snippets in Google and social shares on LinkedIn/Slack display developer starter text instead of PanelRight's PCB optimization value proposition.

### Finding 2: Primary Homepage CTA Links to a 25-Word "Under Construction" Page
- **Observed:** On the homepage, the prominent link *"How We Find Efficient Solutions"* leads to `https://www.panelright.com/efficiency`.
- **Evidence:** The page contains only 25 total words:
  > *"Under Construction. This page is currently being built. Please check back soon."*
- **Impact:** The page has **0 H1 tags**, offers zero value to prospective customers, returns HTTP 200 without a `noindex` tag, and causes visitors to immediately bounce.

### Finding 3: Severe Heading Dilution (7 H1 Tags on Homepage)
- **Observed:** The homepage contains **7 separate `<h1>` tags**:
  1. `<h1>Minimize eWaste. Reduce Cost.</h1>`
  2. `<h1>Aviation & Defense</h1>`
  3. `<h1>Marine</h1>`
  4. `<h1>Medical Device</h1>`
  5. `<h1>Automotive</h1>`
  6. `<h1>Industrial & Energy</h1>`
  7. `<h1>Consumer & Appliance</h1>`
- **Impact:** In HTML5 semantics and SEO, having 7 H1s on a single 341-word page confuses search engine topic modeling by treating each industry tab as the primary page title.

### Finding 4: FAQ Answers Unmounted in Server HTML (Invisible to Googlebot)
- **Observed:** On `https://www.panelright.com/faq`, 14 high-value questions are displayed.
- **Evidence:** In server-rendered HTML, the Radix UI accordion renders closed items with `<div hidden=""></div>` containing zero text. Crawlers see only 130 words of question headings and **zero answer text**.
- **Impact:** Googlebot cannot index the answers, cannot award FAQ Rich Snippets, and flags the page as thin content.

### Finding 5: Live Production Legal Pages Contain Latin Lorem Ipsum
- **Observed:** The URLs `https://www.panelright.com/privacy` and `https://www.panelright.com/terms` are live on production and return HTTP 200.
- **Evidence:**
  - `/privacy` begins: *"The Privacy Policy for Taxonomy App. Blandit libero volutpat sed cras ornare arcu..."*
  - `/terms` begins: *"Read our terms and conditions. Lorem ipsumMagna fermentum iaculis..."*
  - Neither page is linked in the footer.
- **Impact:** Demonstrates unfinished development to enterprise B2B prospects and severely undermines Google E-E-A-T.

### Finding 6: Total Absence of XML Sitemap & Canonical Tags
- **Observed:** `https://www.panelright.com/sitemap.xml` returns **HTTP 404 Not Found**.
- **Observed:** 100% of pages lack `<link rel="canonical">` tags.

---

## 3. Comprehensive Technical Audit by Module

### 3.1 Crawlability & Indexability
- **Robots.txt:** Serves HTTP 200, allowing all user-agents, but fails to include a `Sitemap:` pointer.
- **Sitemap Hygiene:** Completely absent (404). In Next.js App Router, this is resolved by creating `app/sitemap.ts`.
- **Redirect Chains:** `http://panelright.com/` requires 2 hops (308 -> 308) to reach `https://www.panelright.com/`.

### 3.2 On-Page SEO & Metadata Optimization
- **Title Tags:** Currently 10–23 characters long (`PanelRight`, `FAQ | PanelRight`, `Efficiency | PanelRight`). They miss all primary search volume for *"PCB Panel Optimization"*, *"PCB Panelization Software"*, and *"PCB Array Nesting"*.
- **Meta Descriptions:** 2 pages share identical Next.js 13 template descriptions.
- **Heading Order:** The homepage jumps from H1 to H2 with 7 duplicate H1 tags; `/efficiency` has an H2 without any H1.

### 3.3 Content & Information Architecture
- The entire public marketing footprint consists of fewer than 530 total words.
- To rank for high-intent B2B electronics manufacturing queries, PanelRight must establish topical authority by building out dedicated industry pages and publishing technical guides on PCB panel utilization formulas.

### 3.4 Security & Server Configuration
- **Server:** Hosted on Vercel / AWS.
- **SSL/TLS:** TLS 1.3 active with valid certificates.
- **Security Headers:** Missing `X-Frame-Options`, `X-Content-Type-Options`, and `Content-Security-Policy` on the main domain. These should be defined in `next.config.js`.

---

## 4. Prioritised Action Items & 30-Day Quick Wins

```mermaid
quadrantChart
    title PanelRight Implementation Matrix (Impact vs Effort)
    x-axis Low Effort --> High Effort
    y-axis Low Impact --> High Impact
    quadrant-1 Strategic Projects
    quadrant-2 Immediate Quick Wins
    quadrant-3 Backlog Items
    quadrant-4 Low Value
    "Fix Next.js Template Description": [0.10, 0.95]
    "Fix Homepage 7 H1 Tags": [0.15, 0.90]
    "Deploy app/sitemap.ts": [0.20, 0.88]
    "Deploy Canonical Tags in layout.tsx": [0.15, 0.85]
    "Fix Radix FAQ SSR Unmounting": [0.35, 0.85]
    "Build out /efficiency Solution Page": [0.75, 0.95]
    "Replace Lorem Ipsum on Legal Pages": [0.40, 0.80]
    "Deploy Schema.org JSON-LD": [0.40, 0.75]
    "Consolidate Subdomain Contact Form": [0.50, 0.70]
```

### Top 10 Quick Wins (Deploy Within 7 Days)
1. **Replace Default Next.js 13 Description:** Update `app/layout.tsx` metadata with optimized PCB optimization copy (15 mins).
2. **Correct Homepage H1s:** Demote 6 industry H1s to `<h3>` or `<div>`, keeping only the primary title as `<h1>` (20 mins).
3. **Deploy `app/sitemap.ts`:** Automatically generate a valid XML sitemap containing all routes (30 mins).
4. **Deploy Canonical Tags in `app/layout.tsx`:** Add `metadataBase` and `alternates` configuration (15 mins).
5. **Fix Radix UI FAQ Accordion:** Ensure FAQ answers are rendered into the server HTML payload (45 mins).
6. **Apply Temporary Fix to `/efficiency`:** If the content is not ready, add a `noindex` tag or redirect to `/#workSection` (15 mins).
7. **Replace Latin Lorem Ipsum on `/privacy` and `/terms`:** Draft clean, legitimate commercial B2B policies (1 hour).
8. **Add Footer Links:** Link Privacy Policy, Terms, and Contact Us in the global website footer (20 mins).
9. **Update OpenGraph Image:** Replace the temporary Vercel preview URL with a permanent branded graphic (20 mins).
10. **Add Security Headers in `next.config.js`:** Add `X-Frame-Options` and `X-Content-Type-Options` (30 mins).
"""

with open(os.path.join(output_dir, "SEO_Audit_Report.md"), "w", encoding="utf-8") as f:
    f.write(report_md)

print("SEO_Audit_Report.md generated successfully!")

print("\n=== GENERATING CLIENT_SEO_AUDIT_REPORT.HTML ===")

html_report = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Technical SEO & On-Page Audit Report | PanelRight</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #0a192f;
            --primary-light: #172a45;
            --accent: #2563eb;
            --accent-glow: rgba(37, 99, 235, 0.15);
            --teal: #059669;
            --bg-main: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --critical: #dc2626;
            --critical-bg: #fef2f2;
            --warning: #d97706;
            --warning-bg: #fffbeb;
            --success: #059669;
            --success-bg: #ecfdf5;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Plus Jakarta Sans', sans-serif; background: var(--bg-main); color: var(--text-main); line-height: 1.6; }
        .container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }

        header {
            background: linear-gradient(135deg, var(--primary) 0%, #06101e 100%);
            color: white; padding: 50px 0; border-bottom: 4px solid var(--accent);
        }

        .badge-client {
            display: inline-flex; align-items: center; background: rgba(255, 255, 255, 0.1);
            padding: 6px 14px; border-radius: 999px; font-size: 13px; font-weight: 600;
            color: #93c5fd; text-transform: uppercase; margin-bottom: 16px;
        }

        .hero-title { font-family: 'Space Grotesk', sans-serif; font-size: 34px; font-weight: 700; margin-bottom: 10px; }
        .hero-subtitle { font-size: 16px; color: #cbd5e1; max-width: 800px; margin-bottom: 24px; }

        .meta-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px; background: rgba(255, 255, 255, 0.05); padding: 16px 20px; border-radius: 10px;
        }
        .meta-item .lbl { font-size: 11px; text-transform: uppercase; color: #94a3b8; font-weight: 600; }
        .meta-item .val { font-size: 14px; font-weight: 700; color: #f8fafc; }

        .sticky-nav {
            position: sticky; top: 0; background: white; border-bottom: 1px solid var(--border);
            z-index: 100; box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        }
        .nav-links { display: flex; gap: 20px; padding: 12px 0; overflow-x: auto; white-space: nowrap; }
        .nav-links a { text-decoration: none; color: var(--text-muted); font-weight: 600; font-size: 13px; padding: 6px 10px; border-radius: 6px; }
        .nav-links a:hover { color: var(--accent); background: var(--accent-glow); }

        main { padding: 40px 0 70px; }

        .score-hero-card {
            background: white; border-radius: 14px; border: 1px solid var(--border);
            padding: 30px; margin-bottom: 36px; display: grid; grid-template-columns: 240px 1fr;
            gap: 36px; align-items: center; box-shadow: 0 8px 24px rgba(0,0,0,0.02);
        }
        .score-circle {
            text-align: center; background: #fff5f5; border: 4px solid var(--critical);
            border-radius: 50%; width: 170px; height: 170px; display: flex;
            flex-direction: column; align-items: center; justify-content: center; margin: 0 auto;
        }
        .score-val { font-family: 'Space Grotesk', sans-serif; font-size: 50px; font-weight: 800; color: var(--critical); line-height: 1; }
        .score-lbl { font-size: 12px; font-weight: 700; color: #991b1b; text-transform: uppercase; margin-top: 4px; }

        .card { background: white; border-radius: 12px; border: 1px solid var(--border); padding: 24px; margin-bottom: 28px; }
        .card h3 { font-size: 18px; font-weight: 700; color: var(--primary); margin-bottom: 12px; }

        .callout-critical {
            background: #fff5f5; border: 1px solid #fed7d7; border-left: 5px solid var(--critical);
            border-radius: 8px; padding: 18px 20px; margin-bottom: 20px;
        }
        .callout-critical h4 { font-size: 15px; font-weight: 800; color: var(--critical); margin-bottom: 4px; }
        .callout-critical p { font-size: 13px; color: #7f1d1d; }

        .table-wrap { background: white; border-radius: 10px; border: 1px solid var(--border); overflow-x: auto; margin-bottom: 30px; }
        table { width: 100%; border-collapse: collapse; font-size: 13.5px; text-align: left; }
        thead { background: #f8fafc; border-bottom: 2px solid var(--border); }
        th { padding: 12px 16px; font-weight: 700; color: var(--primary); text-transform: uppercase; font-size: 11px; }
        td { padding: 12px 16px; border-bottom: 1px solid var(--border); color: #334155; }
        tbody tr:hover { background-color: #f8fafc; }

        .badge { display: inline-block; padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; text-transform: uppercase; }
        .badge-critical { background: var(--critical-bg); color: var(--critical); border: 1px solid #fecaca; }
        .badge-warning { background: var(--warning-bg); color: var(--warning); border: 1px solid #fde68a; }
        .badge-pass { background: var(--success-bg); color: var(--success); border: 1px solid #a7f3d0; }

        footer { background: white; border-top: 1px solid var(--border); padding: 30px 0; text-align: center; color: var(--text-muted); font-size: 13px; }
    </style>
</head>
<body>

<header>
    <div class="container">
        <div class="badge-client">Technical SEO & Next.js Website Audit</div>
        <h1 class="hero-title">PanelRight: Comprehensive Technical & On-Page Audit</h1>
        <p class="hero-subtitle">Rigorous diagnostic of www.panelright.com covering Next.js App Router architecture, crawlability, on-page semantics, and B2B organic lead generation.</p>
        
        <div class="meta-grid">
            <div class="meta-item"><div class="lbl">Domain</div><div class="val">www.panelright.com</div></div>
            <div class="meta-item"><div class="lbl">Framework / Host</div><div class="val">Next.js 13+ on Vercel</div></div>
            <div class="meta-item"><div class="lbl">Domain Authority</div><div class="val">DA: 6 | AS: 2 (Semrush)</div></div>
            <div class="meta-item"><div class="lbl">Organic Traffic</div><div class="val">0 Visits / Month</div></div>
        </div>
    </div>
</header>

<div class="sticky-nav">
    <div class="container">
        <div class="nav-links">
            <a href="#executive">Executive Summary</a>
            <a href="#critical-blockers">Critical Smoking Guns</a>
            <a href="#scorecard">Health Scorecard</a>
            <a href="#issues">Issues Log</a>
            <a href="#metadata">Metadata Rewrites</a>
            <a href="#roadmap">30-60-90 Roadmap</a>
        </div>
    </div>
</div>

<main class="container">

    <section id="executive">
        <div class="score-hero-card">
            <div class="score-circle">
                <div class="score-val">33</div>
                <div class="score-lbl">Health Score / 100</div>
            </div>
            <div>
                <h3 style="font-size: 22px; color: var(--primary); margin-bottom: 8px;">Technical Hosting is Fast, But SEO Foundation is Severely Incomplete</h3>
                <p style="color: #475569; font-size: 14.5px; margin-bottom: 14px;">
                    PanelRight is hosted on modern Vercel Edge infrastructure delivering lightning-fast response times (TTFB: 68 ms). However, the site suffers from <strong>zero organic search visibility</strong> because the development team deployed the site with <strong>Next.js 13 boilerplate template descriptions</strong>, <strong>7 H1 tags on the homepage</strong>, <strong>an 'Under Construction' placeholder page linked from the primary CTA</strong>, <strong>unmounted FAQ answers</strong>, and <strong>missing sitemaps/canonicals</strong>.
                </p>
                <div style="display: flex; gap: 8px; flex-wrap: wrap;">
                    <span class="badge badge-critical">Next.js Template Description Live</span>
                    <span class="badge badge-critical">7 H1 Tags on Homepage</span>
                    <span class="badge badge-critical">No XML Sitemap (404)</span>
                    <span class="badge badge-pass">TTFB 68ms (Vercel Edge)</span>
                </div>
            </div>
        </div>
    </section>

    <section id="critical-blockers">
        <h2 style="font-size: 22px; color: var(--primary); margin-bottom: 18px;">Critical "Smoking Gun" Defects</h2>

        <div class="callout-critical">
            <h4>1. Default Next.js 13 Template Description Active in Production</h4>
            <p><strong>Observed:</strong> Meta description on homepage reads: <em>"An open source application built using the new router, server components and everything new in Next.js 13."</em> This developer boilerplate from the <code>shadcn/taxonomy</code> starter kit appears in live Google search snippets.</p>
        </div>

        <div class="callout-critical">
            <h4>2. Primary CTA Links to a 25-Word "Under Construction" Page (/efficiency)</h4>
            <p><strong>Observed:</strong> The homepage CTA <em>"How We Find Efficient Solutions"</em> links to <code>/efficiency</code>, which displays only: <em>"Under Construction. This page is currently being built. Please check back soon."</em> Returns HTTP 200 without a noindex tag.</p>
        </div>

        <div class="callout-critical">
            <h4>3. Heading Dilution: 7 Separate H1 Tags on Homepage</h4>
            <p><strong>Observed:</strong> The homepage marks up every industry tab (Aviation, Marine, Medical, Automotive, Industrial, Consumer) as an <code>&lt;h1&gt;</code>, completely diluting core keyword focus.</p>
        </div>

        <div class="callout-critical">
            <h4>4. FAQ Answers Unmounted in Server-Rendered HTML (Invisible to Crawlers)</h4>
            <p><strong>Observed:</strong> Radix UI accordion renders closed answers with <code>&lt;div hidden=""&gt;&lt;/div&gt;</code>. Crawlers see 130 words of question headings and zero answers, blocking FAQ Rich Snippets.</p>
        </div>

        <div class="callout-critical">
            <h4>5. Live Legal Pages Contain Latin Lorem Ipsum ('Taxonomy App')</h4>
            <p><strong>Observed:</strong> <code>/privacy</code> and <code>/terms</code> are live on production and contain unedited Latin filler text referencing <em>"Taxonomy App"</em>.</p>
        </div>
    </section>

    <section id="scorecard">
        <h2 style="font-size: 22px; color: var(--primary); margin-bottom: 18px;">Detailed Audit Scorecard</h2>
        <div class="table-wrap">
            <table>
                <thead>
                    <tr><th>Area</th><th>Weight</th><th>Score</th><th>Status</th><th>Defect Summary</th></tr>
                </thead>
                <tbody>
                    <tr><td><strong>Crawlability & Sitemaps</strong></td><td>10</td><td><strong>2 / 10</strong></td><td><span class="badge badge-critical">Fail</span></td><td>sitemap.xml is 404; no sitemap pointer in robots.txt</td></tr>
                    <tr><td><strong>Canonicalisation</strong></td><td>10</td><td><strong>2 / 10</strong></td><td><span class="badge badge-critical">Fail</span></td><td>Missing canonical tags across 100% of pages</td></tr>
                    <tr><td><strong>On-Page Metadata</strong></td><td>10</td><td><strong>2 / 10</strong></td><td><span class="badge badge-critical">Critical</span></td><td>Next.js 13 template descriptions; titles under 20 chars</td></tr>
                    <tr><td><strong>Heading Hierarchy</strong></td><td>10</td><td><strong>2 / 10</strong></td><td><span class="badge badge-critical">Critical</span></td><td>7 H1 tags on homepage; 0 H1 tags on /efficiency</td></tr>
                    <tr><td><strong>Content Depth</strong></td><td>10</td><td><strong>2 / 10</strong></td><td><span class="badge badge-critical">Critical</span></td><td>Primary CTA leads to 25-word 'Under Construction' page; FAQ unmounted</td></tr>
                    <tr><td><strong>Performance & Speed</strong></td><td>10</td><td><strong>10 / 10</strong></td><td><span class="badge badge-pass">Pass</span></td><td>Vercel Edge delivery is ultra fast (TTFB 68ms, FCP 500ms)</td></tr>
                    <tr><td><strong>Structured Data</strong></td><td>10</td><td><strong>0 / 10</strong></td><td><span class="badge badge-critical">Fail</span></td><td>Zero Schema.org JSON-LD blocks across the domain</td></tr>
                    <tr><td><strong>E-E-A-T & Trust</strong></td><td>10</td><td><strong>2 / 10</strong></td><td><span class="badge badge-critical">Critical</span></td><td>No company address, phone, or leadership info; Latin Lorem Ipsum legal pages</td></tr>
                </tbody>
            </table>
        </div>
    </section>

</main>

<footer>
    <div class="container">
        <p>PanelRight Technical SEO & Website Audit &bull; Confidential Client Deliverable</p>
    </div>
</footer>

</body>
</html>
"""

with open(os.path.join(output_dir, "Client_SEO_Audit_Report.html"), "w", encoding="utf-8") as f:
    f.write(html_report)
with open(os.path.join(output_dir, "SEO_Audit_Report.html"), "w", encoding="utf-8") as f:
    f.write(html_report)

print("Client_SEO_Audit_Report.html generated successfully!")

print("\n=== GENERATING CLIENT_SEO_AUDIT_REPORT.DOCX ===")

doc = docx.Document()
for s in doc.sections:
    s.top_margin = Inches(1.0)
    s.bottom_margin = Inches(1.0)
    s.left_margin = Inches(1.0)
    s.right_margin = Inches(1.0)

COLOR_NAVY = RGBColor(10, 25, 47)
COLOR_BLUE = RGBColor(37, 99, 235)
COLOR_RED = RGBColor(220, 38, 38)
COLOR_DARK = RGBColor(15, 23, 42)

title_p = doc.add_paragraph()
r = title_p.add_run("TECHNICAL SEO & ON-PAGE WEBSITE AUDIT")
r.font.name = "Arial"
r.font.size = Pt(22)
r.font.bold = True
r.font.color.rgb = COLOR_NAVY
title_p.paragraph_format.space_after = Pt(2)

sub_p = doc.add_paragraph()
r_sub = sub_p.add_run("PanelRight (www.panelright.com) | PCB Panel Optimization Software")
r_sub.font.name = "Arial"
r_sub.font.size = Pt(13)
r_sub.font.color.rgb = COLOR_BLUE
sub_p.paragraph_format.space_after = Pt(16)

meta_table = doc.add_table(rows=5, cols=2)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_data = [
    ("Client Website:", "https://www.panelright.com/"),
    ("Application Portal:", "https://solutions.panelright.com/contact"),
    ("Technology Stack:", "Next.js 13+ (App Router) on Vercel / AWS"),
    ("Audit Date:", "October 14, 2026"),
    ("Overall Website Health Score:", "33 / 100 (Critical Remediation Required)")
]
for idx, (lbl, val) in enumerate(meta_data):
    c1, c2 = meta_table.rows[idx].cells
    c1.text = lbl
    c2.text = val
    c1.paragraphs[0].runs[0].bold = True
    if "Health Score" in lbl:
        c2.paragraphs[0].runs[0].bold = True
        c2.paragraphs[0].runs[0].font.color.rgb = COLOR_RED

doc.add_paragraph().paragraph_format.space_after = Pt(12)

def add_heading(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = COLOR_NAVY
    return p

def add_p(text, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.name = "Arial"
        r_pre.font.size = Pt(10)
    r = p.add_run(text)
    r.font.name = "Arial"
    r.font.size = Pt(10)
    r.font.color.rgb = COLOR_DARK
    return p

add_heading("1. Executive Summary & Core Baseline")
add_p("PanelRight provides a specialized B2B algorithmic software solution for PCB panel optimization and circuit board nesting to minimize eWaste and reduce fabrication costs. Despite fast Vercel server performance (TTFB 68ms), the site achieves an overall technical health score of only 33/100 and currently has zero organic search visibility (Semrush Authority Score: 2, Organic Traffic: 0, AI Search Visibility: 0; Moz DA: 6, Brand Authority: 1).")

add_heading("2. Critical 'Smoking Gun' Findings")
add_p("Meta description on homepage and /efficiency reads: 'An open source application built using the new router, server components and everything new in Next.js 13.' This template boilerplate from the shadcn/taxonomy starter kit appears directly in Google search snippets.", "1. Default Next.js 13 Description in Production: ")
add_p("The primary homepage CTA ('How We Find Efficient Solutions') links to /efficiency, which displays a 25-word 'Under Construction' placeholder. It contains 0 H1s and returns HTTP 200 without a noindex tag.", "2. Broken Primary CTA Page: ")
add_p("The homepage marks up 7 separate <h1> tags (the main slogan plus all 6 industry tabs: Aviation, Marine, Medical, Automotive, Industrial, Consumer), severely diluting keyword relevance.", "3. Severe Heading Dilution (7 H1s): ")
add_p("Radix UI accordion unmounts answers from the server HTML (<div hidden=''></div>). Googlebot sees only 130 words of question headings and zero answer text.", "4. FAQ Answers Unmounted in Server DOM: ")
add_p("/privacy and /terms are live in production containing unedited Latin Lorem Ipsum text referencing 'Taxonomy App'. Neither is linked in the footer.", "5. Latin Lorem Ipsum on Legal Pages: ")
add_p("https://www.panelright.com/sitemap.xml returns HTTP 404, and 100% of pages lack canonical tags.", "6. Missing Sitemaps & Canonical Tags: ")

add_heading("3. Immediate 10-Point Technical Action Plan")
add_p("1. Replace Next.js 13 template description in app/layout.tsx with optimized B2B PCB panelization copy.")
add_p("2. Demote the 6 industry H1 tags on the homepage to <h3> or <div>, retaining a single optimized <h1>.")
add_p("3. Deploy app/sitemap.ts in Next.js and add the sitemap reference to public/robots.txt.")
add_p("4. Configure metadataBase and alternates: { canonical: './' } in app/layout.tsx to deploy canonical tags.")
add_p("5. Ensure Radix UI FAQ accordion renders answer text into the initial server HTML payload.")
add_p("6. Replace the 25-word 'Under Construction' placeholder on /efficiency with a comprehensive technical algorithm breakdown.")
add_p("7. Draft and publish legitimate B2B Privacy Policy and Terms of Service, replacing the Latin Lorem Ipsum.")
add_p("8. Add links to Privacy, Terms, and Contact in the global footer.")
add_p("9. Replace the ephemeral Vercel preview OpenGraph image with an official production asset.")
add_p("10. Add X-Frame-Options and X-Content-Type-Options security headers in next.config.js.")

doc.save(os.path.join(output_dir, "Client_SEO_Audit_Report.docx"))
doc.save(os.path.join(output_dir, "SEO_Audit_Report.docx"))
print("Client_SEO_Audit_Report.docx generated successfully!")
