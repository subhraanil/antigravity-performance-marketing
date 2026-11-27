import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import shutil

wb = openpyxl.Workbook()

# Setup styles
font_family = "Calibri"
navy_fill = PatternFill(start_color="102C57", end_color="102C57", fill_type="solid")
header_fill = PatternFill(start_color="164863", end_color="164863", fill_type="solid")
baseline_fill = PatternFill(start_color="F2F4F4", end_color="F2F4F4", fill_type="solid")
zebra_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
total_fill = PatternFill(start_color="EAEDED", end_color="EAEDED", fill_type="solid")

header_font = Font(name=font_family, size=10, bold=True, color="FFFFFF")
baseline_font = Font(name=font_family, size=10, italic=True, color="4A5568")
cell_font = Font(name=font_family, size=10, color="000000")
total_font = Font(name=font_family, size=10, bold=True, color="102C57")
title_font = Font(name=font_family, size=14, bold=True, color="102C57")
subtitle_font = Font(name=font_family, size=10, italic=True, color="718096")

thin_gray = Side(style='thin', color="CBD5E0")
border_cell = Border(left=thin_gray, right=thin_gray, top=thin_gray, bottom=thin_gray)
double_bottom = Side(style='double', color="102C57")
border_total = Border(left=thin_gray, right=thin_gray, top=thin_gray, bottom=double_bottom)

# ---------------------------------------------------------------------------
# SHEET 1: BLENDED & TOTAL STORE 3-MONTH FORECAST
# ---------------------------------------------------------------------------
ws1 = wb.active
ws1.title = "Blended Store 3M Forecast"
ws1.views.sheetView[0].showGridLines = True

ws1.cell(row=1, column=1, value="FABB6 (Glanzzkart Pvt Ltd) — Conservative 3-Month Turnaround Forecast").font = title_font
ws1.cell(row=2, column=1, value="De-risked Low-Growth Financial Model: Google Ads + Meta Ads + Organic/Repeat (Dec 2026 – Feb 2027)").font = subtitle_font

headers_ws1 = [
    "Month", "Operational Phase / Strategy", 
    "Google Spend (₹)", "Meta Spend (₹)", "Total Paid Spend (₹)",
    "Google Orders", "Meta Orders", "Total Paid Orders", "Blended Paid CPA (₹)", "Paid Revenue (₹)", "Paid ROAS",
    "Organic & Repeat Orders", "Repeat Share (%)", "Total Store Orders", "Daily Store Orders",
    "Total Net Revenue (₹)", "Store Blended CPA (₹)", "Store Blended ROAS"
]

for col_idx, h in enumerate(headers_ws1, 1):
    c = ws1.cell(row=4, column=col_idx, value=h)
    c.fill = header_fill
    c.font = header_font
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = border_cell
ws1.row_dimensions[4].height = 28

rows_ws1 = [
    ("Nov 2026 (Run-Rate)", "Baseline (Competitor Damage Period)", 345000, 2800000, 3145000, 1010, 6166, 7176, 438.27, 10008500, 3.18, 4163, 0.367, 11339, 378, 15636000, 277.36, 4.97),
    ("Dec 2026 (M1)", "Triage: 404 Purge, Glam+ Deletion, DPA Negatives", 400000, 2600000, 3000000, 1270, 6265, 7535, 398.14, 10511325, 3.50, 4200, 0.358, 11735, 379, 16370325, 255.65, 5.46),
    ("Jan 2027 (M2)", "Rebuild: Advantage+ Catalog, Search Hygiene, PMax", 450000, 2750000, 3200000, 1525, 7143, 8668, 369.17, 12091860, 3.78, 4450, 0.339, 13118, 423, 18299610, 243.94, 5.72),
    ("Feb 2027 (M3)", "Restoration: Return to August 2026 Baseline Efficiency", 500000, 2900000, 3400000, 1786, 8056, 9842, 345.46, 13729590, 4.04, 4750, 0.325, 14592, 521, 20355840, 233.00, 5.99),
]

for row_idx, r_data in enumerate(rows_ws1, 5):
    for col_idx, val in enumerate(r_data, 1):
        c = ws1.cell(row=row_idx, column=col_idx, value=val)
        c.font = baseline_font if row_idx == 5 else cell_font
        if row_idx == 5:
            c.fill = baseline_fill
        elif row_idx % 2 == 1:
            c.fill = zebra_fill
        c.border = border_cell
        
        # Formatting
        if col_idx in [1, 2]:
            c.alignment = Alignment(horizontal="left", vertical="center")
        elif col_idx in [3, 4, 5, 10, 16]:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '"₹"#,##0'
        elif col_idx in [6, 7, 8, 12, 14, 15]:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = '#,##0'
        elif col_idx in [9, 17]:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '"₹"#,##0.00'
        elif col_idx in [11, 18]:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = '0.00"x"'
        elif col_idx == 13:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = '0.0%'
    ws1.row_dimensions[row_idx].height = 22

# Totals row for 3-Month Plan (Dec, Jan, Feb)
tot_row = 9
ws1.cell(row=tot_row, column=1, value="3-Month Total (Dec-Feb)")
ws1.cell(row=tot_row, column=2, value="Cumulative Low-Risk Recovery Plan")
ws1.cell(row=tot_row, column=3, value=1350000)
ws1.cell(row=tot_row, column=4, value=8250000)
ws1.cell(row=tot_row, column=5, value=9600000)
ws1.cell(row=tot_row, column=6, value=4581)
ws1.cell(row=tot_row, column=7, value=21464)
ws1.cell(row=tot_row, column=8, value=26045)
ws1.cell(row=tot_row, column=9, value=368.59)
ws1.cell(row=tot_row, column=10, value=36332775)
ws1.cell(row=tot_row, column=11, value=3.78)
ws1.cell(row=tot_row, column=12, value=13400)
ws1.cell(row=tot_row, column=13, value=0.340)
ws1.cell(row=tot_row, column=14, value=39445)
ws1.cell(row=tot_row, column=15, value=438)
ws1.cell(row=tot_row, column=16, value=55025775)
ws1.cell(row=tot_row, column=17, value=243.38)
ws1.cell(row=tot_row, column=18, value=5.73)

for col_idx in range(1, 19):
    c = ws1.cell(row=tot_row, column=col_idx)
    c.fill = total_fill
    c.font = total_font
    c.border = border_total
    if col_idx in [1, 2]:
        c.alignment = Alignment(horizontal="left", vertical="center")
    elif col_idx in [3, 4, 5, 10, 16]:
        c.alignment = Alignment(horizontal="right", vertical="center")
        c.number_format = '"₹"#,##0'
    elif col_idx in [6, 7, 8, 12, 14, 15]:
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.number_format = '#,##0'
    elif col_idx in [9, 17]:
        c.alignment = Alignment(horizontal="right", vertical="center")
        c.number_format = '"₹"#,##0.00'
    elif col_idx in [11, 18]:
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.number_format = '0.00"x"'
    elif col_idx == 13:
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.number_format = '0.0%'
ws1.row_dimensions[tot_row].height = 24

# ---------------------------------------------------------------------------
# SHEET 2: GOOGLE ADS 3-MONTH FORECAST
# ---------------------------------------------------------------------------
ws2 = wb.create_sheet(title="Google Ads 3M Forecast")
ws2.views.sheetView[0].showGridLines = True

ws2.cell(row=1, column=1, value="FABB6 — Google Ads Conservative 3-Month Recovery Forecast").font = title_font
ws2.cell(row=2, column=1, value="Optimization: Purge 110 Broken 404 URLs, Remove 'Glam+' Assets, Rebuild Primary Smart Bidding (Dec 2026 – Feb 2027)").font = subtitle_font

headers_ws2 = [
    "Month", "Strategic Focus & Key Tactics", 
    "Monthly Budget (₹)", "Daily Budget (₹)", "Target CPA (₹)", "Orders / Purchases", 
    "Daily Orders", "Average Order Value (AOV)", "Conversion Value / Revenue (₹)", "ROAS", 
    "CPA Improvement vs Baseline", "Order Growth MoM"
]

for col_idx, h in enumerate(headers_ws2, 1):
    c = ws2.cell(row=4, column=col_idx, value=h)
    c.fill = header_fill
    c.font = header_font
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = border_cell
ws2.row_dimensions[4].height = 28

rows_ws2 = [
    ("Nov 2026 (Run-Rate)", "Baseline: PMax suffering from 110 broken 404 URLs & 'Glam+' copy", 345000, 11500, 341.65, 1010, 34, 1393, 1406930, 4.08, 0.0, 0.0),
    ("Dec 2026 (M1)", "Triage: Exclude 110 404 URLs, purge Glam+ copy, re-align PMax assets", 400000, 12903, 315.00, 1270, 41, 1395, 1771650, 4.43, -0.078, 0.257),
    ("Jan 2027 (M2)", "Feed & Asset Refresh: High-margin SKU prioritization, search negative hygiene", 450000, 14516, 295.00, 1525, 49, 1395, 2127375, 4.73, -0.137, 0.201),
    ("Feb 2027 (M3)", "Restoration: Non-brand search expansion, returning to August CPA benchmark", 500000, 17857, 280.00, 1786, 64, 1395, 2491470, 4.98, -0.180, 0.171),
]

for row_idx, r_data in enumerate(rows_ws2, 5):
    for col_idx, val in enumerate(r_data, 1):
        c = ws2.cell(row=row_idx, column=col_idx, value=val)
        c.font = baseline_font if row_idx == 5 else cell_font
        if row_idx == 5:
            c.fill = baseline_fill
        elif row_idx % 2 == 1:
            c.fill = zebra_fill
        c.border = border_cell
        
        # Formatting
        if col_idx in [1, 2]:
            c.alignment = Alignment(horizontal="left", vertical="center")
        elif col_idx in [3, 4, 8, 9]:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '"₹"#,##0'
        elif col_idx in [6, 7]:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = '#,##0'
        elif col_idx == 5:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '"₹"#,##0.00'
        elif col_idx == 10:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = '0.00"x"'
        elif col_idx in [11, 12]:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = '+0.0%;-0.0%;"0.0%"'
    ws2.row_dimensions[row_idx].height = 22

# Totals row for Google Ads
tot_row_g = 9
ws2.cell(row=tot_row_g, column=1, value="3-Month Total (Dec-Feb)")
ws2.cell(row=tot_row_g, column=2, value="Disciplined PMax & Search Restructuring")
ws2.cell(row=tot_row_g, column=3, value=1350000)
ws2.cell(row=tot_row_g, column=4, value=15000)
ws2.cell(row=tot_row_g, column=5, value=294.70)
ws2.cell(row=tot_row_g, column=6, value=4581)
ws2.cell(row=tot_row_g, column=7, value=51)
ws2.cell(row=tot_row_g, column=8, value=1395)
ws2.cell(row=tot_row_g, column=9, value=6390495)
ws2.cell(row=tot_row_g, column=10, value=4.73)
ws2.cell(row=tot_row_g, column=11, value=-0.137)
ws2.cell(row=tot_row_g, column=12, value=0.768)

for col_idx in range(1, 13):
    c = ws2.cell(row=tot_row_g, column=col_idx)
    c.fill = total_fill
    c.font = total_font
    c.border = border_total
    if col_idx in [1, 2]:
        c.alignment = Alignment(horizontal="left", vertical="center")
    elif col_idx in [3, 4, 8, 9]:
        c.alignment = Alignment(horizontal="right", vertical="center")
        c.number_format = '"₹"#,##0'
    elif col_idx in [6, 7]:
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.number_format = '#,##0'
    elif col_idx == 5:
        c.alignment = Alignment(horizontal="right", vertical="center")
        c.number_format = '"₹"#,##0.00'
    elif col_idx == 10:
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.number_format = '0.00"x"'
    elif col_idx in [11, 12]:
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.number_format = '+0.0%;-0.0%;"0.0%"'
ws2.row_dimensions[tot_row_g].height = 24

# ---------------------------------------------------------------------------
# SHEET 3: META ADS 3-MONTH FORECAST
# ---------------------------------------------------------------------------
ws3 = wb.create_sheet(title="Meta Ads 3M Forecast")
ws3.views.sheetView[0].showGridLines = True

ws3.cell(row=1, column=1, value="FABB6 — Meta Ads Conservative 3-Month Recovery Forecast").font = title_font
ws3.cell(row=2, column=1, value="Optimization: Cut ₹50K Dead Traffic Ad, Fix Retargeting CPA Inversion with 30-Day Customer Exclusions (Dec 2026 – Feb 2027)").font = subtitle_font

headers_ws3 = [
    "Month", "Strategic Focus & Key Tactics", 
    "Monthly Budget (₹)", "Daily Budget (₹)", "Target CPA (₹)", "Orders / Purchases", 
    "Daily Orders", "Average Order Value (AOV)", "Conversion Value / Revenue (₹)", "ROAS", 
    "CPA Improvement vs Baseline", "Order Growth MoM"
]

for col_idx, h in enumerate(headers_ws3, 1):
    c = ws3.cell(row=4, column=col_idx, value=h)
    c.fill = header_fill
    c.font = header_font
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = border_cell
ws3.row_dimensions[4].height = 28

rows_ws3 = [
    ("Nov 2026 (Run-Rate)", "Baseline: DPA inverted at ₹513 CPA, ₹50k burned on 99.97% drop-off traffic ad", 2800000, 93333, 454.10, 6166, 206, 1395, 8601570, 3.07, 0.0, 0.0),
    ("Dec 2026 (M1)", "Triage: Kill IG traffic ad, pause zombie app ads, enforce 30-day exclusions on DPA", 2600000, 83871, 415.00, 6265, 202, 1395, 8739675, 3.36, -0.086, 0.016),
    ("Jan 2027 (M2)", "Restructure: Advantage+ Shopping consolidation, fresh creative testing batch (10 UGC)", 2750000, 88710, 385.00, 7143, 230, 1395, 9964485, 3.62, -0.152, 0.140),
    ("Feb 2027 (M3)", "Restoration: Scaling winning ad angles, returning near August CPA benchmark (₹343)", 2900000, 103571, 360.00, 8056, 288, 1395, 11238120, 3.88, -0.207, 0.128),
]

for row_idx, r_data in enumerate(rows_ws3, 5):
    for col_idx, val in enumerate(r_data, 1):
        c = ws3.cell(row=row_idx, column=col_idx, value=val)
        c.font = baseline_font if row_idx == 5 else cell_font
        if row_idx == 5:
            c.fill = baseline_fill
        elif row_idx % 2 == 1:
            c.fill = zebra_fill
        c.border = border_cell
        
        # Formatting
        if col_idx in [1, 2]:
            c.alignment = Alignment(horizontal="left", vertical="center")
        elif col_idx in [3, 4, 8, 9]:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '"₹"#,##0'
        elif col_idx in [6, 7]:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = '#,##0'
        elif col_idx == 5:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '"₹"#,##0.00'
        elif col_idx == 10:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = '0.00"x"'
        elif col_idx in [11, 12]:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = '+0.0%;-0.0%;"0.0%"'
    ws3.row_dimensions[row_idx].height = 22

# Totals row for Meta Ads
tot_row_m = 9
ws3.cell(row=tot_row_m, column=1, value="3-Month Total (Dec-Feb)")
ws3.cell(row=tot_row_m, column=2, value="Advantage+ Consolidation & Creative Velocity")
ws3.cell(row=tot_row_m, column=3, value=8250000)
ws3.cell(row=tot_row_m, column=4, value=91667)
ws3.cell(row=tot_row_m, column=5, value=384.36)
ws3.cell(row=tot_row_m, column=6, value=21464)
ws3.cell(row=tot_row_m, column=7, value=238)
ws3.cell(row=tot_row_m, column=8, value=1395)
ws3.cell(row=tot_row_m, column=9, value=29942280)
ws3.cell(row=tot_row_m, column=10, value=3.63)
ws3.cell(row=tot_row_m, column=11, value=-0.154)
ws3.cell(row=tot_row_m, column=12, value=0.307)

for col_idx in range(1, 13):
    c = ws3.cell(row=tot_row_m, column=col_idx)
    c.fill = total_fill
    c.font = total_font
    c.border = border_total
    if col_idx in [1, 2]:
        c.alignment = Alignment(horizontal="left", vertical="center")
    elif col_idx in [3, 4, 8, 9]:
        c.alignment = Alignment(horizontal="right", vertical="center")
        c.number_format = '"₹"#,##0'
    elif col_idx in [6, 7]:
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.number_format = '#,##0'
    elif col_idx == 5:
        c.alignment = Alignment(horizontal="right", vertical="center")
        c.number_format = '"₹"#,##0.00'
    elif col_idx == 10:
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.number_format = '0.00"x"'
    elif col_idx in [11, 12]:
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.number_format = '+0.0%;-0.0%;"0.0%"'
ws3.row_dimensions[tot_row_m].height = 24

# Auto-fit column widths across all sheets
for ws in [ws1, ws2, ws3]:
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or '')
            if cell.row in [1, 2]:
                continue
            if len(val_str) > max_len:
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

# Specific tweaks
ws1.column_dimensions['A'].width = 20
ws1.column_dimensions['B'].width = 38
ws2.column_dimensions['A'].width = 20
ws2.column_dimensions['B'].width = 44
ws3.column_dimensions['A'].width = 20
ws3.column_dimensions['B'].width = 44

output_path = r"C:\Users\test\Videos\Office\reports\FABB6_Conservative_3Month_Turnaround_Forecast_Dec2026_Feb2027.xlsx"
wb.save(output_path)
print(f"Saved conservative 3M forecast workbook to: {output_path}")

case_study_path = r"C:\Users\test\Videos\Office\case-studies\fabb6\FABB6_Conservative_3Month_Turnaround_Forecast_Dec2026_Feb2027.xlsx"
shutil.copyfile(output_path, case_study_path)
print(f"Copied to case studies: {case_study_path}")

artifact_path = r"C:\Users\test\.gemini\antigravity\brain\29f77e0a-5ed5-4d24-842c-443d9957274c\FABB6_Conservative_3Month_Turnaround_Forecast_Dec2026_Feb2027.xlsx"
shutil.copyfile(output_path, artifact_path)
print(f"Copied to artifacts: {artifact_path}")
