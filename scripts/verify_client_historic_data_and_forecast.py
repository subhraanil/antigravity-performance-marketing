import openpyxl

excel_path = r'data/fabb6/Historic Data and Forecast.xlsx'

# Inspect values
wb_val = openpyxl.load_workbook(excel_path, data_only=True)
print("Sheet names:", wb_val.sheetnames)

for sheetname in wb_val.sheetnames:
    print(f"\n=================== SHEET: {sheetname} (Values) ===================")
    ws = wb_val[sheetname]
    for r in range(1, ws.max_row + 1):
        row_vals = [ws.cell(row=r, column=c).value for c in range(1, ws.max_column + 1)]
        if any(v is not None for v in row_vals):
            row_str = " | ".join([str(v).replace('\u20b9', 'INR ') if v is not None else "" for v in row_vals])
            print(f"Row {r:2d}: {row_str}")

# Inspect formulas
wb_form = openpyxl.load_workbook(excel_path, data_only=False)
for sheetname in wb_form.sheetnames:
    print(f"\n=================== SHEET: {sheetname} (Formulas) ===================")
    ws = wb_form[sheetname]
    for r in range(1, ws.max_row + 1):
        row_vals = [ws.cell(row=r, column=c).value for c in range(1, ws.max_column + 1)]
        if any(v is not None and str(v).startswith('=') for v in row_vals):
            row_str = " | ".join([str(v) if v is not None else "" for v in row_vals])
            print(f"Row {r:2d} Formulas: {row_str}")
