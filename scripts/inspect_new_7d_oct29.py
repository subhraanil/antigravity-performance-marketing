import openpyxl
import pandas as pd

f = r'c:\Users\test\Videos\Office\data\IAOL\Search terms report.xlsx'
wb = openpyxl.load_workbook(f)
print("Sheet names:", wb.sheetnames)
for s in wb.sheetnames:
    ws = wb[s]
    print(f"Sheet: {s} | State: {ws.sheet_state} | Max row: {ws.max_row} | Max col: {ws.max_column}")

df_raw = pd.read_excel(f, header=None)
print("\nRow 0:", df_raw.iloc[0, 0])
print("Row 1 (Date range):", df_raw.iloc[1, 0])
print("Row 2 (Columns):", df_raw.iloc[2, :].dropna().tolist())
