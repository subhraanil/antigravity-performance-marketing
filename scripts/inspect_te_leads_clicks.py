import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

f_14d = r'.\data\IHLS\Search terms report.xlsx'
df = pd.read_excel(f_14d, skiprows=2)
df_clean = df[~df['Search term'].astype(str).str.startswith('Total:')].copy()
for col in ['Cost', 'Conversions', 'Clicks']:
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0)

te_leads = df_clean[df_clean['Campaign'] == 'TE Leads - 2026-03-04'].copy()
print(f"TE Leads Search Campaign:")
print(f"Total search terms: {len(te_leads)}")
print(f"Total spend: ${te_leads['Cost'].sum():.2f}")
print(f"Total conversions: {te_leads['Conversions'].sum()}")
print(f"Total clicks: {te_leads['Clicks'].sum()}")

print("\nBreakdown by Match Type in TE Leads:")
print(te_leads.groupby('Match type').agg({
    'Search term': 'count',
    'Cost': 'sum',
    'Clicks': 'sum',
    'Conversions': 'sum'
}))

print("\nAll clicks in TE Leads (sorted by cost):")
clicked_terms = te_leads[te_leads['Clicks'] > 0].sort_values(by='Cost', ascending=False)
print(clicked_terms[['Search term', 'Match type', 'Clicks', 'Cost', 'Conversions']].to_string())
