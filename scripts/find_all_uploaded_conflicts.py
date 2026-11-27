import pandas as pd
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

f_user_txt = r'.\data\IHLS\user_uploaded_negatives.txt'
f_all = r'.\data\IHLS\Search terms report - all time.xlsx'

df_all = pd.read_excel(f_all, skiprows=2)
df_all = df_all[~df_all['Search term'].astype(str).str.startswith('Total:')].copy()
for col in ['Cost', 'Conversions', 'Clicks']:
    df_all[col] = pd.to_numeric(df_all[col], errors='coerce').fillna(0)

# Check all converting search terms
conv_terms = df_all[df_all['Conversions'] > 0][['Search term', 'Cost', 'Conversions']].drop_duplicates()

with open(f_user_txt, 'r', encoding='utf-8') as f:
    user_lines = [l.strip() for l in f if l.strip()]

critical_warnings = []
for line in user_lines:
    raw = line
    if raw.startswith('"') and raw.endswith('"'):
        clean = raw[1:-1].strip().lower()
        mt = 'PHRASE'
    elif raw.startswith('[') and raw.endswith(']'):
        clean = raw[1:-1].strip().lower()
        mt = 'EXACT'
    else:
        clean = raw.strip().lower()
        mt = 'BROAD'
    
    # Check if this term matches ANY converting search term with stemming / plural
    for idx, r in conv_terms.iterrows():
        st = str(r['Search term']).lower()
        blocked = False
        
        if mt == 'EXACT':
            if clean == st:
                blocked = True
        elif mt == 'PHRASE':
            # Check exact word boundary
            if re.search(r'\b' + re.escape(clean) + r'\b', st):
                blocked = True
            # Also check simple plural / singular in phrase
            elif clean.endswith('s') and re.search(r'\b' + re.escape(clean[:-1]) + r'\b', st):
                blocked = True
            elif not clean.endswith('s') and re.search(r'\b' + re.escape(clean + 's') + r'\b', st):
                blocked = True
        elif mt == 'BROAD':
            # Google Ads broad negative matches exact token, but NOT synonyms or plurals
            # HOWEVER, if token is present, it blocks!
            tokens = clean.split()
            if all(re.search(r'\b' + re.escape(t) + r'\b', st) for t in tokens):
                blocked = True
            # Also check plural/singular
            elif all(re.search(r'\b' + re.escape(t) + r's?\b', st) for t in tokens):
                blocked = True
        
        if blocked:
            critical_warnings.append({
                'Negative Uploaded': raw,
                'Match Type': mt,
                'Blocked Converting Term': r['Search term'],
                'Conversions': r['Conversions'],
                'Cost': r['Cost']
            })

df_crit = pd.DataFrame(critical_warnings).drop_duplicates(subset=['Negative Uploaded', 'Blocked Converting Term'])
print(f"Total critical warnings: {len(df_crit)}")
print(df_crit.to_string())
