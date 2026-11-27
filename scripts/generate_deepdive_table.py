import pandas as pd
import numpy as np

excel_path = r'data/IAOL/October/IAOL-GoogleAds.xlsx'
target_campaigns = [
    'DemandGen', 'French-Bangalore', 'French-Mumbai', 'German-Bangalore',
    'German-Hydrabad', 'German-Mumbai', 'German-Pune', 'New Merged', 'Remarketing-PMax'
]

windows = {
    'October (Oct 1 - Oct 31)': ('2026-10-01', '2026-10-31'),
    'Last 14 Days (Oct 19 - Nov 1)': ('2026-10-19', '2026-11-01'),
    'Last 7 Days (Oct 26 - Nov 1)': ('2026-10-26', '2026-11-01')
}

all_data = []

for camp in target_campaigns:
    df = pd.read_excel(excel_path, sheet_name=camp)
    date_col = [c for c in df.columns if 'date' in str(c).lower() or 'day' in str(c).lower()][0]
    df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
    
    # normalize columns
    cost_col = [c for c in df.columns if c.lower() == 'cost'][0]
    leads_col = [c for c in df.columns if c.lower() in ['leads', 'lead', 'conversion', 'conversions']][0]
    clicks_col = [c for c in df.columns if c.lower() == 'clicks'][0] if any(c.lower() == 'clicks' for c in df.columns) else None
    imp_col = [c for c in df.columns if 'imp' in c.lower()][0] if any('imp' in c.lower() for c in df.columns) else None

    camp_res = {'Campaign': camp}
    for w_name, (s_date, e_date) in windows.items():
        sub = df[(df[date_col] >= pd.to_datetime(s_date)) & (df[date_col] <= pd.to_datetime(e_date))]
        cost = sub[cost_col].sum()
        leads = sub[leads_col].sum()
        clicks = sub[clicks_col].sum() if clicks_col else 0
        imps = sub[imp_col].sum() if imp_col else 0
        cpa = cost / leads if leads > 0 else (cost if cost > 0 else 0)
        cpc = cost / clicks if clicks > 0 else 0
        cvr = (leads / clicks * 100) if clicks > 0 else 0
        ctr = (clicks / imps * 100) if imps > 0 else 0
        
        prefix = 'Oct' if 'October' in w_name else ('14d' if '14' in w_name else '7d')
        camp_res[f'{prefix}_Cost'] = cost
        camp_res[f'{prefix}_Leads'] = leads
        camp_res[f'{prefix}_Clicks'] = clicks
        camp_res[f'{prefix}_CPA'] = cpa
        camp_res[f'{prefix}_CPC'] = cpc
        camp_res[f'{prefix}_CvR'] = cvr
        camp_res[f'{prefix}_CTR'] = ctr

    all_data.append(camp_res)

res_df = pd.DataFrame(all_data)
pd.set_option('display.max_columns', 30)
pd.set_option('display.width', 1000)
print(res_df.to_string())

res_df.to_csv(r'scripts/cpa_comparison_deepdive.csv', index=False)
