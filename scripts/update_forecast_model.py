import os
import shutil
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

file_path = "data/Pet Mode/Forecast - 25 Sept - Pet Mode.xlsx"
wb = openpyxl.load_workbook(file_path)

currency_fmt = "[$£-809]#,##0.00"
number_fmt = "#,##0"
percent_fmt = "0.00%"
decimal_fmt = "0.00"

header_font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid") # Deep Navy
subhdr_font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")
subhdr_fill = PatternFill(start_color="DBEAFE", end_color="DBEAFE", fill_type="solid") # Light Blue
total_font = Font(name="Calibri", size=10, bold=True, color="0F172A")
total_fill = PatternFill(start_color="E2E8F0", end_color="E2E8F0", fill_type="solid") # Light Slate
regular_font = Font(name="Calibri", size=10)
bold_font = Font(name="Calibri", size=10, bold=True)

thin_side = Side(border_style="thin", color="CBD5E1")
cell_border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
total_top = Side(border_style="thin", color="1E3A8A")
total_bot = Side(border_style="double", color="1E3A8A")
total_border = Border(left=thin_side, right=thin_side, top=total_top, bottom=total_bot)

align_center = Alignment(horizontal="center", vertical="center")
align_right = Alignment(horizontal="right", vertical="center")
align_left = Alignment(horizontal="left", vertical="center")

# =============================================================
# 1. UPDATE 'Forecast - Recomended' (MATCHING FINAL CLIENT REPORT)
# =============================================================
ws_rec = wb["Forecast - Recomended"]

# Titles
ws_rec["A1"] = "Forecast Shopify"
ws_rec["A1"].font = subhdr_font
ws_rec["A7"] = "Forecast Google Ads"
ws_rec["A7"].font = subhdr_font
ws_rec["B13"] = "Forecast Meta Ads"
ws_rec["B13"].font = subhdr_font

# Shopify Table
shopify_headers = ["Months", "Spend", "Paid Order", "Other order", "Total Orders", "Paid CPA", "Blended CPA", "Total Revenue", "AOV", "ROAS"]
for c_idx, h in enumerate(shopify_headers, start=1):
    cell = ws_rec.cell(row=2, column=c_idx, value=h)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = align_center
    cell.border = cell_border

# October Shopify (Row 3)
ws_rec["A3"] = "October"
ws_rec["B3"] = "=B9+B15"           # £1,100.00
ws_rec["C3"] = "=E9+E15"           # 47
ws_rec["D3"] = 10                  # 10 other orders (email/organic)
ws_rec["E3"] = "=C3+D3"           # 57 total orders
ws_rec["F3"] = "=B3/C3"           # £23.40 Paid CPA
ws_rec["G3"] = "=B3/E3"           # £19.30 Blended CPA
ws_rec["H3"] = 1493.00            # £1,493.00 Total Revenue
ws_rec["I3"] = "=H3/E3"           # £26.19 AOV
ws_rec["J3"] = "=H3/B3"           # 1.36 ROAS

# November Shopify (Row 4)
ws_rec["A4"] = "November"
ws_rec["B4"] = "=B10+B16"         # £1,300.00
ws_rec["C4"] = "=E10+E16"         # 66
ws_rec["D4"] = 14                 # 14 other orders
ws_rec["E4"] = "=C4+D4"          # 80 total orders
ws_rec["F4"] = "=B4/C4"          # £19.70 Paid CPA
ws_rec["G4"] = "=B4/E4"          # £16.25 Blended CPA
ws_rec["H4"] = 2252.00           # £2,252.00 Total Revenue
ws_rec["I4"] = "=H4/E4"          # £28.15 AOV
ws_rec["J4"] = "=H4/B4"          # 1.73 ROAS

# December Shopify (Row 5)
ws_rec["A5"] = "December"
ws_rec["B5"] = "=B11+B17"         # £1,400.00
ws_rec["C5"] = "=E11+E17"         # 73
ws_rec["D5"] = 14                 # 14 other orders
ws_rec["E5"] = "=C5+D5"          # 87 total orders
ws_rec["F5"] = "=B5/C5"          # £19.18 Paid CPA
ws_rec["G5"] = "=B5/E5"          # £16.09 Blended CPA
ws_rec["H5"] = 2575.00           # £2,575.00 Total Revenue
ws_rec["I5"] = "=H5/E5"          # £29.60 AOV
ws_rec["J5"] = "=H5/B5"          # 1.84 ROAS

# 3-Month Total Shopify (Row 6)
ws_rec["A6"] = "3-Month Total"
ws_rec["B6"] = "=SUM(B3:B5)"      # £3,800.00
ws_rec["C6"] = "=SUM(C3:C5)"      # 186
ws_rec["D6"] = "=SUM(D3:D5)"      # 38
ws_rec["E6"] = "=SUM(E3:E5)"      # 224
ws_rec["F6"] = "=B6/C6"          # £20.43 Paid CPA
ws_rec["G6"] = "=B6/E6"          # £16.96 Blended CPA
ws_rec["H6"] = "=SUM(H3:H5)"      # £6,320.00 Total Revenue
ws_rec["I6"] = "=H6/E6"          # £28.21 AOV
ws_rec["J6"] = "=H6/B6"          # 1.66 ROAS

# Format Shopify Rows 3-6
for r in range(3, 7):
    is_tot = (r == 6)
    ws_rec.cell(r, 1).alignment = align_left
    ws_rec.cell(r, 1).font = total_font if is_tot else bold_font
    ws_rec.cell(r, 1).border = total_border if is_tot else cell_border
    if is_tot: ws_rec.cell(r, 1).fill = total_fill
    
    for c in range(2, 11):
        cell = ws_rec.cell(r, c)
        cell.font = total_font if is_tot else regular_font
        cell.border = total_border if is_tot else cell_border
        cell.alignment = align_right
        if is_tot: cell.fill = total_fill
        
        # Formats
        if c in [2, 6, 7, 8, 9]: # Currency
            cell.number_format = currency_fmt
        elif c in [3, 4, 5]: # Counts
            cell.number_format = number_fmt
        elif c == 10: # ROAS
            cell.number_format = decimal_fmt

# Google Ads Table
channel_headers = ["Months", "Spend", "Impression", "Clicks", "Orders", "CPA", "Conv rate", "Total Revenue", "AOV", "ROAS", "CTR", "Avg CPC"]
for c_idx, h in enumerate(channel_headers, start=1):
    cell = ws_rec.cell(row=8, column=c_idx, value=h)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = align_center
    cell.border = cell_border

# October Google Ads (Row 9)
ws_rec["A9"] = "October"
ws_rec["B9"] = 500.00
ws_rec["C9"] = "=D9/K9"           # 34,722
ws_rec["D9"] = "=B9/L9"           # 833.33
ws_rec["E9"] = "=G9*D9"           # 20.0 orders
ws_rec["F9"] = "=B9/E9"           # £25.00 CPA
ws_rec["G9"] = 0.024              # 2.40% Conv Rate
ws_rec["H9"] = "=I9*E9"           # £540.00 Revenue
ws_rec["I9"] = 27.00              # £27.00 AOV
ws_rec["J9"] = "=H9/B9"           # 1.08 ROAS
ws_rec["K9"] = 0.024              # 2.40% CTR
ws_rec["L9"] = 0.60               # £0.60 Avg CPC

# November Google Ads (Row 10)
ws_rec["A10"] = "November"
ws_rec["B10"] = 600.00
ws_rec["C10"] = "=D10/K10"        # 37,221
ws_rec["D10"] = "=B10/L10"        # 967.74
ws_rec["E10"] = "=G10*D10"        # 26.0 orders
ws_rec["F10"] = "=B10/E10"        # £23.08 CPA
ws_rec["G10"] = 0.02686667        # 2.69% Conv Rate
ws_rec["H10"] = "=I10*E10"        # £728.00 Revenue
ws_rec["I10"] = 28.00             # £28.00 AOV
ws_rec["J10"] = "=H10/B10"        # 1.21 ROAS
ws_rec["K10"] = 0.026             # 2.60% CTR
ws_rec["L10"] = 0.62              # £0.62 Avg CPC

# December Google Ads (Row 11)
ws_rec["A11"] = "December"
ws_rec["B11"] = 600.00
ws_rec["C11"] = "=D11/K11"        # 36,946
ws_rec["D11"] = "=B11/L11"        # 1,034.48
ws_rec["E11"] = "=G11*D11"        # 29.0 orders
ws_rec["F11"] = "=B11/E11"        # £20.69 CPA
ws_rec["G11"] = 0.02803333        # 2.80% Conv Rate
ws_rec["H11"] = "=I11*E11"        # £855.50 Revenue
ws_rec["I11"] = 29.50             # £29.50 AOV
ws_rec["J11"] = "=H11/B11"        # 1.43 ROAS
ws_rec["K11"] = 0.028             # 2.80% CTR
ws_rec["L11"] = 0.58              # £0.58 Avg CPC

# Total Google Ads (Row 12)
ws_rec["A12"] = "Total"
ws_rec["B12"] = "=SUM(B9:B11)"    # £1,700.00
ws_rec["C12"] = "=SUM(C9:C11)"
ws_rec["D12"] = "=SUM(D9:D11)"
ws_rec["E12"] = "=SUM(E9:E11)"    # 75 orders
ws_rec["F12"] = "=B12/E12"        # £22.67 CPA
ws_rec["G12"] = "=E12/D12"        # 2.65% Conv Rate
ws_rec["H12"] = "=SUM(H9:H11)"    # £2,123.50 Revenue
ws_rec["I12"] = "=H12/E12"        # £28.31 AOV
ws_rec["J12"] = "=H12/B12"        # 1.25 ROAS
ws_rec["K12"] = "=D12/C12"        # 2.60% CTR
ws_rec["L12"] = "=B12/D12"        # £0.60 Avg CPC

# Format Google Ads Rows 9-12
for r in range(9, 13):
    is_tot = (r == 12)
    ws_rec.cell(r, 1).alignment = align_left
    ws_rec.cell(r, 1).font = total_font if is_tot else bold_font
    ws_rec.cell(r, 1).border = total_border if is_tot else cell_border
    if is_tot: ws_rec.cell(r, 1).fill = total_fill
    
    for c in range(2, 13):
        cell = ws_rec.cell(r, c)
        cell.font = total_font if is_tot else regular_font
        cell.border = total_border if is_tot else cell_border
        cell.alignment = align_right
        if is_tot: cell.fill = total_fill
        
        if c in [2, 6, 8, 9, 12]: # Currency
            cell.number_format = currency_fmt
        elif c in [3, 4, 5]: # Counts
            cell.number_format = number_fmt
        elif c in [7, 11]: # Percentage
            cell.number_format = percent_fmt
        elif c == 10: # ROAS
            cell.number_format = decimal_fmt

# Meta Ads Table
meta_headers = ["Months", "Spend", "Reach", "Clicks", "Orders", "CPA", "Conv rate", "Total Revenue", "AOV", "ROAS", "CTR", "Avg CPC"]
for c_idx, h in enumerate(meta_headers, start=1):
    cell = ws_rec.cell(row=14, column=c_idx, value=h)
    cell.font = header_font
    cell.fill = header_fill
    cell.alignment = align_center
    cell.border = cell_border

# October Meta Ads (Row 15)
ws_rec["A15"] = "October"
ws_rec["B15"] = 600.00
ws_rec["C15"] = "=D15/K15"        # 14,778
ws_rec["D15"] = "=B15/L15"        # 857.14
ws_rec["E15"] = "=G15*D15"        # 27.0 orders
ws_rec["F15"] = "=B15/E15"        # £22.22 CPA
ws_rec["G15"] = 0.0315            # 3.15% Conv Rate
ws_rec["H15"] = "=I15*E15"        # £688.50 Revenue
ws_rec["I15"] = 25.50             # £25.50 AOV
ws_rec["J15"] = "=H15/B15"        # 1.15 ROAS
ws_rec["K15"] = 0.058             # 5.80% CTR
ws_rec["L15"] = 0.70              # £0.70 Avg CPC

# November Meta Ads (Row 16)
ws_rec["A16"] = "November"
ws_rec["B16"] = 700.00
ws_rec["C16"] = "=D16/K16"        # 17,107
ws_rec["D16"] = "=B16/L16"        # 1,060.61
ws_rec["E16"] = "=G16*D16"        # 40.0 orders
ws_rec["F16"] = "=B16/E16"        # £17.50 CPA
ws_rec["G16"] = 0.03771429        # 3.77% Conv Rate
ws_rec["H16"] = "=I16*E16"        # £1,120.00 Revenue
ws_rec["I16"] = 28.00             # £28.00 AOV
ws_rec["J16"] = "=H16/B16"        # 1.60 ROAS
ws_rec["K16"] = 0.062             # 6.20% CTR
ws_rec["L16"] = 0.66              # £0.66 Avg CPC

# December Meta Ads (Row 17)
ws_rec["A17"] = "December"
ws_rec["B17"] = 800.00
ws_rec["C17"] = "=D17/K17"        # 19,851
ws_rec["D17"] = "=B17/L17"        # 1,230.77
ws_rec["E17"] = "=G17*D17"        # 44.0 orders
ws_rec["F17"] = "=B17/E17"        # £18.18 CPA
ws_rec["G17"] = 0.03574634        # 3.57% Conv Rate
ws_rec["H17"] = "=I17*E17"        # £1,276.00 Revenue
ws_rec["I17"] = 29.00             # £29.00 AOV
ws_rec["J17"] = "=H17/B17"        # 1.60 ROAS
ws_rec["K17"] = 0.062             # 6.20% CTR
ws_rec["L17"] = 0.65              # £0.65 Avg CPC

# Total Meta Ads (Row 18)
ws_rec["A18"] = "Total"
ws_rec["B18"] = "=SUM(B15:B17)"   # £2,100.00
ws_rec["C18"] = "=SUM(C15:C17)"
ws_rec["D18"] = "=SUM(D15:D17)"
ws_rec["E18"] = "=SUM(E15:E17)"   # 111 orders
ws_rec["F18"] = "=B18/E18"        # £18.92 CPA
ws_rec["G18"] = "=E18/D18"        # 3.53% Conv Rate
ws_rec["H18"] = "=SUM(H15:H17)"   # £3,084.50 Revenue
ws_rec["I18"] = "=H18/E18"        # £27.79 AOV
ws_rec["J18"] = "=H18/B18"        # 1.47 ROAS
ws_rec["K18"] = "=D18/C18"        # 6.08% CTR
ws_rec["L18"] = "=B18/D18"        # £0.67 Avg CPC

# Format Meta Ads Rows 15-18
for r in range(15, 19):
    is_tot = (r == 18)
    ws_rec.cell(r, 1).alignment = align_left
    ws_rec.cell(r, 1).font = total_font if is_tot else bold_font
    ws_rec.cell(r, 1).border = total_border if is_tot else cell_border
    if is_tot: ws_rec.cell(r, 1).fill = total_fill
    
    for c in range(2, 13):
        cell = ws_rec.cell(r, c)
        cell.font = total_font if is_tot else regular_font
        cell.border = total_border if is_tot else cell_border
        cell.alignment = align_right
        if is_tot: cell.fill = total_fill
        
        if c in [2, 6, 8, 9, 12]: # Currency
            cell.number_format = currency_fmt
        elif c in [3, 4, 5]: # Counts
            cell.number_format = number_fmt
        elif c in [7, 11]: # Percentage
            cell.number_format = percent_fmt
        elif c == 10: # ROAS
            cell.number_format = decimal_fmt


# =============================================================
# 2. UPDATE 'Forecast - Aggressive' (FIX ENCODING, ADD TOTALS)
# =============================================================
ws_agg = wb["Forecast - Aggressive"]

# Fix all number formats in Forecast - Aggressive that had broken currency format
for r in range(1, 19):
    for c in range(1, 13):
        cell = ws_agg.cell(r, c)
        if cell.number_format:
            fmt_str = str(cell.number_format)
            if "" in fmt_str or "?" in fmt_str:
                cell.number_format = currency_fmt

# Add Total Rows in Forecast - Aggressive
# Row 6: Shopify Total
ws_agg["A6"] = "3-Month Total"
ws_agg["B6"] = "=SUM(B3:B5)"
ws_agg["C6"] = "=SUM(C3:C5)"
ws_agg["D6"] = "=SUM(D3:D5)"
ws_agg["E6"] = "=SUM(E3:E5)"
ws_agg["F6"] = "=B6/C6"
ws_agg["G6"] = "=B6/E6"
ws_agg["H6"] = "=SUM(H3:H5)"
ws_agg["I6"] = "=H6/E6"
ws_agg["J6"] = "=H6/B6"

for c in range(1, 11):
    cell = ws_agg.cell(6, c)
    cell.font = total_font
    cell.fill = total_fill
    cell.border = total_border
    if c == 1:
        cell.alignment = align_left
    else:
        cell.alignment = align_right
        if c in [2, 6, 7, 8, 9]:
            cell.number_format = currency_fmt
        elif c in [3, 4, 5]:
            cell.number_format = number_fmt
        elif c == 10:
            cell.number_format = decimal_fmt

# Row 12: Google Ads Total
ws_agg["A12"] = "Total"
ws_agg["B12"] = "=SUM(B9:B11)"
ws_agg["C12"] = "=SUM(C9:C11)"
ws_agg["D12"] = "=SUM(D9:D11)"
ws_agg["E12"] = "=SUM(E9:E11)"
ws_agg["F12"] = "=B12/E12"
ws_agg["G12"] = "=E12/D12"
ws_agg["H12"] = "=SUM(H9:H11)"
ws_agg["I12"] = "=H12/E12"
ws_agg["J12"] = "=H12/B12"
ws_agg["K12"] = "=D12/C12"
ws_agg["L12"] = "=B12/D12"

for c in range(1, 13):
    cell = ws_agg.cell(12, c)
    cell.font = total_font
    cell.fill = total_fill
    cell.border = total_border
    if c == 1:
        cell.alignment = align_left
    else:
        cell.alignment = align_right
        if c in [2, 6, 8, 9, 12]:
            cell.number_format = currency_fmt
        elif c in [3, 4, 5]:
            cell.number_format = number_fmt
        elif c in [7, 11]:
            cell.number_format = percent_fmt
        elif c == 10:
            cell.number_format = decimal_fmt

# Row 18: Meta Ads Total
ws_agg["A18"] = "Total"
ws_agg["B18"] = "=SUM(B15:B17)"
ws_agg["C18"] = "=SUM(C15:C17)"
ws_agg["D18"] = "=SUM(D15:D17)"
ws_agg["E18"] = "=SUM(E15:E17)"
ws_agg["F18"] = "=B18/E18"
ws_agg["G18"] = "=E18/D18"
ws_agg["H18"] = "=SUM(H15:H17)"
ws_agg["I18"] = "=H18/E18"
ws_agg["J18"] = "=H18/B18"
ws_agg["K18"] = "=D18/C18"
ws_agg["L18"] = "=B18/D18"

for c in range(1, 13):
    cell = ws_agg.cell(18, c)
    cell.font = total_font
    cell.fill = total_fill
    cell.border = total_border
    if c == 1:
        cell.alignment = align_left
    else:
        cell.alignment = align_right
        if c in [2, 6, 8, 9, 12]:
            cell.number_format = currency_fmt
        elif c in [3, 4, 5]:
            cell.number_format = number_fmt
        elif c in [7, 11]:
            cell.number_format = percent_fmt
        elif c == 10:
            cell.number_format = decimal_fmt

# Adjust column widths nicely for both sheets
for ws in [ws_rec, ws_agg]:
    for col in range(1, 13):
        col_letter = get_column_letter(col)
        max_len = 0
        for row in range(1, 19):
            val = ws.cell(row, col).value
            if val is not None:
                max_len = max(max_len, len(str(val)))
        ws.column_dimensions[col_letter].width = max(max_len + 3, 13)

# Save workbook
wb.save(file_path)
print(f"Successfully updated and saved: {file_path}")

# Copy to reports/Forecast - 25 Sept.xlsx for mirror sync
shutil.copyfile(file_path, "reports/Forecast - 25 Sept.xlsx")
print("Mirrored to reports/Forecast - 25 Sept.xlsx")
