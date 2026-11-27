import pandas as pd
import numpy as np
import os

input_path = r'C:\Users\test\Videos\Office\data\Share Samadhan\All_Enquiry_List_2026.11.23.06.28.18.csv'
reports_dir = r'C:\Users\test\Videos\Office\reports'
case_studies_dir = r'C:\Users\test\Videos\Office\case-studies\Share Samadhan'

os.makedirs(reports_dir, exist_ok=True)
os.makedirs(case_studies_dir, exist_ok=True)

df = pd.read_csv(input_path, low_memory=False)
print(f"Total Rows Loaded: {len(df):,}")

# 1. Parse Dates
df['Parsed_Date'] = pd.to_datetime(df['Query Date & Time'], format='%d/%m/%Y %I:%M:%p', errors='coerce')
df['YearMonth'] = df['Parsed_Date'].dt.strftime('%Y-%m')
df['Month_Name'] = df['Parsed_Date'].dt.strftime('%B %Y')

# 2. Classify NRI
def check_nri(row):
    if str(row['Source']).strip() == 'NRI Landing Page':
        return True, 'NRI Landing Page'
    
    for col in ['Campaign Name', 'Campaign Source', 'Reference']:
        val = str(row[col]).lower()
        if 'nri' in val:
            return True, f'{col} (NRI tag)'
            
    raw_cc = str(row['Country Code']).strip().replace('+', '')
    if pd.notna(row['Country Code']) and raw_cc not in ['', 'nan', 'none']:
        if raw_cc == '91' or (raw_cc.startswith('91') and len(raw_cc) > 9):
            return False, 'India'
        else:
            return True, f'+{raw_cc}'
            
    city = str(row['City']).strip().lower()
    intl_cities = ['dubai', 'london', 'singapore', 'new york', 'california', 'texas', 'sydney', 'toronto', 'melbourne', 'sharjah', 'abu dhabi', 'doha', 'riyadh', 'kuwait', 'muscat', 'chicago', 'houston', 'fremont', 'new jersey']
    for ic in intl_cities:
        if ic in city:
            return True, f'City: {city}'
            
    return False, 'India'

nri_res = df.apply(check_nri, axis=1)
df['Is_NRI'] = [r[0] for r in nri_res]
df['NRI_Origin'] = [r[1] for r in nri_res]

# 3. Classify Service Category
def classify_service(row):
    noi = str(row['Nature of Investment']).strip().lower()
    src = str(row['Source']).strip().lower()
    c_src = str(row['Campaign Source']).strip().lower()
    c_name = str(row['Campaign Name']).strip().lower()
    ref = str(row['Reference']).strip().lower()
    
    # 1. NRI Samadhan
    if src == 'nri landing page' or 'nri' in c_name or 'nri' in c_src or 'nri' in ref:
        return 'NRI Samadhan'
        
    # 2. Physical Shares to Demat
    if 'demat' in noi or 'dematerialization' in c_name or 'physical shares to demat' in noi:
        return 'Physical Shares to Demat'
        
    # 3. Transmission of Shares (Legal Heir)
    if 'transmission' in c_src or 'transmission' in c_name or 'transmission' in noi:
        return 'Transmission of Shares'
        
    # 4. Duplicate Issue of Shares
    if 'duplicate' in c_src or 'duplicate' in c_name:
        return 'Duplicate Issue of Shares'
        
    # 5. Provident Fund (PF) Claims
    if 'provident' in c_src or 'provident' in c_name or noi == 'pf' or ' pf ' in c_name:
        return 'Provident Fund (PF) Claims'
        
    # 6. Inoperative Bank Deposits (DEAF)
    if 'bank' in c_src or 'bank' in c_name or 'soft assets' in noi:
        return 'Inoperative Bank Deposits (DEAF)'
        
    # 7. Mutual Funds (SCWF)
    if 'mutual' in c_src or 'mutual' in c_name:
        return 'Mutual Funds (SCWF)'
        
    # 8. Unclaimed Insurance
    if 'insurance' in c_src or 'insurance' in c_name or 'insurance' in noi:
        return 'Unclaimed Insurance'
        
    # 9. Debtor Recovery & Litigation Funding
    if 'debtor' in c_src or 'litigation' in noi or noi == 'dr':
        return 'Debtor Recovery & Litigation'
        
    # 10. IEPF Claim & Free IEPF Search
    if 'free iepf search' in noi or 'iepf' in noi or 'iepf' in c_src or 'iepf' in c_name or 'iepf' in src:
        return 'IEPF Claim & Free Search'
        
    # 11. Lost Shares Recovery
    if 'lost share' in src or 'lostshare' in src:
        return 'Lost Shares Recovery (WhatsApp / Web)'
        
    # 12. General Shares Recovery / Portfolio
    if 'shares recovery' in noi or 'recover shares' in c_name:
        return 'Shares Recovery (General)'
        
    if 'shares' in noi:
        return 'Shares (General Portfolio)'
        
    # 13. Others / General Inquiries
    if noi == 'others' or 'others' in c_name:
        return 'Others / General Inquiries'
        
    if src == 'contact us':
        return 'Contact Us Inquiries (General)'
        
    if src == 'supervisor panel':
        return 'Supervisor / Direct Inbound'
        
    return 'Other Web Enquiries'

df['Service_Category'] = df.apply(classify_service, axis=1)

# 4. Classify Lead Source Channel
def classify_channel(row):
    src = str(row['Source']).strip()
    c_src = str(row['Campaign Source']).strip()
    c_name = str(row['Campaign Name']).strip()
    ref = str(row['Reference']).strip()
    
    # Google Ads / Search
    if c_src == 'GoogleAds' or c_name == 'GoogleAds' or ref.startswith('Google'):
        return 'Google Ads / Search'
        
    # Facebook / Meta Ads
    if c_src in ['Facebook', 'MetaAds'] or 'fb -' in c_name or 'ig -' in c_name or 'an - paid' in c_name or 'dematerialization' in c_name or 'Social Media' in ref:
        return 'Facebook / Meta Ads'
        
    # WhatsApp (Anantya & Interakt)
    if 'Anantya.ai' in src or 'WhatsApp' in c_src or 'WhatsApp' in ref or 'interakt' in ref.lower():
        return 'WhatsApp Chatbot (Anantya & Interakt)'
        
    # Contact Us Page
    if src == 'Contact Us':
        return 'Website Contact Us Page'
        
    # Landing Pages
    if src == 'Landing Page':
        return 'Direct / Organic Landing Page'
        
    # Service Pages
    if src == 'Website - Services':
        return 'Website Service Pages'
        
    # NRI Landing Page
    if src == 'NRI Landing Page':
        return 'NRI Landing Page'
        
    # Blog Page
    if src == 'Blog Page':
        return 'Website Blog Page'
        
    # Microsites
    if src in ['www.lostshare.com', 'www.iepfclaim.com']:
        return 'Microsites (LostShare / IEPFClaim)'
        
    # Supervisor Panel / Inbound Calls
    if src == 'Supervisor Panel' or 'Referred by' in ref or '8800' in ref:
        return 'Supervisor Panel / Inbound Calls & Associates'
        
    return 'Direct / Others'

df['Lead_Channel'] = df.apply(classify_channel, axis=1)

print("\nValidation Summary:")
print("YearMonth unique:", df['YearMonth'].unique())
print("Total NRI:", df['Is_NRI'].sum())
print("Total Leads:", len(df))

# ------------------------------------------------------------------------------
# 5. AGGREGATIONS & TABLES
# ------------------------------------------------------------------------------

# Table 1: Master Monthly Summary Table
# Month - No of Leads generated on that month - Top Service Categories - No of NRI Leads - % NRI
monthly_summary = []
for ym in sorted(df['YearMonth'].unique()):
    m_df = df[df['YearMonth'] == ym]
    total_leads = len(m_df)
    nri_leads = m_df['Is_NRI'].sum()
    nri_pct = (nri_leads / total_leads * 100) if total_leads > 0 else 0
    
    # Top 3 services in that month
    top_services = m_df['Service_Category'].value_counts().head(3)
    top_serv_str = ", ".join([f"{k} ({v})" for k, v in top_services.items()])
    
    # Top 2 sources in that month
    top_sources = m_df['Lead_Channel'].value_counts().head(2)
    top_src_str = ", ".join([f"{k} ({v})" for k, v in top_sources.items()])
    
    m_name = m_df['Month_Name'].iloc[0]
    
    monthly_summary.append({
        'Month': ym,
        'Month Name': m_name,
        'Total Leads': total_leads,
        'Top Service Categories (Volume)': top_serv_str,
        'No of NRI Leads': nri_leads,
        'NRI Share %': round(nri_pct, 2),
        'Top Lead Sources': top_src_str
    })

df_monthly_summary = pd.DataFrame(monthly_summary)

# Table 2: Month x Service Category Matrix
pivot_service = pd.crosstab(df['YearMonth'], df['Service_Category'], margins=True, margins_name='Total')

# Table 3: Month x Lead Channel Matrix
pivot_channel = pd.crosstab(df['YearMonth'], df['Lead_Channel'], margins=True, margins_name='Total')

# Table 4: Service Category Summary
service_summary = df.groupby('Service_Category').agg(
    Total_Leads=('Sl.No.', 'count'),
    NRI_Leads=('Is_NRI', 'sum')
).reset_index()
service_summary['Share_%'] = round(service_summary['Total_Leads'] / len(df) * 100, 2)
service_summary['NRI_Share_%'] = round(service_summary['NRI_Leads'] / service_summary['Total_Leads'] * 100, 2)
service_summary = service_summary.sort_values(by='Total_Leads', ascending=False)

# Table 5: Lead Channel Summary
channel_summary = df.groupby('Lead_Channel').agg(
    Total_Leads=('Sl.No.', 'count'),
    NRI_Leads=('Is_NRI', 'sum')
).reset_index()
channel_summary['Share_%'] = round(channel_summary['Total_Leads'] / len(df) * 100, 2)
channel_summary['NRI_Share_%'] = round(channel_summary['NRI_Leads'] / channel_summary['Total_Leads'] * 100, 2)
channel_summary = channel_summary.sort_values(by='Total_Leads', ascending=False)

# Table 6: NRI Country of Origin
nri_df = df[df['Is_NRI']]
nri_country = nri_df['Country Code'].value_counts(dropna=False).head(20).reset_index()
nri_country.columns = ['Country Code', 'Lead Count']

# ------------------------------------------------------------------------------
# 6. EXPORT TO CSV AND EXCEL WORKBOOKS
# ------------------------------------------------------------------------------

# Excel workbook with multiple tabs
excel_path_reports = os.path.join(reports_dir, 'Share_Samadhan_Annual_Leads_Analysis_Nov2025_Nov2026.xlsx')
excel_path_casestudies = os.path.join(case_studies_dir, 'Share_Samadhan_Annual_Leads_Analysis_Nov2025_Nov2026.xlsx')

for target_excel in [excel_path_reports, excel_path_casestudies]:
    with pd.ExcelWriter(target_excel, engine='openpyxl') as writer:
        df_monthly_summary.to_excel(writer, sheet_name='Monthly_Summary', index=False)
        pivot_service.to_excel(writer, sheet_name='Month_x_Service_Matrix')
        pivot_channel.to_excel(writer, sheet_name='Month_x_Source_Matrix')
        service_summary.to_excel(writer, sheet_name='Service_Category_Totals', index=False)
        channel_summary.to_excel(writer, sheet_name='Lead_Source_Totals', index=False)
        nri_country.to_excel(writer, sheet_name='NRI_Country_Distribution', index=False)

# CSV exports
df_monthly_summary.to_csv(os.path.join(reports_dir, 'Share_Samadhan_Monthly_Leads_Summary.csv'), index=False)
pivot_service.to_csv(os.path.join(reports_dir, 'Share_Samadhan_Monthly_Service_Matrix.csv'))
pivot_channel.to_csv(os.path.join(reports_dir, 'Share_Samadhan_Monthly_Source_Matrix.csv'))
service_summary.to_csv(os.path.join(reports_dir, 'Share_Samadhan_Service_Summary.csv'), index=False)
channel_summary.to_csv(os.path.join(reports_dir, 'Share_Samadhan_Source_Summary.csv'), index=False)

print(f"Exported Excel Workbook to: {excel_path_reports}")
print(f"Exported Excel Workbook to: {excel_path_casestudies}")
print("SUCCESS!")
