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
accent_fill = PatternFill(start_color="FEF9E7", end_color="FEF9E7", fill_type="solid")

header_font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
section_font = Font(name="Calibri", size=11, bold=True, color="102C57")
total_font = Font(name="Calibri", size=10, bold=True, color="102C57")
body_font = Font(name="Calibri", size=9.5, color="202020")
body_font_bold = Font(name="Calibri", size=9.5, bold=True, color="202020")

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

# 1. Update Tab 1: Executive Overview
if 'Executive Overview' in wb.sheetnames:
    ws1 = wb['Executive Overview']
    ws1['A1'] = "FABB6 TURNAROUND STRATEGY & SCENARIO MODEL (Q1 2027)"
    ws1['A2'] = "Techno Exponent Growth Practice | Recalibrated Financial Scenarios (AOV Baseline: ₹1,100)"
    
    # Update scenario rows
    # Row 6: Base Plan
    ws1['A6'] = "Plan 1: Base Plan (Capital Preservation)"
    ws1['B6'] = "2.80x / 2.80x / 2.80x"
    ws1['C6'] = 5600000
    ws1['D6'] = 6720000
    ws1['E6'] = 7280000
    ws1['F6'] = 19600000
    ws1['G6'] = "2.80x"
    
    # Row 7: Recommended Plan
    ws1['A7'] = "Plan 2: Recommended Plan (Target Turnaround)"
    ws1['B7'] = "2.50x / 2.55x / 2.60x"
    ws1['C7'] = 6500000
    ws1['D7'] = 7905000
    ws1['E7'] = 8866000
    ws1['F7'] = 23271000
    ws1['G7'] = "2.55x"
    
    # Row 8: Aggressive Plan
    ws1['A8'] = "Plan 3: Aggressive Plan (Market Share Expansion)"
    ws1['B8'] = "2.40x / 2.35x / 2.25x"
    ws1['C8'] = 7200000
    ws1['D8'] = 8812500
    ws1['E8'] = 10125000
    ws1['F8'] = 26137500
    ws1['G8'] = "2.32x"
    
    # Add Marginal Return Analysis block
    ws1.cell(row=16, column=1, value="3. Marginal Return & Capital Allocation Economics").font = section_font
    marginal_headers = ["Strategic Transition", "Incremental Spend", "Incremental Gross Sales", "Marginal ROAS", "Strategic Investment Verdict"]
    for c_idx, h in enumerate(marginal_headers):
        cell = ws1.cell(row=17, column=c_idx+1, value=h)
        cell.fill = sub_header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border
        
    marginal_rows = [
        ["Plan 1 to Plan 2 (Base to Recommended)", "₹21.10 Lakhs", "₹36.71 Lakhs", "1.74x", "HIGH VALUE: Generates robust incremental contribution above variable fulfillment costs."],
        ["Plan 2 to Plan 3 (Recommended to Aggressive)", "₹21.40 Lakhs", "₹28.67 Lakhs", "1.34x", "DIMINISHING RETURNS: Lower marginal return; scaling should only proceed if ROAS ≥ 2.50x."]
    ]
    for r_idx, r_data in enumerate(marginal_rows):
        for c_idx, val in enumerate(r_data):
            cell = ws1.cell(row=18+r_idx, column=c_idx+1, value=val)
            cell.font = body_font_bold if c_idx in [0, 3] else body_font
            cell.border = thin_border
            cell.alignment = Alignment(horizontal="center" if c_idx in [1, 2, 3] else "left", vertical="center")
            if r_idx % 2 == 1: cell.fill = zebra_fill

# 2. Update Tab 2: 3-Month Plan - Master Forecast
if '3-Month Plan - Master Forecast' in wb.sheetnames:
    ws2 = wb['3-Month Plan - Master Forecast']
    ws2['A1'] = "FABB6 MASTER TURNAROUND PLAN (RECOMMENDED SCENARIO)"
    ws2['A2'] = "Recalibrated Target Turnaround Model | AOV Baseline: ₹1,100 | Blended Confirmed ROAS: 2.55x"
    
    # Headers in row 4: Month, Total Ad Spend, Google Spend, Meta Spend, Paid Orders, Orders from Others*, Total Store Orders, Total Sales Revenue, Spend Per Order, Confirmed ROAS
    ws2['I4'] = "Spend Per Order"
    ws2['J4'] = "Confirmed ROAS"
    
    # Row 6: December 2026
    ws2['B6'] = 2600000
    ws2['C6'] = 1600000
    ws2['D6'] = 1000000
    ws2['E6'] = 4667 # Paid platform orders
    ws2['F6'] = 1242 # Organic & repeat
    ws2['G6'] = 5909 # Total store orders (65.0L / 1100)
    ws2['H6'] = 6500000 # Gross sales (26.0L * 2.50)
    ws2['I6'] = 440.01
    ws2['J6'] = "2.50x"
    
    # Row 7: January 2027
    ws2['B7'] = 3100000
    ws2['C7'] = 2000000
    ws2['D7'] = 1100000
    ws2['E7'] = 5732
    ws2['F7'] = 1454
    ws2['G7'] = 7186 # (79.05L / 1100)
    ws2['H7'] = 7905000 # (31.0L * 2.55)
    ws2['I7'] = 431.39
    ws2['J7'] = "2.55x"
    
    # Row 8: February 2027
    ws2['B8'] = 3410000
    ws2['C8'] = 2200000
    ws2['D8'] = 1210000
    ws2['E8'] = 6500
    ws2['F8'] = 1560
    ws2['G8'] = 8060 # (88.66L / 1100)
    ws2['H8'] = 8866000 # (34.1L * 2.60)
    ws2['I8'] = 423.08
    ws2['J8'] = "2.60x"
    
    # Row 9: Total Q1 Plan
    ws2['B9'] = 9110000
    ws2['C9'] = 5800000
    ws2['D9'] = 3310000
    ws2['E9'] = 16899
    ws2['F9'] = 4256
    ws2['G9'] = 21155
    ws2['H9'] = 23271000
    ws2['I9'] = 430.63
    ws2['J9'] = "2.55x"

# 3. Add Tab 6: Strategy & Daily Budgets (3 Plans)
sheet_tab6 = "Strategy & Daily Budgets"
if sheet_tab6 in wb.sheetnames:
    del wb[sheet_tab6]

ws6 = wb.create_sheet(title=sheet_tab6)
ws6.views.sheetView[0].showGridLines = True

ws6.merge_cells("A1:H1")
ws6["A1"] = "FABB6 - FULL-FUNNEL CAMPAIGN ARCHITECTURE & DAILY BUDGET SCHEDULES"
ws6["A1"].font = Font(name="Calibri", size=14, bold=True, color="102C57")

ws6.merge_cells("A2:H2")
ws6["A2"] = "December 2026 – February 2027 | Google Ads (63%) & Meta Ads (37%) | Scenario Allocations"
ws6["A2"].font = Font(name="Calibri", size=10, italic=True, color="555555")

# Month Tables
months_config = [
    ("A. December 2026 Daily Campaign Allocations (31 Days)", 4, 31, 2000000, 2600000, 3000000),
    ("B. January 2027 Daily Campaign Allocations (31 Days)", 18, 31, 2400000, 3100000, 3750000),
    ("C. February 2027 Daily Campaign Allocations (28 Days)", 32, 28, 2600000, 3410000, 4500000),
]

campaign_shares = [
    ("Google Ads", "G_PMAX_BOF_HighMargin_Heroes", "BOF (Heroes)", 0.63 * 0.60),
    ("Google Ads", "G_PMAX_BOF_CoreVolume_Tier2", "BOF (Core)", 0.63 * 0.20),
    ("Google Ads", "G_SRC_MOF_Category_HairCare", "MOF (Search)", 0.63 * 0.13),
    ("Google Ads", "G_SRC_BOF_Brand_FABB6_Exact", "BOF (Brand)", 0.63 * 0.07),
    ("Meta Ads", "M_ASC_TOF_MasterProspecting", "TOF (Prospecting)", 0.37 * 0.70),
    ("Meta Ads", "M_DPA_BOF_DynamicCatalog_7d", "BOF (Retargeting)", 0.37 * 0.15),
    ("Meta Ads", "M_CBO_MOF_HeroCombos_Collection", "MOF (Combos)", 0.37 * 0.15),
]

for section_title, start_r, days, base_spend, rec_spend, agg_spend in months_config:
    ws6.cell(row=start_r, column=1, value=section_title).font = section_font
    
    headers = ["Channel", "Campaign Architecture Node", "Funnel Stage", "% of Total", 
               f"Plan 1: Base (₹{base_spend/100000:.1f}L)", 
               f"Plan 2: Recommended (₹{rec_spend/100000:.1f}L)", 
               f"Plan 3: Aggressive (₹{agg_spend/100000:.1f}L)", 
               "Operational Bidding Directive"]
    
    for c_idx, h in enumerate(headers):
        cell = ws6.cell(row=start_r+1, column=c_idx+1, value=h)
        cell.fill = navy_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border
        
    for r_idx, (channel, camp, stage, share) in enumerate(campaign_shares):
        curr_row = start_r + 2 + r_idx
        daily_base = round((base_spend * share) / days)
        daily_rec = round((rec_spend * share) / days)
        daily_agg = round((agg_spend * share) / days)
        
        directive = "Target ROAS 270%–290%" if "Heroes" in camp else (
            "Target ROAS 230%–250%" if "Core" in camp else (
                "tCPA ceiling ₹480–₹520" if "Search" in camp else (
                    "Absolute Top Impression Share ≥ 95%" if "Brand" in camp else (
                        "Highest Volume (20% existing cap)" if "ASC" in camp else (
                            "Cost Cap ceiling ₹480 (30d excl)" if "DPA" in camp else "Highest Volume (AOV bundles)"
                        )
                    )
                )
            )
        )
        
        row_vals = [channel, camp, stage, f"{share*100:.1f}%", f"₹{daily_base:,} / day", f"₹{daily_rec:,} / day", f"₹{daily_agg:,} / day", directive]
        for c_idx, val in enumerate(row_vals):
            cell = ws6.cell(row=curr_row, column=c_idx+1, value=val)
            cell.font = body_font
            cell.border = thin_border
            if c_idx in [0, 2, 3]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif c_idx in [4, 5, 6]:
                cell.alignment = Alignment(horizontal="right", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")
            if r_idx % 2 == 1: cell.fill = zebra_fill
            
    # Total row
    tot_row = start_r + 2 + len(campaign_shares)
    tot_base_daily = round(base_spend / days)
    tot_rec_daily = round(rec_spend / days)
    tot_agg_daily = round(agg_spend / days)
    
    tot_vals = ["Total", "Combined Cross-Channel Media Investment", "Full Portfolio", "100.0%", 
                f"₹{tot_base_daily:,} / day", f"₹{tot_rec_daily:,} / day", f"₹{tot_agg_daily:,} / day", 
                f"Monthly: Base ₹{base_spend/100000:.1f}L | Rec ₹{rec_spend/100000:.1f}L | Agg ₹{agg_spend/100000:.1f}L"]
    
    for c_idx, val in enumerate(tot_vals):
        cell = ws6.cell(row=tot_row, column=c_idx+1, value=val)
        cell.font = total_font
        cell.fill = total_fill
        cell.border = total_border
        if c_idx in [0, 2, 3]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif c_idx in [4, 5, 6]:
            cell.alignment = Alignment(horizontal="right", vertical="center")
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center")

# Column dimensions
col_widths = {1: 15, 2: 36, 3: 18, 4: 12, 5: 22, 6: 24, 7: 24, 8: 38}
for col_idx, width in col_widths.items():
    ws6.column_dimensions[get_column_letter(col_idx)].width = width

wb.save(wb_path)
print(f"Successfully updated master Excel model at: {wb_path}")

case_study_wb = r"C:\Users\test\Videos\Office\case-studies\fabb6\FABB6_All_Forecasts_and_Turnaround_Master_Model.xlsx"
brain_wb = r"C:\Users\test\.gemini\antigravity\brain\29f77e0a-5ed5-4d24-842c-443d9957274c\FABB6_All_Forecasts_and_Turnaround_Master_Model.xlsx"

shutil.copyfile(wb_path, case_study_wb)
shutil.copyfile(wb_path, brain_wb)
print("Synchronized master Excel model across all locations.")
