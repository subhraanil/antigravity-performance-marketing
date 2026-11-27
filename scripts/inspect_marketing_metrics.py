import openpyxl
import pandas as pd

excel_path = r'reports/Marketing metrics.xlsx'

wb = openpyxl.load_workbook(excel_path)
print("Sheet names in 'Marketing metrics.xlsx':", wb.sheetnames)

for sheet in wb.sheetnames:
    print(f"\n--- SHEET: {sheet} ---")
    df = pd.read_excel(excel_path, sheet_name=sheet)
    print(df.to_string())
