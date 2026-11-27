import pandas as pd
import numpy as np
import re
from collections import Counter

f_all = r'.\data\IHLS\Search terms report - all time.xlsx'
f_oct = r'.\data\IHLS\Search terms report.xlsx'
f_details = r'.\data\IHLS\Negative keyword details report.xlsx'
f_rep = r'.\data\IHLS\Negative keyword report.xlsx'

df_all = pd.read_excel(f_all, skiprows=2)
df_all = df_all[~df_all['Search term'].astype(str).str.startswith('Total:')].copy()

df_oct = pd.read_excel(f_oct, skiprows=2)
df_oct = df_oct[~df_oct['Search term'].astype(str).str.startswith('Total:')].copy()

df_d = pd.read_excel(f_details, skiprows=2)
df_r = pd.read_excel(f_rep, skiprows=2)

for col in ['Cost', 'Conversions', 'Clicks']:
    df_all[col] = pd.to_numeric(df_all[col], errors='coerce').fillna(0)
    df_oct[col] = pd.to_numeric(df_oct[col], errors='coerce').fillna(0)

def clean_kw(kw):
    if pd.isna(kw): return ''
    kw = str(kw).strip().lower()
    if kw.startswith('"') and kw.endswith('"'): kw = kw[1:-1]
    if kw.startswith('[') and kw.endswith(']'): kw = kw[1:-1]
    return kw.strip()

# Existing negatives
details_neg = set(df_d['keyword_text'].apply(clean_kw))
report_neg = set(df_r['Negative keyword'].apply(clean_kw))
all_existing_neg = details_neg.union(report_neg)
all_existing_neg.discard('')

# What campaigns are in All Time and Oct?
print("All Time Spend by Campaign:")
camp_spend = df_all.groupby('Campaign').agg({'Cost': 'sum', 'Conversions': 'sum', 'Clicks': 'sum'}).sort_values(by='Cost', ascending=False)
print(camp_spend)

print("\nOctober 2026 Spend by Campaign:")
oct_camp_spend = df_oct.groupby('Campaign').agg({'Cost': 'sum', 'Conversions': 'sum', 'Clicks': 'sum'}).sort_values(by='Cost', ascending=False)
print(oct_camp_spend)

# Check all non-converting terms in Oct 2026
oct_non_conv = df_oct[df_oct['Conversions'] == 0].groupby(df_oct['Search term'].str.lower().str.strip()).agg({
    'Cost': 'sum',
    'Clicks': 'sum',
    'Campaign': lambda x: ', '.join(set(x))
}).reset_index().sort_values(by='Cost', ascending=False)

print("\nTop 30 non-converting search terms in October 2026:")
print(oct_non_conv.head(30).to_string())

# Check how many October search terms match existing negatives
matches_existing = []
for st in oct_non_conv['Search term']:
    words = st.split()
    matched = False
    for neg in all_existing_neg:
        if neg in st:
            matches_existing.append((st, neg))
            matched = True
            break

print(f"\nOut of {len(oct_non_conv)} non-converting October terms, {len(matches_existing)} contained an existing negative keyword!")
print("Sample matched terms that still showed in October:")
for item in matches_existing[:15]:
    print(f"  Search term: '{item[0]}' matched existing negative: '{item[1]}'")
