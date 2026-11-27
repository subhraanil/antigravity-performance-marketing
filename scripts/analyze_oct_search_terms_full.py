import pandas as pd
import numpy as np
import os

oct_folder = r'C:\Users\test\Videos\Office\data\IAOL\October'
f_st = os.path.join(oct_folder, 'Search terms report.xlsx')
df_st = pd.read_excel(f_st, skiprows=2)

num_cols_st = ['Cost', 'Clicks', 'Impr.', 'Avg. CPC', 'Conversions', 'Cost / conv.', 'Conv. rate']
for c in num_cols_st:
    if c in df_st.columns:
        df_st[c] = pd.to_numeric(df_st[c].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)

df_st = df_st[df_st['Search term'].notnull() & (df_st['Search term'] != '--') & (~df_st['Search term'].astype(str).str.startswith('Total'))]

print("=" * 80)
print("2. SEARCH TERMS REPORT (OCT 1 - OCT 31, 2026)")
print("=" * 80)
print(f"Total Unique Search Queries: {len(df_st)}")

st_camp = df_st.groupby('Campaign').agg({
    'Cost': 'sum',
    'Clicks': 'sum',
    'Impr.': 'sum',
    'Conversions': 'sum'
}).reset_index()
st_camp['Avg_CPC'] = st_camp['Cost'] / st_camp['Clicks']
st_camp['CTR'] = st_camp['Clicks'] / st_camp['Impr.'] * 100
st_camp['CPA'] = st_camp['Cost'] / st_camp['Conversions']
st_camp['CVR'] = st_camp['Conversions'] / st_camp['Clicks'] * 100
st_camp = st_camp.sort_values('Cost', ascending=False)
print(st_camp.to_string(index=False))

tot_cost = df_st['Cost'].sum()
tot_clicks = df_st['Clicks'].sum()
tot_conv = df_st['Conversions'].sum()
print(f"\nAccount Search Terms Total: Spend Rs.{tot_cost:,.2f} | Clicks: {tot_clicks} | Conv: {tot_conv:.1f} | Avg CPC: Rs.{tot_cost/tot_clicks:.2f} | CPA: Rs.{tot_cost/tot_conv:.2f} | CVR: {tot_conv/tot_clicks*100:.2f}%")

# Match type breakdown
print("\n--- Match Type Breakdown in Search Terms ---")
st_mt = df_st.groupby('Match type').agg({'Cost': 'sum', 'Clicks': 'sum', 'Conversions': 'sum'}).reset_index()
st_mt['Avg_CPC'] = st_mt['Cost'] / st_mt['Clicks']
st_mt['CPA'] = st_mt['Cost'] / st_mt['Conversions']
st_mt['CVR'] = st_mt['Conversions'] / st_mt['Clicks'] * 100
print(st_mt.to_string(index=False))

# Zero conversion waste
st_zero = df_st[df_st['Conversions'] == 0]
print(f"\nZero-Conv Search Terms: {len(st_zero)} / {len(df_st)} ({len(st_zero)/len(df_st)*100:.1f}%) | Wasted Spend: Rs. {st_zero['Cost'].sum():,.2f} ({st_zero['Cost'].sum()/tot_cost*100:.1f}%)")

st_z_camp = st_zero.groupby('Campaign').agg({'Cost': 'sum', 'Clicks': 'sum'}).reset_index()
camp_totals = df_st.groupby('Campaign')['Cost'].sum().to_dict()
st_z_camp['Camp_Total'] = st_z_camp['Campaign'].map(camp_totals)
st_z_camp['Waste_Pct'] = (st_z_camp['Cost'] / st_z_camp['Camp_Total'] * 100).round(1)
print(st_z_camp.sort_values('Cost', ascending=False).to_string(index=False))

# Load negative keyword details report to cross check
neg_file = r"c:\Users\test\Videos\Office\data\IAOL\Negative keyword details report.xlsx"
df_neg = pd.read_excel(neg_file, skiprows=2)
existing_negs = set(df_neg['keyword_text'].dropna().astype(str).str.strip().str.lower().tolist())

# Top 30 Wasted Search Terms across all campaigns
print("\nTop 30 Wasted Search Terms (0 Conv) Across All Campaigns:")
for _, r in st_zero.sort_values('Cost', ascending=False).head(30).iterrows():
    term_str = str(r['Search term']).strip().lower()
    in_neg = " [ALREADY IN NEG]" if term_str in existing_negs else ""
    print(f"  [{r['Campaign']}] '{r['Search term']}' ({r['Match type']}) -> Spend: Rs.{r['Cost']:,.2f} | Clicks: {r['Clicks']} | CPC: Rs.{r['Avg. CPC']:.2f}{in_neg}")
