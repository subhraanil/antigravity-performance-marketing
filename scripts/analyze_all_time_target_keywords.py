import pandas as pd

excel_file = r"c:\Users\test\Videos\Office\data\IAOL\IAOL - Target Keywords All time.xlsx"
df = pd.read_excel(excel_file, skiprows=2)

# clean numeric columns
num_cols = ['Impr.', 'Interactions', 'Cost', 'Avg. CPC', 'Clicks', 'Conversions', 'Cost / conv.']
for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)

# filter to valid rows
df = df[df['Campaign'].notnull() & (df['Campaign'] != '--') & (df['Keyword'].notnull())]

print("Total Rows:", len(df))
print("\n--- ALL TIME OVERALL METRICS ---")
total_spend = df['Cost'].sum()
total_clicks = df['Clicks'].sum()
total_impr = df['Impr.'].sum()
total_conv = df['Conversions'].sum()
avg_cpc = total_spend / total_clicks if total_clicks > 0 else 0
cpa = total_spend / total_conv if total_conv > 0 else 0
cvr = (total_conv / total_clicks * 100) if total_clicks > 0 else 0

print(f"Total Spend: Rs. {total_spend:,.2f}")
print(f"Total Clicks: {total_clicks:,.0f}")
print(f"Total Impr: {total_impr:,.0f}")
print(f"Total Leads/Conv: {total_conv:,.2f}")
print(f"Avg CPC: Rs. {avg_cpc:.2f}")
print(f"All Time CPA: Rs. {cpa:.2f}")
print(f"All Time CVR: {cvr:.2f}%")

print("\n--- CAMPAIGN BREAKDOWN (ALL TIME) ---")
camp_grp = df.groupby('Campaign').agg({
    'Cost': 'sum',
    'Clicks': 'sum',
    'Impr.': 'sum',
    'Conversions': 'sum'
}).reset_index()
camp_grp['Avg_CPC'] = camp_grp['Cost'] / camp_grp['Clicks']
camp_grp['CPA'] = camp_grp['Cost'] / camp_grp['Conversions']
camp_grp['CVR'] = camp_grp['Conversions'] / camp_grp['Clicks'] * 100
camp_grp = camp_grp.sort_values('Cost', ascending=False)
for _, r in camp_grp.iterrows():
    print(f"{r['Campaign']}: Spend Rs. {r['Cost']:,.2f} | Clicks: {r['Clicks']:,.0f} | Conv: {r['Conversions']:,.2f} | Avg CPC: Rs. {r['Avg_CPC']:.2f} | CPA: Rs. {r['CPA']:.2f} | CVR: {r['CVR']:.2f}%")

print("\n--- ZERO CONVERSION KEYWORDS (ALL TIME) ---")
zero_conv = df[df['Conversions'] == 0].sort_values('Cost', ascending=False)
zero_spend = zero_conv['Cost'].sum()
print(f"Zero Conv Keywords Count: {len(zero_conv)} | Total Wasted Spend: Rs. {zero_spend:,.2f} ({zero_spend/total_spend*100:.1f}% of total spend)")
print("\nTop 20 Wasted Spend Keywords (All Time with 0 Conversions):")
for _, r in zero_conv.head(20).iterrows():
    print(f"[{r['Campaign']}] {r['Keyword']} ({r['Match type']}) - Spend: Rs. {r['Cost']:,.2f} | Clicks: {r['Clicks']} | CPC: Rs. {r['Avg. CPC']:.2f}")

print("\n--- TOP CONVERTING KEYWORDS (ALL TIME) ---")
top_conv = df[df['Conversions'] >= 1].sort_values('Conversions', ascending=False)
print(f"Converting Keywords Count: {len(top_conv)} | Total Converting Spend: Rs. {top_conv['Cost'].sum():,.2f} | Total Leads: {top_conv['Conversions'].sum():,.2f} | Avg CPA: Rs. {top_conv['Cost'].sum()/top_conv['Conversions'].sum():,.2f}")
print("\nTop 25 Volume Drivers (All Time):")
for _, r in top_conv.head(25).iterrows():
    cpa_k = r['Cost'] / r['Conversions']
    cvr_k = (r['Conversions'] / r['Clicks'] * 100) if r['Clicks'] > 0 else 0
    print(f"[{r['Campaign']}] {r['Keyword']} ({r['Match type']}) - Spend: Rs. {r['Cost']:,.2f} | Leads: {r['Conversions']:.2f} | CPA: Rs. {cpa_k:.2f} | CVR: {cvr_k:.1f}% | CPC: Rs. {r['Avg. CPC']:.2f}")

print("\n--- HIGH CPA BLEEDERS (ALL TIME, CPA > Rs. 1,200 & Conv >= 1) ---")
high_cpa = df[(df['Conversions'] >= 1) & (df['Cost'] / df['Conversions'] > 1200)].sort_values('Cost', ascending=False)
print(f"High CPA Keywords Count: {len(high_cpa)} | Spend: Rs. {high_cpa['Cost'].sum():,.2f} | Leads: {high_cpa['Conversions'].sum():,.2f} | Avg CPA: Rs. {high_cpa['Cost'].sum()/high_cpa['Conversions'].sum():,.2f}")
for _, r in high_cpa.iterrows():
    cpa_k = r['Cost'] / r['Conversions']
    print(f"[{r['Campaign']}] {r['Keyword']} ({r['Match type']}) - Spend: Rs. {r['Cost']:,.2f} | Leads: {r['Conversions']:.2f} | CPA: Rs. {cpa_k:.2f}")
