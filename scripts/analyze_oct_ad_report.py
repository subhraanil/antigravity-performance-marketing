import pandas as pd
import numpy as np
import os

oct_folder = r'C:\Users\test\Videos\Office\data\IAOL\October'
f_ad = os.path.join(oct_folder, 'Ad report (2).xlsx')
df_ad = pd.read_excel(f_ad, skiprows=2)

num_cols_ad = ['Cost', 'Clicks', 'Impr.', 'Avg. CPC', 'Conversions', 'Cost / conv.', 'Conv. rate']
for c in num_cols_ad:
    if c in df_ad.columns:
        df_ad[c] = pd.to_numeric(df_ad[c].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)

df_ad = df_ad[df_ad['Campaign'].notnull() & (df_ad['Campaign'] != '--') & (df_ad['Ad group'].notnull())]

print("=" * 80)
print("3. AD REPORT (OCTOBER 1 - OCTOBER 31, 2026)")
print("=" * 80)
print(f"Total Ads: {len(df_ad)}")

for camp, grp in df_ad.groupby('Campaign'):
    print(f"\n--- CAMPAIGN: {camp} ---")
    tot_cost = grp['Cost'].sum()
    tot_clicks = grp['Clicks'].sum()
    tot_conv = grp['Conversions'].sum()
    print(f"Total Campaign Ad Spend: Rs.{tot_cost:,.2f} | Clicks: {tot_clicks} | Conv: {tot_conv} | CPA: Rs.{tot_cost/tot_conv if tot_conv>0 else 0:,.2f}")
    for idx, r in grp.iterrows():
        cpa = r['Cost'] / r['Conversions'] if r['Conversions'] > 0 else 0
        cvr = (r['Conversions'] / r['Clicks'] * 100) if r['Clicks'] > 0 else 0
        ctr = (r['Clicks'] / r['Impr.'] * 100) if r['Impr.'] > 0 else 0
        print(f"  Ad #{idx} | Status: {r['Ad status']} | Strength: {r['Ad strength']} | Clicks: {r['Clicks']} | Impr: {r['Impr.']} | CTR: {ctr:.1f}% | CPC: Rs.{r['Avg. CPC']:.2f} | Cost: Rs.{r['Cost']:,.2f} | Conv: {r['Conversions']} | CPA: Rs.{cpa:.2f} | CVR: {cvr:.1f}%")
        print(f"    URL: {r['Final URL']}")
        # print headlines
        h_list = [f"H{i}: {r[f'Headline {i}']}" for i in range(1, 16) if f'Headline {i}' in r and pd.notnull(r[f'Headline {i}']) and str(r[f'Headline {i}']).strip() not in ['--', 'nan', '']]
        print(f"    Headlines ({len(h_list)}): {', '.join(h_list[:5])}...")
