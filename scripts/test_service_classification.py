import pandas as pd
import numpy as np

path = r'C:\Users\test\Videos\Office\data\Share Samadhan\All_Enquiry_List_2026.11.23.06.28.18.csv'
df = pd.read_csv(path, low_memory=False)

def classify_service(row):
    noi = str(row['Nature of Investment']).strip().lower()
    src = str(row['Source']).strip().lower()
    c_src = str(row['Campaign Source']).strip().lower()
    c_name = str(row['Campaign Name']).strip().lower()
    ref = str(row['Reference']).strip().lower()
    
    # 1. NRI Specific Landing / Services
    if src == 'nri landing page' or 'nri' in c_name or 'nri' in c_src or 'nri' in ref:
        return 'NRI Samadhan (Global Wealth Recovery)'
    
    # 2. Dematerialization / Physical Shares to Demat
    if 'demat' in noi or 'dematerialization' in c_name or 'physical shares to demat' in noi:
        return 'Physical Shares to Demat'
        
    # 3. Transmission of Shares / Legal Heir
    if 'transmission' in c_src or 'transmission' in c_name or 'transmission' in noi:
        return 'Transmission of Shares (Legal Heir)'
        
    # 4. Duplicate Issue of Shares
    if 'duplicate' in c_src or 'duplicate' in c_name:
        return 'Duplicate Issue of Shares'
        
    # 5. Provident Fund (PF)
    if 'provident' in c_src or 'provident' in c_name or noi == 'pf' or ' pf ' in c_name:
        return 'Provident Fund (PF) Claims'
        
    # 6. Mutual Funds
    if 'mutual' in c_src or 'mutual' in c_name:
        return 'Mutual Funds (SCWF Recovery)'
        
    # 7. Inoperative Bank Deposits / DEAF / NBFC
    if 'bank' in c_src or 'bank' in c_name or 'soft assets' in noi:
        return 'Inoperative Bank Deposits (DEAF)'
        
    # 8. Insurance Claims
    if 'insurance' in c_src or 'insurance' in c_name or 'insurance' in noi:
        return 'Unclaimed Insurance Claims'
        
    # 9. Debtor Recovery / Litigation Funding
    if 'debtor' in c_src or 'litigation' in noi or noi == 'dr':
        return 'Debtor Recovery & Litigation Funding'
        
    # 10. Free IEPF Search & IEPF Claim
    if 'iepf' in noi or 'iepf' in c_src or 'iepf' in c_name or 'iepf' in src:
        return 'IEPF Claim & Free IEPF Search'
        
    # 11. Lost Shares / WhatsApp Lost Share / LostShare.com
    if 'lost share' in src or 'lostshare' in src:
        return 'Lost Shares Recovery (WhatsApp / Web)'
        
    # 12. Shares Recovery / Shares
    if 'shares recovery' in noi or 'recover shares' in c_name:
        return 'Shares Recovery (General)'
        
    if 'shares' in noi:
        return 'Shares (General Portfolio Recovery)'
        
    # 13. Others / Unspecified
    if noi == 'others' or 'others' in c_name:
        return 'Others / General Financial Inquiries'
        
    if src == 'contact us':
        return 'General Inquiries (Contact Us Page)'
        
    if src == 'supervisor panel':
        return 'Supervisor / Telephonic / Associate Inbound'
        
    return 'General / Uncategorized Web Queries'

df['Service_Category'] = df.apply(classify_service, axis=1)
print("=== SERVICE CATEGORY BREAKDOWN ===")
print(df['Service_Category'].value_counts())
print(f"\nTotal: {len(df)}")
