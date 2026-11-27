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

def set_cell_margins(cell, top=16, bottom=16, left=24, right=24):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_styled_table(doc, data, header_bg="102C57", zebra=True, center_cols=[], right_cols=[], col_widths=None, font_size=6.5, header_size=6.8):
    table = doc.add_table(rows=len(data), cols=len(data[0]))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False

    tblPr = table._tbl.tblPr
    tblBorders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="D9D9D9"/>'
        f'<w:bottom w:val="single" w:sz="6" w:space="0" w:color="102C57"/>'
        f'<w:insideH w:val="single" w:sz="4" w:space="0" w:color="E0E0E0"/>'
        f'<w:insideV w:val="none"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(tblBorders)

    for row_idx, row_data in enumerate(data):
        row = table.rows[row_idx]
        is_header = (row_idx == 0)
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        if is_header:
            trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

        for col_idx, cell_value in enumerate(row_data):
            cell = row.cells[col_idx]
            cell.text = str(cell_value)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0.8)
            p.paragraph_format.space_after = Pt(0.8)
            p.paragraph_format.line_spacing = 1.0

            if col_idx in center_cols:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif col_idx in right_cols:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT

            for run in p.runs:
                run.font.name = "Calibri"
                if is_header:
                    run.font.bold = True
                    run.font.size = Pt(header_size)
                    run.font.color.rgb = RGBColor(255, 255, 255)
                else:
                    is_bold = (col_idx in [0, len(row_data)-1] or any(k in str(row_data[0]) for k in ["Total", "3-Month", "Upper", "Plan", "Provable", "Central"]))
                    run.font.bold = is_bold
                    run.font.size = Pt(font_size)
                    run.font.color.rgb = RGBColor(16, 44, 87) if is_bold and "Total" in str(row_data[0]) else RGBColor(30, 30, 30)

            if is_header:
                set_cell_background(cell, header_bg)
            elif "Total" in str(row_data[0]) or "3-Month" in str(row_data[0]):
                set_cell_background(cell, "EAECEE")
            elif zebra and row_idx % 2 == 1:
                set_cell_background(cell, "F7F9FC")
            else:
                set_cell_background(cell, "FFFFFF")

            set_cell_margins(cell, top=14, bottom=14, left=20, right=20)

    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)

    return table

def add_h1(doc, text, space_before=4.0, space_after=1.5):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(space_before)
    h.paragraph_format.space_after = Pt(space_after)
    h.paragraph_format.keep_with_next = True
    r = h.add_run(text)
    r.font.name = "Georgia"
    r.font.size = Pt(11.0)
    r.font.bold = True
    r.font.color.rgb = RGBColor(16, 44, 87)
    return h

def add_h2(doc, text, space_before=3.0, space_after=1.0):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(space_before)
    h.paragraph_format.space_after = Pt(space_after)
    h.paragraph_format.keep_with_next = True
    r = h.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(8.8)
    r.font.bold = True
    r.font.color.rgb = RGBColor(31, 78, 120)
    return h

def add_body(doc, text, bold_prefix="", space_after=1.5, font_size=7.2):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.04
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.name = "Calibri"
        rb.font.size = Pt(font_size)
        rb.font.bold = True
        rb.font.color.rgb = RGBColor(20, 20, 20)
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(font_size)
    r.font.color.rgb = RGBColor(40, 40, 40)
    return p

def add_bullet(doc, text, bold_prefix="", space_after=1.2, font_size=7.2):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.04
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.name = "Calibri"
        rb.font.size = Pt(font_size)
        rb.font.bold = True
        rb.font.color.rgb = RGBColor(20, 20, 20)
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(font_size)
    r.font.color.rgb = RGBColor(40, 40, 40)
    return p

def build_proposal_document(docx_path):
    doc = docx.Document()
    
    # Configure 0.52" margins for perfect fit
    for s in doc.sections:
        s.top_margin = Inches(0.52)
        s.bottom_margin = Inches(0.52)
        s.left_margin = Inches(0.60)
        s.right_margin = Inches(0.60)
        
        # Header setup
        header = s.header
        hp = header.paragraphs[0]
        hp.text = "FABB6 | Performance Marketing Strategy & Campaign Architecture (Dec 2026 – Feb 2027)"
        hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in hp.runs:
            run.font.name = "Calibri"
            run.font.size = Pt(7.0)
            run.font.color.rgb = RGBColor(128, 128, 128)

        # Footer setup
        footer = s.footer
        fp = footer.paragraphs[0]
        fp.text = "Confidential · Prepared by Techno Exponent for FABB6 (Glanzzkart Pvt Ltd) · Page "
        fp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in fp.runs:
            run.font.name = "Calibri"
            run.font.size = Pt(7.0)
            run.font.color.rgb = RGBColor(128, 128, 128)

    # =========================================================================
    # PAGE 1: Title, Executive Summary & 3 Strategic Plans
    # =========================================================================
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    r_t = p_title.add_run("FABB6 Performance Marketing Strategy\n& Campaign Architecture")
    r_t.font.name = "Georgia"
    r_t.font.size = Pt(17.0)
    r_t.font.bold = True
    r_t.font.color.rgb = RGBColor(16, 44, 87)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(3)
    r_sub = p_sub.add_run("Funnel-Wise Architecture, Monthly Budget Schedules & Unit Economics Blueprint")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(9.2)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(41, 128, 185)

    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(0)
    p_meta.paragraph_format.space_after = Pt(4)
    r_meta = p_meta.add_run("Prepared for FABB6 (Glanzzkart Private Limited) · Planning Horizon: Dec 2026 – Feb 2027 · Governance Framework\nPrepared by Sarnendu Patra, Head of Marketing, Techno Exponent · Includes Performance Audit, SEO, AEO, GEO, SMO and CRO plans")
    r_meta.font.name = "Calibri"
    r_meta.font.size = Pt(7.0)
    r_meta.font.color.rgb = RGBColor(100, 100, 100)

    add_h1(doc, "1. Executive Summary & Three Strategic Plans", space_before=2.0)
    add_body(doc, "This master document sets out the turnaround strategy and campaign architecture for FABB6 across Google Ads, Meta Ads, and owned channels. All performance accounting is standardized on Gross Sales Revenue (pre-discount, pre-return sales value), properly isolating marketing efficiency from company-side commercial deductions. Following the forensic audit of historical performance, we present three distinct, reconciled operating scenarios:")

    # Plan 1 Table
    add_h2(doc, "Plan 1: Base / Recommended (Baseline Turnaround — ₹105.00L Total Spend)", space_before=2.0)
    p1_data = [
        ["Month", "Media Spend", "Google / Meta Split", "Paid Orders", "Organic*", "Others*", "Store Orders", "Gross Sales", "Store ROAS", "Blended CPA"],
        ["Dec 2026", "₹30.00L", "₹19.0L / ₹11.0L", "5,455", "1,650", "1,700", "8,805", "₹115.25L", "3.84x", "₹340.73"],
        ["Jan 2027", "₹35.00L", "₹22.0L / ₹13.0L", "6,667", "1,650", "1,870", "10,187", "₹142.61L", "4.07x", "₹343.59"],
        ["Feb 2027", "₹40.00L", "₹25.0L / ₹15.0L", "8,000", "1,650", "2,057", "11,707", "₹175.61L", "4.39x", "₹341.68"]
    ]
    create_styled_table(doc, p1_data, header_bg="102C57", center_cols=[0, 2], right_cols=[1, 3, 4, 5, 6, 7, 8, 9], col_widths=[0.65, 0.70, 1.05, 0.65, 0.55, 0.55, 0.65, 1.10, 0.60, 0.65], font_size=6.2, header_size=6.5)

    # Plan 2 Table
    add_h2(doc, "Plan 2: Moderate (Accelerated Scale — ₹122.00L Total Spend)", space_before=2.5)
    p2_data = [
        ["Month", "Media Spend", "Google / Meta Split", "Paid Orders", "Organic*", "Others*", "Store Orders", "Gross Sales", "Store ROAS", "Blended CPA"],
        ["Dec 2026", "₹35.00L", "₹22.0L / ₹13.0L", "6,364", "1,650", "1,700", "9,714", "₹127.15L", "3.63x", "₹360.32"],
        ["Jan 2027", "₹41.00L", "₹26.0L / ₹15.0L", "7,810", "1,650", "1,870", "11,330", "₹158.61L", "3.87x", "₹361.89"],
        ["Feb 2027", "₹46.00L", "₹29.0L / ₹17.0L", "9,200", "1,650", "2,057", "12,907", "₹193.61L", "4.21x", "₹356.40"]
    ]
    create_styled_table(doc, p2_data, header_bg="1F4E78", center_cols=[0, 2], right_cols=[1, 3, 4, 5, 6, 7, 8, 9], col_widths=[0.65, 0.70, 1.05, 0.65, 0.55, 0.55, 0.65, 1.10, 0.60, 0.65], font_size=6.2, header_size=6.5)

    # Plan 3 Table
    add_h2(doc, "Plan 3: Aggressive (Market Dominance — ₹141.00L Total Spend)", space_before=2.5)
    p3_data = [
        ["Month", "Media Spend", "Google / Meta Split", "Paid Orders", "Organic*", "Others*", "Store Orders", "Gross Sales", "Store ROAS", "Blended CPA"],
        ["Dec 2026", "₹40.00L", "₹25.0L / ₹15.0L", "7,273", "1,650", "1,700", "10,623", "₹139.05L", "3.48x", "₹376.55"],
        ["Jan 2027", "₹47.00L", "₹30.0L / ₹17.0L", "8,952", "1,650", "1,870", "12,472", "₹174.61L", "3.72x", "₹376.83"],
        ["Feb 2027", "₹54.00L", "₹34.0L / ₹20.0L", "10,800", "1,650", "2,057", "14,507", "₹217.61L", "4.03x", "₹372.23"]
    ]
    create_styled_table(doc, p3_data, header_bg="2C3E50", center_cols=[0, 2], right_cols=[1, 3, 4, 5, 6, 7, 8, 9], col_widths=[0.65, 0.70, 1.05, 0.65, 0.55, 0.55, 0.65, 1.10, 0.60, 0.65], font_size=6.2, header_size=6.5)

    add_body(doc, "*Organic represents natural SEO demand (modeled at 1,650 orders/month based on client-provided figures, as historical organic volumes could not be independently verified from past tracking). Others represents repeat customer purchases, automated WhatsApp/email replenishment flows, and GoKwik cart recovery (1,700 in Dec growing +10% monthly to 1,870 and 2,057).", space_after=1.0, font_size=6.5)

    add_bullet(doc, "Average Order Value (AOV) expands from ₹1,309 in December (anchored on November 2026 actual of ₹1,309.12) to ₹1,400 in January and ₹1,500 in February via combo kits and ₹999 free shipping.", bold_prefix="AOV Expansion: ")
    add_bullet(doc, "Spend is balanced at ~63% Google Ads (capturing high-intent professional salon search demand) and ~37% Meta Ads (prospecting via ASC and DPA catalog remarketing).", bold_prefix="Channel Balance: ")
    add_bullet(doc, "Automated retention software incurs ~₹35,000–₹50,000/month in tooling costs but requires zero incremental media spend, unlocking 5,627 high-margin repeat orders.", bold_prefix="Zero-Media-Cost Retention: ")

    doc.add_page_break()

    # =========================================================================
    # PAGE 2: Unit Economics, Checkout Optimization & Retention Strategy
    # =========================================================================
    add_h1(doc, "2. Unit Economics, Checkout Optimization & Retention Strategy")
    add_body(doc, "To establish absolute commercial clarity, this strategy articulates the exact contribution economics of FABB6's business model as an authorized multi-brand distributor for salon-grade professional haircare (L'Oréal Professionnel, Matrix, Schwarzkopf, Floractive, Raaga). Products carry an average gross trade margin of ~25% on ex-GST wholesale value. With 18% GST included in retail selling prices, mathematical media break-even requires a 4.00x ROAS on ex-GST revenue (1 ÷ 0.25) and a 4.72x ROAS on total GST-inclusive sales receipts (4.00x × 1.18).")

    add_h2(doc, "Front-End Acquisition vs. Back-End Lifetime Contribution")
    add_body(doc, "At a planned front-end Paid ROAS of 2.38x to 3.00x (averaging 2.71x across Q1), cold media acquisition is designed to operate near product break-even on first orders. True commercial profitability is unlocked through non-paid organic volume and back-end replenishment cycles. Because professional salon treatments require ongoing replenishment (every 30 to 60 days), customer lifetime value (LTV) recovers initial acquisition investments without incurring additional ad spend.")

    add_h2(doc, "GoKwik Checkout Optimization & Cart Abandonment Recovery")
    add_body(doc, "Industry data reveals that beauty and personal care e-commerce suffers from 68%–72% cart abandonment, exacerbated in India by complex multi-step checkouts and high Cash on Delivery (COD) Return-to-Origin (RTO) rates. To plug this severe revenue leak, FABB6 will integrate GoKwik checkout infrastructure:")
    add_bullet(doc, "One-click checkout pre-filling addresses and phone numbers for over 100M Indian online shoppers across the GoKwik network, reducing checkout friction and increasing conversion by 20%–30%.", bold_prefix="1-Click Express Checkout: ")
    add_bullet(doc, "Machine learning algorithms assign real-time fraud and RTO risk scores, restricting COD for chronic returners and offering dynamic UPI discounts (e.g. ₹50 off prepaid) to drive prepaid conversion above 65%.", bold_prefix="RTO Intelligence Engine: ")
    add_bullet(doc, "Automated WhatsApp and SMS reminders triggered within 15 minutes of checkout drop-off, offering instant 1-click cart recovery links and personalized incentives to recover 12%–18% of abandoned carts.", bold_prefix="Automated Abandonment Recovery: ")

    add_h2(doc, "Low-Cost Retention Channel Architecture (Zero Incremental Media Spend)")
    add_body(doc, "Repeat retention is driven primarily by automated WhatsApp and email replenishment workflows timed to hair spa, shampoo, and color usage cycles (30, 45, and 60 days). While retention software and messaging incurs operational costs (~₹35,000–₹50,000/month), it requires zero incremental media spend. This retention engine unlocks the 5,627 'Orders from Others' in Plan 1 and elevates account efficiency from a 2.71x paid ROAS to a 4.13x blended store ROAS:")

    ret_table_data = [
        ["Workflow / Trigger Stage", "Timing Window", "Primary Channel", "Target Product Category", "Replenishment Trigger & Offer Architecture"],
        ["W1: Core Shampoo & Conditioner", "Day 25 – 35", "WhatsApp Interactive Flow + Email", "L'Oréal, Matrix, Schwarzkopf Care", "Automated usage check-in; 1-click re-order with 5% replenishment loyalty discount."],
        ["W2: Hair Spa & Intensive Masques", "Day 40 – 50", "WhatsApp Catalog + RCS Message", "L'Oréal Deep Nourish, Matrix Masque", "Reminder that 500g tubs reach half-volume; salon combo upsell (Serum + Masque)."],
        ["W3: Salon Pro & Chemical Treatments", "Day 60 – 75", "Email VIP Concierge + WhatsApp", "Floractive Nanoplastia, Raaga De-Tan", "Professional salon replenishment cadence; bulk volume tier pricing for repeat buyers."],
        ["W4: VIP Retention & Cross-Sell", "Day 90+", "Automated SMS / WhatsApp Template", "Cross-Category Beauty / Skincare", "Exclusive early access to seasonal combo kits; dynamic store credit balance alerts."]
    ]
    create_styled_table(doc, ret_table_data, header_bg="102C57", center_cols=[1, 2], right_cols=[], col_widths=[1.5, 0.9, 1.4, 1.4, 2.0], font_size=6.2, header_size=6.5)

    doc.add_page_break()

    # =========================================================================
    # PAGE 3: Google Ads Architecture & Catalog Sync Tooling
    # =========================================================================
    add_h1(doc, "3. Google Ads Architecture & Catalog Sync Tooling")
    add_body(doc, "Google Ads spend (December ₹19.00L, January ₹22.00L, February ₹25.00L) is allocated across high-margin Performance Max campaigns and high-intent Search campaigns to protect branded traffic and scale profitable professional salon hair care. Google Ads accounts for ~63% of the total paid acquisition budget across all plans.")

    g_table_data = [
        ["Campaign Name", "Funnel Level", "Budget Share", "Dec Spend (Daily)", "Jan Spend (Daily)", "Feb Spend (Daily)", "Target ROAS / CPA Guardrail"],
        ["G_PMAX_Hero_HighMargin", "BOF / Growth", "45%", "₹27,581 (₹8.55L)", "₹31,935 (₹9.90L)", "₹40,179 (₹11.25L)", "ROAS ≥ 2.80x (CPA ≤ ₹460)"],
        ["G_SRC_Brand_Protection", "BOF / Capture", "15%", "₹9,194 (₹2.85L)", "₹10,645 (₹3.30L)", "₹13,393 (₹3.75L)", "ROAS ≥ 4.50x (CPA ≤ ₹290)"],
        ["G_SRC_MOF_Category_HairCare", "MOF / Intent", "25%", "₹15,323 (₹4.75L)", "₹17,742 (₹5.50L)", "₹22,321 (₹6.25L)", "ROAS ≥ 2.20x (CPA ≤ ₹590)"],
        ["G_SRC_CatchAll_DSA", "TOF / Discovery", "15%", "₹9,194 (₹2.85L)", "₹10,645 (₹3.30L)", "₹13,393 (₹3.75L)", "ROAS ≥ 2.00x (CPA ≤ ₹650)"],
        ["Total Google Ads Program", "Full Funnel", "100%", "₹61,290 (₹19.00L)", "₹70,968 (₹22.00L)", "₹89,286 (₹25.00L)", "Blended ROAS ≥ 2.38x → 3.00x"]
    ]
    create_styled_table(doc, g_table_data, header_bg="102C57", center_cols=[1, 2], right_cols=[3, 4, 5, 6], col_widths=[1.8, 0.9, 0.7, 1.0, 1.0, 1.0, 1.3], font_size=6.2, header_size=6.5)

    add_h2(doc, "Automated Product Sync Management Tooling (Eliminating 404 & OOS Waste)")
    add_body(doc, "A critical finding of the forensic audit was the persistent drain of ad spend on out-of-stock SKUs and dead 404 landing pages (~₹80,285 in avoidable spend). When products sell out in Shopify, standard Merchant Center feeds experience a 24- to 48-hour synchronization lag, causing Google Ads to continue bidding aggressively on unavailable items. To permanently resolve this, we mandate integrating an automated Google Merchant Center feed management tool:")
    add_bullet(doc, "Provides real-time inventory webhooks between Shopify and Merchant Center, automatically pausing shopping ads within 15 minutes of inventory dropping to zero.", bold_prefix="Instant Out-of-Stock Suppression: ")
    add_bullet(doc, "Automated URL crawler pings all product landing pages daily, immediately disapproving any link returning a 404 error before ad budget is wasted on broken pages.", bold_prefix="Automated 404 Error Quarantine: ")
    add_bullet(doc, "Automatically enriches feed titles with salon-grade keywords (e.g. 'L'Oréal Serie Expert Absolut Repair Shampoo 300ml - Salon Professional Haircare') and injects custom margin labels (custom_label_0: margin_high_28plus, custom_label_1: best_seller) to guide Performance Max bidding toward high-margin hero inventory.", bold_prefix="Dynamic Custom Label Segmentation: ")

    add_h2(doc, "Implementation Details: Search Hygiene & Structure")
    add_bullet(doc, "Exact and phrase match on 'FABB6', 'Fabb 6', 'Glanzzkart'. Prevents competitor poaching and guarantees #1 SERP presence at minimal CPC (₹3–₹8).", bold_prefix="Branded Search Protection: ")
    add_bullet(doc, "The audit revealed heavy budget leakage on unbranded junk terms ('hair cutting style', 'free shampoo sample'). Negative keyword lists containing 750+ verified non-converting search terms will be applied account-wide on Day 1.", bold_prefix="Account-Wide Negative Hygiene: ")
    add_bullet(doc, "Restricted to curated collection URLs only. Product pages are explicitly excluded from DSA auto-targets to prevent bidding on low-margin single items.", bold_prefix="DSA Targeting Guardrails: ")

    doc.add_page_break()

    # =========================================================================
    # PAGE 4: Meta Ads Architecture & Scaling Governance
    # =========================================================================
    add_h1(doc, "4. Meta Ads Architecture & Scaling Governance")
    add_body(doc, "Meta Ads spend (December ₹11.00L, January ₹13.00L, February ₹15.00L) is consolidated from fragmented, overlapping campaigns into a streamlined three-tier funnel to eliminate internal auction competition and bring runaway CPMs (+144% between August and November 2026) back under control. Meta accounts for ~37% of the total media spend:")

    m_table_data = [
        ["Campaign Name", "Funnel Level", "Budget Share", "Dec Spend (Daily)", "Jan Spend (Daily)", "Feb Spend (Daily)", "Audience Targeting & Creative Strategy"],
        ["M_TOF_ASC_Prospecting", "TOF / Cold", "50%", "₹17,742 (₹5.50L)", "₹20,968 (₹6.50L)", "₹26,786 (₹7.50L)", "Advantage+ Shopping Campaign; broad targeting (India, 21-50); video reels, static value hooks."],
        ["M_MOF_Social_Engagers", "MOF / Warm", "25%", "₹8,871 (₹2.75L)", "₹10,484 (₹3.25L)", "₹13,393 (₹3.75L)", "Engaged with IG/FB 90d, video viewers 50%+; salon comparison carousels, routine guides."],
        ["M_BOF_DPA_Catalog_Retarget", "BOF / Hot", "25%", "₹8,871 (₹2.75L)", "₹10,484 (₹3.25L)", "₹13,393 (₹3.75L)", "Catalog Dynamic Product Ads; viewed content/add to cart 7d; excludes 30d purchasers."],
        ["Total Meta Ads Program", "Full Funnel", "100%", "₹35,484 (₹11.00L)", "₹41,935 (₹13.00L)", "₹53,571 (₹15.00L)", "Blended Paid ROAS Target: 2.38x (Dec) → 2.67x (Jan) → 3.00x (Feb)"]
    ]
    create_styled_table(doc, m_table_data, header_bg="102C57", center_cols=[1, 2], right_cols=[3, 4, 5], col_widths=[1.8, 0.8, 0.7, 1.0, 1.0, 1.0, 1.9], font_size=6.2, header_size=6.5)

    add_h2(doc, "Three-Tier Scaling Decision Governance (Weekly Performance Gates)")
    add_body(doc, "Monthly budget scaling from December to January and February is strictly governed by trailing 7-day verified store performance. Scaling is never automated on platform-reported numbers alone; decisions require dual confirmation from Shopify gross sales:")
    add_bullet(doc, "Trailing 7-day confirmed Gross ROAS ≥ 2.50x AND blended CPA within monthly target (Dec ≤ ₹550, Jan ≤ ₹525, Feb ≤ ₹500). Action: Authorize planned budget scale (+10% to +20% weekly increase), deploying additional capital to winning ASC creatives.", bold_prefix="Green Light (Scale): ")
    add_bullet(doc, "Trailing 7-day Gross ROAS between 2.30x and 2.50x OR blended CPA exceeds monthly target by 5%–15%. Action: Freeze spend at current daily run-rate; reallocate budget from underperforming ad sets to top-performing hero SKU campaigns; refresh creative fatigue backlog.", bold_prefix="Yellow Light (Hold & Optimize): ")
    add_bullet(doc, "Trailing 7-day Gross ROAS < 2.30x OR blended CPA exceeds monthly target by > 15%. Action: Mandatory circuit breaker activated. Reduce daily spend by 15%–20% across prospecting campaigns; pause bleeding ad sets; audit Shopify conversion funnel and inventory availability.", bold_prefix="Red Light (Circuit Breaker): ")

    add_h2(doc, "Audience Hygiene & Campaign Consolidation Rules")
    add_bullet(doc, "All cold prospecting campaigns (ASC and MOF) must maintain an active, dynamic exclusion of 30-day purchasers and customer email lists. Retargeting past buyers in cold auctions was a primary driver of October's inflated CPM (₹104.17).", bold_prefix="Universal Purchaser Exclusion: ")
    add_bullet(doc, "Consolidate 12 fragmented campaigns into 3 core architecture nodes. Eliminates internal self-competition in Meta auctions, reduces ad delivery overlap, and accelerates exit from the 50-conversion learning phase.", bold_prefix="Elimination of Internal Bidding Wars: ")

    doc.add_page_break()

    # =========================================================================
    # PAGE 5: Daily Budget Schedules & Measurement Definitions
    # =========================================================================
    add_h1(doc, "5. Daily Budget Schedules & Measurement Definitions")
    add_body(doc, "The schedules below provide the exact campaign-level daily budgets for Plan 1 (Recommended Plan) across all 90 days of Q1. Daily pacing is managed against calendar month day counts:")

    sched_data = [
        ["Channel", "Campaign Architecture Node", "Funnel Level", "Dec Daily (31 Days) [₹30.0L]", "Jan Daily (31 Days) [₹35.0L]", "Feb Daily (28 Days) [₹40.0L]", "Allocation %"],
        ["Google Ads", "G_PMAX_Hero_HighMargin", "BOF / Growth", "₹27,581 / day", "₹31,935 / day", "₹40,179 / day", "45% of Google (28.4% total)"],
        ["Google Ads", "G_SRC_Brand_Protection", "BOF / Capture", "₹9,194 / day", "₹10,645 / day", "₹13,393 / day", "15% of Google (9.5% total)"],
        ["Google Ads", "G_SRC_MOF_Category_HairCare", "MOF / Intent", "₹15,323 / day", "₹17,742 / day", "₹22,321 / day", "25% of Google (15.8% total)"],
        ["Google Ads", "G_SRC_CatchAll_DSA", "TOF / Discovery", "₹9,194 / day", "₹10,645 / day", "₹13,393 / day", "15% of Google (9.5% total)"],
        ["Subtotal", "Google Ads Total", "Channel Total", "₹61,290 / day (₹19.0L)", "₹70,968 / day (₹22.0L)", "₹89,286 / day (₹25.0L)", "63.2% – 62.5% of Media Spend"],
        ["Meta Ads", "M_TOF_ASC_Prospecting", "TOF / Cold", "₹17,742 / day", "₹20,968 / day", "₹26,786 / day", "50% of Meta (18.4% total)"],
        ["Meta Ads", "M_MOF_Social_Engagers", "MOF / Warm", "₹8,871 / day", "₹10,484 / day", "₹13,393 / day", "25% of Meta (9.2% total)"],
        ["Meta Ads", "M_BOF_DPA_Catalog_Retarget", "BOF / Hot", "₹8,871 / day", "₹10,484 / day", "₹13,393 / day", "25% of Meta (9.2% total)"],
        ["Subtotal", "Meta Ads Total", "Channel Total", "₹35,484 / day (₹11.0L)", "₹41,935 / day (₹13.0L)", "₹53,571 / day (₹15.0L)", "36.8% – 37.5% of Media Spend"],
        ["Store Total", "Total Performance Marketing", "Combined Media", "₹96,774 / day (₹30.0L)", "₹1,12,903 / day (₹35.0L)", "₹1,42,857 / day (₹40.0L)", "100.0% (₹105.00L Total Spend)"]
    ]
    create_styled_table(doc, sched_data, header_bg="102C57", center_cols=[0, 2], right_cols=[3, 4, 5, 6], col_widths=[0.8, 1.8, 0.8, 1.1, 1.1, 1.1, 1.3], font_size=6.0, header_size=6.3)

    add_h2(doc, "Measurement & Governance Definitions")
    add_bullet(doc, "Total confirmed gross sales value before promo discounts, refunds, and RTO deductions, divided by total Google and Meta ad spend. This is the primary commercial efficiency KPI governing the account.", bold_prefix="Gross Store ROAS: ")
    add_bullet(doc, "Ad-attributed gross revenue divided by direct platform spend. Serves as a channel-level operational diagnostic. Target scales from 2.38x in December to 2.67x in January and 3.00x in February.", bold_prefix="Paid Ads ROAS: ")
    add_bullet(doc, "Total ad spend divided by total Shopify confirmed store orders. Target: ₹340.73 in Dec, ₹343.59 in Jan, and ₹341.68 in Feb under Plan 1.", bold_prefix="Blended Store CPA: ")
    add_bullet(doc, "Direct media spend divided by ad-attributed purchases. Calibrated conservatively at ₹550 in Dec, ₹525 in Jan, and ₹500 in Feb across Google and Meta.", bold_prefix="Platform Paid CPA: ")
    add_bullet(doc, "Orders generated without direct incremental media spend, comprising Organic SEO search (1,650/month) and Others (1,700 → 1,870 → 2,057 repeat, WhatsApp, and GoKwik cart recovery).", bold_prefix="Non-Paid Orders (Organic + Others): ")

    doc.add_page_break()

    # =========================================================================
    # PAGE 6: Performance Audit Report & 12-Month Gross Reconciliation
    # =========================================================================
    add_h1(doc, "6. Performance Audit Report")
    add_h2(doc, "6.1 Executive Summary of the Audit")
    add_body(doc, "This section audits Google Ads and Meta Ads performance from December 2025 to November 2026, examining account changes, tracking disruptions, and cost inflation. All revenue metrics have been updated and verified against raw Shopify order data, standardizing on Gross Sales Revenue (sum of line items before discounts, returns, and cancellations):")

    add_h2(doc, "6.2 Twelve-Month Historical Performance Reconciliation (Shopify Gross Sales Basis)")
    add_body(doc, "The table below reconciles all twelve historical operating months. Every order count represents confirmed total placed store orders, and Gross Sales reflects total top-line merchandise value created before commercial deductions:")

    audit_table_data = [
        ["Month", "Total Media Spend", "Paid Orders", "Paid CPA", "Store Orders", "Gross Sales", "Store ROAS", "Gross AOV"],
        ["Dec 2025", "₹4.21L", "1,614", "₹260.69", "3,307", "₹29.51L", "7.01x", "₹892.35"],
        ["Jan 2026", "₹12.17L", "4,260", "₹285.57", "7,850", "₹66.14L", "5.44x", "₹842.49"],
        ["Feb 2026", "₹17.97L", "4,817", "₹373.05", "8,250", "₹76.11L", "4.24x", "₹922.49"],
        ["Mar 2026", "₹27.84L", "6,351", "₹438.37", "11,285", "₹101.05L", "3.63x", "₹895.44"],
        ["Apr 2026", "₹32.55L", "5,350", "₹608.45", "10,591", "₹100.32L", "3.08x", "₹947.24"],
        ["May 2026", "₹40.21L", "7,076", "₹568.30", "12,215", "₹119.57L", "2.97x", "₹978.85"],
        ["Jun 2026", "₹42.86L", "6,851", "₹625.67", "12,877", "₹122.87L", "2.87x", "₹954.18"],
        ["Jul 2026", "₹43.62L", "8,313", "₹524.75", "13,420", "₹122.31L", "2.80x", "₹911.43"],
        ["Aug 2026", "₹47.91L", "10,965", "₹436.95", "11,069", "₹111.20L", "2.32x", "₹1,004.62"],
        ["Sep 2026", "₹6.27L", "801", "₹782.84", "3,112", "₹41.47L", "6.61x", "₹1,332.73"],
        ["Oct 2026", "₹42.47L", "8,948", "₹474.58", "9,143", "₹120.93L", "2.85x", "₹1,322.70"],
        ["Nov 2026*", "₹20.78L", "4,538", "₹457.95", "6,061", "₹79.35L", "3.82x", "₹1,309.12"]
    ]
    create_styled_table(doc, audit_table_data, header_bg="102C57", center_cols=[0], right_cols=[1, 2, 3, 4, 5, 6, 7], col_widths=[0.80, 0.90, 0.80, 0.85, 0.85, 1.05, 0.85, 0.95], font_size=6.2, header_size=6.5)

    add_body(doc, "*November 2026 figures reflect actual MTD performance through 24 November (6,061 orders, ₹79.35L gross sales, ₹1,309.12 AOV). In the audit cutoff through 18 November, spend was ₹19.09L across 4,736 orders and ₹61.98L gross sales.", space_after=1.0, font_size=6.2)

    add_bullet(doc, "On a Gross Sales basis, August generated ₹111.20L and October reached a record ₹120.93L. Shifting to Gross Sales properly recognizes total top-line ad generation value created before company-side cancellations, returns, and promo discounts.", bold_prefix="Gross Sales Accounting Impact: ")
    add_bullet(doc, "Gross AOV hovered between ₹842 and ₹1,005 through August 2026, then surged to ₹1,332 in September, ₹1,323 in October, and ₹1,309 in November (+31% increase), providing strong empirical proof for Q1's planned AOV expansion.", bold_prefix="AOV Surge Validation: ")

    doc.add_page_break()

    # =========================================================================
    # PAGE 7: Audit Observations, Google Ads Audit & Meta Ads Audit
    # =========================================================================
    add_h2(doc, "Three observations that shape the plan", space_before=2.0)
    add_bullet(doc, "From December 2025 to August 2026, spend grew more than tenfold and Gross Store ROAS adjusted from 7.01x to 2.32x. Some decline is the normal cost of scaling into colder audiences, and we treat 2.5x–3.5x as the realistic operating baseline for ₹30–45 Lakhs of monthly spend.", bold_prefix="1. Efficiency adjusted as spend scaled: ", space_after=0.8, font_size=6.7)
    add_bullet(doc, "Spend was cut by 87% due to campaign pauses and verification delays, so the 6.61x ratio reflects natural organic and repeat demand that continued without ad spend; it did not represent genuine operational efficiency.", bold_prefix="2. September was not an efficiency gain: ", space_after=0.8, font_size=6.7)
    add_bullet(doc, "April (₹608) and June (₹626) were higher. October ROAS (2.85x) and November (3.82x) were well above August (2.32x), driven by strong order values (₹1,320+ AOV).", bold_prefix="3. October CPA was not a record: ", space_after=0.8, font_size=6.7)
    add_body(doc, "The Festival of Lights (Diwali) fell on 8 November in 2026, so festive demand straddles October and November. The November run-rate includes festive uplift and is not used as an unadjusted December baseline.", space_after=1.5, font_size=6.6)

    add_h1(doc, "6.3 Google Ads Audit", space_before=2.5)
    add_body(doc, "Google Ads spend during the audit period (1 September – 18 November 2026) totaled ₹34.84 Lakhs. Findings from the change history, asset group, product and search term reports:", space_after=1.0, font_size=6.7)
    add_bullet(doc, "The change history shows the 'Purchase-2026' conversion action was deleted by an administrator account (Exhibit A). Smart Bidding lost its main learning signal. September Google spend was ₹3.18 Lakhs for 42 attributed orders (₹7,569 CPA). Because 17 days of the month preceded the deletion and post-deletion sales may be unattributed, the true cost per sale is likely lower than this figure, and we will validate it against Shopify UTM data.", bold_prefix="1. Primary purchase conversion deleted (18 Sep): ", space_after=0.8, font_size=6.5)
    add_bullet(doc, "Several asset groups (T4 Pro/Salon, T3 Premium, Pilgrim, YS24) contained headlines and descriptions promoting a different brand name (Exhibit B). All were rated 'Poor' for Ad Strength.", bold_prefix="2. Another brand's copy in live Performance Max asset groups: ", space_after=0.8, font_size=6.5)
    add_bullet(doc, "Merchant Center shows 216 ineligible products: 110 with 'page unavailable' (404) and 70 with promotional overlay violations. At least ₹80,285 was spent on affected products with zero conversions (for example, one serum SKU spent ₹1,614 on 480 clicks into a 404 page).", bold_prefix="3. 110 broken product pages: ", space_after=0.8, font_size=6.5)
    add_bullet(doc, "Daily budgets were changed 140 times in under 60 days (74 increases, 66 decreases). We cannot isolate the effect on delivery, but constant changes make Smart Bidding performance harder to read and slower to stabilize.", bold_prefix="4. Frequent budget changes: ", space_after=0.8, font_size=6.5)
    add_bullet(doc, "A campaign named 'Search-Brand' used broad match and triggered queries unrelated to beauty (for example, gym equipment and a badminton ankle support). The spend on these queries is not yet quantified; it will be after a full search terms export.", bold_prefix="5. Off-category search queries: ", space_after=1.5, font_size=6.5)

    add_h1(doc, "6.4 Meta Ads Audit", space_before=2.5)
    add_body(doc, "Meta spend during the audit period (1 September – 18 November 2026) totaled ₹32.99 Lakhs.", space_after=1.0, font_size=6.7)
    add_bullet(doc, "'Retargeting — DPA - Fabb6' spent ₹9.50 Lakhs for 1,850 purchases at ₹513.70 CPA (peaking at ₹570.31 in October), against ₹479.53 for cold prospecting, with frequency of 3.21 and no past-purchaser exclusions. Excess cost against the cold-prospecting CPA is about ₹63,000.", bold_prefix="1. Retargeting more expensive than prospecting: ", space_after=0.8, font_size=6.5)
    add_bullet(doc, "Three Advantage+ Shopping campaigns ran at the same time without product exclusions, so they competed in the same auctions. Account CPM rose from ₹56.15 in August to ₹104.17 in October (+85%) and ₹137.03 in November (+144%). Q4 festive demand raises CPMs for all advertisers, so part of this rise is seasonal. Consolidation to one master Advantage+ campaign will let us measure the effect cleanly.", bold_prefix="2. Overlapping Advantage+ Shopping campaigns: ", space_after=0.8, font_size=6.5)
    add_bullet(doc, "₹50,214 across 8.32 million impressions produced 1,02,322 link clicks, 28 landing page views and 0 purchases (99.97% drop-off between click and page view).", bold_prefix="3. 'IG-Traffic' link-click campaign: ", space_after=0.8, font_size=6.5)
    add_bullet(doc, "The iOS campaign spent ₹19,161 at frequency 13.18 with 0 sales. The Android campaign spent about ₹1.38 Lakhs at ₹1,082 CPA.", bold_prefix="4. App install campaigns: ", space_after=0.8, font_size=6.5)
    add_bullet(doc, "Meta reported 7,34,064 link clicks but only 3,01,798 landing page views on Shopify: a 58.9% gap (52.2% excluding IG-Traffic). Likely causes are mobile page speed, accidental clicks, and pixel or Conversions API (CAPI) misfires. We will diagnose these in the first two weeks.", bold_prefix="5. Click-to-landing-page gap: ", space_after=1.0, font_size=6.5)

    doc.add_page_break()

    # =========================================================================
    # PAGE 8: Avoidable Spend & Three-Phase Turnaround Plan
    # =========================================================================
    add_h1(doc, "6.5 Avoidable Spend: A Range, Not a Single Number")
    add_body(doc, "Based on forensic log analysis of ad server logs, change histories, and product feeds between September and November 2026, avoidable waste is categorized into a conservative provable floor and a realistic central estimate:")

    avoid_data = [
        ["Measure", "Avoidable Amount", "Calculation Basis & Audit Evidence"],
        ["Provable Floor: Spend with Zero Return", "₹1,49,660", "404 dead product pages (₹80,285), IG-Traffic zero-conversion campaign (₹50,214), iOS App install campaign running with broken SDK tracking (₹19,161)."],
        ["Central Estimate: Excess Spend vs. Benchmark", "₹5,87,000", "Provable floor (₹1.50L) + Google Ads September efficiency collapse vs. August baseline (₹3.18L) + unsegmented broad search query bleed (₹1.19L)."],
        ["Upper Bound: Total Disrupted Capital", "₹11,94,000", "Central estimate + estimated lost gross sales margin from deleted purchase conversion tracking between 18 Sep and 08 Oct."]
    ]
    create_styled_table(doc, avoid_data, header_bg="102C57", center_cols=[], right_cols=[1], col_widths=[2.0, 1.2, 4.0], font_size=6.2, header_size=6.5)

    add_h1(doc, "7. Turnaround Plan: Three-Phase Roadmap")
    add_body(doc, "To permanently eliminate structural inefficiencies and scale FABB6 profitably toward ₹1.75 Cr monthly gross sales, execution is organized into three sequential phases:")

    add_h2(doc, "Phase 1: Immediate Triage & Account Stabilization (Weeks 1–2)")
    add_bullet(doc, "Verify server-side Conversions API (CAPI) on Meta and Google Tag enhanced conversion tracking. Ensure primary conversion action tracks Shopify gross receipts with accurate transaction IDs.", bold_prefix="1. Conversion Tracking Fix: ")
    add_bullet(doc, "Deploy automated feed management tool to exclude out-of-stock SKUs and dead 404 URLs from Merchant Center. Implement 750+ master negative keywords.", bold_prefix="2. Catalog & Search Bleed Quarantine: ")
    add_bullet(doc, "Pause low-performing standalone campaigns (IG-Traffic, legacy catalog sales); consolidate audiences into clean 3-tier structures.", bold_prefix="3. Funnel Pruning: ")

    add_h2(doc, "Phase 2: Restructure & Baseline Stabilization (December 2026)")
    add_bullet(doc, "Launch consolidated Google Ads architecture (Hero PMax, Branded Search, Category Hair Care, DSA) at ₹19.00L monthly budget.", bold_prefix="1. Google Funnel Deployment: ")
    add_bullet(doc, "Deploy consolidated 3-tier Meta architecture (TOF ASC, MOF Engagers, BOF DPA) at ₹11.00L monthly budget with universal 30-day purchaser exclusions.", bold_prefix="2. Meta Funnel Deployment: ")
    add_bullet(doc, "Set live GoKwik express checkout and automated WhatsApp cart recovery workflows to capture 1,700 non-paid orders.", bold_prefix="3. Checkout & Retention Kickoff: ")

    add_h2(doc, "Phase 3: Profitable Scaling (January – February 2027)")
    add_bullet(doc, "Scale media spend to ₹35.00L in January and ₹40.00L in February subject to trailing 7-day Gross ROAS ≥ 2.50x.", bold_prefix="1. Governed Budget Ramp: ")
    add_bullet(doc, "Expand AOV to ₹1,400 (Jan) and ₹1,500 (Feb) via salon combo bundling, pre-checkout upsells, and ₹999 free shipping tiers.", bold_prefix="2. AOV Merchandising: ")
    add_bullet(doc, "Deploy Princeton KDD 2024 Generative Engine Optimization (GEO) content and execute 8 Reels / 6 Carousels monthly SMO cadence.", bold_prefix="3. Organic Compounding: ")

    doc.add_page_break()

    # =========================================================================
    # PAGE 9: Audit-Stage Forecast: Dec 2026 – Feb 2027
    # =========================================================================
    add_h1(doc, "8. Audit-Stage Forecast: December 2026 – February 2027")
    add_h2(doc, "8.1 Forecasting Methodology & Approach")
    add_body(doc, "The master forecast models total store gross merchandise value across paid media, organic SEO search, and automated retention flows. Planned media spend follows the agreed governance ramp: ₹30.0L in December, ₹35.0L in January, and ₹40.0L in February (₹105.00L total in Plan 1). December spend is calibrated below the November run-rate to allow campaign restructuring and Smart Bidding re-learning:")

    add_h2(doc, "8.2 Master Turnaround Forecast (Plan 1: Base / Recommended)")
    fc_table_data = [
        ["Month", "Total Media Spend", "Google / Meta Split", "Paid Orders", "Organic*", "Others*", "Total Store Orders", "Gross Sales Revenue", "Store ROAS", "Blended CPA"],
        ["Dec 2026", "₹30.00L", "₹19.0L / ₹11.0L", "5,455", "1,650", "1,700", "8,805", "₹115.25L", "3.84x", "₹340.73"],
        ["Jan 2027", "₹35.00L", "₹22.0L / ₹13.0L", "6,667", "1,650", "1,870", "10,187", "₹142.61L", "4.07x", "₹343.59"],
        ["Feb 2027", "₹40.00L", "₹25.0L / ₹15.0L", "8,000", "1,650", "2,057", "11,707", "₹175.61L", "4.39x", "₹341.68"]
    ]
    create_styled_table(doc, fc_table_data, header_bg="102C57", center_cols=[0, 2], right_cols=[1, 3, 4, 5, 6, 7, 8, 9], col_widths=[0.65, 0.70, 1.05, 0.65, 0.55, 0.55, 0.65, 1.10, 0.60, 0.65], font_size=6.2, header_size=6.5)

    add_h2(doc, "8.3 Scenario Sensitivities on Total Spend & Scaling Capacity")
    sens_table_data = [
        ["Scenario Tier", "Q1 Media Spend", "Paid Orders", "Organic Orders", "Others Orders", "Total Orders", "Gross Sales Revenue", "Paid ROAS", "Store ROAS", "Blended CPA"],
        ["Plan 1: Base / Recommended", "₹105.00L", "20,121", "4,950", "5,627", "30,698", "₹433.47L (~₹4.33 Cr)", "2.71x", "4.13x", "₹342.04"],
        ["Plan 2: Moderate", "₹122.00L", "23,373", "4,950", "5,627", "33,950", "₹479.37L (~₹4.79 Cr)", "2.71x", "3.93x", "₹359.35"],
        ["Plan 3: Aggressive", "₹141.00L", "27,025", "4,950", "5,627", "37,602", "₹531.27L (~₹5.31 Cr)", "2.71x", "3.77x", "₹374.98"]
    ]
    create_styled_table(doc, sens_table_data, header_bg="1F4E78", center_cols=[0], right_cols=[1, 2, 3, 4, 5, 6, 7, 8, 9], col_widths=[1.5, 0.65, 0.60, 0.55, 0.55, 0.60, 1.10, 0.55, 0.55, 0.60], font_size=5.8, header_size=6.2)

    add_h2(doc, "8.4 Channel-Level Targets & Operational Guardrails")
    add_bullet(doc, "Google Ads targets 3,455 paid orders in Dec (₹550 CPA), 4,190 in Jan (₹525 CPA), and 5,000 in Feb (₹500 CPA) on budgets of ₹19L, ₹22L, and ₹25L.", bold_prefix="Google Targets: ")
    add_bullet(doc, "Meta Ads targets 2,000 paid orders in Dec (₹550 CPA), 2,476 in Jan (₹525 CPA), and 3,000 in Feb (₹500 CPA) on budgets of ₹11L, ₹13L, and ₹15L.", bold_prefix="Meta Targets: ")

    add_h2(doc, "8.5 Key Assumptions & Risk Management")
    add_bullet(doc, "AOV expands from ₹1,309 to ₹1,400 and ₹1,500, supported by minimum free-shipping thresholds (₹999) and 2-pack combo merchandising.", bold_prefix="AOV Trajectory: ")
    add_bullet(doc, "Paid orders represent 62% (Dec), 65% (Jan), and 68% (Feb) of total store orders, leaving 32%–38% to organic search and retention flows.", bold_prefix="Channel Dependency: ")

    doc.add_page_break()

    # =========================================================================
    # PAGE 10: Operating Guardrails & SEO / AEO / GEO Architecture
    # =========================================================================
    add_h1(doc, "9. Operating Guardrails")
    add_bullet(doc, "New campaigns, ad sets, and creatives are created paused. They go live only after conversion tracking, UTM tagging, and margin review are confirmed.", bold_prefix="1. Paused-First Creation: ")
    add_bullet(doc, "Budget increases are strictly capped at ≤ 20% every 72 hours per campaign to protect Smart Bidding stability.", bold_prefix="2. Budget Pacing: ")
    add_bullet(doc, "Prospecting campaigns maintain universal negative exclusions for past 30-day purchasers and customer lists.", bold_prefix="3. Audience Hygiene: ")
    add_bullet(doc, "Automated daily scans of Merchant Center and Shopify instantly quarantine products with 404 URLs or zero stock.", bold_prefix="4. Daily Feed Scans: ")
    add_bullet(doc, "Daily pacing updates via Slack/WhatsApp, weekly KPI reviews, and monthly reconciliation against Shopify gross revenue.", bold_prefix="5. Reporting Cadence: ")

    add_h1(doc, "10. Search Engine Optimization (SEO, AEO & GEO)")
    add_h2(doc, "10.1 Role in the Growth Engine")
    add_body(doc, "While paid media buys immediate demand, organic optimization builds compounding, owned equity. The 4,950 organic orders in Q1 (1,650/month) represent ₹69.2 Lakhs in gross revenue generated with zero incremental ad spend. Furthermore, catalog-level technical SEO fixes directly enhance Google Shopping and Performance Max Quality Scores, creating an immediate cross-channel efficiency multiplier.")

    add_h2(doc, "10.2 Storefront Baseline & Technical Observations")
    add_bullet(doc, "Shopify collection URLs generated duplicate access paths without canonical consolidation, diluting domain authority.", bold_prefix="Non-Canonical Architecture: ")
    add_bullet(doc, "Hundreds of seasonal or discontinued SKUs return 404 HTTP status codes without 301 redirects to relevant parent categories.", bold_prefix="Broken Indexing & 404 Bleed: ")
    add_bullet(doc, "Missing JSON-LD structured data on price, availability, and brand specifications across key collection pages.", bold_prefix="Schema Deficits: ")

    add_h2(doc, "10.3 Strategic Pillars: Seven Workstreams")
    add_bullet(doc, "Audit XML sitemaps; eliminate 404 errors; resolve redirect chains; ensure 1:1 canonical product mapping.", bold_prefix="1. Catalog & Index Hygiene: ")
    add_bullet(doc, "Map brand, category, and concern queries to matching landing pages. Seed research from high-converting Google Search terms.", bold_prefix="2. Keyword Intent Mapping: ")
    add_bullet(doc, "Enhance titles, H1s, meta copy, and internal links for high-margin hero SKUs (>28% margin), adding usage guides and FAQ schema.", bold_prefix="3. Hero Page Optimization: ")
    add_bullet(doc, "Publish concern-led guides (hairfall, dandruff, post-keratin care) structured to capture informational search intent.", bold_prefix="4. Concern Content Hubs: ")
    add_bullet(doc, "Implement full Schema.org structured data (Product, Offer, MerchantReturnPolicy, AggregateRating, Organization).", bold_prefix="5. Rich Schema Architecture: ")
    add_bullet(doc, "Apply Princeton KDD 2024 levers (authoritative quotes, technical statistics, source citations) to earn inclusion in Google AI Overviews.", bold_prefix="6. Generative Engine Optimization (GEO): ")
    add_bullet(doc, "Format product content around direct conversational answers to voice and AI queries ('How to use L'Oréal Absolut Repair masque?').", bold_prefix="7. Answer Engine Optimization (AEO): ")

    doc.add_page_break()

    # =========================================================================
    # PAGE 11: Monthly SEO / AEO / GEO Deliverables Matrix
    # =========================================================================
    add_h1(doc, "10.4 Monthly Deliverables Matrix: SEO, AEO & GEO")
    add_body(doc, "The matrix below details the technical, content, and generative engine deliverables committed across the 90-day turnaround engagement:")

    seo_matrix_data = [
        ["Workstream", "Month 1 (December 2026)", "Month 2 (January 2027)", "Month 3 (February 2027)"],
        ["Technical SEO & Catalog Hygiene", "• Crawl audit & sitemap cleanup\n• Fix 100% of 404 errors & redirect chains\n• Canonical URL audit on all collections\n• Merchant Center schema & feed validation\n• Core Web Vitals (CWV) baseline diagnostic", "• Image compression & CDN review\n• Mobile INP (< 200ms) optimization\n• Internal link depth remediation\n• Automated 404 monitoring script live\n• Indexation triage for newly added SKUs", "• Quarterly technical hygiene audit\n• JS execution & rendering review\n• Clean indexation check in GSC\n• Server response time (TTFB) tuning\n• Structured data health verification"],
        ["On-Page & Hero Architecture", "• Optimize top 20 hero collection pages\n• H1, Title & Meta description rewrite\n• Target brand + category keyword mapping\n• Implementation of authenticity badges\n• Product FAQ blocks on top 10 SKUs", "• Optimize next 30 collection/brand pages\n• Breadcrumb navigation enhancement\n• Internal linking from blogs to hero PDPs\n• Cross-sell combo link architecture\n• Review rich snippet markup deployment", "• Full catalog on-page audit & polish\n• Seasonal category page refreshes\n• User-generated review schema markup\n• PDP conversion-focused micro-copy\n• Meta tag performance re-indexing"],
        ["Content Hubs & Concern Guides", "• 4 Concern-led blog guides published\n• Topics: Post-salon color protection,\nhair spa at home, dry winter care\n• Embedded product schema & buy-buttons", "• 4 Technical guides & routines\n• Topics: Nanoplastia maintenance,\nMatrix vs L'Oréal masque breakdown\n• Brand comparison shopping tables", "• 4 Seasonal authority articles\n• Topics: Spring anti-frizz routines,\nprofessional de-tan skin regimens\n• Internal link siloing to hero combos"],
        ["AEO & Generative Engine Optimization (GEO)", "• Princeton KDD 2024 GEO audit\n• Establish 30 AI baseline test queries\n• Implement Q&A structured schema\n• Add brand citation anchors on guides", "• Authoritative statistics added to blogs\n• Expert stylist quotes integrated\n• Optimize for Google AI Overviews\n• Perplexity answer snippet optimization", "• Monthly AI citation tracking report\n• Brand sentiment review in LLM answers\n• ChatGPT Search indexing verification\n• Knowledge Graph entity reinforcement"]
    ]
    create_styled_table(doc, seo_matrix_data, header_bg="102C57", center_cols=[0], right_cols=[], col_widths=[1.5, 1.9, 1.9, 1.9], font_size=5.8, header_size=6.2)

    add_body(doc, "All content production is fully managed and published directly to Shopify. Performance is tracked via Google Search Console, Google Analytics 4, and proprietary AI answer engine query tracking panels.", space_after=1.0, font_size=6.5)

    doc.add_page_break()

    # =========================================================================
    # PAGE 12: SEO KPIs & Social Media Optimization (SMO) Strategy
    # =========================================================================
    add_h1(doc, "10.5 Key Performance Indicators: SEO, AEO & GEO")
    add_body(doc, "Organic search success is evaluated across technical hygiene, indexed volume, and commercial order contribution:")

    seo_kpi_data = [
        ["Metric", "Measurement Platform", "Baseline / Month 1 Target", "Month 2 Target", "Month 3 Target"],
        ["Dead 404 URLs in Feed & Sitemap", "Merchant Center / GSC", "0 within 14 days of Phase 1", "0 daily occurrences", "0 daily occurrences"],
        ["Valid Indexed Product & Collection Pages", "Google Search Console", "Establish verified baseline", "+15% valid indexed pages", "+25% valid indexed pages"],
        ["Core Web Vitals Pass Rate (Mobile)", "PageSpeed Insights / CWV", "Baseline audit (> 3.5s LCP)", "LCP ≤ 2.8s, INP ≤ 250ms", "LCP ≤ 2.5s, INP ≤ 200ms (Green)"],
        ["Non-Brand Organic Search Clicks", "Google Search Console", "Baseline recorded Month 1", "+20% non-brand clicks", "+40% non-brand clicks"],
        ["Organic Store Orders", "Shopify Store Analytics", "1,650 orders (₹21.6L gross)", "1,650 orders (₹23.1L gross)", "1,650 orders (₹24.8L gross)"],
        ["AI Answer Citation Rate (30 Target Queries)", "Google AI Overviews / Perplexity", "Baseline citation rate tracked", "≥ 25% query inclusion", "≥ 40% query inclusion"]
    ]
    create_styled_table(doc, seo_kpi_data, header_bg="102C57", center_cols=[1], right_cols=[2, 3, 4], col_widths=[2.1, 1.5, 1.2, 1.2, 1.2], font_size=6.0, header_size=6.3)

    add_h1(doc, "11. Social Media Optimization (SMO)")
    add_h2(doc, "11.1 Strategic Role: The Organic Creative Incubator")
    add_body(doc, "Organic social media serves two indispensable functions in this architecture: (1) it acts as a low-cost testing ground for creative angles, hooks, and product combinations before deploying ad spend, and (2) it nurtures mid-funnel social engagers who are retargeted via Meta campaign `M_MOF_Social_Engagers`. High-performing organic reels are directly amplified with paid media spend to lower overall account CPMs.")

    add_h2(doc, "11.2 Core Channels & Distribution")
    add_bullet(doc, "Primary visual brand home. Dedicated focus on high-retention Reels, aesthetic carousel guides, and daily interactive Stories.", bold_prefix="Instagram (Primary): ")
    add_bullet(doc, "Secondary community touchpoint. Video crossposting and copy-rich educational posts targeted toward professional salon owners and mature buyers.", bold_prefix="Facebook (Secondary): ")

    add_h2(doc, "11.3 Content Pillars")
    add_bullet(doc, "How-to tutorials, salon treatment frequency, common application mistakes, and stylist secrets.", bold_prefix="1. Salon-Grade Education & Usage (35%): ")
    add_bullet(doc, "Direct problem-solution routines for hairfall, dandruff, chemically treated hair, and color preservation.", bold_prefix="2. Concern-Led Solutions (30%): ")
    add_bullet(doc, "Packaging inspection, holographic seal verification, authorized distributor credentials, and unboxing.", bold_prefix="3. Authenticity & Anti-Counterfeit (20%): ")
    add_bullet(doc, "Hero 2-pack/3-pack bundle announcements, seasonal combo launches, and flash discount promotions.", bold_prefix="4. Combos, Merchandising & Offers (15%): ")

    doc.add_page_break()

    # =========================================================================
    # PAGE 13: SMO Cadence, Post Counts, Calendar & CRO Rationale
    # =========================================================================
    add_h1(doc, "11.4 Cadence & Indicative Monthly Output Volume")
    add_body(doc, "To maintain consistent visual presence and fuel the Meta ad account with organic engagement, Techno Exponent commits to the following monthly production schedule:")

    smo_vol_data = [
        ["Content Element / Asset Type", "Monthly Production Volume", "Strategic Purpose & Distribution Channel"],
        ["Instagram Reels (Short-Form Video)", "8 Reels / month (2 / week)", "Problem-solution hooks, before/after salon care, application how-tos; optimized for audio trends."],
        ["Educational Carousels", "6 Carousels / month", "Step-by-step routines, combo explainers, ingredient breakdowns; designed for high saves and shares."],
        ["Single Image / Graphic Posts", "4 Posts / month (1 / week)", "New brand/SKU announcements, flash sales, authenticity trust badges, customer reviews."],
        ["Interactive Story Sets", "3 Sets / week (~12–14 / month)", "Polls, Q&As, behind-the-scenes packaging, product link stickers driving direct traffic to Shopify."],
        ["Facebook Cross-Posting", "All assets crossposted", "Published simultaneously with tailored, long-form copy optimized for Facebook community engagement."],
        ["Community Management & Replies", "Daily (Mon – Fri)", "Active response to comments and DMs within 24 hours; order queries escalated to WhatsApp concierge."],
        ["Paid Amplification of Winners", "As performance dictates", "Top-performing organic Reels boosted directly via M_TOF_ASC or M_MOF to lower blended CPM."]
    ]
    create_styled_table(doc, smo_vol_data, header_bg="102C57", center_cols=[1], right_cols=[], col_widths=[2.1, 1.6, 3.5], font_size=6.0, header_size=6.3)

    add_h2(doc, "11.5 Illustrative First-Week Social Calendar")
    cal_data = [
        ["Day", "Platform & Format", "Content Topic", "Content Pillar", "Call to Action (CTA)"],
        ["Monday", "Instagram Reel", "Winter Hair Care Routine in 3 Easy Steps", "Concern-Led Solutions", "Save this reel for your next wash day!"],
        ["Tuesday", "Instagram Carousel", "Hair Spa Masque: 4 Mistakes Ruining Your Results", "Salon Education", "Shop the Deep Nourish Combo (Link in bio)"],
        ["Wednesday", "Story Set (3 Slides)", "Authenticity Check: How to Spot Fake Salon Products", "Authenticity & Trust", "Tap sticker to shop 100% genuine products"],
        ["Thursday", "Instagram Reel", "Post-Color Hair Protection: Keep Your Salon Tone", "Concern-Led Solutions", "Comment 'COLOR' for direct product link"],
        ["Friday", "Single Graphic Post", "Weekend Combo Drop: Masque + Serum Bundle (₹999)", "Combos & Offers", "Free shipping on orders above ₹999"],
        ["Saturday", "Story Set (Interactive)", "Hair Quiz: Which Professional Treatment Do You Need?", "Salon Education", "Vote on poll & check your personalized routine"]
    ]
    create_styled_table(doc, cal_data, header_bg="1F4E78", center_cols=[0, 1, 3], right_cols=[], col_widths=[0.8, 1.4, 2.2, 1.4, 1.4], font_size=5.8, header_size=6.2)

    add_h1(doc, "12. Conversion Rate Optimization (CRO)")
    add_h2(doc, "12.1 Strategic Rationale")
    add_body(doc, "With ₹30L–₹40L in monthly paid ad spend driving over 70,000 monthly store visits, even modest improvements in conversion rate yield massive profit swings. Moving storefront conversion from 1.2% to 1.6% represents a +33% increase in orders with zero added media cost, dramatically lowering blended CPA.")

    doc.add_page_break()

    # =========================================================================
    # PAGE 14: CRO Storefront Baseline & Funnel Optimization
    # =========================================================================
    add_h1(doc, "12.2 Storefront Baseline & Strategic Hypotheses")
    add_body(doc, "A comprehensive audit of fabb6.com identified several immediate conversion bottlenecks across the desktop and mobile storefront:")

    cro_hyp_data = [
        ["Storefront Area", "Current Observation", "Strategic Test Hypothesis", "Expected Impact"],
        ["Homepage Hero Section", "8 rotating banner slides with auto-scroll; messages diluted across multiple unrelated offers.", "Replace carousel with a static high-impact hero banner highlighting authorized distributor trust badges and top 3 hero salon combos.", "Reduce bounce rate by 15%; increase click-through to high-margin collection pages."],
        ["Promotional Offer Ladder", "Three fragmented coupons: ₹100 off >₹1,000 (FN100), 5% off >₹2,000, 12% in-app (APP12).", "Unify into a transparent cart progress bar: 'Add ₹150 for Free Shipping, Add ₹400 for Free Professional Serum'.", "Directly drive AOV expansion from ₹1,309 toward ₹1,400+ target."],
        ["Product Detail Page (PDP)", "Single-item display; benefits buried under manufacturer boilerplate text.", "Add 'Complete Salon Routine' 2-pack bundle upsell directly above the 'Add to Cart' button with 1-click add.", "Increase multi-item basket conversion; boost combo attach rate by 22%."],
        ["Mobile Page Speed", "Mobile LCP exceeds 3.8s due to unoptimized vendor JavaScript and hero banner image payloads.", "Compress images to WebP format, defer non-critical scripts, and preload primary LCP hero image.", "Decrease mobile bounce rate; improve Google Ads Quality Score."]
    ]
    create_styled_table(doc, cro_hyp_data, header_bg="102C57", center_cols=[0], right_cols=[], col_widths=[1.3, 1.8, 2.3, 1.8], font_size=5.8, header_size=6.2)

    add_h2(doc, "12.3 Program by Funnel Stage")
    add_bullet(doc, "Prominent authenticity guarantees ('100% Genuine Salon Products Sourced Directly from Brands'), authorized distributor seals, and clear category navigation based on hair concern.", bold_prefix="1. Homepage & Discovery: ")
    add_bullet(doc, "Dynamic filtering by brand, hair concern (color-treated, damaged, frizzy), and price; prominent 'Best Seller' and 'Salon Pro' badges.", bold_prefix="2. Collection Architecture: ")
    add_bullet(doc, "Sticky mobile 'Buy Now' button, delivery date estimator by pincode, trust badges, customer review highlights, and salon combo upsells.", bold_prefix="3. Product Detail Page (PDP): ")
    add_bullet(doc, "Slide-out AJAX cart drawer with free shipping threshold progress bar, free gift threshold, and 1-click recommended item upsells.", bold_prefix="4. Cart Experience: ")

    add_h2(doc, "12.4 Experimentation Governance")
    add_body(doc, "All CRO initiatives follow strict statistical rigor: A/B tests run for a minimum of 14 days or until 95% statistical significance is achieved. No major visual tests are deployed during Red Light performance weeks under scaling governance rules.")

    doc.add_page_break()

    # =========================================================================
    # PAGE 15: Monthly CRO Deliverables, KPIs & Commercials
    # =========================================================================
    add_h1(doc, "12.5 Monthly Deliverables: Conversion Rate Optimization")
    add_body(doc, "The matrix below outlines the systematic CRO testing and deployment schedule across the 3-month engagement:")

    cro_deliv_data = [
        ["Deliverable Area", "Month 1 (December 2026)", "Month 2 (January 2027)", "Month 3 (February 2027)"],
        ["Funnel Diagnostics & Analytics", "• Full mobile-first UX audit\n• Session recording & heatmap setup\n• GA4 funnel drop-off audit\n• Pixel & CAPI tracking verification", "• Review session recordings & rage clicks\n• Identify PDP exit bottlenecks\n• Post-festive shopping pattern review\n• Form field abandonment analysis", "• Quarterly conversion retrospective\n• Device-level checkout drop-off review\n• Pincode-level COD delivery audit\n• Customer journey map update"],
        ["Landing Pages & Hero Architecture", "• Design 2 dedicated hero combo LPs\n• High-margin Hair Spa bundle LP\n• Authenticity & Salon Trust LP", "• Design 2 seasonal routine LPs\n• Post-Color Treatment bundle LP\n• VIP Professional Styling kit LP", "• Design 2 high-AOV mega-kit LPs\n• Salon Bulk Order replenishment LP\n• Spring Rejuvenation bundle LP"],
        ["A/B Experimentation Program", "• Test 1: Sticky Mobile 'Add to Cart'\n• Test 2: Progress bar for free shipping\n• Measure lift in AOV & cart-to-checkout", "• Test 3: 2-Pack bundle PDP widget\n• Test 4: Trust badge placement\n• Test 5: Dynamic UPI discount banner", "• Test 6: Simplified 1-step cart drawer\n• Test 7: Pincode delivery estimator\n• Test 8: Personalized cross-sell grid"],
        ["Reporting & Insights", "• Baseline CRO scorecard & audit report\n• Initial A/B test result transmittal", "• Monthly CRO impact & AOV report\n• Winning experiment rollout plan", "• Comprehensive 90-day CRO review\n• Final conversion roadmap for Q2"]
    ]
    create_styled_table(doc, cro_deliv_data, header_bg="102C57", center_cols=[0], right_cols=[], col_widths=[1.5, 1.9, 1.9, 1.9], font_size=5.8, header_size=6.2)

    add_h1(doc, "13. Commercials & Engagement Scope")
    add_body(doc, "Techno Exponent provides a dedicated, multi-disciplinary performance growth team managing paid acquisition, search engine optimization, social media production, and conversion rate engineering:")
    add_bullet(doc, "End-to-end campaign architecture, bid management, feed management tooling, creative production, and daily budget pacing across Google Ads and Meta Ads.", bold_prefix="Performance Marketing: ")
    add_bullet(doc, "Technical audits, Merchant Center sync, 12 authority content articles, schema architecture, and Princeton KDD 2024 GEO implementation.", bold_prefix="SEO, AEO & GEO: ")
    add_bullet(doc, "Monthly production of 8 Reels, 6 Carousels, 4 Single Graphic Posts, 3 Story sets/week, copy creation, and community management.", bold_prefix="Social Media Optimization: ")
    add_bullet(doc, "Funnel diagnostics, 2 new landing page specifications monthly, and 2-3 live A/B experiments per month to elevate AOV and conversion.", bold_prefix="Conversion Rate Optimization: ")

    doc.add_page_break()

    # =========================================================================
    # PAGE 16: Legal Disclaimer & Terms and Conditions
    # =========================================================================
    add_h1(doc, "14. Disclaimer")
    add_body(doc, "The strategy, forecasts, scenario models, and performance targets outlined in this document are developed based on rigorous analysis of historical Shopify store data supplied through 24 November 2026, advertising platform diagnostic logs, and industry benchmarks for professional beauty and personal care e-commerce. Actual performance may vary due to a variety of external and commercial market factors beyond agency control, including consumer purchasing behavior, aggressive competitor pricing, inventory stockouts, platform algorithm updates, and macro-economic demand shifts.")

    add_body(doc, "Techno Exponent could not independently verify historic organic search order numbers from past Shopify or Google Analytics tracking. The baseline volume of 1,650 organic orders per month incorporated into the Q1 turnaround forecast was provided directly by the client, and forward operating models and revenue projections are developed based on this operational assumption.", bold_prefix="Historic Organic Order Baseline & Forecast Assumption: ")

    add_body(doc, "While Techno Exponent will implement industry best practices, deploy proprietary optimization frameworks, and aggressively optimize all campaigns under strict governance rules, we cannot legally guarantee specific revenue figures, return on ad spend (ROAS), search engine rankings, or inclusion rates in AI-generated answer engines. Audit findings are derived from client-provided data, and figures may be refined as additional data (such as raw search term logs) becomes available. We commit to complete transparency, daily reporting, and proactive strategic pivots to protect client capital and maximize growth.")

    add_h1(doc, "15. Terms and Conditions")
    add_bullet(doc, "The scope of work outlined herein encompasses the specific deliverables, ad budgets, post volumes, and optimization routines detailed across Sections 1 through 13. Any additional services (such as custom software development, third-party software subscriptions, or influencer fees) will be quoted separately.", bold_prefix="1. Scope of Engagement: ")
    add_bullet(doc, "Advertising media spend is paid directly by the client to the advertising platforms (Google Ads, Meta Ads). Techno Exponent does not broker or finance media spend.", bold_prefix="2. Media Spend Billing: ")
    add_bullet(doc, "Monthly retainers are payable within 7 days of invoice transmittal at the commencement of each monthly billing cycle.", bold_prefix="3. Professional Retainer: ")
    add_bullet(doc, "The client agrees to maintain adequate stock of advertised hero SKUs, ensure timely replenishment, and notify the agency at least 48 hours in advance of any inventory stockouts or major product price changes.", bold_prefix="4. Inventory & Pricing: ")
    add_bullet(doc, "Content calendars and creative assets will be submitted for client approval 5 business days prior to deployment. The client agrees to provide feedback within 48 business hours to prevent campaign delays.", bold_prefix="5. Creative Approvals: ")
    add_bullet(doc, "Either party may terminate the engagement with a 30-day written notice following the completion of the initial 90-day turnaround commitment.", bold_prefix="6. Engagement Term: ")

    # Save document
    os.makedirs(os.path.dirname(docx_path), exist_ok=True)
    doc.save(docx_path)
    print(f"Master 16-page Word document successfully created at: {docx_path}")

if __name__ == "__main__":
    report_docx = r"C:\Users\test\Videos\Office\reports\FABB6_Performance_Marketing_Strategy_Audit_SEO_SMO_CRO.docx"
    report_pdf = r"C:\Users\test\Videos\Office\reports\FABB6_Performance_Marketing_Strategy_Audit_SEO_SMO_CRO.pdf"

    build_proposal_document(report_docx)

    # Convert to PDF via Word COM
    print("Converting DOCX to PDF via Microsoft Word COM...")
    pythoncom.CoInitialize()
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0

    doc_com = word.Documents.Open(os.path.abspath(report_docx))
    doc_com.SaveAs(os.path.abspath(report_pdf), FileFormat=17) # wdFormatPDF = 17
    doc_com.Close()
    word.Quit()
    pythoncom.CoUninitialize()
    print(f"PDF successfully generated at: {report_pdf}")

    # Verify page count
    reader = pypdf.PdfReader(report_pdf)
    page_count = len(reader.pages)
    print(f"VERIFICATION: Total pages in generated PDF: {page_count}")
    assert page_count == 16, f"Expected 16 pages, got {page_count}"
    print("SUCCESS: Exactly 16 pages confirmed!")

    # Mirror to case studies and artifact directory
    dst_dirs = [
        r"C:\Users\test\Videos\Office\case-studies\fabb6",
        r"C:\Users\test\.gemini\antigravity\brain\29f77e0a-5ed5-4d24-842c-443d9957274c"
    ]
    for d in dst_dirs:
        os.makedirs(d, exist_ok=True)
        shutil.copy2(report_docx, os.path.join(d, os.path.basename(report_docx)))
        shutil.copy2(report_pdf, os.path.join(d, os.path.basename(report_pdf)))
        print(f"Mirrored to: {d}")

    print("All tasks completed successfully!")
