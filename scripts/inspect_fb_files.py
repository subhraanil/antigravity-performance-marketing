import pandas as pd
import openpyxl

print("=== 1. GOOGLE SHEET DATA (French-Bangalore) ===")
df_gs = pd.read_csv('scripts/fb_google_sheet_export.csv')
for col in df_gs.columns:
    if df_gs[col].dtype == object:
        df_gs[col] = df_gs[col].astype(str).str.replace('₹', '').str.replace(',', '').str.strip()

print("Tail 15 rows of Google Sheet:")
for idx, r in df_gs.tail(15).iterrows():
    print(dict(r))

print("\n=== 2. FB/Search keyword report.xlsx ===")
kw_path = r'data/IAOL/October/FB/Search keyword report.xlsx'
wb_kw = openpyxl.load_workbook(kw_path, data_only=True)
print("Keyword report sheets:", wb_kw.sheetnames)
df_kw = pd.read_excel(kw_path)
print("Keyword report head:")
print(df_kw.head(10).to_string().replace('₹', 'Rs'))

print("\n=== 3. FB/Search terms report.xlsx ===")
st_path = r'data/IAOL/October/FB/Search terms report.xlsx'
wb_st = openpyxl.load_workbook(st_path, data_only=True)
print("Search terms report sheets:", wb_st.sheetnames)
df_st = pd.read_excel(st_path)
print("Search terms report head:")
print(df_st.head(10).to_string().replace('₹', 'Rs'))
