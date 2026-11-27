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

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
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
    
    # Page setup - 0.75 in margins
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        
    # Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(10)
    normal_style.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    
    # ------------------ COVER / HEADER ------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(2)
    title_run = title_p.add_run("SHARE SAMADHAN LIMITED")
    title_run.font.size = Pt(22)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(0x0A, 0x25, 0x40) # Deep Navy
    
    subtitle_p = doc.add_paragraph()
    subtitle_p.paragraph_format.space_before = Pt(0)
    subtitle_p.paragraph_format.space_after = Pt(14)
    subtitle_run = subtitle_p.add_run("Annual Performance Report (November 1, 2025 – November 23, 2026)")
    subtitle_run.font.size = Pt(12)
    subtitle_run.font.bold = True
    subtitle_run.font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
    
    # ------------------ 1. EXECUTIVE SCORECARD TABLE ------------------
    h1 = doc.add_heading("1. Executive Scorecard: 10 Major Growth Milestones", level=1)
    h1.runs[0].font.color.rgb = RGBColor(0x0A, 0x25, 0x40)
    h1.runs[0].font.size = Pt(14)
    h1.paragraph_format.space_before = Pt(0)
    h1.paragraph_format.space_after = Pt(6)
    
    milestones_data = [
        ("1. Total Inbound Leads (CRM)", "527 leads / mo", "1,712 leads / mo (Sep '26)", "+224.9% Digital Volume Growth (13,384 Verified Digital Leads)"),
        ("2. Paid Media Leads (Google+Meta)", "440 leads / mo", "1,689 leads / mo (Oct '26)", "+283.9% Lead Growth (Nearly 4x Scale; 12,655 Leads)"),
        ("3. Blended Cost Per Lead (CPL)", "₹141.23 – ₹180.11", "₹54.98 – ₹55.72", "-60.5% to -69.5% CPL Compression (Saved ₹125+/lead)"),
        ("4. Meta Ads CPL Revolution", "₹161.58 – ₹287.65", "₹32.74 (Oct '26)", "-88.6% Reduction in Meta Acquisition Cost (6,492 Leads)"),
        ("5. Google Ads Lead Scale", "208 leads / mo", "775 leads / mo (Jul '26)", "+272.6% Scale; CPL dropped from ₹123.68 to ₹58.45"),
        ("6. Google Search Impressions (GSC)", "Baseline", "3,090,000+ (3.09 Million)", "Undisputed Organic Category Visibility across India"),
        ("7. High-Intent Organic Clicks", "Baseline", "44,100 (44.1K) Clicks", "Captured High-Intent Searchers (Avg Position 7.1)"),
        ("8. Page 1 Google Rankings", "Baseline", "72 Keywords (Top 10)", "Dominating Loss of Shares, Demat & IEPF queries"),
        ("9. Total Website Audience (GA4)", "Baseline", "165,849 Total Users", "161,491 New Users Acquired (97.4% Fresh Reach)"),
        ("10. High-Value Organic Leads", "Baseline", "2,685 Organic Leads", "6.71% Visitor-to-Lead Conversion Rate (39.9K Organic traffic)"),
    ]
    
    t_m = doc.add_table(rows=len(milestones_data) + 1, cols=4)
    t_m.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_m)
    
    headers_m = ["Performance Pillar", "Baseline (Nov '25)", "Peak / Current Performance", "Net Improvement & Milestone"]
    widths_m = [Inches(2.2), Inches(1.3), Inches(1.6), Inches(2.4)]
    
    for c_idx, text in enumerate(headers_m):
        cell = t_m.cell(0, c_idx)
        cell.width = widths_m[c_idx]
        set_cell_background(cell, "0A2540") # Navy
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(9.0)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(milestones_data):
        row = t_m.rows[r_idx + 1]
        bg = "F8F9FA" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, text in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = widths_m[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(text)
            run.font.size = Pt(8.5)
            if c_idx == 0 or c_idx == 3:
                run.bold = True
                
    doc.add_page_break() # Clean transition to Section 2 on Page 2
    
    # ------------------ 2. CRM INBOUND LEADS SECTION ------------------
    h2 = doc.add_heading("2. Inbound Lead Analysis & CRM Intelligence (13,384 Verified Digital Leads)", level=1)
    h2.runs[0].font.color.rgb = RGBColor(0x0A, 0x25, 0x40)
    h2.runs[0].font.size = Pt(14)
    h2.paragraph_format.space_before = Pt(0)
    h2.paragraph_format.space_after = Pt(6)
    
    p = doc.add_paragraph(
        "A rigorous forensic audit of the master CRM database (16,586 records) was conducted to ensure absolute data integrity. "
        "Following the exclusion of 3,202 internal associate-entered entries (logged via the Supervisor Panel), the verified digital inbound volume "
        "stands at 13,384 genuine investor leads. This confirms massive compounding volume, robust channel diversification, and strong demand across Share Samadhan's specialized legal-financial services."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(8)
    
    # Monthly Progression Table
    p_sub = doc.add_paragraph("Table 2.1: Monthly Verified Digital CRM Lead Progression (Nov 2025 – Nov 2026)")
    p_sub.runs[0].bold = True
    p_sub.runs[0].font.size = Pt(10.5)
    p_sub.runs[0].font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
    p_sub.paragraph_format.space_after = Pt(4)
    
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
        set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(monthly_crm_data):
        row = t_crm.rows[r_idx + 1]
        is_total = (r_idx == len(monthly_crm_data) - 1)
        bg = "EBF3FA" if is_total else ("F8F9FA" if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, text in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = widths_crm[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if c_idx in [1, 2, 3, 4] else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(text)
            run.font.size = Pt(8.0)
            if is_total or c_idx == 0:
                run.bold = True
                
    doc.add_page_break() # Clean transition to Practice Areas & Channels on Page 3
    
    # Service Breakdown & NRI Analysis
    p_sub = doc.add_paragraph("Table 2.2: Lead Distribution by Practice Area & Service Category")
    p_sub.runs[0].bold = True
    p_sub.runs[0].font.size = Pt(10.5)
    p_sub.runs[0].font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
    p_sub.paragraph_format.space_after = Pt(3)
    
    services_data = [
        ("Investor Consultation & General Inquiries", "7,334", "54.8%", "Variable", "Multi-asset recovery consultations & initial portfolio reviews"),
        ("Shares Recovery & Physical Certificates", "2,354", "17.6%", "High", "Core revenue engine; physical certificate misplacement & duplicate issue"),
        ("IEPF Claims & Unclaimed Dividends", "2,191", "16.4%", "High", "Government escrow recovery; IEPF-5 filings & corporate reconciliations"),
        ("Deceased Shareholder Folios & Transmission", "972", "7.3%", "Very High", "Estate succession, deceased shareholder folios, probate & NOC advisory"),
        ("Physical Shares to Demat Conversion", "509", "3.8%", "Medium", "Mandatory Demat transition, signature mismatch & KYC rectifications"),
        ("Specialized Dispute Claims (PF, DEAF, Debt)", "24", "0.2%", "Variable", "Stuck EPF/UAN claims (10), Inoperative bank DEAF (6), Insurance (5), Litigation (3)"),
        ("TOTAL VERIFIED DIGITAL LEADS", "13,384", "100.0%", "Blended", "Comprehensive 13-Month Digital Inbound Portfolio (Excl. Associates)"),
    ]
    
    t_s = doc.add_table(rows=len(services_data) + 1, cols=5)
    t_s.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_s)
    
    headers_s = ["Practice Area / Service Line", "Lead Volume", "% Share", "Case Value", "Commercial Significance"]
    widths_s = [Inches(2.5), Inches(1.0), Inches(0.9), Inches(1.0), Inches(2.1)]
    
    for c_idx, text in enumerate(headers_s):
        cell = t_s.cell(0, c_idx)
        cell.width = widths_s[c_idx]
        set_cell_background(cell, "0A2540")
        set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(services_data):
        row = t_s.rows[r_idx + 1]
        is_total = (r_idx == len(services_data) - 1)
        bg = "EBF3FA" if is_total else ("F8F9FA" if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, text in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = widths_s[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if c_idx in [1, 2] else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(text)
            run.font.size = Pt(8.0)
            if is_total or c_idx == 0:
                run.bold = True
                
    p_gap1 = doc.add_paragraph()
    p_gap1.paragraph_format.space_before = Pt(2)
    p_gap1.paragraph_format.space_after = Pt(2)
    
    # NRI Highlight Callout
    nri_box = doc.add_table(rows=1, cols=1)
    nri_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    nri_cell = nri_box.cell(0, 0)
    set_cell_background(nri_cell, "F4FBF7") # Soft Green Tint
    set_cell_margins(nri_cell, top=50, bottom=50, left=100, right=100)
    p_nri = nri_cell.paragraphs[0]
    p_nri.paragraph_format.space_before = Pt(0)
    p_nri.paragraph_format.space_after = Pt(0)
    r_n1 = p_nri.add_run("Strategic Asset Focus: 290 High-Value NRI Leads Generated\n")
    r_n1.bold = True
    r_n1.font.size = Pt(9.5)
    r_n1.font.color.rgb = RGBColor(0x0E, 0x62, 0x51)
    p_nri.add_run(
        "Over the 13-month evaluation period, Share Samadhan generated 290 high-value digital NRI leads originating from prime cross-border wealth hubs: "
        "USA (92 leads), UAE & Middle East (76 leads), United Kingdom (42 leads), Singapore (25 leads), Canada (20 leads), Australia (16 leads), and other jurisdictions (19 leads). "
        "These cross-border inheritance and recovery claims carry an average claim value 5x–8x higher than domestic cases, representing an estimated ₹25 Cr+ in recoverable asset pipeline."
    )
    p_nri.runs[1].font.size = Pt(8.0)
    
    # Lead Source Matrix
    p_sub = doc.add_paragraph("Table 2.3: Inbound Lead Acquisition Channel Breakdown")
    p_sub.runs[0].bold = True
    p_sub.runs[0].font.size = Pt(10.5)
    p_sub.runs[0].font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
    p_sub.paragraph_format.space_before = Pt(4)
    p_sub.paragraph_format.space_after = Pt(3)
    
    sources_data = [
        ("Google Paid Search Ads", "5,010", "37.4%", "Immediate intent; high-urgency physical share & IEPF queries"),
        ("Facebook & Instagram Ads (Meta)", "3,088", "23.1%", "High demographic targeting (40+ age group) & video engagement"),
        ("Conversational WhatsApp (Anantya.ai)", "2,319", "17.3%", "Highest response rate; frictionless mobile engagement"),
        ("Website Contact Us & Service Forms", "1,977", "14.8%", "In-depth case submissions with pre-qualified folio details (Contact: 1,825, Services: 152)"),
        ("Direct / Organic Landing Pages", "666", "5.0%", "Organic landing page visitors and direct brand inquiries"),
        ("Educational Guides, Microsites & NRI Portals", "324", "2.4%", "Legal blog guides (139), Microsites (106), NRI Landing Page (78), Other (1)"),
        ("TOTAL DIGITAL INBOUND", "13,384", "100.0%", "Balanced, resilient, non-dependent acquisition infrastructure"),
    ]
    
    t_src = doc.add_table(rows=len(sources_data) + 1, cols=4)
    t_src.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_src)
    
    headers_src = ["Acquisition Channel", "Volume", "% Share", "Strategic Channel Advantage"]
    widths_src = [Inches(2.5), Inches(1.0), Inches(0.9), Inches(3.1)]
    
    for c_idx, text in enumerate(headers_src):
        cell = t_src.cell(0, c_idx)
        cell.width = widths_src[c_idx]
        set_cell_background(cell, "0A2540")
        set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(sources_data):
        row = t_src.rows[r_idx + 1]
        is_total = (r_idx == len(sources_data) - 1)
        bg = "EBF3FA" if is_total else ("F8F9FA" if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, text in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = widths_src[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=45, bottom=45, left=60, right=60)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if c_idx in [1, 2] else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(text)
            run.font.size = Pt(8.0)
            if is_total or c_idx == 0:
                run.bold = True
                
    doc.add_page_break() # Clean transition to Section 3
    
    # ------------------ 3. PAID MEDIA SECTION ------------------
    h3 = doc.add_heading("3. Paid Media Scale & Cost Efficiency: Google Ads vs Meta Ads", level=1)
    h3.runs[0].font.color.rgb = RGBColor(0x0A, 0x25, 0x40)
    h3.runs[0].font.size = Pt(14)
    h3.paragraph_format.space_before = Pt(0)
    h3.paragraph_format.space_after = Pt(6)
    
    p = doc.add_paragraph(
        "Paid advertising represented the primary growth accelerator over the past 13 months. "
        "Through strategic budget reallocation, granular campaign structure, negative keyword pruning, and conversational ad testing, the paid channels delivered 12,655 leads for ₹11.17 Lakhs at an average blended CPL of ₹88.29."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(8)
    
    # Paid Media Table
    p_sub = doc.add_paragraph("Table 3.1: Complete Monthly Paid Media Performance Breakdown")
    p_sub.runs[0].bold = True
    p_sub.runs[0].font.size = Pt(10.5)
    p_sub.runs[0].font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
    p_sub.paragraph_format.space_after = Pt(4)
    
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
        set_cell_margins(cell, top=60, bottom=60, left=25, right=25)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(7.5)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(paid_monthly_data):
        row = t_pm.rows[r_idx + 1]
        is_total = (r_idx == len(paid_monthly_data) - 1)
        bg = "EBF3FA" if is_total else ("F8F9FA" if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, text in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = widths_pm[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=50, bottom=50, left=35, right=35)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 0 else WD_ALIGN_PARAGRAPH.RIGHT
            run = p.add_run(text)
            run.font.size = Pt(7.5)
            if is_total or c_idx == 0:
                run.bold = True
                
    doc.add_paragraph()
    
    # Paid Media Deep Dive Narrative
    p_meta = doc.add_paragraph()
    r = p_meta.add_run("Key Paid Media Takeaways & Channel Dynamics:\n")
    r.bold = True
    r.font.size = Pt(10.5)
    
    bullet1 = doc.add_paragraph(style='List Bullet')
    r1 = bullet1.add_run("Meta Ads Transformation (-88.6% CPL): ")
    r1.bold = True
    bullet1.add_run(
        "Meta Ads underwent a total revolution. At the start of the engagement in December 2025, Meta CPL peaked at ₹287.65. "
        "By transitioning spend into conversational WhatsApp ad sets (specifically 'New Leads ad set' and 'Leads ad set - 7.11.25 – Copy'), "
        "Meta CPL plunged to an astounding ₹32.74 in October 2026, delivering 1,016 leads in a single month for just ₹33,260.77."
    )
    
    bullet2 = doc.add_paragraph(style='List Bullet')
    r2 = bullet2.add_run("Google Ads Scaling & Quality (+272% Volume): ")
    r2.bold = True
    bullet2.add_run(
        "Google Ads scaled consistently from 208 leads in November 2025 to a peak of 775 leads in July 2026. "
        "During July 2026, Google Ads CPL dropped to a record low of ₹58.45. Google search traffic consistently captured high-urgency, "
        "high-value transmission, IEPF, and loss of share cases."
    )
    
    doc.add_page_break() # Clean transition to Section 4
    
    # ------------------ 4. SEO & GSC SECTION ------------------
    h4 = doc.add_heading("4. Search Engine Optimization (SEO) & Google Search Domination", level=1)
    h4.runs[0].font.color.rgb = RGBColor(0x0A, 0x25, 0x40)
    h4.runs[0].font.size = Pt(14)
    h4.paragraph_format.space_before = Pt(0)
    h4.paragraph_format.space_after = Pt(6)
    
    p = doc.add_paragraph(
        "Organic search represents Share Samadhan's most durable competitive asset. Data from Google Search Console (GSC) "
        "confirms that Share Samadhan has achieved categorical dominance for legal share recovery and IEPF procedures in India."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(8)
    
    # SEO Metrics Highlights
    seo_box = doc.add_table(rows=1, cols=4)
    seo_box.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths_sb = [Inches(1.8), Inches(1.8), Inches(1.8), Inches(2.1)]
    
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
        set_cell_margins(cell, top=80, bottom=80, left=60, right=60)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_val = p.add_run(f"{val}\n")
        r_val.bold = True
        r_val.font.size = Pt(12)
        r_val.font.color.rgb = RGBColor.from_string(col)
        r_lbl = p.add_run(label)
        r_lbl.font.size = Pt(8.0)
        r_lbl.font.color.rgb = RGBColor(0x55, 0x55, 0x55)
        
    doc.add_paragraph()
    
    # Top Queries Table
    p_sub = doc.add_paragraph("Table 4.1: Top Google Organic Search Queries & Category Monopoly")
    p_sub.runs[0].bold = True
    p_sub.runs[0].font.size = Pt(10.5)
    p_sub.runs[0].font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
    p_sub.paragraph_format.space_after = Pt(4)
    
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
    widths_q = [Inches(2.2), Inches(0.9), Inches(1.1), Inches(0.9), Inches(2.4)]
    
    for c_idx, text in enumerate(headers_q):
        cell = t_q.cell(0, c_idx)
        cell.width = widths_q[c_idx]
        set_cell_background(cell, "0A2540")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(queries_data):
        row = t_q.rows[r_idx + 1]
        bg = "F8F9FA" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, text in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = widths_q[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if c_idx in [1, 2, 3] else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(text)
            run.font.size = Pt(8.0)
            if c_idx == 0:
                run.bold = True
                
    doc.add_paragraph()
    
    # Technical SEO Milestones Bullet Points
    p_t = doc.add_paragraph()
    r = p_t.add_run("Key Technical SEO & Content Production Deliverables:\n")
    r.bold = True
    r.font.size = Pt(10.5)
    
    items = [
        ("34 Authoritative Pillar Articles: ", "Published in-depth regulatory guides on IEPF-5 procedures, deceased shareholder succession, and physical-to-Demat conversion rules."),
        ("100% On-Page Optimization: ", "Rewrote and audited meta titles, meta descriptions, and H1/H2 header hierarchies across all core commercial pages."),
        ("Technical Infrastructure Remediations: ", "Resolved duplicate canonical tag issues, compressed legacy oversized images (>100KB), updated XML sitemaps, and eliminated crawl errors."),
        ("AEO (Answer Engine Optimization): ", "Implemented structured JSON-LD schema (FAQPage, FinancialService, Article) to capture Google AI Overviews and featured rich snippets.")
    ]
    for b_title, b_desc in items:
        bp = doc.add_paragraph(style='List Bullet')
        r_t = bp.add_run(b_title)
        r_t.bold = True
        bp.add_run(b_desc)
        
    doc.add_page_break() # Clean transition to Section 5
    
    # ------------------ 5. GA4 SECTION ------------------
    h5 = doc.add_heading("5. Website Audience & Organic Conversion Performance (GA4)", level=1)
    h5.runs[0].font.color.rgb = RGBColor(0x0A, 0x25, 0x40)
    h5.runs[0].font.size = Pt(14)
    h5.paragraph_format.space_before = Pt(0)
    h5.paragraph_format.space_after = Pt(6)
    
    p = doc.add_paragraph(
        "Google Analytics 4 (GA4) traffic intelligence demonstrates robust, continuous top-of-funnel visitor acquisition, capturing 165,849 Total Users and 161,491 New Users. "
        "Crucially, Organic Search delivered 39,998 visitors who converted into 2,685 verified organic leads – an extraordinary 6.71% visitor-to-lead conversion rate."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(8)
    
    # GA4 Monthly Table
    p_sub = doc.add_paragraph("Table 5.1: Monthly Website Traffic & Organic Lead Generation (GA4)")
    p_sub.runs[0].bold = True
    p_sub.runs[0].font.size = Pt(10.5)
    p_sub.runs[0].font.color.rgb = RGBColor(0x00, 0x66, 0xCC)
    p_sub.paragraph_format.space_after = Pt(4)
    
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
    widths_ga4 = [Inches(1.1), Inches(1.0), Inches(1.0), Inches(0.9), Inches(1.2), Inches(1.1), Inches(1.2)]
    
    for c_idx, text in enumerate(headers_ga4):
        cell = t_ga4.cell(0, c_idx)
        cell.width = widths_ga4[c_idx]
        set_cell_background(cell, "0A2540")
        set_cell_margins(cell, top=80, bottom=80, left=60, right=60)
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(8.0)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(ga4_monthly_data):
        row = t_ga4.rows[r_idx + 1]
        is_total = (r_idx == len(ga4_monthly_data) - 1)
        bg = "EBF3FA" if is_total else ("F8F9FA" if r_idx % 2 == 1 else "FFFFFF")
        for c_idx, text in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = widths_ga4[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if c_idx >= 1 else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(text)
            run.font.size = Pt(7.5)
            if is_total or c_idx == 0:
                run.bold = True
                
    doc.add_page_break() # Clean transition to Section 6
    
    # ------------------ 6. SOCIAL MEDIA SECTION ------------------
    h6 = doc.add_heading("6. Omnichannel Social Media Growth & Brand Authority", level=1)
    h6.runs[0].font.color.rgb = RGBColor(0x0A, 0x25, 0x40)
    h6.runs[0].font.size = Pt(14)
    h6.paragraph_format.space_before = Pt(0)
    h6.paragraph_format.space_after = Pt(6)
    
    p = doc.add_paragraph(
        "Multi-channel social media engagement surged dramatically, expanding Share Samadhan's reputation across professional "
        "B2B audiences, high-net-worth investors, and retail shareholders."
    )
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(8)
    
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
    widths_soc = [Inches(1.2), Inches(1.5), Inches(1.2), Inches(1.4), Inches(2.2)]
    
    for c_idx, text in enumerate(headers_soc):
        cell = t_soc.cell(0, c_idx)
        cell.width = widths_soc[c_idx]
        set_cell_background(cell, "0A2540")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        run = p.add_run(text)
        run.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
        
    for r_idx, row_data in enumerate(social_data):
        row = t_soc.rows[r_idx + 1]
        bg = "F8F9FA" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, text in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = widths_soc[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(text)
            run.font.size = Pt(8.0)
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
