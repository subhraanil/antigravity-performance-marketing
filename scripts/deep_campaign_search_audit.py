import pandas as pd
import numpy as np

f_st = r'c:\Users\test\Videos\Office\data\IAOL\Search terms report - this month oct.xlsx'
df = pd.read_excel(f_st, skiprows=2)

num_cols = ['Cost', 'Clicks', 'Impr.', 'Avg. CPC', 'Conversions', 'Cost / conv.', 'Conv. rate']
for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)

df = df[df['Search term'].notnull() & (df['Search term'] != '--') & (~df['Search term'].astype(str).str.startswith('Total'))]

# Existing negatives
neg_file = r"c:\Users\test\Videos\Office\data\IAOL\Negative keyword details report.xlsx"
df_neg = pd.read_excel(neg_file, skiprows=2)
existing_negs = set(df_neg['keyword_text'].dropna().astype(str).str.strip().str.lower().tolist())

campaigns = df['Campaign'].unique()

print("=" * 80)
print("DEEP CAMPAIGN-BY-CAMPAIGN SEARCH TERMS & WASTE AUDIT (OCT 1 - OCT 15, 2026)")
print("=" * 80)

for camp in sorted(campaigns):
    cdf = df[df['Campaign'] == camp]
    tot_cost = cdf['Cost'].sum()
    tot_clicks = cdf['Clicks'].sum()
    tot_conv = cdf['Conversions'].sum()
    cpa = tot_cost / tot_conv if tot_conv > 0 else 0
    cvr = (tot_conv / tot_clicks * 100) if tot_clicks > 0 else 0
    cpc = tot_cost / tot_clicks if tot_clicks > 0 else 0
    
    zero_c = cdf[cdf['Conversions'] == 0]
    conv_c = cdf[cdf['Conversions'] > 0]
    
    print(f"\n>>> CAMPAIGN: {camp} <<<")
    print(f"Spend: Rs. {tot_cost:,.2f} | Clicks: {tot_clicks:.0f} | Leads: {tot_conv:.1f} | Avg CPC: Rs. {cpc:.2f} | CPA: Rs. {cpa:.2f} | CVR: {cvr:.2f}%")
    print(f"Zero-Conv Waste: Rs. {zero_c['Cost'].sum():,.2f} ({zero_c['Cost'].sum()/tot_cost*100:.1f}% of spend) across {len(zero_c)} terms")
    
    print("\n  Top Converting Search Terms:")
    for _, r in conv_c.sort_values('Conversions', ascending=False).head(8).iterrows():
        t_cpa = r['Cost'] / r['Conversions']
        print(f"    - '{r['Search term']}' ({r['Match type']}) -> Leads: {r['Conversions']:.1f} | Spend: Rs.{r['Cost']:.2f} | CPA: Rs.{t_cpa:.2f} | CPC: Rs.{r['Avg. CPC']:.2f}")
        
    print("\n  Top Zero-Conversion Bleeders (Spend >= Rs 150 & 0 Leads):")
    bleeders = zero_c[zero_c['Cost'] >= 150].sort_values('Cost', ascending=False)
    for _, r in bleeders.head(10).iterrows():
        in_neg = " [ALREADY IN NEG]" if str(r['Search term']).strip().lower() in existing_negs else ""
        print(f"    - '{r['Search term']}' ({r['Match type']}) -> Spend: Rs.{r['Cost']:.2f} | Clicks: {r['Clicks']:.0f} | CPC: Rs.{r['Avg. CPC']:.2f}{in_neg}")
