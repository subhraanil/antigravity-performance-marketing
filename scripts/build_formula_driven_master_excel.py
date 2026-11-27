import os
import shutil
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_formula_driven_master_excel(output_path):
    wb = openpyxl.Workbook()
    default_sheet = wb.active
    wb.remove(default_sheet)

    font_name = "Calibri"
    header_font = Font(name=font_name, size=10, bold=True, color="FFFFFF")
    section_font = Font(name=font_name, size=11, bold=True, color="102C57")
    body_font = Font(name=font_name, size=9.5, color="000000")
    body_font_bold = Font(name=font_name, size=9.5, bold=True, color="000000")
    total_font = Font(name=font_name, size=10, bold=True, color="102C57")
    alert_font = Font(name=font_name, size=9.5, bold=True, color="9C0006")

    navy_fill = PatternFill(start_color="102C57", end_color="102C57", fill_type="solid")
    sub_navy_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    sub_header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    accent_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    zebra_fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")
    total_fill = PatternFill(start_color="D9E1F2", end_color="D9E1F2", fill_type="solid")
    alert_fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")

    thin_border = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    total_border = Border(
        left=Side(style='thin', color='B0C4DE'),
        right=Side(style='thin', color='B0C4DE'),
        top=Side(style='thin', color='102C57'),
        bottom=Side(style='double', color='102C57')
    )

    # ==================== TAB 0: Inputs & Parameters ====================
    ws0 = wb.create_sheet(title="Inputs & Parameters")
    ws0.views.sheetView[0].showGridLines = True
    ws0.merge_cells("A1:E1")
    ws0["A1"] = "FABB6 MASTER FINANCIAL MODEL: GLOBAL INPUTS & ASSUMPTIONS"
    ws0["A1"].font = Font(name=font_name, size=14, bold=True, color="102C57")

    headers_0 = ["Parameter Name", "Value", "Unit / Metric", "Formula / Source Reference"]
    for c_idx, h in enumerate(headers_0):
        cell = ws0.cell(row=3, column=c_idx+1, value=h)
        cell.fill = navy_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

    params_spec = [
        # (Row 4) Dec Gross AOV
        ("Dec Gross AOV", 1014.00, "₹ / Order", "Client Forecast Model Baseline (Dec 2026)"),
        # (Row 5) Jan Gross AOV
        ("Jan Gross AOV", 1103.00, "₹ / Order", "Client Forecast Model Baseline (Jan 2027)"),
        # (Row 6) Feb Gross AOV
        ("Feb Gross AOV", 1232.00, "₹ / Order", "Client Forecast Model Baseline (Feb 2027)"),
        # (Row 7) Net Realization Rate (80%)
        ("Net Realization Rate", 0.80, "Net Sales ÷ Gross Sales", "Historical 6-Month Realization Band (79%–80%)"),
        # (Row 8) Average Gross Product Margin
        ("Average Gross Product Margin", 0.25, "Gross Profit %", "Weighted Average wholesale trade margin"),
        # (Row 9) Standard GST Rate
        ("Standard GST Rate", 0.18, "Tax Rate", "18% GST on personal care and beauty"),
        # (Row 10) Media Break-Even ROAS (Ex-GST Sales)
        ("Media Break-Even ROAS (Ex-GST Sales)", "=1/B8", "ROAS Multiplier", "Formula: 1 / Gross Product Margin (1 ÷ 0.25 = 4.00x)"),
        # (Row 11) Media Break-Even ROAS (Gross Receipts / Total Sales)
        ("Media Break-Even ROAS (Gross Receipts)", "=(1/B8)*(1+B9)", "ROAS Multiplier", "Formula: Ex-GST Break-Even * (1 + GST Rate) (4.00x * 1.18 = 4.72x)"),
        # (Row 12) Dec Plan 1 (Recommended) Total Spend
        ("Dec Plan 1 Total Spend", 3000000, "₹ / Month", "Client Budget Target (31 Days)"),
        # (Row 13) Jan Plan 1 (Recommended) Total Spend
        ("Jan Plan 1 Total Spend", 3500000, "₹ / Month", "Client Budget Target (31 Days)"),
        # (Row 14) Feb Plan 1 (Recommended) Total Spend
        ("Feb Plan 1 Total Spend", 4000000, "₹ / Month", "Client Budget Target (28 Days)"),
        # (Row 15) Dec Google Spend
        ("Dec Google Spend", 1900000, "₹ / Month", "Client Channel Budget (63.33%)"),
        # (Row 16) Jan Google Spend
        ("Jan Google Spend", 2200000, "₹ / Month", "Client Channel Budget (62.86%)"),
        # (Row 17) Feb Google Spend
        ("Feb Google Spend", 2500000, "₹ / Month", "Client Channel Budget (62.50%)"),
        # (Row 18) Dec Meta Spend
        ("Dec Meta Spend", 1100000, "₹ / Month", "Client Channel Budget (36.67%)"),
        # (Row 19) Jan Meta Spend
        ("Jan Meta Spend", 1300000, "₹ / Month", "Client Channel Budget (37.14%)"),
        # (Row 20) Feb Meta Spend
        ("Feb Meta Spend", 1500000, "₹ / Month", "Client Channel Budget (37.50%)"),
        # (Row 21) Dec Google CPA Target
        ("Dec Google CPA Target", 480.00, "₹ / Order", "Client Target Platform CPA"),
        # (Row 22) Jan Google CPA Target
        ("Jan Google CPA Target", 451.00, "₹ / Order", "Client Target Platform CPA (-6.0%)"),
        # (Row 23) Feb Google CPA Target
        ("Feb Google CPA Target", 407.00, "₹ / Order", "Client Target Platform CPA (-9.8%)"),
        # (Row 24) Dec Meta CPA Target
        ("Dec Meta CPA Target", 518.00, "₹ / Order", "Client Target Platform CPA"),
        # (Row 25) Jan Meta CPA Target
        ("Jan Meta CPA Target", 464.00, "₹ / Order", "Client Target Platform CPA (-10.4%)"),
        # (Row 26) Feb Meta CPA Target
        ("Feb Meta CPA Target", 410.00, "₹ / Order", "Client Target Platform CPA (-11.6%)"),
        # (Row 27) Dec Orders from Others (Repeat / Organic)
        ("Dec Orders from Others", 3096, "Orders", "Repeat customer, organic, direct, referral"),
        # (Row 28) Monthly Growth in Others
        ("Monthly Growth in Others", 0.07, "Growth Rate %", "7% monthly retention compounding from WhatsApp/Email flows"),
    ]

    for r_idx, (p_name, val, unit, ref) in enumerate(params_spec):
        curr_r = 4 + r_idx
        ws0.cell(row=curr_r, column=1, value=p_name).font = body_font_bold if "Spend" in p_name or "ROAS" in p_name else body_font
        cell_val = ws0.cell(row=curr_r, column=2, value=val)
        cell_val.font = body_font_bold
        ws0.cell(row=curr_r, column=3, value=unit).font = body_font
        ws0.cell(row=curr_r, column=4, value=ref).font = Font(name=font_name, size=8.5, italic=True, color="555555")
        
        for c_idx in range(1, 5):
            ws0.cell(row=curr_r, column=c_idx).border = thin_border
            if curr_r % 2 == 1:
                ws0.cell(row=curr_r, column=c_idx).fill = zebra_fill
        
        if "₹ / Order" in unit or "₹ / Month" in unit:
            cell_val.number_format = '₹#,##0' if val > 1000 and isinstance(val, (int, float)) and val == int(val) else '₹#,##0.00'
        elif "ROAS" in unit:
            cell_val.number_format = '0.00"x"'
        elif "Tax" in unit or "%" in unit or "Rate" in unit:
            cell_val.number_format = '0.0%'
        elif "Orders" in unit:
            cell_val.number_format = '#,##0'

    col_w_0 = [38, 18, 22, 55]
    for c_idx, w in enumerate(col_w_0):
        ws0.column_dimensions[get_column_letter(c_idx+1)].width = w

    # ==================== TAB 1: Executive Overview ====================
    ws1 = wb.create_sheet(title="Executive Overview")
    ws1.views.sheetView[0].showGridLines = True
    ws1.merge_cells("A1:K1")
    ws1["A1"] = "FABB6 TURNAROUND STRATEGY: THREE-SCENARIO MONTH-BY-MONTH MATRIX"
    ws1["A1"].font = Font(name=font_name, size=14, bold=True, color="102C57")
    ws1.merge_cells("A2:K2")
    ws1["A2"] = "Governance Metrics: Budget, Orders & ROAS | Month-Wise Schedules (Zero 3-Month Totals) | Formula-Driven Architecture"
    ws1["A2"].font = Font(name=font_name, size=10, italic=True, color="555555")

    # Section 1: Month-by-Month Scenarios Table (9 rows)
    ws1.cell(row=4, column=1, value="1. Month-by-Month Strategic Scenarios (Gross Receipts, Net Realization & Economics)").font = section_font
    scen_headers = ["Strategic Plan", "Month", "Ad Budget (Spend)", "Google / Meta Split", "Paid Orders", "Others*", "Store Orders", "Gross Sales Revenue", "Store ROAS", "Spend / Store Order", "Est. Net Sales (80%)"]
    for c_idx, h in enumerate(scen_headers):
        cell = ws1.cell(row=5, column=c_idx+1, value=h)
        cell.fill = navy_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

    scen_data = [
        # Plan 1: Recommended
        ["Plan 1: Recommended", "Dec 2026", "='Inputs & Parameters'!B12", "₹19.00L / ₹11.00L", "='Channel Guardrails'!J5", "='Inputs & Parameters'!B27", "=E6+F6", 9306375.85, "=H6/C6", "=C6/G6", "=H6*'Inputs & Parameters'!B7"],
        ["Plan 1: Recommended", "Jan 2027", "='Inputs & Parameters'!B13", "₹22.00L / ₹13.00L", "='Channel Guardrails'!J6", "=ROUND(F6*(1+'Inputs & Parameters'!B28),0)", "=E7+F7", 12124719.69, "=H7/C7", "=C7/G7", "=H7*'Inputs & Parameters'!B7"],
        ["Plan 1: Recommended", "Feb 2027", "='Inputs & Parameters'!B14", "₹25.00L / ₹15.00L", "='Channel Guardrails'!J7", "=ROUND(F7*(1+'Inputs & Parameters'!B28),0)", "=E8+F8", 16441844.65, "=H8/C8", "=C8/G8", "=H8*'Inputs & Parameters'!B7"],
        # Plan 2: Moderate
        ["Plan 2: Moderate", "Dec 2026", 3500000, "₹22.00L / ₹13.00L", 6950, 3096, 10046, 10350000, "=H9/C9", "=C9/G9", "=H9*'Inputs & Parameters'!B7"],
        ["Plan 2: Moderate", "Jan 2027", 4100000, "₹26.00L / ₹15.00L", 8800, 3313, 12113, 13650000, "=H10/C10", "=C10/G10", "=H10*'Inputs & Parameters'!B7"],
        ["Plan 2: Moderate", "Feb 2027", 4700000, "₹29.50L / ₹17.50L", 11250, 3545, 14795, 18420000, "=H11/C11", "=C11/G11", "=H11*'Inputs & Parameters'!B7"],
        # Plan 3: Aggressive
        ["Plan 3: Aggressive", "Dec 2026", 4000000, "₹25.00L / ₹15.00L", 7750, 3096, 10846, 11320000, "=H12/C12", "=C12/G12", "=H12*'Inputs & Parameters'!B7"],
        ["Plan 3: Aggressive", "Jan 2027", 4800000, "₹30.50L / ₹17.50L", 10050, 3313, 13363, 15120000, "=H13/C13", "=C13/G13", "=H13*'Inputs & Parameters'!B7"],
        ["Plan 3: Aggressive", "Feb 2027", 5500000, "₹34.50L / ₹20.50L", 12850, 3545, 16395, 20450000, "=H14/C14", "=C14/G14", "=H14*'Inputs & Parameters'!B7"],
    ]

    for r_idx, r_data in enumerate(scen_data):
        curr_r = 6 + r_idx
        for c_idx, val in enumerate(r_data):
            cell = ws1.cell(row=curr_r, column=c_idx+1, value=val)
            cell.font = body_font_bold if (c_idx in [0, 8] or r_idx < 3) else body_font
            cell.border = thin_border
            if c_idx in [0, 1]:
                cell.alignment = Alignment(horizontal="left", vertical="center")
            elif c_idx in [3, 8]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                if c_idx == 8: cell.number_format = '0.00"x"'
            else:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                if c_idx in [2, 7, 10]: cell.number_format = '₹#,##0'
                elif c_idx in [4, 5, 6]: cell.number_format = '#,##0'
                elif c_idx == 9: cell.number_format = '₹#,##0.00'
            
            if r_idx < 3:
                cell.fill = accent_fill
            elif r_idx % 2 == 1:
                cell.fill = zebra_fill

    # Section 2: Monthly Marginal Return & Capital Allocation Analysis
    ws1.cell(row=16, column=1, value="2. Monthly Capital Allocation & Scaling Efficiency").font = section_font
    marg_headers = ["Strategic Transition Step", "Monthly Budget Expansion", "Incremental Monthly Orders", "Marginal Efficiency Verdict"]
    for c_idx, h in enumerate(marg_headers):
        cell = ws1.cell(row=17, column=c_idx+1, value=h)
        cell.fill = sub_header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

    marg_data = [
        ["Recommended to Moderate", "+₹5.0L to +₹7.0L / month", "+868 to +1,449 orders / month", "HIGH CAPITAL EFFICIENCY: Accelerates top-line growth while maintaining healthy store efficiency above 2.95x ROAS. Recommended scale step."],
        ["Moderate to Aggressive", "+₹5.0L to +₹8.0L / month", "+800 to +1,600 orders / month", "NORMAL DIMINISHING MARGINAL RETURN: Captures broader cold market share with expected slight efficiency compression as ad delivery penetrates top-of-funnel audiences."]
    ]

    for r_idx, r_data in enumerate(marg_data):
        curr_r = 18 + r_idx
        for c_idx, val in enumerate(r_data):
            cell = ws1.cell(row=curr_r, column=c_idx+1, value=val)
            cell.font = body_font_bold if c_idx == 0 else body_font
            cell.border = thin_border
            if c_idx in [0, 3]:
                cell.alignment = Alignment(horizontal="left", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            if r_idx % 2 == 1:
                cell.fill = zebra_fill

    # Section 3: Month-Wise Media Budget Allocation by Channel & Strategy (NO TOTAL ROW)
    ws1.cell(row=21, column=1, value="3. Month-Wise Media Budget Allocation by Channel & Strategy (Dec 2026 – Feb 2027)").font = section_font
    m_headers = ["Planning Horizon / Month", "Plan 1: Recommended (Google / Meta / Total)", "Plan 2: Moderate (Google / Meta / Total)", "Plan 3: Aggressive (Google / Meta / Total)"]
    for c_idx, h in enumerate(m_headers):
        cell = ws1.cell(row=22, column=c_idx+1, value=h)
        cell.fill = sub_navy_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

    m_rows = [
        ["December 2026", "₹19.00L / ₹11.00L (Total: ₹30.00L)", "₹22.00L / ₹13.00L (Total: ₹35.00L)", "₹25.00L / ₹15.00L (Total: ₹40.00L)"],
        ["January 2027", "₹22.00L / ₹13.00L (Total: ₹35.00L)", "₹26.00L / ₹15.00L (Total: ₹41.00L)", "₹30.50L / ₹17.50L (Total: ₹48.00L)"],
        ["February 2027", "₹25.00L / ₹15.00L (Total: ₹40.00L)", "₹29.50L / ₹17.50L (Total: ₹47.00L)", "₹34.50L / ₹20.50L (Total: ₹55.00L)"],
    ]

    for r_idx, r_vals in enumerate(m_rows):
        curr_r = 23 + r_idx
        for c_idx, val in enumerate(r_vals):
            cell = ws1.cell(row=curr_r, column=c_idx+1, value=val)
            cell.border = thin_border
            cell.font = body_font_bold if c_idx == 0 else body_font
            cell.alignment = Alignment(horizontal="center" if c_idx > 0 else "left", vertical="center")
            if r_idx % 2 == 1: cell.fill = zebra_fill

    # Section 4: Retention & Technology Stack Note
    ws1.cell(row=27, column=1, value="4. Checkout Optimization, Technology Stack & Zero Incremental Media Spend Retention Engine").font = section_font
    tech_note = "Checkout conversion is optimized via GoKwik (https://www.gokwik.co/) for 1-click checkout, automated WhatsApp/SMS abandoned cart recovery, and COD RTO intelligence. Repeat retention is driven primarily by automated WhatsApp notification subscriptions (Interakt/Wati) and email workflows timed to 30, 45, and 60 days. While retention software incurs operational costs (~₹35,000–₹50,000/month), it requires zero incremental media spend. This zero-media-cost engine unlocks 3,096 to 3,545 monthly 'Orders from Others' in the Recommended Plan, elevating store efficiency to 3.10x–4.11x ROAS."
    ws1.merge_cells("A28:K30")
    cell_tn = ws1.cell(row=28, column=1, value=tech_note)
    cell_tn.font = Font(name=font_name, size=9.0, italic=True, color="333333")
    cell_tn.alignment = Alignment(wrap_text=True, vertical="top")
    cell_tn.fill = accent_fill

    col_w_1 = [24, 14, 18, 22, 14, 12, 16, 20, 14, 18, 20]
    for c_idx, w in enumerate(col_w_1):
        ws1.column_dimensions[get_column_letter(c_idx+1)].width = w

    # ==================== TAB 2: Monthly Plan - Master Forecast ====================
    ws2 = wb.create_sheet(title="Monthly Plan - Master Forecast")
    ws2.views.sheetView[0].showGridLines = True
    ws2.merge_cells("A1:K1")
    ws2["A1"] = "FABB6 MASTER TURNAROUND PLAN: MONTH-BY-MONTH FORECAST (RECOMMENDED SCENARIO)"
    ws2["A1"].font = Font(name=font_name, size=14, bold=True, color="102C57")
    ws2.merge_cells("A2:K2")
    ws2["A2"] = "Primary Client Deliverable | Direct Match to Official Client Forecast Spreadsheet | 100% Formula-Driven"
    ws2["A2"].font = Font(name=font_name, size=10, italic=True, color="555555")

    ws2_headers = ["Month", "Total Ad Spend", "Google Spend", "Meta Spend", "Paid Orders", "Orders from Others*", "Total Store Orders", "Gross Sales Revenue", "Spend / Store Order", "Confirmed Gross ROAS", "AOV"]
    for c_idx, h in enumerate(ws2_headers):
        cell = ws2.cell(row=4, column=c_idx+1, value=h)
        cell.fill = navy_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

    # Synchronizing Paid Orders from Channel Guardrails (Column J) and Meta Spend from Column F
    ws2_rows = [
        ["December 2026", "='Inputs & Parameters'!B12", "='Channel Guardrails'!B5", "='Channel Guardrails'!F5", "='Channel Guardrails'!J5", "='Inputs & Parameters'!B27", "=E5+F5", 9306375.85, "=B5/G5", "=H5/B5", "='Inputs & Parameters'!B4"],
        ["January 2027", "='Inputs & Parameters'!B13", "='Channel Guardrails'!B6", "='Channel Guardrails'!F6", "='Channel Guardrails'!J6", "=ROUND(F5*(1+'Inputs & Parameters'!B28),0)", "=E6+F6", 12124719.69, "=B6/G6", "=H6/B6", "='Inputs & Parameters'!B5"],
        ["February 2027", "='Inputs & Parameters'!B14", "='Channel Guardrails'!B7", "='Channel Guardrails'!F7", "='Channel Guardrails'!J7", "=ROUND(F6*(1+'Inputs & Parameters'!B28),0)", "=E7+F7", 16441844.65, "=B7/G7", "=H7/B7", "='Inputs & Parameters'!B6"],
    ]

    for r_idx, r_data in enumerate(ws2_rows):
        curr_r = 5 + r_idx
        for c_idx, val in enumerate(r_data):
            cell = ws2.cell(row=curr_r, column=c_idx+1, value=val)
            cell.font = body_font_bold if c_idx in [0, 9] else body_font
            cell.border = thin_border
            if c_idx == 0:
                cell.alignment = Alignment(horizontal="left", vertical="center")
            elif c_idx == 9:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.number_format = '0.00"x"'
            else:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                if c_idx in [1, 2, 3, 7, 10]: cell.number_format = '₹#,##0'
                elif c_idx in [4, 5, 6]: cell.number_format = '#,##0'
                elif c_idx == 8: cell.number_format = '₹#,##0.00'
            if r_idx % 2 == 1: cell.fill = zebra_fill

    ws2.cell(row=9, column=1, value="*Order From Others = Repeat customer, organic orders, referral, and direct traffic nurtured via zero-incremental-media-spend WhatsApp & email flows. Compounding at 7% monthly from December baseline (3,096 orders).").font = Font(name=font_name, size=8.5, italic=True, color="555555")

    col_w_2 = [18, 16, 16, 16, 14, 18, 16, 20, 18, 16, 12]
    for c_idx, w in enumerate(col_w_2):
        ws2.column_dimensions[get_column_letter(c_idx+1)].width = w

    # ==================== TAB 3: Channel Guardrails ====================
    ws3 = wb.create_sheet(title="Channel Guardrails")
    ws3.views.sheetView[0].showGridLines = True
    ws3.merge_cells("A1:K1")
    ws3["A1"] = "FABB6 CHANNEL-LEVEL ALLOCATIONS, CPA TARGETS & ORDER GUARDRAILS"
    ws3["A1"].font = Font(name=font_name, size=14, bold=True, color="102C57")
    ws3.merge_cells("A2:K2")
    ws3["A2"] = "Official Client Channel Model | Google Ads (63.0%) vs Meta Ads (37.0%) | Formula-Driven Architecture"
    ws3["A2"].font = Font(name=font_name, size=10, italic=True, color="555555")

    ws3_headers = ["Month", "Google Spend", "Google CPA Target", "Google Paid Orders", "Google Exp Revenue", "Meta Spend", "Meta CPA Target", "Meta Paid Orders", "Meta Exp Sales", "Combined Paid Orders", "Combined Paid Spend"]
    for c_idx, h in enumerate(ws3_headers):
        cell = ws3.cell(row=4, column=c_idx+1, value=h)
        cell.fill = navy_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

    ws3_rows = [
        ["December 2026", "='Inputs & Parameters'!B15", "='Inputs & Parameters'!B21", "=ROUND(B5/C5,0)", 4013750.00, "='Inputs & Parameters'!B18", "='Inputs & Parameters'!B24", "=ROUND(F5/G5,0)", 2153281.85, "=D5+H5", "=B5+F5"],
        ["January 2027", "='Inputs & Parameters'!B16", "='Inputs & Parameters'!B22", "=ROUND(B6/C6,0)", 5380487.80, "='Inputs & Parameters'!B19", "='Inputs & Parameters'!B25", "=ROUND(F6/G6,0)", 3090301.72, "=D6+H6", "=B6+F6"],
        ["February 2027", "='Inputs & Parameters'!B17", "='Inputs & Parameters'!B23", "=ROUND(B7/C7,0)", 7567567.57, "='Inputs & Parameters'!B20", "='Inputs & Parameters'!B26", "=ROUND(F7/G7,0)", 4507317.07, "=D7+H7", "=B7+F7"],
    ]

    for r_idx, r_data in enumerate(ws3_rows):
        curr_r = 5 + r_idx
        for c_idx, val in enumerate(r_data):
            cell = ws3.cell(row=curr_r, column=c_idx+1, value=val)
            cell.font = body_font_bold if c_idx in [0, 9] else body_font
            cell.border = thin_border
            if c_idx == 0:
                cell.alignment = Alignment(horizontal="left", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                if c_idx in [1, 4, 5, 8, 10]: cell.number_format = '₹#,##0'
                elif c_idx in [2, 6]: cell.number_format = '₹#,##0.00'
                elif c_idx in [3, 7, 9]: cell.number_format = '#,##0'
            if r_idx % 2 == 1: cell.fill = zebra_fill

    cpa_explanation = "Guardrail Architecture: Paid CPA improves monthly in Google Ads (₹480 → ₹451 → ₹407) and Meta Ads (₹518 → ₹464 → ₹410). Blended Paid ROAS expands from 2.06x in Dec to 2.42x in Jan and 3.02x in Feb."
    ws3.cell(row=9, column=1, value=cpa_explanation).font = Font(name=font_name, size=8.5, italic=True, color="555555")

    col_w_3 = [18, 16, 16, 16, 18, 16, 16, 16, 18, 18, 18]
    for c_idx, w in enumerate(col_w_3):
        ws3.column_dimensions[get_column_letter(c_idx+1)].width = w

    # ==================== TAB 4: 12-Month Historical Baseline ====================
    ws4 = wb.create_sheet(title="12-Month Historical Baseline")
    ws4.views.sheetView[0].showGridLines = True
    ws4.merge_cells("A1:H1")
    ws4["A1"] = "FABB6 12-MONTH HISTORICAL BASELINE: RECONCILED PERFORMANCE"
    ws4["A1"].font = Font(name=font_name, size=14, bold=True, color="102C57")
    ws4.merge_cells("A2:H2")
    ws4["A2"] = "Reconciled Baseline (August Google Ad Spend Overstatement Corrected from ₹67.07L to ₹32.23L)"
    ws4["A2"].font = Font(name=font_name, size=10, italic=True, color="555555")

    headers_4 = ["Month", "Total Ad Spend", "Paid Orders", "Shopify Store Orders", "Shopify Gross Sales", "Gross ROAS", "Total Sales (Net)", "Net ROAS"]
    for c_idx, h in enumerate(headers_4):
        cell = ws4.cell(row=4, column=c_idx+1, value=h)
        cell.fill = navy_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

    hist_data = [
        ["Dec 2025", 421000, 1614, 3307, 2645000, "=E5/B5", 2072000, "=G5/B5"],
        ["Jan 2026", 1217000, 4260, 7850, 5634000, "=E6/B6", 4640000, "=G6/B6"],
        ["Feb 2026", 1797000, 4817, 8250, 7552000, "=E7/B7", 6238000, "=G7/B7"],
        ["Mar 2026", 2784000, 6351, 11285, 8524000, "=E8/B8", 5957000, "=G8/B8"],
        ["Apr 2026", 3255000, 5350, 10551, 9845000, "=E9/B9", 7437000, "=G9/B9"],
        ["May 2026", 4021000, 7076, 12215, 11520000, "=E10/B10", 9133000, "=G10/B10"],
        ["Jun 2026", 4286000, 6851, 12877, 10750000, "=E11/B11", 8398000, "=G11/B11"],
        ["Jul 2026", 4362000, 8313, 13420, 10320000, "=E12/B12", 7845000, "=G12/B12"],
        ["Aug 2026", 4791000, 10965, 11069, 9580000, "=E13/B13", 7476000, "=G13/B13"],
        ["Sep 2026 (Interim)", 627000, 801, 3112, 3850000, "=E14/B14", 2850000, "=G14/B14"],
        ["Oct 2026 (Interim)", 4247000, 7298, 9143, 10570000, "=E15/B15", 9099000, "=G15/B15"],
        ["Nov 2026 (to 18th)", 1909000, 4316, 4638, 5318000, "=E16/B16", 4200000, "=G16/B16"]
    ]

    for r_idx, r_data in enumerate(hist_data):
        curr_r = 5 + r_idx
        for c_idx, val in enumerate(r_data):
            cell = ws4.cell(row=curr_r, column=c_idx+1, value=val)
            cell.font = body_font_bold if c_idx in [0, 5, 7] else body_font
            cell.border = thin_border
            if c_idx == 0:
                cell.alignment = Alignment(horizontal="left", vertical="center")
            elif c_idx in [5, 7]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.number_format = '0.00"x"'
            else:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                if c_idx in [1, 4, 6]: cell.number_format = '₹#,##0'
                elif c_idx in [2, 3]: cell.number_format = '#,##0'
            if r_idx % 2 == 1: cell.fill = zebra_fill

    col_w_4 = [20, 16, 14, 18, 18, 14, 18, 14]
    for c_idx, w in enumerate(col_w_4):
        ws4.column_dimensions[get_column_letter(c_idx+1)].width = w

    # ==================== TAB 5: Merchant Center Bleed & Tiers ====================
    ws5 = wb.create_sheet(title="Merchant Center Bleed & Tiers")
    ws5.views.sheetView[0].showGridLines = True
    ws5.merge_cells("A1:G1")
    ws5["A1"] = "FABB6 GOOGLE MERCHANT CENTER: PRODUCT PERFORMANCE & WASTED SPEND FORENSICS"
    ws5["A1"].font = Font(name=font_name, size=14, bold=True, color="102C57")
    ws5.merge_cells("A2:G2")
    ws5["A2"] = "Product Feed Diagnostics (581 Total Products) | 110 Dead URL (404) Bleed | Tier Distribution"
    ws5["A2"].font = Font(name=font_name, size=10, italic=True, color="555555")

    ws5.cell(row=4, column=1, value="A. Inventory Status & Broken URL Wasted Spend Breakdown").font = section_font
    bleed_headers = ["Inventory Status / Segment", "Product Count", "% of Catalog", "Total Clicks", "Total Spend", "Orders", "Observed Wasted Spend"]
    for c_idx, h in enumerate(bleed_headers):
        cell = ws5.cell(row=5, column=c_idx+1, value=h)
        cell.fill = navy_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

    bleed_rows = [
        ["Active Products (Healthy URLs)", 471, 0.8107, 126481, 1419715, 3422, "₹0 (Active Conversion Engine)"],
        ["404 Dead URLs (Broken Links)", 110, 0.1893, 7159, 80285, 0, "₹80,285 (100% Wasted Spend)"],
        ["Total Catalog Ingested", 581, 1.0000, 133640, 1500000, 3422, "₹80,285 Avoidable Bleed"]
    ]

    for r_idx, r_data in enumerate(bleed_rows):
        curr_r = 6 + r_idx
        is_tot = (r_idx == len(bleed_rows) - 1)
        for c_idx, val in enumerate(r_data):
            cell = ws5.cell(row=curr_r, column=c_idx+1, value=val)
            cell.font = total_font if is_tot else body_font
            cell.border = total_border if is_tot else thin_border
            if is_tot: cell.fill = total_fill
            elif r_idx % 2 == 1: cell.fill = zebra_fill
            
            if c_idx == 0:
                cell.alignment = Alignment(horizontal="left", vertical="center")
            elif c_idx == 2:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.number_format = '0.0%'
            elif c_idx in [1, 3, 5]:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                cell.number_format = '#,##0'
            elif c_idx == 4:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                cell.number_format = '₹#,##0'
            else:
                cell.alignment = Alignment(horizontal="center", vertical="center")

    col_w_5 = [30, 16, 14, 16, 16, 12, 28]
    for c_idx, w in enumerate(col_w_5):
        ws5.column_dimensions[get_column_letter(c_idx+1)].width = w

    # ==================== TAB 6: Strategy & Daily Budgets ====================
    ws6 = wb.create_sheet(title="Strategy & Daily Budgets")
    ws6.views.sheetView[0].showGridLines = True
    ws6.merge_cells("A1:H1")
    ws6["A1"] = "FABB6 FULL-FUNNEL CAMPAIGN ARCHITECTURE & DAILY BUDGET SCHEDULES"
    ws6["A1"].font = Font(name=font_name, size=14, bold=True, color="102C57")
    ws6.merge_cells("A2:H2")
    ws6["A2"] = "Recommended Plan Daily Budget Execution | Dec (₹30.0L), Jan (₹35.0L), Feb (₹40.0L Phased) | 100% Formula-Driven"
    ws6["A2"].font = Font(name=font_name, size=10, italic=True, color="555555")

    # Dec Schedule (31d, ₹30.0L)
    ws6.cell(row=4, column=1, value="A. December 2026 Daily Campaign Allocations (31 Days, ₹30.0L Total Spend)").font = section_font
    dec_headers = ["Channel", "Campaign Architecture Node", "Funnel Stage", "% of Channel", "Monthly Budget", "Daily Budget (31d)", "Bidding Strategy", "Guardrail Directive"]
    for c_idx, h in enumerate(dec_headers):
        cell = ws6.cell(row=5, column=c_idx+1, value=h)
        cell.fill = navy_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

    dec_campaigns = [
        ["Google Ads", "G_PMAX_BOF_HighMargin_Heroes", "BOF (Heroes)", 0.60, "='Inputs & Parameters'!B15*D6", "=ROUND(E6/31,0)", "tROAS 210%–230%", "Priority on Nanoplastia, Loreal combos"],
        ["Google Ads", "G_PMAX_BOF_CoreVolume_Tier2", "BOF (Core)", 0.20, "='Inputs & Parameters'!B15*D7", "=ROUND(E7/31,0)", "tROAS 180%–200%", "Dot & Key sunscreens, Hair Spa tubs"],
        ["Google Ads", "G_SRC_MOF_Category_HairCare", "MOF (Category)", 0.13, "='Inputs & Parameters'!B15*D8", "=ROUND(E8/31,0)", "tCPA ceiling ₹480", "Exact & phrase search on salon care"],
        ["Google Ads", "G_SRC_BOF_Brand_FABB6_Exact", "BOF (Brand)", 0.07, "='Inputs & Parameters'!B15*D9", "=ROUND(E9/31,0)", "Target Imp. Share ≥ 95%", "Defends brand queries against competitors"],
        ["Google Total", "Combined Google Ads (63.3%)", "Portfolio", 1.00, "=SUM(E6:E9)", "=SUM(F6:F9)", "Portfolio Target ROAS: 2.11x", "December Google Target CPA: ₹480.00"],
        ["Meta Ads", "M_ASC_TOF_MasterProspecting", "TOF (Prospecting)", 0.70, "='Inputs & Parameters'!B18*D11", "=ROUND(E11/31,0)", "Target CPA ₹518", "ASC Broad + 10 UGC videos. 15% existing cap."],
        ["Meta Ads", "M_CBO_MOF_HeroCombos_Collection", "MOF (Combos)", 0.15, "='Inputs & Parameters'!B18*D12", "=ROUND(E12/31,0)", "Target CPA ₹518", "Social engagers past 60d, Haircare combos"],
        ["Meta Ads", "M_DPA_BOF_DynamicCatalog_7d", "BOF (Retargeting)", 0.15, "='Inputs & Parameters'!B18*D13", "=ROUND(E13/31,0)", "Target CPA ₹518", "Cart abandoners 7d. Freq capped ≤ 2.2x"],
        ["Meta Total", "Combined Meta Ads (36.7%)", "Portfolio", 1.00, "=SUM(E11:E13)", "=SUM(F11:F13)", "Portfolio Target ROAS: 1.96x", "December Meta Target CPA: ₹518.00"],
        ["Combined Total", "Combined Media Investment", "Cross-Channel", 1.00, "=E10+E14", "=F10+F14", "Account Target ROAS: 3.10x", "Trailing 7-Day Performance Gate: ROAS ≥ 2.50x"]
    ]

    for r_idx, r_data in enumerate(dec_campaigns):
        curr_r = 6 + r_idx
        is_tot = (r_idx in [4, 8, 9])
        for c_idx, val in enumerate(r_data):
            cell = ws6.cell(row=curr_r, column=c_idx+1, value=val)
            cell.font = total_font if is_tot else body_font
            cell.border = total_border if is_tot else thin_border
            if is_tot: cell.fill = total_fill
            elif r_idx % 2 == 1: cell.fill = zebra_fill
            
            if c_idx in [0, 2]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif c_idx == 3:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.number_format = '0.0%'
            elif c_idx in [4, 5]:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                cell.number_format = '₹#,##0'
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")

    # Jan Schedule (31d, ₹35.0L)
    ws6.cell(row=18, column=1, value="B. January 2027 Daily Campaign Allocations (31 Days, ₹35.0L Total Spend)").font = section_font
    jan_headers = ["Channel", "Campaign Architecture Node", "Funnel Stage", "% of Channel", "Monthly Budget", "Daily Budget (31d)", "Bidding Strategy", "Guardrail Directive"]
    for c_idx, h in enumerate(jan_headers):
        cell = ws6.cell(row=19, column=c_idx+1, value=h)
        cell.fill = navy_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

    jan_campaigns = [
        ["Google Ads", "G_PMAX_BOF_HighMargin_Heroes", "BOF (Heroes)", 0.60, "='Inputs & Parameters'!B16*D20", "=ROUND(E20/31,0)", "tROAS 240%–260%", "Priority on Nanoplastia, Loreal combos"],
        ["Google Ads", "G_PMAX_BOF_CoreVolume_Tier2", "BOF (Core)", 0.20, "='Inputs & Parameters'!B16*D21", "=ROUND(E21/31,0)", "tROAS 200%–220%", "Dot & Key sunscreens, Hair Spa tubs"],
        ["Google Ads", "G_SRC_MOF_Category_HairCare", "MOF (Category)", 0.13, "='Inputs & Parameters'!B16*D22", "=ROUND(E22/31,0)", "tCPA ceiling ₹451", "Exact & phrase search on salon care"],
        ["Google Ads", "G_SRC_BOF_Brand_FABB6_Exact", "BOF (Brand)", 0.07, "='Inputs & Parameters'!B16*D23", "=ROUND(E23/31,0)", "Target Imp. Share ≥ 95%", "Defends brand queries against competitors"],
        ["Google Total", "Combined Google Ads (62.9%)", "Portfolio", 1.00, "=SUM(E20:E23)", "=SUM(F20:F23)", "Portfolio Target ROAS: 2.45x", "January Google Target CPA: ₹451.00"],
        ["Meta Ads", "M_ASC_TOF_MasterProspecting", "TOF (Prospecting)", 0.70, "='Inputs & Parameters'!B19*D25", "=ROUND(E25/31,0)", "Target CPA ₹464", "ASC Broad + 10 UGC videos. 15% existing cap."],
        ["Meta Ads", "M_CBO_MOF_HeroCombos_Collection", "MOF (Combos)", 0.15, "='Inputs & Parameters'!B19*D26", "=ROUND(E26/31,0)", "Target CPA ₹464", "Social engagers past 60d, Haircare combos"],
        ["Meta Ads", "M_DPA_BOF_DynamicCatalog_7d", "BOF (Retargeting)", 0.15, "='Inputs & Parameters'!B19*D27", "=ROUND(E27/31,0)", "Target CPA ₹464", "Cart abandoners 7d. Freq capped ≤ 2.2x"],
        ["Meta Total", "Combined Meta Ads (37.1%)", "Portfolio", 1.00, "=SUM(E25:E27)", "=SUM(F25:F27)", "Portfolio Target ROAS: 2.38x", "January Meta Target CPA: ₹464.00"],
        ["Combined Total", "Combined Media Investment", "Cross-Channel", 1.00, "=E24+E28", "=F24+F28", "Account Target ROAS: 3.46x", "Trailing 7-Day Performance Gate: ROAS ≥ 2.50x"]
    ]

    for r_idx, r_data in enumerate(jan_campaigns):
        curr_r = 20 + r_idx
        is_tot = (r_idx in [4, 8, 9])
        for c_idx, val in enumerate(r_data):
            cell = ws6.cell(row=curr_r, column=c_idx+1, value=val)
            cell.font = total_font if is_tot else body_font
            cell.border = total_border if is_tot else thin_border
            if is_tot: cell.fill = total_fill
            elif r_idx % 2 == 1: cell.fill = zebra_fill
            
            if c_idx in [0, 2]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif c_idx == 3:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.number_format = '0.0%'
            elif c_idx in [4, 5]:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                cell.number_format = '₹#,##0'
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")

    # Feb Schedule (28d, ₹40.0L, Phased)
    ws6.cell(row=32, column=1, value="C. February 2027 Daily Campaign Allocations (28 Days, ₹40.0L Total Spend, Phased Schedule)").font = section_font
    feb_headers = ["Channel", "Campaign Architecture Node", "Funnel Stage", "% of Channel", "Monthly Budget", "Feb 1–14 Daily", "Feb 15–28 Daily", "Bidding Strategy"]
    for c_idx, h in enumerate(feb_headers):
        cell = ws6.cell(row=33, column=c_idx+1, value=h)
        cell.fill = navy_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

    feb_campaigns = [
        ["Google Ads", "G_PMAX_BOF_HighMargin_Heroes", "BOF (Heroes)", 0.60, "='Inputs & Parameters'!B17*D34", "=ROUND(F38*D34,0)", "=ROUND(G38*D34,0)", "tROAS 300%–320%"],
        ["Google Ads", "G_PMAX_BOF_CoreVolume_Tier2", "BOF (Core)", 0.20, "='Inputs & Parameters'!B17*D35", "=ROUND(F38*D35,0)", "=ROUND(G38*D35,0)", "tROAS 260%–280%"],
        ["Google Ads", "G_SRC_MOF_Category_HairCare", "MOF (Category)", 0.13, "='Inputs & Parameters'!B17*D36", "=ROUND(F38*D36,0)", "=ROUND(G38*D36,0)", "tCPA ceiling ₹407"],
        ["Google Ads", "G_SRC_BOF_Brand_FABB6_Exact", "BOF (Brand)", 0.07, "='Inputs & Parameters'!B17*D37", "=ROUND(F38*D37,0)", "=ROUND(G38*D37,0)", "Target Imp. Share ≥ 95%"],
        ["Google Total", "Combined Google Ads (62.5%)", "Portfolio", 1.00, "=SUM(E34:E37)", 80000, 98571, "Portfolio Target ROAS: 3.03x"],
        ["Meta Ads", "M_ASC_TOF_MasterProspecting", "TOF (Prospecting)", 0.70, "='Inputs & Parameters'!B20*D39", "=ROUND(F42*D39,0)", "=ROUND(G42*D39,0)", "Target CPA ₹410"],
        ["Meta Ads", "M_CBO_MOF_HeroCombos_Collection", "MOF (Combos)", 0.15, "='Inputs & Parameters'!B20*D40", "=ROUND(F42*D40,0)", "=ROUND(G42*D40,0)", "Target CPA ₹410"],
        ["Meta Ads", "M_DPA_BOF_DynamicCatalog_7d", "BOF (Retargeting)", 0.15, "='Inputs & Parameters'!B20*D41", "=ROUND(F42*D41,0)", "=ROUND(G42*D41,0)", "Target CPA ₹410"],
        ["Meta Total", "Combined Meta Ads (37.5%)", "Portfolio", 1.00, "=SUM(E39:E41)", 47143, 60000, "Portfolio Target ROAS: 3.00x"],
        ["Combined Total", "Combined Media Investment", "Cross-Channel", 1.00, "=E38+E42", "=F38+F42", "=G38+G42", "Account Target ROAS: 4.11x"]
    ]

    for r_idx, r_data in enumerate(feb_campaigns):
        curr_r = 34 + r_idx
        is_tot = (r_idx in [4, 8, 9])
        for c_idx, val in enumerate(r_data):
            cell = ws6.cell(row=curr_r, column=c_idx+1, value=val)
            cell.font = total_font if is_tot else body_font
            cell.border = total_border if is_tot else thin_border
            if is_tot: cell.fill = total_fill
            elif r_idx % 2 == 1: cell.fill = zebra_fill
            
            if c_idx in [0, 2]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif c_idx == 3:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.number_format = '0.0%'
            elif c_idx in [4, 5, 6]:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                cell.number_format = '₹#,##0'
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")

    col_w_6 = [18, 32, 16, 14, 16, 18, 24, 38]
    for c_idx, w in enumerate(col_w_6):
        ws6.column_dimensions[get_column_letter(c_idx+1)].width = w

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    wb.save(output_path)
    print(f"Successfully generated Master Excel Model at: {output_path}")

if __name__ == "__main__":
    report_xlsx = r"C:\Users\test\Videos\Office\reports\FABB6_All_Forecasts_and_Turnaround_Master_Model.xlsx"
    case_study_xlsx = r"C:\Users\test\Videos\Office\case-studies\fabb6\FABB6_All_Forecasts_and_Turnaround_Master_Model.xlsx"
    artifact_xlsx = r"C:\Users\test\.gemini\antigravity\brain\29f77e0a-5ed5-4d24-842c-443d9957274c\FABB6_All_Forecasts_and_Turnaround_Master_Model.xlsx"

    build_formula_driven_master_excel(report_xlsx)
    shutil.copyfile(report_xlsx, case_study_xlsx)
    shutil.copyfile(report_xlsx, artifact_xlsx)
    print("All Excel files successfully generated and synchronized.")
