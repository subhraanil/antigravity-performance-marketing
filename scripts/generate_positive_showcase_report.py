import pandas as pd
import numpy as np
import openpyxl
import os

base_dir = r'C:/Users/test/Videos/Office/data/Share Samadhan'
reports_dir = r'C:/Users/test/Videos/Office/reports'
case_studies_dir = r'C:/Users/test/Videos/Office/case-studies/Share Samadhan'

os.makedirs(reports_dir, exist_ok=True)
os.makedirs(case_studies_dir, exist_ok=True)

# 1. Load Share Samadhan - Nov 2025 to Nov 2026.xlsx
f_cost = os.path.join(base_dir, 'Share Samadhan - Nov 2025 to Nov 2026.xlsx')
xl = pd.ExcelFile(f_cost)

# Paid Cost Leads
df_raw_cost = xl.parse('Total CostLeads', skiprows=1)
# Clean columns
paid_cols = [
    'Month', 'Google_Impressions', 'Google_Clicks', 'Google_Leads', 'Google_Spend', 'Google_CPL',
    'Meta_Impressions', 'Meta_Clicks', 'Meta_Leads', 'Meta_Spend', 'Meta_CPL',
    'Total_Impressions', 'Total_Clicks', 'Total_Paid_Leads', 'Total_Paid_Spend', 'Blended_CPL'
]
df_paid = df_raw_cost.iloc[:13, :16].copy()
df_paid.columns = paid_cols
df_paid['Month_Label'] = pd.to_datetime(df_paid['Month']).dt.strftime('%b %Y')
df_paid['YearMonth'] = pd.to_datetime(df_paid['Month']).dt.strftime('%Y-%m')

# GA4 Traffic Report
df_raw_ga = xl.parse('Google Analytics Traffic Report')
df_ga = df_raw_ga.iloc[:13].copy()
df_ga['Month_Label'] = pd.to_datetime(df_ga['Months']).dt.strftime('%b %Y')
df_ga['YearMonth'] = pd.to_datetime(df_ga['Months']).dt.strftime('%Y-%m')

# 2. Compute Growth Metrics & Highlights
# Baseline (Nov 2025) vs Peak / Best Month
nov25_leads = df_paid.loc[0, 'Total_Paid_Leads']
nov25_cpl = df_paid.loc[0, 'Blended_CPL']
nov25_meta_cpl = df_paid.loc[0, 'Meta_CPL']
nov25_google_leads = df_paid.loc[0, 'Google_Leads']
nov25_meta_leads = df_paid.loc[0, 'Meta_Leads']

peak_leads_row = df_paid.loc[df_paid['Total_Paid_Leads'].idxmax()]
best_cpl_row = df_paid.loc[df_paid['Blended_CPL'].idxmin()]
best_meta_cpl_row = df_paid.loc[df_paid['Meta_CPL'].idxmin()]

total_paid_leads = df_paid['Total_Paid_Leads'].sum()
total_paid_spend = df_paid['Total_Paid_Spend'].sum()
total_google_leads = df_paid['Google_Leads'].sum()
total_google_spend = df_paid['Google_Spend'].sum()
total_meta_leads = df_paid['Meta_Leads'].sum()
total_meta_spend = df_paid['Meta_Spend'].sum()

total_users = df_ga['Total User'].sum()
total_new_users = df_ga['New User'].sum()
total_returning_users = df_ga['Return User'].sum()
total_organic_traffic = df_ga['Organic Traffic'].sum()
total_organic_leads = df_ga['Organic Leads'].sum()

overall_paid_cpl = total_paid_spend / total_paid_leads
overall_google_cpl = total_google_spend / total_google_leads
overall_meta_cpl = total_meta_spend / total_meta_leads

lead_growth_pct = ((peak_leads_row['Total_Paid_Leads'] - nov25_leads) / nov25_leads) * 100
cpl_reduction_pct = ((nov25_cpl - best_cpl_row['Blended_CPL']) / nov25_cpl) * 100
meta_cpl_reduction_pct = ((df_paid.loc[1, 'Meta_CPL'] - best_meta_cpl_row['Meta_CPL']) / df_paid.loc[1, 'Meta_CPL']) * 100

print(f"Total Paid Leads: {total_paid_leads:,.0f}")
print(f"Total Paid Spend: INR {total_paid_spend:,.2f}")
print(f"Blended Paid CPL: INR {overall_paid_cpl:.2f}")
print(f"Peak Monthly Paid Leads: {peak_leads_row['Total_Paid_Leads']} ({peak_leads_row['Month_Label']}) -> +{lead_growth_pct:.1f}% growth")
print(f"Best Blended CPL: INR {best_cpl_row['Blended_CPL']:.2f} ({best_cpl_row['Month_Label']}) -> -{cpl_reduction_pct:.1f}% reduction")
print(f"Best Meta CPL: INR {best_meta_cpl_row['Meta_CPL']:.2f} ({best_meta_cpl_row['Month_Label']}) -> -{meta_cpl_reduction_pct:.1f}% reduction")
print(f"Total Organic Users: {total_users:,.0f} | Organic Leads: {total_organic_leads:,.0f}")

# 3. Save Clean Positive Metrics Excel Workbook
excel_out_reports = os.path.join(reports_dir, 'Share_Samadhan_Positive_Performance_Metrics.xlsx')
excel_out_cases = os.path.join(case_studies_dir, 'Share_Samadhan_Positive_Performance_Metrics.xlsx')

for target in [excel_out_reports, excel_out_cases]:
    with pd.ExcelWriter(target, engine='openpyxl') as writer:
        df_paid.to_excel(writer, sheet_name='Paid_Media_Growth', index=False)
        df_ga.to_excel(writer, sheet_name='GA4_Organic_Growth', index=False)

print("Saved Excel metrics to Office reports and case-studies.")
