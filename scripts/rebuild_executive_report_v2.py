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

doc = docx.Document()

# Margins: 0.65 in
for section in doc.sections:
    section.top_margin = Inches(0.65)
    section.bottom_margin = Inches(0.65)
    section.left_margin = Inches(0.7)
    section.right_margin = Inches(0.7)

def set_cell_background(cell, hex_color):
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shd)

def set_cell_margins(cell, top=65, bottom=65, left=75, right=75):
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
hrun = hp.add_run("PET MODE UK  |  EXECUTIVE PERFORMANCE & UNIT ECONOMICS REPORT")
hrun.font.name = "Segoe UI"
hrun.font.size = Pt(7.5)
hrun.font.color.rgb = RGB_MUTED

title_p = doc.add_paragraph()
title_p.paragraph_format.space_before = Pt(2)
title_p.paragraph_format.space_after = Pt(1.5)
title_run = title_p.add_run("PET MODE UK — PERFORMANCE MARKETING & UNIT ECONOMICS REPORT")
title_run.font.name = "Segoe UI"
title_run.font.size = Pt(14)
title_run.font.bold = True
title_run.font.color.rgb = RGB_NAVY

subtitle_p = doc.add_paragraph()
subtitle_p.paragraph_format.space_after = Pt(6)
sub_run = subtitle_p.add_run("Audit of October 1–16 Data, Unit Economics, Conversion Math Reconciliation & 19 October Milestone Plan")
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
    ("Reporting Window", "October 1 – 16, 2026 (Live Synced Data)"),
    ("Prepared By", "Performance Marketing Team"),
    ("Strategic Focus", "Profitability, Unit Margins & Pacing")
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
add_heading_1("Executive Summary: Commercial Discipline & Account Trajectory")

add_body_p(
    "This report provides complete operational transparency following strategic review with Jerzy. "
    "We are in full agreement on the core commercial principles: top-line traffic is secondary to net contribution, three orders represent a preliminary operational baseline rather than evidence of sustained recovery, and advertising spend must remain capped at the existing budget (~£19.69/day). "
    "Across October 1–16, Google Ads recorded £234.07 in spend, 319 clicks, and 3 verified orders (£149.99 revenue, £78.02 CPA, 0.64x ROAS). While the monthly aggregate remains below the 1.64x breakeven threshold due to the pre-fix zero-conversion freeze in early October, the post-fix weekly trajectory demonstrates clear acceleration toward breakeven: "
    "0.00x ROAS (29 Sep–5 Oct) -> 0.91x ROAS (6–12 Oct) -> 1.51x ROAS (13–16 Oct). "
    "To achieve sustained profitability without increasing budget, our primary focus is eliminating £38.24 in identified search query leakage and channelling budget strictly into high-margin products like the Anti-Bark Collar and Car Booster Bed."
)

# ----------------- 5-KPI SUMMARY CARDS -----------------
kpi_table = doc.add_table(rows=1, cols=5)
kpi_table.alignment = WD_TABLE_ALIGNMENT.CENTER
kpi_table.autofit = False
kpi_widths = [Inches(1.4), Inches(1.4), Inches(1.4), Inches(1.4), Inches(1.4)]
kpi_cards = [
    ("GOOGLE SPEND (OCT 1-16)", "£234.07", "319 Clicks | Avg CPC £0.73", HEX_BLUE_BG, RGB_NAVY),
    ("VERIFIED ORDERS", "3.00", "Oct 9 (2) & Oct 15 (1)", HEX_GREEN_BG, RGB_GREEN),
    ("ROAS PROGRESSION", "0.00x -> 1.51x", "Latest Block (13-16 Oct): 1.51x", HEX_GREEN_BG, RGB_GREEN),
    ("LATEST CPA (OCT 13-16)", "£52.86", "Down from £78.02 MTD Avg", HEX_RED_BG, RGBColor(146, 43, 33)),
    ("STOREFRONT TOTAL", "14 Orders", "£405 Rev | 0.79x Blended ROAS", HEX_BLUE_BG, RGB_NAVY)
]

for idx, (title, val, sub, bg, txt_color) in enumerate(kpi_cards):
    c = kpi_table.cell(0, idx)
    c.width = kpi_widths[idx]
    set_cell_background(c, bg)
    set_cell_margins(c, top=45, bottom=45, left=40, right=40)
    set_cell_border(c, top=HEX_BORDER, bottom=HEX_BORDER, left=HEX_BORDER, right=HEX_BORDER)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after = Pt(1)
    
    r1 = p.add_run(title + "\n")
    r1.font.name = "Segoe UI"
    r1.font.size = Pt(6)
    r1.font.bold = True
    r1.font.color.rgb = RGB_MUTED
    
    r2 = p.add_run(val + "\n")
    r2.font.name = "Segoe UI"
    r2.font.size = Pt(11)
    r2.font.bold = True
    r2.font.color.rgb = txt_color
    
    r3 = p.add_run(sub)
    r3.font.name = "Segoe UI"
    r3.font.size = Pt(5.5)
    r3.font.italic = True
    r3.font.color.rgb = RGB_MUTED

doc.add_paragraph().paragraph_format.space_after = Pt(2)

# ----------------- SECTION 1: VISUAL VERIFICATION (TWO SCREENSHOTS) -----------------
add_heading_1("1. Live Account Performance Verification (Dashboard Evidence)")

add_body_p(
    "The two screenshots below provide verification directly from the Google Ads dashboard during the post-fix period. "
    "Figure 1 displays the 7-day overview showing 11.4K impressions, 165 clicks, and 3 conversions (2 on Oct 9, 1 on Oct 15). "
    "Figure 2 shows Google's automated pacing notice comparing this window to the previous stagnant week:"
)

if os.path.exists(img1_path):
    p_img1 = doc.add_paragraph()
    p_img1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img1.paragraph_format.space_before = Pt(1)
    p_img1.paragraph_format.space_after = Pt(1)
    p_img1.add_run().add_picture(img1_path, width=Inches(5.7))

caption_p1 = doc.add_paragraph()
caption_p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
caption_p1.paragraph_format.space_after = Pt(3)
c_run1 = caption_p1.add_run("Figure 1: Official Google Ads Performance Summary (Oct 9 – 15, 2026) showing 3 verified conversions across the 7-day post-turnaround window.")
c_run1.font.name = "Segoe UI"
c_run1.font.size = Pt(6.5)
c_run1.font.italic = True
c_run1.font.color.rgb = RGB_MUTED

if os.path.exists(img2_path):
    p_img2 = doc.add_paragraph()
    p_img2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_img2.paragraph_format.space_before = Pt(1)
    p_img2.paragraph_format.space_after = Pt(1)
    p_img2.add_run().add_picture(img2_path, width=Inches(5.7))

caption_p2 = doc.add_paragraph()
caption_p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
caption_p2.paragraph_format.space_after = Pt(4)
c_run2 = caption_p2.add_run("Figure 2: Google Ads notification noting a 171% cost increase alongside a 118% interaction increase compared to the prior frozen week.")
c_run2.font.name = "Segoe UI"
c_run2.font.size = Pt(6.5)
c_run2.font.italic = True
c_run2.font.color.rgb = RGB_MUTED

# ----------------- SECTION 2: MATHEMATICAL RECONCILIATION -----------------
add_heading_1("2. Mathematical Reconciliation of Conversion Rates & Budget Pacing")

add_body_p("A. Reconciliation of October Conversion Rates & Reporting Periods:", bold_prefix="• ")
add_body_p(
    "Jerzy noted that October's overall rate was 0.89%, while the weekly report quoted 2.56%. "
    "Here is the exact mathematical reconciliation across all reporting periods from the master sheet:\n"
    "1. Jerzy's 0.89% Figure: When Jerzy reviewed the sheet as of 12 October, October MTD had recorded 2 orders from 225 clicks = exactly 0.89% (2 / 225).\n"
    "2. Weekly Block of 6–12 October: During this specific 7-day post-unfreeze week, the campaign logged 78 clicks and 2 orders = 2.56% (2 / 78). The earlier 147 clicks from 1–5 October had 0 orders.\n"
    "3. Weekly Block of 13–16 October: Over the subsequent 4 days, the account logged 73 clicks, 1 order (£79.99 rev) = 1.37% (1 / 73) and 1.51x ROAS.\n"
    "4. Rolling 7-Day Window (9–15 October, Figure 1): This window captures the 3 sales across overlapping days, logging 165 clicks and 3 orders = 1.82% (3 / 165).\n"
    "5. Official October MTD (1–16 October): The master sheet records 319 clicks and 3 orders = 0.94% (3 / 319). The early month non-converting clicks dilute the monthly total."
)

table_recon = doc.add_table(rows=1, cols=8)
table_recon.alignment = WD_TABLE_ALIGNMENT.CENTER
table_recon.autofit = False
rc_widths = [Inches(1.4), Inches(0.7), Inches(0.55), Inches(0.5), Inches(0.65), Inches(0.65), Inches(0.55), Inches(2.0)]

rc_headers = ["Period / Block", "Spend", "Clicks", "Orders", "Conv. Rate", "Revenue", "ROAS", "Operational Status / Reconciling Note"]
for idx, h in enumerate(rc_headers):
    c = table_recon.cell(0, idx)
    c.width = rc_widths[idx]
    set_cell_background(c, HEX_NAVY)
    set_cell_margins(c, top=45, bottom=45, left=30, right=30)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h)
    r.font.name = "Segoe UI"
    r.font.size = Pt(6)
    r.font.bold = True
    r.font.color.rgb = RGB_WHITE

recon_data = [
    ("29 Sep – 5 Oct (Disruption)", "£99.52", "203", "0", "0.00%", "£0.00", "0.00x", "Account starved under £18 tCPA cap; zero orders."),
    ("6 – 12 Oct (Turnaround)", "£83.18", "78", "2", "2.56%", "£75.99", "0.91x", "2 sales on Oct 9 post-unfreeze (2/78 = 2.56%)."),
    ("13 – 16 Oct (Latest Block)", "£52.86", "73", "1", "1.37%", "£79.99", "1.51x", "1 sale on Oct 15; ROAS reaches 1.51x (nearing breakeven)."),
    ("9 – 15 Oct (Rolling 7d)", "£155.00", "165", "3", "1.82%", "~£150.00", "~0.74x", "Figure 1 dashboard window capturing all 3 sales."),
    ("1 – 16 Oct (Master MTD)", "£234.07", "319", "3", "0.94%", "£149.99", "0.64x", "Official master monthly row; early zero-sales dilute aggregate.")
]

for r_data in recon_data:
    row = table_recon.add_row()
    is_curr = "13 – 16 Oct" in r_data[0]
    is_mtd = "1 – 16 Oct" in r_data[0]
    for idx, val in enumerate(r_data):
        c = row.cells[idx]
        c.width = rc_widths[idx]
        bg = HEX_GREEN_BG if is_curr else (HEX_BLUE_BG if is_mtd else "FFFFFF")
        set_cell_background(c, bg)
        set_cell_margins(c, top=40, bottom=40, left=30, right=30)
        set_cell_border(c, top=HEX_BORDER, bottom=HEX_BORDER, left=HEX_BORDER, right=HEX_BORDER)
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        if idx in [1, 5]:
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        elif idx in [2, 3, 4, 6]:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(val)
        r.font.name = "Segoe UI"
        r.font.size = Pt(6)
        if idx in [0, 4, 6]:
            r.font.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(3)

add_body_p("B. Explanation of the £155 Spend vs. £19.69/day Budget Cap:", bold_prefix="• ")
add_body_p(
    "Jerzy noted that £155 spent over 7 days equals ~£22.14/day, which is ~12% above the nominal £19.69 daily budget. "
    "Under Google Ads standard pacing rules, the algorithm may spend up to 2x the daily budget on high-intent days to capture converting traffic, balanced by lower spend on quieter days, ensuring total spend never exceeds the monthly cap (30.4 × £19.69 = £598.58). "
    "The daily budget setting in Google Ads remains strictly capped at £19.69/day with zero increases."
)

# ----------------- SECTION 3: PRODUCT-LEVEL PROFITABILITY & UNIT ECONOMICS -----------------
add_heading_1("3. Product-Level Profitability & Target Unit Economics Matrix")

add_body_p(
    "IMPORTANT NOTE ON ACTUALS VS. TARGETS: The matrix below illustrates target unit economics required for profitability. "
    "Actual account-level CPA stands at £78.02 MTD (£52.86 over 13–16 Oct). "
    "To achieve profitability, aggregate CPA must be driven down toward the £6.50–£14.00 target CPAs below through search term pruning and conversion rate optimization:"
)

table_ue = doc.add_table(rows=1, cols=9)
table_ue.alignment = WD_TABLE_ALIGNMENT.CENTER
table_ue.autofit = False
ue_widths = [Inches(1.5), Inches(0.7), Inches(0.6), Inches(0.6), Inches(0.7), Inches(0.6), Inches(0.7), Inches(0.8), Inches(0.8)]

ue_headers = ["SKU / Product Name", "Retail", "COGS", "Delivery", "Gross Profit", "Margin*", "Target CPA", "Target Contrib.", "Target Margin"]
for idx, h in enumerate(ue_headers):
    c = table_ue.cell(0, idx)
    c.width = ue_widths[idx]
    set_cell_background(c, HEX_NAVY)
    set_cell_margins(c, top=45, bottom=45, left=35, right=35)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h)
    r.font.name = "Segoe UI"
    r.font.size = Pt(6.5)
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
        set_cell_margins(c, top=35, bottom=35, left=35, right=35)
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
        r.font.size = Pt(6.5)
        if idx in [0, 4, 7]:
            r.font.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(3)

add_body_p("*Margin Definition: Gross Margin is defined after deducting both product purchase cost (COGS) and UK tracked delivery.", bold_prefix="Note: ")
add_body_p(
    "Unit Economics Observations:\n"
    "1. Anti-Bark Collar Economics: The model targets £8.00 CPA to yield £9.00 net contribution. In the Oct 1–15 search audit, specific converting queries performed at £3.27 and £5.62 CPA (yielding £11.38–£13.73 contribution), but this is a very small initial sample (1.5 conversions) and cannot yet be assumed as an aggregate CPA.\n"
    "2. Multi-Pack Bundle Margin Impact: Moving a customer from a single Molar Stick (£16.00) to a 2-Pack (£28.00) increases net cash contribution per order by +189% (from £3.50 to £10.10) because shipping is paid once, lifting net margin by +14.2 percentage points (from 21.9% to 36.1%)."
)

# ----------------- SECTION 4: SEARCH LEAKAGE ELIMINATION -----------------
add_heading_1("4. Search Terms Leakage Audit (£38.24 Wasted Across 39 Clicks)")

add_body_p(
    "Our audit of 5,058 search queries (Oct 1–15) identified £38.24 in wasted spend across 39 clicks on products Pet Mode does not sell. "
    "This represents 26.4% of all disclosed query spend (£144.69) and 16.3% of total October MTD spend (£234.07). "
    "Eliminating these 4 categories redirects budget directly toward our converting items:"
)

table_leaks = doc.add_table(rows=1, cols=5)
table_leaks.alignment = WD_TABLE_ALIGNMENT.CENTER
table_leaks.autofit = False
lk_widths = [Inches(1.8), Inches(1.5), Inches(0.8), Inches(1.1), Inches(1.8)]

lk_headers = ["Leakage Category", "Example Search Queries", "Clicks", "Wasted Cost", "Action Taken"]
for idx, h in enumerate(lk_headers):
    c = table_leaks.cell(0, idx)
    c.width = lk_widths[idx]
    set_cell_background(c, HEX_NAVY)
    set_cell_margins(c, top=45, bottom=45, left=35, right=35)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(h)
    r.font.name = "Segoe UI"
    r.font.size = Pt(6.5)
    r.font.bold = True
    r.font.color.rgb = RGB_WHITE

leak_rows = [
    ("AirTags, GPS & Trackers", "air tag cat collar holder, cat tracker", "20", "£15.04", "Phrase negatives applied ('airtag', 'gps')."),
    ("Cat Litter & Automatic Toilets", "cat toilet, automatic litter tray", "13", "£14.85", "Phrase negatives applied ('litter', 'toilet')."),
    ("Competitor Brands", "luther bennett dog pod, pawrade", "4", "£6.03", "Brand negatives applied ('luther bennett', 'pawrade')."),
    ("Medical & Injured Paw", "waterproof dog boot for injured paw", "2", "£2.32", "Medical negatives applied ('injured paw', 'wound')."),
    ("Total Identified Leakage", "Across 39 non-converting clicks", "39", "£38.24", "Eliminates 26.4% of disclosed query waste.")
]

for r_data in leak_rows:
    row = table_leaks.add_row()
    is_tot = "Total" in r_data[0]
    for idx, val in enumerate(r_data):
        c = row.cells[idx]
        c.width = lk_widths[idx]
        set_cell_background(c, HEX_RED_BG if is_tot else "FFFFFF")
        set_cell_margins(c, top=35, bottom=35, left=35, right=35)
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
        r.font.size = Pt(6.5)
        if is_tot or idx in [0, 3]:
            r.font.bold = True

doc.add_paragraph().paragraph_format.space_after = Pt(3)

# ----------------- SECTION 5: ROAS REALITY & MARGIN PROTECTION -----------------
add_heading_1("5. Direct ROAS Benchmarks & Margin Protection Policy")

add_body_p(
    "1. Direct ROAS Reality: Based on Pet Mode's average post-delivery gross margin of 61%, breakeven ROAS is 1 / 0.61 = 1.64x. Target profitable ROAS is 2.0x–2.5x. Over October 1–16, MTD ROAS stands at 0.64x (£149.99 rev / £234.07 spend), diluted by early-month non-converting clicks. However, the post-fix weekly progression demonstrates clear acceleration toward breakeven: 0.00x (29 Sep–5 Oct) -> 0.91x (6–12 Oct) -> 1.51x (13–16 Oct). Three orders do not demonstrate sustained recovery; they provide an initial operational baseline. To bridge the remaining gap to 1.64x breakeven, ad spend must be concentrated on high-margin items while eliminating the £38.24 leakage.\n"
    "2. Margin Protection & Pricing Policy: In accordance with Jerzy's directive, we will not execute blanket price discounts that compromise unit margins. Promotional adjustments will be restricted to visual strikethrough price anchoring (displaying RRP £21 strikethrough to current £16, costing £0) or volume multi-packs where net contribution expands.\n"
    "3. Competitor Pricing Review Plan: We will conduct a structured competitor price and margin audit across our top 10 SKUs against Amazon UK, Pets at Home, and TikTok Shop, delivering a comprehensive Competitor Price & Margin Impact Matrix by Wednesday, 21 October, before any pricing changes are implemented.\n"
    "4. Verification of Store Claims: No delivery promises, customer review ratings, or product safety badges will be published on the store without Jerzy's explicit operational verification."
)

# ----------------- SECTION 6: 19 OCTOBER UPDATE COMMITMENT -----------------
add_heading_1("6. Budget Freeze & Formal Commitment to 19 October Milestone")

callout_table = doc.add_table(rows=1, cols=1)
callout_table.alignment = WD_TABLE_ALIGNMENT.CENTER
callout_table.autofit = False
callout_cell = callout_table.cell(0, 0)
callout_cell.width = Inches(7.0)
set_cell_background(callout_cell, HEX_BLUE_BG)
set_cell_margins(callout_cell, top=70, bottom=70, left=90, right=90)
set_cell_border(callout_cell, top=HEX_NAVY, bottom=HEX_NAVY, left=HEX_NAVY, right=HEX_NAVY, sz="10")

cp = callout_cell.paragraphs[0]
cp.paragraph_format.space_after = Pt(1.5)
c_title = cp.add_run("EXECUTIVE COMMITMENT & SUCCESS CRITERIA (19 OCTOBER REVIEW)\n")
c_title.font.name = "Segoe UI"
c_title.font.size = Pt(8)
c_title.font.bold = True
c_title.font.color.rgb = RGB_NAVY

c_body = cp.add_run(
    "1. Budget Discipline: Spend remains strictly capped at £19.69/day (£135–£140/week). Zero budget increases will occur until ROAS is proven.\n"
    "2. Leakage Elimination: Negative keywords active to stop the £38.24 leakage and redirect funds into the Anti-Bark Collar and Car Booster Bed.\n"
    "3. Objective Success Criteria for 19 October Milestone Review:\n"
    "   • Daily budget pacing strictly within £19.69/day limit.\n"
    "   • Order volume tracking toward 4–6 orders/week.\n"
    "   • Directional improvement in CPA from £52.86 toward £35.00.\n"
    "   • Directional improvement in ROAS from 1.51x toward 1.8x–2.0x.\n"
    "   • A concise numbers update will be delivered on Monday, 19 October covering: Spend, Orders, Revenue, ROAS, and CPA."
)
c_body.font.name = "Segoe UI"
c_body.font.size = Pt(7.5)
c_body.font.color.rgb = RGB_DARK

doc.save(docx_path)
print(f"Rebuilt DOCX saved to: {docx_path}")

# ----------------- WORD COM PDF EXPORT -----------------
word = win32com.client.Dispatch("Word.Application")
word.Visible = False
try:
    wdoc = word.Documents.Open(os.path.abspath(docx_path))
    wdoc.SaveAs(os.path.abspath(pdf_path), FileFormat=17) # 17 = wdFormatPDF
    wdoc.Close()
    print(f"Rebuilt PDF exported successfully: {pdf_path} (Size: {os.path.getsize(pdf_path)} bytes)")
finally:
    word.Quit()
