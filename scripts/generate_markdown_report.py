import pandas as pd
import os

reports_dir = r'C:\Users\test\Videos\Office\reports'
df_m = pd.read_csv(f'{reports_dir}/Share_Samadhan_Monthly_Leads_Summary.csv')
p_s = pd.read_csv(f'{reports_dir}/Share_Samadhan_Monthly_Service_Matrix.csv', index_col=0)
p_c = pd.read_csv(f'{reports_dir}/Share_Samadhan_Monthly_Source_Matrix.csv', index_col=0)
df_serv = pd.read_csv(f'{reports_dir}/Share_Samadhan_Service_Summary.csv')
df_src = pd.read_csv(f'{reports_dir}/Share_Samadhan_Source_Summary.csv')

total_leads = df_m['Total Leads'].sum()
total_nri = df_m['No of NRI Leads'].sum()
overall_nri_share = round(total_nri / total_leads * 100, 2)

lines = []
lines.append("# Share Samadhan: Annual Lead Generation & Source Analysis (Nov 2025 – Nov 2026)")
lines.append("")
lines.append(f"**Date Range**: November 1, 2025 – November 23, 2026 (13 Months)  ")
lines.append(f"**Total Leads Generated**: **{total_leads:,}**  ")
lines.append(f"**Total NRI Leads Generated**: **{total_nri:,}** ({overall_nri_share}% of all inbound inquiries)  ")
lines.append(f"**Primary Lead Acquisition Channels**: Google Ads / Search (34.4%), WhatsApp Chatbot (21.3%), Facebook / Meta Ads (20.6%), Supervisor Panel / Inbound Calls (12.4%)  ")
lines.append(f"**Data Source**: `C:\\Users\\test\\Videos\\Office\\data\\Share Samadhan\\All_Enquiry_List_2026.11.23.06.28.18.csv`  ")
lines.append(f"**Deliverable Output**: [Share_Samadhan_Annual_Leads_Analysis_Nov2025_Nov2026.xlsx](file:///C:/Users/test/Videos/Office/reports/Share_Samadhan_Annual_Leads_Analysis_Nov2025_Nov2026.xlsx)  ")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 1. Master Monthly Lead Summary Table")
lines.append("")
lines.append("This table provides the exact month-by-month breakdown requested: Month, Total Leads, Top Service Categories sought by clients, and Number of NRI Leads.")
lines.append("")
lines.append("| Month | Total Leads | Primary Service Categories (Volume) | No of NRI Leads | NRI Share % | Top Lead Sources (Channels) |")
lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")

for _, r in df_m.iterrows():
    m_name = r['Month Name']
    ym = r['Month']
    tot = f"{int(r['Total Leads']):,}"
    services = r['Top Service Categories (Volume)']
    nri = f"{int(r['No of NRI Leads']):,}"
    nri_pct = f"{r['NRI Share %']}%"
    src = r['Top Lead Sources']
    lines.append(f"| **{m_name}** (`{ym}`) | **{tot}** | {services} | **{nri}** | {nri_pct} | {src} |")

lines.append(f"| **TOTAL (13 Months)** | **{total_leads:,}** | **Equity & IEPF Share Recovery (61.2%), Inbound Direct (17.4%), Demat (11.1%)** | **{total_nri:,}** | **{overall_nri_share}%** | **Google (34.4%), WhatsApp (21.3%), Meta (20.6%)** |")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 2. Service Category Breakdown (Annual Totals)")
lines.append("")
lines.append("| Service Category | Total Leads | Share of Total (%) | NRI Leads | NRI Concentration (%) | Primary Lead Channels |")
lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")

for _, r in df_serv.iterrows():
    serv = r['Service_Category']
    tot = f"{int(r['Total_Leads']):,}"
    sh = f"{r['Share_%']}%"
    nri = f"{int(r['NRI_Leads']):,}"
    nri_sh = f"{r['NRI_Share_%']}%"
    lines.append(f"| **{serv}** | {tot} | {sh} | {nri} | {nri_sh} | High Intent |")

lines.append("")
lines.append("---")
lines.append("")
lines.append("## 3. Lead Acquisition Sources & Marketing Channels")
lines.append("")
lines.append("| Acquisition Channel | Total Leads | Share of Total (%) | NRI Leads | NRI Share (%) | Channel Role & Strategic Insight |")
lines.append("| :--- | :--- | :--- | :--- | :--- | :--- |")

for _, r in df_src.iterrows():
    ch = r['Lead_Channel']
    tot = f"{int(r['Total_Leads']):,}"
    sh = f"{r['Share_%']}%"
    nri = f"{int(r['NRI_Leads']):,}"
    nri_sh = f"{r['NRI_Share_%']}%"
    lines.append(f"| **{ch}** | {tot} | {sh} | {nri} | {nri_sh} | Primary Source |")

lines.append("")
lines.append("---")
lines.append("")
lines.append("## 4. Month-by-Month Lead Source Matrix")
lines.append("")
lines.append("This matrix displays lead acquisition trends across all channels for each month from November 2025 to November 2026:")
lines.append("")

# Format pivot_channel into markdown
headers = ["Month", "Google Ads", "WhatsApp Chatbot", "Meta / Facebook", "Supervisor / Calls", "Contact Us", "Landing Pages", "Service Pages", "NRI Landing", "Microsites & Blog", "Total"]
lines.append("| " + " | ".join(headers) + " |")
lines.append("| " + " | ".join([":---"] * len(headers)) + " |")

for ym in p_c.index:
    if ym == 'Total':
        label = "**Total**"
    else:
        label = f"`{ym}`"
    g = f"{p_c.loc[ym, 'Google Ads / Search']:,}"
    w = f"{p_c.loc[ym, 'WhatsApp Chatbot (Anantya & Interakt)']:,}"
    f = f"{p_c.loc[ym, 'Facebook / Meta Ads']:,}"
    s = f"{p_c.loc[ym, 'Supervisor Panel / Inbound Calls & Associates']:,}"
    c = f"{p_c.loc[ym, 'Website Contact Us Page']:,}"
    l = f"{p_c.loc[ym, 'Direct / Organic Landing Page']:,}"
    sp = f"{p_c.loc[ym, 'Website Service Pages']:,}"
    n = f"{p_c.loc[ym, 'NRI Landing Page']:,}"
    mb = f"{(p_c.loc[ym, 'Microsites (LostShare / IEPFClaim)'] + p_c.loc[ym, 'Website Blog Page']):,}"
    tot = f"{p_c.loc[ym, 'Total']:,}"
    lines.append(f"| {label} | {g} | {w} | {f} | {s} | {c} | {l} | {sp} | {n} | {mb} | **{tot}** |")

lines.append("")
lines.append("---")
lines.append("")
lines.append("## 5. Strategic Highlights & Operational Insights")
lines.append("")
lines.append("1. **Peak Lead Months**: ")
lines.append("   - **July 2026** was the highest volume month (**1,919 leads**), driven by a surge in Google Search (725 leads) and WhatsApp chatbot adoption (626 leads).")
lines.append("   - **September 2026** generated **1,815 leads**, followed by **June 2026** with **1,664 leads**.")
lines.append("2. **Core Revenue Drivers**: ")
lines.append("   - **Equity & IEPF Share Retrieval** forms the bedrock of customer demand (**61.2% / 10,878 leads** across IEPF Claim, Shares Recovery, and Lost Shares WhatsApp).")
lines.append("   - **Physical Shares to Demat** is a rapidly scaling vertical (**1,974 leads / 11.1%**), accelerated by SEBI KYC compliance mandates.")
lines.append("3. **Cross-Border NRI Traction**: ")
lines.append("   - **456 Total NRI Leads (2.56%)** were generated over the 13-month period.")
lines.append("   - While 87 came directly via the NRI Landing Page, **137 NRI leads originated via Google Search** and **88 through inbound calls/associates**, confirming that overseas Indians are actively searching on Google and calling the desk.")
lines.append("   - Highest NRI volumes occurred in **December 2025 (53 leads)**, **January 2026 (50 leads)**, and **April 2026 (49 leads)**.")
lines.append("4. **Digital Channel Dominance**: ")
lines.append("   - **Google Ads & Organic Search** is the single largest lead channel (**6,113 leads / 34.4%**).")
lines.append("   - **WhatsApp Automation (Anantya.ai & Interakt)** grew aggressively from mid-2026 to become the #2 channel (**3,786 leads / 21.3%**).")
lines.append("   - **Meta / Facebook Ads** delivered steady top-of-funnel discovery (**3,662 leads / 20.6%**).")

output_md_path = os.path.join(reports_dir, 'Share_Samadhan_Annual_Leads_Report_Nov2025_Nov2026.md')
with open(output_md_path, 'w', encoding='utf-8') as f:
    f.write("\n".join(lines))

print(f"Report written to: {output_md_path}")
