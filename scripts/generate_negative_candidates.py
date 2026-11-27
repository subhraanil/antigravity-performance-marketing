import pandas as pd

f7 = r'c:\Users\test\Videos\Office\data\IAOL\Search terms report - last 7 days.xlsx'
f14 = r'c:\Users\test\Videos\Office\data\IAOL\Search terms report - last 14 days.xlsx'

df7 = pd.read_excel(f7, skiprows=2)
df14 = pd.read_excel(f14, skiprows=2)

num_cols = ['Cost', 'Clicks', 'Conversions']
for df in [df7, df14]:
    for c in num_cols:
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)

# Combine reports for last 14 days (which includes last 7 days)
df14 = df14[df14['Search term'].notnull() & (~df14['Search term'].astype(str).str.startswith('Total'))]

neg_file = r"c:\Users\test\Videos\Office\data\IAOL\Negative keyword details report.xlsx"
df_neg = pd.read_excel(neg_file, skiprows=2)
existing_negs = set(df_neg['keyword_text'].dropna().astype(str).str.strip().str.lower().tolist())

# Zero conversion terms with spend
zeros = df14[df14['Conversions'] == 0]
zeros_agg = zeros.groupby(['Campaign', 'Search term', 'Match type']).agg({'Cost':'sum', 'Clicks':'sum'}).reset_index()
zeros_agg['CPC'] = zeros_agg['Cost'] / zeros_agg['Clicks']
zeros_agg = zeros_agg.sort_values('Cost', ascending=False)

print(f"Total zero conversion search term instances: {len(zeros_agg)}")
print(f"Total waste spend: Rs. {zeros_agg['Cost'].sum():,.2f}")

# Top waste terms overall
print("\nTop 30 Waste Terms Across All Campaigns (Last 14 Days):")
for _, r in zeros_agg.head(30).iterrows():
    term = str(r['Search term']).strip().lower()
    in_neg = " [ALREADY IN NEG]" if term in existing_negs else ""
    print(f"[{r['Campaign']}] '{r['Search term']}' ({r['Match type']}) -> Spend: Rs.{r['Cost']:.2f} | Clicks: {r['Clicks']:.0f} | CPC: Rs.{r['CPC']:.2f}{in_neg}")
