import openpyxl
import pandas as pd
import numpy as np

f_ga = r'C:\Users\test\Videos\Office\data\IAOL\October\IAOL-GoogleAds.xlsx'
wb = openpyxl.load_workbook(f_ga)

print("=" * 80)
print("ANALYZING IAOL-GoogleAds.xlsx (ALL 13 TABS)")
print("=" * 80)

oct_records = []
all_records = []

for s in wb.sheetnames:
    df = pd.read_excel(f_ga, sheet_name=s)
    # clean column names
    df.columns = [str(c).strip() for c in df.columns]
    
    # date column might be Date or Data
    date_col = 'Date' if 'Date' in df.columns else ('Data' if 'Data' in df.columns else df.columns[0])
    df['Parsed_Date'] = pd.to_datetime(df[date_col], errors='coerce')
    
    # clean numeric columns
    for col in ['Impression', 'Clicks', 'Leads', 'Cost']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)
    
    # filter valid dates
    valid_df = df[df['Parsed_Date'].notnull()].copy()
    
    # October 2026 slice
    oct_df = valid_df[(valid_df['Parsed_Date'] >= '2026-10-01') & (valid_df['Parsed_Date'] <= '2026-10-31')].copy()
    
    # All time stats
    tot_cost = valid_df['Cost'].sum()
    tot_clicks = valid_df['Clicks'].sum()
    tot_leads = valid_df['Leads'].sum()
    tot_impr = valid_df['Impression'].sum()
    
    all_records.append({
        'Tab': s,
        'Date_Min': valid_df['Parsed_Date'].min(),
        'Date_Max': valid_df['Parsed_Date'].max(),
        'Days': len(valid_df),
        'All_Cost': tot_cost,
        'All_Clicks': tot_clicks,
        'All_Leads': tot_leads,
        'All_CPA': tot_cost / tot_leads if tot_leads > 0 else 0,
        'All_CPC': tot_cost / tot_clicks if tot_clicks > 0 else 0,
    })
    
    # October stats
    oct_cost = oct_df['Cost'].sum()
    oct_clicks = oct_df['Clicks'].sum()
    oct_leads = oct_df['Leads'].sum()
    oct_impr = oct_df['Impression'].sum()
    oct_cpa = oct_cost / oct_leads if oct_leads > 0 else 0
    oct_cpc = oct_cost / oct_clicks if oct_clicks > 0 else 0
    oct_cvr = (oct_leads / oct_clicks * 100) if oct_clicks > 0 else 0
    oct_ctr = (oct_clicks / oct_impr * 100) if oct_impr > 0 else 0
    
    oct_records.append({
        'Tab': s,
        'Days_in_Oct': len(oct_df),
        'Oct_Cost': oct_cost,
        'Oct_Impr': oct_impr,
        'Oct_Clicks': oct_clicks,
        'Oct_Leads': oct_leads,
        'Oct_CTR': oct_ctr,
        'Oct_CPC': oct_cpc,
        'Oct_CPA': oct_cpa,
        'Oct_CVR': oct_cvr
    })

print("\n--- OCTOBER 2026 PERFORMANCE BY TAB IN IAOL-GoogleAds.xlsx ---")
oct_res = pd.DataFrame(oct_records)
print(oct_res.to_string(index=False))

print("\n--- ALL-TIME PERFORMANCE SUMMARY BY TAB ---")
all_res = pd.DataFrame(all_records)
print(all_res.to_string(index=False))
