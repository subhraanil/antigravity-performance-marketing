import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

output_path = r"data/Pet Mode/Google Ads/Pet_Mode_Search_Terms_Audit_14d_7d_Oct2026.xlsx"

wb = openpyxl.Workbook()
# remove default sheet
wb.remove(wb.active)

# Styles
navy_fill = PatternFill(start_color="1B365D", end_color="1B365D", fill_type="solid")
navy_font = Font(name="Segoe UI", size=10, bold=True, color="FFFFFF")
header_fill = PatternFill(start_color="2C3E50", end_color="2C3E50", fill_type="solid")
header_font = Font(name="Segoe UI", size=9, bold=True, color="FFFFFF")
green_fill = PatternFill(start_color="E8F8F5", end_color="E8F8F5", fill_type="solid")
blue_fill = PatternFill(start_color="EBF5FB", end_color="EBF5FB", fill_type="solid")
red_fill = PatternFill(start_color="FDEDEC", end_color="FDEDEC", fill_type="solid")
gray_fill = PatternFill(start_color="F8F9FA", end_color="F8F9FA", fill_type="solid")

thin_border = Border(
    left=Side(style='thin', color='D5D8DC'),
    right=Side(style='thin', color='D5D8DC'),
    top=Side(style='thin', color='D5D8DC'),
    bottom=Side(style='thin', color='D5D8DC')
)

bold_font = Font(name="Segoe UI", size=9, bold=True, color="2C3E50")
normal_font = Font(name="Segoe UI", size=9, color="2C3E50")
title_font = Font(name="Segoe UI", size=13, bold=True, color="1B365D")
sub_font = Font(name="Segoe UI", size=9, italic=True, color="566573")

# ----------------- SHEET 1: EXECUTIVE COMPARISON -----------------
ws1 = wb.create_sheet(title="Executive Comparison")
ws1.views.sheetView[0].showGridLines = True

ws1.cell(row=1, column=1, value="Pet Mode UK — Search Terms Forensic Audit & Progression Analysis").font = title_font
ws1.cell(row=2, column=1, value="Comparing Last 14 Days (8–21 Oct) vs Last 7 Days (15–21 Oct) vs First 7 Days (8–14 Oct)").font = sub_font

headers_ws1 = ["Performance Dimension", "Metric", "Week 1 (8–14 Oct)", "Week 2 (15–21 Oct)", "Change (W2 vs W1)", "14-Day Total (8–21 Oct)", "Operational Takeaway / Strategic Impact"]
ws1.row_dimensions[4].height = 24
for col_idx, h in enumerate(headers_ws1, 1):
    cell = ws1.cell(row=4, column=col_idx, value=h)
    cell.fill = navy_fill
    cell.font = navy_font
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

data_ws1 = [
    # Dimension, Metric, W1, W2, Chg, 14d, Note
    ("Account-Level Totals", "Total Ad Spend", "£141.86", "£149.28", "+5.2%", "£291.14", "Disciplined pacing strictly within ~£21.33/day (locked near £19.69 cap)."),
    ("Account-Level Totals", "Impressions", "9,628", "22,239", "+131.0%", "31,867", "Auction delivery expanded +131% as Google algorithm learned high-converting assets."),
    ("Account-Level Totals", "Clicks", "145", "227", "+56.6%", "372", "High-intent traffic delivery increased by +56.6% week-over-week."),
    ("Account-Level Totals", "Average CPC", "£0.98", "£0.66", "-32.5%", "£0.78", "Cost per click decreased by -32.5%, maximizing traffic efficiency per pound spent."),
    ("Account-Level Totals", "Click-Through Rate (CTR)", "1.51%", "1.02%", "-32.3%", "1.17%", "Broadened reach across higher-funnel Shopping inventory."),
    ("Account-Level Totals", "Conversions (Sales)", "2.0", "3.0", "+50.0%", "5.0", "Conversions surged +50% week-over-week; 5 total conversions in 14 days."),
    ("Account-Level Totals", "Cost per Acquisition (CPA)", "£70.93", "£49.76", "-29.8%", "£58.23", "Account CPA dropped below £50 (£49.76), down from £78.02 MTD earlier."),
    ("Disclosed Search Terms", "Disclosed Spend", "£98.34", "£80.89", "-17.7%", "£179.23", "Disclosed query spend became more efficient while capturing 2.0 conversions."),
    ("Disclosed Search Terms", "Disclosed Clicks", "96", "139", "+44.8%", "235", "Disclosed clicks increased by +44.8% at significantly lower unit costs."),
    ("Disclosed Search Terms", "Disclosed Avg CPC", "£1.02", "£0.58", "-43.4%", "£0.76", "Dramatic -43.4% reduction in click costs on specific customer search queries."),
    ("Disclosed Search Terms", "Disclosed CPA", "£65.56", "£40.44", "-38.3%", "£51.21", "Specific customer queries converted at £40.44 CPA in the last 7 days!"),
    ("Negative Keywords Impact", "AirTags / GPS Clicks & Spend", "£0.00 (0 clicks)", "£0.00 (0 clicks)", "100% Eliminated", "£0.00 (0 clicks)", "Negative keywords completely stopped previous £15.04 AirTag leakage!"),
    ("Negative Keywords Impact", "Cat Litter / Toilet Clicks", "£6.05 (2 clicks)", "£0.00 (0 clicks)", "100% Eliminated", "£6.05 (2 clicks)", "Cat litter / toilet clicks dropped to zero in Week 2 following negative addition.")
]

for row_idx, r in enumerate(data_ws1, 5):
    ws1.row_dimensions[row_idx].height = 20
    is_cpa = "CPA" in r[1]
    is_conv = "Conversions" in r[1]
    is_neg = "Negative" in r[0]
    
    fill = green_fill if (is_cpa or is_conv or is_neg) else (gray_fill if row_idx % 2 == 0 else PatternFill(fill_type=None))
    for col_idx, val in enumerate(r, 1):
        cell = ws1.cell(row=row_idx, column=col_idx, value=val)
        cell.font = bold_font if col_idx in [1, 2, 4, 5] else normal_font
        cell.border = thin_border
        cell.fill = fill
        if col_idx in [3, 4, 5, 6]:
            cell.alignment = Alignment(horizontal="right", vertical="center")
        elif col_idx == 7:
            cell.alignment = Alignment(horizontal="left", vertical="center")
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")

# ----------------- SHEET 2: CONVERTING QUERIES -----------------
ws2 = wb.create_sheet(title="Converting Search Queries")
ws2.views.sheetView[0].showGridLines = True

ws2.cell(row=1, column=1, value="Pet Mode UK — Verified Converting Search Terms (8–21 October 2026)").font = title_font
ws2.cell(row=2, column=1, value="Forensic proof of converting customer queries and SKU-level unit margin verification").font = sub_font

headers_ws2 = ["Search Term", "Period", "Matched SKU / Catalog Item", "Impressions", "Clicks", "Avg CPC", "Total Cost", "Conversions", "Actual CPA", "Target CPA", "Net Contribution Impact"]
ws2.row_dimensions[4].height = 24
for col_idx, h in enumerate(headers_ws2, 1):
    cell = ws2.cell(row=4, column=col_idx, value=h)
    cell.fill = navy_fill
    cell.font = navy_font
    cell.alignment = Alignment(horizontal="center", vertical="center")

converting_data = [
    ("stop dog barking device", "Last 7 Days (15–21 Oct)", "Smart Anti-Bark Collar (£25 RRP)", 15, 2, "£0.34", "£0.68", 1.0, "£0.68", "£8.00", "Gross profit £17.00 - £0.68 ad cost = £16.32 net profit (65.3% margin)!"),
    ("cat climbing shelves", "Last 7 Days (15–21 Oct)", "Self-Adhesive Cat Scratching Carpet (£17 RRP)", 1, 1, "£0.95", "£0.95", 1.0, "£0.95", "£6.50", "Gross profit £9.70 - £0.95 ad cost = £8.75 net profit (51.5% margin)!"),
    ("dog barking collar best", "Week 1 (8–14 Oct)", "Smart Anti-Bark Collar (£25 RRP)", 1, 1, "£3.27", "£3.27", 1.0, "£3.27", "£8.00", "Gross profit £17.00 - £3.27 ad cost = £13.73 net profit (54.9% margin)!"),
    ("anti bark dog collar", "Week 1 (8–14 Oct)", "Smart Anti-Bark Collar (£25 RRP)", 32, 2, "£1.83", "£3.65", 0.5, "£7.30", "£8.00", "Gross profit £17.00 - £7.30 ad cost = £9.70 net profit (38.8% margin)!"),
    ("Other search terms (Google hidden)", "Last 7 Days (15–21 Oct)", "Performance Max Cross-Catalog", 7380, 88, "£0.78", "£68.36", 1.0, "£68.36", "£10.00", "1 conversion captured from long-tail aggregated intent."),
    ("Other search terms (Google hidden)", "Week 1 (8–14 Oct)", "Performance Max Cross-Catalog", 2500, 41, "£1.00", "£41.07", 0.5, "£82.14", "£10.00", "0.5 conversion captured from long-tail aggregated intent.")
]

for row_idx, r in enumerate(converting_data, 5):
    ws2.row_dimensions[row_idx].height = 20
    is_bark = "bark" in r[0] or "bark" in r[2]
    fill = green_fill if is_bark else (blue_fill if "cat" in r[0] else gray_fill)
    for col_idx, val in enumerate(r, 1):
        cell = ws2.cell(row=row_idx, column=col_idx, value=val)
        cell.font = bold_font if col_idx in [1, 8, 9] else normal_font
        cell.border = thin_border
        cell.fill = fill
        if col_idx in [4, 5, 8]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif col_idx in [6, 7, 9, 10]:
            cell.alignment = Alignment(horizontal="right", vertical="center")
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")

# ----------------- SHEET 3: CATEGORY SPEND & CONVERSION BREAKDOWN -----------------
ws3 = wb.create_sheet(title="Category Spend Analysis")
ws3.views.sheetView[0].showGridLines = True

ws3.cell(row=1, column=1, value="Pet Mode UK — Disclosed Search Spend by Product Theme (Last 7 Days: 15–21 Oct)").font = title_font
ws3.cell(row=2, column=1, value="Identifying profit centers vs budget-diluting categories across £80.89 disclosed spend").font = sub_font

headers_ws3 = ["Product Category / Search Intent", "Queries", "Clicks", "Spend (£)", "Avg CPC", "Conversions", "Actual CPA", "% Disclosed Spend", "Strategic Evaluation & Recommended Action"]
ws3.row_dimensions[4].height = 24
for col_idx, h in enumerate(headers_ws3, 1):
    cell = ws3.cell(row=4, column=col_idx, value=h)
    cell.fill = navy_fill
    cell.font = navy_font
    cell.alignment = Alignment(horizontal="center", vertical="center")

cat_data_7d = [
    ("Barking / Anti-Bark Collars", 499, 11, "£6.73", "£0.61", 1.0, "£6.73", "8.3%", "PROFIT WINNER: Converts below target CPA (£8.00). Keep scaling safely."),
    ("Cat Scratch / Climbing / Mats", 444, 5, "£2.51", "£0.50", 1.0, "£2.51", "3.1%", "PROFIT WINNER: Trim-to-fit scratching carpet converted at £0.95 CPA."),
    ("Dog Beds (General / Ortho / Large)", 1691, 61, "£38.09", "£0.62", 0.0, "-", "47.1%", "BUDGET HEAVY: 47% of spend with 0 conversions. Prune XXL, sofa & footstool queries."),
    ("Dog Car Seat / Travel Beds", 344, 21, "£11.54", "£0.55", 0.0, "-", "14.3%", "HIGH INTENT: CPC dropped to £0.55. Exclude ISOFIX terms and test volume bundle."),
    ("Other / Miscellaneous Intent", 1388, 28, "£12.04", "£0.43", 0.0, "-", "14.9%", "LONG-TAIL: Low CPC (£0.43). Monitor for unexpected leakage."),
    ("Leads / Harnesses / Apparel", 312, 9, "£5.36", "£0.60", 0.0, "-", "6.6%", "LOW VOLUME: Basic leash/harness clicks. Maintain current negative controls."),
    ("Competitor Brands (Leakage)", 13, 1, "£2.92", "£2.92", 0.0, "-", "3.6%", "LEAKAGE: Wasted click on 'pawcify'. Add negative brand list."),
    ("Dog Food & Meat Treats (Leakage)", 68, 1, "£1.16", "£1.16", 0.0, "-", "1.4%", "LEAKAGE: Click on 'buffalo trachea'. Negative 'trachea' & 'jerky' immediately."),
    ("Dental / Chews / Toys", 143, 2, "£0.54", "£0.27", 0.0, "-", "0.7%", "VERY EFFICIENT: Ultra-low CPC (£0.27) on toothbrush molar stick terms.")
]

for row_idx, r in enumerate(cat_data_7d, 5):
    ws3.row_dimensions[row_idx].height = 20
    is_win = "WINNER" in r[8]
    is_leak = "LEAKAGE" in r[8]
    is_heavy = "BUDGET HEAVY" in r[8]
    fill = green_fill if is_win else (red_fill if (is_leak or is_heavy) else PatternFill(fill_type=None))
    for col_idx, val in enumerate(r, 1):
        cell = ws3.cell(row=row_idx, column=col_idx, value=val)
        cell.font = bold_font if col_idx in [1, 4, 6, 7] else normal_font
        cell.border = thin_border
        cell.fill = fill
        if col_idx in [2, 3, 6]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif col_idx in [4, 5, 7, 8]:
            cell.alignment = Alignment(horizontal="right", vertical="center")
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")

# ----------------- SHEET 4: RECOMMENDED NEGATIVE KEYWORDS -----------------
ws4 = wb.create_sheet(title="Recommended Negatives")
ws4.views.sheetView[0].showGridLines = True

ws4.cell(row=1, column=1, value="Pet Mode UK — Actionable Negative Keywords to Implement (22 October 2026)").font = title_font
ws4.cell(row=2, column=1, value="Eliminating £22.66 in newly detected search leakage to protect daily budget and raise ROAS").font = sub_font

headers_ws4 = ["Category", "Recommended Negative Keyword", "Match Type", "Campaign Level", "7d Wasted Spend", "14d Wasted Spend", "14d Clicks", "Example Search Queries", "Business Justification"]
ws4.row_dimensions[4].height = 24
for col_idx, h in enumerate(headers_ws4, 1):
    cell = ws4.cell(row=4, column=col_idx, value=h)
    cell.fill = navy_fill
    cell.font = navy_font
    cell.alignment = Alignment(horizontal="center", vertical="center")

neg_data = [
    ("Size Mismatch (XXL/Giant)", "xxl", "Phrase", "Account / PMax", "£4.56", "£4.91", 3, "xxl dog beds, waterproof dog bed xxl", "Pet Mode sells standard & large beds, not XXL beds (£2.28 CPC waste)."),
    ("Competitor Brands", "pawcify", "Phrase", "Account / PMax", "£2.92", "£2.92", 1, "pawcify", "Direct competitor brand search; zero Pet Mode brand equity."),
    ("Human & Furniture Items", "heated blanket", "Phrase", "Account / PMax", "£2.26", "£2.26", 2, "dog heated blanket, pet heated blanket", "Pet Mode does not sell electrical heated pet blankets."),
    ("Competitor Brands", "luther bennett", "Phrase", "Account / PMax", "£0.00", "£2.05", 1, "luther bennett dog pod", "Competitor brand for luxury travel dog beds."),
    ("Competitor Brands", "pawrade", "Phrase", "Account / PMax", "£0.00", "£1.89", 1, "pawrade pet car seat", "Competitor brand for pet car seats."),
    ("ISOFIX Car Mechanism", "isofix", "Phrase", "Account / PMax", "£0.71", "£1.58", 6, "isofix dog car seat uk, dog car seat with isofix", "Car booster bed uses seatbelt buckles/straps, not rigid ISOFIX latch anchors."),
    ("Human & Furniture Items", "footstool", "Phrase", "Account / PMax", "£1.49", "£1.49", 1, "footstool dog bed", "Pet Mode does not sell furniture footstools."),
    ("Dog Food & Edible Treats", "trachea", "Phrase", "Account / PMax", "£1.16", "£1.16", 1, "buffalo trachea for dogs", "Pet Mode sells toys and grooming tools, not edible dried meat/organs."),
    ("Dog Food & Edible Treats", "jerky", "Phrase", "Account / PMax", "£0.90", "£0.90", 1, "beef jerky for dogs", "Pet Mode does not sell beef jerky treats."),
    ("Human & Furniture Items", "dog couch", "Phrase", "Account / PMax", "£0.62", "£0.62", 1, "luxury dog couch", "Pet Mode does not sell upholstered couches/sofas."),
    ("Heavy Metal Chains", "necklace", "Phrase", "Account / PMax", "£0.60", "£0.60", 2, "dog necklace chain, dog chain necklace", "Jewelry intent rather than pet functional collars."),
    ("Human & Furniture Items", "dog sofa", "Phrase", "Account / PMax", "£0.54", "£0.54", 1, "dog sofa, dog sofas for large dogs", "Furniture sofa search intent."),
    ("Size Mismatch (XXL/Giant)", "giant dog bed", "Phrase", "Account / PMax", "£0.52", "£0.52", 2, "giant dog bed for humans, giant dog bed", "Search intent for giant breed or human-sized Plufl beds."),
    ("Competitor Brands", "wagging rights", "Phrase", "Account / PMax", "£0.40", "£0.40", 1, "wagging rights car dog bed", "Competitor car bed brand."),
    ("Heavy Metal Chains", "cuban", "Phrase", "Account / PMax", "£0.36", "£0.36", 1, "cuban dog collar", "High-cost luxury jewelry chain queries."),
    ("Competitor Brands", "jacko and co", "Phrase", "Account / PMax", "£0.25", "£0.25", 1, "jacko and co", "Competitor brand name."),
    ("Human & Furniture Items", "for humans", "Phrase", "Account / PMax", "£0.21", "£0.21", 1, "giant dog bed for humans", "Human-sized pet beds (Plufl concept)."),
    ("Dog Food & Edible Treats", "dog food", "Phrase", "Account / PMax", "£0.00", "£0.00", 0, "dog food, puppy food", "Preventative exclusion for pet food.")
]

for row_idx, r in enumerate(neg_data, 5):
    ws4.row_dimensions[row_idx].height = 20
    fill = red_fill if float(r[4].replace("£", "")) > 1.0 else (gray_fill if row_idx % 2 == 0 else PatternFill(fill_type=None))
    for col_idx, val in enumerate(r, 1):
        cell = ws4.cell(row=row_idx, column=col_idx, value=val)
        cell.font = bold_font if col_idx in [1, 2, 5, 6] else normal_font
        cell.border = thin_border
        cell.fill = fill
        if col_idx in [3, 4, 7]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif col_idx in [5, 6]:
            cell.alignment = Alignment(horizontal="right", vertical="center")
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")

# Auto-adjust column widths across all sheets
for ws in [ws1, ws2, ws3, ws4]:
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or '')
            if cell.row in [1, 2]: # skip title rows for width calculation
                continue
            if len(val_str) > max_len:
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 48)

wb.save(output_path)
print(f"Audit workbook saved successfully to: {output_path}")

