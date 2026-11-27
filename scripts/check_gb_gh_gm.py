import pandas as pd

f14 = r'c:\Users\test\Videos\Office\data\IAOL\Search terms report - last 14 days.xlsx'
df14 = pd.read_excel(f14, skiprows=2)
num_cols = ['Cost', 'Clicks', 'Conversions', 'Avg. CPC']
for c in num_cols: df14[c] = pd.to_numeric(df14[c].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)
df14 = df14[df14['Search term'].notnull() & (~df14['Search term'].astype(str).str.startswith('Total'))]

for camp in ['German-Bangalore', 'German-Hydrabad', 'German-Mumbai']:
    c14 = df14[df14['Campaign'] == camp]
    print(f"\n==================== {camp} (Last 14 Days) ====================")
    conv = c14[c14['Conversions'] > 0].sort_values('Conversions', ascending=False)
    print("Converting Search Terms:")
    for _, r in conv.head(8).iterrows():
        print(f"  - '{r['Search term']}' ({r['Match type']}) -> Leads: {r['Conversions']:.1f} | Cost: Rs.{r['Cost']:.2f} | CPA: Rs.{r['Cost']/r['Conversions']:.2f} | CPC: Rs.{r['Avg. CPC']:.2f}")
    waste = c14[c14['Conversions'] == 0].sort_values('Cost', ascending=False)
    print("Top Waste Search Terms:")
    for _, r in waste.head(10).iterrows():
        print(f"  - '{r['Search term']}' ({r['Match type']}) -> Spend: Rs.{r['Cost']:.2f} | Clicks: {r['Clicks']:.0f} | CPC: Rs.{r['Avg. CPC']:.2f}")
