import pandas as pd
import numpy as np

f7 = r'c:\Users\test\Videos\Office\data\IAOL\Search terms report - last 7 days.xlsx'
f14 = r'c:\Users\test\Videos\Office\data\IAOL\Search terms report - last 14 days.xlsx'

def process_report(filepath, name):
    df = pd.read_excel(filepath, skiprows=2)
    num_cols = ['Cost', 'Clicks', 'Impr.', 'Avg. CPC', 'Conversions', 'Cost / conv.', 'Conv. rate']
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)
    
    df = df[df['Search term'].notnull() & (df['Search term'] != '--') & (~df['Search term'].astype(str).str.startswith('Total'))]
    
    print(f"\n{'='*80}\n=== {name} SUMMARY ===\n{'='*80}")
    print(f"Total Rows: {len(df)}")
    
    camp_summary = df.groupby('Campaign').agg({
        'Cost': 'sum',
        'Clicks': 'sum',
        'Impr.': 'sum',
        'Conversions': 'sum'
    }).reset_index()
    
    camp_summary['Avg_CPC'] = (camp_summary['Cost'] / camp_summary['Clicks']).round(2)
    camp_summary['CTR'] = (camp_summary['Clicks'] / camp_summary['Impr.'] * 100).round(2)
    camp_summary['CPA'] = (camp_summary['Cost'] / camp_summary['Conversions']).round(2)
    camp_summary['CVR'] = (camp_summary['Conversions'] / camp_summary['Clicks'] * 100).round(2)
    camp_summary = camp_summary.sort_values('Cost', ascending=False)
    
    print(camp_summary.to_string(index=False))
    
    tot_cost = df['Cost'].sum()
    tot_clicks = df['Clicks'].sum()
    tot_conv = df['Conversions'].sum()
    tot_impr = df['Impr.'].sum()
    avg_cpc = tot_cost / tot_clicks if tot_clicks > 0 else 0
    cpa = tot_cost / tot_conv if tot_conv > 0 else 0
    cvr = (tot_conv / tot_clicks * 100) if tot_clicks > 0 else 0
    ctr = (tot_clicks / tot_impr * 100) if tot_impr > 0 else 0
    
    print(f"\nAccount Totals ({name}):")
    print(f"  Spend: Rs. {tot_cost:,.2f}")
    print(f"  Clicks: {tot_clicks:,.0f} | Impr: {tot_impr:,.0f} | CTR: {ctr:.2f}%")
    print(f"  Leads (Conv): {tot_conv:.2f}")
    print(f"  Avg CPC: Rs. {avg_cpc:.2f}")
    print(f"  CPA: Rs. {cpa:.2f}")
    print(f"  CVR: {cvr:.2f}%")
    
    return df

df7 = process_report(f7, "LAST 7 DAYS (Oct 15 - Oct 21, 2026)")
df14 = process_report(f14, "LAST 14 DAYS (Oct 8 - Oct 21, 2026)")
