import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_reconciled_excel_model(filepath):
    wb = openpyxl.Workbook()
    # Remove default sheet
    default_sheet = wb.active
    wb.remove(default_sheet)
    
    # Styles
    navy_fill = PatternFill(start_color="102C57", end_color="102C57", fill_type="solid")
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    sub_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    total_fill = PatternFill(start_color="EAECEE", end_color="EAECEE", fill_type="solid")
    zebra_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")
    alert_fill = PatternFill(start_color="FDEDEC", end_color="FDEDEC", fill_type="solid")
    
    font_title = Font(name="Calibri", size=15, bold=True, color="FFFFFF")
    font_section = Font(name="Calibri", size=11, bold=True, color="102C57")
    font_hdr = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    font_bold = Font(name="Calibri", size=9.5, bold=True, color="102C57")
    font_bold_charcoal = Font(name="Calibri", size=9.5, bold=True, color="202020")
    font_regular = Font(name="Calibri", size=9.5, color="333333")
    font_alert = Font(name="Calibri", size=9.5, bold=True, color="922B21")
    
    thin_border = Border(
        left=Side(style='thin', color='D0D7DE'),
        right=Side(style='thin', color='D0D7DE'),
        top=Side(style='thin', color='D0D7DE'),
        bottom=Side(style='thin', color='D0D7DE')
    )
    double_bottom_border = Border(
        left=Side(style='thin', color='D0D7DE'),
        right=Side(style='thin', color='D0D7DE'),
        top=Side(style='thin', color='D0D7DE'),
        bottom=Side(style='double', color='102C57')
    )

    # ----------------------------------------------------
    # TAB 1: Executive Overview & Scenarios
    # ----------------------------------------------------
    ws1 = wb.create_sheet(title="Executive Overview")
    ws1.views.sheetView[0].showGridLines = True
    
    # Title Banner
    ws1.merge_cells("A1:G1")
    cell = ws1["A1"]
    cell.value = "FABB6 TURNAROUND FORECAST: TOTAL SALES REVENUE MODEL"
    cell.font = font_title
    cell.fill = navy_fill
    cell.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws1.row_dimensions[1].height = 36
    
    ws1.merge_cells("A2:G2")
    ws1["A2"].value = "Techno Exponent Growth Practice | Total Sales Revenue Metrics | Target Period: Dec 2026 – Feb 2027"
    ws1["A2"].font = Font(name="Calibri", size=10, italic=True, color="555555")
    ws1["A2"].alignment = Alignment(horizontal="left", vertical="center")
    ws1.row_dimensions[2].height = 20
    
    # Section: 3 Scenarios Summary
    ws1["A4"].value = "1. Three-Month Turnaround Scenarios (Total Sales Revenue ÷ Ad Spend)"
    ws1["A4"].font = font_section
    
    scen_headers = ["Scenario", "Total Sales ROAS Multiplier", "Dec 2026 Total Sales", "Jan 2027 Total Sales", "Feb 2027 Total Sales", "Quarter Total Revenue", "Quarter ROAS"]
    for col_idx, h in enumerate(scen_headers, 1):
        c = ws1.cell(row=5, column=col_idx, value=h)
        c.font = font_hdr
        c.fill = header_fill
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = thin_border
    ws1.row_dimensions[5].height = 28
    
    scen_data = [
        ["Conservative Scenario", "3.00x / 3.00x / 3.00x", 7800000, 9300000, 10230000, 27330000, "3.00x"],
        ["Target Plan (Master Forecast)", "3.46x / 3.79x / 4.35x", 8998011, 11743431, 14849692, 35591133, "3.91x"],
        ["Stretch Scenario", "3.70x / 4.10x / 4.65x", 9620000, 12710000, 15856500, 38186500, "4.19x"]
    ]
    for r_idx, row in enumerate(scen_data, 6):
        ws1.row_dimensions[r_idx].height = 22
        for c_idx, val in enumerate(row, 1):
            c = ws1.cell(row=r_idx, column=c_idx, value=val)
            c.border = thin_border
            if c_idx == 1:
                c.font = font_bold
                c.alignment = Alignment(horizontal="left", vertical="center")
            elif c_idx == 2 or c_idx == 7:
                c.font = font_regular
                c.alignment = Alignment(horizontal="center", vertical="center")
            else:
                c.font = font_bold_charcoal if r_idx == 7 else font_regular
                c.alignment = Alignment(horizontal="right", vertical="center")
                c.number_format = "₹#,##,##0"
            if r_idx == 7: # Highlight Target Plan
                c.fill = sub_fill
                
    # Section: Avoidable Spend Range
    ws1["A10"].value = "2. Avoidable Capital Waste Range (Interim Period: Sep 1 – Nov 18, 2026)"
    ws1["A10"].font = font_section
    
    waste_headers = ["Measure Tier", "Amount (₹)", "Basis & Primary Evidence"]
    for col_idx, h in enumerate(waste_headers, 1):
        c = ws1.cell(row=11, column=col_idx, value=h)
        c.font = font_hdr
        c.fill = header_fill
        c.alignment = Alignment(horizontal="center" if col_idx != 3 else "left", vertical="center")
        c.border = thin_border
    ws1.row_dimensions[11].height = 25
    
    waste_rows = [
        ["Provable Floor (Zero-Order Spend)", 149660, "Merchant Center 404 URLs (₹80,285) + IG-Traffic zero-sale ad (₹50,214) + iOS App installs (₹19,161). 100% verified zero sales."],
        ["Central Estimate (Excess CPA Bleed)", 587000, "Floor (₹1.50L) + Google Sep disruption vs Aug ₹480 CPA (₹2.98L) + Android App excess above cold CPA (₹0.77L) + DPA excess vs cold CPA (₹0.63L)."],
        ["Upper Bound (Affected Campaigns)", 746558, "Gross spend in all compromised campaigns: Google Sep (₹3,17,895) + 404 SKUs (₹80,285) + IG-Traffic (₹50,214) + Apps (₹1,57,302) + DPA (₹1,40,862)."]
    ]
    for r_idx, row in enumerate(waste_rows, 12):
        ws1.row_dimensions[r_idx].height = 24
        for c_idx, val in enumerate(row, 1):
            c = ws1.cell(row=r_idx, column=c_idx, value=val)
            c.border = thin_border
            if c_idx == 1:
                c.font = font_bold
                c.alignment = Alignment(horizontal="left", vertical="center")
                if "Floor" in val:
                    c.fill = alert_fill
            elif c_idx == 2:
                c.font = font_alert if "Floor" in row[0] else font_bold_charcoal
                c.alignment = Alignment(horizontal="right", vertical="center")
                c.number_format = "₹#,##,##0"
                if "Floor" in row[0]:
                    c.fill = alert_fill
            else:
                c.font = font_regular
                c.alignment = Alignment(horizontal="left", vertical="center")

    # ----------------------------------------------------
    # TAB 2: Master Turnaround Forecast (Total Sales Revenue)
    # ----------------------------------------------------
    ws2 = wb.create_sheet(title="3-Month Plan - Master Forecast")
    ws2.views.sheetView[0].showGridLines = True
    
    ws2.merge_cells("A1:J1")
    ws2["A1"].value = "FABB6 MASTER TURNAROUND FORECAST (TOTAL SALES REVENUE)"
    ws2["A1"].font = font_title
    ws2["A1"].fill = navy_fill
    ws2["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws2.row_dimensions[1].height = 36
    
    ws2.merge_cells("A2:J2")
    ws2["A2"].value = "Primary Sales Metric: Total Sales Revenue (Shopify Net Recognized Sales). Reconciled with Client Master Sheet."
    ws2["A2"].font = Font(name="Calibri", size=10, italic=True, color="555555")
    ws2["A2"].alignment = Alignment(horizontal="left", vertical="center")
    ws2.row_dimensions[2].height = 20
    
    base_headers = [
        "Month", "Total Ad Spend", "Google Spend", "Meta Spend", "Paid Orders", 
        "Orders from Others*", "Total Store Orders", "Total Sales Revenue", "Blended CPA", "Total Sales ROAS"
    ]
    for col_idx, h in enumerate(base_headers, 1):
        c = ws2.cell(row=4, column=col_idx, value=h)
        c.font = font_hdr
        c.fill = header_fill
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = thin_border
    ws2.row_dimensions[4].height = 28
    
    base_rows = [
        ["Nov 2026 (Extrapolated 30-Day Run-Rate)", 3181667, 1607000, 1574667, 4310*30/18, 4638*30/18 - 4310*30/18, 7730, 7000638, 412, "2.20x"],
        ["December 2026", 2600000, 1600000, 1000000, 5778, 3096, 8874, 8998011, 293.00, "3.46x"],
        ["January 2027", 3100000, 2000000, 1100000, 7334, 3313, 10647, 11743431, 291.17, "3.79x"],
        ["February 2027", 3410000, 2200000, 1210000, 8509, 3545, 12053, 14849692, 282.91, "4.35x"],
        ["Total Q1 Plan (Dec – Feb)", 9110000, 5800000, 3310000, 21621, 9953, 31574, 35591133, 288.53, "3.91x"]
    ]
    for r_idx, row in enumerate(base_rows, 5):
        ws2.row_dimensions[r_idx].height = 22
        is_total = (r_idx == 9)
        is_ref = (r_idx == 5)
        for c_idx, val in enumerate(row, 1):
            c = ws2.cell(row=r_idx, column=c_idx, value=val)
            if is_total:
                c.border = double_bottom_border
                c.fill = total_fill
                c.font = font_bold
            elif is_ref:
                c.border = thin_border
                c.fill = zebra_fill
                c.font = font_regular
            else:
                c.border = thin_border
                c.font = font_regular
                
            if c_idx == 1:
                c.alignment = Alignment(horizontal="left", vertical="center")
            elif c_idx in [2, 3, 4, 8]:
                c.alignment = Alignment(horizontal="right", vertical="center")
                c.number_format = "₹#,##,##0"
            elif c_idx in [5, 6, 7]:
                c.alignment = Alignment(horizontal="center", vertical="center")
                c.number_format = "#,##0"
            elif c_idx == 9:
                c.alignment = Alignment(horizontal="right", vertical="center")
                c.number_format = "₹#,##0.00"
            elif c_idx == 10:
                c.alignment = Alignment(horizontal="center", vertical="center")

    # ----------------------------------------------------
    # TAB 3: Channel-Level Guardrails
    # ----------------------------------------------------
    ws3 = wb.create_sheet(title="Channel Guardrails")
    ws3.views.sheetView[0].showGridLines = True
    
    ws3.merge_cells("A1:H1")
    ws3["A1"].value = "CHANNEL-LEVEL PLATFORM GUARDRAILS (BUDGETS & CPA CEILINGS)"
    ws3["A1"].font = font_title
    ws3["A1"].fill = navy_fill
    ws3["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws3.row_dimensions[1].height = 36
    
    chan_headers = [
        "Month", "Google Budget", "Google Target CPA", "Google Expected Orders", 
        "Meta Budget", "Meta Target CPA", "Meta Expected Orders", "Combined Paid Orders"
    ]
    for col_idx, h in enumerate(chan_headers, 1):
        c = ws3.cell(row=4, column=col_idx, value=h)
        c.font = font_hdr
        c.fill = header_fill
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = thin_border
    ws3.row_dimensions[4].height = 28
    
    chan_rows = [
        ["December 2026", 1600000, 450, 3556, 1000000, 450, 2222, 5778],
        ["January 2027", 2000000, 430, 4651, 1100000, 410, 2683, 7334],
        ["February 2027", 2200000, 410, 5366, 1210000, 385, 3143, 8509],
        ["3-Month Total / Avg", 5800000, 427, 13573, 3310000, 411, 8048, 21621]
    ]
    for r_idx, row in enumerate(chan_rows, 5):
        ws3.row_dimensions[r_idx].height = 22
        is_total = (r_idx == 8)
        for c_idx, val in enumerate(row, 1):
            c = ws3.cell(row=r_idx, column=c_idx, value=val)
            if is_total:
                c.border = double_bottom_border
                c.fill = total_fill
                c.font = font_bold
            else:
                c.border = thin_border
                c.font = font_regular
                
            if c_idx == 1:
                c.alignment = Alignment(horizontal="left", vertical="center")
            elif c_idx in [2, 5]:
                c.alignment = Alignment(horizontal="right", vertical="center")
                c.number_format = "₹#,##,##0"
            elif c_idx in [3, 6]:
                c.alignment = Alignment(horizontal="right", vertical="center")
                c.number_format = "₹#,##0.00"
            elif c_idx in [4, 7, 8]:
                c.alignment = Alignment(horizontal="center", vertical="center")
                c.number_format = "#,##0"

    # ----------------------------------------------------
    # TAB 4: Twelve-Month Reconciled Historical Baseline
    # ----------------------------------------------------
    ws4 = wb.create_sheet(title="12-Month Historical Baseline")
    ws4.views.sheetView[0].showGridLines = True
    
    ws4.merge_cells("A1:G1")
    ws4["A1"].value = "FABB6 12-MONTH HISTORICAL BASELINE (TOTAL SALES REVENUE)"
    ws4["A1"].font = font_title
    ws4["A1"].fill = navy_fill
    ws4["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws4.row_dimensions[1].height = 36
    
    ws4.merge_cells("A2:G2")
    ws4["A2"].value = "Sales Metric: Total Sales Revenue (Shopify Net Recognized Sales). ROAS = Total Sales Revenue ÷ Total Spend."
    ws4["A2"].font = Font(name="Calibri", size=10, italic=True, color="555555")
    ws4["A2"].alignment = Alignment(horizontal="left", vertical="center")
    ws4.row_dimensions[2].height = 20
    
    hist_headers = [
        "Month", "Total Spend", "Paid Orders (Platform)", 
        "Paid CPA", "Shopify Orders", "Total Sales Revenue", "Total Sales ROAS"
    ]
    for col_idx, h in enumerate(hist_headers, 1):
        c = ws4.cell(row=4, column=col_idx, value=h)
        c.font = font_hdr
        c.fill = header_fill
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = thin_border
    ws4.row_dimensions[4].height = 28
    
    hist_rows = [
        ["Dec 2025", 420868, 1614, 260.76, 3307, 2071721.39, "4.92x"],
        ["Jan 2026", 1216540, 4260, 285.57, 7850, 4639790.76, "3.81x"],
        ["Feb 2026", 1797005, 4817, 373.06, 8250, 6238148.88, "3.47x"],
        ["Mar 2026", 2784074, 6351, 438.37, 11285, 5957228.31, "2.14x"],
        ["Apr 2026", 3255208, 5350, 608.45, 10551, 7436807.25, "2.28x"],
        ["May 2026", 4020942, 7076, 568.25, 12215, 9133292.67, "2.27x"],
        ["Jun 2026", 4286412, 6851, 625.66, 12877, 8397879.54, "1.96x"],
        ["Jul 2026", 4362145, 8313, 524.74, 13420, 7845257.64, "1.80x"],
        ["Aug 2026", 4791163, 10965, 436.95, 11069, 7476300.38, "1.56x"],
        ["Sep 2026", 627053, 801, 783.01, 3112, 2849665.77, "4.54x"],
        ["Oct 2026", 4246579, 7298, 581.92, 9143, 9099141.98, "2.14x"],
        ["Nov 2026 (to 18 Nov)", 1909346, 4310, 442.92, 4638, 4200383.06, "2.20x"],
    ]
    for r_idx, row in enumerate(hist_rows, 5):
        ws4.row_dimensions[r_idx].height = 20
        is_interim = row[0] in ["Sep 2026", "Oct 2026", "Nov 2026 (to 18 Nov)"]
        for c_idx, val in enumerate(row, 1):
            c = ws4.cell(row=r_idx, column=c_idx, value=val)
            c.border = thin_border
            if is_interim:
                c.fill = alert_fill if row[0] == "Sep 2026" else zebra_fill
                c.font = font_bold_charcoal if row[0] == "Sep 2026" else font_regular
            else:
                c.font = font_regular
                
            if c_idx == 1:
                c.alignment = Alignment(horizontal="left", vertical="center")
            elif c_idx in [2, 6]:
                c.alignment = Alignment(horizontal="right", vertical="center")
                c.number_format = "₹#,##,##0"
            elif c_idx == 4:
                c.alignment = Alignment(horizontal="right", vertical="center")
                c.number_format = "₹#,##0.00"
            elif c_idx in [3, 5]:
                c.alignment = Alignment(horizontal="center", vertical="center")
                c.number_format = "#,##0"
            elif c_idx == 7:
                c.alignment = Alignment(horizontal="center", vertical="center")

    # Auto-adjust column widths across all sheets
    for ws in wb.worksheets:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                # ignore merged title cells
                if cell.row in [1, 2]:
                    continue
                if cell.value:
                    val_str = str(cell.value)
                    if len(val_str) > max_len:
                        max_len = len(val_str)
            ws.column_dimensions[col_letter].width = max(max_len + 4, 12)
            
    # Save workbook
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    wb.save(filepath)
    print(f"Successfully created reconciled workbook at: {filepath}")

if __name__ == "__main__":
    report_xlsx = r"C:\Users\test\Videos\Office\reports\FABB6_All_Forecasts_and_Turnaround_Master_Model.xlsx"
    case_study_xlsx = r"C:\Users\test\Videos\Office\case-studies\fabb6\FABB6_All_Forecasts_and_Turnaround_Master_Model.xlsx"
    build_reconciled_excel_model(report_xlsx)
    build_reconciled_excel_model(case_study_xlsx)
