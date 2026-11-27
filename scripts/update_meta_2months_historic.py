import pandas as pd
import os

os.makedirs('reports', exist_ok=True)

# Google Ads Deduplicated with AOV
gads_data = [
    {'Month': 'May 2026', 'Type': 'Historic', 'Ad_Spend_INR': 2136192.16, 'Orders': 1477.36, 'CPA_INR': 1445.95, 'AOV_INR': 840.15, 'Revenue_INR': 1241205.26, 'ROAS': 0.58},
    {'Month': 'June 2026', 'Type': 'Historic', 'Ad_Spend_INR': 2733879.76, 'Orders': 1214.63, 'CPA_INR': 2250.79, 'AOV_INR': 877.18, 'Revenue_INR': 1065444.13, 'ROAS': 0.39},
    {'Month': 'July 2026', 'Type': 'Historic', 'Ad_Spend_INR': 2477269.87, 'Orders': 2260.68, 'CPA_INR': 1095.81, 'AOV_INR': 868.82, 'Revenue_INR': 1964115.15, 'ROAS': 0.79},
    {'Month': 'August 2026 (1-21 MTD)', 'Type': 'Historic', 'Ad_Spend_INR': 2817626.07, 'Orders': 5548.92, 'CPA_INR': 507.78, 'AOV_INR': 931.99, 'Revenue_INR': 5171525.13, 'ROAS': 1.84},
    {'Month': 'Sept 2026', 'Type': 'Forecast', 'Ad_Spend_INR': 3200000.00, 'Orders': 6600.00, 'CPA_INR': 484.85, 'AOV_INR': 939.39, 'Revenue_INR': 6200000.00, 'ROAS': 1.94},
    {'Month': 'Oct 2026 (Festive)', 'Type': 'Forecast', 'Ad_Spend_INR': 3800000.00, 'Orders': 8000.00, 'CPA_INR': 475.00, 'AOV_INR': 950.00, 'Revenue_INR': 7600000.00, 'ROAS': 2.00},
    {'Month': 'Nov 2026 (Peak)', 'Type': 'Forecast', 'Ad_Spend_INR': 4500000.00, 'Orders': 9600.00, 'CPA_INR': 468.75, 'AOV_INR': 958.33, 'Revenue_INR': 9200000.00, 'ROAS': 2.04},
    {'Month': 'Dec 2026 (Year-End)', 'Type': 'Forecast', 'Ad_Spend_INR': 5200000.00, 'Orders': 11200.00, 'CPA_INR': 464.29, 'AOV_INR': 964.29, 'Revenue_INR': 10800000.00, 'ROAS': 2.08},
    {'Month': 'Jan 2027', 'Type': 'Forecast', 'Ad_Spend_INR': 5600000.00, 'Orders': 12200.00, 'CPA_INR': 459.02, 'AOV_INR': 967.21, 'Revenue_INR': 11800000.00, 'ROAS': 2.11},
    {'Month': 'Feb 2027 (Milestone)', 'Type': 'Forecast', 'Ad_Spend_INR': 6000000.00, 'Orders': 13200.00, 'CPA_INR': 454.55, 'AOV_INR': 969.70, 'Revenue_INR': 12800000.00, 'ROAS': 2.13}
]

# Meta Ads with AOV
meta_data = [
    {'Month': 'June 2026', 'Type': 'Historic', 'Ad_Spend_INR': 1552618.67, 'Orders': 5606, 'CPA_INR': 276.96, 'AOV_INR': 864.26, 'Revenue_INR': 4845031.10, 'ROAS': 3.12},
    {'Month': 'July 2026', 'Type': 'Historic', 'Ad_Spend_INR': 1817362.07, 'Orders': 6001, 'CPA_INR': 302.84, 'AOV_INR': 857.18, 'Revenue_INR': 5143949.45, 'ROAS': 2.83},
    {'Month': 'Sept 2026', 'Type': 'Forecast', 'Ad_Spend_INR': 2200000.00, 'Orders': 7000, 'CPA_INR': 314.29, 'AOV_INR': 857.14, 'Revenue_INR': 6000000.00, 'ROAS': 2.73},
    {'Month': 'Oct 2026 (Festive)', 'Type': 'Forecast', 'Ad_Spend_INR': 2600000.00, 'Orders': 8200, 'CPA_INR': 317.07, 'AOV_INR': 865.85, 'Revenue_INR': 7100000.00, 'ROAS': 2.73},
    {'Month': 'Nov 2026 (Peak)', 'Type': 'Forecast', 'Ad_Spend_INR': 3200000.00, 'Orders': 9800, 'CPA_INR': 326.53, 'AOV_INR': 877.55, 'Revenue_INR': 8600000.00, 'ROAS': 2.69},
    {'Month': 'Dec 2026 (Year-End)', 'Type': 'Forecast', 'Ad_Spend_INR': 3800000.00, 'Orders': 11400, 'CPA_INR': 333.33, 'AOV_INR': 885.96, 'Revenue_INR': 10100000.00, 'ROAS': 2.66},
    {'Month': 'Jan 2027', 'Type': 'Forecast', 'Ad_Spend_INR': 4200000.00, 'Orders': 12500, 'CPA_INR': 336.00, 'AOV_INR': 888.00, 'Revenue_INR': 11100000.00, 'ROAS': 2.64},
    {'Month': 'Feb 2027 (Milestone)', 'Type': 'Forecast', 'Ad_Spend_INR': 4500000.00, 'Orders': 13400, 'CPA_INR': 335.82, 'AOV_INR': 895.52, 'Revenue_INR': 12000000.00, 'ROAS': 2.67}
]

df_gads = pd.DataFrame(gads_data)
df_meta = pd.DataFrame(meta_data)

# Export Excel & CSV
with pd.ExcelWriter('reports/fabb6_paid_media_with_aov.xlsx') as writer:
    df_gads.to_excel(writer, sheet_name='Google_Ads_AOV', index=False)
    df_meta.to_excel(writer, sheet_name='Meta_Ads_AOV', index=False)

df_gads.to_csv('reports/fabb6_google_ads_aov.csv', index=False)
df_meta.to_csv('reports/fabb6_meta_ads_aov.csv', index=False)

print("Exported Paid Media tables with AOV Column to Excel and CSV successfully!")
