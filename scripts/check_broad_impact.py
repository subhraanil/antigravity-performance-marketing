import pandas as pd
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

f_all = r'.\data\IHLS\Search terms report - all time.xlsx'
df = pd.read_excel(f_all, skiprows=2)
df = df[~df['Search term'].astype(str).str.startswith('Total:')].copy()
for col in ['Cost', 'Conversions', 'Clicks']:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

words_to_check = ['price', 'pricing', 'reason', 'cause', 'shampoos', 'tablets', 'where', 'young', 'natural', 'woman', 'iron']
for w in words_to_check:
    matches = df[df['Search term'].astype(str).str.lower().str.contains(r'\b' + re.escape(w), regex=True, na=False)]
    tot_cost = matches['Cost'].sum()
    tot_conv = matches['Conversions'].sum()
    print(f"Word '{w}': {len(matches)} queries, Cost: ${tot_cost:.2f}, Conv: {tot_conv:.2f}")
    if tot_conv > 0:
        print("  Converting examples:")
        print(matches[matches['Conversions'] > 0][['Search term', 'Cost', 'Conversions']].drop_duplicates().head(5).to_string())
