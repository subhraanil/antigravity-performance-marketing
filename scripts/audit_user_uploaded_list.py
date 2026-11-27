import pandas as pd
import numpy as np
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# File paths
f_all = r'.\data\IHLS\Search terms report - all time.xlsx'
f_user_txt = r'.\data\IHLS\user_uploaded_negatives.txt'

df_all = pd.read_excel(f_all, skiprows=2)
df_all = df_all[~df_all['Search term'].astype(str).str.startswith('Total:')].copy()

for col in ['Cost', 'Conversions', 'Clicks', 'Conv. rate', 'Cost / conv.']:
    df_all[col] = pd.to_numeric(df_all[col], errors='coerce').fillna(0)

# Converting queries
conv_df = df_all[df_all['Conversions'] > 0].groupby(df_all['Search term'].str.lower().str.strip()).agg({
    'Conversions': 'sum',
    'Cost': 'sum',
    'Clicks': 'sum'
}).reset_index().sort_values(by='Conversions', ascending=False)
conv_queries = dict(zip(conv_df['Search term'], conv_df['Conversions']))
print(f"Total converting queries: {len(conv_queries)}")

# Parse user uploaded negatives
with open(f_user_txt, 'r', encoding='utf-8') as f:
    lines = [l.strip() for l in f if l.strip()]

print(f"Total uploaded lines: {len(lines)}")

parsed_negatives = []
for l in lines:
    raw = l
    if raw.startswith('"') and raw.endswith('"'):
        clean = raw[1:-1].strip().lower()
        mt = 'PHRASE'
    elif raw.startswith('[') and raw.endswith(']'):
        clean = raw[1:-1].strip().lower()
        mt = 'EXACT'
    else:
        clean = raw.strip().lower()
        mt = 'BROAD'
    parsed_negatives.append((raw, clean, mt))

print(f"Parsed negatives count: {len(parsed_negatives)}")

# Check conflicts with converting queries
conflicts = []
for raw, clean, mt in parsed_negatives:
    for c_query, convs in conv_queries.items():
        conflict = False
        reason = ''
        if mt == 'EXACT':
            if clean == c_query:
                conflict = True
                reason = 'Exact match block'
        elif mt == 'PHRASE':
            if re.search(r'\b' + re.escape(clean) + r'\b', c_query):
                conflict = True
                reason = 'Phrase match block'
        elif mt == 'BROAD':
            tokens = clean.split()
            if all(re.search(r'\b' + re.escape(t) + r'\b', c_query) for t in tokens):
                conflict = True
                reason = 'Broad match block'
        
        if conflict:
            conflicts.append({
                'Uploaded Negative': raw,
                'Parsed Term': clean,
                'Match Type': mt,
                'Blocked Converting Query': c_query,
                'Lost Conversions': convs,
                'Reason': reason
            })

df_conflicts = pd.DataFrame(conflicts)
print(f"\nTOTAL CONFLICTS DETECTED: {len(df_conflicts)}")
if len(df_conflicts) > 0:
    print("\nSummary of Blocked Converting Queries:")
    print(df_conflicts[['Uploaded Negative', 'Match Type', 'Blocked Converting Query', 'Lost Conversions']].drop_duplicates().to_string())
    print(f"\nTotal potential conversions blocked by these conflicts: {df_conflicts['Lost Conversions'].sum():.2f}")

# Check dangerous broad match words in uploaded list
print("\nDangerous broad match single words in uploaded list:")
for raw, clean, mt in parsed_negatives:
    if mt == 'BROAD' and len(clean.split()) == 1:
        if clean in ['woman', 'women', 'men', 'man', 'hair', 'loss', 'clinic', 'perth', 'subiaco', 'reason', 'reasons', 'cause', 'causes', 'shampoo', 'shampoos', 'tablets', 'tablet', 'symptoms', 'signs', 'stress', 'used', 'ways', 'what', 'when', 'where', 'which', 'will', 'young', 'year', 'years', 'hormonal', 'information', 'iron', 'natural', 'price', 'pricing', 'procedure', 'product', 'products', 'program', 'programs', 'protein', 'protocol']:
            print(f"  BROAD MATCH RISK: '{clean}' will block any query containing the word '{clean}'!")
