import pandas as pd
import numpy as np
import re
import os

f_details = r'.\data\IHLS\Negative keyword details report.xlsx'
df_d = pd.read_excel(f_details, skiprows=2)
f_rep = r'.\data\IHLS\Negative keyword report.xlsx'
df_r = pd.read_excel(f_rep, skiprows=2)

print('=== EXISTING NEGATIVES ===')
print('Details count:', len(df_d))
print('Report count:', len(df_r))

def clean_kw(kw):
    if pd.isna(kw): 
        return ''
    kw = str(kw).strip()
    if kw.startswith('"') and kw.endswith('"'):
        kw = kw[1:-1]
    if kw.startswith('[') and kw.endswith(']'):
        kw = kw[1:-1]
    return kw.lower().strip()

details_kws = set(df_d['keyword_text'].apply(clean_kw))
report_kws = set(df_r['Negative keyword'].apply(clean_kw))

details_kws.discard('')
report_kws.discard('')

print('Unique cleaned kws in details:', len(details_kws))
print('Unique cleaned kws in report:', len(report_kws))
combined_existing = details_kws.union(report_kws)
print('Total unique combined existing negatives:', len(combined_existing))
print('In both:', len(details_kws.intersection(report_kws)))
print('In details only:', len(details_kws - report_kws))
print('In report only:', len(report_kws - details_kws))

# Check match type distributions
print('\nDetails match types:\n', df_d['match_type'].value_counts())
print('\nReport match types:\n', df_r['Match type'].value_counts())
print('\nReport levels:\n', df_r['Level'].value_counts())
print('\nReport campaigns:\n', df_r['Campaign'].value_counts())
