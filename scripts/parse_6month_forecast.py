import pandas as pd
import json

fpath = r'data/fabb6/FABB6_6-Month_Order_Forecast.xlsx'
xl = pd.ExcelFile(fpath)

for sheet in xl.sheet_names:
    print(f"================ SHEET: {sheet} ================")
    df = xl.parse(sheet)
    # drop totally empty rows and columns
    df = df.dropna(how='all').dropna(how='all', axis=1)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    print(df.to_string().encode('ascii', errors='replace').decode('ascii'))
