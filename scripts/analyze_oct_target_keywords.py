import pandas as pd
import numpy as np
import os

oct_folder = r'C:\Users\test\Videos\Office\data\IAOL\October'

# -------------------------------------------------------------
# 1. TARGET KEYWORDS REPORT
# -------------------------------------------------------------
f_kw = os.path.join(oct_folder, 'Search keyword report.xlsx')
df_kw = pd.read_excel(f_kw, skiprows=2)

num_cols_kw = ['Cost', 'Clicks', 'Impr.', 'Avg. CPC', 'Conversions', 'Cost / conv.', 'Conv. rate']
for c in num_cols_kw:
    if c in df_kw.columns:
        df_kw[c] = pd.to_numeric(df_kw[c].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)

df_kw = df_kw[df_kw['Campaign'].notnull() & (df_kw['Campaign'] != '--') & (df_kw['Keyword'].notnull())]

print("=" * 80)
print("1. TARGET KEYWORDS PERFORMANCE (OCT 1 - OCT 31, 2026)")
print("=" * 80)
kw_camp = df_kw.groupby('Campaign').agg({
    'Cost': 'sum',
    'Clicks': 'sum',
    'Impr.': 'sum',
    'Conversions': 'sum'
}).reset_index()
kw_camp['Avg_CPC'] = kw_camp['Cost'] / kw_camp['Clicks']
kw_camp['CPA'] = kw_camp['Cost'] / kw_camp['Conversions']
kw_camp['CVR'] = kw_camp['Conversions'] / kw_camp['Clicks'] * 100
kw_camp = kw_camp.sort_values('Cost', ascending=False)
print(kw_camp.to_string(index=False))

print("\n--- Match Type Breakdown in Target Keywords ---")
kw_mt = df_kw.groupby('Match type').agg({'Cost': 'sum', 'Clicks': 'sum', 'Conversions': 'sum'}).reset_index()
kw_mt['Avg_CPC'] = kw_mt['Cost'] / kw_mt['Clicks']
kw_mt['CPA'] = kw_mt['Cost'] / kw_mt['Conversions']
kw_mt['CVR'] = kw_mt['Conversions'] / kw_mt['Clicks'] * 100
print(kw_mt.to_string(index=False))

# Zero conversion keywords
kw_zero = df_kw[df_kw['Conversions'] == 0]
print(f"\nZero-Conv Target Keywords: {len(kw_zero)} / {len(df_kw)} | Total Wasted Cost: Rs. {kw_zero['Cost'].sum():,.2f}")
print("Top 15 Zero-Conv Target Keywords by Spend:")
for _, r in kw_zero.sort_values('Cost', ascending=False).head(15).iterrows():
    print(f"  [{r['Campaign']}] '{r['Keyword']}' ({r['Match type']}) -> Spend: Rs.{r['Cost']:,.2f} | Clicks: {r['Clicks']:.0f} | CPC: Rs.{r['Avg. CPC']:.2f}")

# Top converting keywords
kw_conv = df_kw[df_kw['Conversions'] > 0]
print(f"\nConverting Target Keywords: {len(kw_conv)} / {len(df_kw)} | Total Conv Cost: Rs. {kw_conv['Cost'].sum():,.2f} | Total Leads: {kw_conv['Conversions'].sum():.1f} | Avg CPA: Rs. {kw_conv['Cost'].sum()/kw_conv['Conversions'].sum():.2f}")
print("Top 20 Converting Target Keywords by Leads:")
for _, r in kw_conv.sort_values('Conversions', ascending=False).head(20).iterrows():
    cpa_k = r['Cost'] / r['Conversions']
    print(f"  [{r['Campaign']}] '{r['Keyword']}' ({r['Match type']}) -> Leads: {r['Conversions']:.1f} | Spend: Rs.{r['Cost']:,.2f} | CPA: Rs.{cpa_k:.2f} | CVR: {r['Conv. rate']*100:.1f}%")

# High CPA Target Keywords (CPA > 1200)
kw_high_cpa = df_kw[(df_kw['Conversions'] > 0) & (df_kw['Cost'] / df_kw['Conversions'] > 1200)].sort_values('Cost', ascending=False)
print(f"\nHigh CPA Target Keywords (CPA > Rs 1,200): {len(kw_high_cpa)} | Spend: Rs. {kw_high_cpa['Cost'].sum():,.2f} | Leads: {kw_high_cpa['Conversions'].sum():.1f} | Avg CPA: Rs. {kw_high_cpa['Cost'].sum()/kw_high_cpa['Conversions'].sum():.2f}")
for _, r in kw_high_cpa.iterrows():
    cpa_k = r['Cost'] / r['Conversions']
    print(f"  [{r['Campaign']}] '{r['Keyword']}' ({r['Match type']}) -> Spend: Rs.{r['Cost']:,.2f} | Leads: {r['Conversions']:.1f} | CPA: Rs.{cpa_k:.2f}")
