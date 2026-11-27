import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

f_14d = r'.\data\IHLS\Search terms report.xlsx'
df = pd.read_excel(f_14d, skiprows=2)
print("Raw rows:", len(df))
print("Columns:", df.columns.tolist())

# Filter out summary rows at the bottom
df_clean = df[~df['Search term'].astype(str).str.startswith('Total:')].copy()
print("Clean search terms count:", len(df_clean))

for col in ['Cost', 'Conversions', 'Clicks', 'Conv. rate', 'Cost / conv.']:
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0)

print(f"\n=== LAST 14 DAYS OVERVIEW (Oct 14 - Oct 27, 2026) ===")
print(f"Total Spend: ${df_clean['Cost'].sum():.2f}")
print(f"Total Conversions: {df_clean['Conversions'].sum():.2f}")
if df_clean['Conversions'].sum() > 0:
    print(f"Blended CPA: ${df_clean['Cost'].sum() / df_clean['Conversions'].sum():.2f}")
print(f"Total Clicks: {df_clean['Clicks'].sum()}")

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

# Converting search terms in last 14 days
conv_terms = df_clean[df_clean['Conversions'] > 0].sort_values(by='Conversions', ascending=False)
print(f"\nConverting Search Terms ({len(conv_terms)} unique):")
print(conv_terms[['Search term', 'Campaign', 'Match type', 'Clicks', 'Cost', 'Conversions', 'Cost / conv.']].to_string())

# Non-converting search terms with spend > 0
non_conv = df_clean[df_clean['Conversions'] == 0].sort_values(by='Cost', ascending=False)
print(f"\nNon-converting Search Terms with Spend ({len(non_conv[non_conv['Cost'] > 0])} terms):")
print(f"Total spend on zero-conv terms: ${non_conv['Cost'].sum():.2f} ({(non_conv['Cost'].sum() / df_clean['Cost'].sum())*100:.1f}% of total spend)")

print("\nTop 25 Highest Spend Zero-Conversion Search Terms (Last 14 Days):")
print(non_conv.head(25)[['Search term', 'Campaign', 'Match type', 'Clicks', 'Cost']].to_string())
