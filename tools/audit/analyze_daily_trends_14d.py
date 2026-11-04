import pandas as pd

excel_path = r'data/IAOL/October/IAOL-GoogleAds.xlsx'
camps = ['French-Bangalore', 'French-Mumbai', 'German-Bangalore', 'German-Hydrabad', 'German-Mumbai', 'German-Pune', 'New Merged']

for camp in camps:
    df = pd.read_excel(excel_path, sheet_name=camp)
    date_col = [c for c in df.columns if 'date' in str(c).lower() or 'day' in str(c).lower()][0]
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    df = df.dropna(subset=[date_col]).sort_values(by=date_col)
    
    last14 = df[df[date_col] >= '2026-10-19']
    print(f"\n==========================================")
    print(f"CAMPAIGN: {camp}")
    print(f"==========================================")
    print("Last 14 days daily performance:")
    cols = [date_col, 'Cost', 'Clicks', 'Leads', 'Avg CPC'] if 'Avg CPC' in df.columns else [date_col, 'Cost', 'Clicks', 'Leads']
    sub = last14[cols].copy()
    sub['CPA'] = sub['Cost'] / sub['Leads'].replace(0, pd.NA)
    sub['CvR%'] = (sub['Leads'] / sub['Clicks'].replace(0, pd.NA)) * 100
    print(sub.to_string(index=False))
