import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import os

def set_cell_background(cell, fill_hex):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

out_dir = 'reports'
os.makedirs(out_dir, exist_ok=True)
docx_path = os.path.join(out_dir, 'FABB6_Growth_and_Performance_Forecast_Report.docx')

doc = docx.Document()

# Page Margins
for section in doc.sections:
    section.top_margin = Inches(0.8)
    section.bottom_margin = Inches(0.8)
    section.left_margin = Inches(0.8)
    section.right_margin = Inches(0.8)

# Styles Setup
styles = doc.styles
normal_style = styles['Normal']
normal_style.font.name = 'Arial'
normal_style.font.size = Pt(10)
normal_style.font.color.rgb = RGBColor(15, 23, 42)

# Title Header
p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_title = p_title.add_run("FABB6 — 6-MONTH MASTER GROWTH & CPA REDUCTION FORECAST REPORT")
run_title.font.size = Pt(16)
run_title.font.bold = True
run_title.font.color.rgb = RGBColor(22, 101, 52)

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
run_sub = p_sub.add_run("Featuring Dual Forecast Models: Plan A (Volume Scaling) & Plan B (CPA Reduction & Remarketing)\nPrepared by Techno Exponent")
run_sub.font.size = Pt(10.5)
run_sub.font.italic = True
run_sub.font.color.rgb = RGBColor(71, 85, 105)

# Executive Summary for Plan B
h1 = doc.add_heading("1. NEW FORECAST: Plan B — CPA Reduction & Funnel Segmentation Model", level=1)
h1.runs[0].font.color.rgb = RGBColor(22, 101, 52)

p_summary = doc.add_paragraph(
    "Strategy Overview:\n"
    "Rather than forcing an aggressive 1,500 orders/day target regardless of ad spend, Plan B focuses on Funnel Segmentation to drive down Blended CPA and maximize Net ROAS Profitability.\n\n"
    "Funnel Strategy Breakdown:\n"
    "• New Customer Acquisition (Prospecting): CPA stays realistic (Meta ~₹400-420, Google ~₹650-700).\n"
    "• Remarketing (Cart Abandoners / Site Visitors): Highly targeted audience capture (Meta ~₹160-180, Google ~₹240-280).\n"
    "• Existing Customer Re-orders (Retention / CRM / App Push): Re-engagement at ultra-low acquisition costs (Meta ~₹78-90, Google ~₹102-118).\n\n"
    "Plan B Highlights:\n"
    "• Blended Paid CPA Reduction: Drops from ₹308.22 to ₹260.32/order.\n"
    "• Overall Business ROAS: Increases from 3.82x to 5.47x (6-Month Average: 4.84x vs Plan A's 3.80x).\n"
    "• 6-Month Revenue: ₹18.49 Crores on ₹3.82 Crores Paid Spend (Saves ₹1.06 Crores in Ad Spend)."
)

# Plan B Channel Table
h2 = doc.add_heading("Plan B — Complete 6-Month Channel Sales Forecast Table (CPA Efficiency Model)", level=2)
h2.runs[0].font.color.rgb = RGBColor(15, 23, 42)

table_b = doc.add_table(rows=1, cols=9)
table_b.alignment = WD_TABLE_ALIGNMENT.CENTER
hdr_cells = table_b.rows[0].cells
headers_b = ["Month", "Total Spend (INR)", "Sales from Ads Only", "Google Ads Sales", "Meta Ads Sales", "Organic Sales", "Return Customer Sales", "Total Sales", "Blended CPA / ROAS"]

for i, title in enumerate(headers_b):
    hdr_cells[i].text = title
    set_cell_background(hdr_cells[i], "16A34A")
    p = hdr_cells[i].paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in p.runs:
        run.font.bold = True
        run.font.size = Pt(8)
        run.font.color.rgb = RGBColor(255, 255, 255)

b_rows = [
    ("Sept 2026", "₹45.00 L", "₹1.325 Cr (77.2%)", "₹63.92 L (37.2%)", "₹68.60 L (39.9%)", "₹22.50 L", "₹16.72 L", "₹1.717 Cr", "₹308 / 3.82x"),
    ("Oct 2026 (Festive)", "₹52.00 L", "₹1.658 Cr (73.4%)", "₹74.10 L (32.8%)", "₹91.67 L (40.6%)", "₹27.00 L", "₹32.98 L", "₹2.258 Cr", "₹287 / 4.34x"),
    ("Nov 2026 (Peak)", "₹60.00 L", "₹1.999 Cr (71.8%)", "₹88.32 L (31.7%)", "₹111.60 L (40.1%)", "₹34.96 L", "₹43.68 L", "₹2.786 Cr", "₹278 / 4.64x"),
    ("Dec 2026 (Year-End)", "₹68.00 L", "₹2.348 Cr (69.9%)", "₹103.79 L (30.9%)", "₹131.04 L (39.0%)", "₹44.64 L", "₹56.42 L", "₹3.359 Cr", "₹271 / 4.94x"),
    ("Jan 2027", "₹75.00 L", "₹2.668 Cr (68.6%)", "₹119.56 L (30.7%)", "₹147.20 L (37.8%)", "₹51.70 L", "₹70.50 L", "₹3.890 Cr", "₹266 / 5.19x"),
    ("Feb 2027 (Milestone)", "₹82.00 L", "₹3.013 Cr (67.2%)", "₹137.61 L (30.7%)", "₹163.68 L (36.5%)", "₹58.90 L", "₹88.20 L", "₹4.484 Cr", "₹260 / 5.47x"),
    ("6-MONTH CUMULATIVE", "₹3.820 Cr", "₹11.333 Cr (61.1%)", "₹5.843 Cr (31.5%)", "₹5.490 Cr (29.6%)", "₹2.970 Cr", "₹4.246 Cr", "₹18.493 Cr", "₹271 avg / 4.84x")
]

for row_data in b_rows:
    row_cells = table_b.add_row().cells
    for i, val in enumerate(row_data):
        row_cells[i].text = val
        p = row_cells[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.size = Pt(8)
            if row_data[0] == "6-MONTH CUMULATIVE":
                run.font.bold = True
                set_cell_background(row_cells[i], "E2E8F0")

doc.add_paragraph()

# Save Document
doc.save(docx_path)
print(f"Updated Word / Google Doc report with Plan B at {docx_path}")
