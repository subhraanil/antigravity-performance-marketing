import pandas as pd
import os

base_dir = r'c:\Users\test\Videos\Office\data\favb6 search console data'

# Load Fabb6 datasets
chart_df = pd.read_csv(os.path.join(base_dir, 'Chart.csv'))
queries_df = pd.read_csv(os.path.join(base_dir, 'Queries.csv'))
pages_df = pd.read_csv(os.path.join(base_dir, 'Pages.csv'))
countries_df = pd.read_csv(os.path.join(base_dir, 'Countries.csv'))
devices_df = pd.read_csv(os.path.join(base_dir, 'Devices.csv'))

# Convert Chart.csv
chart_df['Date'] = pd.to_datetime(chart_df['Date'])
chart_df['CTR'] = chart_df['CTR'].str.rstrip('%').astype('float')
chart_df['YearMonth'] = chart_df['Date'].dt.to_period('M')

# Monthly aggregation
monthly = chart_df.groupby('YearMonth').agg(
    Clicks=('Clicks', 'sum'),
    Impressions=('Impressions', 'sum'),
    Avg_CTR=('CTR', 'mean'),
    Avg_Position=('Position', 'mean'),
    Days=('Date', 'count')
).reset_index()

monthly['Daily_Clicks'] = (monthly['Clicks'] / monthly['Days']).round(2)
monthly['Daily_Impressions'] = (monthly['Impressions'] / monthly['Days']).round(2)

print("=== AUTHENTIC FABB6 MONTHLY PERFORMANCE ===")
print(monthly.to_string(index=False))

print("\n=== AUTHENTIC FABB6 TOP QUERIES (TOP 10) ===")
print(queries_df.head(10).to_string(index=False))

print("\n=== AUTHENTIC FABB6 TOP LANDING PAGES (TOP 10) ===")
print(pages_df.head(10).to_string(index=False))

print("\n=== AUTHENTIC FABB6 GEOGRAPHIC BREAKDOWN (TOP 5) ===")
print(countries_df.head(5).to_string(index=False))

print("\n=== AUTHENTIC FABB6 DEVICE BREAKDOWN ===")
print(devices_df.to_string(index=False))
