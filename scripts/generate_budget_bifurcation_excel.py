import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import shutil
import os

wb = openpyxl.Workbook()

# Style definitions
font_title = Font(name="Calibri", size=14, bold=True, color="0A2540")
font_subtitle = Font(name="Calibri", size=10, italic=True, color="555555")
font_section = Font(name="Calibri", size=11, bold=True, color="0A2540")
font_header = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
font_bold = Font(name="Calibri", size=9.5, bold=True, color="000000")
font_regular = Font(name="Calibri", size=9, color="333333")
font_small = Font(name="Calibri", size=8.5, color="555555")

fill_navy = PatternFill("solid", fgColor="0A2540") # Main header
fill_blue_sub = PatternFill("solid", fgColor="1F4E79") # Sub header
fill_soft_green = PatternFill("solid", fgColor="E8F8F5") # Agency highlight / green
fill_mint = PatternFill("solid", fgColor="D4EFDF") # Positive / total
fill_ice_blue = PatternFill("solid", fgColor="EBF3FA") # Total / summary
fill_zebra = PatternFill("solid", fgColor="F8F9FA")

thin_border_side = Side(border_style="thin", color="D3D3D3")
thick_bottom_side = Side(border_style="medium", color="0A2540")
double_bottom_side = Side(border_style="double", color="0A2540")

border_cell = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
border_header = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thick_bottom_side)
border_total = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=double_bottom_side)

align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
align_right = Alignment(horizontal="right", vertical="center")

# -----------------------------------------------------------------------------
# SHEET 1: Recommended_Bifurcation (₹1,50,000/mo)
# -----------------------------------------------------------------------------
ws1 = wb.active
ws1.title = "Recommended_Bifurcation"
ws1.views.sheetView[0].showGridLines = True

ws1.cell(1, 1, "SHARE SAMADHAN LIMITED - PAID MEDIA BUDGET BIFURCATION (2027)")
ws1.cell(1, 1).font = font_title
ws1.cell(2, 1, "Model: Recommended Monthly Scaling Plan | Total Budget: ₹1,50,000 / month (~₹5,000 / day) | Split: Google Ads 68% / Meta Ads 32%")
ws1.cell(2, 1).font = font_subtitle

headers_ws1 = [
    "Platform", "Campaign Name", "Service Category Focus", "Target Geography",
    "Daily Budget (₹)", "Monthly Budget (₹)", "% Share", "Target CPL (₹)",
    "Est. Monthly Leads (Min)", "Est. Monthly Leads (Max)", "Strategic Commercial Rationale"
]

row_num = 4
for col_idx, h in enumerate(headers_ws1, 1):
    c = ws1.cell(row_num, col_idx, h)
    c.font = font_header
    c.fill = fill_navy
    c.alignment = align_center
    c.border = border_header
ws1.row_dimensions[row_num].height = 28

bifurcation_data = [
    # Google Ads Campaigns
    ("Google Ads", "Search_Core_Shares_IEPF", "Physical Shares, Duplicate Issue & IEPF-5 Claims", "Pan-India (Metro & Tier 1/2)",
     1500, 45000, 0.30, 95, 410, 530, "Core volume engine; captures 34.0% of all inquiries with high-intent immediate documentation."),
    ("Google Ads", "Search_Transmission_Legal_Heir", "Deceased Shareholder Succession, Probate & Legal Heir Folios", "Pan-India (Wealth Hubs: Mumbai, Delhi, Kolkata, Chennai)",
     800, 24000, 0.16, 135, 160, 200, "Highest average claim value (₹15L–₹50L+ per folio); complex legal cases justify premium CPL."),
    ("Google Ads", "Search_NRI_Samadhan", "Cross-Border Wealth Concierge (Zero Travel to India)", "International Hubs (USA, UAE, UK, Singapore, Canada)",
     800, 24000, 0.16, 280, 70, 95, "Captures 290+ organic NRI pool with 5x–8x higher case fees; dedicated overseas remote concierge."),
    ("Google Ads", "Search_PF_Provident_Fund", "Stuck EPF, UAN Mismatch, Death Claims & Pension Disputes", "Industrial & IT Metros (Bengaluru, Pune, Hyderabad, NCR)",
     300, 9000, 0.06, 85, 90, 120, "Controlled low-spend test; strict negative filtering to avoid low-balance routine withdrawal noise."),
    
    # Subtotal Google
    ("Google Subtotal", "4 High-Intent Search Campaigns", "Comprehensive Search Intent Coverage", "Domestic + International NRI",
     3400, 102000, 0.68, 120, 730, 945, "High-urgency commercial search capture delivering qualified corporate & legal claimants."),
    
    # Meta Ads Campaigns
    ("Meta Ads", "WhatsApp_Physical_Shares_Locker", "Locker Physical Share Certificates Awareness & Demat", "Pan-India (Age 45–65+ High Net-Worth Investors)",
     1000, 30000, 0.20, 40, 660, 850, "Proven lowest CPL engine (₹32.74 achieved); video/carousel ads asking 'Old shares in family locker?'"),
    ("Meta Ads", "WhatsApp_IEPF_Unclaimed_Dividends", "Government IEPF Escrow Awareness & 7-Year Dividend Claims", "Pan-India (Age 40–65+ Shareholders)",
     400, 12000, 0.08, 48, 220, 300, "Educates retail shareholders on statutory transfer rules, directing into conversational WhatsApp intake."),
    ("Meta Ads", "Retargeting_All_Website_Visitors", "Past 90-Day Visitors, Form Drop-Offs & Case Studies", "Pan-India (Custom Audiences & GA4 Traffic)",
     200, 6000, 0.04, 70, 75, 100, "Conversion booster retargeting 161K+ annual users with BSE SME credibility and social proof."),
     
    # Subtotal Meta
    ("Meta Subtotal", "3 Conversational WhatsApp Ad Sets", "Conversational Social Intake & Retargeting", "National Senior Investors",
     1600, 48000, 0.32, 42, 955, 1250, "High-volume, frictionless mobile lead generation powering daily associate intake pipeline."),
     
    # Total
    ("GRAND TOTAL", "7 Blended Omnichannel Campaigns", "Full-Funnel Legal-Financial Asset Recovery Ecosystem", "Omnichannel National + Cross-Border",
     5000, 150000, 1.00, 75, 1685, 2195, "Balanced, high-margin, risk-mitigated growth engine delivering 1,700–2,200 leads/month.")
]

for row_data in bifurcation_data:
    row_num += 1
    is_subtotal = "Subtotal" in row_data[0]
    is_grand = "GRAND" in row_data[0]
    
    if is_grand:
        fill_row = fill_mint
        font_row = font_bold
        border_row = border_total
    elif is_subtotal:
        fill_row = fill_ice_blue
        font_row = font_bold
        border_row = border_header
    else:
        fill_row = fill_zebra if row_num % 2 == 1 else None
        font_row = font_regular
        border_row = border_cell
        
    for col_idx, val in enumerate(row_data, 1):
        c = ws1.cell(row_num, col_idx, val)
        c.font = font_row
        c.border = border_row
        if fill_row:
            c.fill = fill_row
            
        # Formats
        if col_idx in [5, 6, 8]: # Currency
            c.number_format = "₹#,##0"
            c.alignment = align_right
        elif col_idx == 7: # Percentage
            c.number_format = "0.0%"
            c.alignment = align_right
        elif col_idx in [9, 10]: # Integer leads
            c.number_format = "#,##0"
            c.alignment = align_right
        elif col_idx in [1, 4]:
            c.alignment = align_center
        else:
            c.alignment = align_left
            
    ws1.row_dimensions[row_num].height = 24 if (is_subtotal or is_grand) else 21

# -----------------------------------------------------------------------------
# SHEET 2: Budget_Scenarios (Conservative, Recommended, Aggressive)
# -----------------------------------------------------------------------------
ws2 = wb.create_sheet(title="Budget_Scenarios")
ws2.views.sheetView[0].showGridLines = True

ws2.cell(1, 1, "SHARE SAMADHAN LIMITED - 3 SCALED BUDGET SCENARIOS")
ws2.cell(1, 1).font = font_title
ws2.cell(2, 1, "Financial Modeling across Conservative, Growth, and Aggressive Market Expansion Tiers")
ws2.cell(2, 1).font = font_subtitle

headers_ws2 = [
    "Scenario Tier", "Monthly Budget (₹)", "Daily Run-Rate (₹)", "Google Ads Share (₹)", "Google Ads %",
    "Meta Ads Share (₹)", "Meta Ads %", "Est. Total Leads (Min)", "Est. Total Leads (Max)",
    "Blended CPL (₹)", "Core Strategic Objectives & Operational Trade-Offs"
]

row_num = 4
for col_idx, h in enumerate(headers_ws2, 1):
    c = ws2.cell(row_num, col_idx, h)
    c.font = font_header
    c.fill = fill_navy
    c.alignment = align_center
    c.border = border_header
ws2.row_dimensions[row_num].height = 28

scenarios_data = [
    ("Conservative Baseline", 100000, 3333, 65000, 0.65, 35000, 0.35, 1150, 1400, 78,
     "Maintains current profitability baseline. Focuses strictly on Core Shares, IEPF and a small ₹15k NRI test. PF campaign kept on hold."),
    ("Recommended Growth (Optimal)", 150000, 5000, 102000, 0.68, 48000, 0.32, 1685, 2195, 75,
     "Optimal balance of volume and margin. Fully funds dedicated NRI Samadhan (₹24k) and launches exploratory PF campaign (₹9k) alongside scaled Meta WhatsApp."),
    ("Aggressive Category Dominance", 200000, 6667, 135000, 0.675, 65000, 0.325, 2400, 3000, 72,
     "Full market monopoly. Expands NRI campaigns to UK/Singapore regional search, launches vernacular Meta video ads (Hindi, Gujarati), and maximizes high-ticket transmission capture.")
]

for row_data in scenarios_data:
    row_num += 1
    is_rec = "Recommended" in row_data[0]
    fill_row = fill_soft_green if is_rec else (fill_zebra if row_num % 2 == 1 else None)
    font_row = font_bold if is_rec else font_regular
    
    for col_idx, val in enumerate(row_data, 1):
        c = ws2.cell(row_num, col_idx, val)
        c.font = font_row
        c.border = border_cell
        if fill_row:
            c.fill = fill_row
            
        if col_idx in [2, 3, 4, 6, 10]:
            c.number_format = "₹#,##0"
            c.alignment = align_right
        elif col_idx in [5, 7]:
            c.number_format = "0.0%"
            c.alignment = align_right
        elif col_idx in [8, 9]:
            c.number_format = "#,##0"
            c.alignment = align_right
        elif col_idx == 1:
            c.alignment = align_left
        else:
            c.alignment = align_left
            
    ws2.row_dimensions[row_num].height = 24

# -----------------------------------------------------------------------------
# SHEET 3: Campaign_Setup_Specs (NRI & PF Guidelines)
# -----------------------------------------------------------------------------
ws3 = wb.create_sheet(title="Campaign_Setup_Specs")
ws3.views.sheetView[0].showGridLines = True

ws3.cell(1, 1, "CAMPAIGN SETUP SPECIFICATIONS: NRI SAMADHAN & PF RESOLUTION")
ws3.cell(1, 1).font = font_title
ws3.cell(2, 1, "Targeting Parameters, Match Types, Negative Keyword Guardrails & Routing Rules")
ws3.cell(2, 1).font = font_subtitle

headers_ws3 = [
    "Campaign Identifier", "Platform", "Match Type", "Target Keyword Themes",
    "Mandatory Negative Keywords (Strict Exclusion)", "Ad Headline & Description Copy Focus", "Lead Routing & Intake Flow"
]

row_num = 4
for col_idx, h in enumerate(headers_ws3, 1):
    c = ws3.cell(row_num, col_idx, h)
    c.font = font_header
    c.fill = fill_navy
    c.alignment = align_center
    c.border = border_header
ws3.row_dimensions[row_num].height = 28

specs_data = [
    ("Search_NRI_Samadhan", "Google Search", "Phrase & Exact Match",
     '• [nri share transmission india]\n• [claim iepf shares from usa]\n• [nri duplicate share certificate]\n• "indian shares recovery for nri"\n• [sell physical shares in india for nri]\n• "nri legal heir shares succession"',
     '• domestic shares\n• demat account opening india\n• share market tips\n• zerodha login\n• angel one account',
     'Headline: NRI Share Samadhan | Zero Travel To India Required\nDescription: Settle inherited Indian shares, IEPF claims & Demat conversion from your home country. Dedicated legal concierge handles all paperwork & POA.',
     'Tag with utm_campaign=nri_samadhan. Route instantly to Senior Wealth Concierge team on WhatsApp with country code prioritization (+1, +971, +44).'),
    
    ("Search_PF_Provident_Fund", "Google Search", "Strict Phrase & Exact Only",
     '• [pf rejection resolution consultant]\n• "stuck epf claim assistance"\n• [pf death claim legal heir dispute]\n• "uan name mismatch lawyer"\n• [pf trust transfer rejection solution]\n• "pf advance rejected claim help"',
     '• free\n• portal\n• login\n• passbook download\n• balance check\n• toll free number\n• epfo office address\n• customer care\n• member home\n• grievances portal\n• download form 19',
     'Headline: Stuck PF Claim Resolution | Expert Legal Assistance\nDescription: Facing multiple PF claim rejections, UAN date-of-exit issues, or complex deceased employee PF disputes? Legal dispute specialists resolve your claim.',
     'Tag with utm_campaign=pf_claims. Route to specialized EPF dispute associate desk; filter inquiries by minimum PF claim value (>₹1,50,000 threshold).'),
    
    ("WhatsApp_Physical_Shares_Locker", "Meta Ads (IG/FB)", "Broad Demographic + Interests",
     '• Interests: BSE India, NSE India, Mutual Funds, Senior Citizen Savings, Stock Exchange\n• Age: 45 to 65+ Years\n• Placement: Facebook Feed, Instagram Feed, Reels',
     '• Job seekers\n• Day trading\n• Crypto currency\n• Forex',
     'Primary Text: Do you or your parents have physical share certificates lying forgotten in home lockers or bank safes? Millions of rupees in dividends are transferred to IEPF each year.\nCTA: Chat on WhatsApp',
     'Direct click-to-WhatsApp (Anantya.ai) automated qualification bot asking: 1) Company Name, 2) Approximate Shares, 3) Certificate availability.'),
    
    ("WhatsApp_IEPF_Unclaimed_Dividends", "Meta Ads (IG/FB)", "Broad 40-65+ Demographic",
     '• Interests: Personal Finance, Fixed Deposits, Government Bonds, Dividend Investing\n• Placement: Mobile Feeds only',
     '• Intraday\n• Penny stocks',
     'Primary Text: Did you know unpaid dividends over 7 years automatically go to the government IEPF authority? Check your rightful claims before they lapse.\nCTA: Free Search on WhatsApp',
     'Automated bot captures shareholder name, folio number, and provides instant lookup initiation.')
]

for row_data in specs_data:
    row_num += 1
    fill_row = fill_zebra if row_num % 2 == 1 else None
    for col_idx, val in enumerate(row_data, 1):
        c = ws3.cell(row_num, col_idx, val)
        c.font = font_regular
        c.border = border_cell
        if fill_row:
            c.fill = fill_row
        if col_idx in [1, 2, 3]:
            c.alignment = align_center
        else:
            c.alignment = align_left
    ws3.row_dimensions[row_num].height = 65

# -----------------------------------------------------------------------------
# SHEET 4: Historical_Performance_Base (Reference Metrics)
# -----------------------------------------------------------------------------
ws4 = wb.create_sheet(title="Historical_Performance_Base")
ws4.views.sheetView[0].showGridLines = True

ws4.cell(1, 1, "HISTORICAL PERFORMANCE BASELINE REFERENCE (13-MONTH AUDIT)")
ws4.cell(1, 1).font = font_title
ws4.cell(2, 1, "Audit Benchmarks: Nov 1, 2025 to Nov 23, 2026 | Master Deliverable: Share Samadhan Performance Operating System")
ws4.cell(2, 1).font = font_subtitle

headers_ws4 = [
    "Performance Channel", "Annual Inbound Volume", "Annual Total Spend (₹)", "Average Realized CPL (₹)",
    "Recent Monthly Run-Rate (₹)", "Recent Month CPL (₹)", "Key Historical Insight"
]

row_num = 4
for col_idx, h in enumerate(headers_ws4, 1):
    c = ws4.cell(row_num, col_idx, h)
    c.font = font_header
    c.fill = fill_navy
    c.alignment = align_center
    c.border = border_header
ws4.row_dimensions[row_num].height = 28

hist_data = [
    ("Google Ads Search (Annual Total)", 6163, 592977, 96.22, 53665, 137.25, "Scaled from 208 leads (Nov '25) to peak of 775 leads (Jul '26); record low CPL ₹58.45."),
    ("Meta Ads Conversational (Annual Total)", 6492, 526512, 81.10, 28648, 46.66, "CPL compressed by -88.6% from ₹287.65 (Dec '25) down to ₹32.74 (Oct '26) with 1,016 leads in a single month."),
    ("Total Paid Media (Google + Meta)", 12655, 1119489, 88.46, 82312, 81.90, "Generated 12,655 paid leads under ₹11.20 Lakhs cumulative investment."),
    ("Verified Digital Inbound Leads (CRM)", 13384, 1119489, 83.64, 82312, 84.50, "Total digital volume excluding 3,202 internal associate-added entries."),
    ("Google Analytics Organic Audience (GA4)", 161781, 0, 0, 0, 0, "161,781 total users (+26.5% YoY), 161,741 new users (+34.8% YoY), and 2,685 verified organic search leads.")
]

for row_data in hist_data:
    row_num += 1
    is_tot = "Total" in row_data[0]
    fill_row = fill_ice_blue if is_tot else (fill_zebra if row_num % 2 == 1 else None)
    font_row = font_bold if is_tot else font_regular
    border_row = border_total if is_tot else border_cell
    
    for col_idx, val in enumerate(row_data, 1):
        c = ws4.cell(row_num, col_idx, val)
        c.font = font_row
        c.border = border_row
        if fill_row:
            c.fill = fill_row
        if col_idx in [3, 4, 5, 6]:
            c.number_format = "₹#,##0.00" if col_idx in [4, 6] else "₹#,##0"
            c.alignment = align_right
        elif col_idx == 2:
            c.number_format = "#,##0"
            c.alignment = align_right
        else:
            c.alignment = align_left
    ws4.row_dimensions[row_num].height = 23

# Adjust Column Widths across all sheets
for ws in [ws1, ws2, ws3, ws4]:
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            val_str = str(cell.value or "")
            # take first line if multiple lines
            first_line = val_str.split("\n")[0]
            if len(first_line) > max_len:
                max_len = len(first_line)
        ws.column_dimensions[col_letter].width = min(max(max_len + 3, 12), 46)

# Specific custom widths for readability
ws1.column_dimensions['A'].width = 16
ws1.column_dimensions['B'].width = 32
ws1.column_dimensions['C'].width = 38
ws1.column_dimensions['D'].width = 24
ws1.column_dimensions['E'].width = 16
ws1.column_dimensions['F'].width = 18
ws1.column_dimensions['G'].width = 12
ws1.column_dimensions['H'].width = 15
ws1.column_dimensions['I'].width = 16
ws1.column_dimensions['J'].width = 16
ws1.column_dimensions['K'].width = 45

ws2.column_dimensions['A'].width = 26
ws2.column_dimensions['B'].width = 18
ws2.column_dimensions['C'].width = 18
ws2.column_dimensions['D'].width = 20
ws2.column_dimensions['E'].width = 14
ws2.column_dimensions['F'].width = 18
ws2.column_dimensions['G'].width = 14
ws2.column_dimensions['H'].width = 16
ws2.column_dimensions['I'].width = 16
ws2.column_dimensions['J'].width = 16
ws2.column_dimensions['K'].width = 50

ws3.column_dimensions['A'].width = 32
ws3.column_dimensions['B'].width = 18
ws3.column_dimensions['C'].width = 22
ws3.column_dimensions['D'].width = 38
ws3.column_dimensions['E'].width = 32
ws3.column_dimensions['F'].width = 46
ws3.column_dimensions['G'].width = 42

ws4.column_dimensions['A'].width = 35
ws4.column_dimensions['B'].width = 18
ws4.column_dimensions['C'].width = 20
ws4.column_dimensions['D'].width = 20
ws4.column_dimensions['E'].width = 22
ws4.column_dimensions['F'].width = 18
ws4.column_dimensions['G'].width = 48

# Output paths
out_p1 = r"C:\Users\test\Videos\Office\reports\Share_Samadhan_Paid_Media_Budget_Bifurcation_2027.xlsx"
out_p2 = r"C:\Users\test\Videos\Office\case-studies\Share Samadhan\Share_Samadhan_Paid_Media_Budget_Bifurcation_2027.xlsx"

os.makedirs(os.path.dirname(out_p1), exist_ok=True)
os.makedirs(os.path.dirname(out_p2), exist_ok=True)

wb.save(out_p1)
shutil.copy2(out_p1, out_p2)

print(f"Successfully generated Budget Bifurcation Excel at:")
print(f"1. {out_p1}")
print(f"2. {out_p2}")
