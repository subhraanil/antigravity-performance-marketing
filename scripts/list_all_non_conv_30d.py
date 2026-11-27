import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

f_30d = r'.\data\IHLS\Search terms report.xlsx'
df = pd.read_excel(f_30d, skiprows=2)
df_clean = df[~df['Search term'].astype(str).str.startswith('Total:')].copy()
for col in ['Cost', 'Conversions', 'Clicks']:
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0)

# Non-converting terms with cost > 0
non_conv = df_clean[(df_clean['Conversions'] == 0) & (df_clean['Cost'] > 0)].sort_values(by='Cost', ascending=False)
print(f"Total non-converting search terms with spend: {len(non_conv)}")
print(f"Total spend: ${non_conv['Cost'].sum():.2f}")
print(f"Total clicks: {non_conv['Clicks'].sum()}")

# Print all 116 terms
for idx, r in non_conv.iterrows():
    print(f"${r['Cost']:6.2f} | Clicks: {int(r['Clicks'])} | {r['Campaign']:22} | {r['Match type']:28} | {r['Search term']}")
