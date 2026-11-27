import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import win32com.client
import pythoncom
import pypdf

# Define paths
report_docx = r"C:\Users\test\Videos\Office\reports\FABB6_Final_Performance_Audit_Strategy_and_Forecast_Report.docx"
case_study_docx = r"C:\Users\test\Videos\Office\case-studies\fabb6\FABB6_Final_Performance_Audit_Strategy_and_Forecast_Report.docx"
artifact_docx = r"C:\Users\test\.gemini\antigravity\brain\29f77e0a-5ed5-4d24-842c-443d9957274c\FABB6_Final_Performance_Audit_Strategy_and_Forecast_Report.docx"

report_pdf = r"C:\Users\test\Videos\Office\reports\FABB6_Final_Performance_Audit_Strategy_and_Forecast_Report.pdf"
case_study_pdf = r"C:\Users\test\Videos\Office\case-studies\fabb6\FABB6_Final_Performance_Audit_Strategy_and_Forecast_Report.pdf"
artifact_pdf = r"C:\Users\test\.gemini\antigravity\brain\29f77e0a-5ed5-4d24-842c-443d9957274c\FABB6_Final_Performance_Audit_Strategy_and_Forecast_Report.pdf"

script_source = r"C:\Users\test\Videos\Office\scripts\build_perfect_report.py"

with open(script_source, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update Section 3
target_sec3 = """    add_bullet("A campaign named 'Search-Brand' used broad match and triggered queries unrelated to beauty (for example, gym equipment and a badminton ankle support). The spend on these queries is not yet quantified; it will be after a full search terms export.", bold_prefix="5. Off-category search queries: ")"""

replacement_sec3 = """    add_bullet("A campaign named 'Search-Brand' used broad match and triggered queries unrelated to beauty (for example, gym equipment and a badminton ankle support). The spend on these queries is not yet quantified; it will be after a full search terms export.", bold_prefix="5. Off-category search queries: ")
    add_bullet("Official Merchant Center performance exports (Sep 1 – Nov 19) across 3,411 SKUs show 6.14 Crore impressions and 6,29,968 clicks, yet only 48.77 purchases were tracked (0.0077% conversion rate) due to the severed conversion action. 86.2% of all clicks (5,42,808 clicks) were concentrated on 3,358 products that produced ZERO purchases because campaigns ran on 'All Products' without custom label margin filtering. Standalone single-use entry items and low-margin products cannibalized the budget without margin exclusions (Exhibit G).", bold_prefix="6. Merchant Center SKU click bleed & feed misallocation: ")

    gmc_table_data = [
        ["Top Bleeding SKU (Zero Purchases)", "Price / Tier", "Margin Class", "Impressions", "Clicks", "Tracked Purchases"],
        ["Raaga Professional De-Tan Cream single use", "₹69 (T1 Entry)", "mid_20_28", "1,261,144", "27,648", "0.00"],
        ["DOT & KEY Strawberry Dew Tinted Sunscreen 50ml", "₹549 (T2 Core)", "mid_20_28", "669,332", "17,485", "0.00"],
        ["Loreal Paris Hair Spa Deep Nourish 490g", "₹650 (T2 Core)", "mid_20_28", "766,242", "13,249", "0.00"],
        ["Matrix Mega Smooth Masque 500g", "₹750 (T2 Core)", "mid_20_28", "810,808", "9,192", "0.00"],
        ["Loreal Majirel 3.0 Combo + Developer 1000ml", "₹755 (T2 Core)", "high_28plus", "673,069", "9,142", "0.00"],
        ["Floractive Professional W One Nanoplastia 1000ml", "₹5,500 (T4 Pro)", "high_28plus", "1,357,589", "6,921", "0.00"],
        ["Total Top 6 Zero-Converting Bleeders", "—", "—", "5,538,184", "83,637", "0.00"]
    ]
    create_styled_table(doc, gmc_table_data, header_bg="102C57", center_cols=[1, 2, 5], right_cols=[3, 4])
    add_body("Products flagged EXCLUDE_lowmargin served 8.47L impressions and 9,354 clicks, while low-margin items (<20%) took 1.07L clicks. These bleeders will be hard-excluded in Phase 1.")"""

if target_sec3 in code:
    code = code.replace(target_sec3, replacement_sec3)
    print("Section 3 replaced.")
else:
    print("Section 3 target not found (may already be replaced).")

# 2. Update Section 6 (Phase 1 & Phase 2)
target_phase1 = """    add_bullet("Pause 'IG-Traffic' and the iOS and Android app install campaigns.")"""
replacement_phase1 = """    add_bullet("Pause 'IG-Traffic' and the iOS and Android app install campaigns.")
    add_bullet("Hard-exclude top 20 zero-converting click bleeder SKUs identified in Merchant Center (e.g., Raaga single-use de-tan cream and unsegmented core SKUs).")"""

if target_phase1 in code:
    code = code.replace(target_phase1, replacement_phase1)
    print("Phase 1 replaced.")
else:
    print("Phase 1 target not found.")

target_phase2 = """    add_bullet("Segment Performance Max into Hero Best-Sellers (60% of budget), Long-Tail Catalog (20%) and Search/Brand (20%).")"""
replacement_phase2 = """    add_bullet("Segment Performance Max and Standard Shopping strictly by Custom Label 1 (Price Tier) and Custom Label 4 (Margin Class): Hero Best-Sellers (high_28plus & T4 Pro/Salon, 60% of budget), Core Catalog (mid_20_28, 20%), and Brand Search (20%). Hard-exclude EXCLUDE_lowmargin and unbundled T1 Entry single sachets.")"""

if target_phase2 in code:
    code = code.replace(target_phase2, replacement_phase2)
    print("Phase 2 replaced.")
else:
    print("Phase 2 target not found.")

# 3. Update Appendix A
target_app_a = """    add_bullet("Meta link clicks versus Shopify landing page views.", bold_prefix="Exhibit F: ")"""
replacement_app_a = """    add_bullet("Meta link clicks versus Shopify landing page views.", bold_prefix="Exhibit F: ")
    add_bullet("Google Merchant Center product performance export (Sep 1 – Nov 19, 2026) and catalog audit showing 86.2% zero-conversion click concentration and price/margin tier misallocation.", bold_prefix="Exhibit G: ")"""

if target_app_a in code:
    code = code.replace(target_app_a, replacement_app_a)
    print("Appendix A replaced.")
else:
    print("Appendix A target not found.")

# Save updated script
with open(script_source, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated build_perfect_report.py successfully.")

# Run build_perfect_report.py
exec_globals = {}
exec(compile(code, script_source, 'exec'), exec_globals)

print("Report generation completed. Checking PDF pages...")
reader = pypdf.PdfReader(report_pdf)
print(f"Total PDF pages: {len(reader.pages)}")
for idx, page in enumerate(reader.pages):
    txt = page.extract_text().strip()
    first_line = txt.split('\n')[0] if txt else ''
    print(f"Page {idx+1}: {len(txt)} chars | Starts: {first_line[:65]}")
