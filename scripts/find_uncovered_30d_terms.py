import pandas as pd
import numpy as np
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

f_30d = r'.\data\IHLS\Search terms report.xlsx'
df_30 = pd.read_excel(f_30d, skiprows=2)
df_30 = df_30[~df_30['Search term'].astype(str).str.startswith('Total:')].copy()
for col in ['Cost', 'Conversions', 'Clicks']:
    df_30[col] = pd.to_numeric(df_30[col], errors='coerce').fillna(0)

# Load existing negatives from previous uploads
f_master = r'C:\Users\test\.gemini\antigravity\brain\df28e754-e5af-4512-9dfa-8b5ee40a4aed\Master_Negative_Keywords_IHLS.xlsx'
df_master = pd.read_excel(f_master, sheet_name='Master Negative List')
master_negatives = set(df_master['Negative Keyword'].astype(str).str.lower().str.strip())

# Add previously recommended 14d and 7d additions
f_14d = r'C:\Users\test\.gemini\antigravity\brain\df28e754-e5af-4512-9dfa-8b5ee40a4aed\New_Negative_Additions_Last14Days.xlsx'
if f_14d:
    df_14 = pd.read_excel(f_14d)
    master_negatives.update(df_14['Negative Keyword'].astype(str).str.lower().str.strip())

f_7d = r'C:\Users\test\.gemini\antigravity\brain\df28e754-e5af-4512-9dfa-8b5ee40a4aed\New_Negative_Additions_Last7Days.xlsx'
if f_7d:
    df_7 = pd.read_excel(f_7d)
    master_negatives.update(df_7['Negative Keyword'].astype(str).str.lower().str.strip())

print(f"Total existing negative keywords in knowledge base: {len(master_negatives)}")

# Check non-converting terms with cost > 0
non_conv_cost = df_30[(df_30['Conversions'] == 0) & (df_30['Cost'] > 0)].copy()

# Find terms that are pure waste and not covered yet
uncovered = []
for idx, r in non_conv_cost.iterrows():
    st = r['Search term'].lower().strip()
    cost = r['Cost']
    clicks = r['Clicks']
    camp = r['Campaign']
    
    # Check if any negative is present as substring
    is_covered = any(neg in st for neg in master_negatives)
    uncovered.append({
        'Search term': st,
        'Campaign': camp,
        'Clicks': clicks,
        'Cost': cost,
        'Covered': is_covered
    })

df_unc = pd.DataFrame(uncovered)
print("\nUncovered non-converting search terms with spend:")
not_covered = df_unc[~df_unc['Covered']].sort_values(by='Cost', ascending=False)
print(not_covered.to_string())
print(f"\nTotal spend on uncovered non-converting terms: ${not_covered['Cost'].sum():.2f}")
