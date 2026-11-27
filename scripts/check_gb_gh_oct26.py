import pandas as pd

f = r'c:\Users\test\Videos\Office\data\IAOL\Search terms report.xlsx'
df = pd.read_excel(f, skiprows=2)
num_cols = ['Cost', 'Clicks', 'Conversions', 'Avg. CPC']
for c in num_cols: df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)
df = df[df['Search term'].notnull() & (~df['Search term'].astype(str).str.startswith('Total'))]

for camp in ['German-Bangalore', 'German-Hydrabad']:
    c = df[df['Campaign'] == camp]
    print(f"\n==================== {camp} ====================")
    conv = c[c['Conversions'] > 0].sort_values('Conversions', ascending=False)
    print("Converting Search Terms:")
    for _, r in conv.iterrows():
        print(f"  - '{r['Search term']}' ({r['Match type']}) -> Leads: {r['Conversions']} | Spend: Rs.{r['Cost']:.2f} | CPA: Rs.{r['Cost']/r['Conversions']:.2f}")
    waste = c[c['Conversions'] == 0].sort_values('Cost', ascending=False)
    print("\nTop Waste Search Terms:")
    for _, r in waste.head(10).iterrows():
        print(f"  - '{r['Search term']}' ({r['Match type']}) -> Spend: Rs.{r['Cost']:.2f} | Clicks: {r['Clicks']} | CPC: Rs.{r['Avg. CPC']:.2f}")
