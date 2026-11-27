import pandas as pd
import openpyxl

# -------------------------------------------------------------
# 1. COMPILE NEGATIVE KEYWORDS MASTER
# -------------------------------------------------------------

negatives_data = [
    # --- Category 1: Scams, Chit Funds & Defunct Schemes (Pure Waste) ---
    {"Category": "Scams, Chit Funds & Ponzi Schemes", "Negative Keyword": "pacl", "Match Type": "Broad", "Level": "Account", "Reason": "Defunct PACL/Pearls chit fund scam; not serviced"},
    {"Category": "Scams, Chit Funds & Ponzi Schemes", "Negative Keyword": "sebipacl", "Match Type": "Broad", "Level": "Account", "Reason": "SEBI PACL refund portal search"},
    {"Category": "Scams, Chit Funds & Ponzi Schemes", "Negative Keyword": "sebipaclrefund", "Match Type": "Broad", "Level": "Account", "Reason": "SEBI PACL refund portal query"},
    {"Category": "Scams, Chit Funds & Ponzi Schemes", "Negative Keyword": '"pacl refund"', "Match Type": "Phrase", "Level": "Account", "Reason": "PACL refund search"},
    {"Category": "Scams, Chit Funds & Ponzi Schemes", "Negative Keyword": '"pacl claim"', "Match Type": "Phrase", "Level": "Account", "Reason": "PACL claim query"},
    {"Category": "Scams, Chit Funds & Ponzi Schemes", "Negative Keyword": '"pacl login"', "Match Type": "Phrase", "Level": "Account", "Reason": "PACL portal login"},
    {"Category": "Scams, Chit Funds & Ponzi Schemes", "Negative Keyword": "sahara", "Match Type": "Broad", "Level": "Account", "Reason": "Sahara cooperative society refund query"},
    {"Category": "Scams, Chit Funds & Ponzi Schemes", "Negative Keyword": '"sahara refund"', "Match Type": "Phrase", "Level": "Account", "Reason": "Central CRCS Sahara refund portal query"},
    {"Category": "Scams, Chit Funds & Ponzi Schemes", "Negative Keyword": '"sahara portal"', "Match Type": "Phrase", "Level": "Account", "Reason": "Sahara refund portal"},
    {"Category": "Scams, Chit Funds & Ponzi Schemes", "Negative Keyword": '"chit fund"', "Match Type": "Phrase", "Level": "Account", "Reason": "General chit fund queries"},
    {"Category": "Scams, Chit Funds & Ponzi Schemes", "Negative Keyword": '"pearls agrotech"', "Match Type": "Phrase", "Level": "Account", "Reason": "PACL Pearls agrotech queries"},
    {"Category": "Scams, Chit Funds & Ponzi Schemes", "Negative Keyword": '"rose valley"', "Match Type": "Phrase", "Level": "Account", "Reason": "Rose valley chit fund scam query"},
    {"Category": "Scams, Chit Funds & Ponzi Schemes", "Negative Keyword": '"saradha"', "Match Type": "Phrase", "Level": "Account", "Reason": "Saradha chit fund scam"},

    # --- Category 2: Government Welfare Schemes, Scholarships & PFMS ---
    {"Category": "Govt Welfare & Non-Asset Portals", "Negative Keyword": "pfms", "Match Type": "Broad", "Level": "Account", "Reason": "Public Financial Management System (govt subsidies/DBT)"},
    {"Category": "Govt Welfare & Non-Asset Portals", "Negative Keyword": '"government scheme"', "Match Type": "Phrase", "Level": "Account", "Reason": "General government welfare schemes"},
    {"Category": "Govt Welfare & Non-Asset Portals", "Negative Keyword": '"government schemes"', "Match Type": "Phrase", "Level": "Account", "Reason": "Welfare scheme inquiries"},
    {"Category": "Govt Welfare & Non-Asset Portals", "Negative Keyword": "pmkisan", "Match Type": "Broad", "Level": "Account", "Reason": "PM Kisan Samman Nidhi farmer subsidy"},
    {"Category": "Govt Welfare & Non-Asset Portals", "Negative Keyword": '"pm kisan"', "Match Type": "Phrase", "Level": "Account", "Reason": "Farmer welfare subsidy"},
    {"Category": "Govt Welfare & Non-Asset Portals", "Negative Keyword": "ration", "Match Type": "Broad", "Level": "Account", "Reason": "Ration card queries"},
    {"Category": "Govt Welfare & Non-Asset Portals", "Negative Keyword": "ayushman", "Match Type": "Broad", "Level": "Account", "Reason": "Ayushman Bharat health card"},
    {"Category": "Govt Welfare & Non-Asset Portals", "Negative Keyword": "scholarship", "Match Type": "Broad", "Level": "Account", "Reason": "Student scholarships"},
    {"Category": "Govt Welfare & Non-Asset Portals", "Negative Keyword": "epfigms", "Match Type": "Broad", "Level": "Account", "Reason": "EPFO grievance portal; not asset recovery"},
    {"Category": "Govt Welfare & Non-Asset Portals", "Negative Keyword": "mudra", "Match Type": "Broad", "Level": "Account", "Reason": "Mudra loan scheme"},
    {"Category": "Govt Welfare & Non-Asset Portals", "Negative Keyword": "ladli", "Match Type": "Broad", "Level": "Account", "Reason": "State welfare schemes"},

    # --- Category 3: Retail Stock Trading, Demat Opening & Discount Brokers ---
    {"Category": "Stock Trading & Broking", "Negative Keyword": "trading", "Match Type": "Broad", "Level": "Account", "Reason": "Retail stock/day trading, not asset recovery"},
    {"Category": "Stock Trading & Broking", "Negative Keyword": "trader", "Match Type": "Broad", "Level": "Account", "Reason": "Intraday/retail traders"},
    {"Category": "Stock Trading & Broking", "Negative Keyword": "intraday", "Match Type": "Broad", "Level": "Account", "Reason": "Day trading queries"},
    {"Category": "Stock Trading & Broking", "Negative Keyword": '"stock market"', "Match Type": "Phrase", "Level": "Account", "Reason": "General market news/education"},
    {"Category": "Stock Trading & Broking", "Negative Keyword": '"share bazar"', "Match Type": "Phrase", "Level": "Account", "Reason": "Hindi share market queries"},
    {"Category": "Stock Trading & Broking", "Negative Keyword": '"option chain"', "Match Type": "Phrase", "Level": "Account", "Reason": "Derivatives/F&O queries"},
    {"Category": "Stock Trading & Broking", "Negative Keyword": '"call and put"', "Match Type": "Phrase", "Level": "Account", "Reason": "Options trading"},
    {"Category": "Stock Trading & Broking", "Negative Keyword": '"nifty 50"', "Match Type": "Phrase", "Level": "Account", "Reason": "Index tracking"},
    {"Category": "Stock Trading & Broking", "Negative Keyword": '"bank nifty"', "Match Type": "Phrase", "Level": "Account", "Reason": "Index trading"},
    {"Category": "Stock Trading & Broking", "Negative Keyword": "zerodha", "Match Type": "Broad", "Level": "Account", "Reason": "Discount broker app"},
    {"Category": "Stock Trading & Broking", "Negative Keyword": "groww", "Match Type": "Broad", "Level": "Account", "Reason": "Discount broker app"},
    {"Category": "Stock Trading & Broking", "Negative Keyword": "upstox", "Match Type": "Broad", "Level": "Account", "Reason": "Discount broker app"},
    {"Category": "Stock Trading & Broking", "Negative Keyword": "angelone", "Match Type": "Broad", "Level": "Account", "Reason": "Discount broker brand"},
    {"Category": "Stock Trading & Broking", "Negative Keyword": '"angel broking"', "Match Type": "Phrase", "Level": "Account", "Reason": "Discount broker"},
    {"Category": "Stock Trading & Broking", "Negative Keyword": '"dhan app"', "Match Type": "Phrase", "Level": "Account", "Reason": "Trading app"},
    {"Category": "Stock Trading & Broking", "Negative Keyword": "tradingview", "Match Type": "Broad", "Level": "Account", "Reason": "Charting platform"},
    {"Category": "Stock Trading & Broking", "Negative Keyword": "screener", "Match Type": "Broad", "Level": "Account", "Reason": "Stock screener website"},
    {"Category": "Stock Trading & Broking", "Negative Keyword": '"broker list"', "Match Type": "Phrase", "Level": "Account", "Reason": "Broker directories"},
    {"Category": "Stock Trading & Broking", "Negative Keyword": '"ipo allotment status"', "Match Type": "Phrase", "Level": "Account", "Reason": "New IPO status check"},
    {"Category": "Stock Trading & Broking", "Negative Keyword": '"open demat account"', "Match Type": "Phrase", "Level": "Account", "Reason": "New account opening, not old share recovery"},

    # --- Category 4: Government Credentials, Navigational Logins & Passwords ---
    {"Category": "Navigational Logins & Passwords", "Negative Keyword": '"password reset"', "Match Type": "Phrase", "Level": "Account", "Reason": "Seeking password recovery on govt portals"},
    {"Category": "Navigational Logins & Passwords", "Negative Keyword": '"forgot password"', "Match Type": "Phrase", "Level": "Account", "Reason": "Seeking password recovery on govt portals"},
    {"Category": "Navigational Logins & Passwords", "Negative Keyword": '"change password"', "Match Type": "Phrase", "Level": "Account", "Reason": "Credential management"},
    {"Category": "Navigational Logins & Passwords", "Negative Keyword": '"uan login"', "Match Type": "Phrase", "Level": "Account", "Reason": "Direct EPFO member login intent"},
    {"Category": "Navigational Logins & Passwords", "Negative Keyword": '"epfo login"', "Match Type": "Phrase", "Level": "Account", "Reason": "Direct EPFO portal login"},
    {"Category": "Navigational Logins & Passwords", "Negative Keyword": '"passbook login"', "Match Type": "Phrase", "Level": "Account", "Reason": "EPFO passbook checking"},
    {"Category": "Navigational Logins & Passwords", "Negative Keyword": '"member portal"', "Match Type": "Phrase", "Level": "Account", "Reason": "EPFO member login portal"},
    {"Category": "Navigational Logins & Passwords", "Negative Keyword": '"incometax login"', "Match Type": "Phrase", "Level": "Account", "Reason": "Income tax portal login"},
    {"Category": "Navigational Logins & Passwords", "Negative Keyword": '"net banking login"', "Match Type": "Phrase", "Level": "Account", "Reason": "Bank account login queries"},

    # --- Category 5: Jobs, Recruitment & Career Inquiries ---
    {"Category": "Jobs & Careers", "Negative Keyword": "job", "Match Type": "Broad", "Level": "Account", "Reason": "Job hunters"},
    {"Category": "Jobs & Careers", "Negative Keyword": "jobs", "Match Type": "Broad", "Level": "Account", "Reason": "Job hunters"},
    {"Category": "Jobs & Careers", "Negative Keyword": "career", "Match Type": "Broad", "Level": "Account", "Reason": "Employment seekers"},
    {"Category": "Jobs & Careers", "Negative Keyword": "careers", "Match Type": "Broad", "Level": "Account", "Reason": "Employment seekers"},
    {"Category": "Jobs & Careers", "Negative Keyword": "vacancy", "Match Type": "Broad", "Level": "Account", "Reason": "Hiring queries"},
    {"Category": "Jobs & Careers", "Negative Keyword": "vacancies", "Match Type": "Broad", "Level": "Account", "Reason": "Hiring queries"},
    {"Category": "Jobs & Careers", "Negative Keyword": "recruitment", "Match Type": "Broad", "Level": "Account", "Reason": "Recruitment inquiries"},
    {"Category": "Jobs & Careers", "Negative Keyword": "salary", "Match Type": "Broad", "Level": "Account", "Reason": "Salary reviews"},
    {"Category": "Jobs & Careers", "Negative Keyword": "interview", "Match Type": "Broad", "Level": "Account", "Reason": "Interview questions"},
    {"Category": "Jobs & Careers", "Negative Keyword": "internship", "Match Type": "Broad", "Level": "Account", "Reason": "Internship queries"},
    {"Category": "Jobs & Careers", "Negative Keyword": '"glassdoor"', "Match Type": "Phrase", "Level": "Account", "Reason": "Company reviews/salary"},
    {"Category": "Jobs & Careers", "Negative Keyword": '"ambitionbox"', "Match Type": "Phrase", "Level": "Account", "Reason": "Company reviews/salary"},

    # --- Category 6: Informational, Samples, Free Templates & Circulars ---
    {"Category": "Free Downloads & Samples", "Negative Keyword": '"free download"', "Match Type": "Phrase", "Level": "Account", "Reason": "Looking for free forms without paying fees"},
    {"Category": "Free Downloads & Samples", "Negative Keyword": '"sample format"', "Match Type": "Phrase", "Level": "Account", "Reason": "Looking for legal drafting templates for free"},
    {"Category": "Free Downloads & Samples", "Negative Keyword": '"sample draft"', "Match Type": "Phrase", "Level": "Account", "Reason": "Looking for free drafts"},
    {"Category": "Free Downloads & Samples", "Negative Keyword": '"circular pdf"', "Match Type": "Phrase", "Level": "Account", "Reason": "Regulatory circular search"},
    {"Category": "Free Downloads & Samples", "Negative Keyword": '"gazette notification"', "Match Type": "Phrase", "Level": "Account", "Reason": "Legal research queries"},
    {"Category": "Free Downloads & Samples", "Negative Keyword": '"meaning of"', "Match Type": "Phrase", "Level": "Account", "Reason": "Academic / definition intent"},
    {"Category": "Free Downloads & Samples", "Negative Keyword": '"wikipedia"', "Match Type": "Phrase", "Level": "Account", "Reason": "Encyclopedia searches"},

    # --- Category 7: Unrelated Companies, Mobile Tech & App Glitches ---
    {"Category": "Unrelated Tech & Brands", "Negative Keyword": '"mud management"', "Match Type": "Phrase", "Level": "Account", "Reason": "Unrelated company"},
    {"Category": "Unrelated Tech & Brands", "Negative Keyword": '"idlc asset management"', "Match Type": "Phrase", "Level": "Account", "Reason": "Foreign asset management firm"},
    {"Category": "Unrelated Tech & Brands", "Negative Keyword": '"raise securities"', "Match Type": "Phrase", "Level": "Account", "Reason": "Unrelated entity"},
    {"Category": "Unrelated Tech & Brands", "Negative Keyword": '"uniresearch global"', "Match Type": "Phrase", "Level": "Account", "Reason": "Unrelated entity"},
    {"Category": "Unrelated Tech & Brands", "Negative Keyword": '"horizon investment"', "Match Type": "Phrase", "Level": "Account", "Reason": "Unrelated firm"},
    {"Category": "Unrelated Tech & Brands", "Negative Keyword": '"contact recovery apps"', "Match Type": "Phrase", "Level": "Account", "Reason": "Android phone contacts recovery"},
    {"Category": "Unrelated Tech & Brands", "Negative Keyword": '"mobile phones"', "Match Type": "Phrase", "Level": "Account", "Reason": "Old test campaign junk"},
    {"Category": "Unrelated Tech & Brands", "Negative Keyword": '"smartphone"', "Match Type": "Phrase", "Level": "Account", "Reason": "Old test campaign junk"},
    {"Category": "Unrelated Tech & Brands", "Negative Keyword": '"samsung mobile"', "Match Type": "Phrase", "Level": "Account", "Reason": "Old test campaign junk"},
]

df_neg = pd.DataFrame(negatives_data)
df_neg.to_excel(r'data\Share Samadhan\Recommended_Negative_Keywords_Master.xlsx', index=False)
df_neg.to_csv(r'data\Share Samadhan\Recommended_Negative_Keywords_Master.csv', index=False)
print(f"Generated {len(df_neg)} Master Negative Keywords across {df_neg['Category'].nunique()} categories.")

# -------------------------------------------------------------
# 2. COMPILE TARGET KEYWORDS MASTER
# -------------------------------------------------------------

targets_data = [
    # === AD GROUP 1: IEPF Recovery Core ===
    {"Campaign": "Search_IEPF_Recovery", "Ad Group": "IEPF_Core_Recovery", "Keyword": "[iepf]", "Match Type": "Exact", "Intent": "High-Volume Core Brand Search", "Landing Page": "https://sharesamadhan.com/iepfclaim", "Suggested Max CPC": 30.0},
    {"Campaign": "Search_IEPF_Recovery", "Ad Group": "IEPF_Core_Recovery", "Keyword": "[iepfa]", "Match Type": "Exact", "Intent": "Authority Search", "Landing Page": "https://sharesamadhan.com/iepfclaim", "Suggested Max CPC": 30.0},
    {"Campaign": "Search_IEPF_Recovery", "Ad Group": "IEPF_Core_Recovery", "Keyword": "[iepf portal]", "Match Type": "Exact", "Intent": "Core Navigational", "Landing Page": "https://sharesamadhan.com/iepfclaim", "Suggested Max CPC": 28.0},
    {"Campaign": "Search_IEPF_Recovery", "Ad Group": "IEPF_Core_Recovery", "Keyword": "[iepf website]", "Match Type": "Exact", "Intent": "Core Navigational", "Landing Page": "https://sharesamadhan.com/iepfclaim", "Suggested Max CPC": 25.0},
    {"Campaign": "Search_IEPF_Recovery", "Ad Group": "IEPF_Core_Recovery", "Keyword": "[iepf claim]", "Match Type": "Exact", "Intent": "Direct Commercial Recovery Intent", "Landing Page": "https://sharesamadhan.com/iepfclaim", "Suggested Max CPC": 35.0},
    {"Campaign": "Search_IEPF_Recovery", "Ad Group": "IEPF_Core_Recovery", "Keyword": '"iepf claim"', "Match Type": "Phrase", "Intent": "Direct Commercial Recovery Intent", "Landing Page": "https://sharesamadhan.com/iepfclaim", "Suggested Max CPC": 32.0},
    {"Campaign": "Search_IEPF_Recovery", "Ad Group": "IEPF_Core_Recovery", "Keyword": '"iepf consultant"', "Match Type": "Phrase", "Intent": "Professional Service Inquiry", "Landing Page": "https://sharesamadhan.com/iepfclaim", "Suggested Max CPC": 40.0},
    {"Campaign": "Search_IEPF_Recovery", "Ad Group": "IEPF_Core_Recovery", "Keyword": '"iepf share recovery"', "Match Type": "Phrase", "Intent": "Core Solution Intent", "Landing Page": "https://sharesamadhan.com/iepfclaim", "Suggested Max CPC": 38.0},
    {"Campaign": "Search_IEPF_Recovery", "Ad Group": "IEPF_Core_Recovery", "Keyword": '"how to claim shares from iepf"', "Match Type": "Phrase", "Intent": "High Problem Aware", "Landing Page": "https://sharesamadhan.com/iepfclaim", "Suggested Max CPC": 35.0},
    {"Campaign": "Search_IEPF_Recovery", "Ad Group": "IEPF_Core_Recovery", "Keyword": '"unclaimed shares in iepf"', "Match Type": "Phrase", "Intent": "Problem Aware", "Landing Page": "https://sharesamadhan.com/iepfclaim", "Suggested Max CPC": 32.0},
    {"Campaign": "Search_IEPF_Recovery", "Ad Group": "IEPF_Core_Recovery", "Keyword": "[iepfa integrated portal]", "Match Type": "Exact", "Intent": "Harvested Top Performer", "Landing Page": "https://sharesamadhan.com/iepfclaim", "Suggested Max CPC": 28.0},
    {"Campaign": "Search_IEPF_Recovery", "Ad Group": "IEPF_Core_Recovery", "Keyword": '"iepfa integrated portal"', "Match Type": "Phrase", "Intent": "Harvested Top Performer", "Landing Page": "https://sharesamadhan.com/iepfclaim", "Suggested Max CPC": 25.0},
    {"Campaign": "Search_IEPF_Recovery", "Ad Group": "IEPF_Core_Recovery", "Keyword": "[iepf form 5]", "Match Type": "Exact", "Intent": "Filing Assistance Intent", "Landing Page": "https://sharesamadhan.com/iepfclaim", "Suggested Max CPC": 26.0},
    {"Campaign": "Search_IEPF_Recovery", "Ad Group": "IEPF_Core_Recovery", "Keyword": '"form iepf 5 claim"', "Match Type": "Phrase", "Intent": "Filing Assistance Intent", "Landing Page": "https://sharesamadhan.com/iepfclaim", "Suggested Max CPC": 26.0},

    # === AD GROUP 2: Duplicate Shares & Lost Certificates (LOC) ===
    {"Campaign": "Search_Duplicate_Shares", "Ad Group": "Duplicate_Shares_LOC", "Keyword": "[duplicate share certificate]", "Match Type": "Exact", "Intent": "High Commercial Intent", "Landing Page": "https://sharesamadhan.com/duplicate-issue-of-shares", "Suggested Max CPC": 35.0},
    {"Campaign": "Search_Duplicate_Shares", "Ad Group": "Duplicate_Shares_LOC", "Keyword": '"duplicate share certificate"', "Match Type": "Phrase", "Intent": "High Commercial Intent", "Landing Page": "https://sharesamadhan.com/duplicate-issue-of-shares", "Suggested Max CPC": 32.0},
    {"Campaign": "Search_Duplicate_Shares", "Ad Group": "Duplicate_Shares_LOC", "Keyword": '"how to get duplicate shares"', "Match Type": "Phrase", "Intent": "Solution Seeking", "Landing Page": "https://sharesamadhan.com/duplicate-issue-of-shares", "Suggested Max CPC": 30.0},
    {"Campaign": "Search_Duplicate_Shares", "Ad Group": "Duplicate_Shares_LOC", "Keyword": '"lost share certificate procedure"', "Match Type": "Phrase", "Intent": "Procedural High-Intent", "Landing Page": "https://sharesamadhan.com/duplicate-issue-of-shares", "Suggested Max CPC": 35.0},
    {"Campaign": "Search_Duplicate_Shares", "Ad Group": "Duplicate_Shares_LOC", "Keyword": '"letter of confirmation for shares"', "Match Type": "Phrase", "Intent": "LOC Direct Intent (SEBI)", "Landing Page": "https://sharesamadhan.com/duplicate-issue-of-shares", "Suggested Max CPC": 35.0},
    {"Campaign": "Search_Duplicate_Shares", "Ad Group": "Duplicate_Shares_LOC", "Keyword": '"lost physical share certificate"', "Match Type": "Phrase", "Intent": "Physical Share Loss", "Landing Page": "https://sharesamadhan.com/duplicate-issue-of-shares", "Suggested Max CPC": 34.0},
    {"Campaign": "Search_Duplicate_Shares", "Ad Group": "Duplicate_Shares_LOC", "Keyword": '"indemnity bond for duplicate shares"', "Match Type": "Phrase", "Intent": "Documentation Assistance", "Landing Page": "https://sharesamadhan.com/duplicate-issue-of-shares", "Suggested Max CPC": 30.0},

    # === AD GROUP 3: Transmission of Shares & Legal Heir Succession (Highest Ticket) ===
    {"Campaign": "Search_Transmission_Shares", "Ad Group": "Transmission_LegalHeir", "Keyword": "[transmission of shares]", "Match Type": "Exact", "Intent": "High-Ticket Estate Succession", "Landing Page": "https://sharesamadhan.com/transmission-of-shares", "Suggested Max CPC": 45.0},
    {"Campaign": "Search_Transmission_Shares", "Ad Group": "Transmission_LegalHeir", "Keyword": '"transmission of shares"', "Match Type": "Phrase", "Intent": "High-Ticket Estate Succession", "Landing Page": "https://sharesamadhan.com/transmission-of-shares", "Suggested Max CPC": 40.0},
    {"Campaign": "Search_Transmission_Shares", "Ad Group": "Transmission_LegalHeir", "Keyword": '"transmission of shares after death"', "Match Type": "Phrase", "Intent": "Deceased Shareholder Estate", "Landing Page": "https://sharesamadhan.com/transmission-of-shares", "Suggested Max CPC": 45.0},
    {"Campaign": "Search_Transmission_Shares", "Ad Group": "Transmission_LegalHeir", "Keyword": '"claim shares of deceased person"', "Match Type": "Phrase", "Intent": "High Emotional & Financial Urgency", "Landing Page": "https://sharesamadhan.com/transmission-of-shares", "Suggested Max CPC": 45.0},
    {"Campaign": "Search_Transmission_Shares", "Ad Group": "Transmission_LegalHeir", "Keyword": '"transmission of shares without succession certificate"', "Match Type": "Phrase", "Intent": "Legal Bottleneck Resolution", "Landing Page": "https://sharesamadhan.com/transmission-of-shares", "Suggested Max CPC": 48.0},
    {"Campaign": "Search_Transmission_Shares", "Ad Group": "Transmission_LegalHeir", "Keyword": '"legal heir claim shares"', "Match Type": "Phrase", "Intent": "Inheritance Retrieval", "Landing Page": "https://sharesamadhan.com/transmission-of-shares", "Suggested Max CPC": 42.0},
    {"Campaign": "Search_Transmission_Shares", "Ad Group": "Transmission_LegalHeir", "Keyword": '"probate of will shares transmission"', "Match Type": "Phrase", "Intent": "Complex Legal Case", "Landing Page": "https://sharesamadhan.com/transmission-of-shares", "Suggested Max CPC": 45.0},

    # === AD GROUP 4: Physical to Demat Conversion & KYC Rectification (SEBI ISR) ===
    {"Campaign": "Search_Demat_Services", "Ad Group": "Physical_to_Demat_KYC", "Keyword": "[physical shares to demat]", "Match Type": "Exact", "Intent": "Compulsory SEBI Conversion", "Landing Page": "https://sharesamadhan.com/demat-services", "Suggested Max CPC": 35.0},
    {"Campaign": "Search_Demat_Services", "Ad Group": "Physical_to_Demat_KYC", "Keyword": '"convert physical shares to demat"', "Match Type": "Phrase", "Intent": "Compulsory SEBI Conversion", "Landing Page": "https://sharesamadhan.com/demat-services", "Suggested Max CPC": 32.0},
    {"Campaign": "Search_Demat_Services", "Ad Group": "Physical_to_Demat_KYC", "Keyword": '"signature mismatch in shares"', "Match Type": "Phrase", "Intent": "RTA KYC Rejection Resolution", "Landing Page": "https://sharesamadhan.com/demat-services", "Suggested Max CPC": 36.0},
    {"Campaign": "Search_Demat_Services", "Ad Group": "Physical_to_Demat_KYC", "Keyword": '"form isr 1 submission"', "Match Type": "Phrase", "Intent": "KYC Regularization", "Landing Page": "https://sharesamadhan.com/demat-services", "Suggested Max CPC": 28.0},
    {"Campaign": "Search_Demat_Services", "Ad Group": "Physical_to_Demat_KYC", "Keyword": '"name mismatch share certificate aadhaar"', "Match Type": "Phrase", "Intent": "Identity Discrepancy", "Landing Page": "https://sharesamadhan.com/demat-services", "Suggested Max CPC": 35.0},
    {"Campaign": "Search_Demat_Services", "Ad Group": "Physical_to_Demat_KYC", "Keyword": '"form isr 2 banker attestation"', "Match Type": "Phrase", "Intent": "Bank Attestation Assistance", "Landing Page": "https://sharesamadhan.com/demat-services", "Suggested Max CPC": 28.0},

    # === AD GROUP 5: Unclaimed Wealth Discovery & Free Search ===
    {"Campaign": "Search_Unclaimed_Wealth", "Ad Group": "Unclaimed_Assets_Portal", "Keyword": "[unclaimed assets portal]", "Match Type": "Exact", "Intent": "Harvested Top Performer", "Landing Page": "https://search.sharesamadhan.com/sharesamadhan/login", "Suggested Max CPC": 25.0},
    {"Campaign": "Search_Unclaimed_Wealth", "Ad Group": "Unclaimed_Assets_Portal", "Keyword": '"unclaimed assets portal"', "Match Type": "Phrase", "Intent": "Harvested Top Performer", "Landing Page": "https://search.sharesamadhan.com/sharesamadhan/login", "Suggested Max CPC": 24.0},
    {"Campaign": "Search_Unclaimed_Wealth", "Ad Group": "Unclaimed_Assets_Portal", "Keyword": '"unclaimed assets portal india"', "Match Type": "Phrase", "Intent": "Harvested Top Performer", "Landing Page": "https://search.sharesamadhan.com/sharesamadhan/login", "Suggested Max CPC": 24.0},
    {"Campaign": "Search_Unclaimed_Wealth", "Ad Group": "Unclaimed_Assets_Portal", "Keyword": '"find unclaimed shares"', "Match Type": "Phrase", "Intent": "Discovery / Search Intent", "Landing Page": "https://search.sharesamadhan.com/sharesamadhan/login", "Suggested Max CPC": 26.0},
    {"Campaign": "Search_Unclaimed_Wealth", "Ad Group": "Unclaimed_Assets_Portal", "Keyword": '"how to track unclaimed investments"', "Match Type": "Phrase", "Intent": "Discovery / Search Intent", "Landing Page": "https://search.sharesamadhan.com/sharesamadhan/login", "Suggested Max CPC": 26.0},

    # === AD GROUP 6: Inoperative Bank Deposits (DEAF / UDGAM) & Mutual Funds (SCWF) ===
    {"Campaign": "Search_Bank_MutualFunds", "Ad Group": "Bank_Deposits_DEAF", "Keyword": "[unclaimed deposits]", "Match Type": "Exact", "Intent": "Harvested Performer", "Landing Page": "https://sharesamadhan.com/inoperative-bank-accounts", "Suggested Max CPC": 28.0},
    {"Campaign": "Search_Bank_MutualFunds", "Ad Group": "Bank_Deposits_DEAF", "Keyword": '"unclaimed bank deposits recovery"', "Match Type": "Phrase", "Intent": "Dormant / DEAF Account", "Landing Page": "https://sharesamadhan.com/inoperative-bank-accounts", "Suggested Max CPC": 30.0},
    {"Campaign": "Search_Bank_MutualFunds", "Ad Group": "Bank_Deposits_DEAF", "Keyword": '"rbi deaf account claim"', "Match Type": "Phrase", "Intent": "DEAF Fund Retrieval", "Landing Page": "https://sharesamadhan.com/inoperative-bank-accounts", "Suggested Max CPC": 32.0},
    {"Campaign": "Search_Bank_MutualFunds", "Ad Group": "Mutual_Funds_SCWF", "Keyword": '"unclaimed mutual funds recovery"', "Match Type": "Phrase", "Intent": "Senior Citizen Welfare Fund", "Landing Page": "https://sharesamadhan.com/unclaimed-mutual-funds", "Suggested Max CPC": 32.0},
    {"Campaign": "Search_Bank_MutualFunds", "Ad Group": "Mutual_Funds_SCWF", "Keyword": '"claim old mutual fund folio"', "Match Type": "Phrase", "Intent": "Dormant MF Folio Retrieval", "Landing Page": "https://sharesamadhan.com/unclaimed-mutual-funds", "Suggested Max CPC": 30.0},

    # === AD GROUP 7: Official Brand Protection ===
    {"Campaign": "Search_Brand_Protection", "Ad Group": "Brand_Exact", "Keyword": "[share samadhan]", "Match Type": "Exact", "Intent": "Brand Navigation", "Landing Page": "https://sharesamadhan.com/", "Suggested Max CPC": 15.0},
    {"Campaign": "Search_Brand_Protection", "Ad Group": "Brand_Exact", "Keyword": "[sharesamadhan]", "Match Type": "Exact", "Intent": "Brand Navigation", "Landing Page": "https://sharesamadhan.com/", "Suggested Max CPC": 15.0},
    {"Campaign": "Search_Brand_Protection", "Ad Group": "Brand_Exact", "Keyword": "[share samadhan limited]", "Match Type": "Exact", "Intent": "Brand Navigation", "Landing Page": "https://sharesamadhan.com/", "Suggested Max CPC": 15.0},
    {"Campaign": "Search_Brand_Protection", "Ad Group": "Brand_Exact", "Keyword": "[sare samadhan]", "Match Type": "Exact", "Intent": "Phonetic Misspelling Defense", "Landing Page": "https://sharesamadhan.com/", "Suggested Max CPC": 12.0},
    {"Campaign": "Search_Brand_Protection", "Ad Group": "Brand_Exact", "Keyword": "[wealth samadhan]", "Match Type": "Exact", "Intent": "Group Brand Protection", "Landing Page": "https://sharesamadhan.com/", "Suggested Max CPC": 15.0},
]

df_target = pd.DataFrame(targets_data)
df_target.to_excel(r'data\Share Samadhan\Recommended_Target_Keywords_Master.xlsx', index=False)
df_target.to_csv(r'data\Share Samadhan\Recommended_Target_Keywords_Master.csv', index=False)
print(f"Generated {len(df_target)} Curated Target Keywords across {df_target['Ad Group'].nunique()} Ad Groups.")
