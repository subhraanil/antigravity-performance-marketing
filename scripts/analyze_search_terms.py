import pandas as pd
import numpy as np
import openpyxl

path = r'data\Share Samadhan\Search terms report.xlsx'
df = pd.read_excel(path, skiprows=2)
df_terms = df.iloc[:-3].copy()

numeric_cols = ['Clicks', 'Impr.', 'CTR', 'Avg. CPC', 'Cost', 'Conv. rate', 'Conversions', 'Cost / conv.']
for col in numeric_cols:
    df_terms[col] = pd.to_numeric(df_terms[col], errors='coerce').fillna(0)

conv_df = df_terms[df_terms['Conversions'] > 0].copy()
non_conv_df = df_terms[df_terms['Conversions'] == 0].copy()

total_spend = df_terms['Cost'].sum()
conv_spend = conv_df['Cost'].sum()
non_conv_spend = non_conv_df['Cost'].sum()

print("=" * 80)
print("AGGREGATE REPORTED SEARCH TERMS SUMMARY (2 YEARS: Nov 2024 - Oct 2026)")
print("=" * 80)
print(f"Total Unique Search Terms: {len(df_terms):,}")
print(f"Total Impressions: {df_terms['Impr.'].sum():,}")
print(f"Total Clicks: {df_terms['Clicks'].sum():,}")
print(f"Total Cost: INR {total_spend:,.2f}")
print(f"Total Conversions: {conv_df['Conversions'].sum():,.2f}")
print(f"Average CTR: {(df_terms['Clicks'].sum()/df_terms['Impr.'].sum()*100):.2f}%")
print(f"Average CPC: INR {(total_spend/df_terms['Clicks'].sum()):.2f}")
print(f"Average CPA: INR {(total_spend/conv_df['Conversions'].sum()):.2f}")
print(f"Average Conversion Rate: {(conv_df['Conversions'].sum()/df_terms['Clicks'].sum()*100):.2f}%")

print("\n" + "=" * 80)
print("CONVERTING VS NON-CONVERTING EFFICIENCY")
print("=" * 80)
print(f"Converting Search Terms: {len(conv_df):,} ({len(conv_df)/len(df_terms)*100:.1f}% of terms)")
print(f"Non-Converting Search Terms: {len(non_conv_df):,} ({len(non_conv_df)/len(df_terms)*100:.1f}% of terms)")
print(f"Converting Spend: INR {conv_spend:,.2f} ({conv_spend/total_spend*100:.1f}% of total spend)")
print(f"Non-Converting (Wasted) Spend: INR {non_conv_spend:,.2f} ({non_conv_spend/total_spend*100:.1f}% of total spend)")
print(f"Converting Terms CPA: INR {(conv_spend/conv_df['Conversions'].sum()):.2f}")

print("\n" + "=" * 80)
print("MATCH TYPE PERFORMANCE BREAKDOWN")
print("=" * 80)
mt_summary = df_terms.groupby('Match type').agg(
    terms=('Search term', 'count'),
    clicks=('Clicks', 'sum'),
    cost=('Cost', 'sum'),
    conversions=('Conversions', 'sum')
).reset_index()
mt_summary['Spend_Share_%'] = mt_summary['cost'] / total_spend * 100
mt_summary['Conv_Share_%'] = mt_summary['conversions'] / conv_df['Conversions'].sum() * 100
mt_summary['CPC'] = mt_summary['cost'] / mt_summary['clicks']
mt_summary['CPA'] = mt_summary['cost'] / mt_summary['conversions']
mt_summary['CVR_%'] = mt_summary['conversions'] / mt_summary['clicks'] * 100
print(mt_summary.to_string(index=False))

print("\n" + "=" * 80)
print("ADDED / EXCLUDED STATUS BREAKDOWN")
print("=" * 80)
ae_summary = df_terms.groupby('Added/Excluded').agg(
    terms=('Search term', 'count'),
    clicks=('Clicks', 'sum'),
    cost=('Cost', 'sum'),
    conversions=('Conversions', 'sum')
).reset_index()
ae_summary['CPA'] = ae_summary['cost'] / ae_summary['conversions']
ae_summary['CVR_%'] = ae_summary['conversions'] / ae_summary['clicks'] * 100
print(ae_summary.to_string(index=False))

print("\n" + "=" * 80)
print("TOP 25 CONVERTING SEARCH TERMS")
print("=" * 80)
top_conv = conv_df.sort_values(by='Conversions', ascending=False).head(25)
print(top_conv[['Search term', 'Match type', 'Added/Excluded', 'Clicks', 'Cost', 'Conversions', 'Cost / conv.', 'Conv. rate']].to_string(index=False))

print("\n" + "=" * 80)
print("TOP 25 HIGHEST SPEND NON-CONVERTING SEARCH TERMS (WASTED BUDGET)")
print("=" * 80)
top_wasted = non_conv_df.sort_values(by='Cost', ascending=False).head(25)
print(top_wasted[['Search term', 'Match type', 'Added/Excluded', 'Clicks', 'Cost', 'Avg. CPC']].to_string(index=False))
