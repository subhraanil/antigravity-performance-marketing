import pandas as pd

df = pd.read_excel(r'data/IAOL/October/Search terms report.xlsx', skiprows=2)
# Clean columns
df.columns = [c.strip() for c in df.columns]

for camp in ['French-Bangalore', 'French-Mumbai', 'German-Mumbai', 'German-Pune', 'German-Hydrabad', 'German-Bangalore', 'New Merged']:
    camp_df = df[df['Campaign'].str.contains(camp, case=False, na=False)]
    if camp_df.empty:
        # try matching partial
        words = camp.split('-')
        camp_df = df[df['Campaign'].str.contains(words[0], case=False, na=False) & df['Campaign'].str.contains(words[1], case=False, na=False)] if len(words)>1 else df[df['Campaign'].str.contains(camp, case=False, na=False)]
    
    print(f"\n==========================================")
    print(f"SEARCH TERMS AUDIT: {camp} (Total queries: {len(camp_df)})")
    print(f"==========================================")
    
    # Top spending zero-conversion terms
    zero_conv = camp_df[camp_df['Conversions'] == 0].sort_values(by='Cost', ascending=False)
    print("Top 5 Wasted Spend Queries (Zero Conversions):")
    print(zero_conv[['Search term', 'Clicks', 'Avg. CPC', 'Cost']].head(5).to_string(index=False))
    
    # Top converting terms
    conv = camp_df[camp_df['Conversions'] > 0].sort_values(by='Conversions', ascending=False)
    print("\nTop 5 Converting Queries:")
    print(conv[['Search term', 'Clicks', 'Cost', 'Conversions', 'Cost / conv.']].head(5).to_string(index=False))
