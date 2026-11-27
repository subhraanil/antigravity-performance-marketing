import pandas as pd

f_ad = r'c:\Users\test\Videos\Office\data\IAOL\Ad report (2).xlsx'
f_st = r'c:\Users\test\Videos\Office\data\IAOL\Search terms report - this month oct.xlsx'

df_ad = pd.read_excel(f_ad, skiprows=2)
df_st = pd.read_excel(f_st, skiprows=2)

print("=== AD REPORT (2).xlsx ===")
print("Shape:", df_ad.shape)
print("Columns:", df_ad.columns.tolist()[:30])
print("Campaigns in Ad Report:")
if 'Campaign' in df_ad.columns:
    print(df_ad['Campaign'].value_counts(dropna=False))

print("\n=== SEARCH TERMS REPORT - THIS MONTH OCT.xlsx ===")
print("Shape:", df_st.shape)
print("Columns:", df_st.columns.tolist())
print("Campaigns in Search Terms Report:")
if 'Campaign' in df_st.columns:
    print(df_st['Campaign'].value_counts(dropna=False))
