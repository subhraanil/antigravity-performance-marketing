import pandas as pd

f_st = r'c:\Users\test\Videos\Office\data\IAOL\Search terms report - this month oct.xlsx'
df_st = pd.read_excel(f_st, skiprows=2)

num_cols = ['Cost', 'Clicks', 'Impr.', 'Avg. CPC', 'Conversions', 'Cost / conv.', 'Conv. rate']
for c in num_cols:
    if c in df_st.columns:
        df_st[c] = pd.to_numeric(df_st[c].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)

# Filter valid rows
df_st = df_st[df_st['Search term'].notnull() & (df_st['Search term'] != '--') & (~df_st['Search term'].astype(str).str.startswith('Total'))]

print("=== CAMPAIGN TYPES IN SEARCH TERMS REPORT ===")
print(df_st.groupby(['Campaign', 'Campaign type']).agg({'Cost':'sum', 'Clicks':'sum', 'Conversions':'sum'}).reset_index())
