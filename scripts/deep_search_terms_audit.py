import pandas as pd
import numpy as np
import re
from collections import Counter

f_all = r'.\data\IHLS\Search terms report - all time.xlsx'
f_oct = r'.\data\IHLS\Search terms report.xlsx'
f_details = r'.\data\IHLS\Negative keyword details report.xlsx'
f_rep = r'.\data\IHLS\Negative keyword report.xlsx'

# Load search terms
df_all = pd.read_excel(f_all, skiprows=2)
df_all = df_all[~df_all['Search term'].astype(str).str.startswith('Total:')].copy()

df_oct = pd.read_excel(f_oct, skiprows=2)
df_oct = df_oct[~df_oct['Search term'].astype(str).str.startswith('Total:')].copy()

# Load existing negatives
df_d = pd.read_excel(f_details, skiprows=2)
df_r = pd.read_excel(f_rep, skiprows=2)

def clean_kw(kw):
    if pd.isna(kw): return ''
    kw = str(kw).strip()
    if kw.startswith('"') and kw.endswith('"'): kw = kw[1:-1]
    if kw.startswith('[') and kw.endswith(']'): kw = kw[1:-1]
    return kw.lower().strip()

existing_negatives = set(df_d['keyword_text'].apply(clean_kw)).union(set(df_r['Negative keyword'].apply(clean_kw)))
existing_negatives.discard('')

print(f"Total search terms all time: {len(df_all)}")
print(f"Total search terms Oct 2026: {len(df_oct)}")
print(f"Total existing negatives: {len(existing_negatives)}")

# Ensure numeric columns
for col in ['Cost', 'Conversions', 'Clicks', 'Conv. rate', 'Cost / conv.']:
    df_all[col] = pd.to_numeric(df_all[col], errors='coerce').fillna(0)
    df_oct[col] = pd.to_numeric(df_oct[col], errors='coerce').fillna(0)

# Analyzing Converting Queries (Alpha list)
conv_all = df_all[df_all['Conversions'] > 0].copy()
conv_terms_set = set(conv_all['Search term'].str.lower().str.strip())
print(f"\nUnique converting terms all time: {len(conv_terms_set)}")
print(f"Total conversions all time: {conv_all['Conversions'].sum():.2f}")
print(f"Total cost on converting terms: ${conv_all['Cost'].sum():.2f}")
print(f"Average CPA on converting terms: ${conv_all['Cost'].sum() / conv_all['Conversions'].sum():.2f}")

print("\nTop 15 Converting Search Terms:")
print(conv_all.groupby('Search term')[['Conversions', 'Cost', 'Clicks']].sum().sort_values(by='Conversions', ascending=False).head(15))

# Analyzing Non-Converting Queries
non_conv_all = df_all[df_all['Conversions'] == 0].copy()
print(f"\nNon-converting terms count: {len(non_conv_all)}")
print(f"Total wasted cost on non-converting terms: ${non_conv_all['Cost'].sum():.2f}")

# Group by search term across all campaigns
st_summary = df_all.groupby(df_all['Search term'].str.lower().str.strip()).agg({
    'Cost': 'sum',
    'Conversions': 'sum',
    'Clicks': 'sum',
}).reset_index()

st_summary['CPA'] = np.where(st_summary['Conversions'] > 0, st_summary['Cost'] / st_summary['Conversions'], np.nan)

# Top wasted spend terms (Cost > $20 and Conversions == 0)
high_waste = st_summary[(st_summary['Conversions'] == 0) & (st_summary['Cost'] >= 20)].sort_values(by='Cost', ascending=False)
print(f"\nNumber of zero-conversion terms with Cost >= $20: {len(high_waste)}")
print(f"Total spend on these high-waste terms: ${high_waste['Cost'].sum():.2f}")
print("\nTop 25 highest spend zero-conversion terms:")
print(high_waste.head(25).to_string())

# October 2026 performance
st_oct_summary = df_oct.groupby(df_oct['Search term'].str.lower().str.strip()).agg({
    'Cost': 'sum',
    'Conversions': 'sum',
    'Clicks': 'sum',
}).reset_index()

oct_waste = st_oct_summary[(st_oct_summary['Conversions'] == 0) & (st_oct_summary['Cost'] > 0)].sort_values(by='Cost', ascending=False)
print(f"\nOctober 2026 non-converting terms with cost: {len(oct_waste)}, spend: ${oct_waste['Cost'].sum():.2f}")
print("\nTop 15 wasted terms in October 2026:")
print(oct_waste.head(15).to_string())
