import pandas as pd
import numpy as np
import os

oct_folder = r'C:\Users\test\Videos\Office\data\IAOL\October'

# 1. Search keyword report
f_kw = os.path.join(oct_folder, 'Search keyword report.xlsx')
df_kw = pd.read_excel(f_kw, skiprows=2)
print("=== SEARCH KEYWORD REPORT (TARGET KEYWORDS) ===")
print("Columns:", df_kw.columns.tolist())
print("Shape:", df_kw.shape)
print("Campaigns:", df_kw['Campaign'].value_counts(dropna=False))

# 2. Ad report
f_ad = os.path.join(oct_folder, 'Ad report (2).xlsx')
df_ad = pd.read_excel(f_ad, skiprows=2)
print("\n=== AD REPORT ===")
print("Columns:", df_ad.columns.tolist()[:20])
print("Shape:", df_ad.shape)
print("Campaigns:", df_ad['Campaign'].value_counts(dropna=False))

# 3. Search terms report
f_st = os.path.join(oct_folder, 'Search terms report.xlsx')
df_st = pd.read_excel(f_st, skiprows=2)
print("\n=== SEARCH TERMS REPORT ===")
print("Columns:", df_st.columns.tolist())
print("Shape:", df_st.shape)
print("Campaigns:", df_st['Campaign'].value_counts(dropna=False))
