import pandas as pd
import numpy as np

# Load excel, row 2 is date, row 3 is header (skiprows=2)
file_path = r'data/Pet Mode/Search terms report.xlsx'
df = pd.read_excel(file_path, skiprows=2)

print("Columns:", df.columns.tolist())
print(f"Total Search Terms in report: {len(df)}")

# Numeric conversion
for col in ['Clicks', 'Impr.', 'Cost', 'Conversions', 'Avg. CPC', 'Cost / conv.', 'Conv. rate', 'CTR']:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

total_impr = df['Impr.'].sum()
total_clicks = df['Clicks'].sum()
total_cost = df['Cost'].sum()
total_conv = df['Conversions'].sum()

print("\n================ TOTAL OVERVIEW (OCT 1 - OCT 15, 2026) ================")
print(f"Total Impressions: {total_impr:,.0f}")
print(f"Total Clicks: {total_clicks:,.0f}")
print(f"Total Cost: £{total_cost:,.2f}")
print(f"Total Conversions: {total_conv:.2f}")
print(f"CTR: {(total_clicks / total_impr * 100):.2f}%" if total_impr > 0 else "CTR: N/A")
print(f"Avg CPC: £{(total_cost / total_clicks):.2f}" if total_clicks > 0 else "Avg CPC: N/A")
print(f"Cost per Conversion (CPA): £{(total_cost / total_conv):.2f}" if total_conv > 0 else "CPA: N/A")
print(f"Conversion Rate: {(total_conv / total_clicks * 100):.2f}%" if total_clicks > 0 else "Conv Rate: N/A")

# 1. Converting Search Terms
print("\n================ 1. CONVERTING SEARCH TERMS ================")
conv_df = df[df['Conversions'] > 0].sort_values(by='Conversions', ascending=False)
print(f"Found {len(conv_df)} converting search terms:")
for idx, r in conv_df.iterrows():
    print(f"• '{r['Search term']}' | Clicks: {r['Clicks']} | Impr: {r['Impr.']} | Cost: £{r['Cost']:.2f} | Conv: {r['Conversions']} | CPA: £{r['Cost / conv.']:.2f} | Status: {r['Added/Excluded']}")

# 2. Terms with Clicks
clicks_df = df[df['Clicks'] > 0].copy()
print(f"\n================ 2. SEARCH TERMS WITH CLICKS ================")
print(f"Total terms with >= 1 click: {len(clicks_df)} (out of {len(df)} total terms)")
print(f"Spend on clicked terms: £{clicks_df['Cost'].sum():,.2f}")

# 3. Top Spenders without Conversions (Wasted Spend)
print("\n================ 3. TOP WASTED SPEND (CLICKS >= 1, CONVERSIONS == 0) ================")
zero_conv_df = clicks_df[clicks_df['Conversions'] == 0].sort_values(by='Cost', ascending=False)
print(f"Total zero-conversion terms with spend: {len(zero_conv_df)} | Total Wasted Cost: £{zero_conv_df['Cost'].sum():,.2f}")
print(zero_conv_df[['Search term', 'Clicks', 'Impr.', 'Cost', 'Avg. CPC', 'Added/Excluded']].head(25).to_string())

# 4. Search Term Categories / Thematic Clustering
print("\n================ 4. THEMATIC INTENT BREAKDOWN ================")
themes = {
    'Dental & Teeth (Hero)': r'teeth|dental|toothbrush|chew|tartar|plaque|molar',
    'Beds & Furniture': r'bed|cot|sofa|cushion|mat|cooling mat|calming',
    'Car & Travel': r'car|seat|booster|travel|seatbelt|belt|carrier',
    'Grooming & Hair': r'brush|steam|groom|clipper|nail|hair remover|shedding',
    'Cat Products & Scratchers': r'cat|scratch|scratching|kitten|litter',
    'Bark & Training Collars': r'bark|collar|training|anti bark|shock',
    'Harness & Leashes': r'harness|leash|lead|collar|reflective',
    'Water Fountains & Feeding': r'fountain|water|bowl|feeder|dispenser',
    'Electronics / Leakage (AirTag/GPS/Trackers)': r'airtag|gps|tracker|apple|moravon|tile',
    'Competitor Brands': r'luther bennett|pawrade|zoospot|pets at home|amazon|omlet|tractive|pitpat',
    'Veterinary / Medical / Injury': r'vet|injury|paw|surgery|cone|wound|parvovirus|arthritis'
}

for theme_name, pattern in themes.items():
    theme_matches = df[df['Search term'].str.contains(pattern, case=False, na=False)]
    theme_clicks = theme_matches['Clicks'].sum()
    theme_cost = theme_matches['Cost'].sum()
    theme_conv = theme_matches['Conversions'].sum()
    theme_impr = theme_matches['Impr.'].sum()
    print(f"• {theme_name}: {len(theme_matches)} terms | Impr: {theme_impr:,.0f} | Clicks: {theme_clicks:.0f} | Cost: £{theme_cost:.2f} | Conv: {theme_conv:.1f}")

# 5. High Impression / Zero Click Terms (CTR < 0.1% or 0 clicks with high impressions)
print("\n================ 5. HIGH IMPRESSION TERMS (IMPR >= 20, CLICKS == 0) ================")
high_impr_zero_click = df[(df['Impr.'] >= 15) & (df['Clicks'] == 0)].sort_values(by='Impr.', ascending=False)
print(f"Count: {len(high_impr_zero_click)}")
print(high_impr_zero_click[['Search term', 'Impr.', 'Added/Excluded']].head(20).to_string())

# 6. Specific Leakage & Junk Terms to Exclude
print("\n================ 6. IDENTIFIED LEAKAGE SEARCH TERMS ================")
leak_patterns = r'airtag|gps|tracker|apple|camera|phone|free|cheap|diy|vet|parvo|flea|tick|injury|boot|bandage|luther bennett|pawrade|zoospot'
leaks = df[df['Search term'].str.contains(leak_patterns, case=False, na=False)]
print(f"Total leak terms found: {len(leaks)} | Clicks: {leaks['Clicks'].sum()} | Cost: £{leaks['Cost'].sum():.2f}")
print(leaks[leaks['Clicks'] > 0][['Search term', 'Clicks', 'Cost', 'Avg. CPC', 'Added/Excluded']].to_string())
