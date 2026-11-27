import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
import pandas as pd
import os

out_dir = 'reports'
os.makedirs(out_dir, exist_ok=True)
excel_out = os.path.join(out_dir, 'FABB6_CPA_and_ROAS_Improvement_Forecast.xlsx')

wb = openpyxl.Workbook()

# Sheet 1: 6-Month Forecast
ws1 = wb.active
ws1.title = "6-Month Forecast"

# Header Title
ws1.merge_cells('A1:O1')
cell_a1 = ws1['A1']
cell_a1.value = "FABB6 — 6-Month CPA & ROAS Improvement Forecast (Efficiency & Sustainable Profit Growth)"
cell_a1.font = Font(name='Calibri', size=14, bold=True, color='1E3A8A')
cell_a1.alignment = Alignment(horizontal='left', vertical='center')

# 15 Columns matching client format exactly:
headers_15 = [
    "Month",
    "Total Orders",
    "Google Orders",
    "Meta Orders",
    "Organic/Direct Orders",
    "Repeat/Retention Orders",
    "Google Spend (INR)",
    "Meta Spend (INR)",
    "Total Paid Spend (INR)",
    "Blended Paid CPA (INR)",
    "AOV (INR)",
    "Est. Total Revenue (INR)",
    "Blended ROAS (Rev/Ad Spend)",
    "Avg Daily Orders",
    "CPA Improvement Status"
]

for col_num, h_text in enumerate(headers_15, start=1):
    cell = ws1.cell(row=3, column=col_num)
    cell.value = h_text
    cell.font = Font(name='Calibri', size=10, bold=True, color='FFFFFF')
    cell.fill = PatternFill(start_color='1E293B', end_color='1E293B', fill_type='solid')
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

forecast_rows = [
    ["Month 1 (Sep '26)", 18500, 6800, 7500, 2400, 1800, 2176000.0, 2025000.0, 4201000.0, 293.78, 880, 16280000.0, 3.88, 617, "Baseline Efficiency (CPA ₹293.78 | 3.88x ROAS)"],
    ["Month 2 (Oct '26)", 21200, 7400, 8300, 2900, 2600, 2257000.0, 2116500.0, 4373500.0, 278.57, 895, 18974000.0, 4.34, 707, "Moderate CPA Improvement (CPA ₹278.57 | 4.34x ROAS)"],
    ["Month 3 (Nov '26)", 24500, 8100, 9200, 3500, 3700, 2349000.0, 2208000.0, 4557000.0, 263.41, 905, 22172500.0, 4.87, 817, "Strong Efficiency Gain (CPA ₹263.41 | 4.87x ROAS)"],
    ["Month 4 (Dec '26)", 27800, 8700, 10100, 4200, 4800, 2392500.0, 2272500.0, 4665000.0, 248.14, 915, 25437000.0, 5.45, 927, "High ROAS Achievement (CPA ₹248.14 | 5.45x ROAS)"],
    ["Month 5 (Jan '27)", 31000, 9300, 11000, 4900, 5800, 2418000.0, 2365000.0, 4783000.0, 235.62, 925, 28675000.0, 6.00, 1033, "Optimum Funnel CPA (CPA ₹235.62 | 6.00x ROAS)"],
    ["Month 6 (Feb '27)", 34500, 10000, 12000, 5700, 6800, 2500000.0, 2520000.0, 5020000.0, 228.18, 935, 32257500.0, 6.43, 1150, "Milestone Peak Efficiency (CPA ₹228.18 | 6.43x ROAS)"],
    ["6-Month Cumulative", 157500, 50300, 58100, 23600, 25500, 14092500.0, 13507000.0, 27599500.0, 254.61, 913, 143796000.0, 5.21, 875, "Cumulative 15.5% CPA Improvement & 5.21x ROAS"]
]

for r_idx, r_data in enumerate(forecast_rows, start=4):
    for c_idx, val in enumerate(r_data, start=1):
        cell = ws1.cell(row=r_idx, column=c_idx)
        cell.value = val
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.font = Font(name='Calibri', size=10)
        if r_data[0] == "6-Month Cumulative":
            cell.font = Font(name='Calibri', size=10, bold=True)
            cell.fill = PatternFill(start_color='E2E8F0', end_color='E2E8F0', fill_type='solid')

# Sheet 2: Assumptions
ws2 = wb.create_sheet(title="Assumptions")
ws2.cell(row=1, column=1, value="Forecast Assumptions — CPA & ROAS Improvement Model").font = Font(size=12, bold=True, color='1E3A8A')
ws2.cell(row=3, column=1, value="Strategy Focus: Reduce Google & Meta CPA via Funnel Segmentation (Prospecting vs Remarketing vs Re-orders).").font = Font(italic=True)

assumptions_data = [
    ["Month", "Google Ads CPA (INR)", "Meta Ads CPA (INR)", "Blended Paid CPA (INR)", "Blended AOV (INR)", "Target ROAS"],
    ["Month 1 (Sep '26)", 320, 270, 293.78, 880, 3.88],
    ["Month 2 (Oct '26)", 305, 255, 278.57, 895, 4.34],
    ["Month 3 (Nov '26)", 290, 240, 263.41, 905, 4.87],
    ["Month 4 (Dec '26)", 275, 225, 248.14, 915, 5.45],
    ["Month 5 (Jan '27)", 260, 215, 235.62, 925, 6.00],
    ["Month 6 (Feb '27)", 250, 210, 228.18, 935, 6.43]
]

for r_idx, r_data in enumerate(assumptions_data, start=5):
    for c_idx, val in enumerate(r_data, start=1):
        cell = ws2.cell(row=r_idx, column=c_idx, value=val)
        cell.alignment = Alignment(horizontal='center', vertical='center')
        if r_idx == 5:
            cell.font = Font(bold=True, color='FFFFFF')
            cell.fill = PatternFill(start_color='1E293B', end_color='1E293B', fill_type='solid')

# Sheet 3: Historical Data
ws3 = wb.create_sheet(title="Historical Data")
ws3.cell(row=1, column=1, value="FABB6 — Past Performance Baseline").font = Font(size=12, bold=True)
ws3.cell(row=3, column=1, value="Google Ads Baseline (Google Shopping App Purchase Deduplicated): Aug MTD CPA INR 507.78 | 1.84x ROAS").font = Font(italic=True)
ws3.cell(row=4, column=1, value="Meta Ads Baseline: July CPA INR 302.84 | 2.83x ROAS | June CPA INR 276.96 | 3.12x ROAS").font = Font(italic=True)

wb.save(excel_out)
print(f"Successfully generated client-formatted Excel workbook at {excel_out}")
