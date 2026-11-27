import pandas as pd
import os

base_dir = r'c:\Users\test\Videos\Office\data\favb6 search console data'
os.makedirs('reports', exist_ok=True)

chart_df = pd.read_csv(os.path.join(base_dir, 'Chart.csv'))
queries_df = pd.read_csv(os.path.join(base_dir, 'Queries.csv'))
pages_df = pd.read_csv(os.path.join(base_dir, 'Pages.csv'))
countries_df = pd.read_csv(os.path.join(base_dir, 'Countries.csv'))
devices_df = pd.read_csv(os.path.join(base_dir, 'Devices.csv'))

chart_df['Date'] = pd.to_datetime(chart_df['Date'])
chart_df['CTR'] = chart_df['CTR'].str.rstrip('%').astype('float')
chart_df['YearMonth'] = chart_df['Date'].dt.to_period('M')

monthly = chart_df.groupby('YearMonth').agg(
    Clicks=('Clicks', 'sum'),
    Impressions=('Impressions', 'sum'),
    Avg_CTR=('CTR', 'mean'),
    Avg_Position=('Position', 'mean'),
    Days=('Date', 'count')
).reset_index()

monthly['Daily_Clicks'] = (monthly['Clicks'] / monthly['Days']).round(2)
monthly['Daily_Impressions'] = (monthly['Impressions'] / monthly['Days']).round(2)

# Export Excel
with pd.ExcelWriter('reports/fabb6_authentic_search_performance.xlsx') as writer:
    monthly.to_excel(writer, sheet_name='Monthly_Organic', index=False)
    queries_df.head(100).to_excel(writer, sheet_name='Top_Queries', index=False)
    pages_df.head(100).to_excel(writer, sheet_name='Top_Pages', index=False)
    countries_df.to_excel(writer, sheet_name='Countries', index=False)
    devices_df.to_excel(writer, sheet_name='Devices', index=False)

monthly.to_csv('reports/fabb6_monthly_search.csv', index=False)
print("Exported authentic Fabb6 performance data to reports/fabb6_authentic_search_performance.xlsx")
