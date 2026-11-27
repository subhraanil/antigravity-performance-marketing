import pandas as pd
import numpy as np
import re

path = r'data\Share Samadhan\Search terms report.xlsx'
df = pd.read_excel(path, skiprows=2)
df_terms = df.iloc[:-3].copy()

numeric_cols = ['Clicks', 'Impr.', 'CTR', 'Avg. CPC', 'Cost', 'Conv. rate', 'Conversions', 'Cost / conv.']
for col in numeric_cols:
    df_terms[col] = pd.to_numeric(df_terms[col], errors='coerce').fillna(0)

def categorize(term):
    t = str(term).lower().strip()
    
    # 1. Brand (Share Samadhan)
    if any(k in t for k in ['share samadhan', 'sharesamadhan', 'wealth samadhan', 'nyay samadhan']):
        return 'Brand (Share Samadhan)'
    
    # 2. IEPF - Government Portal / Login / Navigational
    # Check if contains iepf/iepfa AND navigational words
    is_iepf = bool(re.search(r'\biepfa?\b', t)) or 'iepf' in t
    
    if is_iepf:
        if any(k in t for k in ['login', 'portal', 'gov', 'website', 'link', 'official', 'status', 'form', 'authority', 'track', 'challan', 'srn', 'cin', 'helpdesk', 'toll free', 'contact']):
            return 'IEPF: Govt Portal / Login / Forms (Navigational)'
        elif any(k in t for k in ['consultant', 'agent', 'service', 'advisor', 'company', 'agency', 'expert', 'lawyer', 'help', 'process', 'procedure', 'how to', 'claim', 'refund', 'recovery', 'recover']):
            return 'IEPF: Commercial / Intent to Recover / Consult'
        else:
            return 'IEPF: Head Keywords (iepf, iepfa, unclaimed shares)'
    
    # 3. PACL / Sahara / Chit Funds (Scam / Non-serviceable Waste)
    if any(k in t for k in ['pacl', 'sebipacl', 'sahara', 'chit fund', 'ponzi', 'pearls', 'pearll']):
        return 'PACL / Sahara / Chit Fund Inquiries (Junk / Waste)'
    
    # 4. Duplicate / Lost Shares / Demat conversion / KYC
    if any(k in t for k in ['duplicate', 'lost share', 'lost certificate', 'physical share', 'demat', 'loc', 'letter of confirmation', 'isr-1', 'isr-2', 'isr-4', 'signature mismatch', 'kyc']):
        return 'Duplicate Shares / Demat / Lost Certificates'
    
    # 5. Transmission / Legal Heir / Deceased Holder
    if any(k in t for k in ['transmission', 'deceased', 'death', 'legal heir', 'succession', 'probate', 'will', 'nominee', 'nomination', 'surviving']):
        return 'Transmission / Legal Heir / Inheritance'
    
    # 6. Unclaimed Assets / General Wealth Recovery (Non-IEPF branded)
    if any(k in t for k in ['unclaimed asset', 'unclaimed investment', 'unclaimed money', 'lost investment', 'recover shares', 'unclaimed dividend', 'old share', 'forgotten share', 'unclaimed property']):
        return 'General Unclaimed Assets & Wealth Recovery'
    
    # 7. Banking / Deposits / UDGAM / DEAF
    if any(k in t for k in ['udgam', 'rbi', 'bank deposit', 'unclaimed deposit', 'deaf', 'fixed deposit', 'saving account', 'dormant account', 'inoperative']):
        return 'Bank Deposits / UDGAM / DEAF'
    
    # 8. True EPF / EPFO / Provident Fund (excluding IEPF)
    if any(k in t for k in ['epfo', 'provident fund', 'uan', 'epfigms', 'pension', 'pf balance', 'pf withdrawal', 'pf claim']) or re.search(r'\bepf\b', t) or re.search(r'\bpf\b', t):
        return 'PF / EPFO / Pension Services'
    
    # 9. Insurance & Policy Claims
    if any(k in t for k in ['insurance', 'lic', 'policy', 'policyholder']):
        return 'Insurance & Policy Claims'
    
    # 10. Mutual Funds / SCWF
    if any(k in t for k in ['mutual fund', 'scwf', 'cams', 'kfintech', 'amfi']):
        return 'Mutual Funds (SCWF)'
    
    # 11. Debtors / MSME / Legal Recovery
    if any(k in t for k in ['debtor', 'msme', 'litigation', 'court', 'dispute', 'recovery agent']):
        return 'Debtors / MSME / Legal Dispute'
    
    # 12. Trading / Stock Broking / Market / Tips
    if any(k in t for k in ['trading', 'trader', 'intraday', 'zerodha', 'groww', 'upstox', 'angel', 'demat account open', 'broker', 'nifty', 'sensex', 'stock market', 'share market', 'ipo', 'share price', 'share holding']):
        return 'Trading / Stock Broking / Retail Market (Unqualified)'
    
    # 13. Government Schemes / Welfare / Miscellaneous Govt (PFMS, PM schemes, etc.)
    if any(k in t for k in ['scheme', 'yojana', 'pfms', 'ration', 'ayushman', 'pmkisan', 'kisan']):
        return 'Govt Welfare Schemes / PFMS (Irrelevant Waste)'
    
    return 'Other Unclassified / Long-tail'

df_terms['Category'] = df_terms['Search term'].apply(categorize)

cat_summary = df_terms.groupby('Category').agg(
    terms=('Search term', 'count'),
    clicks=('Clicks', 'sum'),
    cost=('Cost', 'sum'),
    conversions=('Conversions', 'sum')
).reset_index()

total_cost = df_terms['Cost'].sum()
total_conv = df_terms['Conversions'].sum()

cat_summary['Spend_Share_%'] = cat_summary['cost'] / total_cost * 100
cat_summary['Conv_Share_%'] = cat_summary['conversions'] / total_conv * 100
cat_summary['CPC'] = cat_summary['cost'] / cat_summary['clicks']
cat_summary['CPA'] = cat_summary['cost'] / cat_summary['conversions']
cat_summary['CVR_%'] = cat_summary['conversions'] / cat_summary['clicks'] * 100

cat_summary = cat_summary.sort_values(by='cost', ascending=False)

print("=" * 110)
print("REFINED SEARCH TERMS BREAKDOWN BY THEMATIC INTENT (2-YEAR PERFORMANCE)")
print("=" * 110)
print(cat_summary.to_string(index=False))
