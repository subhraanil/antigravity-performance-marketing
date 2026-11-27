import pandas as pd
import os

out_dir = 'reports'
os.makedirs(out_dir, exist_ok=True)

# 15 Columns matching Google Sheet Template exactly:
columns = [
    'Month',
    'Total Orders',
    'Google Orders',
    'Meta Orders',
    'Organic/Direct Orders',
    'Repeat/Retention Orders',
    'Google Spend (INR)',
    'Meta Spend (INR)',
    'Total Paid Spend (INR)',
    'Blended Paid CPA (INR)',
    'AOV (INR)',
    'Est. Total Revenue (INR)',
    'Blended ROAS (Rev/Ad Spend)',
    'Avg Daily Orders',
    '% of Daily Target (1,500)'
]

rows = [
    {
        'Month': "Month 1 (Sep '26)",
        'Total Orders': 21450,
        'Google Orders': 6600,
        'Meta Orders': 7000,
        'Organic/Direct Orders': 3550,
        'Repeat/Retention Orders': 4300,
        'Google Spend (INR)': 3200000.0,
        'Meta Spend (INR)': 2200000.0,
        'Total Paid Spend (INR)': 5400000.0,
        'Blended Paid CPA (INR)': 397.06,
        'AOV (INR)': 896.50,
        'Est. Total Revenue (INR)': 19230000.0,
        'Blended ROAS (Rev/Ad Spend)': 3.56,
        'Avg Daily Orders': 715,
        '% of Daily Target (1,500)': '47.7%'
    },
    {
        'Month': "Month 2 (Oct '26)",
        'Total Orders': 25400,
        'Google Orders': 8000,
        'Meta Orders': 8200,
        'Organic/Direct Orders': 3900,
        'Repeat/Retention Orders': 5300,
        'Google Spend (INR)': 3800000.0,
        'Meta Spend (INR)': 2600000.0,
        'Total Paid Spend (INR)': 6400000.0,
        'Blended Paid CPA (INR)': 395.06,
        'AOV (INR)': 907.87,
        'Est. Total Revenue (INR)': 23060000.0,
        'Blended ROAS (Rev/Ad Spend)': 3.60,
        'Avg Daily Orders': 820,
        '% of Daily Target (1,500)': '54.7%'
    },
    {
        'Month': "Month 3 (Nov '26)",
        'Total Orders': 31000,
        'Google Orders': 9600,
        'Meta Orders': 9800,
        'Organic/Direct Orders': 4800,
        'Repeat/Retention Orders': 6800,
        'Google Spend (INR)': 4500000.0,
        'Meta Spend (INR)': 3200000.0,
        'Total Paid Spend (INR)': 7700000.0,
        'Blended Paid CPA (INR)': 396.91,
        'AOV (INR)': 914.52,
        'Est. Total Revenue (INR)': 28350000.0,
        'Blended ROAS (Rev/Ad Spend)': 3.68,
        'Avg Daily Orders': 1033,
        '% of Daily Target (1,500)': '68.9%'
    },
    {
        'Month': "Month 4 (Dec '26)",
        'Total Orders': 37500,
        'Google Orders': 11200,
        'Meta Orders': 11400,
        'Organic/Direct Orders': 6100,
        'Repeat/Retention Orders': 8800,
        'Google Spend (INR)': 5200000.0,
        'Meta Spend (INR)': 3800000.0,
        'Total Paid Spend (INR)': 9000000.0,
        'Blended Paid CPA (INR)': 398.23,
        'AOV (INR)': 921.60,
        'Est. Total Revenue (INR)': 34560000.0,
        'Blended ROAS (Rev/Ad Spend)': 3.84,
        'Avg Daily Orders': 1210,
        '% of Daily Target (1,500)': '80.7%'
    },
    {
        'Month': "Month 5 (Jan '27)",
        'Total Orders': 41400,
        'Google Orders': 12200,
        'Meta Orders': 12500,
        'Organic/Direct Orders': 6400,
        'Repeat/Retention Orders': 10300,
        'Google Spend (INR)': 5600000.0,
        'Meta Spend (INR)': 4200000.0,
        'Total Paid Spend (INR)': 9800000.0,
        'Blended Paid CPA (INR)': 396.76,
        'AOV (INR)': 924.15,
        'Est. Total Revenue (INR)': 38260000.0,
        'Blended ROAS (Rev/Ad Spend)': 3.90,
        'Avg Daily Orders': 1335,
        '% of Daily Target (1,500)': '89.0%'
    },
    {
        'Month': "Month 6 (Feb '27)",
        'Total Orders': 45000,
        'Google Orders': 13200,
        'Meta Orders': 13400,
        'Organic/Direct Orders': 7000,
        'Repeat/Retention Orders': 11400,
        'Google Spend (INR)': 6000000.0,
        'Meta Spend (INR)': 4500000.0,
        'Total Paid Spend (INR)': 10500000.0,
        'Blended Paid CPA (INR)': 394.74,
        'AOV (INR)': 933.33,
        'Est. Total Revenue (INR)': 42000000.0,
        'Blended ROAS (Rev/Ad Spend)': 4.00,
        'Avg Daily Orders': 1500,
        '% of Daily Target (1,500)': '100.0%'
    },
    {
        'Month': '6-Month Cumulative',
        'Total Orders': 201750,
        'Google Orders': 68800,
        'Meta Orders': 67300,
        'Organic/Direct Orders': 31750,
        'Repeat/Retention Orders': 43900,
        'Google Spend (INR)': 28300000.0,
        'Meta Spend (INR)': 20500000.0,
        'Total Paid Spend (INR)': 48800000.0,
        'Blended Paid CPA (INR)': 395.73,
        'AOV (INR)': 919.26,
        'Est. Total Revenue (INR)': 185460000.0,
        'Blended ROAS (Rev/Ad Spend)': 3.80,
        'Avg Daily Orders': 1102,
        '% of Daily Target (1,500)': '73.5% avg'
    }
]

df = pd.DataFrame(rows, columns=columns)

csv_path = os.path.join(out_dir, 'fabb6_populated_google_sheet.csv')
xlsx_path = os.path.join(out_dir, 'FABB6_Populated_Google_Sheet_Model.xlsx')

df.to_csv(csv_path, index=False)
with pd.ExcelWriter(xlsx_path) as writer:
    df.to_excel(writer, sheet_name='Forecast_Sheet', index=False)

print(f"Generated populated Google Sheet CSV at {csv_path}")
print(f"Generated populated Google Sheet Excel at {xlsx_path}")
