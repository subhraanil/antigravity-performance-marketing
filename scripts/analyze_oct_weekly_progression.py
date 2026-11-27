import pandas as pd
import openpyxl

f_ga = r'C:\Users\test\Videos\Office\data\IAOL\October\IAOL-GoogleAds.xlsx'
wb_ga = openpyxl.load_workbook(f_ga)

print("=" * 80)
print("WEEKLY PROGRESSION ACROSS OCTOBER 2026 (FROM IAOL-GoogleAds.xlsx)")
print("=" * 80)

weeks = [
    ('Oct 1 - Oct 7', '2026-10-01', '2026-10-07'),
    ('Oct 8 - Oct 14', '2026-10-08', '2026-10-14'),
    ('Oct 15 - Oct 21', '2026-10-15', '2026-10-21'),
    ('Oct 22 - Oct 28', '2026-10-22', '2026-10-28'),
    ('Oct 29 - Oct 31', '2026-10-29', '2026-10-31')
]

active_camps = ['German-Mumbai', 'German-Pune', 'German-Hydrabad', 'German-Bangalore', 'French-Mumbai', 'French-Bangalore', 'New Merged']

week_records = []

for w_name, start_d, end_d in weeks:
    tot_cost = 0
    tot_clicks = 0
    tot_leads = 0
    tot_impr = 0
    camp_stats = {}
    for camp in active_camps:
        df = pd.read_excel(f_ga, sheet_name=camp)
        date_col = 'Date' if 'Date' in df.columns else ('Data' if 'Data' in df.columns else df.columns[0])
        df['Parsed_Date'] = pd.to_datetime(df[date_col], errors='coerce')
        for col in ['Impression', 'Clicks', 'Leads', 'Cost']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '').str.replace(' --', '0').str.replace('--', '0').str.strip(), errors='coerce').fillna(0)
        
        w_df = df[(df['Parsed_Date'] >= start_d) & (df['Parsed_Date'] <= end_d)]
        c_cost = w_df['Cost'].sum()
        c_clicks = w_df['Clicks'].sum()
        c_leads = w_df['Leads'].sum()
        c_cpa = c_cost / c_leads if c_leads > 0 else 0
        camp_stats[camp] = (c_cost, c_leads, c_cpa)
        tot_cost += c_cost
        tot_clicks += c_clicks
        tot_leads += c_leads
        tot_impr += w_df['Impression'].sum()
    
    tot_cpa = tot_cost / tot_leads if tot_leads > 0 else 0
    tot_cpc = tot_cost / tot_clicks if tot_clicks > 0 else 0
    tot_cvr = tot_leads / tot_clicks * 100 if tot_clicks > 0 else 0
    
    week_records.append({
        'Week': w_name,
        'Spend': tot_cost,
        'Clicks': tot_clicks,
        'Leads': tot_leads,
        'Avg_CPC': tot_cpc,
        'CPA': tot_cpa,
        'CVR': tot_cvr,
        'Camp_Stats': camp_stats
    })

df_weeks = pd.DataFrame(week_records)
print(df_weeks[['Week', 'Spend', 'Clicks', 'Leads', 'Avg_CPC', 'CPA', 'CVR']].to_string(index=False))

print("\n--- Campaign Breakdown Week-over-Week ---")
for r in week_records:
    print(f"\n{r['Week']} (Total Spend: Rs.{r['Spend']:,.2f} | Leads: {r['Leads']:.1f} | Blended CPA: Rs.{r['CPA']:.2f}):")
    for camp, stats in r['Camp_Stats'].items():
        print(f"  {camp:<18}: Spend Rs.{stats[0]:>8,.2f} | Leads: {stats[1]:>4.1f} | CPA: Rs.{stats[2]:>8.2f}")
