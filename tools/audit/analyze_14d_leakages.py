import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

f_14d = r'.\data\IHLS\Search terms report.xlsx'
df = pd.read_excel(f_14d, skiprows=2)
df_clean = df[~df['Search term'].astype(str).str.startswith('Total:')].copy()
for col in ['Cost', 'Conversions', 'Clicks']:
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0)

# Load master negative list uploaded previously
f_master = r'.\data\IHLS\Master_Negative_Keywords_IHLS.xlsx'
df_neg = pd.read_excel(f_master, sheet_name='Master Negative List')
existing_negatives = set(df_neg['Negative Keyword'].astype(str).str.lower().str.strip())

# New negative opportunities from last 14 days
new_candidates = [
    # Weight Loss & GLP-1 Medications causing hair loss
    ('mounjaro', 'PHRASE', 'Weight loss drug causing hair loss (low commercial intent for in-clinic hair systems)'),
    ('ozempic', 'PHRASE', 'GLP-1 drug causing hair shedding'),
    ('wegovy', 'PHRASE', 'GLP-1 drug causing hair shedding'),
    
    # Pet & Veterinary Medications
    ('meloxidyl', 'PHRASE', 'Veterinary NSAID pet medication'),
    
    # Subiaco / Perth Hair Salons & Retail Chains
    ('hairhouse', 'PHRASE', 'Hairhouse Warehouse salon chain (Subiaco, Midland, Perth)'),
    ('hairhouse midland', 'PHRASE', 'Specific Midland salon store'),
    ('bouf', 'PHRASE', 'Bouf Hair Salon in Subiaco'),
    ('jamie lee hair', 'PHRASE', 'Local Perth hair salon'),
    ('cecred', 'PHRASE', 'Beyonce consumer retail hair care line'),
    ('zova', 'PHRASE', 'Retail hair growth product'),
    ('absci', 'PHRASE', 'Biotech lab research drug development query'),
    
    # Local Aesthetic / Injector Clinics (Non-Hair Loss)
    ('rejuva', 'PHRASE', 'Rejuva cosmetic clinic (Como)'),
    ('rejuva como', 'PHRASE', 'Specific Como cosmetic clinic'),
    ('luume', 'PHRASE', 'Luume Aesthetics cosmetic injector clinic'),
    ('elevated aesthetics', 'PHRASE', 'Aesthetic clinic'),
    
    # Broad Generic Match Traps
    ('treatment', 'EXACT', 'Single word broad trap ($14.60 wasted on 1 click)'),
    ('dermatology', 'EXACT', 'Single word general dermatology trap'),
    
    # Surgical FUE clinics (if non-surgical is IHLS focus)
    ('fue clinics perth', 'PHRASE', 'Surgical FUE clinic inquiry ($22.80 wasted)'),
    ('fue clinics', 'PHRASE', 'Surgical FUE clinic inquiry')
]

print("=== NEW NEGATIVE CANDIDATES FROM LAST 14 DAYS ===")
df_new_neg = pd.DataFrame(new_candidates, columns=['Negative Keyword', 'Match Type', 'Reason'])

# Check which ones are already in master list
df_new_neg['Already in Master'] = df_new_neg['Negative Keyword'].apply(lambda x: x in existing_negatives)
print(df_new_neg.to_string())

# Calculate spend on these new leakage terms in last 14 days
total_leakage_spend = 0
for kw, mt, reason in new_candidates:
    matched = df_clean[df_clean['Search term'].str.lower().str.contains(kw)]
    spend = matched['Cost'].sum()
    clicks = matched['Clicks'].sum()
    if spend > 0 or clicks > 0:
        print(f"Leakage matched '{kw}': {len(matched)} queries, {clicks} clicks, ${spend:.2f} spend")
        total_leakage_spend += spend

print(f"\nTotal spend on these specific leakages in last 14 days: ${total_leakage_spend:.2f}")
