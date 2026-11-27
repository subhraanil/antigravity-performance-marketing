import pandas as pd

f = r'c:\Users\test\Videos\Office\data\IAOL\Search terms report.xlsx'
df = pd.read_excel(f, skiprows=2)

# Exclude PMax
df = df[df['Campaign'] != 'Remarketing-PMax']

if 'Interactions' in df.columns and 'Clicks' not in df.columns:
    df['Clicks'] = df['Interactions']
if 'Avg. cost' in df.columns and 'Avg. CPC' not in df.columns:
    df['Avg. CPC'] = df['Avg. cost']

num_cols = ['Cost', 'Clicks', 'Impr.', 'Avg. CPC', 'Conversions', 'Cost / conv.', 'Conv. rate']
for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)

df = df[df['Search term'].notnull() & (df['Search term'] != '--') & (~df['Search term'].astype(str).str.startswith('Total'))]

# Load existing negatives
neg_file = r"c:\Users\test\Videos\Office\data\IAOL\Negative keyword details report.xlsx"
df_neg = pd.read_excel(neg_file, skiprows=2)
existing_negs = set(df_neg['keyword_text'].dropna().astype(str).str.strip().str.lower().tolist())

campaigns = sorted(df['Campaign'].unique())

print("=" * 85)
print("CAMPAIGN-BY-CAMPAIGN QUERY AUDIT: OCTOBER 22 - OCTOBER 28, 2026")
print("=" * 85)

for camp in campaigns:
    cdf = df[df['Campaign'] == camp]
    tot_cost = cdf['Cost'].sum()
    tot_clicks = cdf['Clicks'].sum()
    tot_conv = cdf['Conversions'].sum()
    cpa = tot_cost / tot_conv if tot_conv > 0 else 0
    cvr = (tot_conv / tot_clicks * 100) if tot_clicks > 0 else 0
    cpc = tot_cost / tot_clicks if tot_clicks > 0 else 0
    
    conv_c = cdf[cdf['Conversions'] > 0].sort_values('Conversions', ascending=False)
    zero_c = cdf[cdf['Conversions'] == 0].sort_values('Cost', ascending=False)
    
    print(f"\n{'*'*75}")
    print(f"CAMPAIGN: {camp}")
    print(f"Spend: Rs.{tot_cost:,.2f} | Clicks: {tot_clicks:.0f} | Leads: {tot_conv:.2f} | Avg CPC: Rs.{cpc:.2f} | CPA: Rs.{cpa:.2f} | CVR: {cvr:.2f}%")
    print(f"Zero-Conv Waste: Rs.{zero_c['Cost'].sum():,.2f} ({zero_c['Cost'].sum()/tot_cost*100:.1f}%) across {len(zero_c)} terms")
    print(f"{'*'*75}")
    
    print("  Converting Search Terms:")
    if len(conv_c) == 0:
        print("    None")
    for _, r in conv_c.iterrows():
        t_cpa = r['Cost'] / r['Conversions']
        print(f"    - '{r['Search term']}' ({r['Match type']}) -> Leads: {r['Conversions']:.2f} | Spend: Rs.{r['Cost']:.2f} | CPA: Rs.{t_cpa:.2f} | CPC: Rs.{r['Avg. CPC']:.2f}")
        
    print("\n  Top Zero-Conversion Bleeders (Spend >= Rs 150):")
    high_waste = zero_c[zero_c['Cost'] >= 150]
    if len(high_waste) == 0:
        print("    None")
    for _, r in high_waste.head(10).iterrows():
        term_str = str(r['Search term']).strip().lower()
        in_neg = " [ALREADY IN NEG]" if term_str in existing_negs else ""
        print(f"    - '{r['Search term']}' ({r['Match type']}) -> Spend: Rs.{r['Cost']:.2f} | Clicks: {r['Clicks']:.0f} | CPC: Rs.{r['Avg. CPC']:.2f}{in_neg}")
