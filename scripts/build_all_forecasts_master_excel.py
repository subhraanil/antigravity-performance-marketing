import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import shutil

wb = openpyxl.Workbook()

# Setup styles
font_family = "Calibri"
navy_fill = PatternFill(start_color="102C57", end_color="102C57", fill_type="solid")
header_fill = PatternFill(start_color="164863", end_color="164863", fill_type="solid")
sub_header_fill = PatternFill(start_color="427D9D", end_color="427D9D", fill_type="solid")
baseline_fill = PatternFill(start_color="F2F4F4", end_color="F2F4F4", fill_type="solid")
zebra_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
total_fill = PatternFill(start_color="EAEDED", end_color="EAEDED", fill_type="solid")
highlight_fill = PatternFill(start_color="E8F8F5", end_color="E8F8F5", fill_type="solid")

header_font = Font(name=font_family, size=10, bold=True, color="FFFFFF")
sub_header_font = Font(name=font_family, size=10, bold=True, color="FFFFFF")
baseline_font = Font(name=font_family, size=10, italic=True, color="4A5568")
cell_font = Font(name=font_family, size=10, color="000000")
total_font = Font(name=font_family, size=10, bold=True, color="102C57")
title_font = Font(name=font_family, size=13, bold=True, color="102C57")
subtitle_font = Font(name=font_family, size=9.5, italic=True, color="718096")

thin_gray = Side(style='thin', color="CBD5E0")
border_cell = Border(left=thin_gray, right=thin_gray, top=thin_gray, bottom=thin_gray)
double_bottom = Side(style='double', color="102C57")
border_total = Border(left=thin_gray, right=thin_gray, top=thin_gray, bottom=double_bottom)

# ===========================================================================
# SHEET 1: EXECUTIVE OVERVIEW & SCENARIO COMPARISON
# ===========================================================================
ws1 = wb.active
ws1.title = "Executive Overview"
ws1.views.sheetView[0].showGridLines = True

ws1.cell(row=1, column=1, value="FABB6 (Glanzzkart Pvt Ltd) — Master Forecast & Turnaround Financial Model").font = title_font
ws1.cell(row=2, column=1, value="Consolidated Comparative Scenarios: Historic Baseline vs Past 4 Proposed Plans vs New Conservative 3-Month Plan vs 6-Month Scale").font = subtitle_font

headers_ws1 = [
    "Scenario / Forecast Model", "Strategic Classification", "Timeline", 
    "Total Ad Spend (₹)", "Paid Orders", "Paid CPA (₹)", "Paid Revenue (₹)", "Paid ROAS", 
    "Organic & Repeat Orders", "Total Store Orders", "Daily Orders", "Total Net Revenue (₹)", "Store Blended ROAS"
]

for col_idx, h in enumerate(headers_ws1, 1):
    c = ws1.cell(row=4, column=col_idx, value=h)
    c.fill = header_fill
    c.font = header_font
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = border_cell
ws1.row_dimensions[4].height = 28

overview_rows = [
    ("August 2026 Actuals", "Proven Historical Baseline (Pre-Competitor)", "Aug 2026", 3000000, 8953, 335.08, 12506000, 4.17, 5047, 14000, 452, 18760000, 6.25),
    ("November 2026 Run-Rate", "Current Competitor Damage Baseline", "Nov 2026", 3145000, 7176, 438.27, 10008500, 3.18, 4163, 11339, 378, 15636000, 4.97),
    ("Plan - A (Past Proposal)", "Aggressive Sprint (1500 orders/day)", "6 Months", 45000000, 168000, 267.86, 235200000, 5.23, 102000, 270000, 1500, 378000000, 8.40),
    ("Plan - C (Past Proposal)", "Step-Up Efficiency Model (30L to 35L)", "6 Months", 19500000, 54500, 357.80, 76300000, 3.91, 35500, 90000, 500, 126000000, 6.46),
    ("Plan - C.1 (Past Proposal)", "Conservative Step-Up (30L flat)", "6 Months", 18000000, 48000, 375.00, 67200000, 3.73, 32000, 80000, 444, 112000000, 6.22),
    ("Plan - B (Past Proposal)", "Aggressive Scaling (50L Step-Up)", "6 Months", 30000000, 92000, 326.09, 128800000, 4.29, 58000, 150000, 833, 210000000, 7.00),
    ("Calibrated 3-Month Plan (Recommended)", "Q1 2027 Structured Turnaround Plan", "Dec 2026 - Feb 2027", 9600000, 26045, 368.59, 36332775, 3.78, 13400, 39445, 438, 55025775, 5.73),
    ("Scaled 6-Month Turnaround Model", "Phase-Gated Omnichannel Compounding", "Dec 2026 - May 2027", 25500000, 90500, 281.77, 117412245, 4.60, 31500, 122000, 674, 168438000, 6.61),
]

for row_idx, r_data in enumerate(overview_rows, 5):
    for col_idx, val in enumerate(r_data, 1):
        c = ws1.cell(row=row_idx, column=col_idx, value=val)
        c.border = border_cell
        c.font = cell_font
        if row_idx in [5, 6]:
            c.fill = baseline_fill
            c.font = baseline_font
        elif row_idx == 11:
            c.fill = highlight_fill
            c.font = total_font
        elif row_idx % 2 == 1:
            c.fill = zebra_fill
            
        # Formatting
        if col_idx in [1, 2]:
            c.alignment = Alignment(horizontal="left", vertical="center")
        elif col_idx == 3:
            c.alignment = Alignment(horizontal="center", vertical="center")
        elif col_idx in [4, 7, 12]:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '"₹"#,##0'
        elif col_idx in [5, 9, 10, 11]:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = '#,##0'
        elif col_idx == 6:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '"₹"#,##0.00'
        elif col_idx in [8, 13]:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = '0.00"x"'
    ws1.row_dimensions[row_idx].height = 22

# ===========================================================================
# SHEET 2: CONSERVATIVE 3M - BLENDED STORE FORECAST
# ===========================================================================
ws2 = wb.create_sheet(title="3-Month Plan - Blended")
ws2.views.sheetView[0].showGridLines = True

ws2.cell(row=1, column=1, value="FABB6 — Calibrated 3-Month Blended Store Turnaround Forecast").font = title_font
ws2.cell(row=2, column=1, value="Phased Performance Model: Waste elimination, CPA normalization, and profitable order scaling").font = subtitle_font

headers_ws2 = [
    "Month", "Operational Phase / Strategy", 
    "Google Spend (₹)", "Meta Spend (₹)", "Total Paid Spend (₹)",
    "Google Orders", "Meta Orders", "Total Paid Orders", "Blended Paid CPA (₹)", "Paid Revenue (₹)", "Paid ROAS",
    "Organic & Repeat Orders", "Repeat Share (%)", "Total Store Orders", "Daily Store Orders",
    "Total Net Revenue (₹)", "Store Blended CPA (₹)", "Store Blended ROAS"
]

for col_idx, h in enumerate(headers_ws2, 1):
    c = ws2.cell(row=4, column=col_idx, value=h)
    c.fill = header_fill
    c.font = header_font
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = border_cell
ws2.row_dimensions[4].height = 28

rows_ws2 = [
    ("Nov 2026 (Run-Rate)", "Baseline (Competitor Damage Period)", 345000, 2800000, 3145000, 1010, 6166, 7176, 438.27, 10008500, 3.18, 4163, 0.367, 11339, 378, 15636000, 277.36, 4.97),
    ("Dec 2026 (M1)", "Triage: 404 Purge, Glam+ Deletion, DPA Negatives", 400000, 2600000, 3000000, 1270, 6265, 7535, 398.14, 10511325, 3.50, 4200, 0.358, 11735, 379, 16370325, 255.65, 5.46),
    ("Jan 2027 (M2)", "Rebuild: Advantage+ Catalog, Search Hygiene, PMax", 450000, 2750000, 3200000, 1525, 7143, 8668, 369.17, 12091860, 3.78, 4450, 0.339, 13118, 423, 18299610, 243.94, 5.72),
    ("Feb 2027 (M3)", "Restoration: Return to August 2026 Baseline Efficiency", 500000, 2900000, 3400000, 1786, 8056, 9842, 345.46, 13729590, 4.04, 4750, 0.325, 14592, 521, 20355840, 233.00, 5.99),
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
    ws2.row_dimensions[row_idx].height = 22

# Totals row
tot_row = 9
ws2.cell(row=tot_row, column=1, value="3-Month Total (Dec-Feb)")
ws2.cell(row=tot_row, column=2, value="Q1 2027 Cumulative Turnaround Plan")
ws2.cell(row=tot_row, column=3, value=1350000)
ws2.cell(row=tot_row, column=4, value=8250000)
ws2.cell(row=tot_row, column=5, value=9600000)
ws2.cell(row=tot_row, column=6, value=4581)
ws2.cell(row=tot_row, column=7, value=21464)
ws2.cell(row=tot_row, column=8, value=26045)
ws2.cell(row=tot_row, column=9, value=368.59)
ws2.cell(row=tot_row, column=10, value=36332775)
ws2.cell(row=tot_row, column=11, value=3.78)
ws2.cell(row=tot_row, column=12, value=13400)
ws2.cell(row=tot_row, column=13, value=0.340)
ws2.cell(row=tot_row, column=14, value=39445)
ws2.cell(row=tot_row, column=15, value=438)
ws2.cell(row=tot_row, column=16, value=55025775)
ws2.cell(row=tot_row, column=17, value=243.38)
ws2.cell(row=tot_row, column=18, value=5.73)

for col_idx in range(1, 19):
    c = ws2.cell(row=tot_row, column=col_idx)
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
ws2.row_dimensions[tot_row].height = 24

# ===========================================================================
# SHEET 3: CONSERVATIVE 3M - GOOGLE ADS
# ===========================================================================
ws3 = wb.create_sheet(title="3-Month Plan - Google Ads")
ws3.views.sheetView[0].showGridLines = True

ws3.cell(row=1, column=1, value="FABB6 — Google Ads 3-Month Performance Recovery Forecast").font = title_font
ws3.cell(row=2, column=1, value="Optimization: Exclude 110 Broken 404 URLs, Purge 'Glam+' Assets, Rebuild Smart Bidding (Dec 2026 – Feb 2027)").font = subtitle_font

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
    ("Nov 2026 (Run-Rate)", "Baseline: PMax suffering from 110 broken 404 URLs & 'Glam+' copy", 345000, 11500, 341.65, 1010, 34, 1393, 1406930, 4.08, 0.0, 0.0),
    ("Dec 2026 (M1)", "Triage: Exclude 110 404 URLs, purge Glam+ copy, re-align PMax assets", 400000, 12903, 315.00, 1270, 41, 1395, 1771650, 4.43, -0.078, 0.257),
    ("Jan 2027 (M2)", "Feed & Asset Refresh: High-margin SKU prioritization, search negative hygiene", 450000, 14516, 295.00, 1525, 49, 1395, 2127375, 4.73, -0.137, 0.201),
    ("Feb 2027 (M3)", "Restoration: Non-brand search expansion, returning to August CPA benchmark", 500000, 17857, 280.00, 1786, 64, 1395, 2491470, 4.98, -0.180, 0.171),
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

tot_row_g = 9
ws3.cell(row=tot_row_g, column=1, value="3-Month Total (Dec-Feb)")
ws3.cell(row=tot_row_g, column=2, value="Disciplined PMax & Search Restructuring")
ws3.cell(row=tot_row_g, column=3, value=1350000)
ws3.cell(row=tot_row_g, column=4, value=15000)
ws3.cell(row=tot_row_g, column=5, value=294.70)
ws3.cell(row=tot_row_g, column=6, value=4581)
ws3.cell(row=tot_row_g, column=7, value=51)
ws3.cell(row=tot_row_g, column=8, value=1395)
ws3.cell(row=tot_row_g, column=9, value=6390495)
ws3.cell(row=tot_row_g, column=10, value=4.73)
ws3.cell(row=tot_row_g, column=11, value=-0.137)
ws3.cell(row=tot_row_g, column=12, value=0.768)

for col_idx in range(1, 13):
    c = ws3.cell(row=tot_row_g, column=col_idx)
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
ws3.row_dimensions[tot_row_g].height = 24

# ===========================================================================
# SHEET 4: CONSERVATIVE 3M - META ADS
# ===========================================================================
ws4 = wb.create_sheet(title="3-Month Plan - Meta Ads")
ws4.views.sheetView[0].showGridLines = True

ws4.cell(row=1, column=1, value="FABB6 — Meta Ads 3-Month Performance Recovery Forecast").font = title_font
ws4.cell(row=2, column=1, value="Optimization: Cut ₹50K Dead Traffic Ad, Fix Retargeting CPA Inversion with 30-Day Customer Exclusions (Dec 2026 – Feb 2027)").font = subtitle_font

headers_ws4 = [
    "Month", "Strategic Focus & Key Tactics", 
    "Monthly Budget (₹)", "Daily Budget (₹)", "Target CPA (₹)", "Orders / Purchases", 
    "Daily Orders", "Average Order Value (AOV)", "Conversion Value / Revenue (₹)", "ROAS", 
    "CPA Improvement vs Baseline", "Order Growth MoM"
]

for col_idx, h in enumerate(headers_ws4, 1):
    c = ws4.cell(row=4, column=col_idx, value=h)
    c.fill = header_fill
    c.font = header_font
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = border_cell
ws4.row_dimensions[4].height = 28

rows_ws4 = [
    ("Nov 2026 (Run-Rate)", "Baseline: DPA inverted at ₹513 CPA, ₹50k burned on 99.97% drop-off traffic ad", 2800000, 93333, 454.10, 6166, 206, 1395, 8601570, 3.07, 0.0, 0.0),
    ("Dec 2026 (M1)", "Triage: Kill traffic ad, pause zombie app ads, enforce 30-day exclusions on DPA", 2600000, 83871, 415.00, 6265, 202, 1395, 8739675, 3.36, -0.086, 0.016),
    ("Jan 2027 (M2)", "Restructure: Advantage+ Shopping consolidation, fresh creative testing batch (10 UGC)", 2750000, 88710, 385.00, 7143, 230, 1395, 9964485, 3.62, -0.152, 0.140),
    ("Feb 2027 (M3)", "Restoration: Scaling winning ad angles, returning near August CPA benchmark (₹343)", 2900000, 103571, 360.00, 8056, 288, 1395, 11238120, 3.88, -0.207, 0.128),
]

for row_idx, r_data in enumerate(rows_ws4, 5):
    for col_idx, val in enumerate(r_data, 1):
        c = ws4.cell(row=row_idx, column=col_idx, value=val)
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
    ws4.row_dimensions[row_idx].height = 22

tot_row_m = 9
ws4.cell(row=tot_row_m, column=1, value="3-Month Total (Dec-Feb)")
ws4.cell(row=tot_row_m, column=2, value="Advantage+ Consolidation & Creative Velocity")
ws4.cell(row=tot_row_m, column=3, value=8250000)
ws4.cell(row=tot_row_m, column=4, value=91667)
ws4.cell(row=tot_row_m, column=5, value=384.36)
ws4.cell(row=tot_row_m, column=6, value=21464)
ws4.cell(row=tot_row_m, column=7, value=238)
ws4.cell(row=tot_row_m, column=8, value=1395)
ws4.cell(row=tot_row_m, column=9, value=29942280)
ws4.cell(row=tot_row_m, column=10, value=3.63)
ws4.cell(row=tot_row_m, column=11, value=-0.154)
ws4.cell(row=tot_row_m, column=12, value=0.307)

for col_idx in range(1, 13):
    c = ws4.cell(row=tot_row_m, column=col_idx)
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
ws4.row_dimensions[tot_row_m].height = 24

# ===========================================================================
# SHEET 5: SCALED 6-MONTH TURNAROUND MODEL
# ===========================================================================
ws5 = wb.create_sheet(title="Scaled 6M Turnaround Model")
ws5.views.sheetView[0].showGridLines = True

ws5.cell(row=1, column=1, value="FABB6 — Scaled 6-Month Turnaround Financial Model (Dec 2026 – May 2027)").font = title_font
ws5.cell(row=2, column=1, value="Strategic Scaling: Triage in M1, Advantage+ consolidation in M2, scaling to 1,000 orders/day by Month 6").font = subtitle_font

headers_ws5 = [
    "Month", "Strategic Scaling Phase", "Google Spend (₹)", "Meta Spend (₹)", "Total Paid Spend (₹)",
    "Paid CPA (₹)", "Paid Orders", "Organic/Repeat Orders", "Total Store Orders", "Daily Orders",
    "Net Revenue (₹)", "Blended Net ROAS"
]

for col_idx, h in enumerate(headers_ws5, 1):
    c = ws5.cell(row=4, column=col_idx, value=h)
    c.fill = header_fill
    c.font = header_font
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = border_cell
ws5.row_dimensions[4].height = 28

rows_ws5 = [
    ("Dec 2026", "M1: Triage & Waste Purging", 400000, 2600000, 3000000, 348.84, 8600, 3800, 12400, 400, 11197200, 3.73),
    ("Jan 2027", "M2: Retention & PMax Rebuild", 500000, 3000000, 3500000, 318.18, 11000, 4200, 15200, 490, 14057340, 4.02),
    ("Feb 2027", "M3: Scaled Prospecting", 600000, 3400000, 4000000, 294.12, 13600, 4900, 18500, 661, 17403525, 4.35),
    ("Mar 2027", "M4: Creative Velocity", 750000, 3750000, 4500000, 277.78, 16200, 5800, 22000, 710, 21056805, 4.68),
    ("Apr 2027", "M5: Omnichannel Compounding", 850000, 4150000, 5000000, 265.96, 18800, 6700, 25500, 850, 24718050, 4.94),
    ("May 2027", "M6: Scale Peak (1,000/day)", 1000000, 4500000, 5500000, 255.81, 21500, 8000, 29500, 983, 28979325, 5.27),
]

for row_idx, r_data in enumerate(rows_ws5, 5):
    for col_idx, val in enumerate(r_data, 1):
        c = ws5.cell(row=row_idx, column=col_idx, value=val)
        c.font = cell_font
        if row_idx % 2 == 1:
            c.fill = zebra_fill
        c.border = border_cell
        
        # Formatting
        if col_idx in [1, 2]:
            c.alignment = Alignment(horizontal="left", vertical="center")
        elif col_idx in [3, 4, 5, 11]:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '"₹"#,##0'
        elif col_idx in [7, 8, 9, 10]:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = '#,##0'
        elif col_idx == 6:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '"₹"#,##0.00'
        elif col_idx == 12:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = '0.00"x"'
    ws5.row_dimensions[row_idx].height = 22

tot_row_s6 = 11
ws5.cell(row=tot_row_s6, column=1, value="6-Month Total (Dec-May)")
ws5.cell(row=tot_row_s6, column=2, value="H1 2027 Scaled Turnaround")
ws5.cell(row=tot_row_s6, column=3, value=4100000)
ws5.cell(row=tot_row_s6, column=4, value=21400000)
ws5.cell(row=tot_row_s6, column=5, value=25500000)
ws5.cell(row=tot_row_s6, column=6, value=281.77)
ws5.cell(row=tot_row_s6, column=7, value=90500)
ws5.cell(row=tot_row_s6, column=8, value=31500)
ws5.cell(row=tot_row_s6, column=9, value=122000)
ws5.cell(row=tot_row_s6, column=10, value=674)
ws5.cell(row=tot_row_s6, column=11, value=117412245)
ws5.cell(row=tot_row_s6, column=12, value=4.60)

for col_idx in range(1, 13):
    c = ws5.cell(row=tot_row_s6, column=col_idx)
    c.fill = total_fill
    c.font = total_font
    c.border = border_total
    if col_idx in [1, 2]:
        c.alignment = Alignment(horizontal="left", vertical="center")
    elif col_idx in [3, 4, 5, 11]:
        c.alignment = Alignment(horizontal="right", vertical="center")
        c.number_format = '"₹"#,##0'
    elif col_idx in [7, 8, 9, 10]:
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.number_format = '#,##0'
    elif col_idx == 6:
        c.alignment = Alignment(horizontal="right", vertical="center")
        c.number_format = '"₹"#,##0.00'
    elif col_idx == 12:
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.number_format = '0.00"x"'
ws5.row_dimensions[tot_row_s6].height = 24

# ===========================================================================
# SHEET 6: PAST 4 FORECASTS VS ACTUALS EVALUATION
# ===========================================================================
ws6 = wb.create_sheet(title="Past 4 Forecasts vs Actuals")
ws6.views.sheetView[0].showGridLines = True

ws6.cell(row=1, column=1, value="FABB6 — Evaluation of Past 4 Proposed Plans vs Actual Performance").font = title_font
ws6.cell(row=2, column=1, value="Forensic Comparison: Plan A (1500/day Sprint), Plan C (30L Step-Up), Plan C.1 (30L Flat), Plan B (50L Step-Up) vs Actuals").font = subtitle_font

headers_ws6 = [
    "Month / Period", "Metric Category", 
    "Actual Delivered", "Plan - A (1500 Orders)", "Plan - C (30L Step-Up)", "Plan - C.1 (30L Flat)", "Plan - B (50L Step-Up)",
    "Variance vs Plan C (%)", "Diagnostic Root-Cause Analysis"
]

for col_idx, h in enumerate(headers_ws6, 1):
    c = ws6.cell(row=4, column=col_idx, value=h)
    c.fill = header_fill
    c.font = header_font
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = border_cell
ws6.row_dimensions[4].height = 28

rows_ws6 = [
    ("September 2026", "Total Paid Ad Spend (₹)", 3049103, 7500000, 3000000, 3000000, 5000000, 0.016, "Spend matched Plan C budget, but delivered 0 Google sales due to deleted conversion action"),
    ("September 2026", "Paid Orders Delivered", 7185, 23077, 8571, 7500, 13889, -0.162, "Orders trailed Plan C by 16.2% due to Google PMax blackout (only 42 orders on 3.18L spend)"),
    ("September 2026", "Blended Paid CPA (₹)", 424.36, 325.00, 350.00, 400.00, 360.00, 0.212, "CPA inflated by +21.2% above Plan C target due to wasted Google spend at 7,569 CPA"),
    ("September 2026", "Total Store Orders (Shopify)", 11260, 45000, 15000, 13333, 25000, -0.249, "Trailing Plan C by 24.9%; organic repeat rate held at 36.2% but paid acquisition lagged"),
    
    ("October 2026", "Total Paid Ad Spend (₹)", 4246944, 7500000, 3000000, 3000000, 5000000, 0.416, "Competitor overspent by +41.6% (₹12.47L excess) trying to force Diwali volume"),
    ("October 2026", "Paid Orders Delivered", 7298, 24000, 7878, 8000, 14286, -0.074, "Orders within 7.4% of Plan C target! Shows account volume capacity was sound"),
    ("October 2026", "Blended Paid CPA (₹)", 581.84, 312.50, 380.81, 375.00, 350.00, 0.528, "Catastrophic CPA inflation (+52.8% vs Plan C); burned cash on inverted DPA and dead clicks"),
    ("October 2026", "Total Store Orders (Shopify)", 11540, 45000, 15000, 13333, 25000, -0.231, "Shopify orders stalled at 372/day despite 42.47L paid media burn"),
    
    ("November 2026 (Run-Rate)", "Total Paid Ad Spend (₹)", 3148000, 7500000, 3200000, 3000000, 5000000, -0.016, "Pacing closely tracks Plan C Month 3 budget (32.0L)"),
    ("November 2026 (Run-Rate)", "Paid Orders Delivered", 7183, 25000, 8206, 8500, 14706, -0.125, "Paid orders within 12.5% of Plan C target, confirming predictable baseline capacity"),
    ("November 2026 (Run-Rate)", "Blended Paid CPA (₹)", 438.28, 300.00, 389.96, 352.94, 340.00, 0.124, "CPA still +12.4% inflated vs Plan C due to 110 broken 404 URLs and dead IG-traffic campaign"),
    ("November 2026 (Run-Rate)", "Total Store Orders (Shopify)", 11346, 45000, 15000, 13333, 25000, -0.244, "Stalled at 378 orders/day; requires waste purge to unlock profitable growth")
]

for row_idx, r_data in enumerate(rows_ws6, 5):
    for col_idx, val in enumerate(r_data, 1):
        c = ws6.cell(row=row_idx, column=col_idx, value=val)
        c.font = cell_font
        if row_idx in [5, 9, 13]:
            c.fill = zebra_fill
        c.border = border_cell
        
        # Formatting
        if col_idx in [1, 2, 9]:
            c.alignment = Alignment(horizontal="left", vertical="center")
        elif col_idx in [3, 4, 5, 6, 7]:
            if "Spend" in str(r_data[1]):
                c.alignment = Alignment(horizontal="right", vertical="center")
                c.number_format = '"₹"#,##0'
            elif "CPA" in str(r_data[1]):
                c.alignment = Alignment(horizontal="right", vertical="center")
                c.number_format = '"₹"#,##0.00'
            else:
                c.alignment = Alignment(horizontal="center", vertical="center")
                c.number_format = '#,##0'
        elif col_idx == 8:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = '+0.0%;-0.0%;"0.0%"'
    ws6.row_dimensions[row_idx].height = 22

# ===========================================================================
# SHEET 7: 12-MONTH HISTORICAL BASELINE (DEC 2025 - NOV 2026)
# ===========================================================================
ws7 = wb.create_sheet(title="12-Month Historical Baseline")
ws7.views.sheetView[0].showGridLines = True

ws7.cell(row=1, column=1, value="FABB6 — 12-Month Historical Store & Paid Performance Audit (Dec 2025 – Nov 2026)").font = title_font
ws7.cell(row=2, column=1, value="Longitudinal Trends: Shopify Gross/Net Sales, Google Ads, Meta Ads, Blended CPA, and ROAS Trajectory").font = subtitle_font

headers_ws7 = [
    "Month", "Managing Agency", "Google Spend (₹)", "Meta Spend (₹)", "Total Paid Spend (₹)",
    "Paid Purchases", "Blended Paid CPA (₹)", "Paid Conversion Value (₹)", "Paid ROAS",
    "Shopify Total Orders", "Shopify Daily Orders", "Shopify Gross Sales (₹)", "Shopify Net Sales (₹)", "Store Blended ROAS"
]

for col_idx, h in enumerate(headers_ws7, 1):
    c = ws7.cell(row=4, column=col_idx, value=h)
    c.fill = header_fill
    c.font = header_font
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = border_cell
ws7.row_dimensions[4].height = 28

rows_ws7 = [
    ("Dec 2025", "Prior Agency", 185000, 1540000, 1725000, 4850, 355.67, 7250000, 4.20, 8100, 261, 12500000, 10800000, 6.26),
    ("Jan 2026", "Prior Agency", 210000, 1720000, 1930000, 5320, 362.78, 7980000, 4.13, 8900, 287, 13800000, 11950000, 6.19),
    ("Feb 2026", "Prior Agency", 225000, 1850000, 2075000, 5890, 352.29, 8820000, 4.25, 9600, 343, 14900000, 12900000, 6.22),
    ("Mar 2026", "Prior Agency", 240000, 1980000, 2220000, 6150, 360.98, 9210000, 4.15, 10100, 326, 15700000, 13600000, 6.13),
    ("Apr 2026", "Prior Agency", 260000, 2150000, 2410000, 6800, 354.41, 10180000, 4.22, 11050, 368, 17200000, 14900000, 6.18),
    ("May 2026", "Prior Agency", 280000, 2300000, 2580000, 7120, 362.36, 10650000, 4.13, 11500, 371, 17900000, 15500000, 6.01),
    ("Jun 2026", "Prior Agency", 295000, 2420000, 2715000, 7450, 364.43, 11150000, 4.11, 12050, 402, 18800000, 16250000, 5.99),
    ("Jul 2026", "Prior Agency", 320000, 2550000, 2870000, 7850, 365.61, 11750000, 4.09, 12700, 410, 19800000, 17100000, 5.96),
    ("Aug 2026", "Proven Baseline", 344199, 2655801, 3000000, 8953, 335.08, 12506000, 4.17, 14000, 452, 21800000, 18760000, 6.25),
    ("Sep 2026", "SilverXis (Failure)", 317895, 2731208, 3049103, 7185, 424.36, 9772000, 3.20, 11260, 375, 17680000, 15200000, 4.99),
    ("Oct 2026", "SilverXis (Failure)", 375990, 3870954, 4246944, 7298, 581.84, 11123000, 2.62, 11540, 372, 18560000, 15980000, 3.76),
    ("Nov 2026 (Run-Rate)", "SilverXis (Current)", 345000, 2800000, 3145000, 7176, 438.27, 10008500, 3.18, 11339, 378, 18150000, 15636000, 4.97)
]

for row_idx, r_data in enumerate(rows_ws7, 5):
    for col_idx, val in enumerate(r_data, 1):
        c = ws7.cell(row=row_idx, column=col_idx, value=val)
        c.font = cell_font
        if "SilverXis" in str(r_data[1]):
            c.fill = PatternFill(start_color="FDEDEC", end_color="FDEDEC", fill_type="solid")
        elif "Proven" in str(r_data[1]):
            c.fill = highlight_fill
            c.font = Font(name=font_family, size=10, bold=True, color="102C57")
        elif row_idx % 2 == 1:
            c.fill = zebra_fill
        c.border = border_cell
        
        # Formatting
        if col_idx in [1, 2]:
            c.alignment = Alignment(horizontal="left", vertical="center")
        elif col_idx in [3, 4, 5, 8, 12, 13]:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '"₹"#,##0'
        elif col_idx in [6, 10, 11]:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = '#,##0'
        elif col_idx == 7:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '"₹"#,##0.00'
        elif col_idx in [9, 14]:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = '0.00"x"'
    ws7.row_dimensions[row_idx].height = 22

# Auto-fit column widths across all sheets
for ws in [ws1, ws2, ws3, ws4, ws5, ws6, ws7]:
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
ws1.column_dimensions['A'].width = 32
ws1.column_dimensions['B'].width = 38
ws2.column_dimensions['A'].width = 20
ws2.column_dimensions['B'].width = 38
ws3.column_dimensions['A'].width = 20
ws3.column_dimensions['B'].width = 44
ws4.column_dimensions['A'].width = 20
ws4.column_dimensions['B'].width = 44
ws5.column_dimensions['A'].width = 20
ws5.column_dimensions['B'].width = 32
ws6.column_dimensions['A'].width = 22
ws6.column_dimensions['B'].width = 26
ws6.column_dimensions['I'].width = 55
ws7.column_dimensions['A'].width = 20
ws7.column_dimensions['B'].width = 24

output_path = r"C:\Users\test\Videos\Office\reports\FABB6_All_Forecasts_and_Turnaround_Master_Model.xlsx"
wb.save(output_path)
print(f"Saved master all-forecasts workbook to: {output_path}")

case_study_path = r"C:\Users\test\Videos\Office\case-studies\fabb6\FABB6_All_Forecasts_and_Turnaround_Master_Model.xlsx"
shutil.copyfile(output_path, case_study_path)
print(f"Copied to case studies: {case_study_path}")

artifact_path = r"C:\Users\test\.gemini\antigravity\brain\29f77e0a-5ed5-4d24-842c-443d9957274c\FABB6_All_Forecasts_and_Turnaround_Master_Model.xlsx"
shutil.copyfile(output_path, artifact_path)
print(f"Copied to artifacts: {artifact_path}")
