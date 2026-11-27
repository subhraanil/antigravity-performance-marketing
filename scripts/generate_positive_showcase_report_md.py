import pandas as pd
import numpy as np
import os

base_dir = r'C:/Users/test/Videos/Office/data/Share Samadhan'
reports_dir = r'C:/Users/test/Videos/Office/reports'
case_studies_dir = r'C:/Users/test/Videos/Office/case-studies/Share Samadhan'

# Load paid & ga data
f_cost = os.path.join(base_dir, 'Share Samadhan - Nov 2025 to Nov 2026.xlsx')
xl = pd.ExcelFile(f_cost)

df_raw_cost = xl.parse('Total CostLeads', skiprows=1)
paid_cols = [
    'Month', 'Google_Impressions', 'Google_Clicks', 'Google_Leads', 'Google_Spend', 'Google_CPL',
    'Meta_Impressions', 'Meta_Clicks', 'Meta_Leads', 'Meta_Spend', 'Meta_CPL',
    'Total_Impressions', 'Total_Clicks', 'Total_Paid_Leads', 'Total_Paid_Spend', 'Blended_CPL'
]
df_paid = df_raw_cost.iloc[:13, :16].copy()
df_paid.columns = paid_cols
df_paid['Month_Label'] = pd.to_datetime(df_paid['Month']).dt.strftime('%B %Y')
df_paid['YearMonth'] = pd.to_datetime(df_paid['Month']).dt.strftime('%Y-%m')

df_raw_ga = xl.parse('Google Analytics Traffic Report')
df_ga = df_raw_ga.iloc[:13].copy()
df_ga['Month_Label'] = pd.to_datetime(df_ga['Months']).dt.strftime('%B %Y')
df_ga['YearMonth'] = pd.to_datetime(df_ga['Months']).dt.strftime('%Y-%m')

lines = []
lines.append("# Share Samadhan Limited: Annual Performance Showcase & Positive Growth Report")
lines.append("## Executive Highlights Across Paid Media, SEO Domination, GA4 Traffic & Omnichannel Scale")
lines.append("")
lines.append("**Reporting Period**: November 1, 2025 – November 23, 2026 (13 Months)  ")
lines.append("**Client**: Share Samadhan Limited (BSE SME: `SHARESAM`)  ")
lines.append("**Primary Files Analyzed**:  ")
lines.append("1. `Share Samadhan - Nov 2025 to Nov 2026.xlsx` (Google Ads, Meta Ads & GA4 Traffic)  ")
lines.append("2. `Nov-1-2025-to-Nov-23-2026.xlsx` (Meta Ad Set Level Granular Performance)  ")
lines.append("3. `Comparison Report.pdf` (Multi-Platform SEO, GSC, Social Media & Content KPIs)  ")
lines.append("4. `All_Enquiry_List_2026.11.23.06.28.18.csv` (17,782 Verified CRM Lead Records)  ")
lines.append("**Deliverable Output**: [Share_Samadhan_Positive_Performance_Metrics.xlsx](file:///C:/Users/test/Videos/Office/reports/Share_Samadhan_Positive_Performance_Metrics.xlsx)  ")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 1. Executive Scorecard: 10 Major Growth Milestones")
lines.append("")
lines.append("| Performance Pillar | Baseline / Start (Nov 2025) | Peak / Current Performance | Net Improvement / Milestone |")
lines.append("| :--- | :--- | :--- | :--- |")
lines.append("| **1. Total Inbound Leads** | 1,090 leads / mo | **1,919 leads / mo** (July 2026) | **+76.1% Overall Volume Growth** (**17,782 Total Leads**) |")
lines.append("| **2. Paid Media Leads (Google + Meta)** | 440 leads / mo | **1,689 leads / mo** (October 2026) | **+283.9% Growth (Nearly 4x Scale)** (**12,655 Paid Leads**) |")
lines.append("| **3. Blended Cost Per Lead (CPL)** | ₹141.23 – ₹180.11 | **₹54.98 – ₹55.72** | **-60.5% to -69.5% CPL Reduction** (Over ₹125 saved per lead) |")
lines.append("| **4. Meta Ads CPL Revolution** | ₹161.58 – ₹287.65 | **₹32.74** (October 2026) | **-88.6% Reduction in Meta Acquisition Cost** (6,492 leads total) |")
lines.append("| **5. Google Ads Lead Scale** | 208 leads / mo | **775 leads / mo** (July 2026) | **+272.6% Lead Scale** with CPL dropping from ₹123.68 to **₹58.45** |")
lines.append("| **6. Google Search Console Reach** | Baseline | **3.09 Million Impressions** | **44.1K High-Intent Organic Clicks** from searchers |")
lines.append("| **7. Google Organic Search Ranking** | Baseline | **Average Position 7.1** | **72 Keywords on Page 1 of Google (Top 10 Rankings)** |")
lines.append("| **8. Total Website Audience (GA4)** | Baseline | **165,849 Total Users** | **161,491 New Users Acquired** (97.4% fresh market reach) |")
lines.append("| **9. High-Value Organic Leads** | Baseline | **2,685 Organic Search Leads** | **6.71% Organic Visitor-to-Lead Conversion Rate** |")
lines.append("| **10. Social Media Engagement** | Baseline | **+103.7% Instagram Interactions** | **1.9M Video Views**, **73.8K LinkedIn Reach**, **96.7K YouTube Views** |")
lines.append("")
lines.append("```mermaid")
lines.append("xychart-beta")
lines.append("    title \"Monthly Paid Lead Volume Scale vs Cost Per Lead (CPL) Compression\"")
lines.append("    x-axis [\"Nov 25\", \"Dec 25\", \"Jan 26\", \"Feb 26\", \"Mar 26\", \"Apr 26\", \"May 26\", \"Jun 26\", \"Jul 26\", \"Aug 26\", \"Sep 26\", \"Oct 26\", \"Nov 26\"]")
lines.append("    y-axis \"Paid Leads Generated\" 0 --> 1800")
lines.append("    bar [440, 523, 599, 558, 661, 994, 968, 1216, 1516, 1006, 1480, 1689, 1005]")
lines.append("```")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 2. Paid Media Performance Deep Dive: The 4x Scale & Efficiency Story")
lines.append("")
lines.append("The combined paid media strategy across Google Ads and Meta Ads achieved unprecedented scaling while simultaneously compressing costs. Over the 13 months, paid campaigns delivered **12,655 verified leads** for **₹11,17,331.26**, achieving an overall blended CPL of only **₹88.29**.")
lines.append("")
lines.append("### Full Monthly Paid Media Breakdown Table")
lines.append("")
lines.append("| Month | Google Leads | Google Spend (₹) | Google CPL (₹) | Meta Leads | Meta Spend (₹) | Meta CPL (₹) | Total Paid Leads | Total Spend (₹) | Blended CPL (₹) |")
lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")

for _, r in df_paid.iterrows():
    m = r['Month_Label']
    gl = f"{int(r['Google_Leads']):,}"
    gs = f"₹{r['Google_Spend']:,.2f}"
    gc = f"₹{r['Google_CPL']:.2f}"
    ml = f"{int(r['Meta_Leads']):,}"
    ms = f"₹{r['Meta_Spend']:,.2f}"
    mc = f"₹{r['Meta_CPL']:.2f}"
    tl = f"{int(r['Total_Paid_Leads']):,}"
    ts = f"₹{r['Total_Paid_Spend']:,.2f}"
    bc = f"₹{r['Blended_CPL']:.2f}"
    lines.append(f"| **{m}** | {gl} | {gs} | {gc} | {ml} | {ms} | {mc} | **{tl}** | **{ts}** | **{bc}** |")

lines.append(f"| **TOTAL / AVG** | **6,163** | **₹5,92,976.88** | **₹96.22** | **6,492** | **₹5,24,354.38** | **₹46.53** | **12,655** | **₹11,17,331.26** | **₹88.29** |")
lines.append("")
lines.append("### Key Paid Media Achievements:")
lines.append("1. **Continuous CPL Compression**:")
lines.append("   - At the beginning of the engagement, leads were costing between **₹141.23 (Nov 2025)** and **₹180.11 (Dec 2025)**.")
lines.append("   - Through audience refinement, creative testing, and negative keyword pruning, CPL steadily declined every quarter: falling to **₹108.67 by April**, **₹82.72 by June**, **₹54.98 by July**, and reaching **₹55.72 in October 2026**.")
lines.append("2. **Meta Ads Breakthrough (-88.6% CPL Reduction)**:")
lines.append("   - Meta Ads underwent a fundamental performance transformation. By shifting budget into the highly responsive `New Leads ad set` (automated WhatsApp & Messenger conversations) and `Leads ad set - 7.11.25 – Copy`, Meta CPL crashed from **₹287.65 down to ₹32.74** in October 2026.")
lines.append("   - In October alone, Meta Ads generated **1,016 leads for just ₹33,260.77**.")
lines.append("3. **Google Ads Scaling (+272% Volume)**:")
lines.append("   - Google Ads scaled from 208 leads to a peak of **775 leads in July 2026**.")
lines.append("   - Google Ads CPL reached a record low of **₹58.45** in July 2026, delivering high-intent investors directly to Share Samadhan's specialized recovery desks.")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 3. SEO & Google Search Console Domination: 3.09M Impressions & 72 First-Page Keywords")
lines.append("")
lines.append("The organic search campaign delivered exceptional search visibility, establishing Share Samadhan as the undisputed authoritative brand on Google Search.")
lines.append("")
lines.append("### Key Organic Milestones (Google Search Console):")
lines.append("- **Total Organic Impressions**: **3,090,000+ (3.09 Million)** impressions generated across Google Search.")
lines.append("- **Total Organic Clicks**: **44,100 (44.1K)** high-intent organic clicks captured.")
lines.append("- **First Page Ranking Average**: Maintained an **Average Position of 7.1** across all tracked search queries.")
lines.append("- **Top 10 Rankings (Page 1)**: **72 Keywords actively ranking on Page 1 of Google**, with an additional 20 keywords on Page 2 and 16 on Page 3.")
lines.append("")
lines.append("### Top Organic Search Queries (Branded & High Intent):")
lines.append("| Query | Organic Clicks | Organic Impressions | CTR | Strategic Significance |")
lines.append("| :--- | :--- | :--- | :--- | :--- |")
lines.append("| `Share Samadhan` | **5,093** | 8,861 | **57.5%** | Absolute branded search monopoly |")
lines.append("| `Share Samadhan Ltd` | **865** | 1,915 | **45.2%** | High-intent corporate entity search |")
lines.append("| `Sharesamadhan` | **604** | 1,054 | **57.3%** | Phonetic brand variation dominance |")
lines.append("| `IEPF` & `IEPF Portal` | High Volume | 100K+ | Growth Target | Massive organic visibility driving discovery |")
lines.append("")
lines.append("### Technical SEO Deliverables Executed:")
lines.append("- **34 Authoritative Blogs Published**: Addressing complex regulatory topics (IEPF-5 procedures, physical-to-Demat conversion, deceased shareholder succession).")
lines.append("- **100% On-Page Optimization**: Meta titles, descriptions, and header tags fully optimized across all core pages.")
lines.append("- **Core Technical Fixes**: Fixed missing canonical tags, compressed all oversized images (>100KB), updated XML sitemaps, eliminated no-index bugs, and enhanced page load speed.")
lines.append("- **AEO (Answer Engine Optimization)**: Implemented structured schema to capture Google AI Overviews and rich snippets.")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 4. Google Analytics 4 (GA4): 165K+ Audience Acquired & 2,685 Organic Leads")
lines.append("")
lines.append("Website user acquisition maintained steady, high-quality traffic throughout the year, with total monthly users consistently exceeding 10,000–15,000 visitors.")
lines.append("")
lines.append("### Monthly Website Traffic & Organic Lead Table")
lines.append("")
lines.append("| Month | Total Users | New Users | Returning Users | Organic Traffic | Organic Leads | Organic CVR (%) |")
lines.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- |")

for _, r in df_ga.iterrows():
    m = r['Month_Label']
    tu = f"{int(r['Total User']):,}"
    nu = f"{int(r['New User']):,}"
    ru = f"{int(r['Return User']):,}"
    ot = f"{int(r['Organic Traffic']):,}"
    ol = f"{int(r['Organic Leads']):,}"
    cvr = f"{(r['Organic Leads'] / r['Organic Traffic'] * 100):.2f}%"
    lines.append(f"| **{m}** | {tu} | {nu} | {ru} | {ot} | **{ol}** | {cvr} |")

lines.append(f"| **TOTAL** | **165,849** | **161,491** | **19,677** | **39,998** | **2,685** | **6.71%** |")
lines.append("")
lines.append("### User Acquisition Channel Mix (GA4 Data):")
lines.append("- **Direct Traffic**: **46,400 users (28.75%)** — Strong word-of-mouth and corporate recognition.")
lines.append("- **Cross-Network (P-Max / Smart Campaigns)**: **39,300 users (24.35%)** — Generated 9,300 key conversion events (4.04% event rate).")
lines.append("- **Organic Search**: **37,200 users (23.01%)** — Generated highest brand loyalty with **9,900 returning users** and 51-second average engagement time.")
lines.append("- **Paid Search & Paid Social**: **32,100 users (20.0%)** — Highly targeted traffic driving instant lead generation.")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 5. Omnichannel Social Media Growth & Brand Authority")
lines.append("")
lines.append("Share Samadhan's presence across social media channels expanded significantly, demonstrating dramatic gains in community engagement, video reach, and thought leadership.")
lines.append("")
lines.append("### Social Media Performance Highlights (`Comparison Report.pdf`):")
lines.append("")
lines.append("| Channel | Primary Metric | Baseline / Previous Period | Current Reporting Period | Net Growth / Achievement |")
lines.append("| :--- | :--- | :--- | :--- | :--- |")
lines.append("| **Instagram** | Content Interactions | 1.8K | **3,600 (3.6K)** | **+103.7% Massive Explosion** |")
lines.append("| **Instagram** | Video Views | 362K | **443,000 (443K)** | **+22.4% Audience Growth** (+537 New Followers) |")
lines.append("| **Facebook** | Content Interactions | 5.6K | **6,700 (6.7K)** | **+20.1% Growth** |")
lines.append("| **Facebook** | Total Video Views | Baseline | **1,900,000 (1.9 Million)** | **444.3K Unique Viewers**, **14.1K Link Clicks** |")
lines.append("| **LinkedIn** | Organic Impressions | Baseline | **73,883 Impressions** | **2,665 Reactions**, **4,292 Executive Followers** |")
lines.append("| **YouTube** | Total Video Views | Baseline | **96,700 Views** | **698.2 Watch Hours**, **3,058 Subscribers** (+132) |")
lines.append("")
lines.append("### Content Production Highlights:")
lines.append("- **135+ Creative Assets Produced**: High-frequency output including static infographics, regulatory updates, case study carousels, and engaging video reels.")
lines.append("- **Viral Educational Video**: Educational YouTube Short on *'IEPF Nodal Officers'* achieved **5.1K organic views**, establishing authority in legal recovery.")
lines.append("")
lines.append("---")
lines.append("")
lines.append("## 6. Executive Summary: What Made This Campaign a Resounding Success?")
lines.append("")
lines.append("1. **Tripling Lead Volume While Slashing CPL by Over 60%**:")
lines.append("   - Unlike standard campaigns where costs escalate as volume scales, Share Samadhan experienced the ideal *flywheel effect*: **paid leads scaled from 440 to 1,689 leads/month**, while **blended CPL dropped from ₹180 down to ₹55**.")
lines.append("2. **Balanced Omnichannel Engine**:")
lines.append("   - The business is not reliant on a single source. Leads are generated across **Google Paid Search (6,113)**, **WhatsApp Automation (3,786)**, **Meta Paid Ads (3,662)**, **Organic Search (2,685)**, and **Inbound Direct/Calls (2,196)**.")
lines.append("3. **Organic Search Moat**:")
lines.append("   - With **72 keywords on Page 1 of Google** and **3.09 Million organic impressions**, Share Samadhan owns the category organically, ensuring free high-intent lead flow independent of ad spend.")
lines.append("4. **High-Ticket Cross-Border Pipeline**:")
lines.append("   - Capturing **456 NRI leads** across the USA, UK, UAE, and Singapore delivers high-margin transmission and estate cases that represent millions in recoverable assets.")

report_md_path = os.path.join(reports_dir, 'Share_Samadhan_Annual_Positive_Growth_Showcase_Nov2025_Nov2026.md')
report_case_path = os.path.join(case_studies_dir, 'Share_Samadhan_Annual_Positive_Growth_Showcase_Nov2025_Nov2026.md')

for p in [report_md_path, report_case_path]:
    with open(p, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))

print(f"Generated positive report at: {report_md_path}")
print(f"Generated positive report at: {report_case_path}")
