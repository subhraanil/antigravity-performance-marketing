import pandas as pd

oct_kw_path = r'data/IAOL/October/Search keyword report.xlsx'
fb_kw_path = r'data/IAOL/October/FB/Search keyword report.xlsx'

df_oct = pd.read_excel(oct_kw_path, skiprows=2)
df_oct.columns = [str(c).strip() for c in df_oct.columns]
df_oct_fb = df_oct[df_oct['Campaign'].str.contains('French', case=False, na=False) & df_oct['Campaign'].str.contains('Bangalore', case=False, na=False)]

df_new = pd.read_excel(fb_kw_path, skiprows=2)
df_new.columns = [str(c).strip() for c in df_new.columns]
df_new = df_new[df_new['Keyword'].notnull()]

oct_kw_set = set(df_oct_fb['Keyword'].dropna().str.strip())
new_kw_set = set(df_new['Keyword'].dropna().str.strip())

print("=== KEYWORDS IN OCT FULL MONTH BUT MISSING IN NEW (Oct 29 - Nov 5) ===")
missing_in_new = oct_kw_set - new_kw_set
for kw in missing_in_new:
    row = df_oct_fb[df_oct_fb['Keyword'].str.strip() == kw].iloc[0]
    print(f"- {kw} | Match: {row['Match type']} | Oct Clicks: {row.get('Clicks')} | Oct Conv: {row.get('Conversions')}")

print("\n=== KEYWORDS IN NEW BUT NOT IN OCT FULL MONTH ===")
added_in_new = new_kw_set - oct_kw_set
for kw in added_in_new:
    row = df_new[df_new['Keyword'].str.strip() == kw].iloc[0]
    print(f"+ {kw} | Match: {row['Match type']} | New Clicks: {row.get('Clicks')} | New Cost: {row.get('Cost')}")
