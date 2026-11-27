import pandas as pd

df_kw = pd.read_excel(r'data/IAOL/October/FB/Search keyword report.xlsx', skiprows=2)
df_kw.columns = [str(c).strip() for c in df_kw.columns]
print("Keywords in FB/Search keyword report.xlsx:")
for idx, r in df_kw.iterrows():
    kw = r.get('Keyword')
    mt = r.get('Match type')
    status = r.get('Keyword status')
    if pd.notnull(kw):
        print(f"{idx}: {status} | {mt} | {kw}")
