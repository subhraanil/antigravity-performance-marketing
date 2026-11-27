import os
import json
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

out_dir = r"website audit/makemealabel.com"
data_path = os.path.join(out_dir, "audit_data.json")

with open(data_path, "r", encoding="utf-8") as f:
    data = json.load(f)

doc = docx.Document()

# 1. Page Margins (0.75 in = 54 pt)
PAGE_WIDTH_INCHES = 8.27   # A4 width
PAGE_MARGIN_INCHES = 0.75
USABLE_WIDTH_INCHES = PAGE_WIDTH_INCHES - (2 * PAGE_MARGIN_INCHES) # ~6.77 in

for s in doc.sections:
    s.page_width = Inches(8.27)
    s.page_height = Inches(11.69)
    s.top_margin = Inches(0.75)
    s.bottom_margin = Inches(0.75)
    s.left_margin = Inches(0.75)
    s.right_margin = Inches(0.75)

# Styling Colors
HEX_NAVY = "0A192F"
HEX_BLUE = "2563EB"
HEX_RED = "DC2626"
HEX_RED_BG = "FEF2F2"
HEX_BLUE_BG = "EFF6FF"
HEX_GRAY_BG = "F8FAFC"
HEX_BORDER = "CBD5E1"
HEX_DARK = "0F172A"
HEX_MUTED = "64748B"

RGB_NAVY = RGBColor(10, 25, 47)
RGB_BLUE = RGBColor(37, 99, 235)
RGB_RED = RGBColor(220, 38, 38)
RGB_DARK = RGBColor(15, 23, 42)
RGB_MUTED = RGBColor(100, 116, 139)
RGB_WHITE = RGBColor(255, 255, 255)

# XML Helpers
def set_cell_background(cell, hex_color):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=140, right=140):
    # in dxa (1 pt = 20 dxa)
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_border(cell, top=HEX_BORDER, bottom=HEX_BORDER, left=HEX_BORDER, right=HEX_BORDER, sz="4"):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for side, color in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        if color:
            b = OxmlElement(f'w:{side}')
            b.set(qn('w:val'), 'single')
            b.set(qn('w:sz'), sz)
            b.set(qn('w:space'), '0')
            b.set(qn('w:color'), color)
            tcBorders.append(b)
        else:
            b = OxmlElement(f'w:{side}')
            b.set(qn('w:val'), 'none')
            tcBorders.append(b)
    tcPr.append(tcBorders)

def prevent_row_split(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement('w:cantSplit'))

def set_repeat_table_header(row):
    trPr = row._tr.get_or_add_trPr()
    trPr.append(OxmlElement('w:tblHeader'))

# Running Header & Footer
header = doc.sections[0].header
hp = header.paragraphs[0]
hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
hrun = hp.add_run("MAKE ME A LABEL UK  |  TECHNICAL SEO & E-COMMERCE AUDIT")
hrun.font.name = "Arial"
hrun.font.size = Pt(8)
hrun.font.color.rgb = RGB_MUTED

footer = doc.sections[0].footer
fp = footer.paragraphs[0]
fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
frun = fp.add_run("Make Me A Label — SEO & E-Commerce Audit Report  |  Confidential")
frun.font.name = "Arial"
frun.font.size = Pt(8)
frun.font.color.rgb = RGB_MUTED

# ----------------- TITLE & COVER HEADER -----------------
badge_p = doc.add_paragraph()
badge_p.paragraph_format.space_before = Pt(0)
badge_p.paragraph_format.space_after = Pt(2)
r_badge = badge_p.add_run(data.get("badge_text", "UK E-COMMERCE & TECHNICAL SEO AUDIT").upper())
r_badge.font.name = "Arial"
r_badge.font.size = Pt(9.5)
r_badge.font.bold = True
r_badge.font.color.rgb = RGB_BLUE

title_p = doc.add_paragraph()
title_p.paragraph_format.space_before = Pt(2)
title_p.paragraph_format.space_after = Pt(2)
r_title = title_p.add_run(data.get("report_title", "TECHNICAL SEO & E-COMMERCE AUDIT REPORT"))
r_title.font.name = "Arial"
r_title.font.size = Pt(20)
r_title.font.bold = True
r_title.font.color.rgb = RGB_NAVY

sub_p = doc.add_paragraph()
sub_p.paragraph_format.space_before = Pt(0)
sub_p.paragraph_format.space_after = Pt(12)
r_sub = sub_p.add_run(f"{data.get('client_name', 'Make Me A Label')} (makemealabel.com) — Issues & Gap Analysis")
r_sub.font.name = "Arial"
r_sub.font.size = Pt(11)
r_sub.font.color.rgb = RGB_MUTED

# ----------------- EXECUTIVE HEALTH SCORE BOX -----------------
score_box_table = doc.add_table(rows=1, cols=2)
score_box_table.alignment = WD_TABLE_ALIGNMENT.CENTER
score_box_table.autofit = False

# Widths: Left box (2.2 in), Right box (4.5 in) = 6.7 in
c_score = score_box_table.rows[0].cells[0]
c_meta = score_box_table.rows[0].cells[1]
c_score.width = Inches(2.1)
c_meta.width = Inches(4.6)

# Left cell: Health score
set_cell_background(c_score, HEX_RED_BG)
set_cell_border(c_score, top=HEX_RED, bottom=HEX_RED, left=HEX_RED, right=HEX_RED, sz="12")
set_cell_margins(c_score, top=160, bottom=160, left=160, right=160)

p_sc_val = c_score.paragraphs[0]
p_sc_val.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sc_val.paragraph_format.space_after = Pt(0)
r_val = p_sc_val.add_run(f"{data.get('health_score', 36)} / 100")
r_val.font.name = "Arial"
r_val.font.size = Pt(28)
r_val.font.bold = True
r_val.font.color.rgb = RGB_RED

p_sc_lbl = c_score.add_paragraph()
p_sc_lbl.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sc_lbl.paragraph_format.space_before = Pt(2)
p_sc_lbl.paragraph_format.space_after = Pt(0)
r_lbl = p_sc_lbl.add_run("OVERALL HEALTH SCORE\nCritical Remediation Required")
r_lbl.font.name = "Arial"
r_lbl.font.size = Pt(8)
r_lbl.font.bold = True
r_lbl.font.color.rgb = RGB_RED

# Right cell: Meta details
set_cell_background(c_meta, HEX_GRAY_BG)
set_cell_border(c_meta, top=HEX_BORDER, bottom=HEX_BORDER, left=HEX_BORDER, right=HEX_BORDER, sz="4")
set_cell_margins(c_meta, top=140, bottom=140, left=160, right=160)

meta_items = data.get("meta_items", [])
p_m = c_meta.paragraphs[0]
p_m.paragraph_format.space_after = Pt(2)
p_m.paragraph_format.line_spacing = 1.15

for idx, (lbl, val) in enumerate(meta_items[:5]):
    if idx > 0:
        p_m = c_meta.add_paragraph()
        p_m.paragraph_format.space_after = Pt(2)
        p_m.paragraph_format.line_spacing = 1.15
    r_l = p_m.add_run(f"{lbl} ")
    r_l.font.name = "Arial"
    r_l.font.size = Pt(8.5)
    r_l.font.bold = True
    r_l.font.color.rgb = RGB_DARK
    
    r_v = p_m.add_run(val)
    r_v.font.name = "Arial"
    r_v.font.size = Pt(8.5)
    r_v.font.color.rgb = RGB_DARK

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# ----------------- SECTION HELPERS -----------------
def add_heading_1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = RGB_NAVY
    return p

def add_body_p(text, bold_prefix=""):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Arial"
        r_pre.font.size = Pt(9)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGB_DARK
    run = p.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(9)
    run.font.color.rgb = RGB_DARK
    return p

# ----------------- 1. EXECUTIVE SUMMARY -----------------
add_heading_1("1. Executive Summary & Verified Tool Baseline")
for para in data.get("executive_summary", []):
    add_body_p(para.get("text", ""), para.get("bold_prefix", ""))

# ----------------- 2. WEBSITE HEALTH SCORECARD -----------------
add_heading_1(f"2. Website Technical Health Scorecard ({data.get('health_score', 36)} / 100)")

sc_table = doc.add_table(rows=1, cols=5)
sc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
sc_table.autofit = False

# Explicit column widths: total = 6.7 in
col_widths = [Inches(1.8), Inches(0.6), Inches(0.8), Inches(0.8), Inches(2.7)]

headers = ["Audit Category", "Weight", "Score", "Status", "Primary Observed Defect"]
hdr_row = sc_table.rows[0]
prevent_row_split(hdr_row)
set_repeat_table_header(hdr_row)

for idx, h in enumerate(headers):
    c = hdr_row.cells[idx]
    c.width = col_widths[idx]
    c.text = h
    set_cell_background(c, HEX_NAVY)
    set_cell_margins(c, top=140, bottom=140, left=100, right=100)
    set_cell_border(c, top=HEX_NAVY, bottom=HEX_NAVY, left=HEX_NAVY, right=HEX_NAVY)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if idx in [1, 2, 3] else WD_ALIGN_PARAGRAPH.LEFT
    r = p.runs[0]
    r.font.name = "Arial"
    r.font.size = Pt(8.5)
    r.font.bold = True
    r.font.color.rgb = RGB_WHITE

for row_idx, r_data in enumerate(data.get("scorecard", [])):
    row = sc_table.add_row()
    prevent_row_split(row)
    bg_color = HEX_GRAY_BG if row_idx % 2 == 1 else "FFFFFF"
    is_total = "TOTAL" in str(r_data[0])
    if is_total:
        bg_color = HEX_BLUE_BG
        
    for c_idx, val in enumerate(r_data):
        c = row.cells[c_idx]
        c.width = col_widths[c_idx]
        c.text = str(val)
        set_cell_background(c, bg_color)
        set_cell_margins(c, top=100, bottom=100, left=100, right=100)
        set_cell_border(c, top=HEX_BORDER, bottom=HEX_BORDER, left=HEX_BORDER, right=HEX_BORDER)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [1, 2, 3] else WD_ALIGN_PARAGRAPH.LEFT
        r = p.runs[0]
        r.font.name = "Arial"
        r.font.size = Pt(8)
        
        if c_idx == 3: # Status column
            r.font.bold = True
            if val in ["Critical", "Fail"]:
                r.font.color.rgb = RGB_RED
            elif val == "Pass":
                r.font.color.rgb = RGBColor(16, 128, 64)
            elif val == "Warning":
                r.font.color.rgb = RGBColor(200, 120, 0)
        elif is_total:
            r.font.bold = True
            if c_idx == 2:
                r.font.color.rgb = RGB_RED

doc.add_paragraph().paragraph_format.space_after = Pt(6)

# ----------------- 3. COMPREHENSIVE ISSUE CATALOG -----------------
issues = data.get("issues", [])
add_heading_1(f"3. Comprehensive Issue Catalog ({len(issues)} Verified Issues - Issues ONLY)")

# Present issues as a high-readability 3-column table with generous defect width
iss_table = doc.add_table(rows=1, cols=3)
iss_table.alignment = WD_TABLE_ALIGNMENT.CENTER
iss_table.autofit = False

# Widths: Issue & Severity (2.0 in), Affected URLs (1.6 in), Observed Defect & Impact (3.1 in) = 6.7 in
iss_col_widths = [Inches(2.0), Inches(1.6), Inches(3.1)]
iss_headers = ["Issue Title & Severity", "Affected URL(s)", "Observed Defect & Impact"]

hdr_iss = iss_table.rows[0]
prevent_row_split(hdr_iss)
set_repeat_table_header(hdr_iss)

for idx, h in enumerate(iss_headers):
    c = hdr_iss.cells[idx]
    c.width = iss_col_widths[idx]
    c.text = h
    set_cell_background(c, HEX_NAVY)
    set_cell_margins(c, top=140, bottom=140, left=100, right=100)
    set_cell_border(c, top=HEX_NAVY, bottom=HEX_NAVY, left=HEX_NAVY, right=HEX_NAVY)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.runs[0]
    r.font.name = "Arial"
    r.font.size = Pt(8.5)
    r.font.bold = True
    r.font.color.rgb = RGB_WHITE

for row_idx, iss in enumerate(issues, 1):
    row = iss_table.add_row()
    prevent_row_split(row)
    bg_color = HEX_GRAY_BG if row_idx % 2 == 1 else "FFFFFF"
    
    # Cell 0: Title & Severity Badge
    c0 = row.cells[0]
    c0.width = iss_col_widths[0]
    set_cell_background(c0, bg_color)
    set_cell_margins(c0, top=100, bottom=100, left=100, right=100)
    set_cell_border(c0, top=HEX_BORDER, bottom=HEX_BORDER, left=HEX_BORDER, right=HEX_BORDER)
    p0 = c0.paragraphs[0]
    p0.paragraph_format.space_after = Pt(2)
    p0.paragraph_format.line_spacing = 1.15
    r0_num = p0.add_run(f"{row_idx}. {iss.get('title', '')}\n")
    r0_num.font.name = "Arial"
    r0_num.font.size = Pt(8)
    r0_num.font.bold = True
    r0_num.font.color.rgb = RGB_DARK
    
    sev = iss.get("severity", "Medium")
    r0_sev = p0.add_run(f"[{sev.upper()}]")
    r0_sev.font.name = "Arial"
    r0_sev.font.size = Pt(7.5)
    r0_sev.font.bold = True
    r0_sev.font.color.rgb = RGB_RED if sev == "Critical" else (RGBColor(200, 100, 0) if sev == "High" else RGBColor(100, 116, 139))
    
    # Cell 1: Affected URLs
    c1 = row.cells[1]
    c1.width = iss_col_widths[1]
    set_cell_background(c1, bg_color)
    set_cell_margins(c1, top=100, bottom=100, left=100, right=100)
    set_cell_border(c1, top=HEX_BORDER, bottom=HEX_BORDER, left=HEX_BORDER, right=HEX_BORDER)
    p1 = c1.paragraphs[0]
    p1.paragraph_format.space_after = Pt(0)
    p1.paragraph_format.line_spacing = 1.15
    r1 = p1.add_run(iss.get("urls", ""))
    r1.font.name = "Arial"
    r1.font.size = Pt(7.5)
    r1.font.color.rgb = RGB_MUTED
    
    # Cell 2: Observed Defect & Impact
    c2 = row.cells[2]
    c2.width = iss_col_widths[2]
    set_cell_background(c2, bg_color)
    set_cell_margins(c2, top=100, bottom=100, left=100, right=100)
    set_cell_border(c2, top=HEX_BORDER, bottom=HEX_BORDER, left=HEX_BORDER, right=HEX_BORDER)
    p2 = c2.paragraphs[0]
    p2.paragraph_format.space_after = Pt(0)
    p2.paragraph_format.line_spacing = 1.15
    r2 = p2.add_run(iss.get("impact", ""))
    r2.font.name = "Arial"
    r2.font.size = Pt(8)
    r2.font.color.rgb = RGB_DARK

doc.add_paragraph().paragraph_format.space_after = Pt(8)

# ----------------- 4. SCOPE OF IMPROVEMENT -----------------
add_heading_1("4. Scope of Improvement")
for sc in data.get("scope_of_improvement", []):
    add_body_p(sc.get("text", ""), sc.get("bold_prefix", ""))

# ----------------- 5. IMMEDIATE FIXATION NEEDED -----------------
add_heading_1(f"5. Immediate Fixation Needed (Emergency Priority - {len(data.get('immediate_fixations', []))} Items)")
for idx, fix in enumerate(data.get("immediate_fixations", []), 1):
    add_body_p(fix, f"{idx}. ")

# ----------------- 6. STRATEGIC ROADMAP -----------------
add_heading_1("6. What Will Be the Next Step (Strategic 4-Phase Roadmap)")

rm_table = doc.add_table(rows=1, cols=3)
rm_table.alignment = WD_TABLE_ALIGNMENT.CENTER
rm_table.autofit = False

# Widths: Phase (1.6 in), Objectives (3.3 in), Milestone (1.8 in) = 6.7 in
rm_col_widths = [Inches(1.6), Inches(3.3), Inches(1.8)]
rm_headers = ["Phase", "Key Objectives & Focus Areas", "Target Milestone"]

hdr_rm = rm_table.rows[0]
prevent_row_split(hdr_rm)
set_repeat_table_header(hdr_rm)

for idx, h in enumerate(rm_headers):
    c = hdr_rm.cells[idx]
    c.width = rm_col_widths[idx]
    c.text = h
    set_cell_background(c, HEX_NAVY)
    set_cell_margins(c, top=140, bottom=140, left=100, right=100)
    set_cell_border(c, top=HEX_NAVY, bottom=HEX_NAVY, left=HEX_NAVY, right=HEX_NAVY)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p.runs[0]
    r.font.name = "Arial"
    r.font.size = Pt(8.5)
    r.font.bold = True
    r.font.color.rgb = RGB_WHITE

for row_idx, rm in enumerate(data.get("roadmap", [])):
    row = rm_table.add_row()
    prevent_row_split(row)
    bg_color = HEX_GRAY_BG if row_idx % 2 == 1 else "FFFFFF"
    
    # Col 0: Phase
    c0 = row.cells[0]
    c0.width = rm_col_widths[0]
    set_cell_background(c0, bg_color)
    set_cell_margins(c0, top=100, bottom=100, left=100, right=100)
    set_cell_border(c0, top=HEX_BORDER, bottom=HEX_BORDER, left=HEX_BORDER, right=HEX_BORDER)
    p0 = c0.paragraphs[0]
    p0.paragraph_format.line_spacing = 1.15
    r0 = p0.add_run(rm.get("phase", ""))
    r0.font.name = "Arial"
    r0.font.size = Pt(8)
    r0.font.bold = True
    r0.font.color.rgb = RGB_DARK
    
    # Col 1: Objectives
    c1 = row.cells[1]
    c1.width = rm_col_widths[1]
    set_cell_background(c1, bg_color)
    set_cell_margins(c1, top=100, bottom=100, left=100, right=100)
    set_cell_border(c1, top=HEX_BORDER, bottom=HEX_BORDER, left=HEX_BORDER, right=HEX_BORDER)
    p1 = c1.paragraphs[0]
    p1.paragraph_format.line_spacing = 1.15
    r1 = p1.add_run(rm.get("objectives", ""))
    r1.font.name = "Arial"
    r1.font.size = Pt(8)
    r1.font.color.rgb = RGB_DARK
    
    # Col 2: Milestone
    c2 = row.cells[2]
    c2.width = rm_col_widths[2]
    set_cell_background(c2, bg_color)
    set_cell_margins(c2, top=100, bottom=100, left=100, right=100)
    set_cell_border(c2, top=HEX_BORDER, bottom=HEX_BORDER, left=HEX_BORDER, right=HEX_BORDER)
    p2 = c2.paragraphs[0]
    p2.paragraph_format.line_spacing = 1.15
    r2 = p2.add_run(rm.get("milestone", ""))
    r2.font.name = "Arial"
    r2.font.size = Pt(8)
    r2.font.bold = True
    r2.font.color.rgb = RGB_BLUE

target_docx = os.path.join(out_dir, "MakeMeALabel_SEO_Audit_Report.docx")
doc.save(target_docx)
doc.save("MakeMeALabel_SEO_Audit_Report.docx")
print(f"[+] Professionally styled DOCX successfully generated: {target_docx}")
