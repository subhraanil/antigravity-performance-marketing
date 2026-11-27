import pandas as pd
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

f_details = r'.\data\IHLS\Negative keyword details report.xlsx'
df_d = pd.read_excel(f_details, skiprows=2)
f_rep = r'.\data\IHLS\Negative keyword report.xlsx'
df_r = pd.read_excel(f_rep, skiprows=2)

def clean_kw(kw):
    if pd.isna(kw): return ''
    kw = str(kw).strip().lower()
    if kw.startswith('"') and kw.endswith('"'): kw = kw[1:-1]
    if kw.startswith('[') and kw.endswith(']'): kw = kw[1:-1]
    return kw.strip()

df_d['clean'] = df_d['keyword_text'].apply(clean_kw)
df_r['clean'] = df_r['Negative keyword'].apply(clean_kw)

print("Short negatives in details (len <= 3):")
short_d = set(df_d[df_d['clean'].str.len() <= 3]['clean'])
print(sorted([k for k in short_d if k]))

print("\nShort negatives in report (len <= 3):")
short_r = set(df_r[df_r['clean'].str.len() <= 3]['clean'])
print(sorted([k for k in short_r if k]))

dangerous_candidates = ['hair', 'loss', 'clinic', 'perth', 'treatment', 'specialist', 'growth', 'regrowth', 'subiaco', 'ihls', 'doctor', 'dermatologist', 'trichologist']
print("\nDangerous terms in details list:")
for t in dangerous_candidates:
    match = df_d[df_d['clean'] == t]
    if len(match) > 0:
        print(f"  FOUND IN DETAILS: '{t}' with match type {match['match_type'].tolist()}")

print("\nDangerous terms in report list:")
for t in dangerous_candidates:
    match = df_r[df_r['clean'] == t]
    if len(match) > 0:
        print(f"  FOUND IN REPORT: '{t}' with match type {match['Match type'].tolist()} in campaigns {match['Campaign'].tolist()}")
