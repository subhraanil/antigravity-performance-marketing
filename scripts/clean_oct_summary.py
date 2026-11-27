import pandas as pd
import os

oct_folder = r'C:\Users\test\Videos\Office\data\IAOL\October'
f_mtd = os.path.join(oct_folder, 'MTD_Campaign.xlsx')

df = pd.read_excel(f_mtd, sheet_name='OCT26_SUMMARY')

# The rows alternate or have specific names
print("Columns in OCT26_SUMMARY:", df.columns.tolist())

# Clean rows
rows = []
for idx, r in df.iterrows():
    c_name = r.get('Till 31st Oct')
    if pd.notnull(c_name) and str(c_name).strip() not in ['', 'TOTAL', 'nan']:
        rows.append(r)

df_clean = pd.DataFrame(rows)
cols_to_show = [
    'Till 31st Oct', 'TARGET LEADS', 'LEADS RECEIVED(crm)', 'GOOGLE LEADS',
    'TARGET COST', 'ACTUAL COST', 'TARGET CPA', 'ACTUAL CPA(GA)', 'ACTUAL CPA(CRM)',
    'Admission done', 'Conversion %', 'Collection', 'ROI'
]
cols_existing = [c for c in cols_to_show if c in df_clean.columns]
print(df_clean[cols_existing].to_string(index=False))
