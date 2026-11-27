import pandas as pd

f = r'c:\Users\test\Videos\Office\data\IAOL\Search terms report.xlsx'
df = pd.read_excel(f, skiprows=2)
df = df[df['Campaign'] == 'German-Hydrabad']

if 'Interactions' in df.columns and 'Clicks' not in df.columns: df['Clicks'] = df['Interactions']
if 'Avg. cost' in df.columns and 'Avg. CPC' not in df.columns: df['Avg. CPC'] = df['Avg. cost']

num_cols = ['Cost', 'Clicks', 'Conversions', 'Avg. CPC']
for c in num_cols: df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)
df = df[df['Search term'].notnull() & (~df['Search term'].astype(str).str.startswith('Total'))]

print("=== GERMAN HYDERABAD CONVERTING TERMS ===")
conv = df[df['Conversions'] > 0].sort_values('Conversions', ascending=False)
for _, r in conv.iterrows():
    print(f"  CONV: '{r['Search term']}' ({r['Match type']}) -> Leads: {r['Conversions']} | Spend: Rs.{r['Cost']:.2f} | CPA: Rs.{r['Cost']/r['Conversions']:.2f} | CPC: Rs.{r['Avg. CPC']:.2f}")

print("\n=== GERMAN HYDERABAD ZERO CONVERSION BLEEDERS ===")
waste = df[df['Conversions'] == 0].sort_values('Cost', ascending=False)
for _, r in waste.head(15).iterrows():
    print(f"  WASTE: '{r['Search term']}' ({r['Match type']}) -> Spend: Rs.{r['Cost']:.2f} | Clicks: {r['Clicks']} | CPC: Rs.{r['Avg. CPC']:.2f}")
