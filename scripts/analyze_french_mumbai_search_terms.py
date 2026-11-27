import pandas as pd

excel_file = r"c:\Users\test\Videos\Office\data\IAOL\Search terms report - FM.xlsx"
df = pd.read_excel(excel_file, skiprows=2)
print("Columns:", df.columns.tolist())
print("Head:")
print(df.head(5))

# Clean numeric columns
num_cols = ['Cost', 'Impr.', 'Interactions', 'Avg. cost', 'Conv. rate', 'Avg. CPC', 'Clicks', 'Conv. value', 'Conversions', 'Cost / conv.']
for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)

# Drop summary or empty rows
df = df[df['Search term'].notnull() & (df['Search term'] != '--') & (~df['Search term'].astype(str).str.startswith('Total'))]

print("\n--- OVERALL METRICS IN REPORT ---")
tot_cost = df['Cost'].sum()
tot_clicks = df['Clicks'].sum()
tot_conv = df['Conversions'].sum()
avg_cpc = tot_cost / tot_clicks if tot_clicks > 0 else 0
cpa = tot_cost / tot_conv if tot_conv > 0 else 0
cvr = (tot_conv / tot_clicks * 100) if tot_clicks > 0 else 0

print(f"Total Cost: Rs. {tot_cost:,.2f}")
print(f"Total Clicks: {tot_clicks}")
print(f"Total Conversions: {tot_conv}")
print(f"Avg CPC: Rs. {avg_cpc:.2f}")
print(f"CPA: Rs. {cpa:.2f}")
print(f"CVR: {cvr:.2f}%")

# Conversions breakdown
conv_terms = df[df['Conversions'] > 0].sort_values('Conversions', ascending=False)
print("\n--- CONVERTING SEARCH TERMS ---")
print(f"Count of converting search terms: {len(conv_terms)} | Total Conversions: {conv_terms['Conversions'].sum()} | Cost: Rs. {conv_terms['Cost'].sum():,.2f}")
for _, r in conv_terms.iterrows():
    cpa_t = r['Cost'] / r['Conversions']
    print(f"Search Term: '{r['Search term']}' | Match: {r.get('Match type', '')} | Added/Excluded: {r.get('Added/Excluded', '')} | Cost: Rs. {r['Cost']:.2f} | Clicks: {r['Clicks']} | Conv: {r['Conversions']} | CPA: Rs. {cpa_t:.2f}")

# Zero conversion breakdown
zero_conv = df[df['Conversions'] == 0].sort_values('Cost', ascending=False)
print("\n--- TOP WASTED SEARCH TERMS (0 Conversions) ---")
print(f"Count of 0-conv terms: {len(zero_conv)} | Total Wasted Cost: Rs. {zero_conv['Cost'].sum():,.2f} ({zero_conv['Cost'].sum()/tot_cost*100:.1f}%)")
print("Top 30 Wasted Terms by Cost:")
for _, r in zero_conv.head(30).iterrows():
    print(f"'{r['Search term']}' | Added/Excluded: {r.get('Added/Excluded', '')} | Match: {r.get('Match type', '')} | Cost: Rs. {r['Cost']:.2f} | Clicks: {r['Clicks']} | CPC: Rs. {r['Avg. CPC']:.2f}")
