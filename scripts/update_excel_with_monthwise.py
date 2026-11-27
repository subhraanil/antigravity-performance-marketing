import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import win32com.client
import pythoncom
import os
import shutil

print("Updating Master Excel Model with Month-Wise Budgets...")

excel_path = r"C:\Users\test\Videos\Office\reports\FABB6_All_Forecasts_and_Turnaround_Master_Model.xlsx"
wb = openpyxl.load_workbook(excel_path)

font_name = "Calibri"
navy_fill = PatternFill(start_color="102C57", end_color="102C57", fill_type="solid")
sub_navy_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
header_font = Font(name=font_name, size=9.5, bold=True, color="FFFFFF")
section_font = Font(name=font_name, size=11, bold=True, color="102C57")
body_font = Font(name=font_name, size=9, color="222222")
body_font_bold = Font(name=font_name, size=9, bold=True, color="102C57")
zebra_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
total_fill = PatternFill(start_color="EAECEE", end_color="EAECEE", fill_type="solid")

thin_border = Border(
    left=Side(style='thin', color='D3D3D3'),
    right=Side(style='thin', color='D3D3D3'),
    top=Side(style='thin', color='D3D3D3'),
    bottom=Side(style='thin', color='D3D3D3')
)

ws1 = wb["Executive Overview"]

# Let's find where Section 2 starts or append Section 1.1
# Currently Section 2 starts at row 11. Let's insert rows for Section 1.1!
ws1.insert_rows(10, amount=8)

# Now row 10 to 17 are available for Month-Wise Media Budget Allocation Table
ws1.cell(row=10, column=1, value="1.1 Month-Wise Media Budget Allocation by Channel & Strategy (Dec 2026 – Feb 2027)").font = section_font

m_headers = ["Planning Horizon / Month", "Plan 1: Base (Google / Meta / Total)", "Plan 2: Recommended (Google / Meta / Total)", "Plan 3: Aggressive (Google / Meta / Total)"]
for c_idx, h in enumerate(m_headers):
    cell = ws1.cell(row=11, column=c_idx+1, value=h)
    cell.fill = sub_navy_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="center", vertical="center")
    cell.border = thin_border

m_rows = [
    ["December 2026", "₹12.40L / ₹7.60L (Total: ₹20.00L)", "₹16.00L / ₹10.00L (Total: ₹26.00L)", "₹19.20L / ₹10.80L (Total: ₹30.00L)"],
    ["January 2027", "₹15.00L / ₹9.00L (Total: ₹24.00L)", "₹20.00L / ₹11.00L (Total: ₹31.00L)", "₹24.50L / ₹13.50L (Total: ₹38.00L)"],
    ["February 2027", "₹16.10L / ₹9.90L (Total: ₹26.00L)", "₹22.00L / ₹12.10L (Total: ₹34.10L)", "₹28.80L / ₹15.70L (Total: ₹44.50L)"],
    ["Total Q1 Allocation", "₹43.50L / ₹26.50L (Total: ₹70.00L)", "₹58.00L / ₹33.10L (Total: ₹91.10L)", "₹72.50L / ₹40.00L (Total: ₹112.50L)"]
]

for r_idx, r_vals in enumerate(m_rows):
    curr_r = 12 + r_idx
    for c_idx, val in enumerate(r_vals):
        cell = ws1.cell(row=curr_r, column=c_idx+1, value=val)
        cell.border = thin_border
        is_tot = (r_idx == len(m_rows) - 1)
        cell.font = body_font_bold if (is_tot or c_idx == 0) else body_font
        cell.alignment = Alignment(horizontal="center" if c_idx > 0 else "left", vertical="center")
        if is_tot:
            cell.fill = total_fill
        elif r_idx % 2 == 1:
            cell.fill = zebra_fill

wb.save(excel_path)
print("Saved openpyxl workbook with month-wise budget table.")

# Recalculate via Excel COM
pythoncom.CoInitialize()
excel = win32com.client.Dispatch("Excel.Application")
excel.Visible = False
excel.DisplayAlerts = False
try:
    wb_com = excel.Workbooks.Open(os.path.abspath(excel_path))
    excel.CalculateFull()
    wb_com.Save()
    wb_com.Close(True)
    print("Excel COM recalculation completed cleanly!")
finally:
    excel.Quit()

# Mirror to case-studies and artifact directory
case_excel = r"C:\Users\test\Videos\Office\case-studies\fabb6\FABB6_All_Forecasts_and_Turnaround_Master_Model.xlsx"
artifact_excel = r"C:\Users\test\.gemini\antigravity\brain\29f77e0a-5ed5-4d24-842c-443d9957274c\FABB6_All_Forecasts_and_Turnaround_Master_Model.xlsx"
shutil.copy2(excel_path, case_excel)
shutil.copy2(excel_path, artifact_excel)
print("Mirrored Master Excel workbook successfully!")
