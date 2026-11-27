import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
import copy

wb_path = 'data/Pet Mode/Forecast - 25 Sept.xlsx'
wb = openpyxl.load_workbook(wb_path)

# 1. Rename existing 'Forecast' to 'Forecast - A'
if 'Forecast' in wb.sheetnames:
    ws_a = wb['Forecast']
    ws_a.title = 'Forecast - A'
else:
    ws_a = wb['Forecast - A']

# If 'Forecast - B' already exists, remove it first
if 'Forecast - B' in wb.sheetnames:
    wb.remove(wb['Forecast - B'])

# 2. Create 'Forecast - B' in the next tab
ws_b = wb.create_sheet(title='Forecast - B')
ws_b.views.sheetView[0].showGridLines = True

# Copy all cell properties, text, formulas, fills, and formats from ws_a to ws_b
for r in range(1, ws_a.max_row + 1):
    ws_b.row_dimensions[r].height = ws_a.row_dimensions[r].height
    for c in range(1, ws_a.max_column + 1):
        cell_a = ws_a.cell(r, c)
        cell_b = ws_b.cell(r, c)
        
        cell_b.value = cell_a.value
        if cell_a.has_style:
            cell_b.font = copy.copy(cell_a.font)
            cell_b.border = copy.copy(cell_a.border)
            cell_b.fill = copy.copy(cell_a.fill)
            cell_b.number_format = copy.copy(cell_a.number_format)
            cell_b.protection = copy.copy(cell_a.protection)
            cell_b.alignment = copy.copy(cell_a.alignment)

# Copy column dimensions
for col in ws_a.columns:
    col_letter = get_column_letter(col[0].column)
    if col_letter in ws_a.column_dimensions:
        ws_b.column_dimensions[col_letter].width = ws_a.column_dimensions[col_letter].width

# 3. Update the inputs for Forecast - B (Realistic Best Forecast)

# Shopify Store Inputs:
# Row 3: October Other orders = 10, AOV = 26.0 (same as A)
ws_b['D3'].value = 10.0
ws_b['I3'].value = 26.0

# Row 4: November Other orders = 14 (BFCM organic surge), AOV = 28.0
ws_b['D4'].value = 14.0
ws_b['I4'].value = 28.0

# Row 5: December Other orders = 14 (Holiday organic demand), AOV = 29.5 (realistic bundle AOV)
ws_b['D5'].value = 14.0
ws_b['I5'].value = 29.5

# Google Ads Inputs:
# Row 9 (October Google):
# Spend = 500, Conv Rate = 0.024 (2.4%), AOV = 27.0, CTR = 0.024 (2.4%), Avg CPC = 0.60
ws_b['B9'].value = 500.0
ws_b['G9'].value = 0.024
ws_b['I9'].value = 27.0
ws_b['K9'].value = 0.024
ws_b['L9'].value = 0.60

# Row 10 (November Google):
# Spend = 600, Conv Rate = 0.027 (2.7% BFCM intent), AOV = 28.0, CTR = 0.026 (2.6%), Avg CPC = 0.62
ws_b['B10'].value = 600.0
ws_b['G10'].value = 0.027
ws_b['I10'].value = 28.0
ws_b['K10'].value = 0.026
ws_b['L10'].value = 0.62

# Row 11 (December Google):
# Spend = 600, Conv Rate = 0.028 (2.8%), AOV = 29.5, CTR = 0.028 (2.8%), Avg CPC = 0.58
ws_b['B11'].value = 600.0
ws_b['G11'].value = 0.028
ws_b['I11'].value = 29.5
ws_b['K11'].value = 0.028
ws_b['L11'].value = 0.58

# Meta Ads Inputs:
# Row 15 (October Meta):
# Spend = 600, Conv Rate = 0.032 (3.2%), AOV = 25.5, CTR = 0.058 (5.8%), Avg CPC = 0.70
ws_b['B15'].value = 600.0
ws_b['G15'].value = 0.032
ws_b['I15'].value = 25.5
ws_b['K15'].value = 0.058
ws_b['L15'].value = 0.70

# Row 16 (November Meta):
# Spend = 700, Conv Rate = 0.038 (3.8% BFCM surge), AOV = 28.0, CTR = 0.062 (6.2%), Avg CPC = 0.66
ws_b['B16'].value = 700.0
ws_b['G16'].value = 0.038
ws_b['I16'].value = 28.0
ws_b['K16'].value = 0.062
ws_b['L16'].value = 0.66

# Row 17 (December Meta):
# Spend = 800, Conv Rate = 0.036 (3.6%), AOV = 29.0, CTR = 0.062 (6.2%), Avg CPC = 0.65
ws_b['B17'].value = 800.0
ws_b['G17'].value = 0.036
ws_b['I17'].value = 29.0
ws_b['K17'].value = 0.062
ws_b['L17'].value = 0.65

# Ensure formulas remain exact
ws_b['B3'].value = '=B9+B15'
ws_b['C3'].value = '=E9+E15'
ws_b['E3'].value = '=C3+D3'
ws_b['F3'].value = '=B3/C3'
ws_b['G3'].value = '=B3/E3'
ws_b['H3'].value = '=I3*E3'
ws_b['J3'].value = '=H3/B3'

ws_b['B4'].value = '=B10+B16'
ws_b['C4'].value = '=E10+E16'
ws_b['E4'].value = '=C4+D4'
ws_b['F4'].value = '=B4/C4'
ws_b['G4'].value = '=B4/E4'
ws_b['H4'].value = '=I4*E4'
ws_b['J4'].value = '=H4/B4'

ws_b['B5'].value = '=B11+B17'
ws_b['C5'].value = '=E11+E17'
ws_b['E5'].value = '=C5+D5'
ws_b['F5'].value = '=B5/C5'
ws_b['G5'].value = '=B5/E5'
ws_b['H5'].value = '=I5*E5'
ws_b['J5'].value = '=H5/B5'

# Google formulas
for r in [9, 10, 11]:
    ws_b[f'C{r}'].value = f'=D{r}/K{r}'
    ws_b[f'D{r}'].value = f'=B{r}/L{r}'
    ws_b[f'E{r}'].value = f'=G{r}*D{r}'
    ws_b[f'F{r}'].value = f'=B{r}/E{r}'
    ws_b[f'H{r}'].value = f'=I{r}*E{r}'
    ws_b[f'J{r}'].value = f'=H{r}/B{r}'

# Meta formulas
for r in [15, 16, 17]:
    ws_b[f'C{r}'].value = f'=D{r}/K{r}'
    ws_b[f'D{r}'].value = f'=B{r}/L{r}'
    ws_b[f'E{r}'].value = f'=G{r}*D{r}'
    ws_b[f'F{r}'].value = f'=B{r}/E{r}'
    ws_b[f'H{r}'].value = f'=I{r}*E{r}'
    ws_b[f'J{r}'].value = f'=H{r}/B{r}'

# Save to data/Pet Mode/Forecast - 25 Sept.xlsx
wb.save(wb_path)

# Also save mirror in reports/
reports_path = 'reports/Forecast - 25 Sept.xlsx'
wb.save(reports_path)

print(f"Successfully saved updated workbook with sheets: {wb.sheetnames}")
print(f"File saved to:\n1) {wb_path}\n2) {reports_path}")
