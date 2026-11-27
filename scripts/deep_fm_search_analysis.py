import pandas as pd

excel_file = r"c:\Users\test\Videos\Office\data\IAOL\Search terms report - FM.xlsx"
df = pd.read_excel(excel_file, skiprows=2)

num_cols = ['Cost', 'Impr.', 'Interactions', 'Avg. cost', 'Conv. rate', 'Avg. CPC', 'Clicks', 'Conv. value', 'Conversions', 'Cost / conv.']
for c in num_cols:
    if c in df.columns:
        df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)

df = df[df['Search term'].notnull() & (df['Search term'] != '--') & (~df['Search term'].astype(str).str.startswith('Total'))]

print("Total search terms rows:", len(df))

# Check Ad groups
print("\nAd group performance:")
ag_grp = df.groupby('Ad group').agg({'Cost':'sum', 'Clicks':'sum', 'Conversions':'sum'}).reset_index()
ag_grp['CPC'] = ag_grp['Cost'] / ag_grp['Clicks']
ag_grp['CPA'] = ag_grp['Cost'] / ag_grp['Conversions']
ag_grp['CVR'] = ag_grp['Conversions'] / ag_grp['Clicks'] * 100
print(ag_grp.to_string(index=False))

# Check Match types in search terms
print("\nMatch type performance:")
mt_grp = df.groupby('Match type').agg({'Cost':'sum', 'Clicks':'sum', 'Conversions':'sum'}).reset_index()
mt_grp['CPC'] = mt_grp['Cost'] / mt_grp['Clicks']
mt_grp['CPA'] = mt_grp['Cost'] / mt_grp['Conversions']
print(mt_grp.to_string(index=False))

# Look for bizarre / irrelevant search terms
print("\nCheck bizarre search terms with spend:")
terms = df[['Search term', 'Cost', 'Clicks', 'Conversions', 'Avg. CPC', 'Match type']].sort_values('Cost', ascending=False)

# Let's inspect terms with single clicks or high CPC
high_cpc = df[df['Avg. CPC'] > 100].sort_values('Cost', ascending=False)
print(f"\nSearch terms with CPC > Rs 100 (Count: {len(high_cpc)}, Total Cost: Rs {high_cpc['Cost'].sum():.2f}):")
for _, r in high_cpc.head(15).iterrows():
    print(f"'{r['Search term']}' | Cost: Rs {r['Cost']:.2f} | Clicks: {r['Clicks']} | CPC: Rs {r['Avg. CPC']:.2f} | Conv: {r['Conversions']}")

# Terms containing specific patterns
patterns = ['french in a week', 'frites', 'duolingo', 'free', 'jobs', 'salary', 'syllabus', 'kids', 'school', 'delhi', 'pune', 'bangalore', 'chennai', 'hyderabad', 'meaning', 'translation', 'translate', 'french teacher near me', 'tutor', 'tuition']
print("\nPattern check:")
for p in patterns:
    matches = df[df['Search term'].str.lower().str.contains(p, na=False)]
    if len(matches) > 0:
        print(f"Pattern '{p}': {len(matches)} queries | Cost: Rs {matches['Cost'].sum():.2f} | Conv: {matches['Conversions'].sum()}")
