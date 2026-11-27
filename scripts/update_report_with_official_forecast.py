import re

path = r"C:\Users\test\Videos\Office\scripts\generate_client_forensic_doc_and_pdf.py"

with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Replace Section 7 with exact official numbers from Google Sheet
target_sec7 = r"(    # ---------------------------------------------------------------------------\n    # SECTION 7: CALIBRATED 3-MONTH TURNAROUND FINANCIAL FORECAST[\s\S]*?)(    # ---------------------------------------------------------------------------\n    # SECTION 8: OPERATIONAL EXECUTION & IMMEDIATE ACCOUNT RESTORATION)"

replacement_sec7 = """    # ---------------------------------------------------------------------------
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

"""

new_text = re.sub(target_sec7, replacement_sec7 + r"\2", text)

with open(path, "w", encoding="utf-8") as f:
    f.write(new_text)

print("SUCCESS: Updated Section 7 in generate_client_forensic_doc_and_pdf.py")
