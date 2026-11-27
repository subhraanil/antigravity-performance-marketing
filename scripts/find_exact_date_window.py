import pandas as pd

excel_path = r'data/IAOL/October/IAOL-GoogleAds.xlsx'
target_campaigns = [
    'DemandGen', 'French-Bangalore', 'French-Mumbai', 'German-Bangalore',
    'German-Hydrabad', 'German-Mumbai', 'German-Pune', 'New Merged', 'Remarketing-PMax'
]

# We want to match table values:
# French-Bangalore: 7d: 3180.27, 14d: 1608.83
# German-Mumbai: 7d: 1419.97, 14d: 1082.88
# German-Pune: 7d: 747.33, 14d: 891.65

for end_date_str in ['2026-11-01', '2026-10-31', '2026-10-30', '2026-11-02']:
    end_date = pd.to_datetime(end_date_str)
    for d_len in [7, 14]:
        start_date = end_date - pd.Timedelta(days=d_len-1)
        results = {}
        for camp in ['French-Bangalore', 'German-Mumbai', 'German-Pune']:
            df = pd.read_excel(excel_path, sheet_name=camp)
            date_col = [c for c in df.columns if 'date' in str(c).lower() or 'day' in str(c).lower()][0]
            df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
            sub = df[(df[date_col] >= start_date) & (df[date_col] <= end_date)]
            cost = sub['Cost'].sum()
            leads = sub['Leads'].sum()
            cpa = cost / leads if leads > 0 else 0
            results[camp] = cpa
        print(f"Window: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')} ({d_len}d) -> French-Bangalore: {results['French-Bangalore']:.2f}, German-Mumbai: {results['German-Mumbai']:.2f}, German-Pune: {results['German-Pune']:.2f}")
