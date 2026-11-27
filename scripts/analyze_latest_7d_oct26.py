import pandas as pd
import numpy as np

f = r'c:\Users\test\Videos\Office\data\IAOL\Search terms report.xlsx'
df = pd.read_excel(f, skiprows=2)

num_cols = ['Cost', 'Clicks', 'Impr.', 'Avg. CPC', 'Conversions', 'Cost / conv.', 'Conv. rate']
for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)

# Filter out empty or summary rows
df = df[df['Search term'].notnull() & (df['Search term'] != '--') & (~df['Search term'].astype(str).str.startswith('Total'))]

print(f"Total Rows: {len(df)}")
print("Date Range: October 19, 2026 - October 25, 2026")

# Campaign summary
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

print("\n=== CAMPAIGN PERFORMANCE (OCT 19 - OCT 25, 2026) ===")
print(camp_summary.to_string(index=False))

tot_cost = df['Cost'].sum()
tot_clicks = df['Clicks'].sum()
tot_conv = df['Conversions'].sum()
tot_impr = df['Impr.'].sum()
avg_cpc = tot_cost / tot_clicks if tot_clicks > 0 else 0
cpa = tot_cost / tot_conv if tot_conv > 0 else 0
cvr = (tot_conv / tot_clicks * 100) if tot_clicks > 0 else 0
ctr = (tot_clicks / tot_impr * 100) if tot_impr > 0 else 0

print("\n=== ACCOUNT SEARCH TOTALS (OCT 19 - OCT 25, 2026) ===")
print(f"Spend: Rs. {tot_cost:,.2f}")
print(f"Clicks: {tot_clicks:,.0f} | Impr: {tot_impr:,.0f} | CTR: {ctr:.2f}%")
print(f"Leads (Conv): {tot_conv:.2f}")
print(f"Avg CPC: Rs. {avg_cpc:.2f}")
print(f"CPA: Rs. {cpa:.2f}")
print(f"CVR: {cvr:.2f}%")

# Match type breakdown
print("\n=== MATCH TYPE BREAKDOWN ===")
mt = df.groupby('Match type').agg({'Cost': 'sum', 'Clicks': 'sum', 'Conversions': 'sum'}).reset_index()
mt['Avg_CPC'] = (mt['Cost'] / mt['Clicks']).round(2)
mt['CPA'] = (mt['Cost'] / mt['Conversions']).round(2)
mt['CVR'] = (mt['Conversions'] / mt['Clicks'] * 100).round(2)
print(mt.to_string(index=False))

# Zero conversion waste
zero = df[df['Conversions'] == 0]
print("\n=== ZERO-CONVERSION WASTE ===")
print(f"Zero Conv Query Count: {len(zero)} / {len(df)} ({len(zero)/len(df)*100:.1f}%)")
print(f"Zero Conv Spend: Rs. {zero['Cost'].sum():,.2f} ({zero['Cost'].sum()/tot_cost*100:.1f}% of total spend)")

z_camp = zero.groupby('Campaign').agg({'Cost':'sum', 'Clicks':'sum'}).reset_index()
c_tot = df.groupby('Campaign')['Cost'].sum().to_dict()
z_camp['Camp_Total_Cost'] = z_camp['Campaign'].map(c_tot)
z_camp['Waste_Pct'] = (z_camp['Cost'] / z_camp['Camp_Total_Cost'] * 100).round(1)
print(z_camp.sort_values('Cost', ascending=False).to_string(index=False))

# High CPC spikes
print("\n=== HIGH CPC SPIKES (Avg CPC >= Rs 150) ===")
spikes = df[df['Avg. CPC'] >= 150].sort_values('Cost', ascending=False)
print(f"Queries with CPC >= Rs 150: {len(spikes)} | Total Cost: Rs. {spikes['Cost'].sum():,.2f}")
for _, r in spikes.head(15).iterrows():
    print(f"[{r['Campaign']}] '{r['Search term']}' ({r['Match type']}) -> Spend: Rs.{r['Cost']:.2f} | Clicks: {r['Clicks']:.0f} | CPC: Rs.{r['Avg. CPC']:.2f} | Conv: {r['Conversions']}")
