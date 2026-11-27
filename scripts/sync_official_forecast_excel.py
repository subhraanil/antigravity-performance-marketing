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
highlight_fill = PatternFill(start_color="E8F8F5", end_color="E8F8F5", fill_type="solid")

header_font = Font(name=font_family, size=10, bold=True, color="FFFFFF")
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
ws1.cell(row=2, column=1, value="Updated with Corrected August Baseline and Official 3-Month Performance Forecast (Dec 2026 – Feb 2027)").font = subtitle_font

headers_ws1 = [
    "Scenario / Forecast Model", "Strategic Classification", "Timeline", 
    "Total Ad Spend (₹)", "Paid Orders", "Paid CPA (₹)", "Paid Revenue (₹)", "Paid ROAS", 
    "Organic & Repeat Orders", "Total Store Orders", "Daily Orders", "Total Gross Revenue (₹)", "Store Blended ROAS"
]

for col_idx, h in enumerate(headers_ws1, 1):
    c = ws1.cell(row=4, column=col_idx, value=h)
    c.fill = header_fill
    c.font = header_font
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = border_cell
ws1.row_dimensions[4].height = 28

overview_rows = [
    ("August 2026 (Corrected)", "Pre-Competitor Peak (Data Glitch Removed)", "Aug 2026", 4791163, 10965, 436.95, 10847386, 2.26, 104, 11069, 357, 9564391, 1.56),
    ("November 2026 Run-Rate", "Current Competitor Damage Baseline", "Nov 2026", 3145000, 7176, 438.27, 10008500, 3.18, 4163, 11339, 378, 15636000, 4.97),
    ("Plan - A (Past Proposal)", "Aggressive Sprint (1500 orders/day)", "6 Months", 45000000, 168000, 267.86, 235200000, 5.23, 102000, 270000, 1500, 378000000, 8.40),
    ("Plan - C (Past Proposal)", "Step-Up Efficiency Model (30L to 35L)", "6 Months", 19500000, 54500, 357.80, 76300000, 3.91, 35500, 90000, 500, 126000000, 6.46),
    ("Plan - C.1 (Past Proposal)", "Conservative Step-Up (30L flat)", "6 Months", 18000000, 48000, 375.00, 67200000, 3.73, 32000, 80000, 444, 112000000, 6.22),
    ("Updated 3-Month Plan (Official)", "Google Sheet Calibrated Performance Model", "Dec 2026 - Feb 2027", 9110000, 21621, 421.35, 24430899, 2.68, 9953, 31574, 351, 35591133, 3.91),
]

for row_idx, r_data in enumerate(overview_rows, 5):
    for col_idx, val in enumerate(r_data, 1):
        c = ws1.cell(row=row_idx, column=col_idx, value=val)
        c.border = border_cell
        c.font = cell_font
        if row_idx in [5, 6]:
            c.fill = baseline_fill
            c.font = baseline_font
        elif row_idx == 10:
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
# SHEET 2: 3-MONTH PLAN - BLENDED STORE (MATCHING OFFICIAL GOOGLE SHEET)
# ===========================================================================
ws2 = wb.create_sheet(title="3-Month Plan - Blended")
ws2.views.sheetView[0].showGridLines = True

ws2.cell(row=1, column=1, value="FABB6 — Official 3-Month Blended Store Performance Forecast").font = title_font
ws2.cell(row=2, column=1, value="Source: Google Sheet Model | Google Ads (16L-22L) + Meta Ads (10L-12.1L) | Dec 2026 – Feb 2027").font = subtitle_font

headers_ws2 = [
    "Month", "Operational Phase / Growth Levers", 
    "Google Spend (₹)", "Meta Spend (₹)", "Total Paid Spend (₹)",
    "Google Orders", "Meta Orders", "Total Paid Orders", "Blended Paid CPA (₹)", "Paid Revenue (₹)", "Paid ROAS",
    "Organic & Repeat Orders", "Total Store Orders", "Daily Total Orders", "Daily Paid Orders", "AOV (₹)",
    "Total Gross Revenue (₹)", "Store Blended CPA (₹)", "ROAS on Total"
]

for col_idx, h in enumerate(headers_ws2, 1):
    c = ws2.cell(row=4, column=col_idx, value=h)
    c.fill = header_fill
    c.font = header_font
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = border_cell
ws2.row_dimensions[4].height = 28

rows_ws2 = [
    ("Nov 2026 (Run-Rate)", "Baseline (Competitor Damage Period)", 1607000, 1575000, 3182000, 3860, 3315, 7175, 443.48, 8913000, 2.80, 4163, 11338, 378, 239, 1236, 14013000, 280.65, 4.40),
    ("Dec 2026", "M1: Waste Purge, Google Focus (16L), Meta Reset (10L)", 1600000, 1000000, 2600000, 3556, 2222, 5778, 450.00, 5858667, 2.25, 3096, 8874, 296, 193, 1014, 8998011, 293.00, 3.46),
    ("Jan 2027", "M2: Scaling Google (20L), Feed Optimization, UGC Push", 2000000, 1100000, 3100000, 4651, 2683, 7334, 422.68, 8089501, 2.61, 3313, 10647, 355, 244, 1103, 11743431, 291.17, 3.79),
    ("Feb 2027", "M3: Peak Turnaround (22L Google + 12.1L Meta)", 2200000, 1210000, 3410000, 5366, 3143, 8509, 400.77, 10482732, 3.07, 3545, 12053, 402, 284, 1232, 14849692, 282.91, 4.35),
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
        elif col_idx in [3, 4, 5, 10, 17]:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '"₹"#,##0'
        elif col_idx in [6, 7, 8, 12, 13, 14, 15]:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = '#,##0'
        elif col_idx in [9, 16, 18]:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '"₹"#,##0.00'
        elif col_idx in [11, 19]:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = '0.00"x"'
    ws2.row_dimensions[row_idx].height = 22

# Totals row
tot_row = 9
ws2.cell(row=tot_row, column=1, value="3-Month Total (Dec-Feb)")
ws2.cell(row=tot_row, column=2, value="Cumulative Updated Turnaround Plan")
ws2.cell(row=tot_row, column=3, value=5800000)
ws2.cell(row=tot_row, column=4, value=3310000)
ws2.cell(row=tot_row, column=5, value=9110000)
ws2.cell(row=tot_row, column=6, value=13573)
ws2.cell(row=tot_row, column=7, value=8048)
ws2.cell(row=tot_row, column=8, value=21621)
ws2.cell(row=tot_row, column=9, value=421.35)
ws2.cell(row=tot_row, column=10, value=24430899)
ws2.cell(row=tot_row, column=11, value=2.68)
ws2.cell(row=tot_row, column=12, value=9953)
ws2.cell(row=tot_row, column=13, value=31574)
ws2.cell(row=tot_row, column=14, value=351)
ws2.cell(row=tot_row, column=15, value=240)
ws2.cell(row=tot_row, column=16, value=1127.23)
ws2.cell(row=tot_row, column=17, value=35591133)
ws2.cell(row=tot_row, column=18, value=288.53)
ws2.cell(row=tot_row, column=19, value=3.91)

for col_idx in range(1, 20):
    c = ws2.cell(row=tot_row, column=col_idx)
    c.fill = total_fill
    c.font = total_font
    c.border = border_total
    if col_idx in [1, 2]:
        c.alignment = Alignment(horizontal="left", vertical="center")
    elif col_idx in [3, 4, 5, 10, 17]:
        c.alignment = Alignment(horizontal="right", vertical="center")
        c.number_format = '"₹"#,##0'
    elif col_idx in [6, 7, 8, 12, 13, 14, 15]:
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.number_format = '#,##0'
    elif col_idx in [9, 16, 18]:
        c.alignment = Alignment(horizontal="right", vertical="center")
        c.number_format = '"₹"#,##0.00'
    elif col_idx in [11, 19]:
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.number_format = '0.00"x"'
ws2.row_dimensions[tot_row].height = 24

# ===========================================================================
# SHEET 3: 3-MONTH PLAN - GOOGLE ADS
# ===========================================================================
ws3 = wb.create_sheet(title="3-Month Plan - Google Ads")
ws3.views.sheetView[0].showGridLines = True

ws3.cell(row=1, column=1, value="FABB6 — Google Ads 3-Month Performance Recovery Forecast").font = title_font
ws3.cell(row=2, column=1, value="Matching Google Sheet Model: 16L Dec -> 20L Jan -> 22L Feb | Target ROAS scaling from 2.25x to 3.00x").font = subtitle_font

headers_ws3 = [
    "Month", "Strategic Focus & Key Tactics", 
    "Google Budget (₹)", "Daily Budget (₹)", "Google Target CPA (₹)", "Google Orders", 
    "Daily Orders", "AOV (₹)", "Expected Revenue (₹)", "ROAS"
]

for col_idx, h in enumerate(headers_ws3, 1):
    c = ws3.cell(row=4, column=col_idx, value=h)
    c.fill = header_fill
    c.font = header_font
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = border_cell
ws3.row_dimensions[4].height = 28

rows_ws3 = [
    ("Nov 2026 (Run-Rate)", "Baseline: PMax recovering from 404 URLs & foreign copy", 1607000, 53567, 415.60, 3860, 129, 1236.23, 4771850, 2.97),
    ("Dec 2026", "Triage: 16L budget, 404 URL exclusion, purge Glam+ copy", 1600000, 51613, 450.00, 3556, 115, 1014.00, 3605333, 2.25),
    ("Jan 2027", "Scaling: 20L budget, PMax feed cleanup, high-margin SKU push", 2000000, 64516, 430.00, 4651, 150, 1103.00, 5130233, 2.57),
    ("Feb 2027", "Expansion: 22L budget, non-brand search, 3.00x ROAS target", 2200000, 78571, 410.00, 5366, 192, 1232.00, 6610732, 3.00),
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
        elif col_idx in [3, 4, 9]:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '"₹"#,##0'
        elif col_idx in [6, 7]:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = '#,##0'
        elif col_idx in [5, 8]:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '"₹"#,##0.00'
        elif col_idx == 10:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = '0.00"x"'
    ws3.row_dimensions[row_idx].height = 22

tot_row_g = 9
ws3.cell(row=tot_row_g, column=1, value="3-Month Total (Dec-Feb)")
ws3.cell(row=tot_row_g, column=2, value="Google Ads Scaled Turnaround")
ws3.cell(row=tot_row_g, column=3, value=5800000)
ws3.cell(row=tot_row_g, column=4, value=64444)
ws3.cell(row=tot_row_g, column=5, value=427.32)
ws3.cell(row=tot_row_g, column=6, value=13573)
ws3.cell(row=tot_row_g, column=7, value=151)
ws3.cell(row=tot_row_g, column=8, value=1130.68)
ws3.cell(row=tot_row_g, column=9, value=15346298)
ws3.cell(row=tot_row_g, column=10, value=2.65)

for col_idx in range(1, 11):
    c = ws3.cell(row=tot_row_g, column=col_idx)
    c.fill = total_fill
    c.font = total_font
    c.border = border_total
    if col_idx in [1, 2]:
        c.alignment = Alignment(horizontal="left", vertical="center")
    elif col_idx in [3, 4, 9]:
        c.alignment = Alignment(horizontal="right", vertical="center")
        c.number_format = '"₹"#,##0'
    elif col_idx in [6, 7]:
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.number_format = '#,##0'
    elif col_idx in [5, 8]:
        c.alignment = Alignment(horizontal="right", vertical="center")
        c.number_format = '"₹"#,##0.00'
    elif col_idx == 10:
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.number_format = '0.00"x"'
ws3.row_dimensions[tot_row_g].height = 24

# ===========================================================================
# SHEET 4: 3-MONTH PLAN - META ADS
# ===========================================================================
ws4 = wb.create_sheet(title="3-Month Plan - Meta Ads")
ws4.views.sheetView[0].showGridLines = True

ws4.cell(row=1, column=1, value="FABB6 — Meta Ads 3-Month Performance Recovery Forecast").font = title_font
ws4.cell(row=2, column=1, value="Matching Google Sheet Model: 10L Dec -> 11L Jan -> 12.1L Feb | Rebuilding to High-Efficiency Sweet Spot").font = subtitle_font

headers_ws4 = [
    "Month", "Strategic Focus & Key Tactics", 
    "Meta Budget (₹)", "Daily Budget (₹)", "Meta Target CPA (₹)", "Meta Orders", 
    "Daily Orders", "AOV (₹)", "Expected Revenue (₹)", "ROAS"
]

for col_idx, h in enumerate(headers_ws4, 1):
    c = ws4.cell(row=4, column=col_idx, value=h)
    c.fill = header_fill
    c.font = header_font
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = border_cell
ws4.row_dimensions[4].height = 28

rows_ws4 = [
    ("Nov 2026 (Run-Rate)", "Baseline: Inverted DPA & dead traffic ad burn", 1575000, 52500, 474.96, 3315, 111, 1244.69, 4126300, 2.62),
    ("Dec 2026", "Triage: 10L budget, kill traffic ad, 30-day DPA exclusions", 1000000, 32258, 450.00, 2222, 72, 1014.00, 2253333, 2.25),
    ("Jan 2027", "Restructure: 11L budget, Advantage+ Shopping consolidation", 1100000, 35484, 410.00, 2683, 87, 1103.00, 2959268, 2.69),
    ("Feb 2027", "Restoration: 12.1L budget, scale proven creative hooks", 1210000, 43214, 385.00, 3143, 112, 1232.00, 3872000, 3.20),
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
        elif col_idx in [3, 4, 9]:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '"₹"#,##0'
        elif col_idx in [6, 7]:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = '#,##0'
        elif col_idx in [5, 8]:
            c.alignment = Alignment(horizontal="right", vertical="center")
            c.number_format = '"₹"#,##0.00'
        elif col_idx == 10:
            c.alignment = Alignment(horizontal="center", vertical="center")
            c.number_format = '0.00"x"'
    ws4.row_dimensions[row_idx].height = 22

tot_row_m = 9
ws4.cell(row=tot_row_m, column=1, value="3-Month Total (Dec-Feb)")
ws4.cell(row=tot_row_m, column=2, value="Meta Ads Consolidated Turnaround")
ws4.cell(row=tot_row_m, column=3, value=3310000)
ws4.cell(row=tot_row_m, column=4, value=36778)
ws4.cell(row=tot_row_m, column=5, value=411.28)
ws4.cell(row=tot_row_m, column=6, value=8048)
ws4.cell(row=tot_row_m, column=7, value=89)
ws4.cell(row=tot_row_m, column=8, value=1128.80)
ws4.cell(row=tot_row_m, column=9, value=9084601)
ws4.cell(row=tot_row_m, column=10, value=2.74)

for col_idx in range(1, 11):
    c = ws4.cell(row=tot_row_m, column=col_idx)
    c.fill = total_fill
    c.font = total_font
    c.border = border_total
    if col_idx in [1, 2]:
        c.alignment = Alignment(horizontal="left", vertical="center")
    elif col_idx in [3, 4, 9]:
        c.alignment = Alignment(horizontal="right", vertical="center")
        c.number_format = '"₹"#,##0'
    elif col_idx in [6, 7]:
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.number_format = '#,##0'
    elif col_idx in [5, 8]:
        c.alignment = Alignment(horizontal="right", vertical="center")
        c.number_format = '"₹"#,##0.00'
    elif col_idx == 10:
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.number_format = '0.00"x"'
ws4.row_dimensions[tot_row_m].height = 24

# ===========================================================================
# SHEET 5: 12-MONTH HISTORICAL BASELINE (WITH AUGUST CORRECTION)
# ===========================================================================
ws5 = wb.create_sheet(title="12-Month Historical Baseline")
ws5.views.sheetView[0].showGridLines = True

ws5.cell(row=1, column=1, value="FABB6 — 12-Month Historical Store & Paid Performance Audit (Dec 2025 – Nov 2026)").font = title_font
ws5.cell(row=2, column=1, value="Updated with Corrected August Baseline (Google Spend ₹32.23L, Meta Spend ₹15.69L, Total ₹47.91L)").font = subtitle_font

headers_ws5 = [
    "Month", "Managing Agency", "Google Spend (₹)", "Meta Spend (₹)", "Total Paid Spend (₹)",
    "Paid Purchases", "Blended Paid CPA (₹)", "Paid Sales Value (₹)", "Paid ROAS",
    "Shopify Total Orders", "Shopify Daily Orders", "Shopify Gross Sales (₹)", "Shopify Net Sales (₹)", "Store Blended ROAS"
]

for col_idx, h in enumerate(headers_ws5, 1):
    c = ws5.cell(row=4, column=col_idx, value=h)
    c.fill = header_fill
    c.font = header_font
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    c.border = border_cell
ws5.row_dimensions[4].height = 28

rows_ws5 = [
    ("Dec 2025", "Prior Agency", 227772, 193096, 420868, 1614, 260.76, 1477914, 3.51, 3307, 107, 2637583, 2071721, 4.92),
    ("Jan 2026", "Prior Agency", 762405, 454135, 1216540, 4260, 285.57, 3656195, 3.01, 7850, 253, 5552015, 4639791, 3.81),
    ("Feb 2026", "Prior Agency", 863165, 933840, 1797005, 4817, 373.06, 4370065, 2.43, 8250, 295, 6410361, 6238149, 3.47),
    ("Mar 2026", "Prior Agency", 1500636, 1283438, 2784074, 6351, 438.37, 5369919, 1.93, 11285, 364, 8532040, 5957228, 2.14),
    ("Apr 2026", "Prior Agency", 2001447, 1253761, 3255208, 5350, 608.45, 4614651, 1.42, 10551, 352, 8473141, 7436807, 2.28),
    ("May 2026", "Prior Agency", 2136192, 1885111, 4021304, 7076, 568.29, 6389410, 1.59, 12215, 394, 10096287, 9133293, 2.27),
    ("Jun 2026", "Prior Agency", 2733880, 1552619, 4286498, 6851, 625.66, 5945686, 1.39, 12877, 429, 10389397, 8397880, 1.96),
    ("Jul 2026", "Prior Agency", 2477270, 1884953, 4362222, 8313, 524.75, 7171248, 1.64, 13420, 433, 10364270, 7845258, 1.80),
    ("Aug 2026 (Corrected)", "Prior Agency (Glitch Removed)", 3222573, 1568590, 4791163, 10965, 436.95, 10847386, 2.26, 11069, 357, 9564391, 7476300, 1.56),
    ("Sep 2026", "SilverXis (Failure)", 317895, 309158, 627053, 801, 782.84, 1069643, 1.71, 3112, 104, 3601597, 2849666, 4.54),
    ("Oct 2026", "SilverXis (Diwali Surge)", 2202106, 2044474, 4246579, 7298, 581.85, 9315831, 2.19, 9143, 295, 10566667, 9099142, 2.14),
    ("Nov 2026 (Till Now)", "SilverXis (Current)", 964182, 945164, 1909346, 4310, 443.00, 5344996, 2.80, 4638, 258, 5317824, 4200383, 2.20)
]

for row_idx, r_data in enumerate(rows_ws5, 5):
    for col_idx, val in enumerate(r_data, 1):
        c = ws5.cell(row=row_idx, column=col_idx, value=val)
        c.font = cell_font
        if "SilverXis" in str(r_data[1]):
            c.fill = PatternFill(start_color="FDEDEC", end_color="FDEDEC", fill_type="solid")
        elif "Corrected" in str(r_data[0]):
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
    ws5.row_dimensions[row_idx].height = 22

# Auto-fit column widths across all sheets
for ws in [ws1, ws2, ws3, ws4, ws5]:
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

ws1.column_dimensions['A'].width = 30
ws1.column_dimensions['B'].width = 38
ws2.column_dimensions['A'].width = 20
ws2.column_dimensions['B'].width = 44
ws3.column_dimensions['A'].width = 20
ws3.column_dimensions['B'].width = 44
ws4.column_dimensions['A'].width = 20
ws4.column_dimensions['B'].width = 44
ws5.column_dimensions['A'].width = 22
ws5.column_dimensions['B'].width = 28

output_path = r"C:\Users\test\Videos\Office\reports\FABB6_All_Forecasts_and_Turnaround_Master_Model.xlsx"
wb.save(output_path)
print(f"Successfully saved updated master forecast workbook to: {output_path}")

artifact_path = r"C:\Users\test\.gemini\antigravity\brain\29f77e0a-5ed5-4d24-842c-443d9957274c\FABB6_All_Forecasts_and_Turnaround_Master_Model.xlsx"
shutil.copyfile(output_path, artifact_path)
print(f"Copied to artifacts: {artifact_path}")
