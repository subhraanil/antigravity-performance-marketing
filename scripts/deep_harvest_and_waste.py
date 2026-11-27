import pandas as pd
import numpy as np

path = r'data\Share Samadhan\Search terms report.xlsx'
df = pd.read_excel(path, skiprows=2)
df_terms = df.iloc[:-3].copy()

numeric_cols = ['Clicks', 'Impr.', 'CTR', 'Avg. CPC', 'Cost', 'Conv. rate', 'Conversions', 'Cost / conv.']
for col in numeric_cols:
    df_terms[col] = pd.to_numeric(df_terms[col], errors='coerce').fillna(0)

# 1. High-Value Converting Terms NOT YET ADDED (Harvesting Candidates)
unadded_conv = df_terms[(df_terms['Conversions'] > 0) & (df_terms['Added/Excluded'].isna())].copy()
unadded_conv = unadded_conv.sort_values(by='Conversions', ascending=False)

print("=" * 90)
print(f"HIGH-VALUE CONVERTING TERMS NOT YET ADDED AS TARGET KEYWORDS ({len(unadded_conv)} terms)")
print("=" * 90)
print(unadded_conv[['Search term', 'Match type', 'Clicks', 'Cost', 'Conversions', 'Cost / conv.', 'Conv. rate']].head(30).to_string(index=False))

# 2. Complete Zero-Conversion Waste Breakdown
zero_conv = df_terms[df_terms['Conversions'] == 0].copy()
zero_conv_sorted = zero_conv.sort_values(by='Cost', ascending=False)

print("\n" + "=" * 90)
print(f"TOTAL ZERO-CONVERSION WASTED SPEND: INR {zero_conv['Cost'].sum():,.2f} across {len(zero_conv)} terms")
print("=" * 90)
print("TOP 30 HIGHEST BUDGET DRAINS (ZERO CONVERSIONS):")
print(zero_conv_sorted[['Search term', 'Match type', 'Clicks', 'Cost', 'Avg. CPC']].head(30).to_string(index=False))

# 3. Wasted spend by specific themes
pacl_waste = zero_conv[zero_conv['Search term'].str.contains('pacl|sebipacl|sahara|chit fund', case=False, na=False)]
govt_waste = zero_conv[zero_conv['Search term'].str.contains('scheme|yojana|pfms|ration|pmkisan', case=False, na=False)]
trading_waste = zero_conv[zero_conv['Search term'].str.contains('trading|trader|intraday|zerodha|groww|upstox|stock market|share market|broker', case=False, na=False)]
login_waste = zero_conv[zero_conv['Search term'].str.contains('login|portal login|signin|sign in', case=False, na=False)]

print("\n" + "=" * 90)
print("WASTED BUDGET BREAKDOWN BY JUNK/IRRELEVANT CLUSTERS")
print("=" * 90)
print(f"PACL / Sahara Scam Queries: {len(pacl_waste)} terms | Clicks: {pacl_waste['Clicks'].sum()} | Cost: INR {pacl_waste['Cost'].sum():,.2f}")
print(f"Govt Schemes / PFMS:        {len(govt_waste)} terms | Clicks: {govt_waste['Clicks'].sum()} | Cost: INR {govt_waste['Cost'].sum():,.2f}")
print(f"Trading / Broking / Stocks: {len(trading_waste)} terms | Clicks: {trading_waste['Clicks'].sum()} | Cost: INR {trading_waste['Cost'].sum():,.2f}")
print(f"Generic / Govt Login Intent: {len(login_waste)} terms | Clicks: {login_waste['Clicks'].sum()} | Cost: INR {login_waste['Cost'].sum():,.2f}")
