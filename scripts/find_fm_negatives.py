import pandas as pd

excel_file = r"c:\Users\test\Videos\Office\data\IAOL\Search terms report - FM.xlsx"
df = pd.read_excel(excel_file, skiprows=2)

num_cols = ['Cost', 'Impr.', 'Interactions', 'Avg. cost', 'Conv. rate', 'Avg. CPC', 'Clicks', 'Conv. value', 'Conversions', 'Cost / conv.']
for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)

df = df[df['Search term'].notnull() & (df['Search term'] != '--') & (~df['Search term'].astype(str).str.startswith('Total'))]

neg_file = r"c:\Users\test\Videos\Office\data\IAOL\Negative keyword details report.xlsx"
df_neg = pd.read_excel(neg_file, skiprows=2)
existing_negs = set(df_neg['keyword_text'].dropna().astype(str).str.strip().str.lower().tolist())

print(f"Existing negatives loaded: {len(existing_negs)}")

zeros = df[df['Conversions'] == 0].sort_values('Cost', ascending=False)
zero_spend = zeros[zeros['Cost'] > 0]
print(f"Non-converting queries with spend: {len(zero_spend)} | Total Waste: Rs. {zero_spend['Cost'].sum():,.2f}")

print("\n--- ALL ZERO-CONVERTING SEARCH TERMS WITH SPEND ---")
for _, r in zero_spend.iterrows():
    term = str(r['Search term']).strip().lower()
    in_neg = " [ALREADY IN NEG]" if term in existing_negs else ""
    print(f"Rs. {r['Cost']:>7.2f} | Clicks: {r['Clicks']:>2.0f} | CPC: Rs. {r['Avg. CPC']:>6.2f} | {term}{in_neg}")
