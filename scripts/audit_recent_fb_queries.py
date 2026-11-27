import pandas as pd

st_path = r'data/IAOL/October/FB/Search terms report.xlsx'
df = pd.read_excel(st_path, skiprows=2)
df.columns = [str(c).strip() for c in df.columns]

# Filter out totals
df_clean = df[~df['Search term'].str.contains('Total', case=False, na=False)].dropna(subset=['Search term'])

for c in ['Clicks', 'Impr.', 'Cost', 'Avg. CPC', 'Conversions']:
    df_clean[c] = pd.to_numeric(df_clean[c].astype(str).str.replace('₹', '').str.replace(',', '').str.strip(), errors='coerce').fillna(0)

print(f"Total Unique Search Queries: {len(df_clean)}")
print(f"Total Queries with >=1 click: {len(df_clean[df_clean['Clicks'] > 0])}")

print("\n--- ALL QUERIES WITH CLICKS (Oct 29 - Nov 5) ---")
clicked = df_clean[df_clean['Clicks'] > 0].sort_values(by='Cost', ascending=False)
for idx, r in clicked.iterrows():
    print(f"Query: '{r['Search term']}' | Added/Excl: {r.get('Added/Excluded')} | Match: {r['Match type']} | Clicks: {int(r['Clicks'])} | Impr: {int(r['Impr.'])} | CPC: Rs {r['Avg. CPC']:.2f} | Cost: Rs {r['Cost']:.2f}")

print("\n--- QUERIES WITH IMPRESSIONS BUT 0 CLICKS (Top 10 by Impressions) ---")
zero_clicks = df_clean[df_clean['Clicks'] == 0].sort_values(by='Impr.', ascending=False)
for idx, r in zero_clicks.head(15).iterrows():
    print(f"Query: '{r['Search term']}' | Added/Excl: {r.get('Added/Excluded')} | Match: {r['Match type']} | Impr: {int(r['Impr.'])}")
