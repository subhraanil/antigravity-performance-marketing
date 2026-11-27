import pandas as pd
import numpy as np

f_st = r'c:\Users\test\Videos\Office\data\IAOL\Search terms report - this month oct.xlsx'
df = pd.read_excel(f_st, skiprows=2)

num_cols = ['Cost', 'Clicks', 'Impr.', 'Avg. CPC', 'Conversions', 'Cost / conv.', 'Conv. rate']
for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)

# Filter valid rows
df = df[df['Search term'].notnull() & (df['Search term'] != '--') & (~df['Search term'].astype(str).str.startswith('Total'))]

print(f"Total Search Terms Rows: {len(df)}")
print(f"Date Range: October 1, 2026 - October 15, 2026 (15 days)")

# 1. Campaign summary
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

print("\n=== CAMPAIGN PERFORMANCE (OCT 1 - OCT 15, 2026) ===")
print(camp_summary.to_string(index=False))

total_cost = df['Cost'].sum()
total_clicks = df['Clicks'].sum()
total_conv = df['Conversions'].sum()
print("\n=== OVERALL ACCOUNT SEARCH TOTALS ===")
print(f"Total Spend: Rs. {total_cost:,.2f}")
print(f"Total Clicks: {total_clicks:,.0f}")
print(f"Total Conversions: {total_conv:.1f}")
print(f"Avg CPC: Rs. {total_cost/total_clicks:.2f}")
print(f"Account CPA: Rs. {total_cost/total_conv:.2f}")
print(f"Account CVR: {total_conv/total_clicks*100:.2f}%")

# 2. Zero-conversion waste
zero_conv = df[df['Conversions'] == 0]
zero_cost = zero_conv['Cost'].sum()
zero_clicks = zero_conv['Clicks'].sum()
print("\n=== ZERO CONVERSION WASTE (OCT 1 - 15) ===")
print(f"Zero-Conv Query Count: {len(zero_conv)} / {len(df)} ({len(zero_conv)/len(df)*100:.1f}%)")
print(f"Zero-Conv Spend: Rs. {zero_cost:,.2f} ({zero_cost/total_cost*100:.1f}% of total spend!)")
print(f"Zero-Conv Clicks: {zero_clicks:,.0f} ({zero_clicks/total_clicks*100:.1f}% of total clicks)")

# Zero-conv by campaign
zero_by_camp = zero_conv.groupby('Campaign').agg({'Cost': 'sum', 'Clicks': 'sum'}).reset_index()
zero_by_camp['Pct_Camp_Spend'] = (zero_by_camp['Cost'] / zero_by_camp['Campaign'].map(camp_summary.set_index('Campaign')['Cost']) * 100).round(1)
print("\nZero-Conversion Waste by Campaign:")
print(zero_by_camp.to_string(index=False))

# 3. Match type analysis in search terms
print("\n=== MATCH TYPE BREAKDOWN IN SEARCH TERMS ===")
mt_summary = df.groupby('Match type').agg({'Cost': 'sum', 'Clicks': 'sum', 'Conversions': 'sum'}).reset_index()
mt_summary['Avg_CPC'] = (mt_summary['Cost'] / mt_summary['Clicks']).round(2)
mt_summary['CPA'] = (mt_summary['Cost'] / mt_summary['Conversions']).round(2)
mt_summary['CVR'] = (mt_summary['Conversions'] / mt_summary['Clicks'] * 100).round(2)
print(mt_summary.to_string(index=False))
