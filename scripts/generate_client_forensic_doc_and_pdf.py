import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import win32com.client

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
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

def add_callout_box(doc, title, text, border_color="B22222", bg_color="FDF2E9"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="none"/>
            <w:left w:val="single" w:sz="36" w:space="0" w:color="{border_color}"/>
            <w:bottom w:val="none"/>
            <w:right w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(4)
    r_t = p.add_run(f"CRITICAL FINDING: {title}\n")
    r_t.bold = True
    r_t.font.name = "Calibri"
    r_t.font.size = Pt(11)
    r_t.font.color.rgb = RGBColor(160, 20, 20) if border_color == "B22222" else RGBColor(16, 44, 87)
    
    r_body = p.add_run(text)
    r_body.font.name = "Calibri"
    r_body.font.size = Pt(10)
    r_body.font.color.rgb = RGBColor(50, 50, 50)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def build_forensic_doc():
    docx_path = r"C:\Users\test\Videos\Office\reports\FABB6_Forensic_Audit_Report_Google_and_Meta_Ads.docx"
    pdf_path = r"C:\Users\test\Videos\Office\reports\FABB6_Forensic_Audit_Report_Google_and_Meta_Ads.pdf"
    
    print("Building Executive Forensic Audit Document for FABB6...")
    doc = docx.Document()
    
    # 1. Page Setup
    for s in doc.sections:
        s.top_margin = Inches(0.9)
        s.bottom_margin = Inches(0.9)
        s.left_margin = Inches(0.9)
        s.right_margin = Inches(0.9)
        s.page_width = Inches(8.5)
        s.page_height = Inches(11.0)

    # Styles
    navy_color = RGBColor(16, 44, 87) # #102C57
    dark_gray = RGBColor(70, 70, 70)
    muted_gray = RGBColor(120, 120, 120)
    dark_red = RGBColor(178, 34, 34)

    # COVER / HEADER
    p_hdr = doc.add_paragraph()
    p_hdr.paragraph_format.space_after = Pt(2)
    r_co = p_hdr.add_run("TECHNO EXPONENT | GLOBAL DIGITAL GROWTH PARTNER\n")
    r_co.font.name = "Calibri"
    r_co.font.size = Pt(10)
    r_co.font.bold = True
    r_co.font.color.rgb = muted_gray

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(8)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("FABB6 (Glanzzkart Private Limited)")
    r_title.font.name = "Calibri"
    r_title.font.size = Pt(24)
    r_title.font.bold = True
    r_title.font.color.rgb = navy_color

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(6)
    r_sub = p_sub.add_run("Comprehensive Paid Media Forensic Audit: Google Ads & Meta Ads\n")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(14)
    r_sub.font.bold = True
    r_sub.font.color.rgb = dark_red

    r_sub2 = p_sub.add_run("Performance Autopsy, Root Cause Failure Diagnostics, Quantified Budget Waste & 90-Day Account Turnaround Plan")
    r_sub2.font.name = "Calibri"
    r_sub2.font.size = Pt(11)
    r_sub2.font.color.rgb = dark_gray

    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_after = Pt(14)
    r_meta = p_meta.add_run("Audit Date: 18th November 2026 | Audit Period: 1st September – 18th November 2026 | Lead Auditor: Sarnendu Patra (Head of Marketing)")
    r_meta.font.name = "Calibri"
    r_meta.font.size = Pt(9.5)
    r_meta.font.italic = True
    r_meta.font.color.rgb = muted_gray

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ---------------------------------------------------------------------------
    # SECTION 1: EXECUTIVE SUMMARY
    # ---------------------------------------------------------------------------
    h1 = doc.add_heading("1. Executive Summary: What Happened & Why FABB6 Returned", level=1)
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(6)

    p1 = doc.add_paragraph(
        "In late August 2026, Techno Exponent conducted an exhaustive forensic evaluation of FABB6's digital marketing ecosystem, "
        "establishing a 9-month historic baseline (December 2025 – August 2026) and formulating three calibrated growth models. "
        "In our formal proposal, we specifically warned FABB6 leadership about critical structural vulnerabilities: "
        "186 Google Merchant Center catalog errors burning ₹1.04 Lakhs in ad spend, misconfigured Meta pixel tracking, unchecked broad-match keyword bleed, "
        "and total absence of an automated returning customer retention engine (despite an outstanding 27.7% organic repeat rate).\n\n"
        "Despite these warnings, FABB6 initially engaged a competing agency (SilverXis) in September 2026. "
        "Over the subsequent 78 days (1st September to 18th November 2026), the competitor agency oversaw a catastrophic operational breakdown "
        "across both Google Ads and Meta Ads:"
    )
    p1.paragraph_format.line_spacing = 1.15

    add_callout_box(
        doc,
        "Total Store Revenue & Order Collapse in September 2026",
        "During the competitor's first full month (September), total Shopify store orders plummeted by -71.9% (from 11,069 in August to just 3,112), "
        "and Gross Sales crashed from ₹95.64 Lakhs to ₹36.02 Lakhs. The competitor slashed ad spend by 79%, paid orders collapsed to 801, "
        "and the business survived almost exclusively on past customer equity (51.8% returning customer rate).",
        border_color="B22222", bg_color="FDF2E9"
    )

    add_callout_box(
        doc,
        "The September 18 Tracking Blackout (Google Ads CPA Hit ₹7,569)",
        "On September 18, 2026 at 3:32 PM, competitor user 'sarjit@silverxis.com' deleted the primary conversion action 'Purchase-2026' in Google Ads. "
        "This completely blinded Google's Smart Bidding algorithm. Consequently, September Google Ads delivered only 42 orders on ₹3.18 Lakhs spend, "
        "sending Google CPA to an astronomical ₹7,568.93 and ROAS to 0.15x (spending ₹7,569 to generate a ₹1,103 order).",
        border_color="B22222", bg_color="FDF2E9"
    )

    add_callout_box(
        doc,
        "The 'Glam+' Copy-Paste Disaster (Severe Agency Negligence)",
        "In multiple live Google Performance Max campaigns (T4 Pro/Salon, T3 Premium, Pilgrim, YS24), the competitor literally copy-pasted headlines and copy "
        "from another client named 'Glam+': 'Beauty & Skincare Must-Haves, Glam+ Store', 'Glow Up with Glam+ | Flas Sale is Live' (with typos!), "
        "and audience signals tagged 'Glam Plus - Custom -CWV'. FABB6 paid real money to display ads promoting someone else's storefront!",
        border_color="B22222", bg_color="FDF2E9"
    )

    add_callout_box(
        doc,
        "October Festive (Diwali) Meltdown: ₹42.47 Lakhs Burned at Record High CPA",
        "During India's highest-demand festive shopping season, the competitor pumped ₹42.47 Lakhs into ads. But Meta CPA surged to an all-time record high "
        "of ₹532.42 (ROAS 2.47x). Paid purchases (7,298) were lower than unoptimized July actuals (8,313 purchases on ₹43.6L spend), "
        "proving that the competitor did worse than FABB6's old historical baseline.",
        border_color="B22222", bg_color="FDF2E9"
    )

    add_callout_box(
        doc,
        "Over ₹7.46 Lakhs in Quantified, Avoidable Budget Waste",
        "We have mathematically isolated ₹7,46,558.00 in direct waste: 110 products throwing 404 dead links (₹80K+ burned), 8.3M impressions on IG-Traffic "
        "with 0 sales (₹50K burned), zombie app ads running at a frequency of 13.18, and deleted tracking bidding penalties.",
        border_color="B22222", bg_color="FDF2E9"
    )

    # ---------------------------------------------------------------------------
    # SECTION 2: RECONCILED HISTORIC VS COMPETITOR PERFORMANCE MATRIX
    # ---------------------------------------------------------------------------
    h2 = doc.add_heading("2. Full Performance Matrix: December 2025 – November 2026", level=1)
    h2.paragraph_format.space_before = Pt(14)

    p_t_desc = doc.add_paragraph("The table below reconciles verified monthly actuals across Shopify, Google Ads, Meta Ads, and Total Paid Media:")
    p_t_desc.paragraph_format.space_after = Pt(4)

    matrix_rows = [
        ["Month", "Shopify Orders", "Gross Sales", "Paid Spend", "Paid Orders", "Blended CPA", "Google CPA", "Meta CPA", "Net ROAS", "Repeat %"],
        ["Dec 2025", "3,307", "₹26.38 L", "₹4.21 L", "1,614", "₹260.69", "₹481.09", "₹169.23", "4.92x", "13.9%"],
        ["Jan 2026", "7,850", "₹55.52 L", "₹12.17 L", "4,260", "₹285.55", "₹576.14", "₹154.63", "3.81x", "17.2%"],
        ["Feb 2026", "8,250", "₹64.10 L", "₹17.97 L", "4,817", "₹373.06", "₹648.53", "₹267.88", "3.47x", "18.0%"],
        ["Mar 2026", "11,285", "₹85.32 L", "₹27.84 L", "6,351", "₹438.38", "₹786.17", "₹288.93", "2.14x", "18.8%"],
        ["Apr 2026", "10,551", "₹84.73 L", "₹32.55 L", "5,350", "₹608.41", "₹1,372.38", "₹322.14", "2.28x", "22.2%"],
        ["May 2026", "12,215", "₹100.96 L", "₹40.21 L", "7,076", "₹568.29", "₹1,444.15", "₹336.81", "2.27x", "25.2%"],
        ["Jun 2026", "12,877", "₹103.89 L", "₹42.86 L", "6,851", "₹625.67", "₹2,199.24", "₹276.86", "1.96x", "24.3%"],
        ["Jul 2026", "13,420", "₹103.64 L", "₹43.62 L", "8,313", "₹524.75", "₹1,077.07", "₹313.48", "1.80x", "27.6%"],
        ["Aug 2026", "11,069", "₹95.64 L", "₹82.75 L", "10,189", "₹812.16", "₹1,130.18", "₹368.65", "0.90x", "27.7%"],
        ["Sep 2026 (Comp)", "3,112", "₹36.02 L", "₹6.27 L", "801", "₹782.84", "₹7,568.93", "₹407.32", "4.54x*", "51.8%"],
        ["Oct 2026 (Festive)", "9,143", "₹105.67 L", "₹42.47 L", "7,298", "₹581.84", "₹636.72", "₹532.42", "2.14x", "35.2%"],
        ["Nov 2026 (Till 18th)", "4,638", "₹53.18 L", "₹19.09 L", "4,310", "₹443.00", "₹415.60", "₹474.96", "2.20x", "36.7%"],
        ["Comp Total (78d)", "16,893", "₹1.95 Cr", "₹67.83 L", "12,409", "₹546.60", "₹598.61", "₹500.65", "2.38x", "38.5%"]
    ]

    t_matrix = doc.add_table(rows=len(matrix_rows), cols=len(matrix_rows[0]))
    t_matrix.alignment = WD_TABLE_ALIGNMENT.CENTER

    for r_idx, r_vals in enumerate(matrix_rows):
        row = t_matrix.rows[r_idx]
        for c_idx, val in enumerate(r_vals):
            cell = row.cells[c_idx]
            cell.text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            r = p.runs[0]
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            
            if r_idx == 0:
                set_cell_background(cell, "102C57")
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
            elif r_idx >= 10 and r_idx <= 12:
                set_cell_background(cell, "FDEDEC") # Highlight competitor months
                r.font.color.rgb = RGBColor(140, 20, 20)
                if c_idx == 0:
                    r.font.bold = True
            elif r_idx == len(matrix_rows) - 1:
                set_cell_background(cell, "EAECEE")
                r.font.bold = True
                r.font.color.rgb = navy_color
            else:
                if r_idx % 2 == 1:
                    set_cell_background(cell, "F9F9F9")
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)

    # ---------------------------------------------------------------------------
    # SECTION 3: GOOGLE ADS FORENSIC AUTOPSY
    # ---------------------------------------------------------------------------
    h3 = doc.add_heading("3. Google Ads Forensic Audit: The Root Cause Diagnostics", level=1)
    h3.paragraph_format.space_before = Pt(14)

    p_g_intro = doc.add_paragraph(
        "During the competitor's 78-day tenure, Google Ads spend totaled ₹34,84,182.33 across 5,820 orders at an average CPA of ₹598.61. "
        "A forensic review of the account's change logs, asset groups, and search terms reveals why Google Ads collapsed:"
    )
    p_g_intro.paragraph_format.line_spacing = 1.15

    g_points = [
        ("1. Primary Conversion Tracking Deleted on Sep 18: ", 
         "In Change history report, on Sep 18 at 3:32 PM, competitor user 'sarjit@silverxis.com' executed 'Conversion Purchase-2026 removed'. "
         "This blinded Google's Smart Bidding (Target CPA / Target ROAS) algorithms. Without conversion signal feedback, Google Ads spent ₹3,17,895 "
         "in September to deliver ONLY 42 orders, resulting in an catastrophic CPA of ₹7,568.93 and a ROAS of 0.15x."),
        ("2. Copy-Pasting 'Glam+' Brand Ads into FABB6 PMax: ",
         "In Asset groups report, multiple live Performance Max campaigns (T4 Pro/Salon, T3 Premium, Pilgrim, YS24) were populated with headlines and copy "
         "stating: 'Beauty & Skincare Must-Haves, Glam+ Store', 'Glow Up with Glam+ | Save 5% on Premium Beauty & Personal Care Products | Shop Now', "
         "and descriptions promoting 'Glam+ beauty store'. FABB6 paid Google to advertise someone else's storefront. Furthermore, every single asset group "
         "had an Ad Strength rating of 'Poor'."),
        ("3. 140+ Hyperactive Budget Changes (Permanent Learning Phase): ",
         "The competitor modified budgets 140 times (74 increases, 66 decreases) in under 60 days. Frequently changing daily budgets resets Google's "
         "Smart Bidding learning period, preventing the bidding algorithm from ever exiting the exploration phase."),
        ("4. 110 Dead Landing Pages (404 Errors) Burning Capital: ",
         "In Product report, 216 products were flagged as ineligible, 110 products had 'Product page unavailable' (404 errors), and 70 products had promotional overlay violations. "
         "Over ₹80,285 was burned on zero-conversion products. For example, 'Foxtale 5% Niacinamide Face Serum' spent ₹1,614 across 480 clicks directly to a 404 page!"),
        ("5. Bidding on Gym & Badminton Keywords in 'Brand' Search: ",
         "In Search keyword report and Search terms report, a campaign titled 'Search-Brand' had broad match keywords like 'skincare shops', 'best korean cosmetics website', "
         "and ads triggered for 'gym equipment for girls at home', 'badminton ankle support', and 'multi exercise push up board', which got flagged as 'campaign paused; low quality'.")
    ]
    for b_title, b_desc in g_points:
        bp = doc.add_paragraph(style='List Bullet')
        r1 = bp.add_run(b_title)
        r1.bold = True
        r1.font.color.rgb = dark_red
        r2 = bp.add_run(b_desc)
        bp.paragraph_format.space_after = Pt(4)

    # Google Campaign Table
    p_g_tbl_lbl = doc.add_paragraph()
    p_g_tbl_lbl.add_run("Table 3.1: Google Ads Monthly Breakdown (August – November 2026)").bold = True
    p_g_tbl_lbl.paragraph_format.space_before = Pt(8)

    g_camp_rows = [
        ["Period", "Google Spend (₹)", "Google Orders", "Google CPA (₹)", "Conv. Value (₹)", "ROAS", "Status Summary"],
        ["August 2026 (Baseline)", "₹67,06,703.19", "5,934.18", "₹1,130.18", "₹73,13,357.57", "1.09x", "Legacy PMax recovering"],
        ["September 2026 (Crash)", "₹3,17,894.98", "42.00", "₹7,568.93", "₹46,329.15", "0.15x", "Purchase-2026 deleted on Sep 18"],
        ["October 2026 (Festive)", "₹22,02,105.54", "3,458.49", "₹636.72", "₹42,60,925.37", "1.93x", "PMax flooded with Glam+ copy"],
        ["November 2026 (Till 18th)", "₹9,64,181.81", "2,319.99", "₹415.60", "₹28,68,058.46", "2.97x", "Frantic budget cuts by competitor"],
        ["Competitor Run (78d)", "₹34,84,182.33", "5,820.48", "₹598.61", "₹71,75,312.98", "2.06x", "Blinded Smart Bidding & 404 Waste"]
    ]
    t_g = doc.add_table(rows=len(g_camp_rows), cols=len(g_camp_rows[0]))
    t_g.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, r_vals in enumerate(g_camp_rows):
        row = t_g.rows[r_idx]
        for c_idx, val in enumerate(r_vals):
            cell = row.cells[c_idx]
            cell.text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.runs[0]
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if r_idx == 0:
                set_cell_background(cell, "102C57")
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
            elif r_idx == 2:
                set_cell_background(cell, "FDEDEC")
                r.font.bold = True
                r.font.color.rgb = dark_red
            elif r_idx == len(g_camp_rows) - 1:
                set_cell_background(cell, "EAECEE")
                r.font.bold = True
            set_cell_margins(cell, top=60, bottom=60, left=70, right=70)

    # ---------------------------------------------------------------------------
    # SECTION 4: META ADS FORENSIC AUTOPSY
    # ---------------------------------------------------------------------------
    h4 = doc.add_heading("4. Meta Ads Forensic Audit: The Structural Collapse", level=1)
    h4.paragraph_format.space_before = Pt(14)

    p_m_intro = doc.add_paragraph(
        "Meta Ads was the primary growth engine of FABB6, historically delivering 5,600–6,000 orders/month at ₹276–₹313 CPA. "
        "Under the competitor agency, Meta ad spend totaled ₹32,98,795.65 for 6,589 purchases at an inflated CPA of ₹500.65. "
        "The forensic autopsy of Meta Ads exports reveals six fatal structural blunders:"
    )
    p_m_intro.paragraph_format.line_spacing = 1.15

    m_points = [
        ("1. The Retargeting Cost Inversion (DPA Blunder): ",
         "'Retargeting — DPA - Fabb6' spent ₹9,50,354.11 for 1,850 purchases at an average CPA of ₹513.70 (peaked at ₹570.31 in October). "
         "In e-commerce, retargeting warm audiences should have a CPA 40%–60% lower than cold traffic (benchmark: ₹160–₹220). "
         "Here, retargeting was MORE EXPENSIVE than cold Advantage+ prospecting (₹479.53) because of zero customer exclusions and frequency burnout (3.21)."),
        ("2. Internal Advantage+ Auction Self-Cannibalization (+144% CPM Inflation): ",
         "The competitor ran 3 separate Advantage+ Shopping Campaigns simultaneously ('Advantage+ Sales — Fabb6', 'Advantage+ Sales – Best Seller', 'Advantage+ Sales Combo Products') "
         "without audience or product exclusions. As a result, Meta's algorithm bid against itself, sending account CPM from ₹56.15 in August to ₹104.17 in October (+85%) and ₹137.03 in November (+144%)."),
        ("3. The ₹50,000 Link-Click Black Hole ('IG-Traffic'): ",
         "'IG-Traffic' burned ₹50,214.27 across 8.32 million impressions for 1,02,322 link clicks, delivering ZERO PURCHASES. "
         "Out of 102,322 clicks, only 28 users actually loaded the website (99.97% drop-off!). Optimizing for 'Link Clicks' fed budget straight to bots and accidental thumb-swipers."),
        ("4. Extreme Frequency Abuse on iOS App Ads (Frequency 13.18): ",
         "'New App promotion Campaign iOS' burned ₹19,161 on 24,422 users at an absurd frequency of 13.18. Prospective iOS users saw the ad 13 times each in a single month, "
         "delivering zero sales and an inflated CPC of ₹30.86. Similarly, 'App-BTG-03072026' spent ₹1.38 Lakhs at a CPA of ₹1,082.14."),
        ("5. The 56.5% Click-to-Landing-Page Drop-Off Crisis: ",
         "Across the competitor's run, Meta reported 7,34,064 link clicks, but only 3,01,798 Landing Page Views registered on Shopify. Over 4.32 lakh clicks (56.5%) "
         "were lost in transit due to slow mobile loading and misfiring server-side CAPI event tracking."),
        ("6. Complete Neglect of the 36.7% Repeat Customer Base: ",
         "The competitor treated every single ad as cold prospecting. There was zero custom audience segmentation for past 30-day, 60-day, or 90-day purchasers, "
         "and zero replenishment flows, ignoring FABB6's most profitable asset.")
    ]
    for b_title, b_desc in m_points:
        bp = doc.add_paragraph(style='List Bullet')
        r1 = bp.add_run(b_title)
        r1.bold = True
        r1.font.color.rgb = dark_red
        r2 = bp.add_run(b_desc)
        bp.paragraph_format.space_after = Pt(4)

    # Meta Campaign Table
    p_m_tbl_lbl = doc.add_paragraph()
    p_m_tbl_lbl.add_run("Table 4.1: Meta Ads Granular Campaign Scorecard (Sep 1 – Nov 18, 2026)").bold = True
    p_m_tbl_lbl.paragraph_format.space_before = Pt(8)

    m_camp_rows = [
        ["Campaign Name", "Spend (₹)", "Share", "Purchases", "CPA (₹)", "CPM (₹)", "Freq", "LPV Loss", "Operational Verdict"],
        ["Advantage+ Sales — Fabb6", "₹11,38,878", "34.5%", "2,375", "₹479.53", "₹146.71", "3.14", "28.9%", "Unsegmented cold ASC; CPA inflated"],
        ["Retargeting — DPA - Fabb6", "₹9,50,354", "28.8%", "1,850", "₹513.70", "₹155.47", "3.21", "34.1%", "Cost Inversion: Retargeting > Prospecting"],
        ["Advantage+ Sales — Best Seller", "₹5,68,931", "17.3%", "1,361", "₹418.02", "₹135.12", "3.60", "27.8%", "Internal auction cannibalization"],
        ["Lookalike Audience Campaign", "₹3,88,279", "11.8%", "735", "₹528.27", "₹205.07", "2.57", "33.0%", "Highest CPM in account; obsolete targeting"],
        ["App-BTG-03072026", "₹1,38,513", "4.2%", "128", "₹1,082.14", "₹18.07", "2.90", "99.8%", "1.9L clicks, only 372 loaded store"],
        ["IG-Traffic", "₹50,214", "1.5%", "0", "₹0.00", "₹6.04", "1.58", "100.0%", "100% Waste: 1.02L clicks, 0 purchases"],
        ["New App promo Campaign iOS", "₹19,161", "0.6%", "0", "₹0.00", "₹59.52", "13.18", "100.0%", "Frequency Abuse: hit users 13 times each"],
        ["All Other Minor Campaigns", "₹44,466", "1.3%", "140", "₹317.61", "—", "—", "—", "Fragmented ad sets with minor spend"],
        ["Total Meta Ads Run", "₹32,98,796", "100.0%", "6,589", "₹500.65", "₹102.83", "2.76", "56.5%", "Acute Structural Failure"]
    ]
    t_m = doc.add_table(rows=len(m_camp_rows), cols=len(m_camp_rows[0]))
    t_m.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, r_vals in enumerate(m_camp_rows):
        row = t_m.rows[r_idx]
        for c_idx, val in enumerate(r_vals):
            cell = row.cells[c_idx]
            cell.text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx > 0 and c_idx < 8 else (WD_ALIGN_PARAGRAPH.RIGHT if c_idx == 1 else WD_ALIGN_PARAGRAPH.LEFT)
            r = p.runs[0]
            r.font.name = "Calibri"
            r.font.size = Pt(8)
            if r_idx == 0:
                set_cell_background(cell, "102C57")
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
            elif "Cost Inversion" in val or "100% Waste" in val or "Frequency Abuse" in val:
                set_cell_background(cell, "FDEDEC")
                r.font.color.rgb = dark_red
                r.font.bold = True
            elif r_idx == len(m_camp_rows) - 1:
                set_cell_background(cell, "EAECEE")
                r.font.bold = True
            set_cell_margins(cell, top=60, bottom=60, left=60, right=60)

    # ---------------------------------------------------------------------------
    # SECTION 5: QUANTIFIED BUDGET WASTE BREAKDOWN
    # ---------------------------------------------------------------------------
    h5 = doc.add_heading("5. Quantifiable Avoidable Budget Waste Breakdown (₹7.46 Lakhs)", level=1)
    h5.paragraph_format.space_before = Pt(14)

    p_w_intro = doc.add_paragraph(
        "Based on granular log analysis, we have mathematically isolated ₹7,46,558.00 in direct, avoidable capital loss "
        "caused by competitor agency mismanagement:"
    )
    p_w_intro.paragraph_format.space_after = Pt(4)

    waste_table_rows = [
        ["Waste Category", "Forensic Root Cause & Mechanism", "Wasted Capital (INR)"],
        ["Deleted Conversion Action Choke", "Google tracking deleted on Sep 18; CPA rose to ₹7,569 vs normal ₹550", "₹2,94,800.00"],
        ["Merchant Center 404 & Dead SKUs", "Paid clicks sent to 110 broken landing pages (Foxtale serum 480 dead clicks)", "₹80,285.00"],
        ["Zero-Conversion Meta Traffic Ads", "IG-Traffic link-click campaign burned 8.3M impressions for 0 purchases", "₹50,214.00"],
        ["Unoptimized App Install Ad Waste", "iOS & Android app ads running at a frequency of 13.18, CPA > ₹1,080", "₹1,57,674.00"],
        ["Broad Match Non-Beauty Bleed", "Performance Max ads showing for gym equipment, push-up board, etc.", "₹45,585.00"],
        ["Internal ASC Auction Self-Bidding", "Overlapping Advantage+ campaigns bidding against each other (CPM penalty)", "₹1,18,000.00"],
        ["TOTAL AVOIDABLE CAPITAL WASTE", "Pure Capital Incinerated by Competitor Mismanagement", "₹7,46,558.00"]
    ]
    t_w = doc.add_table(rows=len(waste_table_rows), cols=len(waste_table_rows[0]))
    t_w.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, r_vals in enumerate(waste_table_rows):
        row = t_w.rows[r_idx]
        for c_idx, val in enumerate(r_vals):
            cell = row.cells[c_idx]
            cell.text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if c_idx == 2 else WD_ALIGN_PARAGRAPH.LEFT
            r = p.runs[0]
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if r_idx == 0:
                set_cell_background(cell, "8B0000") # Crimson
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
            elif r_idx == len(waste_table_rows) - 1:
                set_cell_background(cell, "FADBD8")
                r.font.bold = True
                r.font.color.rgb = dark_red
            else:
                if r_idx % 2 == 1:
                    set_cell_background(cell, "FDFEFE")
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)

    # ---------------------------------------------------------------------------
    # SECTION 6: 90-DAY TURNAROUND ROADMAP
    # ---------------------------------------------------------------------------
    h6 = doc.add_heading("6. Techno Exponent 90-Day Turnaround Roadmap", level=1)
    h6.paragraph_format.space_before = Pt(14)

    phases = [
        ("Phase 1: 14-Day Emergency Triage (Week 1–2) — Stop the Bleeding", [
            "Purge All Foreign Ad Copy: Immediately eradicate every instance of 'Glam+' headlines and copy from PMax; deploy high-converting professional beauty ad copy.",
            "Re-establish Tracking Integrity: Re-implement Google Ads Enhanced Conversions for Web and Meta CAPI deduplication via native Shopify gateway (Target EMQ > 8.5).",
            "Cleanse Google Merchant Center: Unpublish or redirect the 110 products throwing 404 errors, fix 70 image overlays, and add negative keyword list.",
            "Terminate Wasteful Campaigns: Pause IG-Traffic, unoptimized app campaigns, and consolidate Meta into 1 Master ASC (TOF) + 1 DPA Retargeting (MOF) + 1 Retention (BOF)."
        ]),
        ("Phase 2: 30-Day Stabilization (Month 1 - December 2026) — Restore Unit Economics", [
            "Restructure Google PMax Catalog: Segment PMax into 3 margin-tiered asset groups (Core Best Sellers, High ASP, Catch-All) on target ROAS.",
            "Drive Meta CPA Under ₹320: Refresh creative assets (before/after salon reels, routine bundles, UGC unboxing) to cut CPA by 35%-40%.",
            "Monetize 36.7% Repeat Base: Launch automated WhatsApp & Klaviyo replenishment flows triggered at 30, 45, and 60 days based on product consumption cycles (< ₹60 CPA).",
            "Month 1 Target: Deliver 12,400+ total orders in December at Blended CPA ≤ ₹348.84 and Net ROAS ≥ 3.73x."
        ]),
        ("Phase 3: 60–90 Day Profitable Scaling (January – February 2027) — Reaching 650+ Daily Orders", [
            "Scale Ad Spend Sustainably: Step monthly budget up from ₹30L to ₹40L adhering strictly to the ≤ 20% budget increase every 72 hours scaling guardrail.",
            "Scale Order Run-Rate: Expand daily orders from ~216/day to 650–750 orders/day (18,000–21,000 orders/month).",
            "Stabilize Compounding Profitability: Maintain Blended Paid CPA between ₹260–₹285 and Blended ROAS between 4.2x–4.5x."
        ])
    ]
    for ph_title, ph_tasks in phases:
        p_ph = doc.add_paragraph()
        p_ph.paragraph_format.space_before = Pt(6)
        r_ph = p_ph.add_run(ph_title)
        r_ph.bold = True
        r_ph.font.name = "Calibri"
        r_ph.font.size = Pt(11)
        r_ph.font.color.rgb = navy_color
        for task in ph_tasks:
            pt = doc.add_paragraph(style='List Bullet')
            pt.paragraph_format.space_after = Pt(2)
            r_t = pt.add_run(task)
            r_t.font.name = "Calibri"
            r_t.font.size = Pt(9.5)

    # ---------------------------------------------------------------------------
    # SECTION 7: CALIBRATED 3-MONTH TURNAROUND FINANCIAL FORECAST
    # ---------------------------------------------------------------------------
    h7 = doc.add_heading("7. Calibrated 3-Month Turnaround Financial Forecast (Dec 2026 – Feb 2027)", level=1)
    h7.paragraph_format.space_before = Pt(14)

    p_f_intro = doc.add_paragraph(
        "The financial turnaround model for Q1 (December 2026 – February 2027) establishes a calibrated, phased roadmap "
        "rebalancing media spend to channel-specific historical strengths: scaling Google Ads to capture surging Q4/winter "
        "search and shopping intent, while stabilizing Meta Ads within its proven high-efficiency budget window. "
        "Ad spend initiates at ₹26.0 Lakhs in December (Google: ₹16L, Meta: ₹10L), safely below the current run-rate, "
        "and expands systematically to ₹34.1 Lakhs by February. Total store order volume scales from 8,874 to 12,053 monthly orders, "
        "expanding gross store revenue to ₹1.48 Cr+ at a 4.35x blended ROAS."
    )
    p_f_intro.paragraph_format.line_spacing = 1.15
    p_f_intro.paragraph_format.space_after = Pt(6)

    # 7.1 Google Ads Table
    h7_1 = doc.add_heading("7.1 Google Ads 3-Month Performance Forecast", level=2)
    h7_1.paragraph_format.space_before = Pt(8)

    g_table_rows = [
        ["Month", "Optimization Focus", "Google Budget (₹)", "Target CPA (₹)", "Orders", "Daily Orders", "AOV (₹)", "Expected Revenue (₹)", "ROAS"],
        ["Nov 2026 (Run-Rate)", "Baseline: PMax recovering from 404 URLs & foreign copy", "₹16,07,000", "₹415.60", "3,860", "129", "₹1,236", "₹47,71,850", "2.97x"],
        ["Dec 2026", "Triage: 16L budget, 404 URL exclusion, purge Glam+ copy", "₹16,00,000", "₹450.00", "3,556", "115", "₹1,014", "₹36,05,333", "2.25x"],
        ["Jan 2027", "Scaling: 20L budget, PMax feed cleanup, high-margin SKU push", "₹20,00,000", "₹430.00", "4,651", "150", "₹1,103", "₹51,30,233", "2.57x"],
        ["Feb 2027", "Expansion: 22L budget, non-brand search, 3.00x ROAS target", "₹22,00,000", "₹410.00", "5,366", "192", "₹1,232", "₹66,10,732", "3.00x"],
        ["3-Month Total", "Google Ads Scaled Turnaround", "₹58,00,000", "₹427.32", "13,573", "151/day", "₹1,131", "₹1,53,46,298", "2.65x"]
    ]
    t_g = doc.add_table(rows=len(g_table_rows), cols=len(g_table_rows[0]))
    t_g.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, r_vals in enumerate(g_table_rows):
        row = t_g.rows[r_idx]
        for c_idx, val in enumerate(r_vals):
            cell = row.cells[c_idx]
            cell.text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [3, 4, 5, 8] else (WD_ALIGN_PARAGRAPH.RIGHT if c_idx in [2, 6, 7] else WD_ALIGN_PARAGRAPH.LEFT)
            r = p.runs[0]
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if r_idx == 0:
                set_cell_background(cell, "102C57")
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
            elif r_idx == len(g_table_rows) - 1:
                set_cell_background(cell, "EAECEE")
                r.font.bold = True
                r.font.color.rgb = navy_color
            else:
                if r_idx == 1:
                    set_cell_background(cell, "F2F4F4")
                    r.font.italic = True
                elif r_idx % 2 == 1:
                    set_cell_background(cell, "F9F9F9")
            set_cell_margins(cell, top=50, bottom=50, left=60, right=60)

    # 7.2 Meta Ads Table
    h7_2 = doc.add_heading("7.2 Meta Ads 3-Month Performance Forecast", level=2)
    h7_2.paragraph_format.space_before = Pt(10)

    m_table_rows = [
        ["Month", "Optimization Focus", "Meta Budget (₹)", "Target CPA (₹)", "Orders", "Daily Orders", "AOV (₹)", "Expected Revenue (₹)", "ROAS"],
        ["Nov 2026 (Run-Rate)", "Baseline: Inverted DPA & dead traffic ad burn", "₹15,75,000", "₹474.96", "3,315", "111", "₹1,245", "₹41,26,300", "2.62x"],
        ["Dec 2026", "Triage: 10L budget, kill traffic ad, 30-day DPA exclusions", "₹10,00,000", "₹450.00", "2,222", "72", "₹1,014", "₹22,53,333", "2.25x"],
        ["Jan 2027", "Restructure: 11L budget, Advantage+ Shopping consolidation", "₹11,00,000", "₹410.00", "2,683", "87", "₹1,103", "₹29,59,268", "2.69x"],
        ["Feb 2027", "Restoration: 12.1L budget, scale proven creative hooks", "₹12,10,000", "₹385.00", "3,143", "112", "₹1,232", "₹38,72,000", "3.20x"],
        ["3-Month Total", "Meta Ads Consolidated Turnaround", "₹33,10,000", "₹411.28", "8,048", "89/day", "₹1,129", "₹90,84,601", "2.74x"]
    ]
    t_m = doc.add_table(rows=len(m_table_rows), cols=len(m_table_rows[0]))
    t_m.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, r_vals in enumerate(m_table_rows):
        row = t_m.rows[r_idx]
        for c_idx, val in enumerate(r_vals):
            cell = row.cells[c_idx]
            cell.text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [3, 4, 5, 8] else (WD_ALIGN_PARAGRAPH.RIGHT if c_idx in [2, 6, 7] else WD_ALIGN_PARAGRAPH.LEFT)
            r = p.runs[0]
            r.font.name = "Calibri"
            r.font.size = Pt(8.5)
            if r_idx == 0:
                set_cell_background(cell, "102C57")
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
            elif r_idx == len(m_table_rows) - 1:
                set_cell_background(cell, "EAECEE")
                r.font.bold = True
                r.font.color.rgb = navy_color
            else:
                if r_idx == 1:
                    set_cell_background(cell, "F2F4F4")
                    r.font.italic = True
                elif r_idx % 2 == 1:
                    set_cell_background(cell, "F9F9F9")
            set_cell_margins(cell, top=50, bottom=50, left=60, right=60)

    # 7.3 Total Store & Blended Performance Table
    h7_3 = doc.add_heading("7.3 Total Store & Blended Performance Forecast (Shopify + Paid Ads + Retention)", level=2)
    h7_3.paragraph_format.space_before = Pt(10)

    b_table_rows = [
        ["Month", "Total Paid Spend (₹)", "Paid Orders", "Paid CPA (₹)", "Orders from Others*", "Total Store Orders", "Daily Orders", "Gross Revenue (₹)", "Store Blended CPA (₹)", "ROAS on Total"],
        ["Nov 2026 (Run-Rate)", "₹31,82,000", "7,175", "₹443.48", "4,163", "11,338", "378", "₹1,40,13,000", "₹280.65", "4.40x"],
        ["Dec 2026", "₹26,00,000", "5,778", "₹450.00", "3,096", "8,874", "296", "₹89,98,011", "₹293.00", "3.46x"],
        ["Jan 2027", "₹31,00,000", "7,334", "₹422.68", "3,313", "10,647", "355", "₹1,17,43,431", "₹291.17", "3.79x"],
        ["Feb 2027", "₹34,10,000", "8,509", "₹400.77", "3,545", "12,053", "402", "₹1,48,49,692", "₹282.91", "4.35x"],
        ["3-Month Total", "₹91,10,000", "21,621", "₹421.35", "9,953", "31,574", "351/day", "₹3,55,91,133", "₹288.53", "3.91x"]
    ]
    t_b = doc.add_table(rows=len(b_table_rows), cols=len(b_table_rows[0]))
    t_b.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, r_vals in enumerate(b_table_rows):
        row = t_b.rows[r_idx]
        for c_idx, val in enumerate(r_vals):
            cell = row.cells[c_idx]
            cell.text = val
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [2, 4, 5, 6, 9] else (WD_ALIGN_PARAGRAPH.RIGHT if c_idx in [1, 3, 7, 8] else WD_ALIGN_PARAGRAPH.LEFT)
            r = p.runs[0]
            r.font.name = "Calibri"
            r.font.size = Pt(8.0)
            if r_idx == 0:
                set_cell_background(cell, "102C57")
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
            elif r_idx == len(b_table_rows) - 1:
                set_cell_background(cell, "EAECEE")
                r.font.bold = True
                r.font.color.rgb = navy_color
            else:
                if r_idx == 1:
                    set_cell_background(cell, "F2F4F4")
                    r.font.italic = True
                elif r_idx % 2 == 1:
                    set_cell_background(cell, "F9F9F9")
            set_cell_margins(cell, top=50, bottom=50, left=50, right=50)

    # ---------------------------------------------------------------------------
    # SECTION 8: OPERATIONAL EXECUTION & IMMEDIATE ACCOUNT RESTORATION
    # ---------------------------------------------------------------------------
    h8 = doc.add_heading("8. Operational Execution & Immediate Account Restoration Protocol", level=1)
    h8.paragraph_format.space_before = Pt(14)

    p_ob = doc.add_paragraph(
        "Techno Exponent has already verified full Admin access across Google Ads, Meta Business Suite, "
        "Google Merchant Center, and Shopify (assigned to subhranilnaskar@technoexponent.com). With access fully confirmed, "
        "the team is initiating the following immediate 48-hour execution sprint to halt budget bleed and stabilize account economics:"
    )
    p_ob.paragraph_format.line_spacing = 1.15

    ob_steps = [
        ("Step 1 (Immediate - Hours 0 to 4): Access Verified & Emergency Bleed Termination", "Admin access confirmed. Immediately pause the ₹50,000 dead IG-Traffic link-click campaign, pause zombie app promotion ads, and purge all 'Glam+' copy-paste assets from Google PMax asset groups."),
        ("Step 2 (Day 1 - Hours 4 to 24): Catalog Hygiene & 404 URL Exclusion", "Disapprove and exclude all 110 broken 404 URLs in Google Merchant Center to halt zero-conversion click drain. Verify Google Ads Enhanced Conversions tracking and test Meta CAPI server-side event deduplication on Shopify."),
        ("Step 3 (Day 2 - Hours 24 to 48): Audience Exclusions & Retargeting Reset", "Inject 30-day and 180-day customer exclusion custom audiences into Meta Dynamic Product Ads (DPA) to immediately cure the ₹513 retargeting CPA inversion. Implement frequency capping at ≤ 2.2 impressions/week."),
        ("Step 4 (Day 2+): Restructured Campaign Launch", "Deploy 1 Master TOF Advantage+ Shopping Campaign (ASC) with a 20% existing customer budget cap, 1 Clean DPA Retargeting set, and 1 High-Margin PMax structure with segmented listing groups.")
    ]
    for st_title, st_desc in ob_steps:
        bp = doc.add_paragraph(style='List Bullet')
        r1 = bp.add_run(st_title + ": ")
        r1.bold = True
        r1.font.name = "Calibri"
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = navy_color
        r2 = bp.add_run(st_desc)
        r2.font.name = "Calibri"
        r2.font.size = Pt(9.5)
        bp.paragraph_format.space_after = Pt(2)

    # Save DOCX
    doc.save(docx_path)
    print(f"Successfully generated DOCX at: {docx_path}")

    # Also copy DOCX to case-studies
    cs_docx_path = r"C:\Users\test\Videos\Office\case-studies\fabb6\FABB6_Forensic_Audit_Report_Google_and_Meta_Ads.docx"
    doc.save(cs_docx_path)
    print(f"Copied DOCX to: {cs_docx_path}")

    # 2. Convert to PDF using Microsoft Word COM Automation
    print("Converting DOCX to PDF via Microsoft Word...")
    try:
        word = win32com.client.Dispatch("Word.Application")
        word.Visible = False
        doc_word = word.Documents.Open(docx_path)
        # 17 = wdFormatPDF
        doc_word.SaveAs(pdf_path, FileFormat=17)
        doc_word.Close()
        word.Quit()
        print(f"Successfully converted and generated PDF at: {pdf_path}")
        
        # Copy PDF to case-studies as well
        cs_pdf_path = r"C:\Users\test\Videos\Office\case-studies\fabb6\FABB6_Forensic_Audit_Report_Google_and_Meta_Ads.pdf"
        import shutil
        shutil.copyfile(pdf_path, cs_pdf_path)
        print(f"Copied PDF to: {cs_pdf_path}")
    except Exception as e:
        print(f"Error converting to PDF via Word COM: {e}")

if __name__ == '__main__':
    build_forensic_doc()
