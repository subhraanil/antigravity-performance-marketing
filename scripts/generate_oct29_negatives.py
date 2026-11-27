import pandas as pd

f = r'c:\Users\test\Videos\Office\data\IAOL\Search terms report.xlsx'
df = pd.read_excel(f, skiprows=2)
df = df[df['Campaign'] != 'Remarketing-PMax']

if 'Interactions' in df.columns and 'Clicks' not in df.columns: df['Clicks'] = df['Interactions']
if 'Avg. cost' in df.columns and 'Avg. CPC' not in df.columns: df['Avg. CPC'] = df['Avg. cost']

num_cols = ['Cost', 'Clicks', 'Conversions', 'Avg. CPC']
for c in num_cols: df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)
df = df[df['Search term'].notnull() & (~df['Search term'].astype(str).str.startswith('Total'))]

neg_file = r"c:\Users\test\Videos\Office\data\IAOL\Negative keyword details report.xlsx"
df_neg = pd.read_excel(neg_file, skiprows=2)
existing_negs = set(df_neg['keyword_text'].dropna().astype(str).str.strip().str.lower().tolist())

# Zero conversion terms with spend >= 150
zeros = df[df['Conversions'] == 0]
zeros_150 = zeros[zeros['Cost'] >= 150].sort_values(['Campaign', 'Cost'], ascending=[True, False])

print("=== ZERO CONVERSION TERMS WITH SPEND >= Rs 150 (OCT 22 - OCT 28) ===")
for camp, grp in zeros_150.groupby('Campaign'):
    print(f"\n--- {camp} (Count: {len(grp)}, Total Waste: Rs.{grp['Cost'].sum():,.2f}) ---")
    for _, r in grp.iterrows():
        t = str(r['Search term']).strip().lower()
        in_neg = " [ALREADY IN NEG]" if t in existing_negs else ""
        print(f"  [{r['Match type']}] '{t}' -> Rs.{r['Cost']:.2f} | Clicks: {r['Clicks']} | CPC: Rs.{r['Avg. CPC']:.2f}{in_neg}")
