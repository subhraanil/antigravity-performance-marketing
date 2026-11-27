import pandas as pd
import numpy as np

f_ad = r'c:\Users\test\Videos\Office\data\IAOL\Ad report (2).xlsx'
df_ad = pd.read_excel(f_ad, skiprows=2)

num_cols = ['Clicks', 'Impr.', 'Avg. CPC', 'Cost', 'Conv. rate', 'Conversions', 'Cost / conv.']
for c in num_cols:
    if c in df_ad.columns:
        df_ad[c] = pd.to_numeric(df_ad[c].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)

# Filter out empty or summary rows
df_ad = df_ad[df_ad['Campaign'].notnull() & (df_ad['Campaign'] != '--') & (df_ad['Ad group'].notnull())]

print(f"Total Ads Analyzed: {len(df_ad)}")
print("\n=== ADS BY CAMPAIGN ===")
print(df_ad['Campaign'].value_counts())

print("\n=== AD PERFORMANCE TABLE ===")
perf_cols = ['Campaign', 'Ad group', 'Ad status', 'Ad strength', 'Clicks', 'Impr.', 'CTR', 'Avg. CPC', 'Cost', 'Conversions', 'Cost / conv.', 'Conv. rate']
df_ad_perf = df_ad[perf_cols].copy()
df_ad_perf['CTR'] = (df_ad_perf['Clicks'] / df_ad_perf['Impr.'] * 100).round(2)
df_ad_perf['CPA'] = np.where(df_ad_perf['Conversions'] > 0, (df_ad_perf['Cost'] / df_ad_perf['Conversions']).round(2), 0)
df_ad_perf['CVR'] = np.where(df_ad_perf['Clicks'] > 0, (df_ad_perf['Conversions'] / df_ad_perf['Clicks'] * 100).round(2), 0)

for camp, grp in df_ad_perf.groupby('Campaign'):
    print(f"\n--- {camp} ---")
    for idx, row in grp.iterrows():
        print(f"Ad #{idx}: Status={row['Ad status']} | Strength={row['Ad strength']} | Clicks={row['Clicks']} | Impr={row['Impr.']} | CTR={row['CTR']}% | CPC=Rs.{row['Avg. CPC']:.2f} | Cost=Rs.{row['Cost']:.2f} | Conv={row['Conversions']} | CPA=Rs.{row['CPA']} | CVR={row['CVR']}%")

print("\n=== AD STRENGTH BREAKDOWN ===")
print(df_ad.groupby(['Campaign', 'Ad strength']).size().unstack(fill_value=0))

print("\n=== FINAL URLS USED ACROSS CAMPAIGNS ===")
for camp, grp in df_ad.groupby('Campaign'):
    print(f"{camp}:")
    for u in grp['Final URL'].unique():
        print(f"  - {u}")

print("\n=== HEADLINE PINNING AND IMPROVEMENTS ===")
for idx, row in df_ad.iterrows():
    pins = []
    for h in range(1, 16):
        pos_col = f'Headline {h} position'
        h_col = f'Headline {h}'
        if pos_col in row and pd.notnull(row[pos_col]) and str(row[pos_col]).strip() not in ['--', 'nan', '']:
            pins.append(f"H{h} ('{row[h_col]}') pinned to {row[pos_col]}")
    for d in range(1, 5):
        pos_col = f'Description {d} position'
        d_col = f'Description {d}'
        if pos_col in row and pd.notnull(row[pos_col]) and str(row[pos_col]).strip() not in ['--', 'nan', '']:
            pins.append(f"D{d} pinned to {row[pos_col]}")
    imprv = row.get('Ad strength improvements', '--')
    print(f"Ad #{idx} [{row['Campaign']} - {row['Ad group']}]: Pins: {pins if pins else 'None'} | Improvements: {imprv}")
