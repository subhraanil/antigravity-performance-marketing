import json
import pandas as pd
import os

with open('data/dashboard_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

os.makedirs('reports', exist_ok=True)

# 1. KPIs Summary DataFrame
kpi_df = pd.DataFrame([data['kpis']]).T.reset_index()
kpi_df.columns = ['Metric', 'Value']

# 2. Monthly Revenue & Acquisition DataFrame
monthly_rev = pd.DataFrame(list(data['monthly_revenue'].items()), columns=['Month', 'Revenue_INR'])
monthly_acq = pd.DataFrame(list(data['monthly_acquisitions'].items()), columns=['Month', 'New_User_Acquisitions'])
monthly_df = pd.merge(monthly_acq, monthly_rev, on='Month', how='outer').sort_values('Month')

# 3. City Stats DataFrame
city_df = pd.DataFrame(data['city_stats'])

# 4. Pincode Stats DataFrame
pincode_df = pd.DataFrame(data['pincode_stats'])

# Save to Excel / CSVs
with pd.ExcelWriter('reports/fabb6_google_analytics_extracted.xlsx') as writer:
    kpi_df.to_excel(writer, sheet_name='Core_KPIs', index=False)
    monthly_df.to_excel(writer, sheet_name='Monthly_Performance', index=False)
    city_df.to_excel(writer, sheet_name='Top_Cities', index=False)
    pincode_df.to_excel(writer, sheet_name='Top_Pincodes', index=False)

monthly_df.to_csv('reports/fabb6_monthly_analytics.csv', index=False)
city_df.to_csv('reports/fabb6_city_analytics.csv', index=False)
pincode_df.to_csv('reports/fabb6_pincode_analytics.csv', index=False)

print("Exported Google Analytics data successfully to reports/fabb6_google_analytics_extracted.xlsx!")
