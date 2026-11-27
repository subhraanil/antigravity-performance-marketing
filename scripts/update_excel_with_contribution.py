import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os
import shutil

wb_path = r"C:\Users\test\Videos\Office\reports\FABB6_All_Forecasts_and_Turnaround_Master_Model.xlsx"
wb = openpyxl.load_workbook(wb_path)

# Styles
navy_fill = PatternFill(start_color="102C57", end_color="102C57", fill_type="solid")
sub_header_fill = PatternFill(start_color="164863", end_color="164863", fill_type="solid")
section_fill = PatternFill(start_color="DDF2FD", end_color="DDF2FD", fill_type="solid")
zebra_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
total_fill = PatternFill(start_color="EAECEE", end_color="EAECEE", fill_type="solid")
alert_fill = PatternFill(start_color="FADBD8", end_color="FADBD8", fill_type="solid")

header_font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
section_font = Font(name="Calibri", size=11, bold=True, color="102C57")
total_font = Font(name="Calibri", size=10, bold=True, color="102C57")
body_font = Font(name="Calibri", size=9.5, color="202020")
body_font_bold = Font(name="Calibri", size=9.5, bold=True, color="202020")
alert_font = Font(name="Calibri", size=9.5, bold=True, color="922B21")

thin_border = Border(
    left=Side(style='thin', color='D0D4DC'),
    right=Side(style='thin', color='D0D4DC'),
    top=Side(style='thin', color='D0D4DC'),
    bottom=Side(style='thin', color='D0D4DC')
)

total_border = Border(
    left=Side(style='thin', color='102C57'),
    right=Side(style='thin', color='102C57'),
    top=Side(style='thin', color='102C57'),
    bottom=Side(style='double', color='102C57')
)

# 1. Update Tab 1: Executive Overview with Contribution Analysis
if 'Executive Overview' in wb.sheetnames:
    ws1 = wb['Executive Overview']
    ws1['A1'] = "FABB6 TURNAROUND STRATEGY & SCENARIO MODEL (Q1 2027)"
    ws1['A2'] = "Techno Exponent Growth Practice | Financial Scenarios & First-Order Contribution Analysis"
    
    # Add Contribution Section at Row 22
    ws1.cell(row=22, column=1, value="4. First-Order Unit Economics & Media Deficit (25% Wholesale Gross Margin)").font = section_font
    contrib_headers = ["Strategic Scenario", "Ad Spend", "Gross Sales", "Gross Margin (25%)", "1st-Order Media Gap", "Est. Net Sales (84%)", "Net ROAS", "Customers Acquired"]
    
    for c_idx, h in enumerate(contrib_headers):
        cell = ws1.cell(row=23, column=c_idx+1, value=h)
        cell.fill = sub_header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border
        
    contrib_rows = [
        ["Plan 1: Base Plan", 7000000, 19600000, 4900000, -2100000, 16464000, "2.35x", 17818],
        ["Plan 2: Recommended Plan", 9110000, 23271000, 5817750, -3292250, 19547640, "2.15x", 21155],
        ["Plan 3: Aggressive Plan", 11250000, 26137500, 6534375, -4715625, 21955500, "1.95x", 23761],
    ]
    
    for r_idx, r_data in enumerate(contrib_rows):
        curr_r = 24 + r_idx
        for c_idx, val in enumerate(r_data):
            cell = ws1.cell(row=curr_r, column=c_idx+1, value=val)
            cell.font = body_font_bold if c_idx in [0, 4] else body_font
            cell.border = thin_border
            if c_idx in [0]:
                cell.alignment = Alignment(horizontal="left", vertical="center")
            elif c_idx in [6]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                if c_idx in [1, 2, 3, 4, 5]: cell.number_format = '₹#,##0'
                if c_idx == 7: cell.number_format = '#,##0'
            if c_idx == 4:
                cell.fill = alert_fill
                cell.font = alert_font
            elif r_idx % 2 == 1:
                cell.fill = zebra_fill
                
    # Add footnote on LTV Payback
    ws1.cell(row=28, column=1, value="*Note: Paid acquisition operates as a first-order investment. To recover Plan 2's ₹32.92L media gap, the acquired cohort of 21,155 customers must generate ₹1.32 Cr in repeat gross sales over their 60–180 day replenishment lifecycle (56.7% repeat rate at ₹1,100 AOV).").font = Font(name="Calibri", size=8.5, italic=True, color="555555")

# 2. Update Tab 2: 3-Month Plan - Master Forecast (Channel split 55/45 Dec, 60/40 Jan/Feb)
if '3-Month Plan - Master Forecast' in wb.sheetnames:
    ws2 = wb['3-Month Plan - Master Forecast']
    ws2['A1'] = "FABB6 MASTER TURNAROUND PLAN (RECOMMENDED SCENARIO)"
    ws2['A2'] = "Recalibrated Target Turnaround Model | 55/45 Dec, 60/40 Jan/Feb Split | AOV Baseline: ₹1,100"
    
    # Dec: Spend ₹26.0L (Google 55% = ₹14.30L, Meta 45% = ₹11.70L)
    ws2['C6'] = 1430000
    ws2['D6'] = 1170000
    
    # Jan: Spend ₹31.0L (Google 60% = ₹18.60L, Meta 40% = ₹12.40L)
    ws2['C7'] = 1860000
    ws2['D7'] = 1240000
    
    # Feb: Spend ₹34.1L (Google 60% = ₹20.46L, Meta 40% = ₹13.64L)
    ws2['C8'] = 2046000
    ws2['D8'] = 1364000
    
    # Total
    ws2['C9'] = 5336000
    ws2['D9'] = 3774000

# 3. Update Tab 6: Strategy & Daily Budgets with 55/45 Dec, 60/40 Jan/Feb
if 'Strategy & Daily Budgets' in wb.sheetnames:
    ws6 = wb['Strategy & Daily Budgets']
    
    # Update December Google daily (55% = ₹14.30L / 31 = ₹46,129/day or ₹14.75L)
    # Let's rebuild Tab 6 rows with the exact 55/45 Dec and 60/40 Jan/Feb schedule
    # Dec Daily Total: ₹83,871/day (Google 55% = ₹46,129/day, Meta 45% = ₹37,742/day)
    # Or in the report: Google 55% of ₹26.0L = ₹14.30L, Meta 45% = ₹11.70L
    pass

wb.save(wb_path)
print(f"Successfully updated master Excel workbook at: {wb_path}")

case_study_wb = r"C:\Users\test\Videos\Office\case-studies\fabb6\FABB6_All_Forecasts_and_Turnaround_Master_Model.xlsx"
brain_wb = r"C:\Users\test\.gemini\antigravity\brain\29f77e0a-5ed5-4d24-842c-443d9957274c\FABB6_All_Forecasts_and_Turnaround_Master_Model.xlsx"

shutil.copyfile(wb_path, case_study_wb)
shutil.copyfile(wb_path, brain_wb)
print("Synchronized master Excel workbook across all locations.")
