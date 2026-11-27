import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# Set style
plt.style.use('ggplot')

# Load Chart.csv
df = pd.read_csv('data/favb6 search console data/Chart.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['CTR'] = df['CTR'].str.rstrip('%').astype('float')
df['YearMonth'] = df['Date'].dt.to_period('M')

# Group by month
monthly = df.groupby('YearMonth').agg(
    Clicks=('Clicks', 'sum'),
    Impressions=('Impressions', 'sum'),
    Avg_CTR=('CTR', 'mean'),
    Avg_Position=('Position', 'mean'),
    Days=('Date', 'count')
).reset_index()

monthly['Daily_Clicks'] = monthly['Clicks'] / monthly['Days']
monthly['Daily_Impressions'] = monthly['Impressions'] / monthly['Days']

# Estimate full August 2026 (31 days)
aug_idx = monthly[monthly['YearMonth'] == '2026-08'].index[0]
aug_daily_clicks = monthly.loc[aug_idx, 'Daily_Clicks']
aug_daily_imps = monthly.loc[aug_idx, 'Daily_Impressions']
aug_projected_clicks = int(aug_daily_clicks * 31)
aug_projected_imps = int(aug_daily_imps * 31)

# Historical monthly clicks list
hist_months = ['Nov 25', 'Dec 25', 'Jan 26', 'Feb 26', 'Mar 26', 'Apr 26', 'May 26', 'Jun 26', 'Jul 26', 'Aug 26 (Est)']
hist_clicks = list(monthly['Clicks'][:-1]) + [aug_projected_clicks]
hist_imps = list(monthly['Impressions'][:-1]) + [aug_projected_imps]

# Forecast model for next 3 months (Sept 26, Oct 26, Nov 26)
# Growth rate based on recent MoM momentum (May -> Jun -> Jul -> Aug): ~15% to 20% MoM
# Conservative scenario: +12% MoM
# Moderate growth scenario: +18% MoM
# Aggressive growth scenario: +25% MoM

scenarios = {
    'Conservative (+12% MoM)': 0.12,
    'Moderate (+18% MoM)': 0.18,
    'Aggressive (+25% MoM)': 0.25
}

forecast_results = {}
for sc_name, growth in scenarios.items():
    s_clicks = [int(aug_projected_clicks * ((1 + growth) ** i)) for i in range(1, 4)]
    s_imps = [int(aug_projected_imps * ((1 + growth) ** i)) for i in range(1, 4)]
    forecast_results[sc_name] = {
        'Sep 26 Clicks': s_clicks[0], 'Oct 26 Clicks': s_clicks[1], 'Nov 26 Clicks': s_clicks[2],
        'Sep 26 Imps': s_imps[0], 'Oct 26 Imps': s_imps[1], 'Nov 26 Imps': s_imps[2],
        'Total 3M Clicks': sum(s_clicks), 'Total 3M Imps': sum(s_imps)
    }

# Print summary
print("=== FABB6 HISTORICAL & FORECAST SUMMARY ===")
print(f"Aug 2026 Run-rate (Projected): {aug_projected_clicks:,} organic clicks | {aug_projected_imps:,} impressions")
print("\n3-Month Forecast Scenarios (Sept - Nov 2026):")
for k, v in forecast_results.items():
    print(f"\nScenario: {k}")
    print(f"  Sept 2026: {v['Sep 26 Clicks']:,} clicks ({v['Sep 26 Imps']:,} imps)")
    print(f"  Oct 2026:  {v['Oct 26 Clicks']:,} clicks ({v['Oct 26 Imps']:,} imps)")
    print(f"  Nov 2026:  {v['Nov 26 Clicks']:,} clicks ({v['Nov 26 Imps']:,} imps)")
    print(f"  Total 3-Month Organic Clicks: {v['Total 3M Clicks']:,}")

# Generate visual forecast chart
plt.figure(figsize=(12, 6))

all_months = hist_months + ['Sep 26 (F)', 'Oct 26 (F)', 'Nov 26 (F)']
mod_clicks = hist_clicks + [forecast_results['Moderate (+18% MoM)']['Sep 26 Clicks'],
                            forecast_results['Moderate (+18% MoM)']['Oct 26 Clicks'],
                            forecast_results['Moderate (+18% MoM)']['Nov 26 Clicks']]
cons_clicks = hist_clicks + [forecast_results['Conservative (+12% MoM)']['Sep 26 Clicks'],
                             forecast_results['Conservative (+12% MoM)']['Oct 26 Clicks'],
                             forecast_results['Conservative (+12% MoM)']['Nov 26 Clicks']]
aggr_clicks = hist_clicks + [forecast_results['Aggressive (+25% MoM)']['Sep 26 Clicks'],
                             forecast_results['Aggressive (+25% MoM)']['Oct 26 Clicks'],
                             forecast_results['Aggressive (+25% MoM)']['Nov 26 Clicks']]

x = np.arange(len(all_months))

plt.plot(x[:10], hist_clicks, color='#1A73E8', linewidth=2.5, marker='o', linestyle='-', label='Historical Organic Clicks')
plt.plot(x[9:], cons_clicks[9:], color='#FBBC04', linewidth=2, marker='s', linestyle='--', label='Forecast: Conservative (+12%)')
plt.plot(x[9:], mod_clicks[9:], color='#34A853', linewidth=2.5, marker='*', linestyle='-', label='Forecast: Moderate (+18%)')
plt.plot(x[9:], aggr_clicks[9:], color='#EA4335', linewidth=2, marker='^', linestyle='--', label='Forecast: Aggressive (+25%)')

plt.xticks(x, all_months, rotation=45)
plt.title('Fabb6 Organic Search Performance & 3-Month Growth Forecast (Sept-Nov 2026)', fontsize=14, pad=15)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Monthly Organic Clicks', fontsize=12)
plt.legend(loc='upper left')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()

os.makedirs('reports', exist_ok=True)
chart_path = 'reports/fabb6_3month_forecast.png'
plt.savefig(chart_path, dpi=300)
print(f"\nChart saved successfully to {chart_path}")
