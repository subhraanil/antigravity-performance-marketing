import pandas as pd

f_all = r"c:\Users\test\Videos\Office\data\IAOL\IAOL - Target Keywords All time.xlsx"
f_30d = r"c:\Users\test\Videos\Office\data\IAOL\Target Keywords last 30 days.xlsx"

df_all = pd.read_excel(f_all, skiprows=2)
df_30d = pd.read_excel(f_30d, skiprows=2)

num_cols = ['Impr.', 'Interactions', 'Cost', 'Avg. CPC', 'Clicks', 'Conversions', 'Cost / conv.']
for df in [df_all, df_30d]:
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)

df_all = df_all[df_all['Campaign'].notnull() & (df_all['Campaign'] != '--') & (df_all['Keyword'].notnull())]
df_30d = df_30d[df_30d['Campaign'].notnull() & (df_30d['Campaign'] != '--') & (df_30d['Keyword'].notnull())]

# Group by Campaign + Keyword
grp_all = df_all.groupby(['Campaign', 'Keyword', 'Match type']).agg({'Cost':'sum', 'Clicks':'sum', 'Conversions':'sum'}).reset_index()
grp_all.rename(columns={'Cost':'Cost_All', 'Clicks':'Clicks_All', 'Conversions':'Conv_All'}, inplace=True)
grp_all['CPA_All'] = grp_all['Cost_All'] / grp_all['Conv_All']
grp_all['CPC_All'] = grp_all['Cost_All'] / grp_all['Clicks_All']

grp_30d = df_30d.groupby(['Campaign', 'Keyword', 'Match type']).agg({'Cost':'sum', 'Clicks':'sum', 'Conversions':'sum'}).reset_index()
grp_30d.rename(columns={'Cost':'Cost_30d', 'Clicks':'Clicks_30d', 'Conversions':'Conv_30d'}, inplace=True)
grp_30d['CPA_30d'] = grp_30d['Cost_30d'] / grp_30d['Conv_30d']
grp_30d['CPC_30d'] = grp_30d['Cost_30d'] / grp_30d['Clicks_30d']

merged = pd.merge(grp_all, grp_30d, on=['Campaign', 'Keyword', 'Match type'], how='outer').fillna(0)

print("Merged total unique campaign-keyword pairs:", len(merged))

# 1. Consistent Lifetime Bleeders (Spend >= 3000 All time, CPA > 1200 or 0 conv)
print("\n=== 1. CONSISTENT LIFETIME BLEEDERS (All-Time CPA > Rs 1,200 or 0 Conv & All-Time Spend >= Rs 3,000) ===")
lifetime_bleeders = merged[(merged['Cost_All'] >= 3000) & ((merged['Conv_All'] == 0) | (merged['CPA_All'] > 1200))].sort_values('Cost_All', ascending=False)
for _, r in lifetime_bleeders.iterrows():
    cpa_all_str = f"Rs. {r['CPA_All']:,.0f}" if r['Conv_All'] > 0 else "0 Conv"
    cpa_30d_str = f"Rs. {r['CPA_30d']:,.0f}" if r['Conv_30d'] > 0 else "0 Conv"
    print(f"[{r['Campaign']}] {r['Keyword']} ({r['Match type']}) | Lifetime: Spend Rs. {r['Cost_All']:,.0f}, Leads {r['Conv_All']:.1f}, CPA {cpa_all_str} | Last30d: Spend Rs. {r['Cost_30d']:,.0f}, Leads {r['Conv_30d']:.1f}, CPA {cpa_30d_str}")

# 2. Lifetime Stars that Degraded Recently
print("\n=== 2. HISTORICAL PROVEN STARS THAT DEGRADED RECENTLY (All-Time Leads >= 10, All-Time CPA <= Rs 750, but Last 30d CPA > Rs 1,200 or 0 Conv) ===")
degraded = merged[(merged['Conv_All'] >= 10) & (merged['CPA_All'] <= 750) & (merged['Cost_30d'] >= 1000) & ((merged['Conv_30d'] == 0) | (merged['CPA_30d'] > 1200))].sort_values('Cost_30d', ascending=False)
for _, r in degraded.iterrows():
    cpa_all_str = f"Rs. {r['CPA_All']:,.0f}" if r['Conv_All'] > 0 else "0 Conv"
    cpa_30d_str = f"Rs. {r['CPA_30d']:,.0f}" if r['Conv_30d'] > 0 else "0 Conv"
    print(f"[{r['Campaign']}] {r['Keyword']} ({r['Match type']}) | Lifetime: Spend Rs. {r['Cost_All']:,.0f}, Leads {r['Conv_All']:.1f}, CPA {cpa_all_str} | Last30d: Spend Rs. {r['Cost_30d']:,.0f}, Leads {r['Conv_30d']:.1f}, CPA {cpa_30d_str}")

# 3. Consistent All-Time & Recent Superstars
print("\n=== 3. CONSISTENT ALL-TIME & RECENT SUPERSTARS (All-Time Leads >= 10, Lifetime CPA <= Rs 700, Last 30d CPA <= Rs 700) ===")
stars = merged[(merged['Conv_All'] >= 10) & (merged['CPA_All'] <= 700) & (merged['Conv_30d'] >= 2) & (merged['CPA_30d'] <= 700)].sort_values('Conv_All', ascending=False)
for _, r in stars.iterrows():
    cpa_all_str = f"Rs. {r['CPA_All']:,.0f}"
    cpa_30d_str = f"Rs. {r['CPA_30d']:,.0f}"
    print(f"[{r['Campaign']}] {r['Keyword']} ({r['Match type']}) | Lifetime: Spend Rs. {r['Cost_All']:,.0f}, Leads {r['Conv_All']:.1f}, CPA {cpa_all_str} | Last30d: Spend Rs. {r['Cost_30d']:,.0f}, Leads {r['Conv_30d']:.1f}, CPA {cpa_30d_str}")

# 4. Zero Conversion Lifetime
print("\n=== 4. ZERO CONVERSION IN ENTIRE LIFETIME ===")
lifetime_zeros = merged[(merged['Conv_All'] == 0) & (merged['Cost_All'] >= 500)].sort_values('Cost_All', ascending=False)
for _, r in lifetime_zeros.iterrows():
    print(f"[{r['Campaign']}] {r['Keyword']} ({r['Match type']}) | Lifetime Spend: Rs. {r['Cost_All']:,.0f} (0 Leads) | Last 30d Spend: Rs. {r['Cost_30d']:,.0f}")
