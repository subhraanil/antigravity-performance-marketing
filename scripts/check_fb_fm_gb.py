import pandas as pd

f_st = r'c:\Users\test\Videos\Office\data\IAOL\Search terms report - this month oct.xlsx'
df = pd.read_excel(f_st, skiprows=2)
num_cols = ['Cost', 'Clicks', 'Conversions', 'Avg. CPC']
for c in num_cols:
    df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)
df = df[df['Search term'].notnull() & (~df['Search term'].astype(str).str.startswith('Total'))]

for camp in ['French-Bangalore', 'French-Mumbai', 'German-Bangalore']:
    cdf = df[df['Campaign'] == camp]
    print(f"\n=== {camp} ===")
    conv = cdf[cdf['Conversions'] > 0].sort_values('Conversions', ascending=False)
    print("Converting Search Terms:")
    for _, r in conv.head(8).iterrows():
        print(f"  CONV: '{r['Search term']}' ({r['Match type']}) -> Leads: {r['Conversions']} | Cost: Rs.{r['Cost']:.2f} | CPA: Rs.{r['Cost']/r['Conversions']:.2f} | CPC: Rs.{r['Avg. CPC']:.2f}")
    zeros = cdf[cdf['Conversions'] == 0].sort_values('Cost', ascending=False)
    print("Top Wasted Search Terms:")
    for _, r in zeros.head(10).iterrows():
        print(f"  WASTE: '{r['Search term']}' ({r['Match type']}) -> Cost: Rs.{r['Cost']:.2f} | Clicks: {r['Clicks']:.0f} | CPC: Rs.{r['Avg. CPC']:.2f}")
