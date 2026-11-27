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

def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
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

def add_callout(doc, text, title="STRATEGIC DIRECTIVE", border_color="2361A8", bg_color="F0F4F8"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
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
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(3)
    r_title = p.add_run(f"[{title}] ")
    r_title.bold = True
    r_title.font.size = Pt(10)
    r_title.font.name = 'Arial'
    r_title.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    
    r_body = p.add_run(text)
    r_body.font.size = Pt(10)
    r_body.font.name = 'Arial'
    r_body.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
    
    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(0)
    p_spacer.paragraph_format.space_after = Pt(4)

def format_table(table, col_widths, col_alignments, header_bg="1B365D", alt_bg="F8FAFC"):
    set_table_borders(table)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    hdr = table.rows[0]
    trPr = hdr._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    
    for idx, cell in enumerate(hdr.cells):
        set_cell_background(cell, header_bg)
        set_cell_margins(cell, top=140, bottom=140, left=150, right=150)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
        for p in cell.paragraphs:
            p.alignment = col_alignments[idx]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            for r in p.runs:
                r.bold = True
                r.font.name = 'Arial'
                r.font.size = Pt(9.5)
                r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
                
    for r_idx, row in enumerate(table.rows[1:]):
        bg = alt_bg if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, cell in enumerate(row.cells):
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            for p in cell.paragraphs:
                p.alignment = col_alignments[c_idx]
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                for r in p.runs:
                    r.font.name = 'Arial'
                    r.font.size = Pt(9)
                    r.font.color.rgb = RGBColor(0x2D, 0x37, 0x48)
                    
    for row in table.rows:
        for idx, width in enumerate(col_widths):
            row.cells[idx].width = Inches(width)

def build_proposal():
    doc = docx.Document()
    
    # Page Setup (Letter, 0.8 in margins)
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        section.header.is_linked_to_previous = False
        
        # Header setup
        hp = section.header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("TECHNO EXPONENT  |  Performance Marketing Practice  •  Confidential Client Proposal")
        hrun.font.name = 'Arial'
        hrun.font.size = Pt(8)
        hrun.font.color.rgb = RGBColor(0x71, 0x80, 0x96)
        
        # Footer setup
        fp = section.footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Finaquity Salaried Wealth Acquisition Proposal  •  Strictly Confidential  •  Page ")
        frun.font.name = 'Arial'
        frun.font.size = Pt(8)
        frun.font.color.rgb = RGBColor(0x71, 0x80, 0x96)

    # ------------------ COVER / TITLE SECTION ------------------
    p_agency = doc.add_paragraph()
    p_agency.paragraph_format.space_before = Pt(12)
    p_agency.paragraph_format.space_after = Pt(4)
    r_ag = p_agency.add_run("TECHNO EXPONENT")
    r_ag.font.name = 'Arial'
    r_ag.font.size = Pt(12)
    r_ag.bold = True
    r_ag.font.color.rgb = RGBColor(0x23, 0x61, 0xA8)
    
    p_tag = doc.add_paragraph()
    p_tag.paragraph_format.space_before = Pt(0)
    p_tag.paragraph_format.space_after = Pt(28)
    r_tag = p_tag.add_run("CMMI Level 5 Certified Digital Growth Partner  |  Full-Funnel Performance Marketing")
    r_tag.font.name = 'Arial'
    r_tag.font.size = Pt(9.5)
    r_tag.font.color.rgb = RGBColor(0x71, 0x80, 0x96)
    
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("DIGITAL MARKETING PROPOSAL &\nSALARIED PROFESSIONALS ACQUISITION STRATEGY")
    r_title.font.name = 'Arial'
    r_title.font.size = Pt(22)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(20)
    r_sub = p_sub.add_run("A Lean-Budget Domestic Playbook for Scaling SEBI-Regulated Wealth Stewardship & PMS via Closed-Door Masterclasses & 1-on-1 Portfolio Diagnostics")
    r_sub.font.name = 'Arial'
    r_sub.font.size = Pt(11.5)
    r_sub.italic = True
    r_sub.font.color.rgb = RGBColor(0x4A, 0x55, 0x68)
    
    # Metadata Card
    meta_tbl = doc.add_table(rows=5, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Client Name / Brand:", "Finaquity (finaquity.com) | Incubation: AIC BIMTECH"),
        ("Prepared For:", "Tanmay Singh Rajput (Founder) & Leadership Team"),
        ("Prepared By:", "Techno Exponent Performance Marketing Practice"),
        ("Primary Target Segment:", "High-Income Salaried Working Professionals in India (CTC ₹25L–₹75L+)"),
        ("Monthly Media Spend (Pilot):", "₹60,000 / month (~₹2,000 / day) — India-First Lean Model")
    ]
    for idx, (label, val) in enumerate(meta_data):
        row = meta_tbl.rows[idx]
        set_cell_background(row.cells[0], "F0F4F8")
        set_cell_background(row.cells[1], "FFFFFF")
        set_cell_margins(row.cells[0], top=70, bottom=70, left=120, right=120)
        set_cell_margins(row.cells[1], top=70, bottom=70, left=120, right=120)
        
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
        row.cells[1].width = Inches(4.5)
        
    doc.add_page_break()

    # ------------------ SECTION 1: EXECUTIVE SUMMARY ------------------
    h1 = doc.add_heading(level=1)
    r_h1 = h1.add_run("1. Executive Summary & India-First Strategy Pivot")
    r_h1.font.name = 'Arial'
    r_h1.font.size = Pt(16)
    r_h1.bold = True
    r_h1.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)
    
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("In alignment with client feedback to optimize for a lean advertising budget and prioritize domestic conversion speed, Techno Exponent has re-engineered Finaquity's market entry strategy. Rather than deploying capital across diffuse multi-crore ultra-HNWI or NRI expat pools, this playbook focuses strictly on India's High-Earning Salaried Working Professionals.")
    r.font.name = 'Arial'
    r.font.size = Pt(10)
    
    p2 = doc.add_paragraph()
    p2.paragraph_format.space_after = Pt(6)
    r2 = p2.add_run("Salaried professionals in India's top metropolitan tech and corporate corridors (Bengaluru, Hyderabad, Gurugram, Pune, Mumbai, Noida) earning ₹25L to ₹75L+ CTC represent the most underserved, high-cash-flow demographic in wealth management. They are chronically time-poor, suffer from chaotic mutual fund duplication (running 12+ SIPs across 5 AMCs), and lack the hours to research individual balance sheets or track daily market swings.")
    r2.font.name = 'Arial'
    r2.font.size = Pt(10)

    p3 = doc.add_paragraph()
    p3.paragraph_format.space_after = Pt(8)
    r3 = p3.add_run("By deploying a lean, hyper-targeted ad budget of ₹60,000 / month (~₹2,000 / day) combined with founder thought leadership, Finaquity can acquire qualified registrations at a cost of ₹220–₹350 per lead. High-intent attendees are then converted into active investors via an exclusive 75-minute masterclass ('The Salaried Wealth Blueprint') and a complimentary 1-on-1 Portfolio Health & Risk Audit.")
    r3.font.name = 'Arial'
    r3.font.size = Pt(10)

    add_callout(
        doc,
        "The Two-Tier Escalator Model:\n• Tier 1 (Advisory Model Portfolio): ₹15L to ₹49L liquid assets. Fee-based advisory executed directly in the client's existing Zerodha, Groww, or ICICI Direct Demat.\n• Tier 2 (SEBI Discretionary PMS): ₹50L+ liquid assets. Full discretionary portfolio management under statutory SEBI rules.\nThis escalator maximizes conversion because mid-career professionals enter at ₹20L–₹35L and naturally upgrade to PMS as annual bonuses and ESOPs vest.",
        title="COMMERCIAL ARCHITECTURE",
        border_color="2361A8",
        bg_color="F0F4F8"
    )

    # ------------------ SECTION 2: TARGET AUDIENCE & TECH CORRIDORS ------------------
    h2 = doc.add_heading(level=1)
    r_h2 = h2.add_run("2. Target Audience Profiles & Geographic Pin Code Clusters")
    r_h2.font.name = 'Arial'
    r_h2.font.size = Pt(16)
    r_h2.bold = True
    r_h2.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("To eliminate wasted ad spend on a lean budget, campaigns will concentrate strictly on geographic pin codes with dense corporate and tech employment:")
    r.font.name = 'Arial'
    r.font.size = Pt(10)

    table_geo = doc.add_table(rows=4, cols=3)
    table_geo_data = [
        ["Metropolitan Corridor", "Target Pin Codes & Sub-Markets", "Core Professional Demographics"],
        ["Bengaluru (Tech Capital)", "Whitefield (560066), Bellandur (560103), HSR Layout (560102), Indiranagar (560038), Outer Ring Road Tech Parks.", "Engineering Directors, Software Architects, Staff Engineers, Tech VPs at FAANG, Unicorns & GCCs (CTC: ₹35L–₹90L)."],
        ["Gurugram / NCR (Corporate Hub)", "DLF Cyber City, Golf Course Road, DLF Phase 1–5, Sector 42–56, Noida Sector 62/128.", "Management Consultants (McKinsey, BCG, Big 4), Investment Banking VPs, Fintech Directors, Corporate Strategy Heads (CTC: ₹30L–₹75L)."],
        ["Hyderabad & Pune (Growth Centers)", "Hitec City, Gachibowli, Financial District (HYD); Hinjewadi Phase 1–3, Baner, Kharadi, Magarpatta (PNE).", "Senior Tech Leads, R&D Heads, Semiconductor Engineers, Global Delivery Heads (CTC: ₹25L–₹60L)."]
    ]
    for r_idx, row_data in enumerate(table_geo_data):
        for c_idx, val in enumerate(row_data):
            p_cell = table_geo.rows[r_idx].cells[c_idx].paragraphs[0]
            p_cell.text = val
    format_table(
        table_geo,
        col_widths=[1.8, 2.7, 2.4],
        col_alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    )

    doc.add_page_break()

    # ------------------ SECTION 3: LEAN BUDGET MEDIA ARCHITECTURE ------------------
    h3 = doc.add_heading(level=1)
    r_h3 = h3.add_run("3. Lean Media Architecture: ₹60,000 / Month (~₹2,000 / Day)")
    r_h3.font.name = 'Arial'
    r_h3.font.size = Pt(16)
    r_h3.bold = True
    r_h3.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("On a lean budget, dispersing capital across 5 different platforms dilutes algorithmic learning. We deploy a concentrated 75/25 split between Meta Ads and Google Search Exact Match:")
    r.font.name = 'Arial'
    r.font.size = Pt(10)

    table_media = doc.add_table(rows=3, cols=4)
    table_media_data = [
        ["Channel & Split", "Daily / Monthly Spend", "Targeting Filters & Keywords", "Expected Role & CPL"],
        ["Meta Ads (Instagram & FB)\n75% Allocation", "₹1,500 / day\n(₹45,000 / month)", "Tech Corridor Pin Codes + Job Titles (Software Architect, Engineering Director) + iPhone 13–16 Pro users.", "High-volume visual lead generation.\nTarget CPL: ₹220 – ₹300 per registration."],
        ["Google Search Ads\n25% Allocation", "₹500 / day\n(₹15,000 / month)", "Exact Match Only: [portfolio management for salaried], [pms vs mutual funds], [sebi portfolio manager bangalore].", "Captures high-intent corporate executives actively seeking wealth management.\nTarget CPL: ₹350 – ₹450."]
    ]
    for r_idx, row_data in enumerate(table_media_data):
        for c_idx, val in enumerate(row_data):
            p_cell = table_media.rows[r_idx].cells[c_idx].paragraphs[0]
            p_cell.text = val
    format_table(
        table_media,
        col_widths=[1.8, 1.5, 2.2, 1.4],
        col_alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    )

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_after = Pt(6)

    # ------------------ SECTION 4: THE MASTERCLASS FUNNEL ------------------
    h4 = doc.add_heading(level=1)
    r_h4 = h4.add_run("4. The Salaried Masterclass: Curriculum & Conversion Engine")
    r_h4.font.name = 'Arial'
    r_h4.font.size = Pt(16)
    r_h4.bold = True
    r_h4.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    add_callout(
        doc,
        "Masterclass Title: 'The Salaried Wealth Blueprint: How Busy Professionals Structure, Protect & Compound ₹25L+ Equity Portfolios (Without Watching Stock Tickers All Day).'\nSchedule: Alternate Thursday evenings at 8:00 PM IST (post-commute) via private Zoom.",
        title="MASTERCLASS SPECIFICATION",
        border_color="00AEEF",
        bg_color="F8FAFC"
    )

    table_curr = doc.add_table(rows=6, cols=3)
    table_curr_data = [
        ["Session Stage", "Subject Matter & Core Slides", "Attendee Psychological Transformation"],
        ["Module 1 (0-15m)", "The 'SIP Overload' Reality Check: Showing why 10 mutual funds buy the same 25 stocks.", "Exposes that their portfolio is not diversified; quantifies ₹60k–₹1L annual fee bleed."],
        ["Module 2 (15-30m)", "The Math of Asymmetric Drawdowns: Why a 35% drop requires +54% to recover.", "Shifts mindset from chasing risky multibaggers to protecting hard-earned savings."],
        ["Module 3 (30-45m)", "Factor Investing (Quality + Momentum + Low Volatility): Automated rules without daily trading.", "Demonstrates institutional rigor; proves alpha is generated by math, not market timing."],
        ["Module 4 (45-55m)", "Direct Demat Ownership: Your shares stay 100% in your Zerodha / Groww / ICICI account.", "Overcomes custody hesitation; proves client retains legal control and transparency."],
        ["Module 5 (55-75m)", "The Offer: Complimentary 45-Min 1-on-1 Portfolio Health & Risk Audit + Live Q&A.", "Drives high-intent booking of 1-on-1 strategy sessions with the Portfolio Manager."]
    ]
    for r_idx, row_data in enumerate(table_curr_data):
        for c_idx, val in enumerate(row_data):
            p_cell = table_curr.rows[r_idx].cells[c_idx].paragraphs[0]
            p_cell.text = val
    format_table(
        table_curr,
        col_widths=[1.5, 3.2, 2.2],
        col_alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    )

    doc.add_page_break()

    # ------------------ SECTION 5: FINANCIAL MODELING ------------------
    h5 = doc.add_heading(level=1)
    r_h5 = h5.add_run("5. Financial Modeling & Unit Economics (At ₹60,000 / Month Spend)")
    r_h5.font.name = 'Arial'
    r_h5.font.size = Pt(16)
    r_h5.bold = True
    r_h5.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("The following 3-tier financial projection models the return on a lean pilot spend of ₹60,000 / month across 90 days:")
    r.font.name = 'Arial'
    r.font.size = Pt(10)

    table_model = doc.add_table(rows=10, cols=4)
    table_model_data = [
        ["Metric", "Conservative Tier", "Expected (Target)", "Optimized Scale"],
        ["Monthly Media Spend", "₹60,000", "₹60,000", "₹60,000"],
        ["Blended Cost Per Registration (CPL)", "₹350", "₹280", "₹220"],
        ["Masterclass Registrations", "171 leads", "214 leads", "272 leads"],
        ["Live Attendance Rate (Thursday 8 PM)", "40% (68 attendees)", "45% (96 attendees)", "50% (136 attendees)"],
        ["1-on-1 Diagnostic Bookings (15%)", "10 booked audits", "14 booked audits", "20 booked audits"],
        ["Completed Audits (80% show-up)", "8 completed", "11 completed", "16 completed"],
        ["Mandate Close Rate (25%)", "2 new clients", "3 new clients", "4 new clients"],
        ["Monthly Capital / AUM Added", "₹50L – ₹1.00 Crore", "₹90L – ₹1.50 Crores", "₹1.20 – ₹2.00 Crores"],
        ["Blended CAC per Investor", "₹30,000", "₹20,000", "₹15,000"]
    ]
    for r_idx, row_data in enumerate(table_model_data):
        for c_idx, val in enumerate(row_data):
            p_cell = table_model.rows[r_idx].cells[c_idx].paragraphs[0]
            p_cell.text = val
    format_table(
        table_model,
        col_widths=[2.5, 1.5, 1.5, 1.5],
        col_alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT]
    )

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_after = Pt(8)

    # ------------------ SECTION 6: ROADMAP ------------------
    h6 = doc.add_heading(level=1)
    r_h6 = h6.add_run("6. Lean 90-Day Implementation & Milestone Roadmap")
    r_h6.font.name = 'Arial'
    r_h6.font.size = Pt(16)
    r_h6.bold = True
    r_h6.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    table_road = doc.add_table(rows=4, cols=3)
    table_road_data = [
        ["Sprint Phase", "Core Execution Activities", "Milestones & Output Assets"],
        ["Month 1: Foundation (Days 1–30)", "• Deploy Salaried LP (wealth.finaquity.com)\n• Finalize 30-Slide Deck & Teardown Templates\n• Set up Meta Pixel & Google Exact Match Campaigns\n• WhatsApp Concierge & Calendar Integration", "Live landing page, approved ad creative sets, automated show-up flow, SEBI compliance sign-off."],
        ["Month 2: Pilot Spend (Days 31–60)", "• Activate ₹2,000/day Ad Campaigns (BLR/GGN/HYD)\n• Execute 2 Bi-Weekly Live Masterclasses\n• Deliver 1-on-1 Portfolio Diagnostics\n• Onboard first 5 to 7 salaried clients", "200+ registrations, 90+ attendees, 18+ completed audits, ₹1.5Cr–₹2.5Cr in new capital added."],
        ["Month 3: Calibration & Growth (Days 61–90)", "• Reinvest client advisory fees into ad scaling\n• Activate Founder LinkedIn weekly teardowns\n• Optimize CPL down to ~₹220\n• Establish steady monthly inflow of 4-6 new investors", "Predictable client acquisition loop, automated lead nurturing, scalable AUM expansion engine."]
    ]
    for r_idx, row_data in enumerate(table_road_data):
        for c_idx, val in enumerate(row_data):
            p_cell = table_road.rows[r_idx].cells[c_idx].paragraphs[0]
            p_cell.text = val
    format_table(
        table_road,
        col_widths=[1.8, 3.2, 1.9],
        col_alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    )

    doc.add_page_break()

    # ------------------ SECTION 7: COMMERCIAL INVESTMENT ------------------
    h7 = doc.add_heading(level=1)
    r_h7 = h7.add_run("7. Lean Commercial Scope of Work & Retainer")
    r_h7.font.name = 'Arial'
    r_h7.font.size = Pt(16)
    r_h7.bold = True
    r_h7.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("To accommodate early-stage growth and maintain lean capital efficiency, Techno Exponent offers a streamlined Pilot Retainer structure:")
    r.font.name = 'Arial'
    r.font.size = Pt(10)

    table_price = doc.add_table(rows=3, cols=3)
    table_p_data = [
        ["Engagement Component", "Agency Management Fee", "Direct Media Spend (Paid to Platforms)"],
        ["Lean Performance Retainer (Full Funnel)", "₹45,000 / month\n(Covers Meta, Google Search, Landing Page, WhatsApp Automation & Reporting)", "Lean Pilot Budget:\n₹50,000 – ₹60,000 / month\n(~₹2,000 / day paid directly to platforms)"],
        ["One-Time Asset Setup & Masterclass Build", "WAIVED (Included in 90-Day Commitment)", "Zero platform fees"]
    ]
    for r_idx, row_data in enumerate(table_p_data):
        for c_idx, val in enumerate(row_data):
            p_cell = table_price.rows[r_idx].cells[c_idx].paragraphs[0]
            p_cell.text = val
    format_table(
        table_price,
        col_widths=[2.5, 2.5, 1.9],
        col_alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    )

    p_spacer2 = doc.add_paragraph()
    p_spacer2.paragraph_format.space_after = Pt(8)

    add_callout(
        doc,
        "Commercial Terms & Governance:\n• Engagement Term: Initial 90-day pilot agreement covering setup, execution, calibration, and conversion loops.\n• Complete Ad Spend Transparency: 100% of media spend is billed directly by Meta and Google to Finaquity with zero agency surcharge.\n• SEBI Regulatory Guardrails: All landing page copy, ad graphics, and presentation decks are pre-cleared for SEBI Advertising Code compliance.",
        title="COMMERCIAL TERMS",
        border_color="2361A8",
        bg_color="F0F4F8"
    )

    # ------------------ SECTION 8: SIGN-OFF ------------------
    h8 = doc.add_heading(level=1)
    r_h8 = h8.add_run("8. Authorization & Next Steps")
    r_h8.font.name = 'Arial'
    r_h8.font.size = Pt(16)
    r_h8.bold = True
    r_h8.font.color.rgb = RGBColor(0x1B, 0x36, 0x5D)

    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_after = Pt(14)
    r_sign = p_sign.add_run("To proceed with deploying Finaquity's Salaried Working Professionals acquisition engine, please confirm acceptance below:")
    r_sign.font.name = 'Arial'
    r_sign.font.size = Pt(10)

    table_sign = doc.add_table(rows=4, cols=2)
    table_sign_data = [
        ["Accepted on Behalf of Finaquity:", "Accepted on Behalf of Techno Exponent:"],
        ["Authorized Signatory: ________________________", "Authorized Signatory: ________________________"],
        ["Name & Title: Tanmay Singh Rajput, Founder", "Name & Title: Performance Practice Lead"],
        ["Date: ____ / ____ / 2026", "Date: ____ / ____ / 2026"]
    ]
    for r_idx, row_data in enumerate(table_sign_data):
        for c_idx, val in enumerate(row_data):
            p_cell = table_sign.rows[r_idx].cells[c_idx].paragraphs[0]
            p_cell.text = val
    format_table(
        table_sign,
        col_widths=[3.45, 3.45],
        col_alignments=[WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    )

    # Save files
    report_docx = os.path.abspath(r"C:\Users\test\Videos\Office\reports\Finaquity_HNWI_Marketing_Strategy_and_Proposal.docx")
    report_pdf = os.path.abspath(r"C:\Users\test\Videos\Office\reports\Finaquity_HNWI_Marketing_Strategy_and_Proposal.pdf")
    proposal_docx = os.path.abspath(r"C:\Users\test\Videos\Office\Proposals\Digital_Marketing_Proposal_Finaquity_Techno_Exponent.docx")
    proposal_pdf = os.path.abspath(r"C:\Users\test\Videos\Office\Proposals\Digital_Marketing_Proposal_Finaquity_Techno_Exponent.pdf")

    os.makedirs(os.path.dirname(report_docx), exist_ok=True)
    os.makedirs(os.path.dirname(proposal_docx), exist_ok=True)

    doc.save(report_docx)
    print(f"Saved DOCX to: {report_docx}")
    shutil.copyfile(report_docx, proposal_docx)
    print(f"Copied DOCX to: {proposal_docx}")

    # Convert to PDF via Word COM
    print("Converting DOCX to PDF via MS Word COM...")
    word = win32com.client.Dispatch('Word.Application')
    word.Visible = False
    try:
        wdoc = word.Documents.Open(report_docx)
        wdoc.SaveAs(report_pdf, FileFormat=17) # 17 = wdFormatPDF
        wdoc.Close()
        print(f"Saved PDF to: {report_pdf}")
        shutil.copyfile(report_pdf, proposal_pdf)
        print(f"Copied PDF to: {proposal_pdf}")
    finally:
        word.Quit()

if __name__ == '__main__':
    build_proposal()
