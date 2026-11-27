import pandas as pd
import numpy as np
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# File paths
f_all = r'.\data\IHLS\Search terms report - all time.xlsx'
f_oct = r'.\data\IHLS\Search terms report.xlsx'
f_details = r'.\data\IHLS\Negative keyword details report.xlsx'
f_rep = r'.\data\IHLS\Negative keyword report.xlsx'

# Load data
df_all = pd.read_excel(f_all, skiprows=2)
df_all = df_all[~df_all['Search term'].astype(str).str.startswith('Total:')].copy()

df_oct = pd.read_excel(f_oct, skiprows=2)
df_oct = df_oct[~df_oct['Search term'].astype(str).str.startswith('Total:')].copy()

df_d = pd.read_excel(f_details, skiprows=2)
df_r = pd.read_excel(f_rep, skiprows=2)

for col in ['Cost', 'Conversions', 'Clicks', 'Conv. rate', 'Cost / conv.']:
    df_all[col] = pd.to_numeric(df_all[col], errors='coerce').fillna(0)
    df_oct[col] = pd.to_numeric(df_oct[col], errors='coerce').fillna(0)

# Converting queries
conv_df = df_all[df_all['Conversions'] > 0].groupby(df_all['Search term'].str.lower().str.strip()).agg({
    'Conversions': 'sum',
    'Cost': 'sum',
    'Clicks': 'sum'
}).reset_index().sort_values(by='Conversions', ascending=False)

converting_queries = set(conv_df['Search term'])
print(f"Total converting queries: {len(converting_queries)}")

# Helper to clean keyword strings
def clean_kw(kw):
    if pd.isna(kw): return ''
    kw = str(kw).strip().lower()
    if kw.startswith('"') and kw.endswith('"'): kw = kw[1:-1]
    if kw.startswith('[') and kw.endswith(']'): kw = kw[1:-1]
    return kw.strip()

# Harmful negatives that should NEVER be negative in this account
PROTECTED_TOKENS = {
    'ihls', 'subiaco', 'perth', 'clinic', 'clinics', 'treatment', 'treatments',
    'specialist', 'specialists', 'loss', 'hair', 'growth', 'regrowth', 'hairloss',
    'doctor', 'doctors', 'dermatologist', 'dermatologists', 'trichologist', 'trichologists',
    'restoration', 'transplant', 'transplants', 'system', 'systems', 'consultation', 'analysis'
}

# Stopwords/harmful single words that break query matching if used as broad/phrase
DANGEROUS_STOPWORDS = {
    'is', 'am', 'do', 'can', 'how', 'who', 'why', 'the', 'e', 'new', 'tip', 'way', 'kit', 'map', 'gas'
}

# Clean existing negatives
df_d['clean'] = df_d['keyword_text'].apply(clean_kw)
df_r['clean'] = df_r['Negative keyword'].apply(clean_kw)

# Collect existing negatives
existing_list_d = []
for _, row in df_d.iterrows():
    kw = row['clean']
    mt = str(row['match_type']).strip().upper()
    if kw and kw not in DANGEROUS_STOPWORDS and kw not in PROTECTED_TOKENS:
        existing_list_d.append((kw, mt))

existing_list_r = []
for _, row in df_r.iterrows():
    kw = row['clean']
    mt = str(row['Match type']).strip()
    if 'Phrase' in mt:
        mt_clean = 'PHRASE'
    elif 'Exact' in mt:
        mt_clean = 'EXACT'
    elif 'Broad' in mt:
        mt_clean = 'BROAD'
    else:
        mt_clean = 'PHRASE'
    if kw and kw not in DANGEROUS_STOPWORDS and kw not in PROTECTED_TOKENS:
        existing_list_r.append((kw, mt_clean))

print(f"Valid existing from details list: {len(existing_list_d)}")
print(f"Valid existing from report list: {len(existing_list_r)}")

# Aggregate all search terms all time
st_agg = df_all.groupby(df_all['Search term'].str.lower().str.strip()).agg({
    'Cost': 'sum',
    'Conversions': 'sum',
    'Clicks': 'sum'
}).reset_index()

st_agg_zero = st_agg[st_agg['Conversions'] == 0].sort_values(by='Cost', ascending=False)
print(f"Zero conversion queries count: {len(st_agg_zero)}, Total Spend: ${st_agg_zero['Cost'].sum():.2f}")

# October zero conversion queries
oct_agg = df_oct.groupby(df_oct['Search term'].str.lower().str.strip()).agg({
    'Cost': 'sum',
    'Conversions': 'sum',
    'Clicks': 'sum'
}).reset_index()
oct_agg_zero = oct_agg[oct_agg['Conversions'] == 0].sort_values(by='Cost', ascending=False)
print(f"October zero conversion queries count: {len(oct_agg_zero)}, Total Spend: ${oct_agg_zero['Cost'].sum():.2f}")
