import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os

out_dir = r"c:\Users\test\Videos\Office\data\Pet Mode\Google Ads"
os.makedirs(out_dir, exist_ok=True)
excel_path = os.path.join(out_dir, "Pet_Mode_Product_Level_Profitability_Model.xlsx")

wb = openpyxl.Workbook()

# Styling
font_title = Font(name="Segoe UI", size=15, bold=True, color="1B365D")
font_subtitle = Font(name="Segoe UI", size=10, italic=True, color="555555")
font_header = Font(name="Segoe UI", size=9.5, bold=True, color="FFFFFF")
font_body = Font(name="Segoe UI", size=9.5, color="222222")
font_body_bold = Font(name="Segoe UI", size=9.5, bold=True, color="222222")

fill_navy = PatternFill("solid", fgColor="1B365D")
fill_gold = PatternFill("solid", fgColor="D4AF37")
fill_soft_blue = PatternFill("solid", fgColor="EBF5FB")
fill_soft_green = PatternFill("solid", fgColor="E8F8F5")
fill_soft_red = PatternFill("solid", fgColor="FDEDEC")
fill_zebra = PatternFill("solid", fgColor="FAFAFA")
fill_highlight = PatternFill("solid", fgColor="EAFAF1")

border_thin = Border(
    left=Side(style="thin", color="D5D8DC"),
    right=Side(style="thin", color="D5D8DC"),
    top=Side(style="thin", color="D5D8DC"),
    bottom=Side(style="thin", color="D5D8DC")
)

# ---------------- SHEET 1: Product-Level Profitability & Unit Economics ----------------
ws1 = wb.active
ws1.title = "Unit Economics & Profitability"
ws1.views.sheetView[0].showGridLines = True

ws1["B2"] = "PET MODE UK — PRODUCT-LEVEL UNIT ECONOMICS & CONTRIBUTION MARGIN MODEL"
ws1["B2"].font = font_title
ws1["B3"] = "Contribution Analysis per SKU: Purchase Cost, Tracked Delivery, Allowable CPA, and Net Contribution"
ws1["B3"].font = font_subtitle

headers = [
    "Priority / SKU", "Product Name", "Retail Price (£)", "Est. COGS (£)", 
    "Delivery (£)", "Gross Profit (£)", "Gross Margin (%)", "Max Breakeven CPA (£)", 
    "Target CPA (£)", "Target Net Contribution (£)", "Target Net Margin (%)", "Margin Scaling Strategy"
]

for idx, h in enumerate(headers, start=2):
    c = ws1.cell(5, idx, h)
    c.fill = fill_navy
    c.font = font_header
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

# Data based on Pet Mode product prices, CJ dropshipping / UK fulfillment supplier baselines
skus = [
    ("Hero SKU #1", "Dog Toothbrush Molar Stick (Single)", 16.00, 2.80, 3.20, 10.00, "62.5%", 10.00, 6.50, 3.50, "21.9%", "Front-end traffic driver. Push 2-pack bundle."),
    ("Hero Bundle", "Dog Toothbrush Molar Stick (Buy 2 Bundle)", 28.00, 5.60, 3.80, 18.60, "66.4%", 18.60, 8.50, 10.10, "36.1%", "HIGH MARGIN UNLOCK: Shipping paid once; +£6.60 net profit!"),
    ("Hero SKU #2", "3-in-1 Dog Dental Chew Toy & Stick", 16.99, 3.20, 3.20, 10.59, "62.3%", 10.59, 7.00, 3.59, "21.1%", "Maintain £16.99; test strikethrough £21.00 anchor."),
    ("Top Converter", "Smart Anti-Barking Dog Collar", 25.00, 4.80, 3.20, 17.00, "68.0%", 17.00, 8.00, 9.00, "36.0%", "OCTOBER WINNER: High contribution (£9.00/unit). Scalable!"),
    ("High AOV", "Dog Car Seat Booster Bed (Medium)", 49.99, 13.50, 5.80, 30.69, "61.4%", 30.69, 14.00, 16.69, "33.4%", "EXCELLENT MARGIN: £16.69 net contribution per order!"),
    ("Viral SKU", "Cat & Dog Steam Grooming Brush", 17.49, 3.20, 3.20, 11.09, "63.4%", 11.09, 7.00, 4.09, "23.4%", "Impulse add-on. Strong gift potential for Q4."),
    ("High Volume", "Self-Adhesive Cat Scratching Carpet", 17.00, 3.80, 3.50, 9.70, "57.1%", 9.70, 6.50, 3.20, "18.8%", "Add 2-roll pack (£29.00) to protect margin."),
    ("High Margin", "Elevated Cooling Mesh Dog Cot (Small)", 23.99, 7.20, 4.50, 12.29, "51.2%", 12.29, 8.00, 4.29, "17.9%", "Strikethrough £29.99 anchor. Solid margin buffer."),
    ("High Margin", "Elevated Cooling Bed with Bolsters", 40.00, 12.50, 5.50, 22.00, "55.0%", 22.00, 11.00, 11.00, "27.5%", "High perceived value; strong contribution margin."),
    ("High AOV", "Orthopaedic Waterproof Dog Bed", 38.99, 11.80, 5.80, 21.39, "54.9%", 21.39, 10.50, 10.89, "27.9%", "Premium comfort line; high customer satisfaction."),
    ("High AOV", "Automatic Cordless Water Fountain", 70.00, 22.00, 5.50, 42.50, "60.7%", 42.50, 18.00, 24.50, "35.0%", "Highest gross profit per unit (£42.50). High consideration.")
]

for r_idx, row in enumerate(skus, start=6):
    is_bundle = "Bundle" in row[1]
    is_bark = "Anti-Bark" in row[1]
    is_car = "Car Seat" in row[1]
    for c_idx, val in enumerate(row, start=2):
        c = ws1.cell(r_idx, c_idx, val)
        c.font = font_body_bold if (c_idx in [2, 4, 7, 9, 11] or is_bundle or is_bark) else font_body
        c.border = border_thin
        if is_bundle:
            c.fill = fill_highlight
        elif is_bark:
            c.fill = fill_soft_green
        elif r_idx % 2 == 0:
            c.fill = fill_zebra
            
        if c_idx in [4, 5, 6, 7, 9, 10, 11]:
            if isinstance(val, (int, float)):
                c.number_format = "£#,##0.00"
                c.alignment = Alignment(horizontal="right", vertical="center")
        elif c_idx in [8, 12]:
            c.alignment = Alignment(horizontal="center", vertical="center")
        else:
            c.alignment = Alignment(horizontal="left", vertical="center")

col_widths_s1 = [3, 16, 38, 14, 14, 14, 16, 16, 16, 18, 16, 46]
for col_idx, width in enumerate(col_widths_s1, start=1):
    ws1.column_dimensions[get_column_letter(col_idx)].width = width

# ---------------- SHEET 2: Breakeven ROAS & Scaling Thresholds ----------------
ws2 = wb.create_sheet(title="Breakeven ROAS Benchmarks")
ws2.views.sheetView[0].showGridLines = True

ws2["B2"] = "PET MODE UK — BREAKEVEN ROAS & CHANNEL TARGET MATRIX"
ws2["B2"].font = font_title
ws2["B3"] = "Direct Target ROAS Required for Net Positive Cash Flow Across Product Tiers"
ws2["B3"].font = font_subtitle

headers2 = ["Product Tier / Category", "Average Selling Price", "Gross Margin %", "Breakeven ROAS (Min)", "Target Profitable ROAS", "Allowable Max CPA", "Target Acquisition CPA", "Strategic Objective"]
for idx, h in enumerate(headers2, start=2):
    c = ws2.cell(5, idx, h)
    c.fill = fill_navy
    c.font = font_header
    c.alignment = Alignment(horizontal="center", vertical="center")

tiers = [
    ("Tier 1: Front-End Consumables (Chew Toys, Brushes)", "£16.00 – £17.50", "62% – 64%", "1.60x", "2.20x – 2.50x", "£10.00 – £11.00", "£6.50 – £7.50", "Acquire customer at breakeven/slight profit; push 2-pack bundles."),
    ("Tier 2: Mid-Tier Tech & Travel (Anti-Bark, Harness)", "£22.00 – £28.00", "65% – 68%", "1.50x", "2.00x – 2.40x", "£15.00 – £17.50", "£8.00 – £11.00", "CORE PROFIT ENGINE: Highest volume of net contribution cash flow."),
    ("Tier 3: High AOV Gear (Car Beds, Ortho Beds)", "£40.00 – £50.00", "55% – 61%", "1.65x", "2.20x – 2.60x", "£22.00 – £30.50", "£12.00 – £15.00", "High cash generator: £16+ net contribution per order even at £14 CPA."),
    ("Tier 4: Premium Hardware (Smart Water Fountain)", "£70.00", "60.7%", "1.65x", "2.00x – 2.30x", "£42.50", "£18.00 – £22.00", "Requires high consideration; retargeting / Shopping search focus.")
]

for r_idx, row in enumerate(tiers, start=6):
    for c_idx, val in enumerate(row, start=2):
        c = ws2.cell(r_idx, c_idx, val)
        c.font = font_body_bold if c_idx == 2 else font_body
        c.border = border_thin
        if r_idx % 2 == 0:
            c.fill = fill_zebra
        if c_idx in [3, 4, 5, 6, 7, 8]:
            c.alignment = Alignment(horizontal="center", vertical="center")
        else:
            c.alignment = Alignment(horizontal="left", vertical="center")

col_widths_s2 = [3, 34, 22, 16, 18, 20, 20, 20, 44]
for col_idx, width in enumerate(col_widths_s2, start=1):
    ws2.column_dimensions[get_column_letter(col_idx)].width = width

wb.save(excel_path)
print(f"Profitability workbook successfully saved to: {excel_path}")
