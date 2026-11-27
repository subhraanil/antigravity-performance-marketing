import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import pandas as pd

def build_forecast_workbook():
    wb = openpyxl.Workbook()
    
    # Sheet 1: Forecast Comparison & Variance
    ws1 = wb.active
    ws1.title = "Past 4 Forecasts vs Actuals"
    ws1.views.sheetView[0].showGridLines = True

    # Sheet 2: Next 6-Month Recovery Forecast
    ws2 = wb.create_sheet(title="Next 6M Recovery Forecast")
    ws2.views.sheetView[0].showGridLines = True

    # Styles
    navy_fill = PatternFill(start_color="102C57", end_color="102C57", fill_type="solid")
    gold_fill = PatternFill(start_color="B8860B", end_color="B8860B", fill_type="solid")
    light_blue_fill = PatternFill(start_color="EBF5FB", end_color="EBF5FB", fill_type="solid")
    light_red_fill = PatternFill(start_color="FDEDEC", end_color="FDEDEC", fill_type="solid")
    light_green_fill = PatternFill(start_color="EAFAF1", end_color="EAFAF1", fill_type="solid")
    gray_fill = PatternFill(start_color="F2F4F4", end_color="F2F4F4", fill_type="solid")
    
    font_title = Font(name="Calibri", size=15, bold=True, color="102C57")
    font_sub = Font(name="Calibri", size=10, italic=True, color="555555")
    font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_bold = Font(name="Calibri", size=10, bold=True)
    font_regular = Font(name="Calibri", size=10)
    font_red = Font(name="Calibri", size=10, color="922B21", bold=True)
    font_green = Font(name="Calibri", size=10, color="196F3D", bold=True)

    thin_border = Border(
        left=Side(style='thin', color='D5D8DC'),
        right=Side(style='thin', color='D5D8DC'),
        top=Side(style='thin', color='D5D8DC'),
        bottom=Side(style='thin', color='D5D8DC')
    )

    # -------------------------------------------------------------
    # POPULATE SHEET 1: Past 4 Forecasts vs Actuals
    # -------------------------------------------------------------
    ws1["A1"] = "FABB6 (Glanzzkart Pvt Ltd) — Comparison of Actual Performance vs. 4 Proposed Forecast Plans"
    ws1["A1"].font = font_title
    ws1["A2"] = "Evaluated Period: September 1, 2026 to November 18, 2026 (Competitor Tenure vs Plan A, Plan C, Plan C.1, Plan B)"
    ws1["A2"].font = font_sub

    headers1 = [
        "Month", "Metric Category", "Competitor Actual", "Plan A (Normal Growth)", "Plan C (30L Step-Up)", 
        "Plan C.1 (30L Revised)", "Plan B (1500 Orders)", "Variance vs Plan C (%)", "Evaluation & Root Cause"
    ]
    
    for col_idx, h in enumerate(headers1, 1):
        c = ws1.cell(4, col_idx, h)
        c.font = font_header
        c.fill = navy_fill
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    comparison_data = [
        # September 2026
        ["Sep 2026", "Total Paid Ad Spend", 627052.85, 3000000.0, 3000000.0, 3000000.0, 5600000.0, -79.1, "Competitor slashed spend by 79%; failed to scale"],
        ["Sep 2026", "Paid Orders Delivered", 801.0, 7563.0, 7563.0, 7563.0, 13778.0, -89.4, "Catastrophic collapse: tracking deleted on Sep 18"],
        ["Sep 2026", "Blended Paid CPA", 782.84, 290.50, 290.50, 290.50, 338.54, 169.5, "CPA inflated +169% due to deleted purchase event"],
        ["Sep 2026", "Google Orders / CPA", "42 / ₹7,569", "4,706 / ₹425", "4,706 / ₹425", "4,706 / ₹425", "7,778 / ₹450", 1680.9, "Purchase-2026 removed by competitor on Sep 18"],
        ["Sep 2026", "Shopify Total Orders", 3112.0, 10327.0, 10327.0, 10327.0, 16542.0, -69.9, "Store orders collapsed -70% from August baseline"],
        ["Sep 2026", "Shopify Gross Sales", 3601597.28, 8922550.0, 8922550.0, 8922550.0, 13564258.0, -59.6, "Store survived on 51.8% existing returning customers"],
        
        # October 2026
        ["Oct 2026 (Festive)", "Total Paid Ad Spend", 4246579.26, 3300000.0, 3000000.0, 3000000.0, 7000000.0, 41.6, "Overspent Plan C by ₹12.5L to chase festive volume"],
        ["Oct 2026 (Festive)", "Paid Orders Delivered", 7298.49, 8666.0, 7878.0, 7878.0, 17574.0, -7.4, "Volume close to Plan C (-7.4%), but at massive cost"],
        ["Oct 2026 (Festive)", "Blended Paid CPA", 581.84, 280.57, 274.76, 274.76, 337.31, 111.8, "CPA doubled (+112% higher than Plan C target ₹275)"],
        ["Oct 2026 (Festive)", "Meta Ads CPA", 532.42, 336.00, 336.00, 336.00, 343.00, 58.5, "All-time record Meta CPA: ASC cannibalization & DPA"],
        ["Oct 2026 (Festive)", "Google Ads CPA", 636.72, 408.00, 408.00, 408.00, 441.00, 56.1, "404 dead links & Glam+ copy-paste errors burned ₹80K+"],
        ["Oct 2026 (Festive)", "Shopify Total Orders", 9143.0, 11762.0, 10919.0, 10919.0, 20752.0, -16.3, "Diwali month delivered fewer orders than July (13.4K)"],
        ["Oct 2026 (Festive)", "Net ROAS", 2.14, 3.14, 3.14, 3.21, 2.43, -31.8, "Sub-optimal revenue yield due to high acquisition cost"],

        # November 2026 (Paced Full Month)
        ["Nov 2026 (Paced)", "Total Paid Ad Spend", 3182243.0, 3630000.0, 3000000.0, 3000000.0, 8750000.0, 6.1, "Spend aligned to Plan C budget (₹30L – ₹31.8L)"],
        ["Nov 2026 (Paced)", "Paid Orders Delivered", 7183.0, 9930.0, 8206.0, 8206.0, 22415.0, -12.5, "Pacing ~12.5% below Plan C volume target"],
        ["Nov 2026 (Paced)", "Blended Paid CPA", 443.00, 270.96, 259.72, 259.72, 335.62, 70.6, "CPA recovering slightly to ₹443, still +70% above Plan C"],
        ["Nov 2026 (Paced)", "Shopify Total Orders", 7730.0, 13397.0, 11551.0, 11551.0, 26071.0, -33.1, "Run-rate stagnant at ~260 orders/day vs target 440+"],
        ["Nov 2026 (Paced)", "Net ROAS", 2.80, 3.32, 3.33, 3.46, 2.44, -15.9, "Recovering towards 2.8x, but lagging 3.3x+ target"]
    ]

    r_start = 5
    for r_idx, row in enumerate(comparison_data, r_start):
        for c_idx, val in enumerate(row, 1):
            cell = ws1.cell(r_idx, c_idx, val)
            cell.font = font_regular
            cell.border = thin_border
            if c_idx in [1, 2]:
                cell.alignment = Alignment(horizontal="left", vertical="center")
            elif c_idx == 8:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                cell.number_format = "+0.0%;-0.0%"
                if isinstance(val, (int, float)):
                    cell.font = font_red if val > 20 or val < -20 else font_green
            elif c_idx == 9:
                cell.alignment = Alignment(horizontal="left", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                if isinstance(val, float) and val > 1000:
                    cell.number_format = "₹#,##0"
                elif isinstance(val, float) and val < 10:
                    cell.number_format = "0.00x"
                elif isinstance(val, float):
                    cell.number_format = "₹#,##0.00"

    # Adjust widths
    for col in ws1.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws1.column_dimensions[col_letter].width = max(max_len + 3, 14)
    ws1.column_dimensions['A'].width = 18
    ws1.column_dimensions['B'].width = 24
    ws1.column_dimensions['I'].width = 46

    # -------------------------------------------------------------
    # POPULATE SHEET 2: Next 6-Month Recovery Forecast
    # -------------------------------------------------------------
    ws2["A1"] = "FABB6 (Glanzzkart Pvt Ltd) — Next 6-Month Account Turnaround & Scaled Recovery Forecast"
    ws2["A1"].font = font_title
    ws2["A2"] = "Forecast Period: December 2026 – May 2027 | Baseline: Current Run-Rate (~₹31L Spend, ~7.2K Paid Orders, ₹443 CPA)"
    ws2["A2"].font = font_sub

    headers2 = [
        "Month", "Focus / Operational Phase", "Google Ads Budget (₹)", "Meta Ads Budget (₹)", "Total Paid Spend (₹)",
        "Google Target CPA (₹)", "Meta Target CPA (₹)", "Blended Paid CPA (₹)", "Google Paid Orders", "Meta Paid Orders",
        "Total Paid Purchases", "Returning / Organic Orders", "Total Shopify Orders", "Average Daily Orders",
        "Target AOV (₹)", "Projected Gross Sales (₹)", "Projected Net Revenue (₹)", "Blended Net ROAS"
    ]
    for col_idx, h in enumerate(headers2, 1):
        c = ws2.cell(4, col_idx, h)
        c.font = font_header
        c.fill = navy_fill
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    # 6 Month Forecast Data
    recovery_data = [
        # Dec 2026 (Month 1): Stabilization & Triage
        ["Dec 2026", "M1: Emergency Triage & Stabilization", 1800000.0, 1200000.0, 3000000.0, 360.0, 333.33, 348.84, 5000.0, 3600.0, 8600.0, 3800.0, 12400.0, 400.0, 920.0, 12648000.0, 11197200.0, 3.73],
        # Jan 2027 (Month 2): Retention & Funnel Restructure
        ["Jan 2027", "M2: Automated Retention & PMax Rebuild", 2100000.0, 1400000.0, 3500000.0, 330.71, 301.08, 318.18, 6350.0, 4650.0, 11000.0, 4200.0, 15200.0, 490.3, 935.0, 15884000.0, 14057340.0, 4.02],
        # Feb 2027 (Month 3): Rebuilding 600+ Daily Orders
        ["Feb 2027", "M3: Scaled Prospecting & Category Expansion", 2400000.0, 1600000.0, 4000000.0, 303.80, 280.70, 294.12, 7900.0, 5700.0, 13600.0, 4900.0, 18500.0, 660.7, 950.0, 19665000.0, 17403525.0, 4.35],
        # Mar 2027 (Month 4): 750 Orders/Day Run-Rate
        ["Mar 2027", "M4: High-Velocity Creative & Margin Tiers", 2700000.0, 1800000.0, 4500000.0, 285.71, 266.67, 277.78, 9450.0, 6750.0, 16200.0, 5800.0, 22000.0, 709.7, 965.0, 23793000.0, 21056805.0, 4.68],
        # Apr 2027 (Month 5): Omnichannel Compounding
        ["Apr 2027", "M5: SEO + Paid + Retention Compounding", 3000000.0, 2000000.0, 5000000.0, 272.73, 256.41, 265.96, 11000.0, 7800.0, 18800.0, 6700.0, 25500.0, 850.0, 980.0, 27930000.0, 24718050.0, 4.94],
        # May 2027 (Month 6): 1,000 Orders/Day Scale Target
        ["May 2027", "M6: Scale Peak (1,000 Daily Orders Target)", 3300000.0, 2200000.0, 5500000.0, 261.90, 247.19, 255.81, 12600.0, 8900.0, 21500.0, 8000.0, 29500.0, 951.6, 1000.0, 32745000.0, 28979325.0, 5.27]
    ]

    r_start2 = 5
    for r_idx, row in enumerate(recovery_data, r_start2):
        for c_idx, val in enumerate(row, 1):
            cell = ws2.cell(r_idx, c_idx, val)
            cell.font = font_regular
            cell.border = thin_border
            if c_idx in [1, 2]:
                cell.alignment = Alignment(horizontal="left", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                if c_idx in [3, 4, 5, 16, 17]:
                    cell.number_format = "₹#,##0"
                elif c_idx in [6, 7, 8, 15]:
                    cell.number_format = "₹#,##0.00"
                elif c_idx in [9, 10, 11, 12, 13]:
                    cell.number_format = "#,##0"
                elif c_idx == 14:
                    cell.number_format = "#,##0.0"
                elif c_idx == 18:
                    cell.number_format = "0.00x"
                    cell.font = font_green

    # Add Cumulative 6-Month Total Row
    tot_row_idx = r_start2 + len(recovery_data)
    ws2.cell(tot_row_idx, 1, "6-Month Total / Avg").font = font_bold
    ws2.cell(tot_row_idx, 2, "H1 2027 Scaled Turnaround Program").font = font_bold
    ws2.cell(tot_row_idx, 3, sum(r[2] for r in recovery_data)).number_format = "₹#,##0"
    ws2.cell(tot_row_idx, 4, sum(r[3] for r in recovery_data)).number_format = "₹#,##0"
    ws2.cell(tot_row_idx, 5, sum(r[4] for r in recovery_data)).number_format = "₹#,##0"
    
    tot_spend = sum(r[4] for r in recovery_data)
    tot_paid_pur = sum(r[10] for r in recovery_data)
    tot_orders = sum(r[12] for r in recovery_data)
    tot_net_rev = sum(r[16] for r in recovery_data)
    
    ws2.cell(tot_row_idx, 8, tot_spend / tot_paid_pur).number_format = "₹#,##0.00"
    ws2.cell(tot_row_idx, 9, sum(r[8] for r in recovery_data)).number_format = "#,##0"
    ws2.cell(tot_row_idx, 10, sum(r[9] for r in recovery_data)).number_format = "#,##0"
    ws2.cell(tot_row_idx, 11, tot_paid_pur).number_format = "#,##0"
    ws2.cell(tot_row_idx, 12, sum(r[11] for r in recovery_data)).number_format = "#,##0"
    ws2.cell(tot_row_idx, 13, tot_orders).number_format = "#,##0"
    ws2.cell(tot_row_idx, 14, tot_orders / 181).number_format = "#,##0.0"
    ws2.cell(tot_row_idx, 16, sum(r[15] for r in recovery_data)).number_format = "₹#,##0"
    ws2.cell(tot_row_idx, 17, tot_net_rev).number_format = "₹#,##0"
    ws2.cell(tot_row_idx, 18, tot_net_rev / tot_spend).number_format = "0.00x"
    
    for c_idx in range(1, 19):
        c = ws2.cell(tot_row_idx, c_idx)
        c.fill = light_blue_fill
        c.font = font_bold
        c.border = thin_border

    # Adjust widths Sheet 2
    for col in ws2.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws2.column_dimensions[col_letter].width = max(max_len + 3, 14)
    ws2.column_dimensions['A'].width = 14
    ws2.column_dimensions['B'].width = 38

    output_path = r"C:\Users\test\Videos\Office\reports\FABB6_Next_6Month_Recovery_Forecast_Dec2026_May2027.xlsx"
    wb.save(output_path)
    print(f"Saved master forecast comparison & next 6M recovery workbook to: {output_path}")

    # Also save copy to artifacts directory
    artifact_path = r"C:\Users\test\.gemini\antigravity\brain\29f77e0a-5ed5-4d24-842c-443d9957274c\FABB6_Next_6Month_Recovery_Forecast_Dec2026_May2027.xlsx"
    wb.save(artifact_path)
    print(f"Saved copy to artifact directory: {artifact_path}")

if __name__ == '__main__':
    build_forecast_workbook()
