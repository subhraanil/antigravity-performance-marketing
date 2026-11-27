import pandas as pd
import openpyxl

base_dir = r'data\Share Samadhan'

# ==============================================================================
# CAMPAIGN 1: Search_NRI_Samadhan (High-Ticket Remote Asset Recovery for NRIs)
# ==============================================================================
NRI_CAMPAIGN = "Search_NRI_Samadhan"
NRI_BUDGET = 1500
NRI_TARGET_CPA = 280

nri_ad_groups = {
    "NRI_IEPF_Recovery": {
        "final_url": "https://sharesamadhan.com/nri-samadhan",
        "path1": "NRI-Services",
        "path2": "IEPF-Claim",
        "cpc_bid": 45.0,
        "keywords": [
            {"Keyword": "nri iepf claim", "Match Type": "Exact", "Max CPC": 45.0},
            {"Keyword": "nri iepf claim", "Match Type": "Phrase", "Max CPC": 42.0},
            {"Keyword": "claim iepf shares from abroad", "Match Type": "Phrase", "Max CPC": 45.0},
            {"Keyword": "nri unclaimed dividends india", "Match Type": "Phrase", "Max CPC": 40.0},
            {"Keyword": "how can nri claim iepf shares", "Match Type": "Phrase", "Max CPC": 38.0},
            {"Keyword": "nri unclaimed shares india", "Match Type": "Exact", "Max CPC": 45.0},
            {"Keyword": "nri unclaimed shares india", "Match Type": "Phrase", "Max CPC": 40.0}
        ],
        "headlines": [
            "NRI IEPF Share Recovery",          # 23
            "No Travel to India Needed",       # 25
            "100% Remote Asset Recovery",      # 26
            "Claim IEPF Shares From Abroad",   # 29
            "Recover Indian Dividends",        # 24
            "Form IEPF 5 Assistance NRIs",     # 27
            "India #1 Asset Recovery Firm",    # 28
            "Apostille & Embassy Guidance",    # 28
            "RTA Corporate Liaisoning",        # 24
            "BSE Listed Trusted Experts",      # 26
            "Track Unclaimed Indian Shares",   # 29
            "Fast Remote Documentation",       # 24
            "Legal Support in India",          # 22
            "Check NRI Claim Eligibility",     # 27
            "Share Samadhan NRI Desk"          # 23
        ],
        "descriptions": [
            "Living abroad with shares stuck in IEPF? We handle 100% of recovery with zero travel.",  # 87
            "Complete IEPF-5 filing, RTA liaisoning & corporate verification approval from India.",    # 86
            "We guide you through embassy apostille, banker verification & NRE/NRO Demat credits.",   # 86
            "BSE-listed recovery firm. Over INR 1000+ Cr recovered for global Indian families."        # 85
        ]
    },
    "NRI_Transmission_Ancestral_Estate": {
        "final_url": "https://sharesamadhan.com/nri-samadhan",
        "path1": "NRI-Services",
        "path2": "Transmission",
        "cpc_bid": 50.0,
        "keywords": [
            {"Keyword": "nri share transmission", "Match Type": "Exact", "Max CPC": 50.0},
            {"Keyword": "nri share transmission", "Match Type": "Phrase", "Max CPC": 45.0},
            {"Keyword": "nri claim deceased parents shares in india", "Match Type": "Phrase", "Max CPC": 50.0},
            {"Keyword": "transmission of shares for nri", "Match Type": "Phrase", "Max CPC": 45.0},
            {"Keyword": "nri succession certificate shares india", "Match Type": "Phrase", "Max CPC": 48.0},
            {"Keyword": "ancestral shares claim for nri", "Match Type": "Phrase", "Max CPC": 45.0},
            {"Keyword": "probate of will indian shares nri", "Match Type": "Phrase", "Max CPC": 50.0}
        ],
        "headlines": [
            "NRI Share Transmission",          # 22
            "Inherited Shares in India?",      # 26
            "Claim Deceased Parents Shares",   # 29
            "Zero Travel to India Needed",     # 27
            "100% Remote Transmission",        # 25
            "Shares Without Succession",       # 25
            "Legal Heir Claims for NRIs",      # 26
            "Probate of Will Share Claims",    # 28
            "Consular Attestation Guidance",   # 29
            "Family Estate Settlement",        # 24
            "India Top Inheritance Experts",   # 29
            "BSE Listed Legal Advisory",       # 25
            "Smooth Indian Estate Claim",      # 26
            "Complete Legal Documentation",    # 28
            "Share Samadhan NRI Desk"          # 23
        ],
        "descriptions": [
            "Inherited shares of late parents in India? Claim rightful wealth without visiting India.",# 89
            "We manage Indian court paperwork, succession certificates, legal heir NOCs & RTA filings.",# 90
            "Complete assistance for overseas Indians: power of attorney, apostille, and Demat credit.",# 90
            "India's largest asset retrieval firm. Trusted by thousands of NRI families globally."      # 86
        ]
    },
    "NRI_Physical_to_Demat_KYC": {
        "final_url": "https://sharesamadhan.com/nri-samadhan",
        "path1": "NRI-Services",
        "path2": "Demat-KYC",
        "cpc_bid": 40.0,
        "keywords": [
            {"Keyword": "nri physical shares to demat", "Match Type": "Exact", "Max CPC": 40.0},
            {"Keyword": "convert indian physical shares to demat nri", "Match Type": "Phrase", "Max CPC": 40.0},
            {"Keyword": "nri demat account for physical shares", "Match Type": "Phrase", "Max CPC": 38.0},
            {"Keyword": "nri signature mismatch indian shares", "Match Type": "Phrase", "Max CPC": 40.0},
            {"Keyword": "form isr for nri", "Match Type": "Phrase", "Max CPC": 35.0},
            {"Keyword": "nro demat account physical shares", "Match Type": "Phrase", "Max CPC": 38.0}
        ],
        "headlines": [
            "Convert Indian Paper Shares",     # 26
            "NRI Physical Shares to Demat",    # 28
            "Paper to Demat From Abroad",      # 26
            "No India Visit Required",         # 23
            "Signature Mismatch Solution",     # 27
            "Form ISR 1 2 4 for NRIs",         # 23
            "Name Mismatch Share & Passport",  # 30
            "Unfreeze Old Indian Shares",      # 26
            "SEBI Demat Conversion Help",      # 26
            "NRE NRO Demat Account Support",   # 29
            "Overseas KYC Attestation",        # 24
            "BSE Listed Advisory Firm",        # 24
            "Fast Remote Demat Process",       # 25
            "RTA Query Resolution",            # 21
            "Share Samadhan Demat Desk"        # 25
        ],
        "descriptions": [
            "Physical paper shares can no longer be sold. Dematerialize into your NRE/NRO Demat now.",  # 88
            "Signature mismatch or maiden name change? We resolve all RTA objections remotely.",       # 84
            "End-to-end Form ISR filings, KYC regularization & embassy attestation guidance for NRIs.", # 89
            "Avoid mandatory IEPF forfeiture. Protect and convert your physical shares today."         # 83
        ]
    },
    "NRI_Duplicate_Shares_LOC": {
        "final_url": "https://sharesamadhan.com/nri-samadhan",
        "path1": "NRI-Services",
        "path2": "Duplicate-LOC",
        "cpc_bid": 40.0,
        "keywords": [
            {"Keyword": "nri duplicate share certificate", "Match Type": "Exact", "Max CPC": 40.0},
            {"Keyword": "nri lost share certificate india", "Match Type": "Phrase", "Max CPC": 40.0},
            {"Keyword": "duplicate shares procedure for nri", "Match Type": "Phrase", "Max CPC": 38.0},
            {"Keyword": "letter of confirmation nri shares", "Match Type": "Phrase", "Max CPC": 38.0},
            {"Keyword": "lost indian shares recovery nri", "Match Type": "Phrase", "Max CPC": 38.0}
        ],
        "headlines": [
            "NRI Duplicate Share Help",        # 24
            "Lost Indian Share Certificate",   # 29
            "Get Duplicate Shares in India",   # 29
            "No Travel to India Needed",       # 25
            "SEBI Letter of Confirmation",     # 27
            "Paper Certificate Stolen/Lost",   # 29
            "FIR & Newspaper Notice India",    # 28
            "Indemnity Bond for NRIs",         # 23
            "100% Remote Asset Recovery",      # 26
            "India Top Recovery Advisory",     # 27
            "Hassle-Free RTA Coordination",    # 28
            "BSE Listed Trusted Experts",      # 26
            "Recover Lost Physical Shares",    # 28
            "Fast Duplicate Issue Support",    # 28
            "Share Samadhan NRI Desk"          # 23
        ],
        "descriptions": [
            "Lost or damaged paper certificates of Indian companies? We obtain duplicate shares (LOC).",# 89
            "We handle Indian police FIR reporting, newspaper notices, and RTA indemnity instruments.", # 89
            "Zero travel to India required. Seamless execution for NRIs in USA, UK, UAE & worldwide.",  # 89
            "Reclaim your valuable equity holdings. Contact Share Samadhan's dedicated NRI division."   # 89
        ]
    },
    "NRI_Bank_Accounts_NRE_NRO": {
        "final_url": "https://sharesamadhan.com/nri-samadhan",
        "path1": "NRI-Services",
        "path2": "Bank-Accounts",
        "cpc_bid": 35.0,
        "keywords": [
            {"Keyword": "nri inoperative bank account", "Match Type": "Exact", "Max CPC": 35.0},
            {"Keyword": "dormant nre account recovery", "Match Type": "Phrase", "Max CPC": 35.0},
            {"Keyword": "dormant nro account recovery", "Match Type": "Phrase", "Max CPC": 35.0},
            {"Keyword": "unclaimed bank deposits in india for nri", "Match Type": "Phrase", "Max CPC": 35.0},
            {"Keyword": "rbi deaf claim for nri", "Match Type": "Phrase", "Max CPC": 32.0}
        ],
        "headlines": [
            "NRI Inoperative Bank Accounts",   # 29
            "Dormant NRE NRO Account Help",    # 28
            "Recover Indian Bank Deposits",    # 28
            "RBI DEAF Account Claim NRI",      # 26
            "Unclaimed FDs in Indian Banks",   # 29
            "Reactivate Inactive Bank Ac",     # 27
            "Zero Travel to India Needed",     # 27
            "Forgotten Indian Bank Balances",  # 30
            "Full Bank Liaisoning in India",   # 29
            "100% Remote Legal Recovery",      # 26
            "BSE Listed Trusted Experts",      # 26
            "India #1 Asset Retrieval Firm",   # 29
            "Fast Remote Documentation",       # 24
            "Check Bank Claim Eligibility",    # 28
            "Share Samadhan NRI Desk"          # 23
        ],
        "descriptions": [
            "Dormant bank account in India? Recover funds from RBI's DEAF fund with zero travel.",       # 83
            "We coordinate with SBI, HDFC, ICICI & nationalized banks across India on your behalf.",    # 86
            "Full legal paperwork, overseas KYC verification & credit into active NRE/NRO accounts.",   # 88
            "Reclaim forgotten deposits and ancestral bank balances without flying to India."           # 81
        ]
    }
}

# ==============================================================================
# CAMPAIGN 2: Search_PF_Provident_Fund (Conservative Budget, Targeted Recovery)
# ==============================================================================
PF_CAMPAIGN = "Search_PF_Provident_Fund"
PF_BUDGET = 400
PF_TARGET_CPA = 120

pf_ad_groups = {
    "PF_Withdrawal_Claim_Help": {
        "final_url": "https://sharesamadhan.com/unclaimed-provident-funds",
        "path1": "PF-Services",
        "path2": "Claim-Help",
        "cpc_bid": 22.0,
        "keywords": [
            {"Keyword": "unclaimed pf claim", "Match Type": "Exact", "Max CPC": 22.0},
            {"Keyword": "unclaimed pf recovery", "Match Type": "Phrase", "Max CPC": 22.0},
            {"Keyword": "stuck pf claim help", "Match Type": "Phrase", "Max CPC": 22.0},
            {"Keyword": "pf claim rejected help", "Match Type": "Phrase", "Max CPC": 20.0},
            {"Keyword": "employer denying to sign pf", "Match Type": "Phrase", "Max CPC": 22.0},
            {"Keyword": "previous company closed pf withdrawal", "Match Type": "Phrase", "Max CPC": 22.0},
            {"Keyword": "how to withdraw old pf money", "Match Type": "Phrase", "Max CPC": 20.0},
            {"Keyword": "epf claim rejected assistance", "Match Type": "Phrase", "Max CPC": 20.0}
        ],
        "headlines": [
            "Unclaimed PF Recovery Help",      # 25
            "Stuck Provident Fund Claim?",     # 27
            "Old Company Denying PF?",         # 24
            "Recover Trapped PF Balance",      # 26
            "EPF Claim Rejected Support",      # 26
            "Company Closed? Get Your PF",     # 27
            "PF Withdrawal Assistance",        # 25
            "Trace Forgotten PF Funds",        # 24
            "Resolve Old PF Rejections",       # 25
            "Fast PF Documentation Support",   # 29
            "Legal Assistance for EPF",        # 25
            "100% Trusted Legal Process",      # 26
            "BSE Listed Financial Advisory",   # 29
            "Check PF Claim Eligibility",      # 26
            "Share Samadhan PF Desk"           # 22
        ],
        "descriptions": [
            "Facing PF rejection, or previous employer refusing to sign? We resolve stuck EPF claims.", # 88
            "Recover unclaimed provident funds from previous untraceable or closed companies in India.",# 90
            "Complete legal documentation, employer liaisoning & EPF grievance escalation support.",    # 86
            "Consult Share Samadhan experts today. Hassle-free recovery of your hard-earned PF."        # 84
        ]
    },
    "PF_UAN_Consolidation_Issues": {
        "final_url": "https://sharesamadhan.com/unclaimed-provident-funds",
        "path1": "PF-Services",
        "path2": "UAN-Support",
        "cpc_bid": 20.0,
        "keywords": [
            {"Keyword": "inactive uan resolution", "Match Type": "Exact", "Max CPC": 20.0},
            {"Keyword": "inactive uan pf withdrawal", "Match Type": "Phrase", "Max CPC": 20.0},
            {"Keyword": "forgot pf number company closed", "Match Type": "Phrase", "Max CPC": 20.0},
            {"Keyword": "merge multiple uan accounts", "Match Type": "Phrase", "Max CPC": 20.0},
            {"Keyword": "uan not generated old company pf", "Match Type": "Phrase", "Max CPC": 18.0},
            {"Keyword": "consolidate multiple member id epfo", "Match Type": "Phrase", "Max CPC": 18.0},
            {"Keyword": "old epf account without uan", "Match Type": "Phrase", "Max CPC": 18.0}
        ],
        "headlines": [
            "Inactive UAN Issue Resolved",     # 27
            "Cannot Remember Your UAN?",       # 25
            "Merge Multiple UAN Accounts",     # 27
            "Old PF Without UAN Number?",      # 26
            "Consolidate Member IDs",          # 22
            "Previous Company Denying UAN",    # 28
            "Recover Old Forgotten PF",        # 24
            "PF Account Transfer Support",     # 27
            "Resolve Dual UAN Issues",         # 23
            "EPFO UAN KYC Rectification",      # 26
            "Fast Documentation Assistance",   # 29
            "India Trusted Recovery Team",     # 27
            "BSE Listed Advisory Experts",     # 27
            "Check UAN Eligibility Today",     # 27
            "Share Samadhan UAN Help"          # 23
        ],
        "descriptions": [
            "Inactive UAN or forgot your PF member ID? We help trace and reactivate old PF accounts.",  # 88
            "Merge multiple EPF member IDs into a single active UAN without employer hurdles.",         # 82
            "End-to-end EPFO grievance coordination, joint declarations & KYC data rectification.",     # 87
            "Get your trapped retirement funds back. Talk to Share Samadhan's provident fund team."     # 87
        ]
    }
}

# ==============================================================================
# FUNCTION TO COMPILE CAMPAIGN ARTIFACTS
# ==============================================================================
def compile_campaign(camp_name, budget, target_cpa, ad_groups_dict, custom_negatives=None):
    ag_rows, kw_rows, rsa_rows, neg_rows = [], [], [], []
    
    # 1. Ad Groups
    for ag_name, details in ad_groups_dict.items():
        ag_rows.append({
            "Campaign": camp_name,
            "Campaign Daily Budget": budget,
            "Campaign Type": "Search",
            "Networks": "Google search;Search partners",
            "Languages": "en;hi",
            "Bid Strategy Type": "Target CPA",
            "Target CPA": target_cpa,
            "Campaign Status": "Paused",
            "Ad Group": ag_name,
            "Max CPC": details["cpc_bid"],
            "Ad Group Status": "Paused"
        })
        
        # 2. Keywords
        for kw in details["keywords"]:
            kw_rows.append({
                "Campaign": camp_name,
                "Ad Group": ag_name,
                "Keyword": kw["Keyword"],
                "Match Type": kw["Match Type"],
                "Criterion Type": "Keyword",
                "Max CPC": kw["Max CPC"],
                "Status": "Paused"
            })
            
        # 3. RSAs
        rsa_row = {
            "Campaign": camp_name,
            "Ad Group": ag_name,
            "Status": "Paused",
            "Final URL": details["final_url"],
            "Path 1": details["path1"],
            "Path 2": details["path2"]
        }
        for idx, h in enumerate(details["headlines"]):
            rsa_row[f"Headline {idx+1}"] = h
        for idx, d in enumerate(details["descriptions"]):
            rsa_row[f"Description {idx+1}"] = d
        rsa_rows.append(rsa_row)

    # 4. Negatives
    neg_master = pd.read_excel(r'data\Share Samadhan\Recommended_Negative_Keywords_Master.xlsx')
    for _, row in neg_master.iterrows():
        neg_rows.append({
            "Campaign": camp_name,
            "Criterion Type": "Campaign Negative Keyword",
            "Keyword": str(row["Negative Keyword"]).strip('"[]'),
            "Match Type": str(row["Match Type"]).strip(),
            "Status": "Active"
        })
    if custom_negatives:
        for cn in custom_negatives:
            neg_rows.append({
                "Campaign": camp_name,
                "Criterion Type": "Campaign Negative Keyword",
                "Keyword": cn["Keyword"],
                "Match Type": cn["Match Type"],
                "Status": "Active"
            })

    df_ag = pd.DataFrame(ag_rows)
    df_kw = pd.DataFrame(kw_rows)
    df_rsa = pd.DataFrame(rsa_rows)
    df_neg = pd.DataFrame(neg_rows)
    df_unified = pd.concat([df_ag, df_kw, df_rsa, df_neg], ignore_index=True)
    return df_ag, df_kw, df_rsa, df_neg, df_unified

# Additional negatives for PF campaign (avoid routine passbook lookups)
pf_extra_negatives = [
    {"Keyword": "member login", "Match Type": "Phrase"},
    {"Keyword": "uan login", "Match Type": "Phrase"},
    {"Keyword": "passbook login", "Match Type": "Phrase"},
    {"Keyword": "epfo login", "Match Type": "Phrase"},
    {"Keyword": "pf balance check", "Match Type": "Phrase"},
    {"Keyword": "download umang app", "Match Type": "Phrase"},
    {"Keyword": "umang app", "Match Type": "Phrase"},
    {"Keyword": "epfigms portal", "Match Type": "Phrase"},
    {"Keyword": "epfo passbook view", "Match Type": "Phrase"}
]

# Compile NRI Campaign
nri_ag, nri_kw, nri_rsa, nri_neg, nri_unified = compile_campaign(
    NRI_CAMPAIGN, NRI_BUDGET, NRI_TARGET_CPA, nri_ad_groups
)
nri_unified.to_csv(f"{base_dir}\\05_Editor_Campaign_NRI_Samadhan.csv", index=False)

# Compile PF Campaign
pf_ag, pf_kw, pf_rsa, pf_neg, pf_unified = compile_campaign(
    PF_CAMPAIGN, PF_BUDGET, PF_TARGET_CPA, pf_ad_groups, pf_extra_negatives
)
pf_unified.to_csv(f"{base_dir}\\06_Editor_Campaign_PF_Services.csv", index=False)

# Load existing core campaign
core_unified = pd.read_csv(f"{base_dir}\\Google_Ads_Editor_Unified_Import.csv")

# Combine ALL 3 Campaigns into a Master All-Campaigns Import CSV
all_campaigns_unified = pd.concat([core_unified, nri_unified, pf_unified], ignore_index=True)
all_campaigns_unified.to_csv(f"{base_dir}\\Google_Ads_Editor_All_Campaigns_Master.csv", index=False)

# Update Master Excel Workbook with distinct sheets for each campaign
with pd.ExcelWriter(f"{base_dir}\\Google_Ads_Editor_All_Campaigns_Master.xlsx", engine="openpyxl") as writer:
    core_unified.to_excel(writer, sheet_name="Core_Services_Campaign", index=False)
    nri_unified.to_excel(writer, sheet_name="NRI_Samadhan_Campaign", index=False)
    pf_unified.to_excel(writer, sheet_name="PF_Provident_Fund_Campaign", index=False)
    all_campaigns_unified.to_excel(writer, sheet_name="All_Campaigns_Unified", index=False)

print(f"SUCCESS: Generated NRI Campaign ({len(nri_unified)} rows), PF Campaign ({len(pf_unified)} rows), and Master All-Campaigns CSV ({len(all_campaigns_unified)} rows)!")
