import openpyxl

excel_path = r'reports/Marketing metrics.xlsx'
wb = openpyxl.load_workbook(excel_path)
sheet = wb.active

for r in range(1, min(70, sheet.max_row + 1)):
    row_vals = [sheet.cell(row=r, column=c).value for c in range(1, min(10, sheet.max_column + 1))]
    if any(v is not None for v in row_vals):
        row_str = " | ".join([str(v).replace('\u20b9', 'INR ') if v is not None else "" for v in row_vals])
        print(f"Row {r:2d}: {row_str}")
