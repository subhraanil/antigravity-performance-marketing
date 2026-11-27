import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

f_7d = r'.\data\IHLS\Search terms report.xlsx'
df = pd.read_excel(f_7d, skiprows=2)
print("Raw rows:", len(df))
print("Columns:", df.columns.tolist())

# Filter out summary rows
df_clean = df[~df['Search term'].astype(str).str.startswith('Total:')].copy()
print("Clean search terms count:", len(df_clean))

for col in ['Cost', 'Conversions', 'Clicks', 'Conv. rate', 'Cost / conv.']:
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0)

print(f"\n=== LAST 7 DAYS OVERVIEW (Oct 26 - Nov 1, 2026) ===")
total_spend = df_clean['Cost'].sum()
total_conv = df_clean['Conversions'].sum()
total_clicks = df_clean['Clicks'].sum()
print(f"Total Spend: ${total_spend:.2f}")
print(f"Total Conversions: {total_conv:.2f}")
if total_conv > 0:
    print(f"Blended CPA: ${total_spend / total_conv:.2f}")
print(f"Total Clicks: {total_clicks}")

print("\nCampaign Breakdown:")
camp_perf = df_clean.groupby('Campaign').agg({
    'Cost': 'sum',
    'Conversions': 'sum',
    'Clicks': 'sum'
}).assign(
    CPA=lambda x: np.where(x['Conversions']>0, x['Cost']/x['Conversions'], np.nan)
).sort_values(by='Cost', ascending=False)
print(camp_perf.to_string())

print("\nCampaign Type Breakdown:")
camp_type_perf = df_clean.groupby('Campaign type').agg({
    'Cost': 'sum',
    'Conversions': 'sum',
    'Clicks': 'sum'
}).assign(
    CPA=lambda x: np.where(x['Conversions']>0, x['Cost']/x['Conversions'], np.nan)
).sort_values(by='Cost', ascending=False)
print(camp_type_perf.to_string())

print("\nMatch Type Breakdown:")
match_perf = df_clean.groupby('Match type').agg({
    'Cost': 'sum',
    'Conversions': 'sum',
    'Clicks': 'sum'
}).assign(
    CPA=lambda x: np.where(x['Conversions']>0, x['Cost']/x['Conversions'], np.nan)
).sort_values(by='Cost', ascending=False)
print(match_perf.to_string())

# Converting search terms in last 7 days
conv_terms = df_clean[df_clean['Conversions'] > 0].sort_values(by='Conversions', ascending=False)
print(f"\nConverting Search Terms ({len(conv_terms)} unique):")
print(conv_terms[['Search term', 'Campaign', 'Match type', 'Clicks', 'Cost', 'Conversions', 'Cost / conv.']].to_string())

# Non-converting search terms with spend > 0
non_conv = df_clean[df_clean['Conversions'] == 0].sort_values(by='Cost', ascending=False)
print(f"\nNon-converting Search Terms with Spend ({len(non_conv[non_conv['Cost'] > 0])} terms):")
print(f"Total spend on zero-conv terms: ${non_conv['Cost'].sum():.2f} ({(non_conv['Cost'].sum() / total_spend)*100:.1f}% of total spend)")

print("\nTop 30 Highest Spend Zero-Conversion Search Terms (Last 7 Days):")
print(non_conv.head(30)[['Search term', 'Campaign', 'Match type', 'Clicks', 'Cost']].to_string())
