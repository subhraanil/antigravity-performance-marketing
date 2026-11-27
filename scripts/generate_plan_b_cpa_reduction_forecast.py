import pandas as pd
import openpyxl
import os

out_dir = 'reports'
os.makedirs(out_dir, exist_ok=True)

# 1. Plan B Multi-Channel Channel Sales Forecast Table
plan_b_channel_data = [
    {
        'Month': "Sept 2026",
        'Total_Ads_Spend_INR': 4500000.0,
        'Sales_from_Ads_Only_INR': 13252000.0,
        'Paid_Sales_Share': '77.2%',
        'Google_Ads_Sales_INR': 6392000.0,
        'Google_Ads_Share': '37.2%',
        'Google_Orders': 6800,
        'Meta_Ads_Sales_INR': 6860000.0,
        'Meta_Ads_Share': '39.9%',
        'Meta_Orders': 7800,
        'Organic_Sales_INR': 2250000.0,
        'Organic_Share': '13.1%',
        'Organic_Orders': 2500,
        'Return_Customer_Sales_INR': 1672000.0,
        'Return_Customer_Share': '9.7%',
        'Return_Orders': 1900,
        'Total_Monthly_Sales_INR': 17174000.0,
        'Total_Orders': 19000,
        'Daily_Avg_Orders': 633,
        'Blended_Paid_CPA_INR': 308.22,
        'Overall_ROAS': 3.82
    },
    {
        'Month': "Oct 2026 (Festive)",
        'Total_Ads_Spend_INR': 5200000.0,
        'Sales_from_Ads_Only_INR': 16577000.0,
        'Paid_Sales_Share': '73.4%',
        'Google_Ads_Sales_INR': 7410000.0,
        'Google_Ads_Share': '32.8%',
        'Google_Orders': 7800,
        'Meta_Ads_Sales_INR': 9167000.0,
        'Meta_Ads_Share': '40.6%',
        'Meta_Orders': 10300,
        'Organic_Sales_INR': 2700000.0,
        'Organic_Share': '12.0%',
        'Organic_Orders': 3000,
        'Return_Customer_Sales_INR': 3298000.0,
        'Return_Customer_Share': '14.6%',
        'Return_Orders': 3400,
        'Total_Monthly_Sales_INR': 22575000.0,
        'Total_Orders': 24500,
        'Daily_Avg_Orders': 790,
        'Blended_Paid_CPA_INR': 287.29,
        'Overall_ROAS': 4.34
    },
    {
        'Month': "Nov 2026 (Peak)",
        'Total_Ads_Spend_INR': 6000000.0,
        'Sales_from_Ads_Only_INR': 19992000.0,
        'Paid_Sales_Share': '71.8%',
        'Google_Ads_Sales_INR': 8832000.0,
        'Google_Ads_Share': '31.7%',
        'Google_Orders': 9200,
        'Meta_Ads_Sales_INR': 11160000.0,
        'Meta_Ads_Share': '40.1%',
        'Meta_Orders': 12400,
        'Organic_Sales_INR': 3496000.0,
        'Organic_Share': '12.6%',
        'Organic_Orders': 3800,
        'Return_Customer_Sales_INR': 4368000.0,
        'Return_Customer_Share': '15.7%',
        'Return_Orders': 4800,
        'Total_Monthly_Sales_INR': 27856000.0,
        'Total_Orders': 30200,
        'Daily_Avg_Orders': 1007,
        'Blended_Paid_CPA_INR': 277.78,
        'Overall_ROAS': 4.64
    },
    {
        'Month': "Dec 2026 (Year-End)",
        'Total_Ads_Spend_INR': 6800000.0,
        'Sales_from_Ads_Only_INR': 23483000.0,
        'Paid_Sales_Share': '69.9%',
        'Google_Ads_Sales_INR': 10379000.0,
        'Google_Ads_Share': '30.9%',
        'Google_Orders': 10700,
        'Meta_Ads_Sales_INR': 13104000.0,
        'Meta_Ads_Share': '39.0%',
        'Meta_Orders': 14400,
        'Organic_Sales_INR': 4464000.0,
        'Organic_Share': '13.3%',
        'Organic_Orders': 4800,
        'Return_Customer_Sales_INR': 5642000.0,
        'Return_Customer_Share': '16.8%',
        'Return_Orders': 6200,
        'Total_Monthly_Sales_INR': 33589000.0,
        'Total_Orders': 36100,
        'Daily_Avg_Orders': 1165,
        'Blended_Paid_CPA_INR': 270.92,
        'Overall_ROAS': 4.94
    },
    {
        'Month': "Jan 2027",
        'Total_Ads_Spend_INR': 7500000.0,
        'Sales_from_Ads_Only_INR': 26676000.0,
        'Paid_Sales_Share': '68.6%',
        'Google_Ads_Sales_INR': 11956000.0,
        'Google_Ads_Share': '30.7%',
        'Google_Orders': 12200,
        'Meta_Ads_Sales_INR': 14720000.0,
        'Meta_Ads_Share': '37.8%',
        'Meta_Orders': 16000,
        'Organic_Sales_INR': 5170000.0,
        'Organic_Share': '13.3%',
        'Organic_Orders': 5500,
        'Return_Customer_Sales_INR': 7050000.0,
        'Return_Customer_Share': '18.1%',
        'Return_Orders': 7500,
        'Total_Monthly_Sales_INR': 38896000.0,
        'Total_Orders': 41200,
        'Daily_Avg_Orders': 1329,
        'Blended_Paid_CPA_INR': 265.96,
        'Overall_ROAS': 5.19
    },
    {
        'Month': "Feb 2027 (Milestone)",
        'Total_Ads_Spend_INR': 8200000.0,
        'Sales_from_Ads_Only_INR': 30129000.0,
        'Paid_Sales_Share': '67.2%',
        'Google_Ads_Sales_INR': 13761000.0,
        'Google_Ads_Share': '30.7%',
        'Google_Orders': 13900,
        'Meta_Ads_Sales_INR': 16368000.0,
        'Meta_Ads_Share': '36.5%',
        'Meta_Orders': 17600,
        'Organic_Sales_INR': 5890000.0,
        'Organic_Share': '13.1%',
        'Organic_Orders': 6200,
        'Return_Customer_Sales_INR': 8820000.0,
        'Return_Customer_Share': '19.7%',
        'Return_Orders': 9000,
        'Total_Monthly_Sales_INR': 44839000.0,
        'Total_Orders': 46700,
        'Daily_Avg_Orders': 1557,
        'Blended_Paid_CPA_INR': 260.32,
        'Overall_ROAS': 5.47
    }
]

df_plan_b_channel = pd.DataFrame(plan_b_channel_data)

# 2. Plan B Google Ads Table with Campaign Segmentation
plan_b_gads_data = [
    {'Month': 'May 2026 (Historic)', 'Type': 'Historic', 'Spend_INR': 2136192.16, 'Orders': 1477.36, 'Blended_CPA': 1445.95, 'AOV': 840.15, 'Revenue': 1241205.26, 'ROAS': 0.58},
    {'Month': 'June 2026 (Historic)', 'Type': 'Historic', 'Spend_INR': 2733879.76, 'Orders': 1214.63, 'Blended_CPA': 2250.79, 'AOV': 877.18, 'Revenue': 1065444.13, 'ROAS': 0.39},
    {'Month': 'July 2026 (Historic)', 'Type': 'Historic', 'Spend_INR': 2477269.87, 'Orders': 2260.68, 'Blended_CPA': 1095.81, 'AOV': 868.82, 'Revenue': 1964115.15, 'ROAS': 0.79},
    {'Month': 'August 2026 (1-21 MTD)', 'Type': 'Historic', 'Spend_INR': 2817626.07, 'Orders': 5548.92, 'Blended_CPA': 507.78, 'AOV': 931.99, 'Revenue': 5171525.13, 'ROAS': 1.84},
    {'Month': 'Sept 2026', 'Type': 'Forecast', 'Spend_INR': 2500000.0, 'New_Orders': 2500, 'New_CPA': 700.0, 'Remk_Orders': 1500, 'Remk_CPA': 280.0, 'Reorder_Orders': 2800, 'Reorder_CPA': 118.0, 'Total_Orders': 6800, 'Blended_CPA': 367.65, 'AOV': 940.0, 'Revenue': 6392000.0, 'ROAS': 2.56},
    {'Month': 'Oct 2026 (Festive)', 'Type': 'Forecast', 'Spend_INR': 2800000.0, 'New_Orders': 2800, 'New_CPA': 690.0, 'Remk_Orders': 1900, 'Remk_CPA': 270.0, 'Reorder_Orders': 3100, 'Reorder_CPA': 114.0, 'Total_Orders': 7800, 'Blended_CPA': 358.97, 'AOV': 950.0, 'Revenue': 7410000.0, 'ROAS': 2.65},
    {'Month': 'Nov 2026 (Peak)', 'Type': 'Forecast', 'Spend_INR': 3200000.0, 'New_Orders': 3200, 'New_CPA': 680.0, 'Remk_Orders': 2400, 'Remk_CPA': 260.0, 'Reorder_Orders': 3600, 'Reorder_CPA': 111.0, 'Total_Orders': 9200, 'Blended_CPA': 347.83, 'AOV': 960.0, 'Revenue': 8832000.0, 'ROAS': 2.76},
    {'Month': 'Dec 2026 (Year-End)', 'Type': 'Forecast', 'Spend_INR': 3600000.0, 'New_Orders': 3600, 'New_CPA': 670.0, 'Remk_Orders': 2900, 'Remk_CPA': 250.0, 'Reorder_Orders': 4200, 'Reorder_CPA': 108.0, 'Total_Orders': 10700, 'Blended_CPA': 336.45, 'AOV': 970.0, 'Revenue': 10379000.0, 'ROAS': 2.88},
    {'Month': 'Jan 2027', 'Type': 'Forecast', 'Spend_INR': 4000000.0, 'New_Orders': 4000, 'New_CPA': 660.0, 'Remk_Orders': 3400, 'Remk_CPA': 245.0, 'Reorder_Orders': 4800, 'Reorder_CPA': 105.0, 'Total_Orders': 12200, 'Blended_CPA': 327.87, 'AOV': 980.0, 'Revenue': 11956000.0, 'ROAS': 2.99},
    {'Month': 'Feb 2027 (Milestone)', 'Type': 'Forecast', 'Spend_INR': 4400000.0, 'New_Orders': 4400, 'New_CPA': 650.0, 'Remk_Orders': 4000, 'Remk_CPA': 240.0, 'Reorder_Orders': 5500, 'Reorder_CPA': 102.0, 'Total_Orders': 13900, 'Blended_CPA': 316.55, 'AOV': 990.0, 'Revenue': 13761000.0, 'ROAS': 3.13}
]

df_plan_b_gads = pd.DataFrame(plan_b_gads_data)

# 3. Plan B Meta Ads Table with Campaign Segmentation
plan_b_meta_data = [
    {'Month': 'June 2026 (Historic)', 'Type': 'Historic', 'Spend_INR': 1552618.67, 'Orders': 5606, 'Blended_CPA': 276.96, 'AOV': 864.26, 'Revenue': 4845031.10, 'ROAS': 3.12},
    {'Month': 'July 2026 (Historic)', 'Type': 'Historic', 'Spend_INR': 1817362.07, 'Orders': 6001, 'Blended_CPA': 302.84, 'AOV': 857.18, 'Revenue': 5143949.45, 'ROAS': 2.83},
    {'Month': 'Sept 2026', 'Type': 'Forecast', 'Spend_INR': 2000000.0, 'New_Orders': 3500, 'New_CPA': 400.0, 'Remk_Orders': 1800, 'Remk_CPA': 180.0, 'Reorder_Orders': 2500, 'Reorder_CPA': 90.0, 'Total_Orders': 7800, 'Blended_CPA': 256.41, 'AOV': 879.49, 'Revenue': 6860000.0, 'ROAS': 3.43},
    {'Month': 'Oct 2026 (Festive)', 'Type': 'Forecast', 'Spend_INR': 2400000.0, 'New_Orders': 4000, 'New_CPA': 400.0, 'Remk_Orders': 2500, 'Remk_CPA': 175.0, 'Reorder_Orders': 3800, 'Reorder_CPA': 88.0, 'Total_Orders': 10300, 'Blended_CPA': 233.01, 'AOV': 890.0, 'Revenue': 9167000.0, 'ROAS': 3.82},
    {'Month': 'Nov 2026 (Peak)', 'Type': 'Forecast', 'Spend_INR': 2800000.0, 'New_Orders': 4600, 'New_CPA': 405.0, 'Remk_Orders': 3200, 'Remk_CPA': 170.0, 'Reorder_Orders': 4600, 'Reorder_CPA': 85.0, 'Total_Orders': 12400, 'Blended_CPA': 225.81, 'AOV': 900.0, 'Revenue': 11160000.0, 'ROAS': 3.99},
    {'Month': 'Dec 2026 (Year-End)', 'Type': 'Forecast', 'Spend_INR': 3200000.0, 'New_Orders': 5200, 'New_CPA': 410.0, 'Remk_Orders': 3800, 'Remk_CPA': 165.0, 'Reorder_Orders': 5400, 'Reorder_CPA': 82.0, 'Total_Orders': 14400, 'Blended_CPA': 222.22, 'AOV': 910.0, 'Revenue': 13104000.0, 'ROAS': 4.10},
    {'Month': 'Jan 2027', 'Type': 'Forecast', 'Spend_INR': 3500000.0, 'New_Orders': 5600, 'New_CPA': 415.0, 'Remk_Orders': 4200, 'Remk_CPA': 160.0, 'Reorder_Orders': 6200, 'Reorder_CPA': 80.0, 'Total_Orders': 16000, 'Blended_CPA': 218.75, 'AOV': 920.0, 'Revenue': 14720000.0, 'ROAS': 4.21},
    {'Month': 'Feb 2027 (Milestone)', 'Type': 'Forecast', 'Spend_INR': 3800000.0, 'New_Orders': 6000, 'New_CPA': 420.0, 'Remk_Orders': 4600, 'Remk_CPA': 160.0, 'Reorder_Orders': 7000, 'Reorder_CPA': 78.0, 'Total_Orders': 17600, 'Blended_CPA': 215.91, 'AOV': 930.0, 'Revenue': 16368000.0, 'ROAS': 4.31}
]

df_plan_b_meta = pd.DataFrame(plan_b_meta_data)

# Export Excel
excel_path = os.path.join(out_dir, 'FABB6_Plan_B_CPA_Reduction_Forecast_Model.xlsx')
with pd.ExcelWriter(excel_path) as writer:
    df_plan_b_channel.to_excel(writer, sheet_name='Plan_B_Channel_Forecast', index=False)
    df_plan_b_gads.to_excel(writer, sheet_name='Plan_B_Google_Ads', index=False)
    df_plan_b_meta.to_excel(writer, sheet_name='Plan_B_Meta_Ads', index=False)

print(f"Generated Plan B CPA Reduction Forecast Excel workbook at {excel_path}")
