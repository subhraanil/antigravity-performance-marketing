import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('reports', exist_ok=True)

# 1. GA4 Actuals (Extracted from GA4 Screenshots for Fabb6)
ga4_data = [
    {
        'Month': 'May 2026',
        'Total_Key_Events': 10553.00,
        'Ads_Cost_INR': 2136192.16,
        'CPA_INR': 202.43,
        'Ads_Impressions': 21028268,
        'Ads_Clicks': 406489,
        'CPC_INR': 5.26,
        'Total_Revenue_INR': 9988197.87,
        'Blended_ROAS': 4.68,
        'PMax_Revenue_INR': 6538664.16,
        'Organic_Social_Revenue_INR': 2478486.36,
        'Organic_Search_Revenue_INR': 198334.64,
        'Direct_Revenue_INR': 143145.64
    },
    {
        'Month': 'June 2026',
        'Total_Key_Events': 10824.00,
        'Ads_Cost_INR': 2733879.76,
        'CPA_INR': 252.58,
        'Ads_Impressions': 24195604,
        'Ads_Clicks': 463241,
        'CPC_INR': 5.90,
        'Total_Revenue_INR': 9787782.81,
        'Blended_ROAS': 3.58,
        'PMax_Revenue_INR': 6591668.51,
        'Organic_Social_Revenue_INR': 2199738.80,
        'Organic_Search_Revenue_INR': 259576.50,
        'Direct_Revenue_INR': 126487.53
    },
    {
        'Month': 'July 2026',
        'Total_Key_Events': 11016.00,
        'Ads_Cost_INR': 2477269.87,
        'CPA_INR': 224.88,
        'Ads_Impressions': 24776428,
        'Ads_Clicks': 473338,
        'CPC_INR': 5.23,
        'Total_Revenue_INR': 9523277.02,
        'Blended_ROAS': 3.84,
        'PMax_Revenue_INR': 6490293.13,
        'Organic_Social_Revenue_INR': 1920753.15,
        'Organic_Search_Revenue_INR': 284332.20,
        'Direct_Revenue_INR': 155233.49
    },
    {
        'Month': 'August 2026 (1-21 MTD)',
        'Total_Key_Events': 7078.00,
        'Ads_Cost_INR': 2817626.07,
        'CPA_INR': 398.08,
        'Ads_Impressions': 27441726,
        'Ads_Clicks': 495407,
        'CPC_INR': 5.69,
        'Total_Revenue_INR': 6564039.13,
        'Blended_ROAS': 2.33,
        'PMax_Revenue_INR': 4587423.04,
        'Organic_Social_Revenue_INR': 1051802.62,
        'Organic_Search_Revenue_INR': 350407.75,
        'Direct_Revenue_INR': 121508.93
    }
]

df_ga4 = pd.DataFrame(ga4_data)

# 2. Meta Ads Actuals
meta_data = [
    {'Month': 'June 2026', 'Spend_INR': 1552618.67, 'CPA_INR': 276.96, 'Conversions': 5606, 'AOV_INR': 864.26, 'Revenue_INR': 4845031.10, 'ROAS': 3.12},
    {'Month': 'July 2026', 'Spend_INR': 1817362.07, 'CPA_INR': 302.84, 'Conversions': 6001, 'AOV_INR': 857.18, 'Revenue_INR': 5143949.45, 'ROAS': 2.83}
]

df_meta = pd.DataFrame(meta_data)

# 3. Combined Baseline July 2026 (Google + Meta)
combined_july = {
    'Month': 'July 2026 (Google + Meta)',
    'Total_Spend_INR': 4294631.94,
    'Blended_CPA_INR': 324.75,
    'Total_Conversions': 13224.43,
    'Daily_Orders_Avg': 426.59,
    'Total_Revenue_INR': 11746682.90,
    'Blended_ROAS': 2.74
}

df_combined = pd.DataFrame([combined_july])

# 4. Growth Forecast to 1,500 Orders / Day (Plan A vs Plan B)
growth_plans = [
    {
        'Plan': 'Plan A (Higher AOV Efficiency)',
        'Monthly_Spend_INR': 11500000.00,
        'Target_CPA_INR': 255.56,
        'Target_Monthly_Orders': 45000,
        'Target_Daily_Orders': 1500,
        'Target_AOV_INR': 766.67,
        'Target_Monthly_Revenue_INR': 34500000.00,
        'Target_ROAS': 3.00
    },
    {
        'Plan': 'Plan B (Higher Spend Scaling)',
        'Monthly_Spend_INR': 15750000.00,
        'Target_CPA_INR': 350.00,
        'Target_Monthly_Orders': 45000,
        'Target_Daily_Orders': 1500,
        'Target_AOV_INR': 950.00,
        'Target_Monthly_Revenue_INR': 47250000.00,
        'Target_ROAS': 3.00
    }
]

df_plans = pd.DataFrame(growth_plans)

# Save to Excel
with pd.ExcelWriter('reports/fabb6_complete_ga4_and_ads_analytics.xlsx') as writer:
    df_ga4.to_excel(writer, sheet_name='GA4_All_Channels_Actuals', index=False)
    df_meta.to_excel(writer, sheet_name='Meta_Ads_Actuals', index=False)
    df_combined.to_excel(writer, sheet_name='Combined_Baseline_July', index=False)
    df_plans.to_excel(writer, sheet_name='Target_Growth_Plans', index=False)

df_ga4.to_csv('reports/fabb6_ga4_actuals.csv', index=False)

# Chart Generation: Channel Revenue Breakdown in GA4
plt.figure(figsize=(10, 6))
months = ['May 2026', 'June 2026', 'July 2026', 'Aug 2026 (MTD)']
pmax = [65.38, 65.91, 64.90, 45.87]
social = [24.78, 22.00, 19.21, 10.52]
search = [1.98, 2.60, 2.84, 3.50]
direct = [1.43, 1.26, 1.55, 1.21]

x = np.arange(len(months))
width = 0.2

plt.bar(x - 1.5*width, pmax, width, label='Cross-Network (PMax)', color='#4285F4')
plt.bar(x - 0.5*width, social, width, label='Organic Social', color='#34A853')
plt.bar(x + 0.5*width, search, width, label='Organic Search', color='#FBBC04')
plt.bar(x + 1.5*width, direct, width, label='Direct', color='#EA4335')

plt.xlabel('Month', fontsize=12)
plt.ylabel('Revenue (Lakhs INR)', fontsize=12)
plt.title('Fabb6 Google Analytics (GA4) Revenue Breakdown by Channel (May-Aug 2026)', fontsize=13, pad=15)
plt.xticks(x, months)
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()

chart_path = 'reports/fabb6_ga4_channel_revenue.png'
plt.savefig(chart_path, dpi=300)
print("Saved chart to", chart_path)
print("Exported complete Fabb6 GA4 analytics to reports/fabb6_complete_ga4_and_ads_analytics.xlsx")
