import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

os.makedirs('reports', exist_ok=True)

# Google Ads Historical + Forecast Data (9 Months total: 3 Months Historic + 6 Months Forecast)
gads_data = [
    {'Month': 'June 2026 (Historic)', 'Type': 'Historic', 'Ad_Spend_INR': 2733879.76, 'Orders': 7085, 'CPA_INR': 385.90, 'Revenue_INR': 6768208.71, 'ROAS': 2.48},
    {'Month': 'July 2026 (Historic)', 'Type': 'Historic', 'Ad_Spend_INR': 2477269.87, 'Orders': 7223, 'CPA_INR': 342.95, 'Revenue_INR': 6602733.45, 'ROAS': 2.67},
    {'Month': 'August 2026 (Historic)', 'Type': 'Historic', 'Ad_Spend_INR': 2637979.00, 'Orders': 9730, 'CPA_INR': 271.12, 'Revenue_INR': 8957928.00, 'ROAS': 3.40},
    {'Month': 'Sept 2026 (Forecast)', 'Type': 'Forecast', 'Ad_Spend_INR': 2800000.00, 'Orders': 7800, 'CPA_INR': 358.97, 'Revenue_INR': 7330000.00, 'ROAS': 2.62},
    {'Month': 'Oct 2026 (Forecast)', 'Type': 'Forecast', 'Ad_Spend_INR': 3300000.00, 'Orders': 9100, 'CPA_INR': 362.64, 'Revenue_INR': 8650000.00, 'ROAS': 2.62},
    {'Month': 'Nov 2026 (Forecast)', 'Type': 'Forecast', 'Ad_Spend_INR': 4000000.00, 'Orders': 10800, 'CPA_INR': 370.37, 'Revenue_INR': 10370000.00, 'ROAS': 2.59},
    {'Month': 'Dec 2026 (Forecast)', 'Type': 'Forecast', 'Ad_Spend_INR': 4800000.00, 'Orders': 12800, 'CPA_INR': 375.00, 'Revenue_INR': 12420000.00, 'ROAS': 2.59},
    {'Month': 'Jan 2027 (Forecast)', 'Type': 'Forecast', 'Ad_Spend_INR': 5200000.00, 'Orders': 13700, 'CPA_INR': 379.56, 'Revenue_INR': 13300000.00, 'ROAS': 2.56},
    {'Month': 'Feb 2027 (Forecast)', 'Type': 'Forecast', 'Ad_Spend_INR': 5600000.00, 'Orders': 14600, 'CPA_INR': 383.56, 'Revenue_INR': 14250000.00, 'ROAS': 2.54}
]

df_gads = pd.DataFrame(gads_data)

# Meta Ads Historical + Forecast Data
meta_data = [
    {'Month': 'June 2026 (Historic)', 'Type': 'Historic', 'Ad_Spend_INR': 1552618.67, 'Orders': 5606, 'CPA_INR': 276.96, 'Revenue_INR': 4845031.10, 'ROAS': 3.12},
    {'Month': 'July 2026 (Historic)', 'Type': 'Historic', 'Ad_Spend_INR': 1817362.07, 'Orders': 6001, 'CPA_INR': 302.84, 'Revenue_INR': 5143949.45, 'ROAS': 2.83},
    {'Month': 'August 2026 (Historic)', 'Type': 'Historic', 'Ad_Spend_INR': 1950000.00, 'Orders': 6300, 'CPA_INR': 309.52, 'Revenue_INR': 5655000.00, 'ROAS': 2.90},
    {'Month': 'Sept 2026 (Forecast)', 'Type': 'Forecast', 'Ad_Spend_INR': 2000000.00, 'Orders': 6450, 'CPA_INR': 310.08, 'Revenue_INR': 5550000.00, 'ROAS': 2.78},
    {'Month': 'Oct 2026 (Forecast)', 'Type': 'Forecast', 'Ad_Spend_INR': 2400000.00, 'Orders': 7600, 'CPA_INR': 315.79, 'Revenue_INR': 6610000.00, 'ROAS': 2.75},
    {'Month': 'Nov 2026 (Forecast)', 'Type': 'Forecast', 'Ad_Spend_INR': 3000000.00, 'Orders': 9300, 'CPA_INR': 322.58, 'Revenue_INR': 8180000.00, 'ROAS': 2.73},
    {'Month': 'Dec 2026 (Forecast)', 'Type': 'Forecast', 'Ad_Spend_INR': 3600000.00, 'Orders': 11000, 'CPA_INR': 327.27, 'Revenue_INR': 9790000.00, 'ROAS': 2.72},
    {'Month': 'Jan 2027 (Forecast)', 'Type': 'Forecast', 'Ad_Spend_INR': 3900000.00, 'Orders': 11800, 'CPA_INR': 330.51, 'Revenue_INR': 10560000.00, 'ROAS': 2.71},
    {'Month': 'Feb 2027 (Forecast)', 'Type': 'Forecast', 'Ad_Spend_INR': 4200000.00, 'Orders': 12600, 'CPA_INR': 333.33, 'Revenue_INR': 11340000.00, 'ROAS': 2.70}
]

df_meta = pd.DataFrame(meta_data)

# Combined Paid Media (Google + Meta) Summary Table
df_combined = pd.DataFrame()
df_combined['Month'] = df_gads['Month']
df_combined['Type'] = df_gads['Type']
df_combined['Total_Ad_Spend_INR'] = df_gads['Ad_Spend_INR'] + df_meta['Ad_Spend_INR']
df_combined['Total_Paid_Orders'] = df_gads['Orders'] + df_meta['Orders']
df_combined['Blended_CPA_INR'] = (df_combined['Total_Ad_Spend_INR'] / df_combined['Total_Paid_Orders']).round(2)
df_combined['Total_Paid_Revenue_INR'] = df_gads['Revenue_INR'] + df_meta['Revenue_INR']
df_combined['Blended_ROAS'] = (df_combined['Total_Paid_Revenue_INR'] / df_combined['Total_Ad_Spend_INR']).round(2)

print("=== GOOGLE ADS HISTORIC + FORECAST ===")
print(df_gads.to_string())

print("\n=== META ADS HISTORIC + FORECAST ===")
print(df_meta.to_string())

print("\n=== COMBINED PAID MEDIA (GOOGLE + META) ===")
print(df_combined.to_string())

# Save to Excel & CSV
with pd.ExcelWriter('reports/fabb6_paid_media_historic_and_forecast.xlsx') as writer:
    df_gads.to_excel(writer, sheet_name='Google_Ads', index=False)
    df_meta.to_excel(writer, sheet_name='Meta_Ads', index=False)
    df_combined.to_excel(writer, sheet_name='Combined_Paid_Media', index=False)

df_gads.to_csv('reports/fabb6_google_ads_budget_plan.csv', index=False)
df_meta.to_csv('reports/fabb6_meta_ads_budget_plan.csv', index=False)

# Chart Generation: Spend vs Revenue for Google Ads & Meta Ads
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Google Ads plot
months_labels = ['Jun 26', 'Jul 26', 'Aug 26', 'Sep 26', 'Oct 26', 'Nov 26', 'Dec 26', 'Jan 27', 'Feb 27']
ax1.plot(months_labels, df_gads['Ad_Spend_INR']/100000, 'o--', color='#EA4335', linewidth=2, label='Google Ad Spend (Lakhs)')
ax1.plot(months_labels, df_gads['Revenue_INR']/100000, 's-', color='#4285F4', linewidth=2.5, label='Google Ads Revenue (Lakhs)')
ax1.set_title('Google Ads Performance Roadmap (Historic + 6M Forecast)', fontsize=12)
ax1.set_ylabel('INR (in Lakhs)')
ax1.legend()
ax1.grid(True, linestyle='--', alpha=0.6)
ax1.tick_params(axis='x', rotation=45)

# Meta Ads plot
ax2.plot(months_labels, df_meta['Ad_Spend_INR']/100000, 'o--', color='#E1306C', linewidth=2, label='Meta Ad Spend (Lakhs)')
ax2.plot(months_labels, df_meta['Revenue_INR']/100000, 's-', color='#34A853', linewidth=2.5, label='Meta Ads Revenue (Lakhs)')
ax2.set_title('Meta Ads Performance Roadmap (Historic + 6M Forecast)', fontsize=12)
ax2.set_ylabel('INR (in Lakhs)')
ax2.legend()
ax2.grid(True, linestyle='--', alpha=0.6)
ax2.tick_params(axis='x', rotation=45)

plt.tight_layout()
chart_path = 'reports/fabb6_paid_media_forecast_chart.png'
plt.savefig(chart_path, dpi=300)
print("Saved chart to", chart_path)
