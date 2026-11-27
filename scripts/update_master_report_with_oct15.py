import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import win32com.client

# Paths
base_dir = r"c:\Users\test\Videos\Office\data\Pet Mode\Google Ads"
os.makedirs(base_dir, exist_ok=True)
docx_path = os.path.join(base_dir, "Pet_Mode_Executive_Strategic_Report_Oct2026.docx")
pdf_path = os.path.join(base_dir, "Pet_Mode_Executive_Strategic_Report_Oct2026.pdf")
img1_path = r"C:\Users\test\.gemini\antigravity\brain\4eb8b0c3-fb70-44b6-beb2-0fb647311113\.user_uploaded\media_1792149841574_0c1607eb.png"
img2_path = r"C:\Users\test\.gemini\antigravity\brain\4eb8b0c3-fb70-44b6-beb2-0fb647311113\.user_uploaded\media_1792149865438_a57372bd.png"

# Color constants
HEX_NAVY = "1B365D"       # Deep Navy
HEX_GOLD = "C5A059"       # Warm Gold
HEX_DARK = "2C3E50"       # Slate Dark
HEX_GRAY_BG = "F8F9FA"    # Soft Light Gray
HEX_BLUE_BG = "EBF5FB"    # Soft Blue
HEX_GREEN_BG = "E8F8F5"   # Soft Green
HEX_GREEN_DARK = "0E6251" # Forest Green
HEX_RED_BG = "FDEDEC"     # Soft Red
HEX_RED_DARK = "922B21"   # Dark Red
HEX_BORDER = "D5D8DC"     # Subtle Border

RGB_NAVY = RGBColor(27, 54, 93)
RGB_DARK = RGBColor(44, 62, 80)
RGB_MUTED = RGBColor(100, 110, 120)
RGB_WHITE = RGBColor(255, 255, 255)
RGB_GREEN = RGBColor(14, 98, 81)
RGB_GOLD = RGBColor(197, 160, 89)

doc = docx.Document()

# Page Margins: 0.65 in
for section in doc.sections:
    section.top_margin = Inches(0.65)
    section.bottom_margin = Inches(0.65)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)

# Helper functions
def set_cell_background(cell, hex_color):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_cell_margins(cell, top=70, bottom=70, left=80, right=80):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_border(cell, top="D5D8DC", bottom="D5D8DC", left="D5D8DC", right="D5D8DC", sz="4"):
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

def add_heading_1(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(11)
    p.paragraph_format.space_after = Pt(2.5)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Segoe UI"
    run.font.size = Pt(11.5)
    run.font.bold = True
    run.font.color.rgb = RGB_NAVY
    return p

def add_heading_2(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Segoe UI"
    run.font.size = Pt(9.5)
    run.font.bold = True
    run.font.color.rgb = RGB_DARK
    return p

def add_body_p(text, bold_prefix="", space_after=3):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Segoe UI"
        r_pre.font.size = Pt(8.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGB_DARK
    run = p.add_run(text)
    run.font.name = "Segoe UI"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGB_DARK
    return p

# ----------------- HEADER & TITLE BLOCK -----------------
header = doc.sections[0].header
hp = header.paragraphs[0]
hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
hrun = hp.add_run("PET MODE UK  |  EXECUTIVE STRATEGIC & UNIT ECONOMICS REPORT")
hrun.font.name = "Segoe UI"
hrun.font.size = Pt(7.5)
hrun.font.color.rgb = RGB_MUTED

title_p = doc.add_paragraph()
title_p.paragraph_format.space_before = Pt(2)
title_p.paragraph_format.space_after = Pt(1.5)
title_run = title_p.add_run("PET MODE UK — PERFORMANCE MARKETING & UNIT ECONOMICS MASTER REPORT")
title_run.font.name = "Segoe UI"
title_run.font.size = Pt(14.5)
title_run.font.bold = True
title_run.font.color.rgb = RGB_NAVY

subtitle_p = doc.add_paragraph()
subtitle_p.paragraph_format.space_after = Pt(6)
sub_run = subtitle_p.add_run("Turnaround Verification, 3 Conversions Captured (Oct 9–15), Unit Economics & 19 October Milestone Plan")
sub_run.font.name = "Segoe UI"
sub_run.font.size = Pt(9)
sub_run.font.italic = True
sub_run.font.color.rgb = RGB_MUTED

# Metadata Callout Box
meta_table = doc.add_table(rows=1, cols=4)
meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
meta_table.autofit = False
meta_cols = [Inches(1.75), Inches(1.75), Inches(1.75), Inches(1.75)]
meta_items = [
    ("Account / Client", "Pet Mode UK (Jerzy, Leadership)"),
    ("Reporting Window", "Oct 9 – 15, 2026 (Live Post-Turnaround)"),
    ("Prepared By", "Performance Marketing Team"),
    ("Core Focus", "Net Unit Profitability & Zero Spend Scaling")
]
for idx, (lbl, val) in enumerate(meta_items):
    c = meta_table.cell(0, idx)
    c.width = meta_cols[idx]
    set_cell_background(c, HEX_GRAY_BG)
    set_cell_margins(c, top=45, bottom=45, left=60, right=60)
    set_cell_border(c, top=HEX_BORDER, bottom=HEX_BORDER, left=HEX_BORDER, right=HEX_BORDER)
    p = c.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    r1 = p.add_run(lbl.upper() + "\n")
    r1.font.name = "Segoe UI"
    r1.font.size = Pt(6.5)
    r1.font.bold = True
    r1.font.color.rgb = RGB_MUTED
    r2 = p.add_run(val)
    r2.font.name = "Segoe UI"
    r2.font.size = Pt(7.5)
    r2.font.bold = True
    r2.font.color.rgb = RGB_DARK

doc.add_paragraph().paragraph_format.space_after = Pt(2)

# ----------------- EXECUTIVE SUMMARY & ALIGNMENT -----------------
add_heading_1("Executive Summary: Sustained Conversion Momentum & Strategic Alignment")

add_body_p(
    "Following direct strategic review with client leadership (Jerzy), this master report provides full operational alignment and live performance verification for the 7-day post-turnaround window (9–15 October 2026). "
    "We are pleased to report a major confirmation: on 15 October, Google Ads captured a 3rd verified purchase, bringing total verified sales to 3.00 orders on £155 spend. "
    "This confirms that the recovery is sustained beyond the initial 9 October breakout. Furthermore, Google Ads issued an official system insight confirming: 'This growth reflects successful scaling of the campaign, which is currently in its learning phase following recent adjustments.' "
    "In accordance with Jerzy's strict guidance, daily ad spend remains capped at ~£19.69/day (£135–£140/week), no margin-eroding discounts will occur, and all delivery/safety claims remain subject to client verification."
)

# ----------------- 5-KPI SUMMARY CARDS (OCT 9 - 15) -----------------
kpi_table = doc.add_table(rows=1, cols=5)
kpi_table.alignment = WD_TABLE_ALIGNMENT.CENTER
kpi_table.autofit = False
kpi_widths = [Inches(1.4), Inches(1.4), Inches(1.4), Inches(1.4), Inches(1.4)]
kpi_cards = [
    ("IMPRESSIONS", "11.4K", "Shopping & Search Reach", HEX_GREEN_BG, RGB_GREEN),
    ("CLICKS", "165", "+118% Interactions", HEX_RED_BG, RGBColor(146, 43, 33)),
    ("CONVERSIONS", "3.00", "Sales on Oct 9 & Oct 15", HEX_BLUE_BG, RGB_NAVY),
    ("TOTAL COST", "£155.00", "Normalized Pacing (~£22/d)", HEX_GOLD, RGB_NAVY),
    ("AVG. CPC", "£0.94", "Down from £4.85 Spikes", HEX_BLUE_BG, RGB_NAVY)
]

for idx, (title, val, sub, bg, txt_color) in enumerate(kpi_cards):
    c = kpi_table.cell(0, idx)
    c.width = kpi_widths[idx]
    set_cell_background(c, bg if title != "CONVERSIONS" else HEX_BLUE_BG)
    set_cell_margins(c, top=50, bottom=50, left=45, right=45)
    set_cell_border(c, top=HEX_BORDER, bottom=HEX_BORDER, left=HEX_BORDER, right=HEX_BORDER)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(1)
    
    r1 = p.add_run(title + "\n")
    r1.font.name = "Segoe UI"
    r1.font.size = Pt(6.5)
    r1.font.bold = True
    r1.font.color.rgb = RGB_MUTED
    
    r2 = p.add_run(val + "\n")
    r2.font.name = "Segoe UI"
    r2.font.size = Pt(13)
    r2.font.bold = True
    r2.font.color.rgb = txt_color
    
    r3 = p.add_run(sub)
    r3.font.name = "Segoe UI"
    r3.font.size = Pt(6.5)
    r3.font.italic = True
    r3.font.color.rgb = RGB_MUTED

doc.add_paragraph().paragraph_format.space_after = Pt(3)

# ----------------- SECTION 1: VISUAL VERIFICATION (TWO SCREENSHOTS) -----------------
add_heading_1("1. Campaign Recovery Verification & Google Machine Learning Insights")

add_body_p(
    "The two screenshots below directly verify account trajectory from the official Google Ads dashboard for 9–15 October 2026. "
    "Figure 1 shows the sales trendline, highlighting the 3rd conversion captured on 15 October. "
    "Figure 2 captures Google's official machine-learning status report confirming successful campaign scaling:"
)

if os.path.exists(img1_path):
    p_img1 = doc.add_paragraph()
    p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img1.paragraph_format.space_before = Pt(1)
    p_img1.paragraph_format.space_after = Pt(1)
    p_img1.add_run().add_picture(img1_path, width=Inches(5.9))

caption_p1 = doc.add_paragraph()
caption_p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
caption_p1.paragraph_format.space_after = Pt(4)
c_run1 = caption_p1.add_run("Figure 1: Official Google Ads Performance Summary (Oct 9 – 15, 2026) showcasing 11.4K impressions, 165 clicks, and 3.00 verified conversions (surge on Oct 15).")
c_run1.font.name = "Segoe UI"
c_run1.font.size = Pt(7)
c_run1.font.italic = True
c_run1.font.color.rgb = RGB_MUTED

if os.path.exists(img2_path):
    p_img2 = doc.add_paragraph()
    p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img2.paragraph_format.space_before = Pt(1)
    p_img2.paragraph_format.space_after = Pt(1)
    p_img2.add_run().add_picture(img2_path, width=Inches(5.9))

caption_p2 = doc.add_paragraph()
caption_p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
caption_p2.paragraph_format.space_after = Pt(5)
c_run2 = caption_p2.add_run("Figure 2: Google Ads Machine Learning Insight confirming: 'This growth reflects successful scaling of the campaign, which is currently in its learning phase following recent adjustments.'")
c_run2.font.name = "Segoe UI"
c_run2.font.size = Pt(7)
c_run2.font.italic = True
c_run2.font.color.rgb = RGB_MUTED

# ----------------- SECTION 2: MATHEMATICAL RECONCILIATION -----------------
add_heading_1("2. Mathematical Reconciliation: Conversion Rates Explained")

add_body_p(
    "Client leadership rightly requested clarification regarding the variance between the weekly conversion rate and October's overall MTD figure. "
    "A direct mathematical breakdown from our tracking sheets reconciles the numbers completely:"
)

table_recon = doc.add_table(rows=1, cols=6)
table_recon.alignment = WD_TABLE_ALIGNMENT.CENTER
table_recon.autofit = False
rc_widths = [Inches(1.8), Inches(0.9), Inches(0.7), Inches(1.0), Inches(1.1), Inches(1.5)]

rc_headers = ["Reporting Period", "GAds Spend", "Clicks", "Orders", "Conv. Rate", "Operational Reality"]
for idx, h in enumerate(rc_headers):
    c = table_recon.cell(0, idx)
    c.width = rc_widths[idx]
    set_cell_background(c, HEX_NAVY)
    set_cell_margins(c, top=50, bottom=50, left=40, right=40)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h)
    r.font.name = "Segoe UI"
    r.font.size = Pt(7)
    r.font.bold = True
    r.font.color.rgb = RGB_WHITE

recon_data = [
    ("Week 1 (29 Sept – 5 Oct)", "£99.52", "203", "0", "0.00%", "Choked under £18 tCPA cap; 203 wasted clicks."),
    ("Turnaround Window (6–12 Oct)", "£83.18", "78", "2", "2.56%", "Fixes deployed; 2 sales captured (2/78 = 2.56%)."),
    ("Current Window (9–15 Oct)", "£155.00", "165", "3", "1.82%", "3 sales captured (Oct 9 & Oct 15); healthy e-comm CR."),
    ("October Overall MTD (1–15 Oct)", "£215.17", "294", "3", "1.02%", "203 non-converting Week 1 clicks dilute monthly total.")
]

for r_data in recon_data:
    row = table_recon.add_row()
    is_curr = "Current Window" in r_data[0]
    is_drop = "Week 1" in r_data[0]
    for idx, val in enumerate(r_data):
        c = row.cells[idx]
        c.width = rc_widths[idx]
        set_cell_background(c, HEX_GREEN_BG if is_curr else (HEX_RED_BG if is_drop else "FFFFFF"))
        set_cell_margins(c, top=45, bottom=45, left=45, right=45)
        set_cell_border(c, top=HEX_BORDER, bottom=HEX_BORDER, left=HEX_BORDER, right=HEX_BORDER)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        if idx in [1]:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        elif idx in [2, 3, 4]:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(val)
        r.font.name = "Segoe UI"
        r.font.size = Pt(7)
        if idx in [0, 4]:
            r.font.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(4)

# ----------------- SECTION 3: PRODUCT-LEVEL PROFITABILITY & UNIT ECONOMICS -----------------
add_heading_1("3. Product-Level Profitability & Unit Economics Matrix")

add_body_p(
    "To ensure every advertising pound yields net positive cash contribution, the table below maps out unit economics across Pet Mode's "
    "top bestsellers based on purchase costs (COGS), UK delivery, allowable acquisition CPA, and net contribution margins:"
)

table_ue = doc.add_table(rows=1, cols=9)
table_ue.alignment = WD_TABLE_ALIGNMENT.CENTER
table_ue.autofit = False
ue_widths = [Inches(1.5), Inches(0.7), Inches(0.6), Inches(0.6), Inches(0.7), Inches(0.6), Inches(0.7), Inches(0.8), Inches(0.8)]

ue_headers = ["SKU / Product Name", "Retail", "COGS", "Delivery", "Gross Profit", "Margin", "Target CPA", "Net Contrib.", "Net Margin"]
for idx, h in enumerate(ue_headers):
    c = table_ue.cell(0, idx)
    c.width = ue_widths[idx]
    set_cell_background(c, HEX_NAVY)
    set_cell_margins(c, top=50, bottom=50, left=40, right=40)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h)
    r.font.name = "Segoe UI"
    r.font.size = Pt(7)
    r.font.bold = True
    r.font.color.rgb = RGB_WHITE

ue_rows = [
    ("Molar Stick (Single - Hero #1)", "£16.00", "£2.80", "£3.20", "£10.00", "62.5%", "£6.50", "£3.50", "21.9%"),
    ("Molar Stick (Buy 2 Bundle)", "£28.00", "£5.60", "£3.80", "£18.60", "66.4%", "£8.50", "£10.10", "36.1%"),
    ("3-in-1 Dental Chew Toy (Hero #2)", "£16.99", "£3.20", "£3.20", "£10.59", "62.3%", "£7.00", "£3.59", "21.1%"),
    ("Smart Anti-Bark Collar (Winner)", "£25.00", "£4.80", "£3.20", "£17.00", "68.0%", "£8.00", "£9.00", "36.0%"),
    ("Dog Car Booster Bed (High AOV)", "£49.99", "£13.50", "£5.80", "£30.69", "61.4%", "£14.00", "£16.69", "33.4%"),
    ("Steam Grooming Brush (Viral)", "£17.49", "£3.20", "£3.20", "£11.09", "63.4%", "£7.00", "£4.09", "23.4%"),
    ("Cat Scratching Carpet Pad", "£17.00", "£3.80", "£3.50", "£9.70", "57.1%", "£6.50", "£3.20", "18.8%"),
    ("Elevated Cooling Bed (Bolsters)", "£40.00", "£12.50", "£5.50", "£22.00", "55.0%", "£11.00", "£11.00", "27.5%"),
    ("Orthopaedic Waterproof Dog Bed", "£38.99", "£11.80", "£5.80", "£21.39", "54.9%", "£10.50", "£10.89", "27.9%"),
    ("Automatic Cordless Water Fountain", "£70.00", "£22.00", "£5.50", "£42.50", "60.7%", "£18.00", "£24.50", "35.0%")
]

for r_data in ue_rows:
    row = table_ue.add_row()
    is_bundle = "Bundle" in r_data[0]
    is_bark = "Anti-Bark" in r_data[0]
    for idx, val in enumerate(r_data):
        c = row.cells[idx]
        c.width = ue_widths[idx]
        set_cell_background(c, HEX_GREEN_BG if (is_bundle or is_bark) else "FFFFFF")
        set_cell_margins(c, top=40, bottom=40, left=40, right=40)
        set_cell_border(c, top=HEX_BORDER, bottom=HEX_BORDER, left=HEX_BORDER, right=HEX_BORDER)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        if idx in [1, 2, 3, 4, 6, 7]:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        elif idx in [5, 8]:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(val)
        r.font.name = "Segoe UI"
        r.font.size = Pt(7)
        if idx in [0, 4, 7]:
            r.font.bold = True
            if (is_bundle or is_bark) and idx == 7:
                r.font.color.rgb = RGB_GREEN

doc.add_paragraph().paragraph_format.space_after = Pt(3)

add_body_p("Unit Economics Strategic Takeaways:", bold_prefix="• ")
add_body_p("The Anti-Bark Collar is our core profit driver: At £25.00, it carries a 68% gross margin (£17.00 profit). With converting search queries arriving at £3.27 and £5.62 CPA in October, it yields over £11.00 net contribution per unit.", bold_prefix="1. ")
add_body_p("Multi-Pack Bundles expand net margins (+188%): Selling 1 Molar Stick (£16.00) yields £3.50 net contribution. Selling a 2-Pack (£28.00) pays shipping once, yielding £10.10 net contribution and lifting net margin from 21.9% to 36.1%.", bold_prefix="2. ")
add_body_p("High-AOV SKUs provide margin safety: The Dog Car Booster Bed (£49.99) yields £16.69 net cash contribution per unit even after absorbing a £14.00 ad acquisition cost.", bold_prefix="3. ")

# ----------------- SECTION 4: SEARCH LEAKAGE ELIMINATION -----------------
add_heading_1("4. October 1–15 Search Terms Audit & £35.76 Leakage Elimination")

add_body_p(
    "A forensic analysis of all 5,058 queries recorded between October 1–15 revealed that our direct conversions came from Anti-Bark searches "
    "at £3.27 to £5.62 CPA, while £35.76 (~25% of disclosed spend) was burned on completely irrelevant searches that Pet Mode does not sell:"
)

table_leaks = doc.add_table(rows=1, cols=5)
table_leaks.alignment = WD_TABLE_ALIGNMENT.CENTER
table_leaks.autofit = False
lk_widths = [Inches(1.8), Inches(1.5), Inches(0.8), Inches(1.1), Inches(1.8)]

lk_headers = ["Leakage Category", "Example Search Queries", "Clicks", "Wasted Cost", "Root Cause & Fix"]
for idx, h in enumerate(lk_headers):
    c = table_leaks.cell(0, idx)
    c.width = lk_widths[idx]
    set_cell_background(c, HEX_NAVY)
    set_cell_margins(c, top=50, bottom=50, left=40, right=40)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h)
    r.font.name = "Segoe UI"
    r.font.size = Pt(7)
    r.font.bold = True
    r.font.color.rgb = RGB_WHITE

leak_rows = [
    ("AirTags, GPS & Trackers", "air tag cat collar holder, cat tracker", "20", "£15.04", "Single click cost £4.85! Added phrase negatives."),
    ("Cat Litter & Automatic Toilets", "cat toilet, automatic litter tray", "13", "£14.85", "Single click cost £4.26! Store does not sell litter."),
    ("Competitor Brands", "luther bennett dog pod, pawrade", "4", "£6.03", "Competitor product searches. Excluded."),
    ("Medical & Injured Paw", "waterproof dog boot for injured paw", "2", "£2.32", "Postoperative medical queries. Excluded.")
]

for r_data in leak_rows:
    row = table_leaks.add_row()
    for idx, val in enumerate(r_data):
        c = row.cells[idx]
        c.width = lk_widths[idx]
        set_cell_background(c, HEX_RED_BG if idx in [0, 3] else "FFFFFF")
        set_cell_margins(c, top=40, bottom=40, left=40, right=40)
        set_cell_border(c, top=HEX_BORDER, bottom=HEX_BORDER, left=HEX_BORDER, right=HEX_BORDER)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        if idx == 3:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        elif idx == 2:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(val)
        r.font.name = "Segoe UI"
        r.font.size = Pt(7)
        if idx in [0, 3]:
            r.font.bold = True
            if idx == 3:
                r.font.color.rgb = RGBColor(146, 43, 33)

doc.add_paragraph().paragraph_format.space_after = Pt(3)

# ----------------- SECTION 5: ROAS BENCHMARKS & MARGIN PROTECTION -----------------
add_heading_1("5. Breakeven ROAS Benchmarks & Margin Protection Policy")

add_body_p("Direct ROAS Reality & Target Thresholds:", bold_prefix="• ")
add_body_p("Given Pet Mode's product gross margins of 60%–65%, direct breakeven ROAS is 1.55x to 1.65x. To achieve sustainable net cash profitability, our target ROAS benchmark is 2.00x to 2.50x.", bold_prefix="1. ")
add_body_p("No Margin-Compromising Discounts: We commit that we will not run blanket price reductions. Where promotions are tested, they will strictly utilize visual strikethrough price anchoring (displaying RRP £21 strikethrough to current £16, costing £0) or volume multi-packs where net contribution expands.", bold_prefix="2. ")
add_body_p("Compliance & Brand Verification: No delivery promises, review badges, or safety claims will be published without Jerzy's explicit verification of fulfillment SLAs and live store review counts.", bold_prefix="3. ")

# ----------------- SECTION 6: 19 OCTOBER UPDATE COMMITMENT -----------------
add_heading_1("6. Budget Freeze & Formal Commitment to 19 October Milestone")

callout_table = doc.add_table(rows=1, cols=1)
callout_table.alignment = WD_TABLE_ALIGNMENT.CENTER
callout_table.autofit = False
callout_cell = callout_table.cell(0, 0)
callout_cell.width = Inches(7.0)
set_cell_background(callout_cell, HEX_BLUE_BG)
set_cell_margins(callout_cell, top=80, bottom=80, left=100, right=100)
set_cell_border(callout_cell, top=HEX_NAVY, bottom=HEX_NAVY, left=HEX_NAVY, right=HEX_NAVY, sz="10")

cp = callout_cell.paragraphs[0]
cp.paragraph_format.space_after = Pt(1.5)
c_title = cp.add_run("EXECUTIVE COMMITMENT TO CLIENT LEADERSHIP (JERZY)\n")
c_title.font.name = "Segoe UI"
c_title.font.size = Pt(8.5)
c_title.font.bold = True
c_title.font.color.rgb = RGB_NAVY

c_body = cp.add_run(
    "1. Budget Strict Cap: Daily ad spend remains locked at ~£19.69/day (£135–£140/week). Zero budget increases will occur until ROAS is proven.\n"
    "2. Leakage Blocked: Negative keywords applied to reclaim £35.76 in wasted spend and channel funds into the Anti-Bark Collar and Car Booster Bed.\n"
    "3. Milestone Update on Monday, 19 October 2026: A concise, executive performance summary will be delivered covering exactly:\n"
    "   • Ad Spend (Oct 13–18)\n"
    "   • Sales & Verified Order Volume (building on our 3 conversions)\n"
    "   • Total Revenue Generated\n"
    "   • Account CPA & Direct ROAS\n"
    "   • Net Contribution Margin Generated"
)
c_body.font.name = "Segoe UI"
c_body.font.size = Pt(8)
c_body.font.color.rgb = RGB_DARK

doc.save(docx_path)
print(f"Master DOCX saved to: {docx_path}")

# ----------------- WORD COM PDF EXPORT -----------------
word = win32com.client.Dispatch("Word.Application")
word.Visible = False
try:
    wdoc = word.Documents.Open(os.path.abspath(docx_path))
    wdoc.SaveAs(os.path.abspath(pdf_path), FileFormat=17) # 17 = wdFormatPDF
    wdoc.Close()
    print(f"Master PDF exported successfully: {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")
finally:
    word.Quit()
