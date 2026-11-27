import pandas as pd
import json
import os

folder = r'data/fabb6'

for fname in ['FABB66 Forecast.xlsx', 'FABB6_6-Month_Order_Forecast.xlsx']:
    fpath = os.path.join(folder, fname)
    print("==================================================")
    print(f"FILE: {fname}")
    xl = pd.ExcelFile(fpath)
    print("Sheets:", xl.sheet_names)
    for sname in xl.sheet_names:
        print(f"\n--- SHEET: {sname} ---")
        df = xl.parse(sname)
        text = df.to_string()
        print(text.encode('ascii', errors='replace').decode('ascii'))
