import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import win32com.client

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=80, bottom=80, left=130, right=130):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="D1D5DB", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:left w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'  <w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def add_callout(doc, text, title="STRATEGIC FOCUS", border_color="2361A8", bg_color="F0F4F8"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:left w:val="single" w:sz="36" w:space="0" w:color="{border_color}"/>'
        f'  <w:top w:val="none"/>'
        f'  <w:right w:val="none"/>'
        f'  <w:bottom w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    r_title = p.add_run(f"[{title}] ")
    r_title.bold = True
    r_title.font.size = Pt(9)
    r_title.font.name = 'Arial'
    r_title.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    
    r_body = p.add_run(text)
    r_body.font.size = Pt(9)
    r_body.font.name = 'Arial'
    r_body.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
    
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(0)
    p_spacer.paragraph_format.space_after = Pt(2)

def format_table(table, col_widths, col_alignments, header_bg="1B365D", alt_bg="F8FAFC", pad_tb=70):
    set_table_borders(table)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    hdr = table.rows[0]
    trPr = hdr._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    
    for idx, cell in enumerate(hdr.cells):
        set_cell_background(cell, header_bg)
        set_cell_margins(cell, top=pad_tb+30, bottom=pad_tb+30, left=130, right=130)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        for p in cell.paragraphs:
            p.alignment = col_alignments[idx]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            for r in p.runs:
                r.bold = True
                r.font.name = 'Arial'
                r.font.size = Pt(9)
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                
    for r_idx, row in enumerate(table.rows[1:]):
        bg = alt_bg if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, cell in enumerate(row.cells):
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=pad_tb, bottom=pad_tb, left=130, right=130)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            for p in cell.paragraphs:
                p.alignment = col_alignments[c_idx]
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                for r in p.runs:
                    r.font.name = 'Arial'
                    r.font.size = Pt(8.5)
                    r.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
                    
    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = Inches(width)

def build_client_proposal():
    doc = docx.Document()
    
    for section in doc.sections:
        section.top_margin = Inches(0.7)
        section.bottom_margin = Inches(0.7)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)
        section.header.is_linked_to_previous = False
        
        hp = section.header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("TECHNO EXPONENT  |  Performance Marketing Practice  •  Client Proposal")
        hrun.font.name = 'Arial'
        hrun.font.size = Pt(8)
        hrun.font.color.rgb = RGBColor(0x71, 0x80, 0x96)
        
        fp = section.footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Finaquity Lead Generation Proposal  •  Strictly Confidential  •  Page ")
        frun.font.name = 'Arial'
        frun.font.size = Pt(8)
        frun.font.color.rgb = RGBColor(0x71, 0x80, 0x96)

    # ------------------ COVER SECTION (PAGE 1) ------------------
    p_agency = doc.add_paragraph()
    p_agency.paragraph_format.space_before = Pt(16)
    p_agency.paragraph_format.space_after = Pt(4)
    r_ag = p_agency.add_run("TECHNO EXPONENT")
    r_ag.font.name = 'Arial'
    r_ag.font.size = Pt(13)
    r_ag.bold = True
    r_ag.font.color.rgb = RGBColor(0x23, 0x61, 0xA8)
    
    p_tag = doc.add_paragraph()
    p_tag.paragraph_format.space_before = Pt(0)
    p_tag.paragraph_format.space_after = Pt(36)
    r_tag = p_tag.add_run("Full-Funnel Performance Marketing  |  Digital Growth Partner")
    r_tag.font.name = 'Arial'
    r_tag.font.size = Pt(10)
    r_tag.font.color.rgb = RGBColor(0x71, 0x80, 0x96)
    
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(10)
    r_title = p_title.add_run("DIGITAL MARKETING PROPOSAL &\nLEAD GENERATION STRATEGY")
    r_title.font.name = 'Arial'
    r_title.font.size = Pt(24)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(28)
    r_sub = p_sub.add_run("A Lean-Budget Performance Marketing Engine to Generate Qualified Attendees for Finaquity's Masterclasses, Webinars & Executive Courses")
    r_sub.font.name = 'Arial'
    r_sub.font.size = Pt(12)
    r_sub.italic = True
    r_sub.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)
    
    meta_tbl = doc.add_table(rows=5, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Client / Brand:", "Finaquity (finaquity.com) | Incubation: AIC BIMTECH"),
        ("Prepared For:", "Tanmay Singh Rajput (Founder) & Leadership Team"),
        ("Prepared By:", "Techno Exponent Performance Marketing Practice"),
        ("Primary Deliverable:", "Qualified Lead Generation for Masterclasses, Webinars & Courses"),
        ("Monthly Media Budget:", "₹50,000 – ₹60,000 / month (~₹2,000 / day, paid directly to ad platforms)")
    ]
    for idx, (label, val) in enumerate(meta_data):
        row = meta_tbl.rows[idx]
        set_cell_background(row.cells[0], "F0F4F8")
        set_cell_background(row.cells[1], "FFFFFF")
        set_cell_margins(row.cells[0], top=80, bottom=80, left=120, right=120)
        set_cell_margins(row.cells[1], top=80, bottom=80, left=120, right=120)
        
        p0 = row.cells[0].paragraphs[0]
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(label)
        r0.bold = True
        r0.font.name = 'Arial'
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        
        p1 = row.cells[1].paragraphs[0]
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(val)
        r1.font.name = 'Arial'
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
        
    set_table_borders(meta_tbl, color="CBD5E0", sz="4")
    for row in meta_tbl.rows:
        row.cells[0].width = Inches(2.4)
        row.cells[1].width = Inches(4.6)
        
    doc.add_page_break()

    # ------------------ PAGE 2: EXEC SUMMARY & AUDIENCE ------------------
    h1 = doc.add_heading(level=1)
    r_h1 = h1.add_run("1. Executive Summary & Core Objective")
    r_h1.font.name = 'Arial'
    r_h1.font.size = Pt(14)
    r_h1.bold = True
    r_h1.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("The primary objective of this engagement is to build and manage a predictable, cost-efficient lead generation engine for Finaquity. Techno Exponent will generate high volumes of qualified registrations and attendees for Finaquity's exclusive webinars, masterclasses, and executive training sessions.")
    r.font.name = 'Arial'
    r.font.size = Pt(9.5)
    
    p2 = doc.add_paragraph()
    p2.paragraph_format.space_after = Pt(4)
    r2 = p2.add_run("In capital markets and financial stewardship, cold advertising that directly pitches discretionary wealth management experiences significant friction due to trust hurdles. Educating prospects through institutional-grade masterclasses and workshops breaks this barrier—delivering immense upfront value, proving market expertise, and creating an eager pool of qualified attendees for Finaquity to engage, consult, and onboard.")
    r2.font.name = 'Arial'
    r2.font.size = Pt(9.5)

    add_callout(
        doc,
        "Clear Division of Responsibilities:\n• Techno Exponent's Responsibility: Full-funnel digital marketing, ad creative production, audience targeting, conversion copy, campaign management across Meta & Google, tracking guidance, and continuous CPL optimization.\n• Finaquity's Responsibility: Landing page development & hosting (agency provides copy and wireframe), WhatsApp & CRM automation integration (agency provides messaging sequence), masterclass delivery, 1-on-1 consultations, and client onboarding.",
        title="AGENCY VS. CLIENT MANDATE",
        border_color="2361A8",
        bg_color="F0F4F8"
    )

    h2 = doc.add_heading(level=1)
    r_h2 = h2.add_run("2. Target Audience & Residential Tech Corridors")
    r_h2.font.name = 'Arial'
    r_h2.font.size = Pt(14)
    r_h2.bold = True
    r_h2.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("To maximize registration quality and maintain a low Cost Per Lead (CPL) on a lean budget, advertising will concentrate on high-density residential clusters where senior salaried professionals reside in India:")
    r.font.name = 'Arial'
    r.font.size = Pt(9.5)

    table_geo = doc.add_table(rows=4, cols=3)
    table_geo_data = [
        ["Metropolitan Corridor", "Target Residential Clusters", "Professional Audience Profile"],
        ["Bengaluru (Tech Capital)", "Whitefield, Sarjapur Road, Bellandur, HSR Layout, Koramangala, Indiranagar.", "Engineering Directors, Software Architects, Staff Engineers, Tech VPs at global firms, unicorns, and GCCs (CTC ₹25L–₹75L+)."],
        ["Gurugram / NCR (Corporate Hub)", "Golf Course Road, DLF Phases 1–5, Sushant Lok, Sectors 42–57; Noida Sectors 128 & 137.", "Management Consultants, Investment Bankers, Fintech Leaders, and Corporate Strategy Heads."],
        ["Hyderabad & Pune (Growth Centers)", "Gachibowli, Kondapur, Financial District (HYD); Baner, Aundh, Kharadi, Hinjewadi (PNE).", "Senior Tech Leads, R&D Heads, Delivery Managers, and Enterprise Solution Architects."]
    ]
    for r_idx, row_data in enumerate(table_geo_data):
        for c_idx, val in enumerate(row_data):
            p_cell = table_geo.rows[r_idx].cells[c_idx].paragraphs[0]
            p_cell.text = val
    format_table(
        table_geo,
        col_widths=[1.8, 2.7, 2.5],
        col_alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT],
        pad_tb=60
    )

    doc.add_page_break()

    # ------------------ PAGE 3: CHANNELS & FUNNEL ------------------
    h3 = doc.add_heading(level=1)
    r_h3 = h3.add_run("3. Lead Generation Channels & Lean Media Plan")
    r_h3.font.name = 'Arial'
    r_h3.font.size = Pt(14)
    r_h3.bold = True
    r_h3.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("We deploy an 80/20 media allocation model designed to generate steady, predictable masterclass registrations while capturing active search intent:")
    r.font.name = 'Arial'
    r.font.size = Pt(9.5)

    table_media = doc.add_table(rows=4, cols=4)
    table_media_data = [
        ["Channel", "Monthly Budget", "Targeting Setup & Strategy", "Role in Funnel & Expected CPL"],
        ["Meta Ads (Instagram & Facebook)", "₹48,000 (80%)\n~₹1,600 / day", "Consolidated campaign across residential clusters with 4 distinct creative concepts. Professional title and affluence proxies.", "Primary volume engine.\nPlanning CPL: ₹300 – ₹550 per registration."],
        ["Google Search Ads", "₹12,000 (20%)\n~₹400 / day", "Exact & phrase match on high-intent terms: [portfolio management for salaried], [pms vs mutual funds], [wealth masterclass].", "Intent capture engine.\nPlanning CPL: ₹500 – ₹800 per registration."],
        ["Organic & Owned Channels", "₹0 media cost", "Client network referrals, employer wellness sessions, and founder educational LinkedIn thought leadership.", "Supplemental zero-CAC registrations that increase total cohort volume."]
    ]
    for r_idx, row_data in enumerate(table_media_data):
        for c_idx, val in enumerate(row_data):
            p_cell = table_media.rows[r_idx].cells[c_idx].paragraphs[0]
            p_cell.text = val
    format_table(
        table_media,
        col_widths=[1.7, 1.4, 2.4, 1.5],
        col_alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT],
        pad_tb=60
    )

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_after = Pt(4)

    h4 = doc.add_heading(level=1)
    r_h4 = h4.add_run("4. The Educational Masterclass & Course Lead Funnel")
    r_h4.font.name = 'Arial'
    r_h4.font.size = Pt(14)
    r_h4.bold = True
    r_h4.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("The funnel is engineered to pre-screen registrants, build anticipation, and maximize live show-up rates:")
    r.font.name = 'Arial'
    r.font.size = Pt(9.5)

    bullets = [
        ("Dedicated Registration Landing Page (Client-Built): ", "Developed and hosted by Finaquity (wealth.finaquity.com or learn.finaquity.com) using high-converting wireframes and copy provided by Techno Exponent."),
        ("Pre-Qualification Lead Form: ", "Form captures Name, Corporate Email, Mobile Number (WhatsApp), City, CTC Band (₹25L–₹40L, ₹40L–₹75L, ₹75L+), Investable Corpus (₹15L–₹35L, ₹35L–₹50L, ₹50L+), and explicit consent."),
        ("WhatsApp & CRM Automation (Client-Integrated): ", "Configured in Finaquity's CRM/WhatsApp gateway to send calendar passes (.ics), reminders, and countdowns using timing schedules and message copy created by Techno Exponent."),
        ("Masterclass / Course Delivery (Finaquity): ", "75-minute structured session covering mutual fund overlap teardowns, drawdown math, rules-based investing, and ending with an invitation to book a 1-on-1 portfolio review.")
    ]
    for b_title, b_desc in bullets:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(2)
        r_bt = bp.add_run(b_title)
        r_bt.bold = True
        r_bt.font.name = 'Arial'
        r_bt.font.size = Pt(9)
        r_bt.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
        r_bd = bp.add_run(b_desc)
        r_bd.font.name = 'Arial'
        r_bd.font.size = Pt(9)

    doc.add_page_break()

    # ------------------ PAGE 4: FORECASTS & ROADMAP ------------------
    h5 = doc.add_heading(level=1)
    r_h5 = h5.add_run("5. Campaign Forecasts & Lead Generation Metrics")
    r_h5.font.name = 'Arial'
    r_h5.font.size = Pt(14)
    r_h5.bold = True
    r_h5.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("The following model illustrates expected monthly lead generation performance across three planning cases at the ₹60,000 monthly media budget:")
    r.font.name = 'Arial'
    r.font.size = Pt(9.5)

    # EXACT USER REQUIREMENTS:
    # Monthly Media Budget: ₹60,000
    # Blended Cost Per Registration (CPL): 550 - 400 - 300
    # Masterclass / Class Registrations: 109 - 150 - 200 leads
    # Live Attendance Rate: 10% – 20% range
    # Qualified Registrations: REMOVED
    table_forecast = doc.add_table(rows=5, cols=4)
    table_forecast_data = [
        ["Lead Generation Metric", "Conservative Case", "Expected Target", "Optimized Scale Case"],
        ["Monthly Media Budget", "₹60,000", "₹60,000", "₹60,000"],
        ["Blended Cost Per Registration (CPL)", "₹550", "₹400", "₹300"],
        ["Masterclass / Class Registrations", "109 leads", "150 leads", "200 leads"],
        ["Live Attendance Rate (Thursday 8 PM)", "10% – 20% (~11 to ~22 attendees)", "10% – 20% (~15 to ~30 attendees)", "10% – 20% (~20 to ~40 attendees)"]
    ]
    for r_idx, row_data in enumerate(table_forecast_data):
        for c_idx, val in enumerate(row_data):
            p_cell = table_forecast.rows[r_idx].cells[c_idx].paragraphs[0]
            p_cell.text = val
    format_table(
        table_forecast,
        col_widths=[2.5, 1.5, 1.5, 1.5],
        col_alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT],
        pad_tb=60
    )

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_after = Pt(6)

    h6 = doc.add_heading(level=1)
    r_h6 = h6.add_run("6. 90-Day Implementation & Delivery Roadmap")
    r_h6.font.name = 'Arial'
    r_h6.font.size = Pt(14)
    r_h6.bold = True
    r_h6.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    table_road = doc.add_table(rows=4, cols=3)
    table_road_data = [
        ["Sprint Phase", "Key Execution Activities", "Milestones & Output Deliverables"],
        ["Month 1: Foundation & Asset Build", "• Client deploys Landing Page & WhatsApp/CRM integration\n• Agency designs 4 high-converting ad concepts & copy\n• Agency installs Meta Pixel, Conversions API & Google tags\n• Agency delivers automated WhatsApp/email message sequences", "Tested funnel live. Compliance sign-off on ad copy and landing page. Baseline tracking dashboard ready."],
        ["Month 2: Campaign Pilot & First Cohorts", "• Launch ₹2,000/day ad campaigns in BLR, GGN, HYD\n• Host 2 bi-weekly live masterclasses / webinars\n• Deliver registered leads directly to Finaquity\n• Monitor CPL, attendance rate, and audience feedback", "Initial live cohorts delivered. Real-world CPL benchmark established."],
        ["Month 3: Calibration & Scaling", "• Refresh ad creatives based on CTR and CPL data\n• Scale winning ad sets across top-performing pin codes\n• Activate organic founder LinkedIn content\n• Optimize registration-to-attendee conversion rate", "Optimized CPL engine delivering consistent weekly registrant cohorts for ongoing webinars and courses."]
    ]
    for r_idx, row_data in enumerate(table_road_data):
        for c_idx, val in enumerate(row_data):
            p_cell = table_road.rows[r_idx].cells[c_idx].paragraphs[0]
            p_cell.text = val
    format_table(
        table_road,
        col_widths=[1.8, 3.2, 2.0],
        col_alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT],
        pad_tb=60
    )

    doc.add_page_break()

    # ------------------ PAGE 5: COMPLIANCE & BLANK COMMERCIAL SCOPE ------------------
    h7 = doc.add_heading(level=1)
    r_h7 = h7.add_run("7. Regulatory & Compliance Framework")
    r_h7.font.name = 'Arial'
    r_h7.font.size = Pt(14)
    r_h7.bold = True
    r_h7.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run("All advertising materials, landing pages, and lead communications adhere to SEBI's advertising code and data protection standards:")
    r.font.name = 'Arial'
    r.font.size = Pt(9.5)

    table_comp = doc.add_table(rows=3, cols=2)
    table_comp_data = [
        ["Compliance Dimension", "Execution Protocol"],
        ["No Guaranteed Return Claims", "All promotional copy focuses strictly on financial literacy, portfolio risk engineering, and rules-based investing. Zero promises of guaranteed or market-beating returns."],
        ["Statutory Disclaimers & DPDP", "SEBI statutory disclaimers displayed on all landing pages and decks. Explicit opt-in consent for email/WhatsApp aligned with the Digital Personal Data Protection Act."]
    ]
    for r_idx, row_data in enumerate(table_comp_data):
        for c_idx, val in enumerate(row_data):
            p_cell = table_comp.rows[r_idx].cells[c_idx].paragraphs[0]
            p_cell.text = val
    format_table(
        table_comp,
        col_widths=[2.2, 4.8],
        col_alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT],
        pad_tb=60
    )

    p_spacer2 = doc.add_paragraph()
    p_spacer2.paragraph_format.space_before = Pt(8)
    p_spacer2.paragraph_format.space_after = Pt(6)

    h8 = doc.add_heading(level=1)
    r_h8 = h8.add_run("8. Commercial Scope & Engagement Terms")
    r_h8.font.name = 'Arial'
    r_h8.font.size = Pt(14)
    r_h8.bold = True
    r_h8.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_comm = doc.add_paragraph()
    p_comm.paragraph_format.space_after = Pt(4)
    r_comm = p_comm.add_run("The scope of services and commercials for managing the Masterclass & Course Lead Generation campaigns are outlined below:")
    r_comm.font.name = 'Arial'
    r_comm.font.size = Pt(9.5)

    # USER REQUIREMENT:
    # "Need to done by the client - Landing Page, WhatsApp & CRM Automation Integration"
    # "Commercial Scope & Engagement Terms - keep it blank"
    table_price = doc.add_table(rows=4, cols=3)
    table_p_data = [
        ["Scope Component", "Agency Management Fee", "Direct Media Spend / Execution"],
        ["Masterclass & Webinar Lead Generation Retainer (Meta & Google Campaign Management)", "", "₹50,000 – ₹60,000 / month\n(Paid directly to ad platforms)"],
        ["Landing Page Development & Hosting", "To be done by Client\n(Agency provides copy & wireframe)", "Client infrastructure"],
        ["WhatsApp & CRM Automation Integration", "To be done by Client\n(Agency provides sequence scripts & timing)", "Client CRM / WhatsApp API"]
    ]
    for r_idx, row_data in enumerate(table_p_data):
        for c_idx, val in enumerate(row_data):
            p_cell = table_price.rows[r_idx].cells[c_idx].paragraphs[0]
            p_cell.text = val
    format_table(
        table_price,
        col_widths=[2.8, 2.2, 2.0],
        col_alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT],
        pad_tb=70
    )

    p_spacer3 = doc.add_paragraph()
    p_spacer3.paragraph_format.space_after = Pt(8)

    add_callout(
        doc,
        "Commercial Governance & Division of Responsibility:\n• 100% Asset Ownership: Finaquity retains full ownership of all ad accounts, tracking pixels, landing pages, creative assets, and lead databases.\n• Media Transparency: 100% of media spend is billed directly by Meta and Google to Finaquity with zero agency surcharge.\n• Client-Managed Integrations: Landing page development and WhatsApp/CRM tooling are managed and hosted by Finaquity, with Techno Exponent providing conversion wireframes, ad copy, and automated messaging scripts.",
        title="COMMERCIAL GOVERNANCE",
        border_color="2361A8",
        bg_color="F0F4F8"
    )

    report_docx = os.path.abspath(r"C:\Users\test\Videos\Office\reports\Finaquity_HNWI_Marketing_Strategy_and_Proposal.docx")
    report_pdf = os.path.abspath(r"C:\Users\test\Videos\Office\reports\Finaquity_HNWI_Marketing_Strategy_and_Proposal.pdf")
    proposal_docx = os.path.abspath(r"C:\Users\test\Videos\Office\Proposals\Digital_Marketing_Proposal_Finaquity_Techno_Exponent.docx")
    proposal_pdf = os.path.abspath(r"C:\Users\test\Videos\Office\Proposals\Digital_Marketing_Proposal_Finaquity_Techno_Exponent.pdf")

    os.makedirs(os.path.dirname(report_docx), exist_ok=True)
    os.makedirs(os.path.dirname(proposal_docx), exist_ok=True)

    doc.save(report_docx)
    print(f"Saved clean client DOCX to: {report_docx}")
    shutil.copyfile(report_docx, proposal_docx)
    print(f"Copied clean client DOCX to: {proposal_docx}")

    print("Converting DOCX to PDF via MS Word COM...")
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    try:
        wdoc = word.Documents.Open(report_docx)
        wdoc.SaveAs(report_pdf, FileFormat=17)
        wdoc.Close()
        print(f"Saved clean client PDF to: {report_pdf}")
        shutil.copyfile(report_pdf, proposal_pdf)
        print(f"Copied clean client PDF to: {proposal_pdf}")
    finally:
        word.Quit()

if __name__ == '__main__':
    build_client_proposal()
