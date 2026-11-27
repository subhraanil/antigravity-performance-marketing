import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 30-day report (Oct 14 - Nov 12)
f_30d = r'.\data\IHLS\Search terms report.xlsx'
df_30 = pd.read_excel(f_30d, skiprows=2)
df_30 = df_30[~df_30['Search term'].astype(str).str.startswith('Total:')].copy()
for col in ['Cost', 'Conversions', 'Clicks']:
    df_30[col] = pd.to_numeric(df_30[col], errors='coerce').fillna(0)

# Previous 7-day report (Oct 26 - Nov 1)
f_7d = r'C:\Users\test\Videos\Office\data\IHLS\Search terms report.xlsx'
df_7 = pd.read_excel(f_7d, skiprows=2)
df_7 = df_7[~df_7['Search term'].astype(str).str.startswith('Total:')].copy()
for col in ['Cost', 'Conversions', 'Clicks']:
    df_7[col] = pd.to_numeric(df_7[col], errors='coerce').fillna(0)

# Previous 14-day report (Oct 14 - Oct 27)
# Let's see if we can find new terms or clicks in 30d that were not in 14d
print(f"30-day total terms: {len(df_30)}, Spend: ${df_30['Cost'].sum():.2f}, Conv: {df_30['Conversions'].sum():.2f}")
print(f"7-day (Oct 26 - Nov 1) total terms: {len(df_7)}, Spend: ${df_7['Cost'].sum():.2f}, Conv: {df_7['Conversions'].sum():.2f}")

# Compare converting terms
print("\nConverting terms in 30-day:")
conv_30 = df_30[df_30['Conversions'] > 0][['Search term', 'Campaign', 'Clicks', 'Cost', 'Conversions']].sort_values(by='Conversions', ascending=False)
print(conv_30.to_string())

# Terms with spend in 30-day that had 0 spend in Oct 26-Nov 1
terms_7d_dict = dict(zip(df_7['Search term'].str.lower().str.strip(), df_7['Cost']))
terms_7d_clicks = dict(zip(df_7['Search term'].str.lower().str.strip(), df_7['Clicks']))

df_30['Cost_in_7d'] = df_30['Search term'].str.lower().str.strip().map(terms_7d_dict).fillna(0)
df_30['Clicks_in_7d'] = df_30['Search term'].str.lower().str.strip().map(terms_7d_clicks).fillna(0)

df_30['Delta_Cost'] = df_30['Cost'] - df_30['Cost_in_7d']
df_30['Delta_Clicks'] = df_30['Clicks'] - df_30['Clicks_in_7d']

print("\nTerms with significant spend in 30-day:")
top_spend_30 = df_30.sort_values(by='Cost', ascending=False).head(30)
print(top_spend_30[['Search term', 'Campaign', 'Clicks', 'Cost', 'Conversions', 'Cost_in_7d']].to_string())
