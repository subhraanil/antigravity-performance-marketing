import pandas as pd
import numpy as np
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

f_30d = r'.\data\IHLS\Search terms report.xlsx'
df = pd.read_excel(f_30d, skiprows=2)
df_clean = df[~df['Search term'].astype(str).str.startswith('Total:')].copy()
for col in ['Cost', 'Conversions', 'Clicks']:
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0)

# Non-converting terms with cost > 0
non_conv = df_clean[(df_clean['Conversions'] == 0) & (df_clean['Cost'] > 0)].copy()

categories = {
    '1. Exosomes & Biologicals (TGA Risk)': [
        r'\bexosome\w*\b', r'\bexoscalp\b', r'\bdutexome\b'
    ],
    '2. Veterinary & Pet Drugs': [
        r'\bmeloxidyl\b', r'\bdog\b', r'\bcat\b', r'\bpet\b'
    ],
    '3. Weight Loss / GLP-1 Shedding': [
        r'\bmounjaro\b', r'\bozempic\b', r'\bwegovy\b'
    ],
    '4. Local Salons, Barbers & Hairdressers': [
        r'\bhairhouse\b', r'\bdjura\b', r'\bfloreat hair\b', r'\bmorris mead\b', r'\bjamie lee hair\b',
        r'\bbouf\b', r'\bcircles of hair\b', r'\bvelona\b', r'\bmiss paris\b', r'\bhair dresser\b',
        r'\bhairdresser\b', r'\bbarber\b', r'\bcoiffeur\b', r'\bfade\b', r'\bhair salon\b'
    ],
    '5. Cosmetic Aesthetic & Injector Clinics': [
        r'\brejuva\b', r'\bluume\b', r'\belevated aesthetics\b', r'\bpreventive dermatology\b'
    ],
    '6. Retail Brands, Shampoos & Supplements': [
        r'\baphogee\b', r'\ba ph ogee\b', r'\bcecred\b', r'\bzova\b', r'\bnourkrin\b',
        r'\bforce factor\b', r'\buniwigs\b', r'\bdekohair\b', r'\bgond katira\b', r'\bghk cu\b',
        r'\bchinamed\b', r'\bpantogar\b', r'\bk18\b', r'\bshampoo\b'
    ],
    '7. Competitor Hair Clinics & Telehealth': [
        r'\bgro clinics?\b', r'\bashley\s*(and|&)?\s*martin\b', r'\bbioscor\b', r'\bsvenson\b',
        r'\bmosh\b', r'\bpilot\b', r'\bhims\b', r'\bmira clinic\b', r'\beste medical\b',
        r'\bpeptonik\b', r'\bpeptonix\b', r'\bfloxhair\b', r'\byoracare\b', r'\bnovo\s*cabelo\b',
        r'\bhair doctors\b', r'\bregrowl\b'
    ],
    '8. Surgical Hair Transplants (FUE)': [
        r'\bfue clinic\w*\b', r'\bfue\b', r'\btransplant\b'
    ],
    '9. Standalone Broad Match Traps': [
        r'^treatment$', r'^dermatology$', r'^hair loss$', r'^hair growth$'
    ]
}

cat_results = []
for cat, patterns in categories.items():
    combined_regex = '|'.join(patterns)
    matched = non_conv[non_conv['Search term'].str.lower().str.contains(combined_regex, regex=True, na=False)]
    cost = matched['Cost'].sum()
    clicks = matched['Clicks'].sum()
    terms = len(matched)
    cat_results.append({
        'Category': cat,
        'Search Terms Count': terms,
        'Clicks': clicks,
        'Wasted Cost': cost,
        'Examples': matched.sort_values(by='Cost', ascending=False)['Search term'].head(3).tolist()
    })

df_cats = pd.DataFrame(cat_results).sort_values(by='Wasted Cost', ascending=False)
print("=== 30-DAY ZERO-CONVERSION WASTED SPEND BREAKDOWN ===")
print(df_cats.to_string(index=False))

# Check terms that don't match any category above
matched_any = non_conv['Search term'].str.lower().str.contains('|'.join([p for pats in categories.values() for p in pats]), regex=True, na=False)
unmatched = non_conv[~matched_any].sort_values(by='Cost', ascending=False)
print(f"\nUnmatched Non-Converting Terms (Spend: ${unmatched['Cost'].sum():.2f}):")
print(unmatched.head(20)[['Search term', 'Campaign', 'Match type', 'Clicks', 'Cost']].to_string())
