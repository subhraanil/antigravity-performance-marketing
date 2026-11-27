import pandas as pd
import openpyxl

f_ga = r'C:\Users\test\Videos\Office\data\IAOL\October\IAOL-GoogleAds.xlsx'
wb = openpyxl.load_workbook(f_ga)

print("Checking dates across tabs in IAOL-GoogleAds.xlsx:")
for s in wb.sheetnames:
    df = pd.read_excel(f_ga, sheet_name=s)
    date_col = 'Date' if 'Date' in df.columns else ('Data' if 'Data' in df.columns else df.columns[0])
    df['Parsed_Date'] = pd.to_datetime(df[date_col], errors='coerce')
    v = df[df['Parsed_Date'].notnull()]
    if len(v) > 0:
        print(f"{s:<22}: Min={v['Parsed_Date'].min().strftime('%Y-%m-%d')} | Max={v['Parsed_Date'].max().strftime('%Y-%m-%d')} | Rows={len(v)}")
