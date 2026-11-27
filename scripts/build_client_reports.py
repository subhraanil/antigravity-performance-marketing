import os
import csv
import json
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

dest_dirs = [r"website audit\victoryhcspl.com", "."]

print("=== 1. UPDATING 04_ISSUES_LOG.CSV WITH NEW VERIFIED FINDINGS ===")
# Read existing issues
existing_issues = []
with open(r"website audit\victoryhcspl.com\04_issues_log.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    existing_issues = list(reader)

new_findings = [
    {
        "ID": "ISS-021",
        "Category": "UX & Conversion (Critical)",
        "Severity": "P0 Critical",
        "Issue": "Hero Banner CTA Button 'Our Services' Links to Non-Existent Anchor (#services)",
        "Affected URLs": "https://victoryhcspl.com/ (Homepage Hero Section)",
        "Evidence": "Button href is '#services', but no DOM element on the homepage has id='services'. Clicking the button produces zero action.",
        "Fix": "Assign id='services' to the services section container in Elementor, or update button link directly to 'https://victoryhcspl.com/healthcare-training/'.",
        "Effort": "S",
        "Owner": "Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-022",
        "Category": "UX & Mobile Usability",
        "Severity": "P1 High",
        "Issue": "Top Header Menu Email and Phone Number Are Plain Text (Not Clickable)",
        "Affected URLs": "Site-wide Header (All Pages)",
        "Evidence": "Header contact info rendered inside <p class='elementor-icon-box-description'> with 0 <a> tags. Users cannot click to call or click to mail.",
        "Fix": "Wrap email with <a href='mailto:victoryantovijay@gmail.com'> and phone with <a href='tel:+919916509090'> in Elementor Header Template.",
        "Effort": "S",
        "Owner": "Developer",
        "Status": "Open"
    },
    {
        "ID": "ISS-023",
        "Category": "Branding & Knowledge Graph",
        "Severity": "P2 Medium",
        "Issue": "Facebook & LinkedIn Icons Link to Founder's Personal Profile Instead of Company Pages",
        "Affected URLs": "Header & Footer (All Pages)",
        "Evidence": "Links point to personal profiles: facebook.com/anto.r.delvi/ and linkedin.com/in/antorameshdelvi.",
        "Fix": "Create/link official company pages (e.g. linkedin.com/company/victory-healthcare-services/) for institutional branding and Google Entity recognition.",
        "Effort": "S",
        "Owner": "Client / SEO",
        "Status": "Open"
    },
    {
        "ID": "ISS-024",
        "Category": "Hygiene & Social Signals",
        "Severity": "P2 Medium",
        "Issue": "Twitter/X and Instagram Social Icons Have Blank Links (href='')",
        "Affected URLs": "Header & Footer (All Pages)",
        "Evidence": "Social icon anchors have href='' resulting in dead links.",
        "Fix": "Add active company social profile URLs, or remove the icons from Elementor social widget if channels are inactive.",
        "Effort": "S",
        "Owner": "Developer",
        "Status": "Open"
    }
]

# Avoid duplicate additions
existing_ids = {r["ID"] for r in existing_issues}
for nf in new_findings:
    if nf["ID"] not in existing_ids:
        existing_issues.append(nf)

for d in dest_dirs:
    with open(f"{d}/04_issues_log.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["ID", "Category", "Severity", "Issue", "Affected URLs", "Evidence", "Fix", "Effort", "Owner", "Status"])
        writer.writeheader()
        writer.writerows(existing_issues)

print(f"Updated 04_issues_log.csv with {len(existing_issues)} total issues.")

print("\n=== 2. GENERATING PROFESSIONAL HTML CLIENT REPORT ===")

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Technical SEO & Website Audit Report | Victory Healthcare Services Pvt Ltd</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary: #0f2b48;
            --primary-light: #1a4470;
            --accent: #0284c7;
            --accent-glow: rgba(2, 132, 199, 0.15);
            --teal: #0d9488;
            --bg-main: #f8fafc;
            --card-bg: #ffffff;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --critical: #ef4444;
            --critical-bg: #fef2f2;
            --warning: #f59e0b;
            --warning-bg: #fffbeb;
            --success: #10b981;
            --success-bg: #ecfdf5;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: var(--bg-main);
            color: var(--text-main);
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }

        .container {
            max-width: 1240px;
            margin: 0 auto;
            padding: 0 24px;
        }

        /* Header / Hero */
        header {
            background: linear-gradient(135deg, var(--primary) 0%, #081a2d 100%);
            color: white;
            padding: 60px 0 50px;
            border-bottom: 4px solid var(--accent);
            position: relative;
            overflow: hidden;
        }

        header::after {
            content: '';
            position: absolute;
            top: -50%;
            right: -10%;
            width: 500px;
            height: 500px;
            background: radial-gradient(circle, var(--accent-glow) 0%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
        }

        .badge-client {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(255, 255, 255, 0.12);
            backdrop-filter: blur(8px);
            padding: 6px 14px;
            border-radius: 9999px;
            font-size: 13px;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            color: #93c5fd;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.15);
        }

        .hero-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 38px;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 14px;
            color: #ffffff;
        }

        .hero-subtitle {
            font-size: 17px;
            color: #cbd5e1;
            max-width: 850px;
            margin-bottom: 28px;
        }

        .meta-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
            background: rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 18px 24px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }

        .meta-item .label {
            font-size: 12px;
            text-transform: uppercase;
            color: #94a3b8;
            font-weight: 600;
            margin-bottom: 4px;
        }

        .meta-item .val {
            font-size: 15px;
            font-weight: 700;
            color: #f8fafc;
        }

        /* Navigation Bar */
        .sticky-nav {
            position: sticky;
            top: 0;
            background: white;
            border-bottom: 1px solid var(--border);
            z-index: 100;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        }

        .nav-links {
            display: flex;
            gap: 24px;
            padding: 14px 0;
            overflow-x: auto;
            white-space: nowrap;
        }

        .nav-links a {
            text-decoration: none;
            color: var(--text-muted);
            font-weight: 600;
            font-size: 14px;
            transition: all 0.2s;
            padding: 6px 12px;
            border-radius: 6px;
        }

        .nav-links a:hover, .nav-links a.active {
            color: var(--accent);
            background: var(--accent-glow);
        }

        /* Main Content */
        main {
            padding: 48px 0 80px;
        }

        .section-header {
            margin-bottom: 28px;
        }

        .section-tag {
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--accent);
            margin-bottom: 6px;
            display: block;
        }

        .section-title {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 26px;
            font-weight: 700;
            color: var(--primary);
        }

        /* Scorecards */
        .score-hero-card {
            background: white;
            border-radius: 16px;
            border: 1px solid var(--border);
            padding: 32px;
            margin-bottom: 40px;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.04);
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 40px;
            align-items: center;
        }

        .score-circle {
            text-align: center;
            background: #fff5f5;
            border: 4px solid var(--critical);
            border-radius: 50%;
            width: 200px;
            height: 200px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0 auto;
            box-shadow: 0 8px 24px rgba(239, 68, 68, 0.15);
        }

        .score-val {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 58px;
            font-weight: 800;
            color: var(--critical);
            line-height: 1;
        }

        .score-label {
            font-size: 14px;
            font-weight: 700;
            color: #991b1b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 6px;
        }

        .score-breakdown-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
        }

        .cat-card {
            background: #f8fafc;
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 14px 16px;
        }

        .cat-card .cat-title {
            font-size: 13px;
            font-weight: 700;
            color: var(--text-muted);
            margin-bottom: 4px;
        }

        .cat-card .cat-score {
            font-size: 18px;
            font-weight: 800;
            color: var(--primary);
        }

        /* User Findings Callout Box */
        .callout-box {
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border: 1px solid #bfdbfe;
            border-left: 6px solid var(--accent);
            border-radius: 12px;
            padding: 24px 28px;
            margin-bottom: 40px;
        }

        .callout-title {
            font-size: 18px;
            font-weight: 800;
            color: #1e40af;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .findings-list {
            list-style: none;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 16px;
        }

        .finding-item {
            background: white;
            border-radius: 8px;
            padding: 14px 18px;
            border: 1px solid #cbd5e1;
            box-shadow: 0 2px 6px rgba(0,0,0,0.02);
        }

        .finding-item h4 {
            font-size: 14px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .finding-item p {
            font-size: 13px;
            color: #475569;
        }

        /* Tables */
        .table-wrap {
            background: white;
            border-radius: 12px;
            border: 1px solid var(--border);
            overflow-x: auto;
            margin-bottom: 36px;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.02);
        }

        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
            text-align: left;
        }

        thead {
            background: #f1f5f9;
            border-bottom: 2px solid var(--border);
        }

        th {
            padding: 14px 18px;
            font-weight: 700;
            color: var(--primary);
            text-transform: uppercase;
            font-size: 12px;
            letter-spacing: 0.5px;
        }

        td {
            padding: 14px 18px;
            border-bottom: 1px solid var(--border);
            color: #334155;
            vertical-align: top;
        }

        tbody tr:last-child td {
            border-bottom: none;
        }

        tbody tr:hover {
            background-color: #f8fafc;
        }

        /* Badges */
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 700;
            text-transform: uppercase;
        }

        .badge-critical {
            background: var(--critical-bg);
            color: var(--critical);
            border: 1px solid #fca5a5;
        }

        .badge-warning {
            background: var(--warning-bg);
            color: #b45309;
            border: 1px solid #fde68a;
        }

        .badge-pass {
            background: var(--success-bg);
            color: var(--teal);
            border: 1px solid #a7f3d0;
        }

        /* Deep Dive Box */
        .card {
            background: white;
            border-radius: 14px;
            border: 1px solid var(--border);
            padding: 28px;
            margin-bottom: 32px;
            box-shadow: 0 4px 16px rgba(0,0,0,0.02);
        }

        .card h3 {
            font-size: 18px;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 12px;
        }

        .highlight-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }

        .highlight-item {
            border-left: 4px solid var(--accent);
            background: #f8fafc;
            padding: 14px 16px;
            border-radius: 0 8px 8px 0;
        }

        .highlight-item h5 {
            font-size: 13px;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 4px;
        }

        .highlight-item p {
            font-size: 13px;
            color: #475569;
        }

        /* Code block */
        pre {
            background: #0f172a;
            color: #e2e8f0;
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            font-size: 13px;
            margin: 14px 0;
        }

        /* Footer */
        footer {
            background: white;
            border-top: 1px solid var(--border);
            padding: 36px 0;
            text-align: center;
            color: var(--text-muted);
            font-size: 14px;
        }

        @media (max-width: 768px) {
            .score-hero-card {
                grid-template-columns: 1fr;
                gap: 24px;
                text-align: center;
            }
            .hero-title {
                font-size: 28px;
            }
        }
    </style>
</head>
<body>

<header>
    <div class="container">
        <div class="badge-client">Client Technical SEO & Growth Report</div>
        <h1 class="hero-title">Website Technical Audit & Strategic SEO Roadmap</h1>
        <p class="hero-subtitle">Comprehensive diagnostic of victoryhcspl.com with deep-dive performance analysis of the Primary Service Page (/healthcare-training/) for the Indian market.</p>
        
        <div class="meta-grid">
            <div class="meta-item">
                <div class="label">Client Website</div>
                <div class="val">victoryhcspl.com</div>
            </div>
            <div class="meta-item">
                <div class="label">Target Market</div>
                <div class="val">India (Bangalore Focus)</div>
            </div>
            <div class="meta-item">
                <div class="label">Audit Date</div>
                <div class="val">September 24, 2026</div>
            </div>
            <div class="meta-item">
                <div class="label">Auditor</div>
                <div class="val">Senior Technical SEO Auditor</div>
            </div>
        </div>
    </div>
</header>

<div class="sticky-nav">
    <div class="container">
        <div class="nav-links">
            <a href="#executive-summary">Executive Summary</a>
            <a href="#client-findings">Client Verified UX Issues</a>
            <a href="#health-score">Health Scorecard</a>
            <a href="#primary-service">Course Page Deep-Dive</a>
            <a href="#technical-modules">Technical Findings</a>
            <a href="#competitors">Competitors & Keywords</a>
            <a href="#roadmap">30-60-90 Roadmap</a>
        </div>
    </div>
</div>

<main class="container">

    <!-- Section 1: Executive Summary -->
    <section id="executive-summary" style="margin-bottom: 48px;">
        <div class="section-header">
            <span class="section-tag">High-Level Executive Brief</span>
            <h2 class="section-title">Executive Summary & Current State</h2>
        </div>

        <div class="score-hero-card">
            <div class="score-circle">
                <div class="score-val">44</div>
                <div class="score-label">Health Score / 100</div>
            </div>
            <div>
                <h3 style="font-size: 22px; font-weight: 800; color: var(--primary); margin-bottom: 12px;">Critical Technical & Conversion Intervention Required</h3>
                <p style="color: #475569; font-size: 15px; margin-bottom: 16px;">
                    Victory Healthcare Services possesses an exceptional real-world foundation: leadership by <strong>Mr. Anto Ramesh Delvi</strong> (30 years experience; former General Manager at <strong>Columbia Asia Hospitals</strong>; trained 300+ imaging officers) and <strong>Mr. Vijaya Kumar C</strong> (19+ years at Columbia Asia & Manipal). However, the digital asset is currently hindered by <strong>broken robots governance</strong>, <strong>missing H1 headings across 90% of the site</strong>, <strong>zero analytics/conversion tracking</strong>, and a <strong>total lack of enquiry forms on course pages</strong>.
                </p>
                <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                    <span class="badge badge-critical">100% Tracking Blindspot</span>
                    <span class="badge badge-critical">0 Lead Forms on Service Page</span>
                    <span class="badge badge-warning">Missing Legal Trust Pages</span>
                    <span class="badge badge-pass">Fast Server (Mumbai 67ms)</span>
                </div>
            </div>
        </div>
    </section>

    <!-- Section 2: Client Verified UX Issues -->
    <section id="client-findings" style="margin-bottom: 48px;">
        <div class="callout-box">
            <div class="callout-title">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>
                Verified Client UX & Conversion Deficiencies (Immediate Fixes)
            </div>
            <p style="font-size: 14px; color: #1e3a8a; margin-bottom: 16px;">The specific front-end navigation and conversion issues reported have been empirically verified in the live code and documented below:</p>
            
            <div class="findings-list">
                <div class="finding-item">
                    <h4>1. Top Menu Email & Phone Not Clickable <span class="badge badge-critical">P1 High</span></h4>
                    <p><strong>Observed:</strong> Contact information is wrapped in <code>&lt;p class="elementor-icon-box-description"&gt;</code> without any <code>&lt;a&gt;</code> tag. Users cannot click to call on mobile or click to email.</p>
                    <p style="margin-top: 6px; color: #0284c7;"><strong>Fix:</strong> Wrap phone in <code>&lt;a href="tel:+919916509090"&gt;</code> and email in <code>&lt;a href="mailto:victoryantovijay@gmail.com"&gt;</code>.</p>
                </div>
                
                <div class="finding-item">
                    <h4>2. Banner Button "Our Services" Broken <span class="badge badge-critical">P0 Critical</span></h4>
                    <p><strong>Observed:</strong> The hero CTA button links to <code>href="#services"</code>. However, no element with <code>id="services"</code> exists anywhere on the homepage, rendering the main CTA dead.</p>
                    <p style="margin-top: 6px; color: #0284c7;"><strong>Fix:</strong> Add <code>id="services"</code> to the services section or link directly to <code>/healthcare-training/</code>.</p>
                </div>

                <div class="finding-item">
                    <h4>3. Facebook & LinkedIn Link to Personal Profile <span class="badge badge-warning">P2 Med</span></h4>
                    <p><strong>Observed:</strong> Links point to <code>facebook.com/anto.r.delvi/</code> and <code>linkedin.com/in/antorameshdelvi</code> instead of corporate business pages.</p>
                    <p style="margin-top: 6px; color: #0284c7;"><strong>Fix:</strong> Point social links to official corporate pages to support Google Entity recognition.</p>
                </div>

                <div class="finding-item">
                    <h4>4. Twitter/X and Instagram Blank Links <span class="badge badge-warning">P2 Med</span></h4>
                    <p><strong>Observed:</strong> Social icons in both header and footer have empty <code>href=""</code> attributes, frustrating users who click them.</p>
                    <p style="margin-top: 6px; color: #0284c7;"><strong>Fix:</strong> Add active social links or disable the unused social icons in Elementor.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- Section 3: Health Score Breakdown -->
    <section id="health-score" style="margin-bottom: 48px;">
        <div class="section-header">
            <span class="section-tag">Audit Breakdown</span>
            <h2 class="section-title">Website Technical Health Scorecard</h2>
        </div>

        <div class="table-wrap">
            <table>
                <thead>
                    <tr>
                        <th>Category</th>
                        <th>Weight</th>
                        <th>Score</th>
                        <th>Status</th>
                        <th>Observed Defect & Primary Fix</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Crawlability & Robots Hygiene</strong></td>
                        <td>10</td>
                        <td><strong>5 / 10</strong></td>
                        <td><span class="badge badge-critical">Fail</span></td>
                        <td>robots.txt redirects (301) to homepage; dummy <code>#!</code> navigation links create crawl loops. Deploy valid static robots.txt.</td>
                    </tr>
                    <tr>
                        <td><strong>Indexability & URL Architecture</strong></td>
                        <td>10</td>
                        <td><strong>7 / 10</strong></td>
                        <td><span class="badge badge-warning">Warning</span></td>
                        <td>Core 10 pages indexable, but 10 duplicate <code>#!</code> URLs discovered by crawlers. Remove internal dummy links.</td>
                    </tr>
                    <tr>
                        <td><strong>On-Page SEO & Metadata</strong></td>
                        <td>10</td>
                        <td><strong>3 / 10</strong></td>
                        <td><span class="badge badge-critical">Critical</span></td>
                        <td>Missing H1 on 90% of site (including course page); auto-scraped 420+ char meta descriptions. Deploy unique H1s and 155-char meta copy.</td>
                    </tr>
                    <tr>
                        <td><strong>Content Quality & E-E-A-T</strong></td>
                        <td>10</td>
                        <td><strong>4 / 10</strong></td>
                        <td><span class="badge badge-warning">Warning</span></td>
                        <td>Founders' 49+ years Columbia Asia/Manipal experience omitted on course page; 0 blog articles. Inject faculty profiles.</td>
                    </tr>
                    <tr>
                        <td><strong>Performance & Core Web Vitals</strong></td>
                        <td>10</td>
                        <td><strong>6 / 10</strong></td>
                        <td><span class="badge badge-warning">Warning</span></td>
                        <td>Server responds fast in Mumbai (TTFB 67ms), but malformed script tag causes duplicate download of 220KB HTML as JS.</td>
                    </tr>
                    <tr>
                        <td><strong>Mobile & Rendering Parity</strong></td>
                        <td>10</td>
                        <td><strong>7 / 10</strong></td>
                        <td><span class="badge badge-pass">Pass</span></td>
                        <td>Responsive viewport; no horizontal overflow on Pixel 7; but contact form depends 100% on client-side JS rendering.</td>
                    </tr>
                    <tr>
                        <td><strong>Structured Data (Schema.org)</strong></td>
                        <td>10</td>
                        <td><strong>3 / 10</strong></td>
                        <td><span class="badge badge-critical">Fail</span></td>
                        <td>Only generic AIOSEO WebPage; 0 Course, 0 LocalBusiness, 0 FAQ schemas. Deploy validated JSON-LD schema suite.</td>
                    </tr>
                    <tr>
                        <td><strong>Local SEO & Geo-Targeting</strong></td>
                        <td>10</td>
                        <td><strong>3 / 10</strong></td>
                        <td><span class="badge badge-warning">Warning</span></td>
                        <td>Residential apartment listed without clinical training lab mention; unverified GBP embed; missing Indian citations.</td>
                    </tr>
                    <tr>
                        <td><strong>UX & Conversion Optimization</strong></td>
                        <td>10</td>
                        <td><strong>2 / 10</strong></td>
                        <td><span class="badge badge-critical">Critical</span></td>
                        <td>Zero enquiry forms on /healthcare-training/; free Gmail used; dead hero banner CTA button.</td>
                    </tr>
                    <tr>
                        <td><strong>Security & Legal Compliance</strong></td>
                        <td>10</td>
                        <td><strong>4 / 10</strong></td>
                        <td><span class="badge badge-critical">Critical</span></td>
                        <td>Missing X-Frame-Options/CSP; 404 on Privacy Policy violates India's Digital Personal Data Protection Act 2023.</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </section>

    <!-- Section 4: Primary Service Page Deep-Dive -->
    <section id="primary-service" style="margin-bottom: 48px;">
        <div class="section-header">
            <span class="section-tag">Focal Opportunity</span>
            <h2 class="section-title">Primary Service Page Deep-Dive: /healthcare-training/</h2>
        </div>

        <div class="card">
            <h3>Current State vs. Conversion Best Practice</h3>
            <p style="color: #475569; margin-bottom: 16px;">
                The primary service page targets students, technologists, and hospital administrators seeking advanced radiology training in India. However, it currently contains only 571 words of high-level overview text without tuition fees, course duration, batch dates, eligibility criteria, or downloadable curriculum.
            </p>

            <div class="highlight-grid">
                <div class="highlight-item">
                    <h5>Missing H1 Tag (0 Found)</h5>
                    <p>The page currently lacks an H1 tag. Recommended fix: <code>&lt;h1&gt;Comprehensive Healthcare & Medical Imaging Training Programs&lt;/h1&gt;</code>.</p>
                </div>
                <div class="highlight-item">
                    <h5>Corrupted Heading Typography</h5>
                    <p>An entire 50-word overview paragraph is wrapped in an <code>&lt;h3&gt;</code> tag, and the footer agency credit is an <code>&lt;h2&gt;</code>.</p>
                </div>
                <div class="highlight-item">
                    <h5>0 Conversion Forms on Page</h5>
                    <p>Visitors who want to apply or request fees cannot do so on the page, resulting in near-total conversion bounce.</p>
                </div>
                <div class="highlight-item">
                    <h5>Unleveraged E-E-A-T Credentials</h5>
                    <p>Mr. Anto Ramesh Delvi and Mr. Vijaya Kumar C's 49+ years of hospital leadership at Columbia Asia are omitted from this page.</p>
                </div>
            </div>

            <h4 style="margin: 20px 0 10px; color: var(--primary);">Identified Modality Scope (Pillar Structure)</h4>
            <p style="font-size: 14px; color: #475569;">Victory HCS specializes in high-end medical imaging modalities that should each have dedicated landing pages:</p>
            <ul style="margin-left: 20px; font-size: 14px; color: #334155; line-height: 1.8;">
                <li><strong>Cross Sectional Imaging Course:</strong> Anatomy protocols & multiplanar diagnostic interpretation.</li>
                <li><strong>CT & MRI Module-Based Training:</strong> Hands-on scanner protocols, artifact reduction, clinical workflows.</li>
                <li><strong>Training on Ultrasound (Sonographer):</strong> Probe manipulation, pelvic/abdominal scanning, imaging physics.</li>
                <li><strong>Post Processing Hands-On Training (Bi-Annual):</strong> 3D volume rendering on Siemens, GE, Vitrea workstations.</li>
                <li><strong>Radiology Administration:</strong> PACS/RIS administration, department logistics, turnaround time management.</li>
                <li><strong>Quality Assurance:</strong> Radiation safety, AERB/NABH compliance, routine equipment QA audits.</li>
            </ul>
        </div>
    </section>

    <!-- Section 5: Roadmap -->
    <section id="roadmap" style="margin-bottom: 48px;">
        <div class="section-header">
            <span class="section-tag">Action Plan</span>
            <h2 class="section-title">Phased 30-60-90 Day Implementation Roadmap</h2>
        </div>

        <div class="card">
            <h4 style="color: var(--primary); margin-bottom: 8px;">Phase 1: Days 1–30 (Foundation & Quick Wins)</h4>
            <p style="font-size: 14px; color: #475569; margin-bottom: 12px;">Deploy valid robots.txt; install GTM & GA4; fix hero CTA button "Our Services"; make top bar email and phone clickable; embed admission lead form on /healthcare-training/; publish DPDP-compliant Privacy Policy; deploy security headers.</p>

            <h4 style="color: var(--primary); margin-bottom: 8px;">Phase 2: Days 31–60 (Authority & Architecture Expansion)</h4>
            <p style="font-size: 14px; color: #475569; margin-bottom: 12px;">Create 6 dedicated child modality landing pages (CT/MRI, Ultrasound, Post-Processing); inject Columbia Asia faculty credentials; deploy Schema.org Course and LocalBusiness markup; execute internal linking plan.</p>

            <h4 style="color: var(--primary); margin-bottom: 8px;">Phase 3: Days 61–90 (Local Domination & Scale)</h4>
            <p style="font-size: 14px; color: #475569;">Claim and optimize Google Business Profile; build 25+ local citations across Indian directories (Justdial, Sulekha, IndiaMART); initiate thought leadership PR; review CRO funnels.</p>
        </div>
    </section>

</main>

<footer>
    <div class="container">
        <p>Technical SEO & Website Audit Report &bull; Victory Healthcare Services Pvt Ltd &bull; Confidential Client Document</p>
        <p style="font-size: 12px; margin-top: 6px; color: #94a3b8;">Generated on September 24, 2026 by Senior Technical SEO & Website Auditor</p>
    </div>
</footer>

</body>
</html>
"""

for d in dest_dirs:
    with open(f"{d}/Client_SEO_Audit_Report.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    with open(f"{d}/SEO_Audit_Report.html", "w", encoding="utf-8") as f:
        f.write(html_content)

print("Client_SEO_Audit_Report.html and SEO_Audit_Report.html generated successfully!")

print("\n=== 3. GENERATING EXECUTIVE CLIENT DOCX REPORT ===")

def create_client_docx(file_path):
    doc = docx.Document()
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # Styles
    COLOR_NAVY = RGBColor(15, 43, 72)
    COLOR_BLUE = RGBColor(2, 132, 199)
    COLOR_RED = RGBColor(239, 68, 68)
    COLOR_DARK = RGBColor(15, 23, 42)

    # Cover Header
    title_p = doc.add_paragraph()
    r = title_p.add_run("TECHNICAL SEO & COMPREHENSIVE WEBSITE AUDIT")
    r.font.name = "Arial"
    r.font.size = Pt(22)
    r.font.bold = True
    r.font.color.rgb = COLOR_NAVY
    title_p.paragraph_format.space_after = Pt(2)

    sub_p = doc.add_paragraph()
    r_sub = sub_p.add_run("Client Technical & Conversion Report | Healthcare Training Growth Strategy")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(13)
    r_sub.font.color.rgb = COLOR_BLUE
    sub_p.paragraph_format.space_after = Pt(18)

    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_info = [
        ("Client Website:", "https://victoryhcspl.com/"),
        ("Primary Service Focus:", "https://victoryhcspl.com/healthcare-training/"),
        ("Target Market & Geo:", "India (Bangalore & Pan-India Medical Technologists)"),
        ("Audit Date:", "September 24, 2026"),
        ("Overall Technical Health Score:", "44 / 100 (Critical Remediation Required)")
    ]
    for idx, (lbl, val) in enumerate(meta_info):
        c1, c2 = meta_table.rows[idx].cells
        c1.text = lbl
        c2.text = val
        c1.paragraphs[0].runs[0].bold = True
        c1.paragraphs[0].runs[0].font.size = Pt(10)
        c2.paragraphs[0].runs[0].font.size = Pt(10)
        if "Health Score" in lbl:
            c2.paragraphs[0].runs[0].bold = True
            c2.paragraphs[0].runs[0].font.color.rgb = COLOR_RED

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(text)
        run.font.name = "Arial"
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = COLOR_NAVY
        return p

    def add_para(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            rp = p.add_run(bold_prefix)
            rp.bold = True
            rp.font.name = "Arial"
            rp.font.size = Pt(10)
        r = p.add_run(text)
        r.font.name = "Arial"
        r.font.size = Pt(10)
        r.font.color.rgb = COLOR_DARK
        return p

    add_h1("1. Client-Identified Front-End & UX Issues (Empirically Verified)")
    add_para("The specific front-end defects and conversion issues identified have been tested directly against the live DOM and verified with exact technical evidence:")

    ux_table = doc.add_table(rows=1, cols=4)
    ux_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cols = ["Defect", "Priority", "Observed Code State", "Recommended Fix"]
    for i, col in enumerate(cols):
        ux_table.rows[0].cells[i].text = col
        ux_table.rows[0].cells[i].paragraphs[0].runs[0].bold = True
        ux_table.rows[0].cells[i].paragraphs[0].runs[0].font.size = Pt(9.5)

    ux_rows = [
        ("Banner Button 'Our Services' Broken", "P0 Critical", "Button href='#services'. No DOM element with id='services' exists on homepage; clicking button produces zero action.", "Assign id='services' to services container, or link directly to /healthcare-training/."),
        ("Top Menu Phone & Email Not Clickable", "P1 High", "Header contact rendered in <p class='elementor-icon-box-description'> with 0 <a> tags. Users cannot click to call or click to mail.", "Wrap phone with <a href='tel:+919916509090'> and email with <a href='mailto:victoryantovijay@gmail.com'>."),
        ("Facebook & LinkedIn Link to Personal Profile", "P2 Medium", "Links point to personal profiles: facebook.com/anto.r.delvi/ and linkedin.com/in/antorameshdelvi.", "Point to official corporate company pages to build Google Knowledge Graph entity authority."),
        ("Twitter/X and Instagram Blank Links", "P2 Medium", "Social icon anchors in header and footer have empty href='' attributes.", "Add active corporate social profiles or remove unused placeholder icons.")
    ]

    for row in ux_rows:
        rc = ux_table.add_row().cells
        for idx, val in enumerate(row):
            rc[idx].text = val
            rc[idx].paragraphs[0].runs[0].font.name = "Arial"
            rc[idx].paragraphs[0].runs[0].font.size = Pt(9)
            if idx == 1:
                rc[idx].paragraphs[0].runs[0].bold = True

    add_h1("2. Executive Summary & Health Scorecard (44/100)")
    add_para("Victory Healthcare Services operates at the intersection of medical technology solutions and clinical healthcare education. While the website enjoys fast server performance hosted in Mumbai, India (TTFB 67ms), the overall health score of 44/100 reflects severe technical and conversion barriers: robots.txt redirects to the homepage, 90% of pages lack an H1 heading, zero analytics tags are installed, and no enquiry forms exist on the primary service page.")

    score_table = doc.add_table(rows=1, cols=4)
    score_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_cols = ["Audit Category", "Weight", "Score", "Primary Finding"]
    for i, col in enumerate(s_cols):
        score_table.rows[0].cells[i].text = col
        score_table.rows[0].cells[i].paragraphs[0].runs[0].bold = True
        score_table.rows[0].cells[i].paragraphs[0].runs[0].font.size = Pt(9.5)

    s_rows = [
        ("Crawlability & Robots Hygiene", "10", "5 / 10 (Fail)", "robots.txt redirects (301) to homepage; dummy #! links create crawl loops"),
        ("Indexability & Architecture", "10", "7 / 10 (Warning)", "Core 10 pages indexable; 10 duplicate #! URLs canonicalised"),
        ("On-Page SEO & Metadata", "10", "3 / 10 (Critical)", "Missing H1 on 90% of site; auto-scraped 420+ char meta descriptions"),
        ("Content Quality & E-E-A-T", "10", "4 / 10 (Warning)", "Founders' Columbia Asia/Manipal credentials omitted on course page; 0 blogs"),
        ("Performance & Core Web Vitals", "10", "6 / 10 (Warning)", "Server fast (Mumbai TTFB 67ms), but malformed script downloads full HTML as JS"),
        ("Mobile & Rendering Parity", "10", "7 / 10 (Pass)", "Responsive viewport; but contact form depends 100% on client-side JS rendering"),
        ("Structured Data (Schema)", "10", "3 / 10 (Critical)", "Only generic AIOSEO WebPage; 0 Course, 0 LocalBusiness, 0 FAQ schemas"),
        ("Local SEO & Geo-Signals", "10", "3 / 10 (Warning)", "Residential address listed; unverified GBP embed; missing Indian citations"),
        ("UX & Conversion", "10", "2 / 10 (Critical)", "Zero enquiry forms on /healthcare-training/; free Gmail used; dead hero CTA"),
        ("Security & Compliance", "10", "4 / 10 (Critical)", "Missing X-Frame-Options/CSP; 404 Privacy Policy violates India DPDP Act 2023"),
        ("OVERALL HEALTH SCORE", "100", "44 / 100", "Immediate 30-Day Intervention Recommended")
    ]

    for row in s_rows:
        rc = score_table.add_row().cells
        for idx, val in enumerate(row):
            rc[idx].text = val
            rc[idx].paragraphs[0].runs[0].font.name = "Arial"
            rc[idx].paragraphs[0].runs[0].font.size = Pt(9)
            if "OVERALL" in row[0]:
                rc[idx].paragraphs[0].runs[0].bold = True

    add_h1("3. Primary Service Page Deep-Dive: /healthcare-training/")
    add_para("The primary service page targets radiographers, sonographers, and medical imaging technologists in India. Currently, the page contains 571 words of high-level overview copy without pricing, duration, batch dates, eligibility criteria, or downloadable curriculum.")
    add_para("Missing H1 Heading: The page contains 0 <h1> tags. Recommended: <h1>Comprehensive Healthcare & Medical Imaging Training Programs</h1>.", "Critical Flaw: ")
    add_para("0 Lead Capture Forms: Prospective candidates cannot submit an admission enquiry on the page, creating massive drop-off.", "Critical Flaw: ")
    add_para("Unleveraged Founder Authority: Mr. Anto Ramesh Delvi and Mr. Vijaya Kumar C bring 49+ years of hospital experience from Columbia Asia and Manipal, but their profiles are omitted from the training page.", "E-E-A-T Flaw: ")
    add_para("Modality Scope to Expand: Cross-Sectional Imaging, CT & MRI Modular Training, Ultrasound (Sonographer) Clinical Training, Bi-Annual 3D Post-Processing, Radiology Administration, and Quality Assurance.", "Modality Scope: ")

    add_h1("4. Phased 30-60-90 Day Execution Roadmap")
    add_para("Days 1–30 (Foundation): Deploy valid robots.txt; install GTM & GA4; fix hero CTA button 'Our Services'; make top bar email and phone clickable; embed admission lead form on /healthcare-training/; publish DPDP-compliant Privacy Policy; deploy security headers.")
    add_para("Days 31–60 (Authority): Build 6 dedicated child modality landing pages (CT/MRI, Ultrasound, Post-Processing); inject Columbia Asia faculty credentials; deploy Schema.org Course and LocalBusiness markup; execute internal linking plan.")
    add_para("Days 61–90 (Scale): Claim and optimize Google Business Profile; build 25+ local citations across Indian directories (Justdial, Sulekha, IndiaMART); initiate thought leadership PR; review CRO funnels.")

    doc.save(file_path)
    print(f"Generated DOCX: {file_path}")

create_client_docx(r"website audit\victoryhcspl.com\Client_SEO_Audit_Report.docx")
create_client_docx(r"website audit\victoryhcspl.com\SEO_Audit_Report.docx")
create_client_docx(r"Client_SEO_Audit_Report.docx")
create_client_docx(r"SEO_Audit_Report.docx")

print("All client reports (DOCX and HTML) generated successfully!")
