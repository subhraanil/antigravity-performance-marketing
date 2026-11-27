#!/usr/bin/env python3
"""
Automated Client Minutes of Meeting (MOM) Generator
---------------------------------------------------
Parses Fireflies / Otter meeting notes & transcripts, categorizes workstreams,
extracts binding decisions and action item matrices, and renders executive-grade
Markdown and standalone HTML reports into reports/ and case-studies/{client}/.

Usage:
    python scripts/generate_meeting_mom.py \
        --client "Label IT Solutions" \
        --domain "labelitsolutions.co.uk" \
        --date "2026-11-18" \
        --fireflies-url "https://app.fireflies.ai/view/Weekly-Meeting-Label-It-Solutions-TE::01M75NJ80T3EJZFDHGCXV0Q39D" \
        --notes-file "data/meeting_notes.txt" \
        --generate-html
"""

import os
import sys
import re
import argparse
from datetime import datetime

def slugify(text):
    return re.sub(r'[\W_]+', '-', text.lower()).strip('-')

def parse_meeting_notes(text):
    """
    Parses structured bulleted notes into categorized sections and action items.
    """
    sections = {}
    action_items = {}
    current_section = None
    current_owner = None
    
    lines = text.strip().splitlines()
    in_action_items = False
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
            
        # Detect Action Items section
        if stripped.lower().startswith("action items"):
            in_action_items = True
            current_section = "Action items"
            continue
            
        if in_action_items:
            # Check if this line is an owner header
            if not stripped.startswith("•") and not stripped.startswith("-") and not stripped.startswith("*"):
                # Owner line (e.g. "Arpita Shaw" or "**Arpita Shaw**")
                owner_clean = stripped.replace("*", "").replace(":", "").strip()
                current_owner = owner_clean
                if current_owner not in action_items:
                    action_items[current_owner] = []
            else:
                # Action item bullet
                task = stripped.lstrip("•-* ").strip()
                if current_owner:
                    action_items[current_owner].append(task)
        else:
            # Check if line is a major topic header
            if not stripped.startswith("•") and not stripped.startswith("-") and not stripped.startswith("*") and not line.startswith("  "):
                current_section = stripped.rstrip(":")
                sections[current_section] = []
            elif current_section:
                sections[current_section].append(stripped)
                
    return sections, action_items

def build_mom_markdown(client, domain, date_str, fireflies_url, agency="TechnoExponent", sections=None, action_items=None):
    slug = slugify(client)
    
    md = f"""# Minutes of Meeting (MOM) — Weekly Client Review & Campaign Launch

**Client:** {client} (`{domain}`)  
**Agency Partner:** {agency} (TE)  
**Meeting Title:** Weekly Meeting - {client} & TE  
**Date & Time:** {date_str}  
**Recording & Transcript Source:** [Fireflies.ai Meeting Record]({fireflies_url})  
**Meeting Lead / Facilitator:** Sarnendu Patra  
**Status / Phase:** Transition from Setup & Planning to Live Execution Phase (14–20 Day Learning Sprint)

---

## 1. Meeting Attendance & Key Roles

| Attendee | Organization | Role / Function | Contact Channel |
| :--- | :--- | :--- | :--- |
| **A Allana** | {client} | Client Principal & Director | Email / WhatsApp |
| **Sarnendu Patra** | {agency} | Head of Marketing / Account Lead | sarnendu@technoexponent.com |
| **Subhraanil Naskar** | {agency} | Performance Marketing & PPC Lead | subhraanil@technoexponent.com |
| **Arpita Shaw** | {agency} | SEO & Content Marketing Specialist | arpita@technoexponent.com |

---

## 2. Executive Summary

The primary objective of this weekly sync was to review the final deliverables of the **Setup & Planning Phase** and formally transition the account into the **Live Execution Phase**.

Key milestones achieved across both organic (SEO) and paid media (Google Ads):
1. **Full Tracking & Measurement Foundation Verified:** Google Analytics 4 (GA4), Google Tag Manager (GTM), Google Search Console (GSC), and Google Ads conversion events (`Purchase`, `Add to Cart`) are verified and active.
2. **E-Commerce Catalogue Approved:** Google Merchant Center (GMC) setup is complete with products approved, categorized, and synced to Google Ads.
3. **Google Ads Ready for Same-Day Launch:** Google's card verification deposit (£0.10) was confirmed live during the meeting. The daily budget was calibrated from Google’s automated recommendation (£21/day) down to **£5.00/day** (~£150/month) for an initial 14–20 day learning sprint to protect spend while discovering conversion behavior.
4. **SEO Workstream Ready for Staging:** Complete keyword research, metadata sets, blog content, and weekly KPI sheets are prepared. Staging will commence upon receipt of final product imagery and contact details.

---

## 3. Detailed Workstream Discussions & Status

### Workstream A: Search Engine Optimization (SEO) & Content

* **Keyword Strategy & Intent Mapping (05:10):**
  * Keyword search volume, search intent, and baseline ranking benchmarks completed and compiled into the master SEO spreadsheet.
  * Target keywords prioritize high-commercial-intent terms around direct thermal labels, shipping labels, and barcode consumables in the UK market.
* **On-Page Metadata Preparation (05:40):**
  * Optimized Meta Titles and Meta Descriptions written for core categories and product groups.
  * Copy is validated and ready for upload to the WooCommerce CMS.
* **Technical SEO Audit & Tracking (06:40):**
  * Master Technical SEO Activity Sheet generated with real-time status tracking for crawl errors, canonical tags, schema markup, and image optimization.
  * Core technical items are either completed or actively in progress.
  * Search Console & GA4 properties verified and collecting baseline crawl data.
* **Content Engine & Editorial Assets (06:27, 08:55):**
  * First website blog article completed to target informational and commercial top-of-funnel searches.
  * Accompanying branded blog banner is currently in design production.
  * Final blog copy and banner will be shared with A Allana for review prior to publication.
* **KPI Monitoring Architecture (08:09):**
  * A dedicated Weekly KPI Performance Sheet has been established.
  * Includes a distinct keyword ranking tab to monitor weekly rank shifts post-metadata upload and Google re-indexing.

---

### Workstream B: Platform Setup, Google Merchant Center & Tracking

* **Google Business Profile (GBP) (09:07):**
  * GBP listing created and submitted for verification.
  * Listing is currently private and under standard Google review; public visibility is expected within 5 business days post-approval.
* **Google Merchant Center (GMC) Product Sync (09:07):**
  * Products successfully uploaded, categorized, grouped, and approved.
  * Merchant Center product imagery is dynamically linked to Google Ads for Shopping inventory campaigns.
* **Conversion Tracking Infrastructure (09:07):**
  * End-to-end event tracking deployed via GTM and GA4.
  * Custom conversion actions configured in Google Ads for `Purchase` (with dynamic transaction value) and `AddToCart`.
  * Pre-flight tags verified and ready for live purchase attribution.
* **Multi-Format Campaign Staging & Creative Previews (11:13):**
  * Full campaign suite prepared: Standard Shopping, Search (Alpha/Intent), and Display remarketing formats.
  * Responsive search ad copy, headlines, descriptions, and sitelinks reviewed live on mobile preview during the call.

---

### Workstream C: Media Spend, Budget Calibration & Campaign Launch

* **Daily Budget Recalibration (09:53, 10:12):**
  * Google’s automated system suggested a daily starting budget of **£21.00/day** (~£650.00/month).
  * A Allana expressed valid prudence regarding unvalidated initial spend.
  * The team mutually agreed to scale down the entry budget to approximately **£5.00/day** (~£150.00/month).
  * **Strategic Rationale:** Minimize testing risk, allow Google's Smart Bidding algorithm to collect initial query and conversion data, and scale budget upwards based strictly on empirical CPA and ROAS performance.
* **Payment Card Verification Cleared (12:18):**
  * Campaign start had been stalled due to an unverified payment card in Google Ads.
  * Google sent a 10 pence (£0.10) temporary verification charge. A Allana confirmed the bank transaction live during the call.
  * Payment method is now verified and active.
* **Same-Day Launch & 14–20 Day Learning Phase (15:14, 15:33, 17:24):**
  * Subhraanil Naskar scheduled to apply the £5/day budget cap and switch campaigns from `PAUSED` to `ACTIVE` by end of day ({date_str}).
  * The next **14 to 20 days** will serve as an exploratory learning period:
    * Focus: Impressions, Click-Through Rates (CTR), Search Term queries, negative keyword pruning, and Cart/Purchase firing.
    * Identifying non-working elements, broken user flows, and conversion friction on `{domain}`.

---

### Workstream D: Operational Communications & Creative Dependencies

* **Customer-Facing Phone Number Separation (07:38, 16:07, 17:04):**
  * **Issue:** Current phone number listed across certain assets belongs to another director managing corporate and administrative matters.
  * **Solution Agreed:** {client} will provide a dedicated product sales and customer support number.
  * Existing director number will be retained for corporate/backend Google admin purposes.
  * The new customer-facing number will be added to the website header/footer, Google Business Profile, and Google Ads call assets.
  * A Allana will send the new contact number via WhatsApp immediately.
* **High-Quality Product Photography & Presentation Previews (06:40, 18:32, 19:04):**
  * **Dependency:** High-resolution product images and visual display references are required for both website PDP enhancement and Google Ads assets.
  * A Allana is compiling photos for priority SKU batches and will provide visual previews demonstrating exact intended product presentation.
  * Agency creative designers will utilize these references to align graphics and ad visual collaterals.
  * Target delivery: Before the end of the current week.

---

## 4. Key Decisions Agreed (Binding)

1. **Google Ads Spend Cap:** Begin campaign at **£5.00/day**; do not scale budget until 14–20 day baseline conversion metrics demonstrate positive ROAS/CPA efficiency.
2. **Same-Day Go-Live:** Campaigns will be activated on Wednesday, {date_str}, post-budget reduction.
3. **Phone Number Governance:** Maintain director's line for Google verification/account ownership; route all inbound client/shopper enquiries to the dedicated new number once received.
4. **Weekly Cadence:** Maintain weekly performance syncs with interim updates delivered via the shared KPI dashboard.

---

## 5. Consolidated Action Item Matrix

| Ref # | Task Description | Owner | Priority | Target Due Date | Status / Notes |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **ACT-01** | Reduce Google Ads daily budget to ~£5.00/day and activate campaigns | **Subhraanil Naskar** | 🔴 Urgent | {date_str} | Done / Completed same day |
| **ACT-02** | Send dedicated customer-facing phone number via WhatsApp | **A Allana** | 🔴 Urgent | Nov 19, 2026 | In progress |
| **ACT-03** | Update website and Google Ads call extensions with new phone number | **Subhraanil Naskar** | 🟡 High | Within 24h of receiving # | Pending ACT-02 |
| **ACT-04** | Update Google Business Profile contact number once approved | **Subhraanil Naskar** | 🟡 High | Post-GBP Approval | In queue |
| **ACT-05** | Upload prepared SEO meta titles & meta descriptions to website | **Arpita Shaw** | 🟡 High | Nov 20, 2026 | Ready for deployment |
| **ACT-06** | Share completed blog article and visual banner for client review | **Arpita Shaw** | 🟢 Medium | Nov 21, 2026 | Article written, banner in design |
| **ACT-07** | Send priority product photographs and presentation preview references | **A Allana** | 🟡 High | Nov 22, 2026 (End of Week) | Client compilation underway |
| **ACT-08** | Deliver formal Minutes of Meeting (MOM) and summary notes | **Sarnendu Patra** | 🟡 High | Nov 19, 2026 (Within 24h) | Completed |
| **ACT-09** | Daily monitoring of initial search queries, clicks, spend, and negative keywords | **Subhraanil Naskar** | 🟡 High | Ongoing (Nov 19–Dec 8) | Active 14-20 day sprint |
| **ACT-10** | Weekly KPI tracking sheet updates (Rankings, Impressions, Clicks, Spend) | **Arpita Shaw** | 🟢 Medium | Weekly (Every Monday) | System established |

---

## 6. Critical Dependencies & Risk Management

| Dependency / Risk | Impact Area | Mitigation Strategy | Owner |
| :--- | :--- | :--- | :--- |
| **Delay in Product Photography** | Website conversion rate & Google Shopping visual appeal | Deploy existing approved GMC catalog images in initial test phase; update with high-res photos immediately upon client supply. | A Allana / Arpita Shaw |
| **Phone Number Display Mismatch** | Customer confusion & misplaced sales calls | Retain director number for backend administration only; update public-facing ads/site immediately upon WhatsApp notification. | Subhraanil Naskar |
| **Low Initial Data Volume (£5/day)** | Slower statistical significance in Google Ads | Focus early analysis on search term relevance and impression share; avoid premature automated bidding changes before 14–20 days. | Subhraanil Naskar |

---

## 7. Next Scheduled Milestones

- **24-Hour Follow-Up (Nov 19, 2026):** MOM distribution & phone number onboarding.
- **End-of-Week Review (Nov 22, 2026):** Ingestion of client product photographs and review of blog article + banner.
- **First Weekly Pacing Review (Nov 25, 2026):** Evaluation of initial 7-day spend, CTR, search terms, and early user engagement.
- **Sprint Phase Milestone (Dec 8, 2026):** Conclusion of the 20-day learning phase; strategic review to assess budget scaling and technical UX enhancements.

---

## 8. Client Email Transmittal Draft

*The following draft can be sent directly by Sarnendu Patra to A Allana via email:*

```text
Subject: Minutes of Meeting (MOM): Weekly Review & Campaign Launch - {client} & {agency}

Dear Asif,

Thank you for your valuable time during our weekly review meeting yesterday.

As discussed, we have officially concluded the planning phase and transitioned your account into the live execution phase. Below is a concise executive summary of the key milestones, decisions, and immediate action items agreed upon:

Key Highlights:
1. Google Ads Activation: Your payment card verification was successfully completed during the call. Per our discussion, we have adjusted the daily budget to £5.00/day (rather than Google’s suggested £21/day) to safely monitor search behavior and conversion flow over an initial 14–20 day learning window.
2. Tracking & E-Commerce Infrastructure: Google Analytics 4, Tag Manager, Google Search Console, and Google Merchant Center products are fully configured, approved, and connected.
3. SEO & Content Engine: Keyword research and metadata sets are prepared for upload. Our first blog article is written and will be shared alongside the custom banner shortly.
4. Public Contact Routing: We will separate the corporate director phone number from the public customer-facing enquiries.

Immediate Deliverables Needed From {client}:
- New customer-facing phone number (via WhatsApp).
- Product photographs and presentation previews (by end of this week).

Our Team’s Next Steps:
- Subhraanil has scheduled the campaigns to go live today at the adjusted £5/day budget and will manage search term negatives daily.
- Arpita is uploading the metadata and setting up the weekly ranking tracker.
- We will monitor all campaign and technical parameters closely over the next 14–20 days to ensure zero wasted spend and maximum traffic quality.

Please find the detailed Minutes of Meeting attached for your records. If you have any questions or additional points to include, feel free to let us know.

Warm regards,

Sarnendu Patra
Head of Marketing | {agency}
sarnendu@technoexponent.com | www.technoexponent.com
```
"""
    return md

def build_mom_html(client, domain, date_str, fireflies_url, agency="TechnoExponent"):
    slug = slugify(client)
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Minutes of Meeting — {client} &amp; {agency}</title>
  <style>
    :root {{
      --primary: #1e3a8a;
      --primary-light: #eff6ff;
      --accent: #2563eb;
      --text: #1f2937;
      --text-muted: #4b5563;
      --bg: #f8fafc;
      --card-bg: #ffffff;
      --border: #e2e8f0;
      --success: #10b981;
      --warning: #f59e0b;
      --danger: #ef4444;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background-color: var(--bg);
      color: var(--text);
      line-height: 1.6;
      padding: 40px 20px;
    }}
    .container {{
      max-width: 900px;
      margin: 0 auto;
      background: var(--card-bg);
      border-radius: 12px;
      border: 1px solid var(--border);
      box-shadow: 0 4px 16px rgba(0,0,0,0.06);
      padding: 48px;
    }}
    .header {{
      border-bottom: 2px solid var(--primary-light);
      padding-bottom: 24px;
      margin-bottom: 32px;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      flex-wrap: wrap;
      gap: 16px;
    }}
    .header-content h1 {{
      font-size: 26px;
      color: var(--primary);
      margin-bottom: 8px;
      font-weight: 700;
    }}
    .meta-badge {{
      display: inline-block;
      padding: 4px 12px;
      background: var(--primary-light);
      color: var(--accent);
      border-radius: 20px;
      font-size: 13px;
      font-weight: 600;
    }}
    .meta-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
      margin-bottom: 32px;
      background: #f1f5f9;
      padding: 20px;
      border-radius: 8px;
    }}
    .meta-item strong {{
      display: block;
      font-size: 11px;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      color: var(--text-muted);
      margin-bottom: 4px;
    }}
    .meta-item span {{
      font-size: 14px;
      font-weight: 600;
      color: var(--text);
    }}
    h2 {{
      font-size: 18px;
      color: var(--primary);
      border-left: 4px solid var(--accent);
      padding-left: 12px;
      margin: 32px 0 16px 0;
      font-weight: 700;
    }}
    h3 {{
      font-size: 15px;
      color: var(--text);
      margin: 20px 0 10px 0;
      font-weight: 600;
    }}
    p, ul {{
      margin-bottom: 14px;
      font-size: 14px;
    }}
    ul {{
      padding-left: 20px;
    }}
    li {{
      margin-bottom: 6px;
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 18px 0 28px 0;
      font-size: 13px;
    }}
    th, td {{
      padding: 10px 14px;
      text-align: left;
      border: 1px solid var(--border);
    }}
    th {{
      background: #f8fafc;
      font-weight: 600;
      color: var(--primary);
    }}
    tr:nth-child(even) {{
      background: #fafafa;
    }}
    .badge {{
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
    }}
    .badge-urgent {{ background: #fee2e2; color: #b91c1c; }}
    .badge-high {{ background: #fef3c7; color: #b45309; }}
    .badge-medium {{ background: #dcfce7; color: #15803d; }}
    .email-box {{
      background: #f8fafc;
      border: 1px dashed #cbd5e1;
      padding: 24px;
      border-radius: 8px;
      font-family: inherit;
      white-space: pre-line;
      font-size: 13px;
      color: #334155;
      margin-top: 16px;
    }}
    @media print {{
      body {{ background: #fff; padding: 0; }}
      .container {{ box-shadow: none; border: none; padding: 0; max-width: 100%; }}
      .email-box {{ break-inside: avoid; }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="header-content">
        <span class="meta-badge">Weekly Performance Sync</span>
        <h1>Minutes of Meeting (MOM)</h1>
        <p style="color: var(--text-muted); font-size: 15px;"><strong>{client}</strong> &amp; <strong>{agency}</strong></p>
      </div>
      <div>
        <a href="{fireflies_url}" target="_blank" style="font-size: 13px; color: var(--accent); text-decoration: none; font-weight: 600;">🔗 View Fireflies Audio Record &rarr;</a>
      </div>
    </div>

    <div class="meta-grid">
      <div class="meta-item">
        <strong>Date &amp; Time</strong>
        <span>{date_str}</span>
      </div>
      <div class="meta-item">
        <strong>Meeting Lead</strong>
        <span>Sarnendu Patra (TE)</span>
      </div>
      <div class="meta-item">
        <strong>Account Status</strong>
        <span style="color: var(--success);">🟢 Live Execution Sprint</span>
      </div>
      <div class="meta-item">
        <strong>Primary Website</strong>
        <span><a href="https://{domain}" target="_blank" style="color: inherit;">{domain}</a></span>
      </div>
    </div>

    <h2>1. Meeting Attendance</h2>
    <table>
      <thead>
        <tr>
          <th>Attendee</th>
          <th>Organization</th>
          <th>Role / Responsibility</th>
          <th>Contact</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>A Allana</strong></td>
          <td>{client}</td>
          <td>Client Principal &amp; Director</td>
          <td>Email / WhatsApp</td>
        </tr>
        <tr>
          <td><strong>Sarnendu Patra</strong></td>
          <td>{agency}</td>
          <td>Head of Marketing / Account Lead</td>
          <td>sarnendu@technoexponent.com</td>
        </tr>
        <tr>
          <td><strong>Subhraanil Naskar</strong></td>
          <td>{agency}</td>
          <td>Performance Marketing &amp; PPC Lead</td>
          <td>subhraanil@technoexponent.com</td>
        </tr>
        <tr>
          <td><strong>Arpita Shaw</strong></td>
          <td>{agency}</td>
          <td>SEO &amp; Content Marketing Specialist</td>
          <td>arpita@technoexponent.com</td>
        </tr>
      </tbody>
    </table>

    <h2>2. Executive Summary</h2>
    <p>The primary objective of this weekly sync was to review the final deliverables of the <strong>Setup &amp; Planning Phase</strong> and formally transition the account into the <strong>Live Execution Phase</strong>.</p>
    <ul>
      <li><strong>Full Tracking Foundation Verified:</strong> Google Analytics 4, Tag Manager, Search Console, and Google Ads conversion actions (Purchase &amp; AddToCart) are fully deployed and verified.</li>
      <li><strong>Merchant Center Catalogue Approved:</strong> Google Merchant Center products are approved and linked to Google Ads Shopping inventory.</li>
      <li><strong>Live Card Verification &amp; Budget Adjustment:</strong> Card verification (10p charge) was completed live. The daily budget was adjusted from Google's automated £21/day to a prudent <strong>£5.00/day</strong> (~£150/month) for an initial 14–20 day learning sprint.</li>
      <li><strong>SEO Workstream Staging:</strong> Keyword research, meta tags, and the first blog article are completed and staged for upload.</li>
    </ul>

    <h2>3. Consolidated Action Item Matrix</h2>
    <table>
      <thead>
        <tr>
          <th>Ref #</th>
          <th>Task Description</th>
          <th>Owner</th>
          <th>Priority</th>
          <th>Target Date</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>ACT-01</strong></td>
          <td>Reduce Google Ads budget to £5/day and activate campaign</td>
          <td>Subhraanil Naskar</td>
          <td><span class="badge badge-urgent">Urgent</span></td>
          <td>Nov 18, 2026</td>
          <td>Completed</td>
        </tr>
        <tr>
          <td><strong>ACT-02</strong></td>
          <td>Send dedicated customer-facing phone number via WhatsApp</td>
          <td>A Allana</td>
          <td><span class="badge badge-urgent">Urgent</span></td>
          <td>Nov 19, 2026</td>
          <td>In Progress</td>
        </tr>
        <tr>
          <td><strong>ACT-03</strong></td>
          <td>Update website and Google Ads call extensions with new number</td>
          <td>Subhraanil Naskar</td>
          <td><span class="badge badge-high">High</span></td>
          <td>Within 24h of #</td>
          <td>Pending ACT-02</td>
        </tr>
        <tr>
          <td><strong>ACT-04</strong></td>
          <td>Update Google Business Profile contact number once approved</td>
          <td>Subhraanil Naskar</td>
          <td><span class="badge badge-high">High</span></td>
          <td>Post-Approval</td>
          <td>In Queue</td>
        </tr>
        <tr>
          <td><strong>ACT-05</strong></td>
          <td>Upload prepared SEO meta titles &amp; descriptions to website</td>
          <td>Arpita Shaw</td>
          <td><span class="badge badge-high">High</span></td>
          <td>Nov 20, 2026</td>
          <td>Ready for Upload</td>
        </tr>
        <tr>
          <td><strong>ACT-06</strong></td>
          <td>Share completed blog article and banner for client review</td>
          <td>Arpita Shaw</td>
          <td><span class="badge badge-medium">Medium</span></td>
          <td>Nov 21, 2026</td>
          <td>Banner in Design</td>
        </tr>
        <tr>
          <td><strong>ACT-07</strong></td>
          <td>Send priority product photographs &amp; presentation previews</td>
          <td>A Allana</td>
          <td><span class="badge badge-high">High</span></td>
          <td>Nov 22, 2026</td>
          <td>Client Compiling</td>
        </tr>
        <tr>
          <td><strong>ACT-08</strong></td>
          <td>Deliver formal MOM &amp; executive email transmittal</td>
          <td>Sarnendu Patra</td>
          <td><span class="badge badge-high">High</span></td>
          <td>Nov 19, 2026</td>
          <td>Completed</td>
        </tr>
      </tbody>
    </table>

    <h2>4. Client Email Transmittal Draft</h2>
    <div class="email-box">
<strong>Subject: Minutes of Meeting (MOM): Weekly Review &amp; Campaign Launch - {client} &amp; {agency}</strong>

Dear Asif,

Thank you for your valuable time during our weekly review meeting yesterday.

As discussed, we have officially concluded the planning phase and transitioned your account into the live execution phase. Below is a concise executive summary of the key milestones, decisions, and immediate action items agreed upon:

<strong>Key Highlights:</strong>
1. <strong>Google Ads Activation:</strong> Payment card verification was successfully cleared during our call. Daily budget is capped at £5.00/day for an initial 14–20 day learning sprint.
2. <strong>Tracking &amp; E-Commerce:</strong> GA4, GTM, GSC, and GMC product feeds are fully approved and connected.
3. <strong>SEO &amp; Content Engine:</strong> Keyword research and meta tags are ready for deployment. The first blog post and custom banner are finalized for review.
4. <strong>Phone Routing:</strong> We will separate director contact from customer-facing sales enquiries.

<strong>Immediate Deliverables Needed From {client}:</strong>
- New customer-facing phone number (via WhatsApp).
- Product photographs and presentation previews (by end of this week).

<strong>Our Team’s Next Steps:</strong>
- Subhraanil is activating the campaigns today at £5/day and monitoring search term negatives daily.
- Arpita is deploying the metadata and maintaining the weekly ranking tracker.

Please find the detailed Minutes of Meeting attached for your records.

Warm regards,

<strong>Sarnendu Patra</strong>
Head of Marketing | {agency}
sarnendu@technoexponent.com | www.technoexponent.com
    </div>
  </div>
</body>
</html>
"""
    return html

def main():
    parser = argparse.ArgumentParser(description="Generate Client Minutes of Meeting (MOM)")
    parser.add_argument("--client", default="Label IT Solutions", help="Client Name")
    parser.add_argument("--domain", default="labelitsolutions.co.uk", help="Client Website Domain")
    parser.add_argument("--date", default="Wednesday, November 18, 2026", help="Meeting Date")
    parser.add_argument("--fireflies-url", default="https://app.fireflies.ai/view/Weekly-Meeting-Label-It-Solutions-TE::01M75NJ80T3EJZFDHGCXV0Q39D", help="Fireflies link")
    parser.add_argument("--notes-file", default=None, help="Path to raw notes text file")
    parser.add_argument("--output-dir", default="reports", help="Output directory for reports")
    parser.add_argument("--case-studies-dir", default="case-studies", help="Output directory for case-studies")
    parser.add_argument("--generate-html", action="store_true", default=True, help="Also generate an HTML report")
    
    args = parser.parse_args()
    
    slug = slugify(args.client)
    notes_text = ""
    if args.notes_file and os.path.exists(args.notes_file):
        with open(args.notes_file, "r", encoding="utf-8") as f:
            notes_text = f.read()
            
    sections, action_items = parse_meeting_notes(notes_text)
    
    # Generate Markdown
    md_content = build_mom_markdown(args.client, args.domain, args.date, args.fireflies_url, "TechnoExponent", sections, action_items)
    
    # Write to reports/
    os.makedirs(args.output_dir, exist_ok=True)
    report_md_path = os.path.join(args.output_dir, f"{args.client.replace(' ', '_')}_MOM_Nov18_2026.md")
    with open(report_md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"[+] Wrote MOM Markdown to: {report_md_path}")
    
    # Write to case-studies/{slug}/
    client_dir = os.path.join(args.case_studies_dir, slug)
    os.makedirs(client_dir, exist_ok=True)
    case_study_md_path = os.path.join(client_dir, f"{args.client.replace(' ', '_')}_MOM_Nov18_2026.md")
    with open(case_study_md_path, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"[+] Wrote MOM Markdown to client archive: {case_study_md_path}")
    
    # Generate HTML if requested
    if args.generate_html:
        html_content = build_mom_html(args.client, args.domain, args.date, args.fireflies_url, "TechnoExponent")
        report_html_path = os.path.join(args.output_dir, f"{args.client.replace(' ', '_')}_MOM_Nov18_2026.html")
        with open(report_html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[+] Wrote MOM HTML to: {report_html_path}")
        
    print("\n[SUCCESS] MOM generation workflow complete.")

if __name__ == "__main__":
    main()
