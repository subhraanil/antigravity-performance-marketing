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
        is_total = (r_idx == len(data) - 1 and any(k in str(row_vals[0]) for k in ["Total", "Combined", "Plan 3"]))
        
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
                elif is_total:
                    run.font.size = Pt(7.0)
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(16, 44, 87)
                else:
                    run.font.size = Pt(6.8)
                    run.font.color.rgb = RGBColor(30, 30, 30)
                    
            if is_header:
                set_cell_background(cell, header_bg)
            elif is_total:
                set_cell_background(cell, "EAECEE")
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

    # PAGE 1
    add_title("FABB6 Performance Marketing Strategy\n& Campaign Architecture (Q1 2027)")
    add_subtitle("Funnel-Wise Campaign Architecture, Daily Budget Execution & Unit Economics Blueprint")
    add_meta_info("Prepared for FABB6 (Glanzzkart Private Limited) · Planning Horizon: Dec 2026 – Feb 2027 · Governance: Budget, Orders & ROAS")

    add_h1("1. Executive Summary & Three Strategic Plans")
    add_body("This document articulates the complete performance marketing strategy, full-funnel media architecture, and daily budget execution schedules for FABB6 across Google Ads and Meta Ads for December 2026 to February 2027. Following the forensic audit of the interim agency tenure (SilverXis, Sep 1 – Nov 18), this strategy restructures campaigns to eliminate wasteful spend on broken URLs and negative-margin items, implements automated catalog sync tooling, and activates high-intent demand generation.")

    add_body("The three strategic plans below are governed strictly by Total Media Budget (Spend), Total Store Orders (Order Volume), and Shopify Gross Sales ROAS (Confirmed ROAS). Below, each plan provides the month-wise budget schedule alongside full-quarter volume and efficiency outcomes. The Recommended Plan represents the client's validated target turnaround model (Dec ₹26.0L / Jan ₹31.0L / Feb ₹34.1L; Total ₹91.1L), flanked by a defensive Base Plan and a high-scale Aggressive Plan:")

    # Three Strategic Plans Table with Month-Wise Budget Columns
    scen_table_data = [
        ["Plan Name", "Strategic Posture", "Dec 2026 Budget", "Jan 2027 Budget", "Feb 2027 Budget", "Total Media Spend", "Google / Meta Split", "Paid Orders", "Orders Others*", "Total Store Orders", "Gross Sales Revenue", "Store ROAS"],
        ["Plan 1: Base", "Minimum / Capital Preservation", "₹20.00L", "₹24.00L", "₹26.00L", "₹70.00L", "₹43.5L / ₹26.5L (62/38)", "17,129", "8,359", "25,488", "₹287.21L (~₹2.87 Cr)", "4.10x"],
        ["Plan 2: Recommended", "Target Turnaround (Client Model)", "₹26.00L", "₹31.00L", "₹34.10L", "₹91.10L", "₹58.0L / ₹33.1L (64/36)", "21,621", "9,954", "31,574", "₹355.91L (~₹3.56 Cr)", "3.91x"],
        ["Plan 3: Aggressive", "High Scale / Market Dominance", "₹30.00L", "₹38.00L", "₹44.50L", "₹112.50L", "₹72.5L / ₹40.0L (64/36)", "25,833", "11,038", "36,871", "₹416.83L (~₹4.17 Cr)", "3.71x"]
    ]
    create_styled_table(doc, scen_table_data, header_bg="102C57", center_cols=[2, 3, 4, 5, 6, 7, 8, 9, 11], right_cols=[10], col_widths=[0.85, 1.05, 0.52, 0.52, 0.52, 0.58, 0.85, 0.48, 0.45, 0.48, 0.90, 0.44])
    add_body("*Order From Others represents repeat customer purchases, organic search, direct store traffic, and automated retention flows. Growth is modeled at +7% monthly in Plan 2, +5% in Plan 1, and +8% in Plan 3.")

    # Dedicated Month-Wise Channel Allocation Sub-Table
    add_h2("Month-Wise Media Budget Allocation by Channel & Strategy")
    month_channel_table = [
        ["Planning Horizon", "Plan 1: Base (Google / Meta / Total)", "Plan 2: Recommended (Google / Meta / Total)", "Plan 3: Aggressive (Google / Meta / Total)"],
        ["December 2026", "₹12.40L / ₹7.60L (Total: ₹20.00L)", "₹16.00L / ₹10.00L (Total: ₹26.00L)", "₹19.20L / ₹10.80L (Total: ₹30.00L)"],
        ["January 2027", "₹15.00L / ₹9.00L (Total: ₹24.00L)", "₹20.00L / ₹11.00L (Total: ₹31.00L)", "₹24.50L / ₹13.50L (Total: ₹38.00L)"],
        ["February 2027", "₹16.10L / ₹9.90L (Total: ₹26.00L)", "₹22.00L / ₹12.10L (Total: ₹34.10L)", "₹28.80L / ₹15.70L (Total: ₹44.50L)"],
        ["Total Q1 Allocation", "₹43.50L / ₹26.50L (Total: ₹70.00L)", "₹58.00L / ₹33.10L (Total: ₹91.10L)", "₹72.50L / ₹40.00L (Total: ₹112.50L)"]
    ]
    create_styled_table(doc, month_channel_table, header_bg="1F4E78", center_cols=[1, 2, 3], right_cols=[], col_widths=[1.2, 2.0, 2.0, 2.0])

    add_h2("Capital Allocation Analysis & Marginal Return")
    add_bullet("Moving from Plan 1 to Plan 2 commits an incremental ₹21.10 Lakhs in ad spend to generate ₹68.70 Lakhs in additional gross sales—delivering a 3.26x Marginal ROAS and capturing 6,086 incremental orders at ₹346.70 spend per order. This makes Plan 2 the highly efficient, profit-maximizing growth tier.", bold_prefix="Base to Recommended (Plan 1 → Plan 2): ")
    add_bullet("Moving from Plan 2 to Plan 3 invests an additional ₹21.40 Lakhs in ad spend to generate ₹60.92 Lakhs in gross sales—delivering a 2.85x Marginal ROAS and capturing 5,297 incremental orders at ₹404.00 spend per order. While volume expands to 36,871 orders, marginal efficiency begins normal diminishing returns as ad delivery penetrates broader audiences.", bold_prefix="Recommended to Aggressive (Plan 2 → Plan 3): ")

    # PAGE 2: UNIT ECONOMICS, RETENTION & GOKWIK / SUBSCRIPTION TECH STACK
    add_h1("2. Unit Economics, Checkout Optimization & Retention Strategy", page_break_before=True)
    add_body("To maintain complete financial clarity, this strategy articulates the exact contribution economics of customer acquisition. As an authorized distributor for professional salon brands (Swiss Beauty, L'Oréal Professionnel, Matrix, Schwarzkopf, Floractive), FABB6 operates on gross wholesale product margins of ~25% on ex-GST trade value. Assuming 18% GST, mathematical media break-even requires a 4.00x ROAS on ex-GST revenue (1 ÷ 0.25) and 4.72x ROAS on GST-inclusive total receipts (4.00x × 1.18). Front-end paid media acquires customers near first-order margin break-even, while sustainable profit is achieved through repeat replenishment that incurs zero incremental media cost.")

    add_h2("Low-Cost Retention Channel Architecture (Zero Incremental Media Spend)")
    add_body("Repeat retention is driven primarily by automated WhatsApp and email replenishment workflows timed to hair spa, shampoo, and color usage cycles (30, 45, and 60 days). While retention software and messaging incurs operational costs (~₹35,000–₹50,000/month), it requires zero incremental media spend. This zero-media-cost retention engine unlocks 9,954 'Orders from Others' in Plan 2 (31.5% of total volume) and elevates account efficiency from a 2.68x paid ROAS to a 3.91x blended store ROAS:")

    # Retention Workflows Table
    ret_table_data = [
        ["Workflow / Trigger Stage", "Timing Window", "Primary Messaging Channel", "Target Product Category", "Replenishment Trigger & Offer Architecture"],
        ["W1: Core Shampoo & Conditioner", "Day 25 – 35", "WhatsApp Interactive Flow + Email", "L'Oréal, Matrix, Schwarzkopf Care", "Automated usage check-in; one-click re-order with 5% replenishment loyalty discount."],
        ["W2: Hair Spa & Intensive Masques", "Day 40 – 50", "WhatsApp Catalog + RCS Message", "L'Oréal Deep Nourish, Matrix Masque", "Reminder that 500g tubs reach half-volume; salon combo upsell (Serum + Masque)."],
        ["W3: Salon Pro & Chemical Treatments", "Day 60 – 75", "Email VIP Concierge + WhatsApp", "Floractive Nanoplastia, Raaga De-Tan", "Professional salon replenishment cadence; bulk volume tier pricing for repeat buyers."],
        ["W4: VIP Retention & Cross-Sell", "Day 90+", "Automated SMS / WhatsApp Template", "Cross-Category Beauty / Skincare", "Exclusive early access to seasonal combo kits; dynamic store credit balance alerts."]
    ]
    create_styled_table(doc, ret_table_data, header_bg="102C57", center_cols=[1, 2], right_cols=[], col_widths=[1.5, 0.9, 1.4, 1.4, 2.0])

    add_h2("Required Technology Tooling: GoKwik Checkout & Customer Notification Stack")
    add_bullet("We will integrate GoKwik (https://www.gokwik.co/) on Shopify to maximize checkout conversion and remarketing: (1) 1-Click KwikCheckout with 100M+ pre-filled Indian shopper addresses, drastically reducing drop-offs; (2) Automated WhatsApp and SMS abandoned cart remarketing sequences with personalized checkout recovery links, recapturing 15–20% of lost carts; (3) AI RTO risk intelligence and COD-to-Prepaid conversion discounts to minimize failed delivery costs.", bold_prefix="GoKwik Checkout & Abandoned Cart Remarketing: ")
    add_bullet("To execute the W1–W4 replenishment flows, we deploy a dedicated WhatsApp Business API & automated notification subscription (such as Interakt, Wati, or Bik.ai) paired with Klaviyo email CRM. This infrastructure triggers timely replenishment notifications directly to existing customer phones based on purchase history, driving high repeat volume without any media spend.", bold_prefix="Existing Customer Notification Subscriptions: ")

    add_h2("Recommended Plan Unit Economics & Margin Walkthrough")
    add_bullet("Paid CPA reduces systematically by 4% monthly from ₹450.00 in December to ₹422.68 in January and ₹400.77 in February, driven by negative keyword hygiene, conversion tracking stabilization, and Performance Max asset score optimization.", bold_prefix="Paid CPA Discipline: ")
    add_bullet("Because 31.5% of store orders (9,954 orders) stem from organic traffic and zero-media-cost retention flows, blended acquisition cost is just ₹288.53 per order—well below the ₹421.35 paid CPA.", bold_prefix="Blended Store Economics: ")
    add_bullet("Acquisition economics and average order sizes are safeguarded through minimum free-shipping thresholds (₹999) and dedicated 2-pack and 3-pack combo merchandising across core haircare collections.", bold_prefix="Order Value Protection: ")

    # PAGE 3: GOOGLE ADS
    add_h1("3. Channel Allocation, Google Ads & Merchant Center Automation", page_break_before=True)
    add_body("In Plan 2 (Recommended), Q1 ad spend is allocated 63.7% Google Ads (₹58.00 Lakhs) and 36.3% Meta Ads (₹33.10 Lakhs). In December, Google is allocated ₹16.00 Lakhs (61.5%) and Meta ₹10.00 Lakhs (38.5%), transitioning to ₹20.0L Google / ₹11.0L Meta in January and ₹22.0L Google / ₹12.1L Meta in February.")

    add_h2("Google Ads Campaign Architecture (₹58.00L Total Spend)")
    add_body("Google Ads spend is structured into four distinct campaign nodes to ensure high-margin catalog SKUs receive the majority of budget while broad query waste is permanently eliminated:")

    g_table_data = [
        ["Campaign Name", "Funnel Node", "Budget Share", "Dec Spend (Daily)", "Jan Spend (Daily)", "Feb Spend (Daily)", "Bidding Strategy & CPA/ROAS Targets"],
        ["G_PMAX_BOF_HighMargin_Heroes", "BOF (Heroes)", "60% (₹34.80L)", "₹9.60L (₹30,968/d)", "₹12.00L (₹38,710/d)", "₹13.20L (₹47,143/d)", "tROAS: 220% Dec → 240% Jan → 260% Feb. Priority on Nanoplastia, Loreal combos."],
        ["G_PMAX_BOF_CoreVolume_Tier2", "BOF (Core)", "20% (₹11.60L)", "₹3.20L (₹10,323/d)", "₹4.00L (₹12,903/d)", "₹4.40L (₹15,714/d)", "tROAS: 190% Dec → 210% Jan → 230% Feb. Dot & Key sunscreens, Hair Spa tubs."],
        ["G_SRC_MOF_Category_HairCare", "MOF (Category)", "13% (₹7.54L)", "₹2.08L (₹6,710/d)", "₹2.60L (₹8,387/d)", "₹2.86L (₹10,214/d)", "tCPA: ₹450 Dec → ₹430 Jan → ₹410 Feb. Exact & phrase search on professional hair care."],
        ["G_SRC_BOF_Brand_FABB6_Exact", "BOF (Brand)", "7% (₹4.06L)", "₹1.12L (₹3,613/d)", "₹1.40L (₹4,516/d)", "₹1.54L (₹5,500/d)", "Target Impression Share ≥ 95% Absolute Top. Defends brand queries against competitors."],
        ["Total Google Ads Portfolio", "Combined", "100% (₹58.00L)", "₹16.00L (₹51,613/d)", "₹20.00L (₹64,516/d)", "₹22.00L (₹78,571/d)", "Target CPA: ₹450 → ₹430 → ₹410 | Target ROAS: 2.25x → 2.57x → 3.00x"]
    ]
    create_styled_table(doc, g_table_data, header_bg="102C57", center_cols=[1, 2], right_cols=[3, 4, 5], col_widths=[1.5, 0.7, 0.8, 1.0, 1.0, 1.0, 1.2])

    add_h2("Merchant Center Product Sync Tool Recommendation: Simprosys Google Shopping Feed")
    add_body("To permanently eliminate wasted spend on 404 broken links (110 broken URLs identified in audit) and out-of-stock products, we recommend deploying Simprosys Google Shopping Feed (Shopify App):")
    add_bullet("Directly syncs Shopify inventory and price updates via Shopify webhooks to Google Content API in minutes. When an item drops to 0 inventory, it is instantly suppressed from Google Shopping and PMax ads, halting click bleed.", bold_prefix="Real-Time Webhook Synchronization: ")
    add_bullet("Continuously validates Shopify product URLs. Inactive, deleted, or draft products are automatically removed from the active feed before Merchant Center disapproves them.", bold_prefix="Automated 404 Broken Link Detection: ")
    add_bullet("Maps Shopify product tags (high_28plus, mid_20_28, EXCLUDE_lowmargin, single_sachet) to custom_label_0 through custom_label_4 for automated campaign bid gating.", bold_prefix="Automated Custom Label & Margin Tagging: ")
    add_bullet("Operational cost is ~$15–$25/month (~₹1,200–₹2,100/mo), paying for itself on day 1 by preventing broken URL waste. Enterprise alternative: Feedonomics for advanced multi-channel rule engines.", bold_prefix="Low Cost & High ROI: ")

    # PAGE 4: META ADS
    add_h1("4. Meta Ads Architecture & Scaling Governance", page_break_before=True)
    add_body("Meta Ads spend (₹33.10 Lakhs total across Q1) is consolidated from fragmented, overlapping campaigns into a streamlined three-tier funnel to eliminate internal auction competition and bring runaway CPMs (+144% under interim agency) back under control:")

    m_table_data = [
        ["Campaign Name", "Funnel Level", "Budget Share", "Dec Spend (Daily)", "Jan Spend (Daily)", "Feb Spend (Daily)", "Audience Targeting & Creative Strategy"],
        ["M_ASC_TOF_MasterProspecting", "TOF (Prospecting)", "70% (₹23.17L)", "₹7.00L (₹22,581/d)", "₹7.70L (₹24,839/d)", "₹8.47L (₹30,250/d)", "Advantage+ Shopping Campaign. Broad open targeting with 10 new UGC problem-solution creator videos. 15% existing customer budget cap; 30-day purchaser exclusion."],
        ["M_CBO_MOF_HeroCombos_Collection", "MOF (Combos)", "15% (₹4.965L)", "₹1.50L (₹4,839/d)", "₹1.65L (₹5,323/d)", "₹1.815L (₹6,482/d)", "Engaged Instagram/FB visitors (past 60d) and 3s+ video viewers. Carousel & collection ads featuring high-value haircare combos (>₹1,200)."],
        ["M_DPA_BOF_DynamicCatalog_7d", "BOF (Retargeting)", "15% (₹4.965L)", "₹1.50L (₹4,839/d)", "₹1.65L (₹5,323/d)", "₹1.815L (₹6,482/d)", "Dynamic Product Ads for ViewContent (3–7d) & AddToCart (3–14d). Strict 30d/180d purchaser exclusions. Frequency capped ≤ 2.2x."],
        ["Total Meta Ads Portfolio", "Combined", "100% (₹33.10L)", "₹10.00L (₹32,258/d)", "₹11.00L (₹35,484/d)", "₹12.10L (₹43,214/d)", "Target CPA: ₹450 → ₹410 → ₹385 | Target ROAS: 2.25x → 2.69x → 3.20x"]
    ]
    create_styled_table(doc, m_table_data, header_bg="102C57", center_cols=[1, 2], right_cols=[3, 4, 5], col_widths=[1.5, 0.7, 0.8, 1.0, 1.0, 1.2])

    add_h2("Three-Tier Scaling Decision Governance (Weekly Performance Gates)")
    add_body("Budget scaling from December to January and February is strictly governed by trailing 7-day verified store performance:")
    add_bullet("Trailing 7-day confirmed Gross ROAS ≥ 2.50x AND blended CPA within target (Dec ≤ ₹450, Jan ≤ ₹425, Feb ≤ ₹405). Approve scheduled monthly budget increase, capped at ≤ 20% every 72 hours per campaign.", bold_prefix="Green Light (Scale): ")
    add_bullet("Trailing 7-day Gross ROAS between 2.30x and 2.50x. Hold daily budgets completely flat. Analyze SKU-level contribution, rotate creative fatigue, and allow Smart Bidding algorithms to consolidate.", bold_prefix="Yellow Light (Hold): ")
    add_bullet("Trailing 7-day Gross ROAS < 2.30x for 7 consecutive days (or blended CPA exceeds target by >25%). Immediately roll back the last budget increase by 20% and pause any underperforming ad set.", bold_prefix="Red Light (Rollback): ")

    # PAGE 5: DAILY BUDGET SCHEDULES
    add_h1("5. Daily Budget Schedules & Measurement Definitions", page_break_before=True)
    add_body("The schedules below provide the exact campaign-level daily budgets for Plan 2 (Recommended Plan) across December, January (two-step Google pacing to respect ≤ 20% scaling), and February (phased):")

    daily_rec_table = [
        ["Channel", "Campaign Name / Architecture Node", "Funnel Node", "Dec Daily (₹26.0L)", "Jan 1–10 Daily", "Jan 11–31 Daily", "Feb 1–14 Daily", "Feb 15–28 Daily"],
        ["Google Ads", "G_PMAX_BOF_HighMargin_Heroes", "BOF (Heroes 60%)", "₹30,968 / day", "₹34,800 / day", "₹40,571 / day", "₹44,400 / day", "₹49,886 / day"],
        ["Google Ads", "G_PMAX_BOF_CoreVolume_Tier2", "BOF (Core 20%)", "₹10,323 / day", "₹11,600 / day", "₹13,524 / day", "₹14,800 / day", "₹16,629 / day"],
        ["Google Ads", "G_SRC_MOF_Category_HairCare", "MOF (Category 13%)", "₹6,710 / day", "₹7,540 / day", "₹8,790 / day", "₹9,620 / day", "₹10,809 / day"],
        ["Google Ads", "G_SRC_BOF_Brand_FABB6_Exact", "BOF (Brand 7%)", "₹3,613 / day", "₹4,060 / day", "₹4,733 / day", "₹5,180 / day", "₹5,820 / day"],
        ["Google Total", "Combined Google Ads (61.5% / 64.5%)", "Google Portfolio", "₹51,613 / day", "₹58,000 / day", "₹67,619 / day", "₹74,000 / day", "₹83,143 / day"],
        ["Meta Ads", "M_ASC_TOF_MasterProspecting", "TOF (ASC 70%)", "₹22,581 / day", "₹24,839 / day", "₹24,839 / day", "₹28,000 / day", "₹32,500 / day"],
        ["Meta Ads", "M_CBO_MOF_HeroCombos_Collection", "MOF (Combos 15%)", "₹4,839 / day", "₹5,323 / day", "₹5,323 / day", "₹6,000 / day", "₹6,964 / day"],
        ["Meta Ads", "M_DPA_BOF_DynamicCatalog_7d", "BOF (DPA 15%)", "₹4,839 / day", "₹5,323 / day", "₹5,323 / day", "₹6,000 / day", "₹6,964 / day"],
        ["Meta Total", "Combined Meta Ads (38.5% / 35.5%)", "Meta Portfolio", "₹32,258 / day", "₹35,484 / day", "₹35,484 / day", "₹40,000 / day", "₹46,429 / day"],
        ["Total Media", "Combined Account Daily Spend", "Full Account", "₹83,871 / day", "₹93,484 / day", "₹103,103 / day", "₹114,000 / day", "₹129,571 / day"]
    ]
    create_styled_table(doc, daily_rec_table, header_bg="102C57", center_cols=[0, 2], right_cols=[3, 4, 5, 6, 7], col_widths=[0.8, 1.8, 1.0, 0.8, 0.8, 0.8, 0.8, 0.8])

    add_h2("Operational Measurement Definitions & KPI Hierarchy")
    add_bullet("Total confirmed sales revenue recorded in Shopify before cancellations, discounts and returns. Primary top-line metric evaluated weekly.", bold_prefix="Gross Sales Revenue: ")
    add_bullet("Total Gross Sales Revenue divided by total ad spend. Account targets: 3.46x Dec, 3.79x Jan, 4.35x Feb (3.91x Q1 blended).", bold_prefix="Shopify Gross ROAS: ")
    add_bullet("Total media spend divided by total Shopify store orders (₹293 Dec, ₹291 Jan, ₹283 Feb; Q1 avg ₹288.53). Primary governing business unit metric.", bold_prefix="Spend per Store Order (Blended CPA): ")
    add_bullet("Ad spend divided by platform-reported orders (Google ₹450 → ₹410, Meta ₹450 → ₹385; Q1 avg ₹421.35). Operational secondary guardrail.", bold_prefix="Platform Paid CPA: ")
    add_bullet("Target cost ceilings entered in campaign bid settings (Search tCPA ₹410–₹450, Meta Cost Cap ₹385–₹450).", bold_prefix="Bidding CPA Ceilings: ")
    add_bullet("Daily tracking snapshot via Slack/WhatsApp, weekly gate reviews, and monthly Shopify financial reconciliation.", bold_prefix="Agency Cadence: ")

    os.makedirs(os.path.dirname(docx_path), exist_ok=True)
    doc.save(docx_path)
    print(f"Successfully generated strategy DOCX at: {docx_path}")

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
    t_docx = r"C:\Users\test\Videos\Office\reports\test_gokwik.docx"
    t_pdf = r"C:\Users\test\Videos\Office\reports\test_gokwik.pdf"
    test_build(t_docx)
    convert_docx_to_pdf(t_docx, t_pdf)
    reader = pypdf.PdfReader(t_pdf)
    print(f"RESULTING PDF PAGE COUNT: {len(reader.pages)}")
