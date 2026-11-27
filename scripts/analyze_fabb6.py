import pandas as pd
import numpy as np

# Load Chart.csv
df = pd.read_csv('data/favb6 search console data/Chart.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['CTR'] = df['CTR'].str.rstrip('%').astype('float')

# Add Year-Month
df['YearMonth'] = df['Date'].dt.to_period('M')

# Group by Month
monthly = df.groupby('YearMonth').agg(
    Clicks=('Clicks', 'sum'),
    Impressions=('Impressions', 'sum'),
    Avg_CTR=('CTR', 'mean'),
    Avg_Position=('Position', 'mean'),
    Days=('Date', 'count')
).reset_index()

print("Monthly Historical Data for Fabb6:")
print(monthly.to_string())

# Daily average per month
monthly['Daily_Clicks'] = monthly['Clicks'] / monthly['Days']
monthly['Daily_Impressions'] = monthly['Impressions'] / monthly['Days']

print("\nFull Month Metrics & Daily Averages:")
print(monthly[['YearMonth', 'Clicks', 'Daily_Clicks', 'Impressions', 'Daily_Impressions', 'Avg_CTR', 'Avg_Position']].to_string())
