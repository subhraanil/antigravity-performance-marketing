import openpyxl
import pandas as pd

f1 = r'c:\Users\test\Videos\Office\data\IAOL\Ad report (2).xlsx'
f2 = r'c:\Users\test\Videos\Office\data\IAOL\Search terms report - this month oct.xlsx'

print("=== CHECKING AD REPORT (2).xlsx ===")
wb1 = openpyxl.load_workbook(f1)
print("All Sheet Names:", wb1.sheetnames)
for name in wb1.sheetnames:
    sheet = wb1[name]
    print(f"Sheet '{name}': sheet_state = {sheet.sheet_state}, max_row = {sheet.max_row}, max_column = {sheet.max_column}")

print("\nFirst 10 rows of Ad report:")
df_ad_raw = pd.read_excel(f1, header=None)
print(df_ad_raw.iloc[:10, :10])

print("\n=== CHECKING SEARCH TERMS REPORT - THIS MONTH OCT.xlsx ===")
wb2 = openpyxl.load_workbook(f2)
print("All Sheet Names:", wb2.sheetnames)
for name in wb2.sheetnames:
    sheet = wb2[name]
    print(f"Sheet '{name}': sheet_state = {sheet.sheet_state}, max_row = {sheet.max_row}, max_column = {sheet.max_column}")

print("\nFirst 10 rows of Search terms report:")
df_st_raw = pd.read_excel(f2, header=None)
print(df_st_raw.iloc[:10, :10])
