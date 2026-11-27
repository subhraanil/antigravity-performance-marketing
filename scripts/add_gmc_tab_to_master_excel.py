import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import os
import shutil

wb_path = r"C:\Users\test\Videos\Office\reports\FABB6_All_Forecasts_and_Turnaround_Master_Model.xlsx"
wb = openpyxl.load_workbook(wb_path)

sheet_name = "Merchant Center Bleed & Tiers"
if sheet_name in wb.sheetnames:
    del wb[sheet_name]

ws = wb.create_sheet(title=sheet_name)
ws.views.sheetView[0].showGridLines = True

# Styling helpers
navy_header_fill = PatternFill(start_color="102C57", end_color="102C57", fill_type="solid")
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

# Title Block
ws.merge_cells("A1:I1")
ws["A1"] = "FABB6 - Google Merchant Center SKU Click Bleed & Product Catalog Analysis"
ws["A1"].font = Font(name="Calibri", size=14, bold=True, color="102C57")

ws.merge_cells("A2:I2")
ws["A2"] = "Audit Period: 1 September 2026 – 19 November 2026 | Performance Max & Standard Shopping Traffic Forensics"
ws["A2"].font = Font(name="Calibri", size=10, italic=True, color="555555")

# KPI Summary Cards
kpis = [
    ("Total GMC Impressions", "61,389,771", "6.14 Crore total impressions served"),
    ("Total GMC Clicks", "629,968", "6.30 Lakh total clicks received"),
    ("Tracked Purchases", "48.77", "0.0077% recorded conversion rate"),
    ("Zero-Purchase Clicks", "542,808", "86.2% of all clicks burned on 0-order SKUs"),
    ("Active Catalog SKUs", "1,309", "100% In Stock (Price Range: ₹69 to ₹24,500)"),
]

ws.row_dimensions[4].height = 20
ws.row_dimensions[5].height = 25
ws.row_dimensions[6].height = 18

for idx, (label, val, note) in enumerate(kpis):
    col = idx * 2 + 1
    end_col = col + 1 if idx < 4 else col
    if idx < 4:
        ws.merge_cells(start_row=4, start_column=col, end_row=4, end_column=end_col)
        ws.merge_cells(start_row=5, start_column=col, end_row=5, end_column=end_col)
        ws.merge_cells(start_row=6, start_column=col, end_row=6, end_column=end_col)
    
    cell_lbl = ws.cell(row=4, column=col, value=label)
    cell_lbl.font = Font(name="Calibri", size=8.5, bold=True, color="555555")
    cell_lbl.alignment = Alignment(horizontal="center", vertical="center")
    cell_lbl.fill = section_fill
    
    cell_val = ws.cell(row=5, column=col, value=val)
    cell_val.font = Font(name="Calibri", size=12, bold=True, color="922B21" if "Zero" in label or "Purchases" in label else "102C57")
    cell_val.alignment = Alignment(horizontal="center", vertical="center")
    cell_val.fill = alert_fill if "Zero" in label else section_fill
    
    cell_note = ws.cell(row=6, column=col, value=note)
    cell_note.font = Font(name="Calibri", size=7.5, italic=True, color="666666")
    cell_note.alignment = Alignment(horizontal="center", vertical="center")
    cell_note.fill = section_fill

# Section A: Top Zero-Converting Click Bleeders
ws.cell(row=8, column=1, value="A. Top Zero-Converting Click Bleeder SKUs (Sep 1 – Nov 19, 2026)").font = section_font

top_bleeders = [
    ["Rank", "Product Title", "Sale Price", "Price Tier (CL 1)", "Margin Class (CL 4)", "Impressions", "Clicks", "CTR", "Tracked Purchases"],
    [1, "Raaga Professional De-Tan Tan Removal Cream single use", "₹69", "T1 Entry (<₹500)", "mid_20_28", 1261144, 27648, "2.19%", 0.0],
    [2, "DOT & KEY STRAWBERRY DEW TINTED SUNSCREEN 50ml", "₹549", "T2 Core (₹500–900)", "mid_20_28", 669332, 17485, "2.61%", 0.0],
    [3, "Loreal Paris Hair Spa Deep Nourish Creambath (490 Gm)", "₹650", "T2 Core (₹500–900)", "mid_20_28", 766242, 13249, "1.73%", 0.0],
    [4, "Matrix Mega Smooth silk protein + shea butter masque 500Gm", "₹750", "T2 Core (₹500–900)", "mid_20_28", 810808, 9192, "1.13%", 0.0],
    [5, "Loreal Majirel Hair Color 60ml Shade 3.0 Combo", "₹755", "T2 Core (₹500–900)", "high_28plus", 673069, 9142, "1.36%", 0.0],
    [6, "Loreal Professional Majirel Hair Color 50G 5.35", "₹495", "T1 Entry (<₹500)", "high_28plus", 1132797, 8978, "0.79%", 0.0],
    [7, "Loreal Absolut Repair Cellular Shampoo - 1500Ml", "₹2,650", "T4 Pro/Salon (>₹1,300)", "high_28plus", 1663445, 8007, "0.48%", 0.0],
    [8, "Floractive Professional W One Nanoplastia Hair Treatment 1000Ml", "₹5,500", "T4 Pro/Salon (>₹1,300)", "high_28plus", 1357589, 6921, "0.51%", 0.0],
    [9, "Loreal Professionnel Serie Expert Absolut Repair Shampoo 300ml", "₹720", "T2 Core (₹500–900)", "high_28plus", 635116, 6426, "1.01%", 0.0],
    [10, "Loreal Majirel 3.0 Dark Brown 60 Ml", "₹415", "T1 Entry (<₹500)", "high_28plus", 697847, 4921, "0.71%", 0.0],
    [11, "Loreal Xtenso Smoothing Cream Resistant Hair 400ML", "₹1,450", "T4 Pro/Salon (>₹1,300)", "high_28plus", 969982, 4352, "0.45%", 0.0],
    [12, "Loreal Hair Spa Purifying Concentrate 8ML", "₹120", "T1 Entry (<₹500)", "mid_20_28", 174406, 4131, "2.37%", 0.0],
    [13, "Inoa 4 Tube Intense Brown 60G", "₹475", "T1 Entry (<₹500)", "high_28plus", 202661, 4031, "1.99%", 0.0],
    [14, "Loreal Professionnel Absolut Repair combo", "₹1,370", "T4 Pro/Salon (>₹1,300)", "high_28plus", 286747, 4019, "1.40%", 0.0],
    [15, "Loreal Professionnel Majirel Color Tube 7.23", "₹415", "T1 Entry (<₹500)", "high_28plus", 485780, 3836, "0.79%", 0.0],
]

start_row = 10
for r_idx, row in enumerate(top_bleeders):
    curr_row = start_row + r_idx
    is_header = (r_idx == 0)
    for c_idx, val in enumerate(row):
        col_letter = get_column_letter(c_idx + 1)
        cell = ws.cell(row=curr_row, column=c_idx + 1, value=val)
        cell.border = thin_border
        if is_header:
            cell.fill = navy_header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")
        else:
            cell.font = alert_font if c_idx == 8 else body_font
            if c_idx in [0, 2, 3, 4, 7]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif c_idx in [5, 6, 8]:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                if c_idx in [5, 6]: cell.number_format = '#,##0'
                if c_idx == 8: cell.number_format = '0.00'
            else:
                cell.alignment = Alignment(horizontal="left", vertical="center")
            if r_idx % 2 == 0:
                cell.fill = zebra_fill

# Total Row for Top 15 Bleeders
total_row = start_row + len(top_bleeders)
ws.cell(row=total_row, column=1, value="—").alignment = Alignment(horizontal="center")
ws.cell(row=total_row, column=2, value="Total Top 15 Zero-Converting Bleeders").font = total_font
ws.cell(row=total_row, column=3, value="—").alignment = Alignment(horizontal="center")
ws.cell(row=total_row, column=4, value="—").alignment = Alignment(horizontal="center")
ws.cell(row=total_row, column=5, value="—").alignment = Alignment(horizontal="center")
ws.cell(row=total_row, column=6, value=f"=SUM(F{start_row+1}:F{total_row-1})").font = total_font
ws.cell(row=total_row, column=7, value=f"=SUM(G{start_row+1}:G{total_row-1})").font = total_font
ws.cell(row=total_row, column=8, value="1.03%").font = total_font
ws.cell(row=total_row, column=9, value=0.0).font = total_font

for c in range(1, 10):
    cell = ws.cell(row=total_row, column=c)
    cell.fill = total_fill
    cell.border = total_border
    if c in [6, 7]:
        cell.alignment = Alignment(horizontal="right", vertical="center")
        cell.number_format = '#,##0'
    elif c == 9:
        cell.alignment = Alignment(horizontal="right", vertical="center")
        cell.number_format = '0.00'

# Section B: Price Tier Summary (Custom Label 1)
sec_b_row = total_row + 3
ws.cell(row=sec_b_row, column=1, value="B. Performance by Price Tier (Custom Label 1)").font = section_font

tier_data = [
    ["Price Tier (Custom Label 1)", "Catalog SKUs", "Impressions", "Clicks", "Share of Clicks", "Tracked Purchases", "Purchase Rate", "Turnaround Directive"],
    ["T1 Entry (<₹500)", 626, 16989281, 190347, "30.2%", 14.31, "0.0075%", "Restrict to Combo Bundles only; halt standalone single-use sachets"],
    ["T2 Core (₹500–900)", 299, 11558620, 153185, "24.3%", 10.41, "0.0068%", "Standard Shopping / PMax Core Volume campaign (30% budget)"],
    ["T3 Premium (₹900–1,300)", 125, 5258641, 40986, "6.5%", 0.00, "0.0000%", "Audit landing pages & bundle with high-velocity hero products"],
    ["T4 Pro/Salon (>₹1,300)", 247, 20356952, 156716, "24.9%", 18.21, "0.0116%", "High Margin Hero PMax Campaign (60% budget allocation)"],
    ["Other / Unmatched Catalog", 12, 7226277, 88734, "14.1%", 5.84, "0.0066%", "Catalog feed hygiene audit & tag reconciliation"],
]

start_tier_row = sec_b_row + 2
for r_idx, row in enumerate(tier_data):
    curr_row = start_tier_row + r_idx
    is_header = (r_idx == 0)
    for c_idx, val in enumerate(row):
        cell = ws.cell(row=curr_row, column=c_idx + 1, value=val)
        cell.border = thin_border
        if is_header:
            cell.fill = sub_header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")
        else:
            cell.font = body_font_bold if c_idx == 0 else body_font
            if c_idx in [0, 7]:
                cell.alignment = Alignment(horizontal="left", vertical="center")
            elif c_idx in [1, 4, 6]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                if c_idx in [2, 3]: cell.number_format = '#,##0'
                if c_idx == 5: cell.number_format = '0.00'
            if r_idx % 2 == 0:
                cell.fill = zebra_fill

# Section C: Margin Class Summary (Custom Label 4)
sec_c_row = start_tier_row + len(tier_data) + 2
ws.cell(row=sec_c_row, column=1, value="C. Performance by Profit Margin Class (Custom Label 4)").font = section_font

margin_data = [
    ["Margin Class (Custom Label 4)", "Catalog SKUs", "Gross Margin %", "Impressions", "Clicks", "Share of Clicks", "Tracked Purchases", "Turnaround Directive"],
    ["high_28plus", 431, "> 28%", 10621338, 117562, "18.7%", 6.96, "PRIORITY HERO: Target with 60% of Google Shopping spend"],
    ["mid_20_28", 585, "20% – 28%", 31176608, 307803, "48.9%", 20.74, "CORE VOLUME: Maintain controlled tROAS bidding (2.4x)"],
    ["low_15_20", 218, "15% – 20%", 11576206, 107250, "17.0%", 13.66, "CAPPED BIDDING: Strict tROAS 3.0x threshold to avoid margin loss"],
    ["EXCLUDE_lowmargin", 28, "< 15%", 847010, 9354, "1.5%", 1.23, "HARD EXCLUSION: Add negative product group filter immediately"],
    ["unknown_cogs / Unmatched", 47, "Unassigned", 7168609, 87999, "14.0%", 6.18, "COGS ENRICHMENT: Update Shopify cost-of-goods to unlock bidding"],
]

start_margin_row = sec_c_row + 2
for r_idx, row in enumerate(margin_data):
    curr_row = start_margin_row + r_idx
    is_header = (r_idx == 0)
    for c_idx, val in enumerate(row):
        cell = ws.cell(row=curr_row, column=c_idx + 1, value=val)
        cell.border = thin_border
        if is_header:
            cell.fill = sub_header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")
        else:
            cell.font = alert_font if "EXCLUDE" in str(val) else (body_font_bold if c_idx == 0 else body_font)
            if c_idx in [0, 7]:
                cell.alignment = Alignment(horizontal="left", vertical="center")
            elif c_idx in [1, 2, 5]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cell.alignment = Alignment(horizontal="right", vertical="center")
                if c_idx in [3, 4]: cell.number_format = '#,##0'
                if c_idx == 6: cell.number_format = '0.00'
            if r_idx % 2 == 0:
                cell.fill = zebra_fill
            if "EXCLUDE" in str(val):
                cell.fill = alert_fill

# Column widths
col_widths = {
    1: 30, # Rank / Category
    2: 45, # Title
    3: 16, # Price / Margin
    4: 22, # Tier / Impressions
    5: 22, # Margin / Clicks
    6: 18, # Impressions / Share
    7: 16, # Clicks / Purchases
    8: 15, # CTR / Pur Rate
    9: 45, # Purchases / Directive
}

for col_idx, width in col_widths.items():
    ws.column_dimensions[get_column_letter(col_idx)].width = width

wb.save(wb_path)
print(f"Successfully added Tab 5 to {wb_path}")

# Copy to case-study and brain
case_study_wb = r"C:\Users\test\Videos\Office\case-studies\fabb6\FABB6_All_Forecasts_and_Turnaround_Master_Model.xlsx"
brain_wb = r"C:\Users\test\.gemini\antigravity\brain\29f77e0a-5ed5-4d24-842c-443d9957274c\FABB6_All_Forecasts_and_Turnaround_Master_Model.xlsx"

shutil.copyfile(wb_path, case_study_wb)
shutil.copyfile(wb_path, brain_wb)
print("Synchronized master workbook across all locations.")
