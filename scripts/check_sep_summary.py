import pandas as pd
import os

oct_folder = r'C:\Users\test\Videos\Office\data\IAOL\October'
f_mtd = os.path.join(oct_folder, 'MTD_Campaign.xlsx')

df_sep = pd.read_excel(f_mtd, sheet_name='SEP26_SUMMARY')
print("=== SEP26_SUMMARY ===")
rows = []
for idx, r in df_sep.iterrows():
    c_name = r.get('Till 30th sep')
    if pd.notnull(c_name) and str(c_name).strip() not in ['', 'TOTAL', 'nan']:
        rows.append(r)
df_s_clean = pd.DataFrame(rows)
cols = ['Till 30th sep', 'LEADS RECEIVED(crm)', 'GOOGLE LEADS', 'ACTUAL COST', 'Admission done', 'Conversion %', 'Collection', 'ROI']
cols_ex = [c for c in cols if c in df_s_clean.columns]
print(df_s_clean[cols_ex].to_string(index=False))
