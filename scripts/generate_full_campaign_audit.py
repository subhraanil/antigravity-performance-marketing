import pandas as pd

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

# Load existing negatives
neg_file = r"c:\Users\test\Videos\Office\data\IAOL\Negative keyword details report.xlsx"
df_neg = pd.read_excel(neg_file, skiprows=2)
existing_negs = set(df_neg['keyword_text'].dropna().astype(str).str.strip().str.lower().tolist())

campaigns = sorted(df14['Campaign'].unique())

print("=" * 80)
print("CAMPAIGN-BY-CAMPAIGN DETAILED AUDIT: LAST 7 DAYS & LAST 14 DAYS")
print("=" * 80)

for camp in campaigns:
    c7 = df7[df7['Campaign'] == camp]
    c14 = df14[df14['Campaign'] == camp]
    
    spend7 = c7['Cost'].sum()
    conv7 = c7['Conversions'].sum()
    cpa7 = spend7 / conv7 if conv7 > 0 else 0
    cpc7 = spend7 / c7['Clicks'].sum() if c7['Clicks'].sum() > 0 else 0
    
    spend14 = c14['Cost'].sum()
    conv14 = c14['Conversions'].sum()
    cpa14 = spend14 / conv14 if conv14 > 0 else 0
    cpc14 = spend14 / c14['Clicks'].sum() if c14['Clicks'].sum() > 0 else 0
    
    print(f"\n{'*'*70}")
    print(f"CAMPAIGN: {camp}")
    print(f"  Last 7 Days:  Spend Rs.{spend7:,.2f} | Clicks: {c7['Clicks'].sum():.0f} | Leads: {conv7:.1f} | Avg CPC: Rs.{cpc7:.2f} | CPA: Rs.{cpa7:.2f}")
    print(f"  Last 14 Days: Spend Rs.{spend14:,.2f} | Clicks: {c14['Clicks'].sum():.0f} | Leads: {conv14:.1f} | Avg CPC: Rs.{cpc14:.2f} | CPA: Rs.{cpa14:.2f}")
    print(f"{'*'*70}")
    
    # Converting terms in 14d
    conv_terms14 = c14[c14['Conversions'] > 0].sort_values('Conversions', ascending=False)
    print("  Converting Search Terms (Last 14 Days):")
    if len(conv_terms14) == 0:
        print("    None")
    for _, r in conv_terms14.iterrows():
        cpa_term = r['Cost'] / r['Conversions']
        print(f"    - '{r['Search term']}' ({r['Match type']}) -> Leads: {r['Conversions']:.1f} | Cost: Rs.{r['Cost']:.2f} | CPA: Rs.{cpa_term:.2f} | CPC: Rs.{r['Avg. CPC']:.2f}")
        
    # Top Waste terms in 14d (Spend >= 200 and 0 conv)
    waste_terms14 = c14[c14['Conversions'] == 0].sort_values('Cost', ascending=False)
    print("\n  Top Zero-Conversion Waste Terms (Spend >= Rs 200, Last 14 Days):")
    high_waste = waste_terms14[waste_terms14['Cost'] >= 200]
    if len(high_waste) == 0:
        print("    None")
    for _, r in high_waste.head(12).iterrows():
        term_str = str(r['Search term']).strip().lower()
        in_neg = " [ALREADY IN NEG]" if term_str in existing_negs else ""
        print(f"    - '{r['Search term']}' ({r['Match type']}) -> Spend: Rs.{r['Cost']:.2f} | Clicks: {r['Clicks']:.0f} | CPC: Rs.{r['Avg. CPC']:.2f}{in_neg}")
