import pandas as pd
import numpy as np

f7 = r'c:\Users\test\Videos\Office\data\IAOL\Search terms report - last 7 days.xlsx'
f14 = r'c:\Users\test\Videos\Office\data\IAOL\Search terms report - last 14 days.xlsx'

df7 = pd.read_excel(f7, skiprows=2)
df14 = pd.read_excel(f14, skiprows=2)

num_cols = ['Cost', 'Clicks', 'Impr.', 'Avg. CPC', 'Conversions', 'Cost / conv.', 'Conv. rate']
for df in [df7, df14]:
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)

df7 = df7[df7['Search term'].notnull() & (df7['Search term'] != '--') & (~df7['Search term'].astype(str).str.startswith('Total'))]
df14 = df14[df14['Search term'].notnull() & (df14['Search term'] != '--') & (~df14['Search term'].astype(str).str.startswith('Total'))]

# Check existing negatives
neg_file = r"c:\Users\test\Videos\Office\data\IAOL\Negative keyword details report.xlsx"
df_neg = pd.read_excel(neg_file, skiprows=2)
existing_negs = set(df_neg['keyword_text'].dropna().astype(str).str.strip().str.lower().tolist())

print("=== MATCH TYPE PERFORMANCE IN LAST 7 DAYS ===")
mt7 = df7.groupby('Match type').agg({'Cost': 'sum', 'Clicks': 'sum', 'Conversions': 'sum'}).reset_index()
mt7['Avg_CPC'] = (mt7['Cost'] / mt7['Clicks']).round(2)
mt7['CPA'] = (mt7['Cost'] / mt7['Conversions']).round(2)
mt7['CVR'] = (mt7['Conversions'] / mt7['Clicks'] * 100).round(2)
print(mt7.to_string(index=False))

print("\n=== MATCH TYPE PERFORMANCE IN LAST 14 DAYS ===")
mt14 = df14.groupby('Match type').agg({'Cost': 'sum', 'Clicks': 'sum', 'Conversions': 'sum'}).reset_index()
mt14['Avg_CPC'] = (mt14['Cost'] / mt14['Clicks']).round(2)
mt14['CPA'] = (mt14['Cost'] / mt14['Conversions']).round(2)
mt14['CVR'] = (mt14['Conversions'] / mt14['Clicks'] * 100).round(2)
print(mt14.to_string(index=False))

print("\n=== ZERO-CONVERSION WASTE IN LAST 7 DAYS ===")
zero7 = df7[df7['Conversions'] == 0]
tot_cost7 = df7['Cost'].sum()
print(f"Zero Conv Terms Count: {len(zero7)} / {len(df7)} ({len(zero7)/len(df7)*100:.1f}%)")
print(f"Zero Conv Spend: Rs. {zero7['Cost'].sum():,.2f} ({zero7['Cost'].sum()/tot_cost7*100:.1f}% of total 7d spend!)")

print("\nZero Conv Waste by Campaign (Last 7 Days):")
z7_camp = zero7.groupby('Campaign').agg({'Cost':'sum', 'Clicks':'sum'}).reset_index()
c7_tot = df7.groupby('Campaign')['Cost'].sum().to_dict()
z7_camp['Camp_Total_Cost'] = z7_camp['Campaign'].map(c7_tot)
z7_camp['Waste_Pct'] = (z7_camp['Cost'] / z7_camp['Camp_Total_Cost'] * 100).round(1)
print(z7_camp.sort_values('Cost', ascending=False).to_string(index=False))

print("\n=== EXTREME CPC SPIKES (> Rs 150) IN LAST 7 DAYS ===")
spikes7 = df7[df7['Avg. CPC'] >= 150].sort_values('Cost', ascending=False)
print(f"Count of queries with CPC >= Rs 150: {len(spikes7)} | Total Cost: Rs. {spikes7['Cost'].sum():,.2f}")
for _, r in spikes7.head(20).iterrows():
    print(f"[{r['Campaign']}] '{r['Search term']}' ({r['Match type']}) -> Spend: Rs.{r['Cost']:.2f} | Clicks: {r['Clicks']:.0f} | CPC: Rs.{r['Avg. CPC']:.2f} | Conv: {r['Conversions']}")
