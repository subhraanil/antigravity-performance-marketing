import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import win32com.client
import pythoncom
import pypdf

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=35, bottom=35, left=50, right=50):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{color}"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def build_docx_report(output_path):
    doc = docx.Document()
    
    # Page setup - 0.50 in top/bottom, 0.60 in left/right
    for section in doc.sections:
        section.top_margin = Inches(0.50)
        section.bottom_margin = Inches(0.50)
        section.left_margin = Inches(0.60)
        section.right_margin = Inches(0.60)
        
    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(9.5)
    normal_style.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    
    # =========================================================================
    # PAGE 1: COVER HEADER & 1. EXECUTIVE SCORECARD (10 MAJOR MILESTONES)
    # =========================================================================
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(1)
    title_run = title_p.add_run("SHARE SAMADHAN LIMITED")
    title_run.font.size = Pt(21)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(0x0A, 0x25, 0x40) # Deep Navy
    
    subtitle_p = doc.add_paragraph()
    subtitle_p.paragraph_format.space_before = Pt(0)
    subtitle_p.paragraph_format.space_after = Pt(8)
    subtitle_run = subtitle_p.add_run("Annual Performance & Year-over-Year (YoY) Growth Audit (Nov 2025 – Nov 2026)")
    subtitle_run.font.size = Pt(11)
    subtitle_run.font.bold = True
    subtitle_run.font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
    
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(0)
    h1.paragraph_format.space_after = Pt(4)
    r_h1 = h1.add_run("1. Executive Scorecard: 10 Major Growth Milestones")
    r_h1.font.size = Pt(12.5)
    r_h1.font.bold = True
    r_h1.font.color.rgb = RGBColor(0x0A, 0x25, 0x40)
    
    milestones_data = [
        ("1. Total Digital Leads (CRM)", "527 leads / mo", "1,712 leads / mo (Sep '26)", "+224.9% Volume Growth (13,384 Verified Digital Leads)"),
        ("2. Paid Media Leads (Google+Meta)", "440 leads / mo", "1,689 leads / mo (Oct '26)", "+283.9% Monthly Scale; YoY Paid Leads: 10,376 → 12,695 (+22.3% ▲)"),
        ("3. Blended Cost Per Lead (CPL)", "₹141.23 – ₹180.11", "₹54.98 – ₹55.72", "-60.5% to -69.5% CPL Compression (Saved ₹125+/lead ▼)"),
        ("4. Meta Ads CPL Revolution", "₹161.58 – ₹287.65", "₹32.74 (Oct '26)", "-88.6% Monthly Reduction; YoY CPL dropped from ₹111 to ₹81 (-27.0% ▼)"),
        ("5. Google Ads Intent & Quality Scale", "208 leads / mo", "775 leads / mo (Jul '26)", "+272.6% Scale; YoY Leads: 5,551 → 6,203 (+11.7% ▲) & +2.8% Clicks ▲"),
        ("6. Google Search Impressions (GSC)", "1.75 Million (Prior)", "1.99 Million (Recent)", "+13.7% Search Visibility Surge (3,090,000+ Total Impressions ▲)"),
        ("7. High-Intent Organic Clicks", "24,100 (Prior)", "35,300 (Recent)", "+46.5% Organic Click Surge ▲ (44,100 Total Clicks; Avg Rank 7.1)"),
        ("8. Page 1 Google Rankings", "48 Keywords", "72 Keywords (Top 10)", "+50.0% Increase in Page 1 Category Monopoly for Loss of Shares & IEPF ▲"),
        ("9. Total Website Audience (GA4)", "127,920 (Prior Year)", "161,781 Users", "+26.5% Audience Scale ▲; New Users reached 161,741 (+34.8% YoY ▲)"),
        ("10. High-Value Organic Leads", "Baseline", "2,685 Organic Leads", "6.71% Visitor-to-Lead Conversion Rate (39.9K Organic Visitors)"),
    ]
    
    t_m = doc.add_table(rows=len(milestones_data) + 1, cols=4)
    t_m.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_m)
    
    headers_m = ["Performance Pillar", "Baseline / Prior Period", "Peak / Current Performance", "Net Improvement & Milestone"]
    widths_m = [Inches(2.1), Inches(1.4), Inches(1.6), Inches(2.4)]
    
    for c_idx, text in enumerate(headers_m):
        cell = t_m.cell(0, c_idx)
        cell.width = widths_m[c_idx]
        set_cell_background(cell, "0A2540")
        set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(milestones_data):
        row = t_m.rows[r_idx + 1]
        bg = "F8F9FA" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, text in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = widths_m[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=35, bottom=35, left=60, right=60)
            p = cell.paragraphs[0]
            run = p.add_run(text)
            run.font.size = Pt(7.5)
            if c_idx == 0 or c_idx == 3:
                run.bold = True
                
    doc.add_page_break() # CLEAN TRANSITION TO PAGE 2
    
    # =========================================================================
    # PAGE 2: YEAR-OVER-YEAR (YoY) MULTI-CHANNEL PERFORMANCE BENCHMARK
    # =========================================================================
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(0)
    h2.paragraph_format.space_after = Pt(2)
    r_h2 = h2.add_run("2. Year-over-Year (YoY) Multi-Channel Performance Benchmark")
    r_h2.font.size = Pt(12.5)
    r_h2.font.bold = True
    r_h2.font.color.rgb = RGBColor(0x0A, 0x25, 0x40)
    
    # Key Takeaways Box
    summary_box = doc.add_table(rows=1, cols=1)
    summary_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_cell = summary_box.cell(0, 0)
    set_cell_background(s_cell, "F4FBF7") # Soft Mint Tint
    set_cell_margins(s_cell, top=40, bottom=40, left=70, right=70)
    p_box = s_cell.paragraphs[0]
    p_box.paragraph_format.space_before = Pt(0)
    p_box.paragraph_format.space_after = Pt(0)
    r_b1 = p_box.add_run("Executive YoY Growth & Strategic Quality Optimization Highlights:\n")
    r_b1.bold = True
    r_b1.font.size = Pt(8.5)
    r_b1.font.color.rgb = RGBColor(0x0E, 0x62, 0x51)
    
    bullets = (
        "• Google Ads Search Intent & Quality Focus: Raw impressions were deliberately reduced by -57.0% to prune non-converting search queries. "
        "Through strict negative filtering and high-intent targeting, Clicks increased (+2,181 clicks, 79.2K → 81.4K) and Leads expanded by +11.7% (5,551 → 6,203 leads).\n"
        "• Meta Ads Scale & Cost Efficiency: Generated +1,667 additional leads (+34.5% surge to 6,492 leads) and tripled click volume (+199.1% to 55,862 clicks) "
        "while slashing CPL by -27.0% (from ₹111 down to ₹81, saving ₹30 per lead).\n"
        "• Substantial Audience Scale (GA4): Total website users expanded by +26.5% YoY (127,920 → 161,781 users) with New Users jumping by +34.8% YoY (119,994 → 161,741).\n"
        "• Accelerating Search Visibility (GSC): Organic Google Search clicks surged by +46.5% (24,100 → 35,300 clicks), impressions grew to 1.99M, and Page 1 Top 10 rankings expanded by +50.0% (48 → 72 keywords)."
    )
    r_b2 = p_box.add_run(bullets)
    r_b2.font.size = Pt(7.5)
    
    # Table 2.1: Google Ads YoY
    p_g = doc.add_paragraph("Table 2.1: Google Ads Year-over-Year (YoY) Performance Benchmark (Quality & Lead Scale)")
    p_g.paragraph_format.space_before = Pt(4)
    p_g.paragraph_format.space_after = Pt(2)
    p_g.runs[0].bold = True
    p_g.runs[0].font.size = Pt(8.5)
    p_g.runs[0].font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
    
    t_g = doc.add_table(rows=4, cols=6)
    set_table_borders(t_g)
    headers_g = ["Performance Year", "Impressions", "Clicks", "Leads", "Spend (₹)", "Cost / Lead (₹)"]
    widths_g = [Inches(1.8), Inches(1.1), Inches(1.1), Inches(1.1), Inches(1.2), Inches(1.2)]
    data_g = [
        ("Oct 2024 - Oct 2025 (Baseline)", "1,786,105", "79,222", "5,551", "₹4,15,578", "₹75"),
        ("Nov 2025 - Nov 2026 (Agency Period)", "767,474", "81,403", "6,203", "₹5,92,977", "₹96"),
        ("Net Growth & Quality Optimization Delta", "-57.0% (Pruned Waste)", "+2,181 Clicks (+2.8% ▲)", "+652 Leads (+11.7% ▲)", "+₹1,77,399", "+₹21 (High Intent)"),
    ]
    for c_idx, text in enumerate(headers_g):
        cell = t_g.cell(0, c_idx)
        cell.width = widths_g[c_idx]
        set_cell_background(cell, "0A2540")
        set_cell_margins(cell, top=30, bottom=30, left=45, right=45)
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(7.0)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(data_g):
        bg = "D4EFDF" if r_idx == 2 else ("E8F8F5" if r_idx == 1 else "FFFFFF")
        for c_idx, text in enumerate(row_data):
            cell = t_g.cell(r_idx + 1, c_idx)
            cell.width = widths_g[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=25, bottom=25, left=45, right=45)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if c_idx >= 1 else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(text)
            run.font.size = Pt(7.0)
            if r_idx in [1, 2] or c_idx == 0:
                run.bold = True
            if r_idx == 2 and c_idx in [2, 3]:
                run.font.color.rgb = RGBColor(0x0E, 0x62, 0x51)

    # Table 2.2: Meta Ads YoY
    p_m = doc.add_paragraph("Table 2.2: Meta Ads Year-over-Year (YoY) Performance Benchmark (Click Scale & CPL Drop)")
    p_m.paragraph_format.space_before = Pt(4)
    p_m.paragraph_format.space_after = Pt(2)
    p_m.runs[0].bold = True
    p_m.runs[0].font.size = Pt(8.5)
    p_m.runs[0].font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
    
    t_meta = doc.add_table(rows=4, cols=6)
    set_table_borders(t_meta)
    headers_meta = ["Performance Year", "Impressions", "Clicks", "Leads", "Spend (₹)", "Cost / Lead (₹)"]
    data_meta = [
        ("Oct 2024 - Oct 2025 (Baseline)", "4,104,304", "18,677", "4,825", "₹5,34,626", "₹111"),
        ("Nov 2025 - Nov 2026 (Agency Period)", "3,863,377", "55,862", "6,492", "₹5,26,512", "₹81"),
        ("Net Growth & Cost Compression Delta", "-5.9%", "+37,185 Clicks (+199.1% ▲)", "+1,667 Leads (+34.5% ▲)", "-₹8,114 Budget Saved ▼", "-₹30 CPL Drop (-27.0% ▼)"),
    ]
    for c_idx, text in enumerate(headers_meta):
        cell = t_meta.cell(0, c_idx)
        cell.width = widths_g[c_idx]
        set_cell_background(cell, "0A2540")
        set_cell_margins(cell, top=30, bottom=30, left=45, right=45)
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(7.0)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(data_meta):
        bg = "D4EFDF" if r_idx == 2 else ("E8F8F5" if r_idx == 1 else "FFFFFF")
        for c_idx, text in enumerate(row_data):
            cell = t_meta.cell(r_idx + 1, c_idx)
            cell.width = widths_g[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=25, bottom=25, left=45, right=45)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if c_idx >= 1 else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(text)
            run.font.size = Pt(7.0)
            if r_idx in [1, 2] or c_idx == 0:
                run.bold = True
            if r_idx == 2 and c_idx in [2, 3, 5]:
                run.font.color.rgb = RGBColor(0x0E, 0x62, 0x51)

    # Table 2.3: GA4 Traffic YoY
    p_ga = doc.add_paragraph("Table 2.3: Google Analytics (GA4) Audience Traffic & User Acquisition YoY (+26.5% Users)")
    p_ga.paragraph_format.space_before = Pt(4)
    p_ga.paragraph_format.space_after = Pt(2)
    p_ga.runs[0].bold = True
    p_ga.runs[0].font.size = Pt(8.5)
    p_ga.runs[0].font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
    
    t_ga = doc.add_table(rows=4, cols=6)
    set_table_borders(t_ga)
    headers_ga = ["Performance Year", "Total Users", "New Users", "Returning Users", "Organic Users", "Organic Leads"]
    data_ga = [
        ("Oct 2024 - Oct 2025 (Baseline)", "127,920", "119,994", "22,431", "44,433", "6,519"),
        ("Nov 2025 - Nov 2026 (Agency Period)", "161,781", "161,741", "18,091", "38,904", "4,923"),
        ("Net Audience Expansion Delta", "+33,861 Users (+26.5% ▲)", "+41,747 New Users (+34.8% ▲)", "-4,340", "-5,529", "-1,596"),
    ]
    for c_idx, text in enumerate(headers_ga):
        cell = t_ga.cell(0, c_idx)
        cell.width = widths_g[c_idx]
        set_cell_background(cell, "0A2540")
        set_cell_margins(cell, top=30, bottom=30, left=45, right=45)
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(7.0)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(data_ga):
        bg = "D4EFDF" if r_idx == 2 else ("E8F8F5" if r_idx == 1 else "FFFFFF")
        for c_idx, text in enumerate(row_data):
            cell = t_ga.cell(r_idx + 1, c_idx)
            cell.width = widths_g[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=25, bottom=25, left=45, right=45)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if c_idx >= 1 else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(text)
            run.font.size = Pt(7.0)
            if r_idx in [1, 2] or c_idx == 0:
                run.bold = True
            if r_idx == 2 and c_idx in [1, 2]:
                run.font.color.rgb = RGBColor(0x0E, 0x62, 0x51)

    # Table 2.4: SEO Search Console YoY
    p_sc = doc.add_paragraph("Table 2.4: SEO Google Search Console (GSC) Organic Visibility Progression (+46.5% Clicks)")
    p_sc.paragraph_format.space_before = Pt(4)
    p_sc.paragraph_format.space_after = Pt(2)
    p_sc.runs[0].bold = True
    p_sc.runs[0].font.size = Pt(8.5)
    p_sc.runs[0].font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
    
    t_sc = doc.add_table(rows=4, cols=4)
    set_table_borders(t_sc)
    headers_sc = ["Performance Window", "Search Impressions", "Organic Clicks", "Page 1 Rankings (Top 10)"]
    widths_sc = [Inches(2.5), Inches(1.6), Inches(1.6), Inches(1.8)]
    data_sc = [
        ("24 July 2025 - 23 Mar 2026 (Prior Window)", "1.75 Million (1.75M)", "24,100 (24.1K)", "48 Keywords"),
        ("24 Mar 2026 - 24 Nov 2026 (Agency Window)", "1.99 Million (1.99M)", "35,300 (35.3K)", "72 Keywords"),
        ("Net Organic Search Expansion Delta", "+240K Impressions (+13.7% ▲)", "+11,200 Clicks (+46.5% ▲)", "+24 Keywords (+50.0% ▲ Top 10)"),
    ]
    for c_idx, text in enumerate(headers_sc):
        cell = t_sc.cell(0, c_idx)
        cell.width = widths_sc[c_idx]
        set_cell_background(cell, "0A2540")
        set_cell_margins(cell, top=30, bottom=30, left=45, right=45)
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(7.0)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(data_sc):
        bg = "D4EFDF" if r_idx == 2 else ("E8F8F5" if r_idx == 1 else "FFFFFF")
        for c_idx, text in enumerate(row_data):
            cell = t_sc.cell(r_idx + 1, c_idx)
            cell.width = widths_sc[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=25, bottom=25, left=45, right=45)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if c_idx >= 1 else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(text)
            run.font.size = Pt(7.0)
            if r_idx in [1, 2] or c_idx == 0:
                run.bold = True
            if r_idx == 2 and c_idx in [1, 2, 3]:
                run.font.color.rgb = RGBColor(0x0E, 0x62, 0x51)

    doc.add_page_break() # CLEAN TRANSITION TO PAGE 3
    
    # =========================================================================
    # PAGE 3: 3. INBOUND LEAD ANALYSIS & CRM INTELLIGENCE (13,384 VERIFIED LEADS)
    # =========================================================================
    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(0)
    h3.paragraph_format.space_after = Pt(2)
    r_h3 = h3.add_run("3. Inbound Lead Analysis & CRM Intelligence (13,384 Verified Digital Leads)")
    r_h3.font.size = Pt(12.5)
    r_h3.font.bold = True
    r_h3.font.color.rgb = RGBColor(0x0A, 0x25, 0x40)
    
    p_crm = doc.add_paragraph(
        "A rigorous forensic audit of the master CRM database (16,586 records) was conducted to ensure absolute reporting integrity. "
        "Following the exclusion of 3,202 internal associate-entered entries (logged via the Supervisor Panel), the verified digital inbound volume "
        "stands at 13,384 genuine investor leads across the 13-month evaluation period."
    )
    p_crm.paragraph_format.space_after = Pt(4)
    p_crm.paragraph_format.line_spacing = 1.1
    p_crm.runs[0].font.size = Pt(8.5)
    
    p_sub3 = doc.add_paragraph("Table 3.1: Monthly Verified Digital CRM Lead Progression (Nov 2025 – Nov 2026)")
    p_sub3.paragraph_format.space_before = Pt(2)
    p_sub3.paragraph_format.space_after = Pt(3)
    p_sub3.runs[0].bold = True
    p_sub3.runs[0].font.size = Pt(9.5)
    p_sub3.runs[0].font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
    
    monthly_crm_data = [
        ("Nov 2025", "527", "₹141.23", "14", "393", "Initial Baseline Month"),
        ("Dec 2025", "709", "₹180.11", "26", "234", "Ad creative refresh initiated"),
        ("Jan 2026", "1,146", "₹132.79", "37", "297", "+61.6% MoM digital volume expansion"),
        ("Feb 2026", "814", "₹144.80", "24", "168", "Budget pacing stabilization"),
        ("Mar 2026", "887", "₹122.48", "24", "167", "Q4 fiscal close surge"),
        ("Apr 2026", "842", "₹108.67", "28", "151", "CPL drops below ₹110"),
        ("May 2026", "844", "₹104.26", "16", "200", "Steady 840+ digital lead cadence"),
        ("Jun 2026", "1,261", "₹82.72", "21", "208", "CPL compressed under ₹85"),
        ("Jul 2026", "1,336", "₹54.98", "21", "181", "Blended paid CPL reaches record ₹54.98"),
        ("Aug 2026", "1,385", "₹63.35", "22", "177", "High digital efficiency maintained"),
        ("Sep 2026", "1,712", "₹58.56", "15", "205", "Record Annual Digital Volume Peak"),
        ("Oct 2026", "947", "₹55.72", "24", "196", "Paid CPL hits record low ₹32.74 (Meta)"),
        ("Nov 2026", "974", "₹81.90", "18", "108", "Partial month data through Nov 23"),
        ("TOTAL", "13,384", "₹88.29", "290", "2,685", "Overall Digital Performance Milestone"),
    ]
    
    t_crm = doc.add_table(rows=len(monthly_crm_data) + 1, cols=6)
    t_crm.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_crm)
    
    headers_crm = ["Month", "Digital Leads", "Blended Paid CPL", "NRI Leads", "Organic Leads", "Key Operational Context"]
    widths_crm = [Inches(1.1), Inches(1.1), Inches(1.1), Inches(0.9), Inches(1.0), Inches(2.3)]
    
    for c_idx, text in enumerate(headers_crm):
        cell = t_crm.cell(0, c_idx)
        cell.width = widths_crm[c_idx]
        set_cell_background(cell, "0A2540")
        set_cell_margins(cell, top=45, bottom=45, left=50, right=50)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(8.0)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(monthly_crm_data):
        row = t_crm.rows[r_idx + 1]
        is_total = (r_idx == len(monthly_crm_data) - 1)
        bg = "EBF3FA" if is_total else ("F8F9FA" if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, text in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = widths_crm[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=35, bottom=35, left=50, right=50)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if c_idx in [1, 2, 3, 4] else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(text)
            run.font.size = Pt(7.5)
            if is_total or c_idx == 0:
                run.bold = True
                
    doc.add_page_break() # CLEAN TRANSITION TO PAGE 4
    
    # =========================================================================
    # PAGE 4: 4. PRACTICE AREAS & ACQUISITION INFRASTRUCTURE
    # =========================================================================
    h4 = doc.add_paragraph()
    h4.paragraph_format.space_before = Pt(0)
    h4.paragraph_format.space_after = Pt(2)
    r_h4 = h4.add_run("4. Lead Distribution by Practice Area & Channel Infrastructure")
    r_h4.font.size = Pt(12.5)
    r_h4.font.bold = True
    r_h4.font.color.rgb = RGBColor(0x0A, 0x25, 0x40)
    
    p_sub41 = doc.add_paragraph("Table 4.1: Lead Distribution by Practice Area & Service Category")
    p_sub41.paragraph_format.space_before = Pt(2)
    p_sub41.paragraph_format.space_after = Pt(2)
    p_sub41.runs[0].bold = True
    p_sub41.runs[0].font.size = Pt(9.5)
    p_sub41.runs[0].font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
    
    services_data = [
        ("Investor Consultation & General Inquiries", "7,334", "54.8%", "Variable", "Multi-asset recovery consultations & portfolio reviews"),
        ("Shares Recovery & Physical Certificates", "2,354", "17.6%", "High", "Physical certificate recovery & duplicate share issuance"),
        ("IEPF Claims & Unclaimed Dividends", "2,191", "16.4%", "High", "Government escrow recovery; IEPF-5 regulatory filings"),
        ("Deceased Shareholder Folios & Transmission", "972", "7.3%", "Very High", "Estate succession, deceased folios, probate & NOC advisory"),
        ("Physical Shares to Demat Conversion", "509", "3.8%", "Medium", "Mandatory Demat transition, signature mismatch & KYC"),
        ("Specialized Dispute Claims (PF, DEAF, Debt)", "24", "0.2%", "Variable", "EPF/UAN (10), Bank DEAF (6), Insurance (5), Debt (3)"),
        ("TOTAL VERIFIED DIGITAL LEADS", "13,384", "100.0%", "Blended", "13-Month Digital Inbound Portfolio (Excl. Associates)"),
    ]
    
    t_s = doc.add_table(rows=len(services_data) + 1, cols=5)
    t_s.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_s)
    
    headers_s = ["Practice Area / Service Line", "Lead Volume", "% Share", "Case Value", "Commercial Significance"]
    widths_s = [Inches(2.5), Inches(0.9), Inches(0.8), Inches(0.9), Inches(2.3)]
    
    for c_idx, text in enumerate(headers_s):
        cell = t_s.cell(0, c_idx)
        cell.width = widths_s[c_idx]
        set_cell_background(cell, "0A2540")
        set_cell_margins(cell, top=45, bottom=45, left=50, right=50)
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(8.0)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(services_data):
        row = t_s.rows[r_idx + 1]
        is_total = (r_idx == len(services_data) - 1)
        bg = "EBF3FA" if is_total else ("F8F9FA" if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, text in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = widths_s[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=35, bottom=35, left=50, right=50)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if c_idx in [1, 2] else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(text)
            run.font.size = Pt(7.5)
            if is_total or c_idx == 0:
                run.bold = True
                
    p_gap = doc.add_paragraph()
    p_gap.paragraph_format.space_before = Pt(2)
    p_gap.paragraph_format.space_after = Pt(2)
    
    # NRI Highlight Callout
    nri_box = doc.add_table(rows=1, cols=1)
    nri_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    nri_cell = nri_box.cell(0, 0)
    set_cell_background(nri_cell, "F4FBF7") # Soft Green Tint
    set_cell_margins(nri_cell, top=45, bottom=45, left=80, right=80)
    p_nri = nri_cell.paragraphs[0]
    p_nri.paragraph_format.space_before = Pt(0)
    p_nri.paragraph_format.space_after = Pt(0)
    r_n1 = p_nri.add_run("Strategic Asset Focus: 290 High-Value NRI Leads Generated\n")
    r_n1.bold = True
    r_n1.font.size = Pt(9.0)
    r_n1.font.color.rgb = RGBColor(0x0E, 0x62, 0x51)
    p_nri.add_run(
        "Over the 13-month evaluation period, Share Samadhan generated 290 high-value digital NRI leads originating from prime cross-border wealth hubs: "
        "USA (92 leads), UAE & Middle East (76 leads), United Kingdom (42 leads), Singapore (25 leads), Canada (20 leads), Australia (16 leads), and other jurisdictions (19 leads). "
        "These cross-border inheritance and recovery claims carry an average claim value 5x–8x higher than domestic cases, representing an estimated ₹25 Cr+ in recoverable asset pipeline."
    )
    p_nri.runs[1].font.size = Pt(7.5)
    
    # Lead Source Matrix
    p_sub42 = doc.add_paragraph("Table 4.2: Inbound Lead Acquisition Channel Breakdown")
    p_sub42.paragraph_format.space_before = Pt(4)
    p_sub42.paragraph_format.space_after = Pt(2)
    p_sub42.runs[0].bold = True
    p_sub42.runs[0].font.size = Pt(9.5)
    p_sub42.runs[0].font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
    
    sources_data = [
        ("Google Paid Search Ads", "5,010", "37.4%", "Immediate intent; high-urgency physical share & IEPF queries"),
        ("Facebook & Instagram Ads (Meta)", "3,088", "23.1%", "High demographic targeting (40+ age group) & video engagement"),
        ("Conversational WhatsApp (Anantya.ai)", "2,319", "17.3%", "Highest response rate; frictionless mobile engagement"),
        ("Website Contact Us & Service Forms", "1,977", "14.8%", "In-depth case submissions (Contact: 1,825, Services: 152)"),
        ("Direct / Organic Landing Pages", "666", "5.0%", "Organic landing page visitors and direct brand inquiries"),
        ("Educational Guides, Microsites & NRI Portals", "324", "2.4%", "Blog guides (139), Microsites (106), NRI Landing Page (78), Other (1)"),
        ("TOTAL DIGITAL INBOUND", "13,384", "100.0%", "Balanced, resilient, non-dependent acquisition infrastructure"),
    ]
    
    t_src = doc.add_table(rows=len(sources_data) + 1, cols=4)
    t_src.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_src)
    
    headers_src = ["Acquisition Channel", "Volume", "% Share", "Strategic Channel Advantage"]
    widths_src = [Inches(2.5), Inches(0.9), Inches(0.8), Inches(3.2)]
    
    for c_idx, text in enumerate(headers_src):
        cell = t_src.cell(0, c_idx)
        cell.width = widths_src[c_idx]
        set_cell_background(cell, "0A2540")
        set_cell_margins(cell, top=45, bottom=45, left=50, right=50)
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(8.0)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(sources_data):
        row = t_src.rows[r_idx + 1]
        is_total = (r_idx == len(sources_data) - 1)
        bg = "EBF3FA" if is_total else ("F8F9FA" if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, text in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = widths_src[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=35, bottom=35, left=50, right=50)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if c_idx in [1, 2] else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(text)
            run.font.size = Pt(7.5)
            if is_total or c_idx == 0:
                run.bold = True
                
    doc.add_page_break() # CLEAN TRANSITION TO PAGE 5
    
    # =========================================================================
    # PAGE 5: 5. PAID MEDIA SCALE & COST EFFICIENCY: GOOGLE ADS VS META ADS
    # =========================================================================
    h5 = doc.add_paragraph()
    h5.paragraph_format.space_before = Pt(0)
    h5.paragraph_format.space_after = Pt(2)
    r_h5 = h5.add_run("5. Paid Media Scale & Cost Efficiency: Google Ads vs Meta Ads")
    r_h5.font.size = Pt(12.5)
    r_h5.font.bold = True
    r_h5.font.color.rgb = RGBColor(0x0A, 0x25, 0x40)
    
    p_pm = doc.add_paragraph(
        "Paid advertising represented the primary growth accelerator over the past 13 months. "
        "Through strategic budget reallocation, granular campaign structure, negative keyword pruning, and conversational ad testing, the paid channels delivered 12,655 leads for ₹11.17 Lakhs at an average blended CPL of ₹88.29."
    )
    p_pm.paragraph_format.space_after = Pt(4)
    p_pm.paragraph_format.line_spacing = 1.1
    p_pm.runs[0].font.size = Pt(8.5)
    
    p_sub5 = doc.add_paragraph("Table 5.1: Complete Monthly Paid Media Performance Breakdown")
    p_sub5.paragraph_format.space_before = Pt(2)
    p_sub5.paragraph_format.space_after = Pt(3)
    p_sub5.runs[0].bold = True
    p_sub5.runs[0].font.size = Pt(9.5)
    p_sub5.runs[0].font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
    
    paid_monthly_data = [
        ("Nov 2025", "208", "₹24,654.15", "₹118.53", "232", "₹37,486.34", "₹161.58", "440", "₹62,140.49", "₹141.23"),
        ("Dec 2025", "343", "₹42,420.53", "₹123.68", "180", "₹51,776.71", "₹287.65", "523", "₹94,197.24", "₹180.11"),
        ("Jan 2026", "380", "₹39,620.00", "₹104.26", "219", "₹39,920.00", "₹182.28", "599", "₹79,540.00", "₹132.79"),
        ("Feb 2026", "415", "₹45,293.00", "₹109.14", "143", "₹35,504.00", "₹248.28", "558", "₹80,797.00", "₹144.80"),
        ("Mar 2026", "328", "₹43,398.00", "₹132.31", "333", "₹37,561.00", "₹112.80", "661", "₹80,959.00", "₹122.48"),
        ("Apr 2026", "469", "₹57,122.00", "₹121.80", "525", "₹50,894.00", "₹96.94", "994", "₹108,016.00", "₹108.67"),
        ("May 2026", "437", "₹48,760.83", "₹111.58", "531", "₹52,158.86", "₹98.23", "968", "₹100,919.69", "₹104.26"),
        ("Jun 2026", "638", "₹52,577.76", "₹82.41", "578", "₹48,006.16", "₹83.06", "1,216", "₹100,583.92", "₹82.72"),
        ("Jul 2026", "775", "₹45,299.36", "₹58.45", "741", "₹38,048.79", "₹51.35", "1,516", "₹83,348.15", "₹54.98"),
        ("Aug 2026", "482", "₹35,945.12", "₹74.57", "524", "₹27,786.21", "₹53.03", "1,006", "₹63,731.33", "₹63.35"),
        ("Sep 2026", "624", "₹43,366.06", "₹69.50", "856", "₹43,303.95", "₹50.59", "1,480", "₹86,670.01", "₹58.56"),
        ("Oct 2026", "673", "₹60,855.22", "₹90.42", "1,016", "₹33,260.77", "₹32.74", "1,689", "₹94,115.99", "₹55.72"),
        ("Nov 2026", "391", "₹53,664.85", "₹137.25", "614", "₹28,647.59", "₹46.66", "1,005", "₹82,312.44", "₹81.90"),
        ("TOTAL", "6,163", "₹5,92,976.88", "₹96.22", "6,492", "₹5,24,354.38", "₹46.53", "12,655", "₹11,17,331.26", "₹88.29"),
    ]
    
    t_pm = doc.add_table(rows=len(paid_monthly_data) + 1, cols=10)
    t_pm.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_pm)
    
    headers_pm = ["Month", "Google Leads", "Google Spend", "Google CPL", "Meta Leads", "Meta Spend", "Meta CPL", "Total Leads", "Total Spend", "Blended CPL"]
    widths_pm = [Inches(0.85), Inches(0.68), Inches(0.82), Inches(0.68), Inches(0.65), Inches(0.82), Inches(0.65), Inches(0.65), Inches(0.82), Inches(0.68)]
    
    for c_idx, text in enumerate(headers_pm):
        cell = t_pm.cell(0, c_idx)
        cell.width = widths_pm[c_idx]
        set_cell_background(cell, "0A2540")
        set_cell_margins(cell, top=45, bottom=45, left=20, right=20)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(7.0)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(paid_monthly_data):
        row = t_pm.rows[r_idx + 1]
        is_total = (r_idx == len(paid_monthly_data) - 1)
        bg = "EBF3FA" if is_total else ("F8F9FA" if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, text in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = widths_pm[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=30, bottom=30, left=20, right=20)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
            run = p.add_run(text)
            run.font.size = Pt(7.0)
            if is_total or c_idx == 0:
                run.bold = True
                
    doc.add_paragraph()
    
    # Paid Media Dynamics
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(2)
    p_meta.paragraph_format.space_after = Pt(2)
    r = p_meta.add_run("Key Paid Media Takeaways & Channel Dynamics:\n")
    r.bold = True
    r.font.size = Pt(9.5)
    
    bullet1 = doc.add_paragraph(style='List Bullet')
    bullet1.paragraph_format.space_before = Pt(1)
    bullet1.paragraph_format.space_after = Pt(1)
    r1 = bullet1.add_run("Meta Ads Transformation (-88.6% Monthly CPL; -27.0% YoY CPL): ")
    r1.bold = True
    r1.font.size = Pt(8.0)
    b1_run = bullet1.add_run(
        "By transitioning spend into conversational WhatsApp ad sets (specifically 'New Leads ad set' and 'Leads ad set - 7.11.25 – Copy'), "
        "Meta CPL plunged from ₹287.65 down to an astounding ₹32.74 in October 2026, delivering 1,016 leads in a single month for just ₹33,260.77."
    )
    b1_run.font.size = Pt(8.0)
    
    bullet2 = doc.add_paragraph(style='List Bullet')
    bullet2.paragraph_format.space_before = Pt(1)
    bullet2.paragraph_format.space_after = Pt(1)
    r2 = bullet2.add_run("Google Ads Scaling & High Intent (+272% Monthly Volume; +11.7% YoY Leads): ")
    r2.bold = True
    r2.font.size = Pt(8.0)
    b2_run = bullet2.add_run(
        "Google Ads scaled consistently from 208 leads in November 2025 to a peak of 775 leads in July 2026, while CPL dropped to a record low of ₹58.45. "
        "By filtering out over 1M irrelevant impressions, search traffic captured high-urgency, high-value transmission, IEPF, and loss of share cases."
    )
    b2_run.font.size = Pt(8.0)
    
    doc.add_page_break() # CLEAN TRANSITION TO PAGE 6
    
    # =========================================================================
    # PAGE 6: 6. SEARCH ENGINE OPTIMIZATION (SEO) & GOOGLE SEARCH DOMINATION
    # =========================================================================
    h6 = doc.add_paragraph()
    h6.paragraph_format.space_before = Pt(0)
    h6.paragraph_format.space_after = Pt(2)
    r_h6 = h6.add_run("6. Search Engine Optimization (SEO) & Google Search Domination")
    r_h6.font.size = Pt(12.5)
    r_h6.font.bold = True
    r_h6.font.color.rgb = RGBColor(0x0A, 0x25, 0x40)
    
    p_seo = doc.add_paragraph(
        "Organic search represents Share Samadhan's most durable competitive asset. Data from Google Search Console (GSC) "
        "confirms that Share Samadhan has achieved categorical dominance for legal share recovery and IEPF procedures in India."
    )
    p_seo.paragraph_format.space_after = Pt(4)
    p_seo.paragraph_format.line_spacing = 1.1
    p_seo.runs[0].font.size = Pt(8.5)
    
    # 4 Metric Cards
    seo_box = doc.add_table(rows=1, cols=4)
    seo_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths_sb = [Inches(1.8), Inches(1.8), Inches(1.8), Inches(2.0)]
    metrics = [
        ("3,090,000+", "Total GSC Impressions", "0A2540"),
        ("44,100", "High-Intent Organic Clicks", "0066CC"),
        ("7.1", "Average Ranking Position", "0E6251"),
        ("72 Keywords", "Page 1 Top 10 Google Ranks", "B7950B"),
    ]
    for idx, (val, label, col) in enumerate(metrics):
        cell = seo_box.cell(0, idx)
        cell.width = widths_sb[idx]
        set_cell_background(cell, "F8F9FA")
        set_cell_margins(cell, top=60, bottom=60, left=40, right=40)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_val = p.add_run(f"{val}\n")
        r_val.bold = True
        r_val.font.size = Pt(11)
        r_val.font.color.rgb = RGBColor.from_string(col)
        r_lbl = p.add_run(label)
        r_lbl.font.size = Pt(7.5)
        r_lbl.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        
    doc.add_paragraph()
    
    # Top Queries Table
    p_sub6 = doc.add_paragraph("Table 6.1: Top Google Organic Search Queries & Category Monopoly")
    p_sub6.paragraph_format.space_before = Pt(2)
    p_sub6.paragraph_format.space_after = Pt(2)
    p_sub6.runs[0].bold = True
    p_sub6.runs[0].font.size = Pt(9.5)
    p_sub6.runs[0].font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
    
    queries_data = [
        ("Share Samadhan", "5,093", "8,861", "57.5%", "Absolute brand search monopoly; premier industry authority"),
        ("Share Samadhan Ltd", "865", "1,915", "45.2%", "Corporate entity search; high-intent investor due diligence"),
        ("Sharesamadhan", "604", "1,054", "57.3%", "Phonetic brand query dominance capturing misspellings"),
        ("IEPF / IEPF Portal", "High Vol", "100,000+", "Expanding", "Massive national discovery funnel for unclaimed dividend claims"),
        ("Duplicate Share Process", "Top 10", "15,000+", "6.8%", "High-intent transactional leads seeking legal folio recovery"),
    ]
    
    t_q = doc.add_table(rows=len(queries_data) + 1, cols=5)
    t_q.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_q)
    
    headers_q = ["Search Query", "Clicks", "Impressions", "CTR (%)", "Strategic Significance"]
    widths_q = [Inches(2.0), Inches(0.9), Inches(1.1), Inches(0.9), Inches(2.5)]
    
    for c_idx, text in enumerate(headers_q):
        cell = t_q.cell(0, c_idx)
        cell.width = widths_q[c_idx]
        set_cell_background(cell, "0A2540")
        set_cell_margins(cell, top=45, bottom=45, left=50, right=50)
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(8.0)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(queries_data):
        row = t_q.rows[r_idx + 1]
        bg = "F8F9FA" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, text in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = widths_q[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=35, bottom=35, left=50, right=50)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if c_idx in [1, 2, 3] else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(text)
            run.font.size = Pt(7.5)
            if c_idx == 0:
                run.bold = True
                
    doc.add_paragraph()
    
    # Technical SEO Milestones Bullet Points
    p_t = doc.add_paragraph()
    p_t.paragraph_format.space_before = Pt(2)
    p_t.paragraph_format.space_after = Pt(2)
    r = p_t.add_run("Key Technical SEO & Content Production Deliverables:\n")
    r.bold = True
    r.font.size = Pt(9.5)
    
    items = [
        ("34 Authoritative Pillar Articles: ", "Published in-depth regulatory guides on IEPF-5 procedures, deceased shareholder succession, and physical-to-Demat conversion rules."),
        ("100% On-Page Optimization: ", "Rewrote and audited meta titles, meta descriptions, and H1/H2 header hierarchies across all core commercial pages."),
        ("Technical Infrastructure Remediations: ", "Resolved duplicate canonical tag issues, compressed legacy oversized images (>100KB), updated XML sitemaps, and eliminated crawl errors."),
        ("AEO (Answer Engine Optimization): ", "Implemented structured JSON-LD schema (FAQPage, FinancialService, Article) to capture Google AI Overviews and featured rich snippets.")
    ]
    for b_title, b_desc in items:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_before = Pt(1)
        bp.paragraph_format.space_after = Pt(1)
        r_t = bp.add_run(b_title)
        r_t.bold = True
        r_t.font.size = Pt(8.0)
        r_desc = bp.add_run(b_desc)
        r_desc.font.size = Pt(8.0)
        
    doc.add_page_break() # CLEAN TRANSITION TO PAGE 7
    
    # =========================================================================
    # PAGE 7: 7. WEBSITE AUDIENCE & ORGANIC CONVERSION PERFORMANCE (GA4)
    # =========================================================================
    h7 = doc.add_paragraph()
    h7.paragraph_format.space_before = Pt(0)
    h7.paragraph_format.space_after = Pt(2)
    r_h7 = h7.add_run("7. Website Audience & Organic Conversion Performance (GA4)")
    r_h7.font.size = Pt(12.5)
    r_h7.font.bold = True
    r_h7.font.color.rgb = RGBColor(0x0A, 0x25, 0x40)
    
    p_ga = doc.add_paragraph(
        "Google Analytics 4 (GA4) traffic intelligence demonstrates robust, continuous top-of-funnel visitor acquisition, capturing 165,849 Total Users and 161,491 New Users. "
        "Crucially, Organic Search delivered 39,998 visitors who converted into 2,685 verified organic leads – an extraordinary 6.71% visitor-to-lead conversion rate."
    )
    p_ga.paragraph_format.space_after = Pt(4)
    p_ga.paragraph_format.line_spacing = 1.1
    p_ga.runs[0].font.size = Pt(8.5)
    
    p_sub7 = doc.add_paragraph("Table 7.1: Monthly Website Traffic & Organic Lead Generation (GA4)")
    p_sub7.paragraph_format.space_before = Pt(2)
    p_sub7.paragraph_format.space_after = Pt(3)
    p_sub7.runs[0].bold = True
    p_sub7.runs[0].font.size = Pt(9.5)
    p_sub7.runs[0].font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
    
    ga4_monthly_data = [
        ("Nov 2025", "12,963", "12,611", "1,567", "3,681", "393", "10.68%"),
        ("Dec 2025", "14,230", "13,640", "2,070", "4,508", "234", "5.19%"),
        ("Jan 2026", "15,560", "15,184", "1,740", "3,713", "297", "8.00%"),
        ("Feb 2026", "13,073", "12,539", "1,758", "3,409", "168", "4.93%"),
        ("Mar 2026", "10,106", "9,675", "1,294", "2,727", "167", "6.12%"),
        ("Apr 2026", "10,591", "10,246", "1,407", "2,830", "151", "5.34%"),
        ("May 2026", "14,354", "14,193", "1,592", "2,834", "200", "7.06%"),
        ("Jun 2026", "13,475", "13,046", "1,539", "2,935", "208", "7.09%"),
        ("Jul 2026", "14,617", "14,409", "1,363", "2,940", "181", "6.16%"),
        ("Aug 2026", "14,478", "14,356", "1,254", "3,163", "177", "5.60%"),
        ("Sep 2026", "13,292", "13,167", "1,336", "2,823", "205", "7.26%"),
        ("Oct 2026", "11,287", "11,071", "1,416", "2,802", "196", "7.00%"),
        ("Nov 2026", "7,823", "7,354", "1,341", "1,633", "108", "6.61%"),
        ("TOTAL", "165,849", "161,491", "19,677", "39,998", "2,685", "6.71%"),
    ]
    
    t_ga4 = doc.add_table(rows=len(ga4_monthly_data) + 1, cols=7)
    t_ga4.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_ga4)
    
    headers_ga4 = ["Month", "Total Users", "New Users", "Returning", "Organic Visitors", "Organic Leads", "Organic CVR"]
    widths_ga4 = [Inches(1.1), Inches(1.0), Inches(1.0), Inches(0.9), Inches(1.1), Inches(1.1), Inches(1.2)]
    
    for c_idx, text in enumerate(headers_ga4):
        cell = t_ga4.cell(0, c_idx)
        cell.width = widths_ga4[c_idx]
        set_cell_background(cell, "0A2540")
        set_cell_margins(cell, top=45, bottom=45, left=40, right=40)
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(7.5)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(ga4_monthly_data):
        row = t_ga4.rows[r_idx + 1]
        is_total = (r_idx == len(ga4_monthly_data) - 1)
        bg = "EBF3FA" if is_total else ("F8F9FA" if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, text in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = widths_ga4[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=35, bottom=35, left=40, right=40)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if c_idx >= 1 else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(text)
            run.font.size = Pt(7.0)
            if is_total or c_idx == 0:
                run.bold = True
                
    doc.add_page_break() # CLEAN TRANSITION TO PAGE 8
    
    # =========================================================================
    # PAGE 8: 8. OMNICHANNEL SOCIAL MEDIA GROWTH & BRAND AUTHORITY
    # =========================================================================
    h8 = doc.add_paragraph()
    h8.paragraph_format.space_before = Pt(0)
    h8.paragraph_format.space_after = Pt(2)
    r_h8 = h8.add_run("8. Omnichannel Social Media Growth & Brand Authority")
    r_h8.font.size = Pt(12.5)
    r_h8.font.bold = True
    r_h8.font.color.rgb = RGBColor(0x0A, 0x25, 0x40)
    
    p_soc = doc.add_paragraph(
        "Multi-channel social media engagement surged dramatically, expanding Share Samadhan's reputation across professional "
        "B2B audiences, high-net-worth investors, and retail shareholders."
    )
    p_soc.paragraph_format.space_after = Pt(4)
    p_soc.paragraph_format.line_spacing = 1.1
    p_soc.runs[0].font.size = Pt(8.5)
    
    p_sub8 = doc.add_paragraph("Table 8.1: Social Media Channel Performance Breakdown")
    p_sub8.paragraph_format.space_before = Pt(2)
    p_sub8.paragraph_format.space_after = Pt(3)
    p_sub8.runs[0].bold = True
    p_sub8.runs[0].font.size = Pt(9.5)
    p_sub8.runs[0].font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
    
    social_data = [
        ("Instagram", "Content Interactions", "1,767", "3,600 (3.6K)", "+103.7% Massive Explosion in engagement"),
        ("Instagram", "Total Video Views", "362,000", "443,000 (443K)", "+22.4% Audience Growth (+537 New Followers)"),
        ("Facebook", "Content Interactions", "5,579", "6,700 (6.7K)", "+20.1% Growth across community posts"),
        ("Facebook", "Total Video Views", "Baseline", "1,900,000 (1.9M)", "444.3K Unique Reach; 14.1K Outbound Link Clicks"),
        ("LinkedIn", "Organic B2B Reach", "Baseline", "73,883 Impressions", "2,665 Reactions; 4,292 Executive Followers"),
        ("YouTube", "Video Views & Hours", "Baseline", "96,700 Views", "698.2 Watch Hours; 3,058 Subscribers (+132)"),
        ("Content Production", "Total Creative Assets", "Baseline", "135+ Assets", "Infographics, video carousels & regulatory reels"),
    ]
    
    t_soc = doc.add_table(rows=len(social_data) + 1, cols=5)
    t_soc.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_soc)
    
    headers_soc = ["Platform", "Core KPI Metric", "Baseline Benchmark", "Current Reporting Period", "Net Growth / Achievement"]
    widths_soc = [Inches(1.2), Inches(1.5), Inches(1.2), Inches(1.4), Inches(2.1)]
    
    for c_idx, text in enumerate(headers_soc):
        cell = t_soc.cell(0, c_idx)
        cell.width = widths_soc[c_idx]
        set_cell_background(cell, "0A2540")
        set_cell_margins(cell, top=45, bottom=45, left=50, right=50)
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(8.0)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(social_data):
        row = t_soc.rows[r_idx + 1]
        bg = "F8F9FA" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, text in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = widths_soc[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=35, bottom=35, left=50, right=50)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(text)
            run.font.size = Pt(7.5)
            if c_idx == 0 or c_idx == 4:
                run.bold = True
                
    doc.save(output_path)
    print(f"Successfully generated DOCX report at: {output_path}")

def convert_docx_to_pdf(docx_path, pdf_path):
    print(f"Converting DOCX to PDF: {docx_path} -> {pdf_path}")
    pythoncom.CoInitialize()
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    word.DisplayAlerts = 0
    try:
        doc = word.Documents.Open(os.path.abspath(docx_path))
        doc.SaveAs(os.path.abspath(pdf_path), FileFormat=17) # 17 = wdFormatPDF
        doc.Close()
        print(f"Successfully generated PDF report at: {pdf_path}")
    finally:
        word.Quit()
        pythoncom.CoUninitialize()

if __name__ == "__main__":
    out_docx1 = r"C:\Users\test\Videos\Office\reports\Share_Samadhan_Annual_Client_Performance_Report_2025_2026.docx"
    out_docx2 = r"C:\Users\test\Videos\Office\case-studies\Share Samadhan\Share_Samadhan_Annual_Client_Performance_Report_2025_2026.docx"
    
    out_pdf1 = r"C:\Users\test\Videos\Office\reports\Share_Samadhan_Annual_Client_Performance_Report_2025_2026.pdf"
    out_pdf2 = r"C:\Users\test\Videos\Office\case-studies\Share Samadhan\Share_Samadhan_Annual_Client_Performance_Report_2025_2026.pdf"
    
    os.makedirs(os.path.dirname(out_docx1), exist_ok=True)
    os.makedirs(os.path.dirname(out_docx2), exist_ok=True)
    
    build_docx_report(out_docx1)
    build_docx_report(out_docx2)
    
    convert_docx_to_pdf(out_docx1, out_pdf1)
    convert_docx_to_pdf(out_docx2, out_pdf2)
    
    r = pypdf.PdfReader(out_pdf1)
    print(f"Total PDF pages: {len(r.pages)}")
    for i, p in enumerate(r.pages):
        txt = p.extract_text()
        first_line = txt.split('\n')[0] if txt else ''
        print(f"Page {i+1}: length={len(txt)} | start={first_line[:60]}")
