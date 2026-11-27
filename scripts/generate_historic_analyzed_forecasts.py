import pandas as pd
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
import os

out_dir = 'reports'
os.makedirs(out_dir, exist_ok=True)
excel_path = os.path.join(out_dir, 'FABB6_Historic_Analyzed_Dual_Forecast_Model.xlsx')

wb = openpyxl.Workbook()

# Setup styles
header_fill = PatternFill(start_color='1E293B', end_color='1E293B', fill_type='solid')
header_font = Font(name='Calibri', size=10, bold=True, color='FFFFFF')
title_font = Font(name='Calibri', size=13, bold=True, color='1E3A8A')

headers_table = [
    "Month",
    "Google Ads Budget (INR)",
    "Google Ads Expected Sales (INR)",
    "Google Orders",
    "Meta Ads Budget (INR)",
    "Meta Ads Expected Sales (INR)",
    "Meta Orders",
    "Total Paid Budget (INR)",
    "Total Paid Sales (INR)",
    "Expected Organic Orders",
    "Expected Return Orders",
    "Total Monthly Orders",
    "Daily Avg Orders",
    "Est. Total Revenue (INR)",
    "Blended Paid CPA (INR)",
    "Overall ROAS (Rev/Ad Spend)"
]

# SCENARIO 1 DATA: Steady Growth & CPA/ROAS Optimization (No Fixed Target)
scen1_data = [
    ["Sept 2026", 2500000.0, 5250000.0, 5500, 1800000.0, 5040000.0, 5300, 4300000.0, 10290000.0, 2500, 1700, 15000, 500, 13125000.0, 398.15, 3.05],
    ["Oct 2026", 2700000.0, 6075000.0, 6300, 2000000.0, 5800000.0, 6100, 4700000.0, 11875000.0, 2900, 2200, 17500, 565, 15487500.0, 379.03, 3.30],
    ["Nov 2026", 3000000.0, 7200000.0, 7300, 2200000.0, 6820000.0, 7100, 5200000.0, 14020000.0, 3400, 2700, 20500, 683, 18347500.0, 361.11, 3.53],
    ["Dec 2026", 3300000.0, 8415000.0, 8300, 2400000.0, 7920000.0, 8100, 5700000.0, 16335000.0, 4000, 3400, 23800, 768, 21539000.0, 347.56, 3.78],
    ["Jan 2027", 3500000.0, 9450000.0, 9200, 2600000.0, 9100000.0, 9200, 6100000.0, 18550000.0, 4600, 4000, 27000, 871, 24705000.0, 331.52, 4.05],
    ["Feb 2027", 3800000.0, 10640000.0, 10200, 2800000.0, 10920000.0, 10500, 6600000.0, 21560000.0, 5200, 4600, 30500, 1017, 28365000.0, 318.84, 4.30],
    ["6-Month Cumulative", 18800000.0, 47030000.0, 46800, 13800000.0, 45600000.0, 46300, 32600000.0, 92630000.0, 22600, 18600, 134300, 746, 121569000.0, 350.16, 3.73]
]

# SCENARIO 2 DATA: Scale Target Model (Reach 45,000 Orders/Month in 6 Months)
scen2_data = [
    ["Sept 2026", 3200000.0, 6460000.0, 6800, 2500000.0, 6768000.0, 7200, 5700000.0, 13228000.0, 3000, 2000, 19000, 633, 17290000.0, 407.14, 3.03],
    ["Oct 2026", 3800000.0, 8075000.0, 8300, 3000000.0, 8455000.0, 8900, 6800000.0, 16530000.0, 3800, 3000, 24000, 774, 22200000.0, 395.35, 3.26],
    ["Nov 2026", 4500000.0, 10080000.0, 10100, 3600000.0, 10620000.0, 11000, 8100000.0, 20700000.0, 4700, 4200, 30000, 1000, 28200000.0, 383.89, 3.48],
    ["Dec 2026", 5200000.0, 12127500.0, 11900, 4200000.0, 12925000.0, 13100, 9400000.0, 25052500.0, 5600, 5400, 36000, 1161, 34380000.0, 376.00, 3.66],
    ["Jan 2027", 6000000.0, 14400000.0, 13700, 4800000.0, 15300000.0, 15100, 10800000.0, 29700000.0, 6500, 6700, 42000, 1355, 40740000.0, 375.00, 3.77],
    ["Feb 2027", 6800000.0, 16524000.0, 15300, 5500000.0, 17869000.0, 17200, 12300000.0, 34393000.0, 7500, 8000, 48000, 1600, 47520000.0, 378.46, 3.86],
    ["6-Month Cumulative", 29500000.0, 67666500.0, 66100, 23600000.0, 71937000.0, 72500, 53100000.0, 139603500.0, 31100, 29300, 199000, 1106, 190330000.0, 383.12, 3.58]
]

def build_sheet(ws, title_text, data):
    ws.cell(row=1, column=1, value=title_text).font = title_font
    for c_idx, h_text in enumerate(headers_table, start=1):
        cell = ws.cell(row=3, column=c_idx, value=h_text)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
    
    for r_idx, r_vals in enumerate(data, start=4):
        for c_idx, val in enumerate(r_vals, start=1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.alignment = Alignment(horizontal='center', vertical='center')
            if r_vals[0] == "6-Month Cumulative":
                cell.font = Font(name='Calibri', size=10, bold=True)
                cell.fill = PatternFill(start_color='E2E8F0', end_color='E2E8F0', fill_type='solid')

# Sheet 1: Scenario 1 - CPA & ROAS Optimization
ws1 = wb.active
ws1.title = "Scenario 1 - CPA & ROAS"
build_sheet(ws1, "FABB6 Scenario 1: CPA & ROAS Optimization Forecast (Steady Growth, No Fixed Target)", scen1_data)

# Sheet 2: Scenario 2 - 45,000 Target Scale
ws2 = wb.create_sheet(title="Scenario 2 - 45K Scale Target")
build_sheet(ws2, "FABB6 Scenario 2: Scale Target Forecast (Reach 45,000 Orders/Month in 6 Months)", scen2_data)

# Sheet 3: Historic Data Summary
ws3 = wb.create_sheet(title="Historic Performance Dec-Aug")
ws3.cell(row=1, column=1, value="FABB6 — Historic Actual Performance (Dec 2025 – Aug 2026)").font = title_font

hist_headers = ["Month", "Shopify Orders", "Shopify Revenue", "Return Rate %", "AOV", "Google Spend", "Google Orders", "Google CPA", "Google ROAS", "Meta Spend", "Meta Orders", "Meta CPA", "Meta ROAS", "Total Paid Spend", "Total Paid Orders", "Blended Paid CPA", "Blended ROAS"]

for c_idx, h_text in enumerate(hist_headers, start=1):
    cell = ws3.cell(row=3, column=c_idx, value=h_text)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

hist_rows = [
    ["December", 3307, 2071721.39, "13.9%", 626.47, 227772.06, 473, 481.09, "1.62x", 193095.79, 1141, 169.00, "5.74x", 420867.85, 1614, 260.76, "3.51x"],
    ["January", 7850, 4639790.76, "17.2%", 591.06, 762405.21, 1323, 576.14, "1.42x", 454134.63, 2937, 154.62, "5.67x", 1216539.84, 4260, 285.57, "3.01x"],
    ["February", 8250, 6238148.88, "18.0%", 756.14, 863165.10, 1331, 648.53, "1.26x", 933839.51, 3486, 267.88, "3.52x", 1797004.61, 4817, 373.05, "2.43x"],
    ["March", 11285, 5957228.31, "18.8%", 527.89, 1500635.87, 1909, 786.17, "0.95x", 1283437.89, 4442, 288.93, "3.08x", 2784073.76, 6351, 438.37, "1.93x"],
    ["April", 10551, 7436807.25, "22.2%", 704.84, 2001446.51, 1458, 1372.38, "0.59x", 1253761.38, 3892, 322.14, "2.74x", 3255207.89, 5350, 608.45, "1.42x"],
    ["May", 12215, 9133292.67, "25.2%", 747.71, 2136192.16, 1479, 1444.15, "0.58x", 1885111.44, 5597, 336.81, "2.73x", 4021303.60, 7076, 568.30, "1.59x"],
    ["June", 12877, 8397879.54, "24.3%", 652.16, 2733879.76, 1243, 2199.24, "0.40x", 1552618.67, 5608, 276.86, "3.12x", 4286498.43, 6851, 625.67, "1.39x"],
    ["July", 13420, 7845257.64, "27.6%", 584.59, 2477269.87, 2300, 1077.07, "0.81x", 1884952.62, 6013, 313.48, "2.73x", 4362222.49, 8313, 524.75, "1.64x"],
    ["August", 10351, 7024176.82, "27.4%", 678.60, 3126167.10, 6435, 485.83, "1.96x", 1451530.72, 3962, 366.36, "2.74x", 4577697.82, 10397, 440.29, "2.21x"]
]

for r_idx, r_vals in enumerate(hist_rows, start=4):
    for c_idx, val in enumerate(r_vals, start=1):
        cell = ws3.cell(row=r_idx, column=c_idx, value=val)
        cell.alignment = Alignment(horizontal='center', vertical='center')

wb.save(excel_path)
print(f"Generated Dual Forecast Excel Workbook with Historic Analysis at {excel_path}")
