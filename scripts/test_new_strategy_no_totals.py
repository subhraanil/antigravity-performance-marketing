import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import win32com.client
import pythoncom
import pypdf

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=25, bottom=25, left=35, right=35):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_styled_table(doc, data, header_bg="102C57", zebra=True, center_cols=[], right_cols=[], col_widths=None):
    table = doc.add_table(rows=len(data), cols=len(data[0]))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    header_tr = table.rows[0]._tr.get_or_add_trPr()
    header_tr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    
    for r_idx, row_vals in enumerate(data):
        row = table.rows[r_idx]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        is_header = (r_idx == 0)
        
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.text = str(val)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1.5)
            p.paragraph_format.space_after = Pt(1.5)
            p.paragraph_format.line_spacing = 1.02
            
            if c_idx in center_cols:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif c_idx in right_cols:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            for run in p.runs:
                run.font.name = "Calibri"
                if is_header:
                    run.font.size = Pt(7.0)
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(255, 255, 255)
                else:
                    run.font.size = Pt(6.8)
                    run.font.color.rgb = RGBColor(30, 30, 30)
                    
            if is_header:
                set_cell_background(cell, header_bg)
            else:
                if zebra and r_idx % 2 == 1:
                    set_cell_background(cell, "F9FAFB")
            set_cell_margins(cell, top=25, bottom=25, left=35, right=35)
            
    if col_widths and len(col_widths) == len(data[0]):
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)

def test_build(docx_path):
    doc = docx.Document()
    for s in doc.sections:
        s.top_margin = Inches(0.55)
        s.bottom_margin = Inches(0.55)
        s.left_margin = Inches(0.65)
        s.right_margin = Inches(0.65)
        
        header = s.header
        hp = header.paragraphs[0]
        hp.text = "FABB6 Performance Marketing Strategy & Campaign Architecture | Dec 2026 – Feb 2027"
        hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in hp.runs:
            run.font.name = "Calibri"
            run.font.size = Pt(7.5)
            run.font.color.rgb = RGBColor(128, 128, 128)
            
        footer = s.footer
        fp = footer.paragraphs[0]
        fp.text = "Techno Exponent · Growth & Performance Media Practice · Confidential Client Deliverable"
        fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        for run in fp.runs:
            run.font.name = "Calibri"
            run.font.size = Pt(7.5)
            run.font.color.rgb = RGBColor(128, 128, 128)

    def add_title(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1.5)
        r = p.add_run(text)
        r.font.name = "Georgia"
        r.font.size = Pt(16)
        r.font.bold = True
        r.font.color.rgb = RGBColor(16, 44, 87)
        return p

    def add_subtitle(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(1.5)
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(8.8)
        r.font.bold = True
        r.font.color.rgb = RGBColor(53, 95, 142)
        return p

    def add_meta_info(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(5)
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(7.6)
        r.font.color.rgb = RGBColor(110, 110, 110)
        return p

    def add_h1(text, page_break_before=False):
        if page_break_before:
            doc.add_page_break()
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(5.5)
        h.paragraph_format.space_after = Pt(2)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.name = "Georgia"
        r.font.size = Pt(11.0)
        r.font.bold = True
        r.font.color.rgb = RGBColor(16, 44, 87)
        return h

    def add_h2(text, page_break_before=False):
        if page_break_before:
            doc.add_page_break()
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(4.0)
        h.paragraph_format.space_after = Pt(1.5)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(8.8)
        r.font.bold = True
        r.font.color.rgb = RGBColor(31, 78, 120)
        return h

    def add_body(text, bold_prefix=""):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2.0)
        p.paragraph_format.line_spacing = 1.05
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = "Calibri"
            rb.font.size = Pt(8.0)
            rb.font.bold = True
            rb.font.color.rgb = RGBColor(30, 30, 30)
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(8.0)
        r.font.color.rgb = RGBColor(40, 40, 40)
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0.5)
        p.paragraph_format.space_after = Pt(1.5)
        p.paragraph_format.line_spacing = 1.05
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = "Calibri"
            rb.font.size = Pt(8.0)
            rb.font.bold = True
            rb.font.color.rgb = RGBColor(30, 30, 30)
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(8.0)
        r.font.color.rgb = RGBColor(40, 40, 40)
        return p

    # ==================== PAGE 1 ====================
    add_title("FABB6 Performance Marketing Strategy\n& Campaign Architecture")
    add_subtitle("Funnel-Wise Architecture, Monthly Budget Schedules & Unit Economics Blueprint")
    add_meta_info("Prepared for FABB6 (Glanzzkart Private Limited) · Planning Horizon: Dec 2026 – Feb 2027 · Governance: Budget, Orders & ROAS")

    add_h1("1. Executive Summary & Three Strategic Plans")
    add_body("This document articulates the performance marketing strategy, campaign architecture, and monthly budget execution schedules for FABB6 across Google Ads and Meta Ads for December 2026, January 2027, and February 2027. Following the forensic audit of the interim agency tenure (SilverXis, Sep 1 – Nov 18), this strategy restructures campaigns to eliminate wasteful spend on broken URLs and negative-margin items, implements automated catalog sync tooling, and activates high-intent demand generation.")

    add_body("All scenarios are governed strictly on a month-by-month basis by Total Media Budget (Spend), Total Store Orders (Order Volume), and Shopify Confirmed Gross Sales ROAS. The Recommended Plan represents the client's official target turnaround model (Dec ₹30.0L / Jan ₹35.0L / Feb ₹40.0L), flanked by an accelerated Moderate Plan and a high-scale Aggressive Plan:")

    # Three Strategic Plans Table - 9 rows (3 plans x 3 months) - ZERO 3-MONTH TOTALS
    scen_table_data = [
        ["Strategic Plan", "Strategic Posture", "Month", "Ad Budget (Spend)", "Google / Meta Split", "Paid Orders", "Others*", "Store Orders", "Gross Sales Revenue", "Store ROAS"],
        ["Plan 1: Recommended", "Baseline Turnaround", "Dec 2026", "₹30.00L", "₹19.00L / ₹11.00L", "6,082", "3,096", "9,178", "₹93.06L", "3.10x"],
        ["Plan 1: Recommended", "Baseline Turnaround", "Jan 2027", "₹35.00L", "₹22.00L / ₹13.00L", "7,680", "3,313", "10,992", "₹121.25L", "3.46x"],
        ["Plan 1: Recommended", "Baseline Turnaround", "Feb 2027", "₹40.00L", "₹25.00L / ₹15.00L", "9,801", "3,545", "13,346", "₹164.42L", "4.11x"],
        ["Plan 2: Moderate", "Accelerated Scale", "Dec 2026", "₹35.00L", "₹22.00L / ₹13.00L", "6,950", "3,096", "10,046", "₹103.50L", "2.96x"],
        ["Plan 2: Moderate", "Accelerated Scale", "Jan 2027", "₹41.00L", "₹26.00L / ₹15.00L", "8,800", "3,313", "12,113", "₹136.50L", "3.33x"],
        ["Plan 2: Moderate", "Accelerated Scale", "Feb 2027", "₹47.00L", "₹29.50L / ₹17.50L", "11,250", "3,545", "14,795", "₹184.20L", "3.92x"],
        ["Plan 3: Aggressive", "Market Dominance", "Dec 2026", "₹40.00L", "₹25.00L / ₹15.00L", "7,750", "3,096", "10,846", "₹113.20L", "2.83x"],
        ["Plan 3: Aggressive", "Market Dominance", "Jan 2027", "₹48.00L", "₹30.50L / ₹17.50L", "10,050", "3,313", "13,363", "₹151.20L", "3.15x"],
        ["Plan 3: Aggressive", "Market Dominance", "Feb 2027", "₹55.00L", "₹34.50L / ₹20.50L", "12,850", "3,545", "16,395", "₹204.50L", "3.72x"]
    ]
    create_styled_table(doc, scen_table_data, header_bg="102C57", center_cols=[2, 3, 4, 5, 6, 7, 9], right_cols=[8], col_widths=[1.1, 1.0, 0.6, 0.75, 1.15, 0.55, 0.45, 0.55, 0.65, 0.45])
    add_body("*Order From Others represents repeat customer purchases, organic search, direct store traffic, and automated retention flows compounding at +7% monthly.")

    add_h2("Monthly Capital Allocation Analysis & Scaling Efficiency")
    add_bullet("Moving from Recommended to Moderate commits ₹5.0L to ₹7.0L additional monthly spend, capturing 868 to 1,449 incremental monthly orders. This tier accelerates top-line growth while maintaining healthy store efficiency above 2.95x ROAS.", bold_prefix="Recommended to Moderate: ")
    add_bullet("Moving from Moderate to Aggressive commits ₹5.0L to ₹8.0L further monthly media spend, capturing 800 to 1,600 incremental monthly orders. Marginal efficiency reflects normal, healthy diminishing returns as ad delivery penetrates broader cold audiences.", bold_prefix="Moderate to Aggressive: ")

    # ==================== PAGE 2 ====================
    add_h1("2. Unit Economics, Checkout Optimization & Retention Strategy", page_break_before=True)
    add_body("To maintain complete financial clarity, this strategy articulates the exact contribution economics of customer acquisition. As an authorized distributor for professional salon brands (Swiss Beauty, L'Oréal Professionnel, Matrix, Schwarzkopf, Floractive), FABB6 operates on gross wholesale product margins of ~25% on ex-GST trade value. Assuming 18% GST, mathematical media break-even requires a 4.00x ROAS on ex-GST revenue (1 ÷ 0.25) and 4.72x ROAS on GST-inclusive total receipts (4.00x × 1.18). Front-end paid media acquires customers near first-order margin break-even, while sustainable profit is achieved through repeat replenishment that incurs zero incremental media cost.")

    add_h2("Low-Cost Retention Channel Architecture (Zero Incremental Media Spend)")
    add_body("Repeat retention is driven primarily by automated WhatsApp and email replenishment workflows timed to hair spa, shampoo, and color usage cycles (30, 45, and 60 days). While retention software and messaging incurs operational costs (~₹35,000–₹50,000/month), it requires zero incremental media spend. This zero-media-cost retention engine unlocks 3,096 (Dec), 3,313 (Jan), and 3,545 (Feb) monthly 'Orders from Others' in the Recommended Plan:")

    # Retention Workflows Table
    ret_table_data = [
        ["Workflow / Trigger Stage", "Timing Window", "Primary Messaging Channel", "Target Product Category", "Replenishment Trigger & Offer Architecture"],
        ["W1: Core Shampoo & Conditioner", "Day 25 – 35", "WhatsApp Interactive Flow + Email", "L'Oréal, Matrix, Schwarzkopf Care", "Automated usage check-in; one-click re-order with 5% replenishment loyalty discount."],
        ["W2: Hair Spa & Intensive Masques", "Day 40 – 50", "WhatsApp Catalog + RCS Message", "L'Oréal Deep Nourish, Matrix Masque", "Reminder that 500g tubs reach half-volume; salon combo upsell (Serum + Masque)."],
        ["W3: Salon Pro & Chemical Treatments", "Day 60 – 75", "Email VIP Concierge + WhatsApp", "Floractive Nanoplastia, Raaga De-Tan", "Professional salon replenishment cadence; bulk volume tier pricing for repeat buyers."],
        ["W4: VIP Retention & Cross-Sell", "Day 90+", "Automated SMS / WhatsApp Template", "Cross-Category Beauty / Skincare", "Exclusive early access to seasonal combo kits; dynamic store credit balance alerts."]
    ]
    create_styled_table(doc, ret_table_data, header_bg="102C57", center_cols=[1, 2], right_cols=[], col_widths=[1.5, 0.9, 1.4, 1.4, 2.0])

    add_h2("Required Technology Stack: GoKwik Checkout & Customer Notification Engine")
    add_bullet("We will integrate GoKwik (https://www.gokwik.co/) on Shopify to maximize checkout conversion and remarketing: (1) 1-Click KwikCheckout with 100M+ pre-filled Indian shopper addresses, drastically reducing checkout abandonment; (2) Automated WhatsApp and SMS abandoned cart remarketing sequences with personalized checkout recovery links, recapturing 15–20% of lost carts; (3) AI RTO risk intelligence and COD-to-Prepaid conversion discounts to minimize failed delivery costs.", bold_prefix="GoKwik Checkout & Abandoned Cart Remarketing: ")
    add_bullet("To execute the W1–W4 replenishment flows, we deploy a dedicated WhatsApp Business API & automated notification subscription (such as Interakt, Wati, or Bik.ai) paired with Klaviyo email CRM. This infrastructure triggers timely replenishment notifications directly to existing customer phones based on purchase history, driving high repeat volume without any media spend.", bold_prefix="Existing Customer Notification Subscriptions: ")

    add_h2("Recommended Plan Monthly Economics & Execution Walkthrough")
    add_bullet("Paid CPA reduces systematically monthly from ₹480/₹518 (Google/Meta) in December to ₹451/₹464 in January and ₹407/₹410 in February, driven by negative keyword hygiene, conversion tracking stabilization, and Performance Max asset score optimization.", bold_prefix="Paid CPA Discipline: ")
    add_bullet("Because substantial store volume stems from organic traffic and zero-media-cost retention flows (3,096 to 3,545 monthly orders), blended acquisition cost improves from ₹326.87 in December to ₹318.40 in January and ₹299.72 in February.", bold_prefix="Blended Store Economics: ")
    add_bullet("Acquisition economics and average order sizes are safeguarded through minimum free-shipping thresholds (₹999) and dedicated 2-pack and 3-pack combo merchandising across core haircare collections.", bold_prefix="Order Value Protection: ")

    # ==================== PAGE 3 ====================
    add_h1("3. Channel Allocation, Google Ads & Merchant Center Automation", page_break_before=True)
    add_body("In the Recommended Plan, monthly ad spend is allocated ~63% Google Ads and ~37% Meta Ads: December allocates ₹19.00L Google (63.3%) and ₹11.00L Meta (36.7%), transitioning to ₹22.00L Google / ₹13.00L Meta in January and ₹25.00L Google / ₹15.00L Meta in February.")

    add_h2("Google Ads Campaign Architecture & Monthly Allocation")
    add_body("Google Ads spend is structured into four distinct campaign nodes to ensure high-margin catalog SKUs receive the majority of budget while broad query waste is permanently eliminated:")

    g_table_data = [
        ["Campaign Name", "Funnel Node", "Budget Share", "Dec Spend (Daily)", "Jan Spend (Daily)", "Feb Spend (Daily)", "Bidding Strategy & CPA/ROAS Targets"],
        ["G_PMAX_BOF_HighMargin_Heroes", "BOF (Heroes)", "60%", "₹11.40L (₹36,774/d)", "₹13.20L (₹42,581/d)", "₹15.00L (₹53,571/d)", "tROAS: 210% Dec → 245% Jan → 300% Feb. Priority on Nanoplastia, Loreal combos."],
        ["G_PMAX_BOF_CoreVolume_Tier2", "BOF (Core)", "20%", "₹3.80L (₹12,258/d)", "₹4.40L (₹14,194/d)", "₹5.00L (₹17,857/d)", "tROAS: 185% Dec → 215% Jan → 250% Feb. Dot & Key sunscreens, Hair Spa tubs."],
        ["G_SRC_MOF_Category_HairCare", "MOF (Category)", "13%", "₹2.47L (₹7,968/d)", "₹2.86L (₹9,226/d)", "₹3.25L (₹11,607/d)", "tCPA: ₹480 Dec → ₹451 Jan → ₹407 Feb. Exact & phrase search on professional hair care."],
        ["G_SRC_BOF_Brand_FABB6_Exact", "BOF (Brand)", "7%", "₹1.33L (₹4,290/d)", "₹1.54L (₹4,968/d)", "₹1.75L (₹6,250/d)", "Target Impression Share ≥ 95% Absolute Top. Defends brand queries against competitors."],
        ["Total Google Ads Portfolio", "Combined", "100%", "₹19.00L (₹61,290/d)", "₹22.00L (₹70,968/d)", "₹25.00L (₹89,286/d)", "Target CPA: ₹480 → ₹451 → ₹407 | Target ROAS: 2.11x → 2.45x → 3.03x"]
    ]
    create_styled_table(doc, g_table_data, header_bg="102C57", center_cols=[1, 2], right_cols=[3, 4, 5], col_widths=[1.5, 0.7, 0.8, 1.0, 1.0, 1.0, 1.2])

    add_h2("Merchant Center Product Sync Tool Recommendation: Simprosys Google Shopping Feed")
    add_body("To permanently eliminate wasted spend on 404 broken links (110 broken URLs identified in audit) and out-of-stock products, we recommend deploying Simprosys Google Shopping Feed (Shopify App):")
    add_bullet("Directly syncs Shopify inventory and price updates via Shopify webhooks to Google Content API in minutes. When an item drops to 0 inventory, it is instantly suppressed from Google Shopping and PMax ads, halting click bleed.", bold_prefix="Real-Time Webhook Synchronization: ")
    add_bullet("Continuously validates Shopify product URLs. Inactive, deleted, or draft products are automatically removed from the active feed before Merchant Center disapproves them.", bold_prefix="Automated 404 Broken Link Detection: ")
    add_bullet("Maps Shopify product tags (high_28plus, mid_20_28, EXCLUDE_lowmargin, single_sachet) to custom_label_0 through custom_label_4 for automated campaign bid gating.", bold_prefix="Automated Custom Label & Margin Tagging: ")
    add_bullet("Operational cost is ~$15–$25/month (~₹1,200–₹2,100/mo), paying for itself on day 1 by preventing broken URL waste. Enterprise alternative: Feedonomics for advanced multi-channel rule engines.", bold_prefix="Low Cost & High ROI: ")

    # ==================== PAGE 4 ====================
    add_h1("4. Meta Ads Architecture & Scaling Governance", page_break_before=True)
    add_body("Meta Ads spend (December ₹11.00L, January ₹13.00L, February ₹15.00L) is consolidated from fragmented, overlapping campaigns into a streamlined three-tier funnel to eliminate internal auction competition and bring runaway CPMs (+144% under interim agency) back under control:")

    m_table_data = [
        ["Campaign Name", "Funnel Level", "Budget Share", "Dec Spend (Daily)", "Jan Spend (Daily)", "Feb Spend (Daily)", "Audience Targeting & Creative Strategy"],
        ["M_ASC_TOF_MasterProspecting", "TOF (Prospecting)", "70%", "₹7.70L (₹24,839/d)", "₹9.10L (₹29,355/d)", "₹10.50L (₹37,500/d)", "Advantage+ Shopping Campaign. Broad open targeting with 10 new UGC problem-solution creator videos. 15% existing customer budget cap; 30-day purchaser exclusion."],
        ["M_CBO_MOF_HeroCombos_Collection", "MOF (Combos)", "15%", "₹1.65L (₹5,323/d)", "₹1.95L (₹6,290/d)", "₹2.25L (₹8,036/d)", "Engaged Instagram/FB visitors (past 60d) and 3s+ video viewers. Carousel & collection ads featuring high-value haircare combos (>₹1,200)."],
        ["M_DPA_BOF_DynamicCatalog_7d", "BOF (Retargeting)", "15%", "₹1.65L (₹5,323/d)", "₹1.95L (₹6,290/d)", "₹2.25L (₹8,036/d)", "Dynamic Product Ads for ViewContent (3–7d) & AddToCart (3–14d). Strict 30d/180d purchaser exclusions. Frequency capped ≤ 2.2x."],
        ["Total Meta Ads Portfolio", "Combined", "100%", "₹11.00L (₹35,484/d)", "₹13.00L (₹41,935/d)", "₹15.00L (₹53,571/d)", "Target CPA: ₹518 → ₹464 → ₹410 | Target ROAS: 1.96x → 2.38x → 3.00x"]
    ]
    create_styled_table(doc, m_table_data, header_bg="102C57", center_cols=[1, 2], right_cols=[3, 4, 5], col_widths=[1.5, 0.7, 0.8, 1.0, 1.0, 1.2])

    add_h2("Three-Tier Scaling Decision Governance (Weekly Performance Gates)")
    add_body("Monthly budget scaling from December to January and February is strictly governed by trailing 7-day verified store performance:")
    add_bullet("Trailing 7-day confirmed Gross ROAS ≥ 2.50x AND blended CPA within monthly target (Dec ≤ ₹480, Jan ≤ ₹450, Feb ≤ ₹410). Approve scheduled monthly budget increase, capped at ≤ 20% every 72 hours per campaign.", bold_prefix="Green Light (Scale): ")
    add_bullet("Trailing 7-day Gross ROAS between 2.30x and 2.50x. Hold daily budgets completely flat. Analyze SKU-level contribution, rotate creative fatigue, and allow Smart Bidding algorithms to consolidate.", bold_prefix="Yellow Light (Hold): ")
    add_bullet("Trailing 7-day Gross ROAS < 2.30x for 7 consecutive days (or blended CPA exceeds target by >25%). Immediately roll back the last budget increase by 20% and pause any underperforming ad set.", bold_prefix="Red Light (Rollback): ")

    # ==================== PAGE 5 ====================
    add_h1("5. Daily Budget Schedules & Measurement Definitions", page_break_before=True)
    add_body("The schedules below provide the exact campaign-level daily budgets for Plan 1 (Recommended Plan) across December, January, and February (phased):")

    daily_rec_table = [
        ["Channel", "Campaign Name / Architecture Node", "Funnel Node", "Dec Daily (₹30.0L)", "Jan Daily (₹35.0L)", "Feb 1–14 Daily", "Feb 15–28 Daily"],
        ["Google Ads", "G_PMAX_BOF_HighMargin_Heroes", "BOF (Heroes 60%)", "₹36,774 / day", "₹42,581 / day", "₹48,000 / day", "₹59,143 / day"],
        ["Google Ads", "G_PMAX_BOF_CoreVolume_Tier2", "BOF (Core 20%)", "₹12,258 / day", "₹14,194 / day", "₹16,000 / day", "₹19,714 / day"],
        ["Google Ads", "G_SRC_MOF_Category_HairCare", "MOF (Category 13%)", "₹7,968 / day", "₹9,226 / day", "₹10,400 / day", "₹12,814 / day"],
        ["Google Ads", "G_SRC_BOF_Brand_FABB6_Exact", "BOF (Brand 7%)", "₹4,290 / day", "₹4,968 / day", "₹5,600 / day", "₹6,900 / day"],
        ["Google Total", "Combined Google Ads (63.3% / 62.5%)", "Google Portfolio", "₹61,290 / day", "₹70,968 / day", "₹80,000 / day", "₹98,571 / day"],
        ["Meta Ads", "M_ASC_TOF_MasterProspecting", "TOF (ASC 70%)", "₹24,839 / day", "₹29,355 / day", "₹33,000 / day", "₹42,000 / day"],
        ["Meta Ads", "M_CBO_MOF_HeroCombos_Collection", "MOF (Combos 15%)", "₹5,323 / day", "₹6,290 / day", "₹7,071 / day", "₹9,000 / day"],
        ["Meta Ads", "M_DPA_BOF_DynamicCatalog_7d", "BOF (DPA 15%)", "₹5,323 / day", "₹6,290 / day", "₹7,071 / day", "₹9,000 / day"],
        ["Meta Total", "Combined Meta Ads (36.7% / 37.5%)", "Meta Portfolio", "₹35,484 / day", "₹41,935 / day", "₹47,143 / day", "₹60,000 / day"],
        ["Total Media", "Combined Account Daily Spend", "Full Account", "₹96,774 / day", "₹1,12,903 / day", "₹1,27,143 / day", "₹1,58,571 / day"]
    ]
    create_styled_table(doc, daily_rec_table, header_bg="102C57", center_cols=[0, 2], right_cols=[3, 4, 5, 6], col_widths=[0.85, 2.0, 1.05, 0.85, 0.85, 0.85, 0.85])

    add_h2("Operational Measurement Definitions & KPI Hierarchy")
    add_bullet("Total confirmed sales revenue recorded in Shopify before cancellations, discounts and returns. Primary top-line metric evaluated weekly.", bold_prefix="Gross Sales Revenue: ")
    add_bullet("Total Gross Sales Revenue divided by total ad spend. Account targets: 3.10x Dec, 3.46x Jan, 4.11x Feb.", bold_prefix="Shopify Gross ROAS: ")
    add_bullet("Total media spend divided by total Shopify store orders (₹326.87 Dec, ₹318.40 Jan, ₹299.72 Feb). Primary governing business unit metric.", bold_prefix="Spend per Store Order (Blended CPA): ")
    add_bullet("Ad spend divided by platform-reported orders (Google ₹480 → ₹407, Meta ₹518 → ₹410). Operational secondary guardrail.", bold_prefix="Platform Paid CPA: ")
    add_bullet("Target cost ceilings entered in campaign bid settings (Search tCPA ₹407–₹480, Meta Cost Cap ₹410–₹518).", bold_prefix="Bidding CPA Ceilings: ")
    add_bullet("Daily tracking snapshot via Slack/WhatsApp, weekly gate reviews, and monthly Shopify financial reconciliation.", bold_prefix="Agency Cadence: ")

    os.makedirs(os.path.dirname(docx_path), exist_ok=True)
    doc.save(docx_path)
    print(f"Successfully generated new strategy DOCX at: {docx_path}")

def convert_docx_to_pdf(docx_path, pdf_path):
    pythoncom.CoInitialize()
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    try:
        abs_docx = os.path.abspath(docx_path)
        abs_pdf = os.path.abspath(pdf_path)
        doc = word.Documents.Open(abs_docx)
        doc.SaveAs(abs_pdf, FileFormat=17)
        doc.Close(False)
        print(f"Successfully converted DOCX to PDF at: {pdf_path}")
    finally:
        word.Quit()

if __name__ == "__main__":
    t_docx = r"C:\Users\test\Videos\Office\reports\test_no_totals.docx"
    t_pdf = r"C:\Users\test\Videos\Office\reports\test_no_totals.pdf"
    test_build(t_docx)
    convert_docx_to_pdf(t_docx, t_pdf)
    reader = pypdf.PdfReader(t_pdf)
    print(f"RESULTING PDF PAGE COUNT: {len(reader.pages)}")
