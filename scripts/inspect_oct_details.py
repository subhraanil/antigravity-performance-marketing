import openpyxl
import pandas as pd
import os

oct_folder = r'C:\Users\test\Videos\Office\data\IAOL\October'

# 1. Ad report
f_ad = os.path.join(oct_folder, 'Ad report (2).xlsx')
df_ad_raw = pd.read_excel(f_ad, header=None)
print("=== AD REPORT HEADER ===")
print("Row 0:", df_ad_raw.iloc[0, 0])
print("Row 1 (Date range):", df_ad_raw.iloc[1, 0])
print("Row 2 (Columns):", df_ad_raw.iloc[2, :15].dropna().tolist())

# 2. Search keyword report
f_kw = os.path.join(oct_folder, 'Search keyword report.xlsx')
df_kw_raw = pd.read_excel(f_kw, header=None)
print("\n=== SEARCH KEYWORD REPORT HEADER ===")
print("Row 0:", df_kw_raw.iloc[0, 0])
print("Row 1 (Date range):", df_kw_raw.iloc[1, 0])
print("Row 2 (Columns):", df_kw_raw.iloc[2, :15].dropna().tolist())

# 3. Search terms report
f_st = os.path.join(oct_folder, 'Search terms report.xlsx')
df_st_raw = pd.read_excel(f_st, header=None)
print("\n=== SEARCH TERMS REPORT HEADER ===")
print("Row 0:", df_st_raw.iloc[0, 0])
print("Row 1 (Date range):", df_st_raw.iloc[1, 0])
print("Row 2 (Columns):", df_st_raw.iloc[2, :15].dropna().tolist())

# 4. IAOL-GoogleAds.xlsx tabs
f_ga = os.path.join(oct_folder, 'IAOL-GoogleAds.xlsx')
wb_ga = openpyxl.load_workbook(f_ga)
print("\n=== IAOL-GoogleAds.xlsx TABS PREVIEW ===")
for s in wb_ga.sheetnames:
    df_tab = pd.read_excel(f_ga, sheet_name=s)
    print(f"Tab '{s}': Shape {df_tab.shape} | Columns: {df_tab.columns.tolist()[:8]}")
    if len(df_tab) > 0:
        print(f"   First row: {df_tab.iloc[0].to_dict()}")
