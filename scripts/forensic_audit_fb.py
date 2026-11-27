import pandas as pd
import openpyxl

kw_path = r'data/IAOL/October/FB/Search keyword report.xlsx'
st_path = r'data/IAOL/October/FB/Search terms report.xlsx'

df_kw = pd.read_excel(kw_path, skiprows=2)
df_kw.columns = [str(c).strip() for c in df_kw.columns]

df_st = pd.read_excel(st_path, skiprows=2)
df_st.columns = [str(c).strip() for c in df_st.columns]

print("=== KEYWORD REPORT COLUMNS ===")
print(df_kw.columns.tolist())

print("\n=== KEYWORD REPORT DATA ===")
for idx, r in df_kw.iterrows():
    kw = r.get('Keyword')
    status = r.get('Keyword status')
    clicks = r.get('Clicks')
    cost = r.get('Cost')
    cpc = r.get('Avg. CPC')
    final_url = r.get('Final URL')
    if pd.notnull(kw):
        print(f"[{status}] {kw} ({r.get('Match type')}): Clicks={clicks}, Cost={cost}, CPC={cpc}, Final URL={final_url}")

print("\n=== SEARCH TERMS REPORT COLUMNS ===")
print(df_st.columns.tolist())

print("\n=== ALL SEARCH TERMS (sorted by clicks/cost) ===")
for idx, r in df_st.iterrows():
    st = r.get('Search term')
    if pd.notnull(st) and 'total' not in str(st).lower():
        clicks = r.get('Clicks')
        impr = r.get('Impr.')
        cost = r.get('Cost')
        cpc = r.get('Avg. CPC')
        conv = r.get('Conversions')
        added = r.get('Added/Excluded')
        match = r.get('Match type')
        if clicks > 0 or impr > 5:
            print(f"Search term: '{st}' | Match: {match} | Added: {added} | Impr: {impr} | Clicks: {clicks} | CPC: {cpc} | Cost: {cost} | Conv: {conv}")
