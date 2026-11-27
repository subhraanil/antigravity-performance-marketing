import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

f_7d = r'.\data\IHLS\Search terms report.xlsx'
df = pd.read_excel(f_7d, skiprows=2)
df_clean = df[~df['Search term'].astype(str).str.startswith('Total:')].copy()
for col in ['Cost', 'Conversions', 'Clicks']:
    df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0)

# Check all terms with clicks
clicked = df_clean[df_clean['Clicks'] > 0].sort_values(by='Cost', ascending=False)
print(f"Total terms with clicks: {len(clicked)}")
print(f"Total spend on clicked terms: ${clicked['Cost'].sum():.2f}")
print(f"Total conversions: {clicked['Conversions'].sum():.2f}")
print("\nAll Clicked Search Terms in Last 7 Days:")
print(clicked[['Search term', 'Campaign', 'Match type', 'Clicks', 'Cost', 'Conversions']].to_string())

# Check terms with impressions but 0 clicks
impr_only = df_clean[df_clean['Clicks'] == 0]
print(f"\nTotal terms with impressions only (0 clicks): {len(impr_only)}")

# Check exosome terms
exo_terms = df_clean[df_clean['Search term'].str.lower().str.contains('exosome')]
print(f"\nExosome terms appearing in last 7 days: {len(exo_terms)}")
print(exo_terms[['Search term', 'Campaign', 'Clicks', 'Cost']])

# Check salon terms
salon_terms = df_clean[df_clean['Search term'].str.lower().str.contains('hairhouse|djura|morris mead|floreat|dresser|coiffeur|barber')]
print(f"\nSalon terms appearing in last 7 days: {len(salon_terms)}")
print(salon_terms[['Search term', 'Campaign', 'Clicks', 'Cost']])

# Check competitor clinic terms
comp_terms = df_clean[df_clean['Search term'].str.lower().str.contains('peptonic|mira|ashley|gro|svenson|mosh|pilot|norwood')]
print(f"\nCompetitor terms appearing in last 7 days: {len(comp_terms)}")
print(comp_terms[['Search term', 'Campaign', 'Clicks', 'Cost']])
