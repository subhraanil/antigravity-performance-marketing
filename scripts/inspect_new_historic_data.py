import openpyxl

excel_path = r'data/fabb6/Historic Data.xlsx'
wb = openpyxl.load_workbook(excel_path, data_only=True)

print("Sheet names in 'Historic Data.xlsx':", wb.sheetnames)

for sheetname in wb.sheetnames:
    print(f"\n=================== SHEET: {sheetname} ===================")
    ws = wb[sheetname]
    for r in range(1, ws.max_row + 1):
        row_vals = [ws.cell(row=r, column=c).value for c in range(1, ws.max_column + 1)]
        if any(v is not None for v in row_vals):
            row_str = " | ".join([str(v).replace('\u20b9', 'INR ') if v is not None else "" for v in row_vals])
            print(f"Row {r:2d}: {row_str}")
