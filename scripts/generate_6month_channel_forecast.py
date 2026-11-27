import pandas as pd
import os

os.makedirs('reports', exist_ok=True)

# Complete 6-Month Forecast Data with Percentage Share Contribution
forecast_data = [
    {
        'Month': 'Sept 2026',
        'Google_Ads_Sales_INR': 6200000.0,
        'Google_Ads_Share': '32.2%',
        'Meta_Ads_Sales_INR': 6000000.0,
        'Meta_Ads_Share': '31.2%',
        'Organic_Sales_INR': 3230000.0,
        'Organic_Share': '16.8%',
        'Return_Customer_Sales_INR': 3800000.0,
        'Return_Customer_Share': '19.8%',
        'Total_Monthly_Sales_INR': 19230000.0,
        'Total_Orders': 21450,
        'Daily_Orders_Avg': 715
    },
    {
        'Month': 'Oct 2026 (Festive)',
        'Google_Ads_Sales_INR': 7600000.0,
        'Google_Ads_Share': '33.0%',
        'Meta_Ads_Sales_INR': 7100000.0,
        'Meta_Ads_Share': '30.8%',
        'Organic_Sales_INR': 3610000.0,
        'Organic_Share': '15.7%',
        'Return_Customer_Sales_INR': 4750000.0,
        'Return_Customer_Share': '20.6%',
        'Total_Monthly_Sales_INR': 23060000.0,
        'Total_Orders': 25400,
        'Daily_Orders_Avg': 820
    },
    {
        'Month': 'Nov 2026 (Peak Festive)',
        'Google_Ads_Sales_INR': 9200000.0,
        'Google_Ads_Share': '32.5%',
        'Meta_Ads_Sales_INR': 8600000.0,
        'Meta_Ads_Share': '30.3%',
        'Organic_Sales_INR': 4450000.0,
        'Organic_Share': '15.7%',
        'Return_Customer_Sales_INR': 6100000.0,
        'Return_Customer_Share': '21.5%',
        'Total_Monthly_Sales_INR': 28350000.0,
        'Total_Orders': 31000,
        'Daily_Orders_Avg': 1033
    },
    {
        'Month': 'Dec 2026 (Year-End)',
        'Google_Ads_Sales_INR': 10800000.0,
        'Google_Ads_Share': '31.2%',
        'Meta_Ads_Sales_INR': 10100000.0,
        'Meta_Ads_Share': '29.2%',
        'Organic_Sales_INR': 5760000.0,
        'Organic_Share': '16.7%',
        'Return_Customer_Sales_INR': 7900000.0,
        'Return_Customer_Share': '22.9%',
        'Total_Monthly_Sales_INR': 34560000.0,
        'Total_Orders': 37500,
        'Daily_Orders_Avg': 1210
    },
    {
        'Month': 'Jan 2027',
        'Google_Ads_Sales_INR': 11800000.0,
        'Google_Ads_Share': '30.8%',
        'Meta_Ads_Sales_INR': 11100000.0,
        'Meta_Ads_Share': '29.0%',
        'Organic_Sales_INR': 6060000.0,
        'Organic_Share': '15.8%',
        'Return_Customer_Sales_INR': 9300000.0,
        'Return_Customer_Share': '24.3%',
        'Total_Monthly_Sales_INR': 38260000.0,
        'Total_Orders': 41400,
        'Daily_Orders_Avg': 1335
    },
    {
        'Month': 'Feb 2027 (Milestone)',
        'Google_Ads_Sales_INR': 12800000.0,
        'Google_Ads_Share': '30.5%',
        'Meta_Ads_Sales_INR': 12000000.0,
        'Meta_Ads_Share': '28.6%',
        'Organic_Sales_INR': 6590000.0,
        'Organic_Share': '15.7%',
        'Return_Customer_Sales_INR': 10610000.0,
        'Return_Customer_Share': '25.3%',
        'Total_Monthly_Sales_INR': 42000000.0,
        'Total_Orders': 45000,
        'Daily_Orders_Avg': 1500
    }
]

df = pd.DataFrame(forecast_data)

# Export Excel & CSV
with pd.ExcelWriter('reports/fabb6_6month_channel_forecast_with_percentages.xlsx') as writer:
    df.to_excel(writer, sheet_name='6_Month_Channel_Forecast', index=False)

df.to_csv('reports/fabb6_6month_channel_forecast_with_percentages.csv', index=False)

print("Exported 6-Month Channel Forecast with % Share Contribution successfully!")
