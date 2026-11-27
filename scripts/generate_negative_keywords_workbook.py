import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os

out_dir = r"c:\Users\test\Videos\Office\data\Pet Mode\Google Ads"
os.makedirs(out_dir, exist_ok=True)
excel_path = os.path.join(out_dir, "Pet_Mode_Recommended_Negative_Keywords_Oct2026.xlsx")

wb = openpyxl.Workbook()

# Styles
font_title = Font(name="Segoe UI", size=15, bold=True, color="1B365D")
font_subtitle = Font(name="Segoe UI", size=10, italic=True, color="555555")
font_header = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
font_body = Font(name="Segoe UI", size=9.5, color="222222")
font_body_bold = Font(name="Segoe UI", size=9.5, bold=True, color="222222")

fill_navy = PatternFill("solid", fgColor="1B365D")
fill_soft_blue = PatternFill("solid", fgColor="EBF5FB")
fill_soft_green = PatternFill("solid", fgColor="E8F8F5")
fill_soft_red = PatternFill("solid", fgColor="FDEDEC")
fill_zebra = PatternFill("solid", fgColor="FAFAFA")

border_thin = Border(
    left=Side(style="thin", color="D5D8DC"),
    right=Side(style="thin", color="D5D8DC"),
    top=Side(style="thin", color="D5D8DC"),
    bottom=Side(style="thin", color="D5D8DC")
)

# ---------------- SHEET 1: Recommended Negative Keywords ----------------
ws1 = wb.active
ws1.title = "Actionable Negatives"
ws1.views.sheetView[0].showGridLines = True

ws1["B2"] = "PET MODE UK — RECOMMENDED NEGATIVE KEYWORDS (OCTOBER 2026)"
ws1["B2"].font = font_title
ws1["B3"] = "Extracted from October 1–15 Search Terms Audit to Eliminate £35.76+ In Wasted Clicks"
ws1["B3"].font = font_subtitle

headers1 = ["Negative Keyword", "Match Type", "Leakage Category", "Triggered Queries in Oct", "Wasted Spend Identified", "Rationale / Action"]
for idx, h in enumerate(headers1, start=2):
    c = ws1.cell(5, idx, h)
    c.fill = fill_navy
    c.font = font_header
    c.alignment = Alignment(horizontal="center", vertical="center")

negatives_list = [
    # AirTag & GPS
    ("airtag", "Phrase", "Electronics & Trackers", "504 queries", "£15.04", "Pet Mode sells standard collars/leashes, not Apple AirTags or electronics."),
    ("air tag", "Phrase", "Electronics & Trackers", "504 queries", "Included above", "Cat collar holder queries costing up to £4.85 per click."),
    ("tracker", "Phrase", "Electronics & Trackers", "247+ impr", "Included above", "Exclude cat/dog GPS trackers (e.g. Tractive, PitPat)."),
    ("gps", "Phrase", "Electronics & Trackers", "150+ impr", "Included above", "Store does not offer electronic tracking systems."),
    ("apple", "Phrase", "Electronics & Trackers", "35+ impr", "Included above", "Blocks Apple-related pet accessories."),
    ("tile", "Phrase", "Electronics & Trackers", "15+ impr", "Included above", "Tile tracker collars."),
    ("moravon", "Phrase", "Electronics & Trackers", "10+ impr", "Included above", "Moravon GPS tracker queries."),
    
    # Cat Litter & Toilets
    ("litter", "Phrase", "Cat Litter & Toilets", "317 queries", "£14.85", "Store does not sell cat litter, litter boxes, or £300+ automatic trays."),
    ("toilet", "Phrase", "Cat Litter & Toilets", "25+ impr", "£4.26 single click!", "Cat toilet queries cost £4.26 per click with 0% relevance."),
    ("litter box", "Phrase", "Cat Litter & Toilets", "80+ impr", "Included above", "Automatic litter box queries trigger rolling toy/scratch pad."),
    ("litter robot", "Phrase", "Cat Litter & Toilets", "67 impr", "Included above", "Competitor automatic litter machine."),
    ("litter tray", "Phrase", "Cat Litter & Toilets", "45+ impr", "Included above", "Non-relevant cat hygiene queries."),
    
    # Competitor Brands
    ("luther bennett", "Phrase", "Competitor Brands", "9 impr, 1 click", "£2.05", "Competitor dog pod brand; does not convert."),
    ("pawrade", "Phrase", "Competitor Brands", "3 impr, 1 click", "£1.89", "Competitor pet travel booster brand."),
    ("zoospot", "Phrase", "Competitor Brands", "2 impr, 1 click", "£1.50", "Competitor store name."),
    ("omlet", "Phrase", "Competitor Brands", "5 impr", "£0.00", "Competitor pet housing brand."),
    ("tractive", "Phrase", "Competitor Brands", "8 impr", "£0.00", "Competitor pet GPS tracker brand."),
    
    # Medical & Injury
    ("injured paw", "Phrase", "Medical & Injury", "15+ impr", "£0.00", "Pet Mode sells regular lifestyle products, not medical bandages."),
    ("injury", "Phrase", "Medical & Injury", "20+ impr", "£0.00", "Medical convalescence terms."),
    ("dog boot for injured paw", "Exact", "Medical & Injury", "5 impr", "£0.00", "Surgical/wound protection queries."),
    ("wound", "Phrase", "Medical & Injury", "10+ impr", "£0.00", "Veterinary wound queries."),
    ("vet", "Phrase", "Medical & Injury", "35+ impr", "£0.00", "Veterinary services searches.")
]

for r_idx, row in enumerate(negatives_list, start=6):
    is_even = (r_idx % 2 == 0)
    for c_idx, val in enumerate(row, start=2):
        c = ws1.cell(r_idx, c_idx, val)
        c.font = font_body_bold if c_idx in [2, 3] else font_body
        c.border = border_thin
        if is_even:
            c.fill = fill_zebra
        if c_idx == 2:
            c.font = Font(name="Segoe UI", size=9.5, bold=True, color="922B21")
        if c_idx in [3, 4, 5]:
            c.alignment = Alignment(horizontal="center", vertical="center")
        else:
            c.alignment = Alignment(horizontal="left", vertical="center")

col_widths_s1 = [3, 28, 16, 26, 26, 24, 48]
for col_idx, width in enumerate(col_widths_s1, start=1):
    ws1.column_dimensions[get_column_letter(col_idx)].width = width


# ---------------- SHEET 2: Category Intent Breakdown ----------------
ws2 = wb.create_sheet(title="Category Intent Breakdown")
ws2.views.sheetView[0].showGridLines = True

ws2["B2"] = "PET MODE UK — OCTOBER 1–15 SEARCH CATEGORY PERFORMANCE"
ws2["B2"].font = font_title
ws2["B3"] = "Analysis of Spending, Clicks, and Conversion Efficiency Across Product Clusters"
ws2["B3"].font = font_subtitle

headers2 = ["Product Category", "Unique Queries", "Impressions", "Clicks", "Ad Spend (£)", "Conversions", "Avg CPC (£)", "Cost / Conv (£)", "Conv. Rate", "Strategic Assessment"]
for idx, h in enumerate(headers2, start=2):
    c = ws2.cell(5, idx, h)
    c.fill = fill_navy
    c.font = font_header
    c.alignment = Alignment(horizontal="center", vertical="center")

cat_data = [
    ("Anti-Bark & Training Collars (WINNER)", 1049, 3590, 47, 42.73, 1.5, 0.91, 28.49, "3.19%", "STAR CONVERTER: Captures all direct conversions. Protect and scale!"),
    ("Dog Car Seat & Travel Bed", 512, 2615, 45, 37.12, 0.0, 0.82, 0.0, "0.00%", "High intent (14 clicks on 'dog car seat'). Needs price & trust badge push."),
    ("Beds & Furniture", 898, 2851, 37, 23.93, 0.0, 0.65, 0.0, "0.00%", "Efficient CPC (£0.65). Good consideration volume on orthopedic & raised beds."),
    ("Leashes & Harnesses", 447, 1082, 11, 7.89, 0.0, 0.72, 0.0, "0.00%", "Low spend. Maintain reflective harness visibility."),
    ("Dental Care & Toothbrushes (HERO SKU)", 149, 423, 4, 1.22, 0.0, 0.31, 0.0, "0.00%", "UNDER-INDEXED! Only £1.22 spend despite being store #1 bestseller! Push budget here."),
    ("Grooming & Steam Brushes", 183, 535, 7, 1.95, 0.0, 0.28, 0.0, "0.00%", "Under-indexed. £0.28 CPC is super cheap. Push viral steam brush."),
    ("Cat Scratchers & Pads", 234, 587, 3, 1.31, 0.0, 0.44, 0.0, "0.00%", "Low volume. Ensure scratch pad is matched to 'cat furniture protector' terms."),
    ("Water Fountains & Bowls", 71, 100, 0, 0.00, 0.0, 0.00, 0.0, "0.00%", "Zero clicks. Review fountain feed titles."),
    ("--- LEAK: Electronics & AirTags ---", 504, 2284, 20, 15.04, 0.0, 0.75, 0.0, "0.00%", "PURE WASTE: £15.04 spent on GPS/AirTag queries Pet Mode does not sell."),
    ("--- LEAK: Cat Litter & Toilets ---", 317, 1094, 13, 14.85, 0.0, 1.14, 0.0, "0.00%", "PURE WASTE: £14.85 spent on automatic litter boxes. Exclude immediately."),
    ("--- LEAK: Competitor Brands ---", 68, 148, 4, 6.03, 0.0, 1.51, 0.0, "0.00%", "PURE WASTE: £6.03 spent on Luther Bennett, Pawrade, Zoospot."),
    ("--- LEAK: Medical & Injured Paw ---", 113, 198, 2, 2.32, 0.0, 1.16, 0.0, "0.00%", "PURE WASTE: £2.32 spent on injury boot queries.")
]

for r_idx, row in enumerate(cat_data, start=6):
    is_winner = "WINNER" in row[0]
    is_leak = "LEAK" in row[0]
    for c_idx, val in enumerate(row, start=2):
        c = ws2.cell(r_idx, c_idx, val)
        c.font = font_body_bold if (c_idx == 2 or is_winner or is_leak) else font_body
        c.border = border_thin
        if is_winner:
            c.fill = fill_soft_green
        elif is_leak:
            c.fill = fill_soft_red
            if c_idx == 2:
                c.font = Font(name="Segoe UI", size=9.5, bold=True, color="922B21")
        if c_idx in [3, 4, 5, 7]:
            c.alignment = Alignment(horizontal="center", vertical="center")
            if isinstance(val, int):
                c.number_format = "#,##0"
        elif c_idx in [6, 8, 9]:
            c.alignment = Alignment(horizontal="right", vertical="center")
            if isinstance(val, (int, float)):
                c.number_format = "£#,##0.00"

col_widths_s2 = [3, 36, 16, 14, 12, 14, 14, 14, 16, 14, 48]
for col_idx, width in enumerate(col_widths_s2, start=1):
    ws2.column_dimensions[get_column_letter(col_idx)].width = width

wb.save(excel_path)
print(f"Negative keywords and category audit workbook saved to: {excel_path}")
