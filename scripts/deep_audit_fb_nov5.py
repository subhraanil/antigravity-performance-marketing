import pandas as pd

kw_path = r'data/IAOL/October/FB/Search keyword report.xlsx'
st_path = r'data/IAOL/October/FB/Search terms report.xlsx'

df_kw = pd.read_excel(kw_path, skiprows=2)
df_kw.columns = [str(c).strip() for c in df_kw.columns]

df_st = pd.read_excel(st_path, skiprows=2)
df_st.columns = [str(c).strip() for c in df_st.columns]

print("=== KEYWORDS IN PERIOD (Oct 29 - Nov 5) ===")
print("Total keywords in file:", len(df_kw))
# Clean numbers
for col in ['Clicks', 'Impr.', 'Cost', 'Avg. CPC', 'Conversions']:
    if col in df_kw.columns:
        df_kw[col] = pd.to_numeric(df_kw[col].astype(str).str.replace('₹', '').str.replace(',', '').str.strip(), errors='coerce').fillna(0)

print(df_kw.sort_values(by='Cost', ascending=False)[['Keyword', 'Match type', 'Clicks', 'Impr.', 'Avg. CPC', 'Cost', 'Conversions']].to_string(index=False))

print("\n=== SEARCH TERMS IN PERIOD (Oct 29 - Nov 5) ===")
print("Total search terms in file:", len(df_st))
for col in ['Clicks', 'Impr.', 'Cost', 'Avg. CPC', 'Conversions']:
    if col in df_st.columns:
        df_st[col] = pd.to_numeric(df_st[col].astype(str).str.replace('₹', '').str.replace(',', '').str.strip(), errors='coerce').fillna(0)

print("Terms with clicks > 0:")
print(df_st[df_st['Clicks'] > 0].sort_values(by='Cost', ascending=False)[['Search term', 'Match type', 'Clicks', 'Impr.', 'Avg. CPC', 'Cost', 'Conversions']].to_string(index=False))

print("\nTotal Spend on Search Terms with clicks:", df_st['Cost'].sum())
print("Total Clicks on Search Terms:", df_st['Clicks'].sum())
print("Total Conversions:", df_st['Conversions'].sum())
