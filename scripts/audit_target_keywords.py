import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load target keywords report
f_kw = r'.\data\IHLS\Search keyword report.xlsx'
df_kw = pd.read_excel(f_kw, skiprows=2)
df_kw_enabled = df_kw[df_kw['Keyword status'] == 'Enabled'].copy()

for col in ['Cost', 'Conversions', 'Clicks', 'Impr.', 'Cost / conv.', 'Avg. CPC']:
    df_kw_enabled[col] = pd.to_numeric(df_kw_enabled[col], errors='coerce').fillna(0)

# Load converting search terms
f_all = r'.\data\IHLS\Search terms report - all time.xlsx'
df_all = pd.read_excel(f_all, skiprows=2)
df_all = df_all[~df_all['Search term'].astype(str).str.startswith('Total:')].copy()
for col in ['Cost', 'Conversions', 'Clicks']:
    df_all[col] = pd.to_numeric(df_all[col], errors='coerce').fillna(0)

conv_st = df_all[df_all['Conversions'] > 0].groupby(df_all['Search term'].str.lower().str.strip()).agg({
    'Conversions': 'sum',
    'Cost': 'sum',
    'Clicks': 'sum'
}).reset_index().sort_values(by='Conversions', ascending=False)

print("=== TARGET KEYWORDS PERFORMANCE SUMMARY ===")
print(f"Total enabled target keywords: {len(df_kw_enabled)}")
print(f"Total Cost: ${df_kw_enabled['Cost'].sum():.2f}")
print(f"Total Conversions: {df_kw_enabled['Conversions'].sum():.2f}")
print(f"Blended CPA: ${df_kw_enabled['Cost'].sum() / df_kw_enabled['Conversions'].sum():.2f}")

# Broad vs Phrase breakdown
print("\nBy Match Type:")
print(df_kw_enabled.groupby('Match type').agg({
    'Keyword': 'count',
    'Cost': 'sum',
    'Conversions': 'sum',
    'Clicks': 'sum'
}).assign(
    CPA=lambda x: np.where(x['Conversions']>0, x['Cost']/x['Conversions'], np.nan)
))

# Exosome keywords performance
exosome_kws = df_kw_enabled[df_kw_enabled['Keyword'].str.lower().str.contains('exosome')]
print("\nExosome keywords (TGA Compliance Hazard):")
print(exosome_kws[['Keyword', 'Match type', 'Cost', 'Conversions', 'Clicks']])
print(f"Total Exosome Spend: ${exosome_kws['Cost'].sum():.2f} on {exosome_kws['Conversions'].sum()} conversions")

# Zero conversion keywords with spend > $50
high_waste_kws = df_kw_enabled[(df_kw_enabled['Conversions'] == 0) & (df_kw_enabled['Cost'] >= 50)].sort_values(by='Cost', ascending=False)
print("\nHigh Waste Keywords (0 conversions, spend >= $50):")
print(high_waste_kws[['Keyword', 'Match type', 'Cost', 'Clicks', 'Avg. CPC']])
print(f"Total spend on zero-conv >= $50 keywords: ${high_waste_kws['Cost'].sum():.2f}")

# Top 15 converting search terms vs Target Keywords
top15_conv = conv_st.head(15).copy()
top15_conv['CPA'] = top15_conv['Cost'] / top15_conv['Conversions']

# Check if each top converting term is explicitly targeted as Exact or Phrase
target_clean = [k.replace('"', '').replace('[', '').replace(']', '').lower().strip() for k in df_kw_enabled['Keyword']]
top15_conv['In Target List'] = top15_conv['Search term'].apply(lambda x: x in target_clean)

print("\nTop 15 Converting Search Terms vs Current Target Keywords:")
print(top15_conv[['Search term', 'Conversions', 'Cost', 'CPA', 'In Target List']].to_string())
