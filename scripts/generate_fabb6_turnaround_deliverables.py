import os
import openpyxl
import pandas as pd
import numpy as np
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def generate_all():
    print("Generating comprehensive deliverables for FABB6 Turnaround & Competitor Failure Forensic Audit...")
    
    # 1. Generate Markdown Report
    md_content = """# FABB6 (Glanzzkart Pvt Ltd) — Forensic Audit of Competitor Failure & Turnaround Win-Back Strategy

**Client:** FABB6 (Glanzzkart Private Limited)  
**Industry:** Premium & Professional Beauty, Haircare & Personal Care E-Commerce  
**Prepared by:** Techno Exponent (CMMI Level 5 Global Digital Growth Partner)  
**Lead Auditor:** Sarnendu Patra (Head of Marketing) & Growth Architecture Team  
**Date of Forensic Audit:** 18th November 2026  
**Audit Scope:** Account Performance, Campaign Architecture, Tracking Integrity & Merchant Diagnostics (1st September – 18th November 2026)  

---

## Executive Summary: What Happened & Why FABB6 Returned

In late August 2026, Techno Exponent delivered a complete 9-month audit (December 2025 – August 2026), strategic roadmap, and 3 calibrated financial models (**Plan A: Balanced Growth**, **Plan B: Accelerated Sprint**, and **Plan C: Step-Up Efficiency / Agency Commitment**). We explicitly alerted FABB6 leadership to critical structural vulnerabilities: Google Merchant Center catalog errors burning ₹1.04 Lakhs, misconfigured Meta conversion tracking, unchecked broad-match keyword bleed, and over-reliance on cold traffic while ignoring the 27.7% repeat-customer asset.

Despite these warnings, FABB6 initially engaged a competing agency (**SilverXis**) in September 2026. 

Over the subsequent 78 days (1st September to 18th November 2026), the competitor agency oversaw a **catastrophic operational failure**:
1. **Total Store Collapse in September:** Shopify orders crashed by **71.9%** (from 11,069 in August to **3,112 in September**), and Gross Sales plummeted from ₹95.64 Lakhs to **₹36.02 Lakhs**.
2. **The September 18 Tracking Blackout:** On 18th September 2026, the competitor literally deleted the primary purchase conversion action (`Purchase-2026 removed`) from Google Ads. This blinded Google's Smart Bidding algorithm, causing Google Ads orders to collapse to **only 42 orders** at an astronomical CPA of **₹7,568.93** and a ROAS of **0.15x** (spending ₹3.18 Lakhs to generate ₹46,329 in sales).
3. **The October Festive (Diwali) Fiasco:** During India's largest annual shopping festival, SilverXis pumped ₹42.47 Lakhs into paid media, but delivered only 7,298 paid purchases at a bloated blended CPA of **₹581.84**. Meta Ads CPA reached an all-time record high of **₹532.42** (ROAS 2.47x), performing substantially worse than the client's unoptimized July baseline (8,313 paid purchases at ₹524.75 CPA).
4. **The "Glam+" Copy-Paste Disaster:** In multiple Google Ads Performance Max campaigns, the competitor literally copy-pasted headlines and copy from another beauty client named **"Glam+"** / **"Glam Plus"**! FABB6 paid Google Ads to show ads stating *"Beauty & Skincare Must-Haves, Glam+ Store"* and *"Glow Up with Glam+ | Flas Sale is Live"*!
5. **Over ₹7.46 Lakhs in Pure Budget Waste:** Money was incinerated on zero-conversion traffic ads (`IG-Traffic`: ₹50,214 for 0 purchases), high-frequency app installs (frequency 13.18, CPA > ₹1,080), 110 products with 404 broken landing pages (over ₹80,000 burned), and broad match non-beauty keywords (`badminton ankle support`, `gym equipment for girls at home`).

FABB6 leadership has rightly recognized that the account is bleeding capital, and on 16th November 2026, issued the invitation to restore Techno Exponent's management. This document provides the mathematical autopsy of the competitor's failure and outlines our **Immediate 14-Day Emergency Triage** and **90-Day Account Turnaround Plan**.

---

## 1. Master Performance Comparison: Pre-Competitor vs. Competitor Tenure

The following table provides the authentic, reconciled performance data across Shopify, Google Ads, and Meta Ads from December 2025 through 18th November 2026.

### Full Account Performance Matrix (Dec 2025 – Nov 2026)

| Month | Shopify Orders | Gross Sales (INR) | Net Revenue (INR) | Total Paid Spend (INR) | Paid Purchases | Blended Paid CPA (INR) | Blended ROAS (Shopify Net / Spend) | Repeat Customer Rate |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Dec 2025** | 3,307 | ₹26,37,583 | ₹20,71,721 | ₹4,20,868 | 1,614 | ₹260.69 | 4.92x | 13.9% |
| **Jan 2026** | 7,850 | ₹55,52,015 | ₹46,39,791 | ₹12,16,540 | 4,260 | ₹285.55 | 3.81x | 17.2% |
| **Feb 2026** | 8,250 | ₹64,10,361 | ₹62,38,149 | ₹17,97,005 | 4,817 | ₹373.06 | 3.47x | 18.0% |
| **Mar 2026** | 11,285 | ₹85,32,040 | ₹59,57,228 | ₹27,84,074 | 6,351 | ₹438.38 | 2.14x | 18.8% |
| **Apr 2026** | 10,551 | ₹84,73,141 | ₹74,36,807 | ₹32,55,208 | 5,350 | ₹608.41 | 2.28x | 22.2% |
| **May 2026** | 12,215 | ₹1,00,96,287 | ₹91,33,293 | ₹40,21,304 | 7,076 | ₹568.29 | 2.27x | 25.2% |
| **Jun 2026** | 12,877 | ₹1,03,89,397 | ₹83,97,880 | ₹42,86,498 | 6,851 | ₹625.67 | 1.96x | 24.3% |
| **Jul 2026** | 13,420 | ₹1,03,64,270 | ₹78,45,258 | ₹43,62,222 | 8,313 | ₹524.75 | 1.80x | 27.6% |
| **Aug 2026** | 11,069 | ₹95,64,391 | ₹74,76,300 | ₹82,75,293 | 10,189 | ₹812.16 | 0.90x | 27.7% |
| **Sep 2026 (Competitor)** | **3,112** | **₹36,01,597** | **₹28,49,666** | **₹6,27,053** | **801** | **₹782.84** | **4.54x\*** | **51.8%** |
| **Oct 2026 (Competitor)** | **9,143** | **₹1,05,66,667** | **₹90,99,142** | **₹42,46,579** | **7,298** | **₹581.84** | **2.14x** | **35.2%** |
| **Nov 2026 (Till 18th)** | **4,638** | **₹53,17,824** | **₹42,00,383** | **₹19,09,346** | **4,310** | **₹443.00** | **2.20x** | **36.7%** |

*\*Note on September ROAS: In September, the artificial 4.54x ROAS on Shopify net sales was caused entirely by existing customer re-orders (51.8% returning customer rate). Paid ad spend was slashed by 92%, paid orders collapsed to just 801, and the store survived almost exclusively on FABB6's past customer equity.*

---

## 2. Platform-by-Platform Autopsy: Where the Money Vanished

### A. Google Ads: Blinded Algorithms, Deleted Tracking & The "Glam+" Copy-Paste Disaster

| Metric | August 2026 Baseline | September 2026 (Competitor) | October 2026 (Competitor Festive) | November 2026 (Till 18th) | Competitor Total (Sep-Nov) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Google Spend** | ₹67,06,703 | ₹3,17,895 | ₹22,02,106 | ₹9,64,182 | **₹34,84,182** |
| **Google Orders** | 5,934.18 | **42.0** | 3,458.49 | 2,319.99 | **5,820.48** |
| **Google CPA** | ₹1,130.18 | **₹7,568.93** | ₹636.72 | ₹415.60 | **₹598.61** |
| **Google ROAS** | 1.09x | **0.15x** | 1.93x | 2.97x | **2.06x** |

#### The 4 Critical Blunders in Google Ads:

1. **The Sep 18 Conversion Deletion (The ₹7,569 CPA Month):**
   - In the account change history on September 18 at 3:32 PM, competitor user `sarjit@silverxis.com` executed: `Conversion "Purchase-2026" removed`.
   - By removing the primary conversion action, Google's Smart Bidding models had zero conversion feedback. In September, the account spent ₹3,17,895 to get **only 42 orders**, resulting in a catastrophic **₹7,568.93 CPA** and **0.15x ROAS**.
2. **The "Glam+" Copy-Paste Blunder (Catastrophic Negligence):**
   - In campaigns `T4 Pro/Salon (>₹1,300)`, `T3 Premium (₹900–1,300)`, `YS24 - PMax | Brand Campaign -- Top 10 products`, and `Pilgrim`, the competitor literally copy-pasted headlines and copy from another client named **"Glam+"**:
     * *Headline:* "Beauty & Skincare Must-Haves, Glam+ Store, Save Big on Top Beauty Brands"
     * *Long Headline:* "Glow Up with Glam+ | Save 5% on Premium Beauty & Personal Care Products | Shop Now, Skincare, Haircare, Makeup & More | Flas Sale is Live - 5% Off on All products" *(with typo "Flas Sale")*
     * *Description:* "Skincare & makeup at Glam+: 5% off, Buy 1 Get 1 on sunscreen & free gift on ₹2000+, Glam+ offers 5% off all products..."
     * *Audience Signals:* "Glam Plus - Custom -CWV - Female Only", "Glam Plus - Pure RT Audience".
   - FABB6 was literally paying Google Ads to advertise an entirely different brand!
3. **Hyperactive Budget Toggling (The "Learning" Trap):**
   - The competitor made **140 budget changes** (74 increases, 66 decreases) in under 60 days, constantly modifying daily budgets by small amounts every few days. This permanently locked Smart Bidding in "Learning Phase," preventing the algorithm from ever stabilizing.
4. **Ignoring Merchant Center 404 Errors:**
   - In `Product report (7).xlsx`, 216 products remain "Not eligible," 110 products show "Product page unavailable" (404 errors), and 70 show promotional image overlay violations. 
   - Over **₹80,285.73** was burned on zero-conversion products. For instance, `Foxtale 5% Niacinamide Face Serum-30ml` spent ₹1,614.38 across 480 clicks directly to a 404 broken page!

---

### B. Meta Ads: Overlapping ASCs, Retargeting Inversion & Traffic Waste

| Metric | August 2026 Baseline | September 2026 (Competitor) | October 2026 (Competitor Festive) | November 2026 (Till 18th) | Competitor Total (Sep-Nov) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Meta Spend** | ₹15,68,590 | ₹3,09,158 | ₹20,44,474 | ₹9,45,164 | **₹32,98,796** |
| **Meta Orders** | 4,255 | 759 | 3,840 | 1,990 | **6,589** |
| **Meta CPA** | ₹368.65 | ₹407.32 | **₹532.42** | ₹474.96 | **₹500.65** |
| **Meta ROAS** | 2.75x | 3.31x | **2.47x** | 2.62x | **2.59x** |

#### The 4 Critical Blunders in Meta Ads:

1. **Festive Month (October) Failure:**
   - October was the peak Diwali shopping window in India. Instead of harvesting high intent at lower CPAs, Meta CPA spiked to **₹532.42 per order** (a 44% increase over August baseline) and ROAS crashed to **2.47x**. 
   - Despite spending ₹20.44 Lakhs, they generated only 3,840 purchases (compared to 6,013 purchases on ₹18.85L in July).
2. **Retargeting Cost Inversion (DPA Failure):**
   - Dynamic Product Ads (`Retargeting — DPA - Fabb6`) spent ₹9,43,971 for 1,833 purchases at a CPA of **₹514.99** (peaking at **₹570.31** in October).
   - In healthy e-commerce accounts, retargeting CPA is 40%–60% lower than cold prospecting (target: ₹160–₹220). Here, retargeting was **MORE EXPENSIVE than prospecting** due to lack of audience exclusions and frequency burn.
3. **Internal Advantage+ Shopping Campaign (ASC) Cannibalization:**
   - The competitor ran multiple Advantage+ Shopping Campaigns simultaneously (`Advantage+ Sales Campaign - Fabb6`, `Advantage+ Sales – Best Seller`, `Advantage+ Sales Combo Products`) targeting the same broad demographic in India without product catalog division.
   - Meta's internal auction bid against itself, inflating CPMs from ₹112 to ₹155–₹205.
4. **Direct Capital Waste on Link Clicks & Zombie Campaigns:**
   - `IG-Traffic`: Burned **₹50,214.27** across 8.31 million impressions for **0 purchases** (₹0 ROAS).
   - `New App promotion Campaign iOS`: Burned ₹19,161 on 24,422 users at an extreme frequency of **13.18** with **0 purchases**.
   - `App-BTG-03072026`: Burned ₹1,38,513 for 128 purchases at a CPA of **₹1,082.14** (ROAS 1.22x).

---

## 3. Quantifiable Budget Waste Summary

Across the 78-day competitor tenure, we have mathematically isolated **₹7,46,558.00** in directly-attributable, avoidable waste:

| Waste Category | Specific Failure Identified | Financial Waste (INR) |
| :--- | :--- | :---: |
| **Deleted Conversion Action Choke** | Google Ads September blackout (CPA ₹7,568.93 vs normal ₹550) | ₹2,94,800.00 |
| **Merchant Center 404 & Dead Products** | Ad spend driving clicks to 110 broken landing pages & dead SKUs | ₹80,285.00 |
| **Zero-Conversion Meta Traffic Ads** | `IG-Traffic` link clicks yielding zero sales | ₹50,214.00 |
| **Unoptimized App Install Ad Waste** | High-frequency iOS/Android app campaigns (CPA > ₹1,080) | ₹1,57,674.00 |
| **Broad Match Non-Beauty Keyword Bleed** | Gym equipment, push-up board, and unrelated generic keywords | ₹45,585.00 |
| **Internal ASC Auction Self-Bidding** | Inflated CPM penalties from overlapping Advantage+ campaigns | ₹1,18,000.00 |
| **Total Directly-Attributable Waste** | **Pure Capital Incinerated by Competitor Mismanagement** | **₹7,46,558.00** |

---

## 4. The Turnaround Plan: How Techno Exponent Recovers Performance

Techno Exponent's turnaround strategy executes across three strict operational phases:

### Phase 1: 14-Day Emergency Triage (Week 1–2) — "Stop the Bleeding"
1. **Immediate Copy & Brand Purge:**
   - Eradicate every single instance of "Glam+" and "Glam Plus" copy, long headlines, and audience signals from Google Ads.
   - Deploy brand-accurate, high-converting copy emphasizing FABB6's curated professional salon assortment (L'Oréal Professionnel, Inoa, Matrix, Sebamed).
2. **Restore Conversion Tracking Hardening:**
   - Re-establish Google Ads Enhanced Conversions for Web via Google Tag Manager with 100% deduplication.
   - Configure Meta Conversions API (CAPI) through the native Shopify gateway to achieve an Event Match Quality (EMQ) score > 8.5/10.
3. **Merchant Center Data Cleanup:**
   - Exclude or redirect the 110 products throwing 404 errors.
   - Re-upload clean product imagery for the 70 SKUs flagged for promotional text overlays.
4. **Kill Budget Bleeders:**
   - Pause `IG-Traffic`, unoptimized app campaigns, and zero-conversion broad match search keywords.
   - Consolidate Meta campaigns into a clean 3-tier structure:
     * **Top of Funnel (TOF):** 1 Master Advantage+ Shopping Campaign with first-party purchaser exclusions (70% budget).
     * **Middle of Funnel (MOF):** Dynamic Product Ads (DPA) retargeting 3-day / 7-day cart abandoners with frequency capped at ≤ 2.5 (20% budget).
     * **Bottom of Funnel (BOF / Retention):** VIP Re-order & loyalty campaign targeting 30-180 day past purchasers (10% budget).

### Phase 2: 30-Day Stabilization (Month 1 - December 2026) — "Restore Unit Economics"
1. **Google Ads Performance Max Catalog Restructuring:**
   - Restructure PMax into 3 margin-aligned asset tiers:
     * *Tier 1 (Core Best Sellers & Hair Color):* Inoa, Majirel, L'Oréal Hair Spa (tROAS 320%).
     * *Tier 2 (High ASP & Premium):* Salon electricals, styling kits (tROAS 280%).
     * *Tier 3 (Catch-All / Long Tail):* Remaining catalog with conservative budget caps.
2. **Meta Ads CPA Reduction:**
   - Drive Meta CPA down from ₹500+ to **≤ ₹320** within 30 days through creative diversification (before/after salon reels, routine bundles, UGC unboxing).
3. **Automated Retention Engine Activation:**
   - FABB6 has a 36.7% repeat-customer rate that is currently left entirely to chance.
   - Implement automated post-purchase replenishment flows (WhatsApp & Klaviyo/Omnisend) triggered at 30, 45, and 60 days based on product consumption cycles (e.g. hair spa mask replenishment). This drives repeat orders at an acquisition cost of under ₹60.

### Phase 3: 60–90 Day Profitable Scaling (January – February 2027) — "Achieve Growth Milestone"
1. **Scale Monthly Ad Spend Sustainably:**
   - Step budget up from ₹30 Lakhs to ₹45L–₹50L in strict compliance with the **≤ 20% budget increase every 72 hours** guardrail to prevent algorithmic shock.
2. **Drive Blended Economics:**
   - Scale total store order volume to **550–700 orders/day** (16,000–21,000 orders/month).
   - Maintain Blended Paid CPA between **₹260 – ₹285** and Blended ROAS between **3.8x – 4.3x**.

---

## 5. Revised 6-Month Recovery Forecast (December 2026 – May 2027)

| Month | Projected Spend (INR) | Projected Paid Orders | Projected Paid CPA (INR) | Projected Shopify Orders | Projected Net Revenue (INR) | Blended ROAS | Key Milestones |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Dec 2026 (Month 1)** | ₹30,00,000 | 8,800 | ₹340.91 | 12,500 | ₹1,08,00,000 | 3.60x | Account stabilized; Glam+ purged; CAPI & PMax fixed. |
| **Jan 2027 (Month 2)** | ₹35,00,000 | 11,200 | ₹312.50 | 15,400 | ₹1,38,60,000 | 3.96x | CPA drops below ₹315; Retention engine live. |
| **Feb 2027 (Month 3)** | ₹40,00,000 | 13,800 | ₹289.86 | 18,600 | ₹1,71,12,000 | 4.28x | Rebuilding to 650+ orders/day run rate. |
| **Mar 2027 (Month 4)** | ₹45,00,000 | 16,300 | ₹276.07 | 21,800 | ₹2,04,92,000 | 4.55x | 700+ orders/day milestone achieved. |
| **Apr 2027 (Month 5)** | ₹50,00,000 | 18,900 | ₹264.55 | 25,200 | ₹2,41,92,000 | 4.84x | Omnichannel compounding (SEO + Paid + Retention). |
| **May 2027 (Month 6)** | ₹55,00,000 | 21,500 | ₹255.81 | 28,500 | ₹2,79,30,000 | 5.08x | Long-term profitable scale; CPA stabilized at ~₹255. |

---

## Conclusion & Next Steps

The failure of the past 2.5 months was not caused by market headwinds or product flaws—it was the direct result of **gross technical negligence, copy-paste errors, broken tracking, and zero funnel discipline**. 

Techno Exponent has the audited forensic evidence, the root-cause diagnosis, and the execution infrastructure to reverse these losses immediately.

### Action Checklist to Resume:
1. **Confirm Handover:** Re-assign Google Ads and Meta Ads Admin access to Techno Exponent (`subhranilnaskar@technoexponent.com`).
2. **Execute Phase 1 Emergency Fixes:** Within 48 hours of access, our team will purge all foreign ad copy, pause bleeding campaigns, fix Google Merchant Center 404 errors, and configure CAPI/Enhanced Conversions.
3. **Kickoff Call:** Align on weekly milestone checkpoints and commence December stabilization.
"""

    # Write Markdown to Office case studies
    md_path_office = r"C:\Users\test\Videos\Office\case-studies\fabb6\FABB6_Competitor_Forensic_Audit_and_Turnaround_Strategy.md"
    with open(md_path_office, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Written Markdown report to: {md_path_office}")

    # Write Markdown to Artifact Directory
    md_path_artifact = r"C:\Users\test\.gemini\antigravity\brain\29f77e0a-5ed5-4d24-842c-443d9957274c\fabb6_competitor_failure_forensic_autopsy_and_turnaround_strategy.md"
    with open(md_path_artifact, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Written Markdown artifact to: {md_path_artifact}")

    # 2. Generate Professional Word Document (.docx)
    doc_path = r"C:\Users\test\Videos\Office\reports\FABB6_Competitor_Forensic_Audit_and_Turnaround_Proposal.docx"
    doc = docx.Document()
    
    # Page Margins (1 inch)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Styles
    # Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_title = p_title.add_run("FABB6 (Glanzzkart Private Limited)")
    r_title.bold = True
    r_title.font.size = Pt(24)
    r_title.font.color.rgb = RGBColor(16, 44, 87) # Deep Navy

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sub = p_sub.add_run("Forensic Audit of Competitor Agency Failure & 90-Day Turnaround Win-Back Strategy")
    r_sub.font.size = Pt(15)
    r_sub.font.color.rgb = RGBColor(80, 80, 80)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_meta = p_meta.add_run("Prepared by Techno Exponent | CMMI Level 5 Global Digital Growth Partner\nDate: 18th November 2026 | Lead Auditor: Sarnendu Patra (Head of Marketing)")
    r_meta.font.size = Pt(10)
    r_meta.font.italic = True
    r_meta.font.color.rgb = RGBColor(120, 120, 120)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Section 1: Executive Summary
    h1 = doc.add_heading("1. Executive Summary: What Happened & Why FABB6 Returned", level=1)
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(6)
    
    p = doc.add_paragraph(
        "In late August 2026, Techno Exponent conducted an exhaustive 9-month audit and presented three calibrated growth models "
        "to FABB6 leadership. We explicitly alerted management to severe pre-existing structural issues: Google Merchant Center catalog errors, "
        "unreliable Meta pixel attribution, broad-match keyword bleed, and lack of an automated retention engine. "
        "FABB6 engaged a competing agency (SilverXis) starting in September 2026. Over the subsequent 78 days (Sep 1 to Nov 18, 2026), "
        "the competitor oversaw a severe operational and financial decline across both Google Ads and Meta Ads."
    )
    p.paragraph_format.line_spacing = 1.15

    # Bullet Callouts
    bullet_points = [
        ("Total Store Collapse in September: ", "Shopify orders collapsed by 71.9% (from 11,069 in August down to 3,112), and Gross Sales fell from ₹95.64 Lakhs to ₹36.02 Lakhs."),
        ("September 18 Tracking Blackout: ", "SilverXis deleted the primary 'Purchase-2026' conversion action in Google Ads. This blinded Smart Bidding, sending September Google Ads CPA to an astronomical ₹7,568.93 and ROAS to 0.15x (generating only 42 orders on ₹3.18L spend)."),
        ("October Diwali Fiasco: ", "During India's highest-demand festive shopping season, the competitor spent ₹42.47 Lakhs on paid ads, but delivered only 7,298 paid purchases at a bloated blended CPA of ₹581.84. Meta CPA surged to ₹532.42 (ROAS 2.47x)."),
        ("The 'Glam+' Copy-Paste Blunder: ", "In multiple live Performance Max campaigns, the competitor literally copy-pasted headlines and ad copy from another client ('Glam+ Store' / 'Glam Plus'), with typos like 'Flas Sale', causing FABB6 to pay Google Ads to advertise an entirely different brand."),
        ("Over ₹7.46 Lakhs in Pure Waste: ", "Budget was burned on zero-conversion link clicks (IG-Traffic: ₹50K for 0 sales), high-frequency app installs (frequency 13.18), 110 products with 404 broken landing pages, and broad match non-beauty keywords.")
    ]
    for b_title, b_desc in bullet_points:
        bp = doc.add_paragraph(style='List Bullet')
        r1 = bp.add_run(b_title)
        r1.bold = True
        r1.font.color.rgb = RGBColor(180, 40, 40)
        r2 = bp.add_run(b_desc)
        bp.paragraph_format.space_after = Pt(4)

    # Section 2: Full Performance Table
    h2 = doc.add_heading("2. Master Performance Matrix: December 2025 – November 2026", level=1)
    h2.paragraph_format.space_before = Pt(16)
    
    # Table of 13 rows x 8 cols
    table_data = [
        ["Month", "Shopify Orders", "Gross Sales", "Paid Spend", "Paid Orders", "Blended CPA", "Net ROAS", "Repeat %"],
        ["Dec 2025", "3,307", "₹26.38 L", "₹4.21 L", "1,614", "₹260.69", "4.92x", "13.9%"],
        ["Jan 2026", "7,850", "₹55.52 L", "₹12.17 L", "4,260", "₹285.55", "3.81x", "17.2%"],
        ["Feb 2026", "8,250", "₹64.10 L", "₹17.97 L", "4,817", "₹373.06", "3.47x", "18.0%"],
        ["Mar 2026", "11,285", "₹85.32 L", "₹27.84 L", "6,351", "₹438.38", "2.14x", "18.8%"],
        ["Apr 2026", "10,551", "₹84.73 L", "₹32.55 L", "5,350", "₹608.41", "2.28x", "22.2%"],
        ["May 2026", "12,215", "₹100.96 L", "₹40.21 L", "7,076", "₹568.29", "2.27x", "25.2%"],
        ["Jun 2026", "12,877", "₹103.89 L", "₹42.86 L", "6,851", "₹625.67", "1.96x", "24.3%"],
        ["Jul 2026", "13,420", "₹103.64 L", "₹43.62 L", "8,313", "₹524.75", "1.80x", "27.6%"],
        ["Aug 2026", "11,069", "₹95.64 L", "₹82.75 L", "10,189", "₹812.16", "0.90x", "27.7%"],
        ["Sep 2026 (Comp)", "3,112", "₹36.02 L", "₹6.27 L", "801", "₹782.84", "4.54x*", "51.8%"],
        ["Oct 2026 (Comp)", "9,143", "₹105.67 L", "₹42.47 L", "7,298", "₹581.84", "2.14x", "35.2%"],
        ["Nov 2026 (Till 18th)", "4,638", "₹53.18 L", "₹19.09 L", "4,310", "₹443.00", "2.20x", "36.7%"]
    ]
    
    table = doc.add_table(rows=len(table_data), cols=len(table_data[0]))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    for r_idx, row_vals in enumerate(table_data):
        row = table.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            if r_idx == 0:
                set_cell_background(cell, "102C57")
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
            elif r_idx >= 10:
                set_cell_background(cell, "FDEED9") # Highlight competitor months
                p.runs[0].font.color.rgb = RGBColor(140, 30, 30)
                if c_idx == 0:
                    p.runs[0].font.bold = True
            else:
                if r_idx % 2 == 1:
                    set_cell_background(cell, "F9F9F9")
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

    # Section 3: Wasted Spend Table
    h3 = doc.add_heading("3. Quantifiable Budget Waste Breakdown (₹7.46 Lakhs)", level=1)
    h3.paragraph_format.space_before = Pt(16)
    
    waste_table_data = [
        ["Failure Category", "Root Cause & Forensic Finding", "Wasted Spend (INR)"],
        ["Deleted Conversion Action Choke", "Google Ads tracking deleted on Sep 18; CPA rose to ₹7,569 vs normal ₹550", "₹2,94,800.00"],
        ["Merchant Center 404 & Dead SKUs", "Ad clicks sent to 110 dead landing pages (e.g. Foxtale serum 480 clicks)", "₹80,285.00"],
        ["Zero-Conversion Meta Traffic Ads", "IG-Traffic link-click campaign burning 8.3M impressions for 0 sales", "₹50,214.00"],
        ["Unoptimized App Install Ad Waste", "iOS & Android app promo running at frequency of 13.18, CPA > ₹1,080", "₹1,57,674.00"],
        ["Broad Match Non-Beauty Bleed", "Performance Max ads showing for gym equipment, push-up board, etc.", "₹45,585.00"],
        ["Internal ASC Self-Bidding", "Multiple overlapping Advantage+ campaigns bidding against each other", "₹1,18,000.00"],
        ["TOTAL AVOIDABLE WASTE", "Direct Capital Incinerated by Competitor Agency Mismanagement", "₹7,46,558.00"]
    ]
    
    w_table = doc.add_table(rows=len(waste_table_data), cols=len(waste_table_data[0]))
    w_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row_vals in enumerate(waste_table_data):
        row = w_table.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.text = val
            p = cell.paragraphs[0]
            if c_idx == 2:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            elif c_idx == 0:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            if r_idx == 0:
                set_cell_background(cell, "8B0000") # Dark Red
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
            elif r_idx == len(waste_table_data) - 1:
                set_cell_background(cell, "FADBD8")
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(140, 20, 20)
            else:
                if r_idx % 2 == 1:
                    set_cell_background(cell, "FDFEFE")
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

    # Section 4: 90-Day Turnaround Roadmap
    h4 = doc.add_heading("4. Techno Exponent 90-Day Turnaround Roadmap", level=1)
    h4.paragraph_format.space_before = Pt(16)
    
    phases = [
        ("Phase 1: 14-Day Emergency Triage (Week 1–2)", [
            "Purge all 'Glam+' copy, long headlines, and audience signals from Google Ads; replace with brand-aligned salon beauty copy.",
            "Re-establish Google Ads Enhanced Conversions and Meta CAPI deduplication via Shopify native gateway (Target EMQ > 8.5).",
            "Cleanse Google Merchant Center: unpublish or redirect the 110 products with 404 errors, fix 70 image overlays, and add negative keyword list.",
            "Terminate IG-Traffic and dead app campaigns; consolidate Meta into 1 Master ASC (TOF) + 1 DPA Retargeting (MOF) + 1 Retention (BOF)."
        ]),
        ("Phase 2: 30-Day Stabilization (Month 1 - December 2026)", [
            "Restructure Google PMax into 3 margin-tiered asset groups (Core Best Sellers, High ASP, Catch-All) on target ROAS.",
            "Drive Meta CPA down from ₹500+ to ≤ ₹320 through creative refresh (salon Reels, UGC routine videos, bundle offers).",
            "Launch automated WhatsApp & Klaviyo re-order flows to monetize the 36.7% repeat customer base at ₹50–₹70 CPA.",
            "Deliver 12,500+ orders in December at a Blended Paid CPA of ≤ ₹340 and Blended ROAS of ≥ 3.60x."
        ]),
        ("Phase 3: 60–90 Day Profitable Scale (January – February 2027)", [
            "Re-scale ad spend to ₹40L–₹50L adhering strictly to the ≤ 20% budget increase every 72 hours scaling rule.",
            "Expand daily orders from ~216/day to 650–750 orders/day (18,000–21,000 orders/month).",
            "Achieve Blended Paid CPA of ₹260–₹285 and Blended ROAS of 4.2x–4.5x, achieving sustainable, compounding profitability."
        ])
    ]
    for ph_title, ph_tasks in phases:
        p_ph = doc.add_paragraph()
        r_ph = p_ph.add_run(ph_title)
        r_ph.bold = True
        r_ph.font.size = Pt(12)
        r_ph.font.color.rgb = RGBColor(16, 44, 87)
        for task in ph_tasks:
            pt = doc.add_paragraph(style='List Bullet')
            pt.add_run(task)
            pt.paragraph_format.space_after = Pt(3)

    # Section 5: Recovery Projections Table
    h5 = doc.add_heading("5. Six-Month Recovery Financial Model (Dec 2026 – May 2027)", level=1)
    h5.paragraph_format.space_before = Pt(16)
    
    rec_data = [
        ["Month", "Ad Spend", "Paid Orders", "Paid CPA", "Total Orders", "Net Revenue", "Blended ROAS"],
        ["Dec 2026 (M1)", "₹30.00 L", "8,800", "₹340.91", "12,500", "₹1.08 Cr", "3.60x"],
        ["Jan 2027 (M2)", "₹35.00 L", "11,200", "₹312.50", "15,400", "₹1.39 Cr", "3.96x"],
        ["Feb 2027 (M3)", "₹40.00 L", "13,800", "₹289.86", "18,600", "₹1.71 Cr", "4.28x"],
        ["Mar 2027 (M4)", "₹45.00 L", "16,300", "₹276.07", "21,800", "₹2.05 Cr", "4.55x"],
        ["Apr 2027 (M5)", "₹50.00 L", "18,900", "₹264.55", "25,200", "₹2.42 Cr", "4.84x"],
        ["May 2027 (M6)", "₹55.00 L", "21,500", "₹255.81", "28,500", "₹2.79 Cr", "5.08x"],
        ["6-Mo Total", "₹2.55 Cr", "90,500", "₹281.77", "1,22,000", "₹11.44 Cr", "4.49x"]
    ]
    r_table = doc.add_table(rows=len(rec_data), cols=len(rec_data[0]))
    r_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row_vals in enumerate(rec_data):
        row = r_table.rows[r_idx]
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            if r_idx == 0:
                set_cell_background(cell, "102C57")
                p.runs[0].font.bold = True
                p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
            elif r_idx == len(rec_data) - 1:
                set_cell_background(cell, "EAECEE")
                p.runs[0].font.bold = True
            else:
                if r_idx % 2 == 1:
                    set_cell_background(cell, "F9F9F9")
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)

    # Save Word Document
    doc.save(doc_path)
    print(f"Written Word Document to: {doc_path}")

    # 3. Generate Interactive HTML Turnaround Dashboard
    html_path = r"C:\Users\test\Videos\Office\reports\fabb6_turnaround_forensic_dashboard.html"
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FABB6 — Competitor Failure Forensic Dashboard & Turnaround Roadmap</title>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Space+Grotesk:wght@500;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-dark: #090D16;
            --card-bg: #121826;
            --card-border: #1E293B;
            --primary: #3B82F6;
            --primary-glow: rgba(59, 130, 246, 0.2);
            --danger: #EF4444;
            --danger-bg: rgba(239, 68, 68, 0.1);
            --success: #10B981;
            --success-bg: rgba(16, 185, 129, 0.1);
            --warning: #F59E0B;
            --text-main: #F8FAFC;
            --text-muted: #94A3B8;
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: var(--bg-dark);
            color: var(--text-main);
            padding: 30px 40px;
            line-height: 1.5;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--card-border);
            padding-bottom: 24px;
            margin-bottom: 30px;
        }
        .header h1 {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 26px;
            font-weight: 700;
            background: linear-gradient(135deg, #FFFFFF, #94A3B8);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .header p { color: var(--text-muted); font-size: 14px; margin-top: 4px; }
        .badge-danger {
            background: var(--danger-bg);
            color: var(--danger);
            border: 1px solid rgba(239, 68, 68, 0.3);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        .grid-kpis {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 20px;
            margin-bottom: 30px;
        }
        .kpi-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 14px;
            padding: 22px;
            position: relative;
            overflow: hidden;
        }
        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 3px;
        }
        .kpi-card.red::before { background: var(--danger); }
        .kpi-card.blue::before { background: var(--primary); }
        .kpi-card.amber::before { background: var(--warning); }
        .kpi-card.green::before { background: var(--success); }
        .kpi-label { font-size: 13px; color: var(--text-muted); font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
        .kpi-val { font-size: 28px; font-weight: 800; margin: 8px 0; font-family: 'Space Grotesk', sans-serif; }
        .kpi-sub { font-size: 12px; }
        .kpi-sub.neg { color: var(--danger); }
        .kpi-sub.pos { color: var(--success); }

        .tabs {
            display: flex;
            gap: 12px;
            margin-bottom: 25px;
            border-bottom: 1px solid var(--card-border);
            padding-bottom: 12px;
        }
        .tab-btn {
            background: transparent;
            border: 1px solid var(--card-border);
            color: var(--text-muted);
            padding: 10px 20px;
            border-radius: 10px;
            font-size: 14px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }
        .tab-btn:hover { background: #1E293B; color: #FFF; }
        .tab-btn.active {
            background: var(--primary);
            border-color: var(--primary);
            color: #FFF;
            box-shadow: 0 0 15px var(--primary-glow);
        }

        .tab-pane { display: none; }
        .tab-pane.active { display: block; }

        .charts-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }
        .chart-box {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 14px;
            padding: 24px;
        }
        .chart-box h3 { font-size: 16px; font-weight: 700; margin-bottom: 18px; color: #E2E8F0; }

        .table-box {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 14px;
            padding: 24px;
            margin-bottom: 30px;
            overflow-x: auto;
        }
        .table-box h3 { font-size: 16px; font-weight: 700; margin-bottom: 18px; }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }
        th, td {
            padding: 12px 14px;
            text-align: left;
            border-bottom: 1px solid var(--card-border);
        }
        th { background: #182234; color: #94A3B8; font-weight: 600; text-transform: uppercase; font-size: 11px; letter-spacing: 0.5px; }
        tr:hover td { background: rgba(255, 255, 255, 0.02); }
        .num { text-align: right; font-variant-numeric: tabular-nums; }
        .highlight-red { color: #F87171; font-weight: 600; }
        .highlight-green { color: #34D399; font-weight: 600; }
        .highlight-blue { color: #60A5FA; font-weight: 600; }

        .blunder-card {
            background: rgba(239, 68, 68, 0.05);
            border: 1px solid rgba(239, 68, 68, 0.2);
            border-left: 4px solid var(--danger);
            border-radius: 10px;
            padding: 18px 22px;
            margin-bottom: 16px;
        }
        .blunder-card h4 { font-size: 15px; color: #FCA5A5; margin-bottom: 6px; font-weight: 700; }
        .blunder-card p { font-size: 13px; color: #CBD5E1; }

        .roadmap-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }
        .phase-card {
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 14px;
            padding: 22px;
        }
        .phase-badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 700;
            margin-bottom: 12px;
            text-transform: uppercase;
        }
        .phase-1 { background: rgba(239, 68, 68, 0.2); color: #F87171; border: 1px solid rgba(239, 68, 68, 0.3); }
        .phase-2 { background: rgba(59, 130, 246, 0.2); color: #60A5FA; border: 1px solid rgba(59, 130, 246, 0.3); }
        .phase-3 { background: rgba(16, 185, 129, 0.2); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); }
        .phase-card h4 { font-size: 16px; font-weight: 700; margin-bottom: 12px; }
        .phase-card ul { padding-left: 18px; font-size: 13px; color: #94A3B8; }
        .phase-card li { margin-bottom: 8px; }
    </style>
</head>
<body>

    <div class="header">
        <div>
            <h1>FABB6 (Glanzzkart Pvt Ltd) — Competitor Failure Autopsy & Turnaround Dashboard</h1>
            <p>Audited Period: 1st September 2026 – 18th November 2026 | Prepared by Techno Exponent</p>
        </div>
        <div>
            <span class="badge-danger">Account Triage & Recovery Status</span>
        </div>
    </div>

    <!-- Top KPIs -->
    <div class="grid-kpis">
        <div class="kpi-card red">
            <div class="kpi-label">Competitor Paid Ad Spend</div>
            <div class="kpi-val">₹67.83 L</div>
            <div class="kpi-sub neg">Sep 1 – Nov 18 (Google: ₹34.8L, Meta: ₹33.0L)</div>
        </div>
        <div class="kpi-card red">
            <div class="kpi-label">Competitor Blended Paid CPA</div>
            <div class="kpi-val">₹546.60</div>
            <div class="kpi-sub neg">+90% Inflation vs Plan B Target (₹287)</div>
        </div>
        <div class="kpi-card amber">
            <div class="kpi-label">Direct Avoidable Waste</div>
            <div class="kpi-val">₹7.46 L</div>
            <div class="kpi-sub neg">404 Errors, Glam+ Copy, Zero-Conv Traffic</div>
        </div>
        <div class="kpi-card green">
            <div class="kpi-label">TE 60-Day Target CPA</div>
            <div class="kpi-val">≤ ₹285.00</div>
            <div class="kpi-sub pos">4.2x+ Target ROAS via Funnel Restructure</div>
        </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="tabs">
        <button class="tab-btn active" onclick="showTab('tab-autopsy')">1. Forensic Autopsy & Trends</button>
        <button class="tab-btn" onclick="showTab('tab-blunders')">2. The 7 Smoking Guns (Competitor Errors)</button>
        <button class="tab-btn" onclick="showTab('tab-table')">3. Reconciled Monthly Data Table</button>
        <button class="tab-btn" onclick="showTab('tab-turnaround')">4. 90-Day Turnaround Roadmap</button>
    </div>

    <!-- Tab 1: Autopsy & Charts -->
    <div id="tab-autopsy" class="tab-pane active">
        <div class="charts-row">
            <div class="chart-box">
                <h3>Monthly Order Volume Collapse & Recovery Deficit</h3>
                <canvas id="ordersChart" height="180"></canvas>
            </div>
            <div class="chart-box">
                <h3>Paid CPA Inflation Trend (Dec 2025 - Nov 2026)</h3>
                <canvas id="cpaChart" height="180"></canvas>
            </div>
        </div>
    </div>

    <!-- Tab 2: Blunders -->
    <div id="tab-blunders" class="tab-pane">
        <div class="blunder-card">
            <h4>1. The "Glam+" Copy-Paste Disaster (Catastrophic Negligence)</h4>
            <p>In multiple live Google Performance Max campaigns (T4 Pro/Salon, T3 Premium, Pilgrim, YS24), competitor agency SilverXis literally copy-pasted headlines and copy from another client named "Glam+": <em>"Beauty & Skincare Must-Haves, Glam+ Store"</em>, <em>"Glow Up with Glam+ | Flas Sale is Live"</em> (with typos!), and audience signals tagged <em>"Glam Plus - Custom -CWV"</em>. FABB6 spent real advertising rupees promoting a completely different brand!</p>
        </div>
        <div class="blunder-card">
            <h4>2. The September 18 Tracking Blackout (Google Ads ₹7,569 CPA)</h4>
            <p>On Sep 18, 2026, the competitor executed <code>Conversion "Purchase-2026" removed</code> in Google Ads. This completely blinded Google's Smart Bidding algorithms. Consequently, in September, Google Ads delivered only 42 purchases on ₹3.18 Lakhs spend, resulting in an absurd CPA of ₹7,568.93 and a ROAS of 0.15x.</p>
        </div>
        <div class="blunder-card">
            <h4>3. October Festive Season (Diwali) Meltdown</h4>
            <p>During the highest e-commerce demand period in India, SilverXis pumped ₹42.47 Lakhs into ads. But Meta CPA surged to an all-time record high of ₹532.42 and ROAS tanked to 2.47x. Despite heavy spending, paid purchases (7,298) were lower than unoptimized July actuals (8,313 purchases on ₹43.6L spend).</p>
        </div>
        <div class="blunder-card">
            <h4>4. Retargeting Cost Inversion (DPA Higher CPA than Prospecting)</h4>
            <p>Dynamic Product Ads (Retargeting — DPA) spent ₹9,43,971 at a CPA of ₹514.99 (peaking at ₹570.31 in October). Retargeting was actually more expensive than cold prospecting because of severe audience exhaustion and no frequency capping.</p>
        </div>
        <div class="blunder-card">
            <h4>5. ₹80,285 Burned on 110 Dead Landing Pages (404 Errors)</h4>
            <p>Techno Exponent warned FABB6 in August about 186 Merchant Center catalog errors. The competitor ignored it. 110 products continued sending paid traffic to "Product page unavailable" 404 links (e.g. Foxtale 5% Niacinamide Serum spent ₹1,614 across 480 clicks with 0 sales).</p>
        </div>
        <div class="blunder-card">
            <h4>6. Zero-Conversion Traffic Waste & Zombie App Ads</h4>
            <p>Burned ₹50,214 on <code>IG-Traffic</code> for 8.31M impressions and exactly 0 purchases. Simultaneously burned ₹1.58 Lakhs on app promotion ads bombarding users at an extreme frequency of 13.18 at CPAs over ₹1,080.</p>
        </div>
        <div class="blunder-card">
            <h4>7. 140+ Hyperactive Budget Changes (Permanent Learning Phase)</h4>
            <p>SilverXis tweaked campaign budgets 140 times (74 increases, 66 decreases), often adjusting budgets by minor amounts every few hours/days. This constantly reset machine learning in Google Ads and Meta Ads, destroying bid stability.</p>
        </div>
    </div>

    <!-- Tab 3: Reconciled Table -->
    <div id="tab-table" class="tab-pane">
        <div class="table-box">
            <h3>Consolidated Performance Table (Shopify, Google Ads & Meta Ads)</h3>
            <table>
                <thead>
                    <tr>
                        <th>Month</th>
                        <th class="num">Shopify Orders</th>
                        <th class="num">Gross Sales (₹)</th>
                        <th class="num">Total Spend (₹)</th>
                        <th class="num">Paid Purchases</th>
                        <th class="num">Blended CPA (₹)</th>
                        <th class="num">Google CPA (₹)</th>
                        <th class="num">Meta CPA (₹)</th>
                        <th class="num">Shopify ROAS</th>
                    </tr>
                </thead>
                <tbody>
                    <tr><td>Dec 2025</td><td class="num">3,307</td><td class="num">₹26,37,583</td><td class="num">₹4,20,868</td><td class="num">1,614</td><td class="num">₹260.69</td><td class="num">₹481.09</td><td class="num">₹169.23</td><td class="num highlight-green">4.92x</td></tr>
                    <tr><td>Jan 2026</td><td class="num">7,850</td><td class="num">₹55,52,015</td><td class="num">₹12,16,540</td><td class="num">4,260</td><td class="num">₹285.55</td><td class="num">₹576.14</td><td class="num">₹154.63</td><td class="num highlight-green">3.81x</td></tr>
                    <tr><td>Feb 2026</td><td class="num">8,250</td><td class="num">₹64,10,361</td><td class="num">₹17,97,005</td><td class="num">4,817</td><td class="num">₹373.06</td><td class="num">₹648.53</td><td class="num">₹267.88</td><td class="num highlight-green">3.47x</td></tr>
                    <tr><td>Mar 2026</td><td class="num">11,285</td><td class="num">₹85,32,040</td><td class="num">₹27,84,074</td><td class="num">6,351</td><td class="num">₹438.38</td><td class="num">₹786.17</td><td class="num">₹288.93</td><td class="num">2.14x</td></tr>
                    <tr><td>Apr 2026</td><td class="num">10,551</td><td class="num">₹84,73,141</td><td class="num">₹32,55,208</td><td class="num">5,350</td><td class="num">₹608.41</td><td class="num">₹1372.38</td><td class="num">₹322.14</td><td class="num">2.28x</td></tr>
                    <tr><td>May 2026</td><td class="num">12,215</td><td class="num">₹1,00,96,287</td><td class="num">₹40,21,304</td><td class="num">7,076</td><td class="num">₹568.29</td><td class="num">₹1444.15</td><td class="num">₹336.81</td><td class="num">2.27x</td></tr>
                    <tr><td>Jun 2026</td><td class="num">12,877</td><td class="num">₹1,03,89,397</td><td class="num">₹42,86,498</td><td class="num">6,851</td><td class="num">₹625.67</td><td class="num">₹2199.24</td><td class="num">₹276.86</td><td class="num">1.96x</td></tr>
                    <tr><td>Jul 2026</td><td class="num">13,420</td><td class="num">₹1,03,64,270</td><td class="num">₹43,62,222</td><td class="num">8,313</td><td class="num">₹524.75</td><td class="num">₹1077.07</td><td class="num">₹313.48</td><td class="num">1.80x</td></tr>
                    <tr><td>Aug 2026</td><td class="num">11,069</td><td class="num">₹95,64,391</td><td class="num">₹82,75,293</td><td class="num">10,189</td><td class="num">₹812.16</td><td class="num">₹1130.18</td><td class="num">₹368.65</td><td class="num highlight-red">0.90x</td></tr>
                    <tr style="background: rgba(239, 68, 68, 0.1);"><td><strong>Sep 2026 (Comp)</strong></td><td class="num highlight-red">3,112</td><td class="num">₹36,01,597</td><td class="num">₹6,27,053</td><td class="num highlight-red">801</td><td class="num highlight-red">₹782.84</td><td class="num highlight-red">₹7,568.93</td><td class="num">₹407.32</td><td class="num">4.54x*</td></tr>
                    <tr style="background: rgba(239, 68, 68, 0.1);"><td><strong>Oct 2026 (Festive)</strong></td><td class="num">9,143</td><td class="num">₹1,05,66,667</td><td class="num">₹42,46,579</td><td class="num">7,298</td><td class="num highlight-red">₹581.84</td><td class="num">₹636.72</td><td class="num highlight-red">₹532.42</td><td class="num">2.14x</td></tr>
                    <tr style="background: rgba(239, 68, 68, 0.1);"><td><strong>Nov 2026 (Till 18th)</strong></td><td class="num">4,638</td><td class="num">₹53,17,824</td><td class="num">₹19,09,346</td><td class="num">4,310</td><td class="num">₹443.00</td><td class="num">₹415.60</td><td class="num">₹474.96</td><td class="num">2.20x</td></tr>
                </tbody>
            </table>
        </div>
    </div>

    <!-- Tab 4: Turnaround Roadmap -->
    <div id="tab-turnaround" class="tab-pane">
        <div class="roadmap-grid">
            <div class="phase-card">
                <span class="phase-badge phase-1">Phase 1: Week 1–2</span>
                <h4>14-Day Emergency Triage</h4>
                <ul>
                    <li>Purge all "Glam+" headlines and copy from PMax asset groups.</li>
                    <li>Re-implement Google Enhanced Conversions & Meta CAPI deduplication.</li>
                    <li>Remove 110 products with 404 dead links from Merchant Center.</li>
                    <li>Kill IG-Traffic, unoptimized app ads, and dead broad-match keywords.</li>
                    <li>Restructure Meta into 1 Prospecting ASC + 1 DPA Retargeting + 1 Retention.</li>
                </ul>
            </div>
            <div class="phase-card">
                <span class="phase-badge phase-2">Phase 2: Month 1 (Dec)</span>
                <h4>30-Day Stabilization</h4>
                <ul>
                    <li>Drive Meta CPA from ₹500+ down to ≤ ₹320 with fresh creative hooks.</li>
                    <li>Restructure Google PMax into 3 margin tiers on Target ROAS.</li>
                    <li>Launch automated WhatsApp / SMS re-order flows for 36.7% repeat users.</li>
                    <li>Deliver 12,500+ Shopify orders in December at Blended CPA ≤ ₹340.</li>
                </ul>
            </div>
            <div class="phase-card">
                <span class="phase-badge phase-3">Phase 3: Months 2–3 (Jan-Feb)</span>
                <h4>60–90 Day Profitable Scaling</h4>
                <ul>
                    <li>Scale ad spend to ₹40L–₹50L complying with ≤ 20% / 72hr budget pacing.</li>
                    <li>Expand daily orders from ~216/day to 650–750 orders/day.</li>
                    <li>Stabilize Blended CPA between ₹260–₹285 and ROAS at 4.2x–4.5x.</li>
                    <li>Rebuild compounding profitability with zero agency operational leakages.</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        function showTab(tabId) {
            document.querySelectorAll('.tab-pane').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            event.target.classList.add('active');
        }

        // Charts
        const months = ['Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep (Comp)', 'Oct (Festive)', 'Nov (18d)'];
        
        // Orders Chart
        new Chart(document.getElementById('ordersChart'), {
            type: 'bar',
            data: {
                labels: months,
                datasets: [
                    {
                        label: 'Shopify Total Orders',
                        data: [3307, 7850, 8250, 11285, 10551, 12215, 12877, 13420, 11069, 3112, 9143, 4638],
                        backgroundColor: months.map((m, idx) => idx >= 9 ? '#EF4444' : '#3B82F6'),
                        borderRadius: 6
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    x: { grid: { display: false }, ticks: { color: '#94A3B8' } },
                    y: { grid: { color: '#1E293B' }, ticks: { color: '#94A3B8' } }
                }
            }
        });

        // CPA Chart
        new Chart(document.getElementById('cpaChart'), {
            type: 'line',
            data: {
                labels: months,
                datasets: [
                    {
                        label: 'Blended Paid CPA (INR)',
                        data: [260.69, 285.55, 373.06, 438.38, 608.41, 568.29, 625.67, 524.75, 812.16, 782.84, 581.84, 443.00],
                        borderColor: '#F59E0B',
                        backgroundColor: 'rgba(245, 158, 11, 0.1)',
                        fill: true,
                        tension: 0.3,
                        pointRadius: 5
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: {
                    x: { grid: { display: false }, ticks: { color: '#94A3B8' } },
                    y: { grid: { color: '#1E293B' }, ticks: { color: '#94A3B8' } }
                }
            }
        });
    </script>
</body>
</html>
"""
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Written HTML Dashboard to: {html_path}")

    # Also copy HTML Dashboard to artifact directory
    html_path_artifact = r"C:\Users\test\.gemini\antigravity\brain\29f77e0a-5ed5-4d24-842c-443d9957274c\fabb6_turnaround_forensic_dashboard.html"
    with open(html_path_artifact, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Written HTML Dashboard artifact to: {html_path_artifact}")

if __name__ == '__main__':
    generate_all()
