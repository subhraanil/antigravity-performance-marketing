import pandas as pd

oct_kw_path = r'data/IAOL/October/Search keyword report.xlsx'
fb_kw_path = r'data/IAOL/October/FB/Search keyword report.xlsx'
ad_path = r'data/IAOL/October/Ad report (2).xlsx'

# 1. Compare October full keywords for French-Bangalore with current FB keywords
df_oct_kw = pd.read_excel(oct_kw_path, skiprows=2)
df_oct_kw.columns = [str(c).strip() for c in df_oct_kw.columns]
fb_oct = df_oct_kw[df_oct_kw['Campaign'].str.contains('French', case=False, na=False) & df_oct_kw['Campaign'].str.contains('Bangalore', case=False, na=False)]

print("=== OCT FULL MONTH: French Bangalore Target Keywords ===")
print("Count:", len(fb_oct))
# Clean numbers
for col in ['Clicks', 'Impr.', 'Cost', 'Avg. CPC', 'Conversions']:
    if col in fb_oct.columns:
        fb_oct[col] = pd.to_numeric(fb_oct[col].astype(str).str.replace('₹', '').str.replace(',', '').str.strip(), errors='coerce').fillna(0)

# Sort by conversions
print("\nTop converting keywords in October full month:")
conv_oct = fb_oct[fb_oct['Conversions'] > 0].sort_values(by='Conversions', ascending=False)
print(conv_oct[['Keyword', 'Match type', 'Clicks', 'Impr.', 'Avg. CPC', 'Cost', 'Conversions', 'Cost / conv.']].to_string(index=False))

print("\n=== ADS FOR French-Bangalore ===")
df_ads = pd.read_excel(ad_path, skiprows=2)
df_ads.columns = [str(c).strip() for c in df_ads.columns]
fb_ads = df_ads[df_ads['Campaign'].str.contains('French', case=False, na=False) & df_ads['Campaign'].str.contains('Bangalore', case=False, na=False)]
print(fb_ads[['Campaign', 'Ad group', 'Ad status', 'Ad strength', 'Final URL', 'Clicks', 'Cost', 'Conversions']].to_string(index=False))
