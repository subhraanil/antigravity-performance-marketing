import pandas as pd
import openpyxl

CAMPAIGN_NAME = "Search_Share_Samadhan_Services"
BUDGET = 1500
TARGET_CPA = 160
LOCATION = "India"
LANGUAGE = "en;hi"

# -------------------------------------------------------------
# 1. AD GROUPS & RSAs DEFINITION
# -------------------------------------------------------------
ad_groups_data = {
    "IEPF_Core_Recovery": {
        "final_url": "https://sharesamadhan.com/iepfclaim",
        "path1": "IEPF-Claim",
        "path2": "Recovery",
        "cpc_bid": 30.0,
        "headlines": [
            "IEPF Share Recovery Experts",       # 27
            "Claim Your IEPF Shares Now",       # 26
            "Unclaimed Dividends & Shares",     # 28
            "Form IEPF 5 Filing Help",          # 23
            "Recover Lost IEPF Investments",    # 29
            "IEPF Authority Claim Support",     # 28
            "India Largest IEPF Consultant",    # 29
            "BSE Listed Recovery Firm",         # 24
            "Track Unclaimed IEPF Assets",      # 27
            "Fast IEPF Verification",           # 22
            "Get Back Blocked Shares",          # 23
            "Expert Legal IEPF Assistance",     # 28
            "100% Legal & Trusted Process",     # 28
            "Check IEPF Claim Eligibility",     # 28
            "Share Samadhan Official Help"      # 28
        ],
        "descriptions": [
            "Dividends unclaimed for 7 years? Recover your transferred shares & funds from IEPF.", # 83
            "India's leading unclaimed investment recovery company. We handle complete IEPF-5 filing.", # 88
            "End-to-end documentation, RTA follow-ups, and corporate verification report approval.", # 85
            "Consult our legal experts today. Hassle-free recovery of your blocked shares and funds."  # 87
        ]
    },
    "Duplicate_Shares_LOC": {
        "final_url": "https://sharesamadhan.com/duplicate-issue-of-shares",
        "path1": "Duplicate",
        "path2": "Shares-LOC",
        "cpc_bid": 32.0,
        "headlines": [
            "Duplicate Share Certificate",      # 27
            "Lost Share Certificate Help",      # 27
            "Get Duplicate Shares Issued",      # 27
            "Letter of Confirmation LOC",       # 26
            "Recover Lost Physical Shares",     # 28
            "Stolen or Damaged Shares?",        # 25
            "SEBI Duplicate Share Process",     # 28
            "Indemnity Bond & Affidavit",       # 26
            "Police FIR & Newspaper Notice",    # 29
            "Issue Duplicate Shares Fast",      # 27
            "Physical Certificate Lost?",       # 26
            "India #1 Share Recovery Team",     # 28
            "Hassle-Free RTA Liaisoning",       # 26
            "BSE Listed Recovery Company",      # 27
            "Share Samadhan Duplicate Help"     # 29
        ],
        "descriptions": [
            "Lost or mutilated paper share certificates? We help you get duplicate shares issued.", # 86
            "End-to-end support: FIR filing, newspaper public notice, Indemnity Bonds, and RTA NOC.", # 87
            "Obtain Letter of Confirmation (LOC) under SEBI guidelines without procedural delays.", # 85
            "India's premier recovery firm. Recover your valuable lost share certificates today."    # 83
        ]
    },
    "Transmission_LegalHeir": {
        "final_url": "https://sharesamadhan.com/transmission-of-shares",
        "path1": "Transmission",
        "path2": "Legal-Heir",
        "cpc_bid": 42.0,
        "headlines": [
            "Transmission of Shares Help",      # 27
            "Deceased Shareholder Claims",      # 27
            "Claim Shares of Late Parents",     # 28
            "Legal Heir Share Transmission",    # 29
            "Shares Without Succession",        # 25
            "Probate of Will Share Claims",     # 28
            "Inherited Share Recovery",         # 24
            "Family Dispute Resolution",        # 25
            "Succession Certificate Help",      # 27
            "Claim Ancestral Shares Today",     # 28
            "Smooth Share Transmission",        # 25
            "Complete Legal Documentation",     # 28
            "India Largest Asset Recovery",     # 28
            "BSE Listed Trusted Experts",       # 26
            "Share Samadhan Legal Heir"         # 25
        ],
        "descriptions": [
            "Inherited shares of deceased family members? We help legal heirs claim rightful wealth.", # 88
            "Transmission without succession certificate or probate where permissible. Legal guidance.", # 90
            "We handle NOC from legal heirs, RTA documentation, and company succession paperwork.", # 86
            "Over ₹1000+ Cr assets resolved. Consult India's leading legal inheritance specialists." # 87
        ]
    },
    "Physical_to_Demat_KYC": {
        "final_url": "https://sharesamadhan.com/",
        "path1": "Physical-Demat",
        "path2": "KYC-Update",
        "cpc_bid": 30.0,
        "headlines": [
            "Physical Shares to Demat",         # 24
            "Convert Paper Shares to Demat",    # 29
            "SEBI Mandatory Demat Help",        # 25
            "Signature Mismatch Solution",      # 27
            "Form ISR 1 2 4 Assistance",        # 25
            "Banker Attestation ISR 2",         # 24
            "Name Mismatch Share & Aadhaar",    # 29
            "KYC Freeze Unlocking Support",     # 28
            "Unfreeze Old Physical Shares",     # 28
            "Demat Conversion Specialists",     # 28
            "RTA Rejection Resolution",         # 24
            "Fast Paper to Demat Process",      # 27
            "BSE Listed Advisory Firm",         # 24
            "100% Compliant With SEBI",         # 24
            "Share Samadhan Demat Support"      # 28
        ],
        "descriptions": [
            "Physical shares can no longer be traded. Convert your paper certificates into Demat now.", # 89
            "Facing signature mismatch, address change, or name discrepancy? We resolve RTA queries.", # 88
            "Complete Form ISR-1, ISR-2 banker attestation, and ISR-4 filing with all major RTAs.", # 86
            "Protect your physical holdings from IEPF transfer. Convert to Demat with our experts."  # 86
        ]
    },
    "Bank_Deposits_DEAF": {
        "final_url": "https://sharesamadhan.com/inoperative-bank-accounts",
        "path1": "Bank-Deposits",
        "path2": "DEAF-Claim",
        "cpc_bid": 28.0,
        "headlines": [
            "Unclaimed Bank Deposits Help",     # 28
            "Dormant Bank Account Recovery",    # 29
            "RBI DEAF Account Claim Support",   # 29
            "Recover Old Inoperative FDs",      # 27
            "Claim Forgotten Bank Money",       # 26
            "Unclaimed Mutual Funds SCWF",      # 27
            "Recover Dormant MF Folios",        # 25
            "Old Fixed Deposit Recovery",       # 26
            "Senior Citizen Welfare Fund",      # 27
            "Bank Account Reactivation",        # 25
            "Recover Unclaimed Balances",       # 26
            "India Top Asset Recovery Team",    # 29
            "Hassle-Free Bank Liaisoning",      # 27
            "BSE Listed Financial Firm",        # 25
            "Share Samadhan Wealth Help"        # 26
        ],
        "descriptions": [
            "Bank account dormant for 10+ years? Recover funds transferred to RBI's DEAF fund today.", # 88
            "We help reclaim unclaimed fixed deposits, savings balances, and inoperative accounts.",   # 86
            "Recover old mutual fund folios transferred to the Senior Citizen Welfare Fund (SCWF).",  # 86
            "Full verification, legal documentation, and bank coordination by Share Samadhan experts." # 89
        ]
    },
    "Brand_Protection": {
        "final_url": "https://sharesamadhan.com/",
        "path1": "Share-Samadhan",
        "path2": "Official",
        "cpc_bid": 15.0,
        "headlines": [
            "Share Samadhan Official Site",     # 28
            "Share Samadhan Limited",           # 22
            "India #1 Asset Recovery Firm",     # 28
            "BSE Listed Recovery Company",      # 27
            "Pioneers in Wealth Retrieval",     # 28
            "Recover Unclaimed Investments",    # 29
            "14+ Years of Legal Excellence",    # 29
            "Free IEPF Search Database",        # 25
            "Trusted by 10000+ Families",       # 26
            "Transmission & Duplicate LOC",     # 28
            "IEPF Share Claim Specialists",     # 28
            "Over 1000 Cr Assets Unlocked",     # 28
            "Official Share Samadhan Team",     # 28
            "Corporate Wealth Protection",      # 27
            "Contact Share Samadhan Now"        # 26
        ],
        "descriptions": [
            "Share Samadhan Limited (BSE SME) is India's pioneer in unclaimed investment recovery.",  # 87
            "Specialists in IEPF claims, duplicate share issue, share transmission & Demat conversion.", # 89
            "Search your family's unclaimed shares and dividends for free on our official portal.",     # 87
            "Call our advisory team at 8800-33-2200 or request a consultation on our official site."    # 88
        ]
    }
}

# -------------------------------------------------------------
# 2. KEYWORDS DEFINITION
# -------------------------------------------------------------
keywords_list = [
    # IEPF_Core_Recovery
    {"Ad Group": "IEPF_Core_Recovery", "Keyword": "[iepf]", "Match Type": "Exact", "Max CPC": 30.0},
    {"Ad Group": "IEPF_Core_Recovery", "Keyword": "[iepfa]", "Match Type": "Exact", "Max CPC": 30.0},
    {"Ad Group": "IEPF_Core_Recovery", "Keyword": "[iepf portal]", "Match Type": "Exact", "Max CPC": 28.0},
    {"Ad Group": "IEPF_Core_Recovery", "Keyword": "[iepf website]", "Match Type": "Exact", "Max CPC": 25.0},
    {"Ad Group": "IEPF_Core_Recovery", "Keyword": "[iepf claim]", "Match Type": "Exact", "Max CPC": 35.0},
    {"Ad Group": "IEPF_Core_Recovery", "Keyword": '"iepf claim"', "Match Type": "Phrase", "Max CPC": 32.0},
    {"Ad Group": "IEPF_Core_Recovery", "Keyword": '"iepf consultant"', "Match Type": "Phrase", "Max CPC": 40.0},
    {"Ad Group": "IEPF_Core_Recovery", "Keyword": '"iepf share recovery"', "Match Type": "Phrase", "Max CPC": 38.0},
    {"Ad Group": "IEPF_Core_Recovery", "Keyword": '"how to claim shares from iepf"', "Match Type": "Phrase", "Max CPC": 35.0},
    {"Ad Group": "IEPF_Core_Recovery", "Keyword": '"unclaimed shares in iepf"', "Match Type": "Phrase", "Max CPC": 32.0},
    {"Ad Group": "IEPF_Core_Recovery", "Keyword": "[iepfa integrated portal]", "Match Type": "Exact", "Max CPC": 28.0},
    {"Ad Group": "IEPF_Core_Recovery", "Keyword": '"iepfa integrated portal"', "Match Type": "Phrase", "Max CPC": 25.0},
    {"Ad Group": "IEPF_Core_Recovery", "Keyword": "[iepf form 5]", "Match Type": "Exact", "Max CPC": 26.0},
    {"Ad Group": "IEPF_Core_Recovery", "Keyword": '"form iepf 5 claim"', "Match Type": "Phrase", "Max CPC": 26.0},

    # Duplicate_Shares_LOC
    {"Ad Group": "Duplicate_Shares_LOC", "Keyword": "[duplicate share certificate]", "Match Type": "Exact", "Max CPC": 35.0},
    {"Ad Group": "Duplicate_Shares_LOC", "Keyword": '"duplicate share certificate"', "Match Type": "Phrase", "Max CPC": 32.0},
    {"Ad Group": "Duplicate_Shares_LOC", "Keyword": '"how to get duplicate shares"', "Match Type": "Phrase", "Max CPC": 30.0},
    {"Ad Group": "Duplicate_Shares_LOC", "Keyword": '"lost share certificate procedure"', "Match Type": "Phrase", "Max CPC": 35.0},
    {"Ad Group": "Duplicate_Shares_LOC", "Keyword": '"letter of confirmation for shares"', "Match Type": "Phrase", "Max CPC": 35.0},
    {"Ad Group": "Duplicate_Shares_LOC", "Keyword": '"lost physical share certificate"', "Match Type": "Phrase", "Max CPC": 34.0},
    {"Ad Group": "Duplicate_Shares_LOC", "Keyword": '"indemnity bond for duplicate shares"', "Match Type": "Phrase", "Max CPC": 30.0},

    # Transmission_LegalHeir
    {"Ad Group": "Transmission_LegalHeir", "Keyword": "[transmission of shares]", "Match Type": "Exact", "Max CPC": 45.0},
    {"Ad Group": "Transmission_LegalHeir", "Keyword": '"transmission of shares"', "Match Type": "Phrase", "Max CPC": 40.0},
    {"Ad Group": "Transmission_LegalHeir", "Keyword": '"transmission of shares after death"', "Match Type": "Phrase", "Max CPC": 45.0},
    {"Ad Group": "Transmission_LegalHeir", "Keyword": '"claim shares of deceased person"', "Match Type": "Phrase", "Max CPC": 45.0},
    {"Ad Group": "Transmission_LegalHeir", "Keyword": '"transmission of shares without succession certificate"', "Match Type": "Phrase", "Max CPC": 48.0},
    {"Ad Group": "Transmission_LegalHeir", "Keyword": '"legal heir claim shares"', "Match Type": "Phrase", "Max CPC": 42.0},
    {"Ad Group": "Transmission_LegalHeir", "Keyword": '"probate of will shares transmission"', "Match Type": "Phrase", "Max CPC": 45.0},

    # Physical_to_Demat_KYC
    {"Ad Group": "Physical_to_Demat_KYC", "Keyword": "[physical shares to demat]", "Match Type": "Exact", "Max CPC": 35.0},
    {"Ad Group": "Physical_to_Demat_KYC", "Keyword": '"convert physical shares to demat"', "Match Type": "Phrase", "Max CPC": 32.0},
    {"Ad Group": "Physical_to_Demat_KYC", "Keyword": '"signature mismatch in shares"', "Match Type": "Phrase", "Max CPC": 36.0},
    {"Ad Group": "Physical_to_Demat_KYC", "Keyword": '"form isr 1 submission"', "Match Type": "Phrase", "Max CPC": 28.0},
    {"Ad Group": "Physical_to_Demat_KYC", "Keyword": '"name mismatch share certificate aadhaar"', "Match Type": "Phrase", "Max CPC": 35.0},
    {"Ad Group": "Physical_to_Demat_KYC", "Keyword": '"form isr 2 banker attestation"', "Match Type": "Phrase", "Max CPC": 28.0},

    # Bank_Deposits_DEAF
    {"Ad Group": "Bank_Deposits_DEAF", "Keyword": "[unclaimed deposits]", "Match Type": "Exact", "Max CPC": 28.0},
    {"Ad Group": "Bank_Deposits_DEAF", "Keyword": '"unclaimed bank deposits recovery"', "Match Type": "Phrase", "Max CPC": 30.0},
    {"Ad Group": "Bank_Deposits_DEAF", "Keyword": '"rbi deaf account claim"', "Match Type": "Phrase", "Max CPC": 32.0},
    {"Ad Group": "Bank_Deposits_DEAF", "Keyword": '"unclaimed mutual funds recovery"', "Match Type": "Phrase", "Max CPC": 32.0},
    {"Ad Group": "Bank_Deposits_DEAF", "Keyword": '"claim old mutual fund folio"', "Match Type": "Phrase", "Max CPC": 30.0},

    # Brand_Protection
    {"Ad Group": "Brand_Protection", "Keyword": "[share samadhan]", "Match Type": "Exact", "Max CPC": 15.0},
    {"Ad Group": "Brand_Protection", "Keyword": "[sharesamadhan]", "Match Type": "Exact", "Max CPC": 15.0},
    {"Ad Group": "Brand_Protection", "Keyword": "[share samadhan limited]", "Match Type": "Exact", "Max CPC": 15.0},
    {"Ad Group": "Brand_Protection", "Keyword": "[sare samadhan]", "Match Type": "Exact", "Max CPC": 12.0},
    {"Ad Group": "Brand_Protection", "Keyword": "[wealth samadhan]", "Match Type": "Exact", "Max CPC": 15.0},
]

# -------------------------------------------------------------
# 3. BUILD EDITOR COMPLIANT DATAFRAMES
# -------------------------------------------------------------

# --- A. Campaigns & Ad Groups ---
ag_rows = []
for ag_name, details in ad_groups_data.items():
    ag_rows.append({
        "Campaign": CAMPAIGN_NAME,
        "Campaign Daily Budget": BUDGET,
        "Campaign Type": "Search",
        "Networks": "Google search;Search partners",
        "Languages": LANGUAGE,
        "Bid Strategy Type": "Target CPA",
        "Target CPA": TARGET_CPA,
        "Campaign Status": "Paused",
        "Ad Group": ag_name,
        "Max CPC": details["cpc_bid"],
        "Ad Group Status": "Paused"
    })
df_ag = pd.DataFrame(ag_rows)

# --- B. Keywords ---
kw_rows = []
for kw in keywords_list:
    raw_kw = str(kw["Keyword"]).strip()
    clean_kw = raw_kw.strip('"[]')
    m_type = str(kw["Match Type"]).strip()
    kw_rows.append({
        "Campaign": CAMPAIGN_NAME,
        "Ad Group": kw["Ad Group"],
        "Keyword": clean_kw,
        "Match Type": m_type,
        "Criterion Type": "Keyword",
        "Max CPC": kw["Max CPC"],
        "Status": "Paused"
    })
df_kw = pd.DataFrame(kw_rows)

# --- C. Responsive Search Ads (RSAs) ---
rsa_rows = []
for ag_name, details in ad_groups_data.items():
    row = {
        "Campaign": CAMPAIGN_NAME,
        "Ad Group": ag_name,
        "Status": "Paused",
        "Final URL": details["final_url"],
        "Path 1": details["path1"],
        "Path 2": details["path2"]
    }
    for idx, h in enumerate(details["headlines"]):
        row[f"Headline {idx+1}"] = h
    for idx, d in enumerate(details["descriptions"]):
        row[f"Description {idx+1}"] = d
    rsa_rows.append(row)
df_rsa = pd.DataFrame(rsa_rows)

# --- D. Negative Keywords (Campaign Level) ---
neg_master = pd.read_excel(r'data\Share Samadhan\Recommended_Negative_Keywords_Master.xlsx')
neg_rows = []
for _, row in neg_master.iterrows():
    raw_kw = str(row["Negative Keyword"]).strip()
    clean_kw = raw_kw.strip('"[]')
    m_type = str(row["Match Type"]).strip()
    neg_rows.append({
        "Campaign": CAMPAIGN_NAME,
        "Criterion Type": "Campaign Negative Keyword",
        "Keyword": clean_kw,
        "Match Type": m_type,
        "Status": "Active"
    })
df_neg = pd.DataFrame(neg_rows)

# -------------------------------------------------------------
# 4. SAVE CSVs & MASTER WORKBOOK
# -------------------------------------------------------------
base_dir = r'data\Share Samadhan'

df_ag.to_csv(f"{base_dir}\\01_Editor_Campaigns_and_AdGroups.csv", index=False)
df_kw.to_csv(f"{base_dir}\\02_Editor_Keywords.csv", index=False)
df_rsa.to_csv(f"{base_dir}\\03_Editor_Responsive_Search_Ads.csv", index=False)
df_neg.to_csv(f"{base_dir}\\04_Editor_Negative_Keywords.csv", index=False)

# Master Excel Workbook
with pd.ExcelWriter(f"{base_dir}\\Google_Ads_Editor_Import_Package.xlsx", engine="openpyxl") as writer:
    df_ag.to_excel(writer, sheet_name="Ad_Groups", index=False)
    df_kw.to_excel(writer, sheet_name="Keywords", index=False)
    df_rsa.to_excel(writer, sheet_name="Responsive_Search_Ads", index=False)
    df_neg.to_excel(writer, sheet_name="Negative_Keywords", index=False)

# Unified Combined CSV
df_unified = pd.concat([df_ag, df_kw, df_rsa, df_neg], ignore_index=True)
df_unified.to_csv(f"{base_dir}\\Google_Ads_Editor_Unified_Import.csv", index=False)

print("SUCCESS: Updated all files with clean keywords and explicit Match Type column!")

