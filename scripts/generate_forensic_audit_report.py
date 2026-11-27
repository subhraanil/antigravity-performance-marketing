import os
import shutil
import pandas as pd
import openpyxl
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
import matplotlib.pyplot as plt

os.makedirs("reports", exist_ok=True)
art_dir = r"C:\Users\test\.gemini\antigravity\brain\4eb8b0c3-fb70-44b6-beb2-0fb647311113"

# -------------------------------------------------------------
# 1. Generate Updated Chart: Forensic Budget Waste vs. Revenue Drivers
# -------------------------------------------------------------
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8), dpi=300)

# Subplot 1: Meta Spend Breakdown
labels1 = [
    'Winning Sales Ads\n(Molar Stick, Trimmer)',
    'Boosted Posts / No-Purchase\n(Simon Squibb, Max, etc.)',
    'Reels Placements\n(FB & IG Reels Bleeders)',
    'Retargeting & Catalog'
]
sizes1 = [2109.41, 1306.80, 993.10, 933.35]
colors1 = ['#10B981', '#EF4444', '#F59E0B', '#3B82F6']
explode1 = (0.05, 0.08, 0.05, 0)

ax1.pie(sizes1, explode=explode1, labels=labels1, colors=colors1, autopct='%1.1f%%',
        startangle=140, textprops={'fontsize': 8.5})
ax1.set_title('Meta Ads: £5,343 Spend Allocation\n(£2,300+ in Wasted / Inefficient Spend)', fontsize=10.5, fontweight='bold', pad=10)

# Subplot 2: Google Ads Spend Breakdown
labels2 = [
    'Converting Product Queries\n(Anti-Bark Collar, Beds, Mats)',
    'Wasted Non-Converting Queries\n(Costco, Gulpup, Shock Collars)',
    'Search & Testing Terms\n(Paused / Low-Intent Terms)'
]
sizes2 = [548.80, 432.60, 32.55]
colors2 = ['#10B981', '#EF4444', '#94A3B8']
explode2 = (0.05, 0.08, 0)

ax2.pie(sizes2, explode=explode2, labels=labels2, colors=colors2, autopct='%1.1f%%',
        startangle=140, textprops={'fontsize': 8.5})
ax2.set_title('Google Ads: £1,014 Spend Allocation\n(42.7% Spent on Non-Converting & Competitor Queries)', fontsize=10.5, fontweight='bold', pad=10)

plt.suptitle('Pet Mode: Forensic Ad Spend Audit Findings', fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
chart_path = 'reports/petmode_forensic_audit_chart.png'
plt.savefig(chart_path, dpi=300, bbox_inches='tight')
plt.close()

if os.path.exists(art_dir):
    shutil.copyfile(chart_path, os.path.join(art_dir, 'petmode_forensic_audit_chart.png'))

# -------------------------------------------------------------
# 2. Helper Functions for Word Document Styling
# -------------------------------------------------------------
doc = Document()
for sec in doc.sections:
    sec.top_margin = Inches(0.75)
    sec.bottom_margin = Inches(0.75)
    sec.left_margin = Inches(0.75)
    sec.right_margin = Inches(0.75)

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(22)
    run.font.bold = True
    run.font.color.rgb = RGBColor(30, 58, 138) # Navy
    p.paragraph_format.space_after = Pt(2)

def add_subtitle(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(11)
    run.font.italic = True
    run.font.color.rgb = RGBColor(100, 116, 139) # Slate
    p.paragraph_format.space_after = Pt(14)

def add_h1(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(13.5)
    run.font.bold = True
    run.font.color.rgb = RGBColor(30, 58, 138)
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)

def add_h2(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = RGBColor(51, 65, 85)
    p.paragraph_format.space_before = Pt(9)
    p.paragraph_format.space_after = Pt(3)

def add_p(text, bold_prefix=None):
    p = doc.add_paragraph()
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Calibri'
        r_pre.font.size = Pt(9.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(15, 23, 42)
    run = p.add_run(text)
    run.font.name = 'Calibri'
    run.font.size = Pt(9.5)
    run.font.color.rgb = RGBColor(51, 65, 85)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15

def add_callout(title, text, bg_hex="EFF6FF", border_hex="3B82F6"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_hex)
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    r1 = p.add_run(f"📌 {title}: ")
    r1.font.name = 'Calibri'
    r1.font.size = Pt(9.5)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(30, 58, 138)
    
    r2 = p.add_run(text)
    r2.font.name = 'Calibri'
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = RGBColor(30, 41, 59)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

# -------------------------------------------------------------
# 3. Document Body Construction
# -------------------------------------------------------------
add_title("PET MODE")
add_subtitle("Forensic Ad Account Audit & Operational Fixation Plan\nRoadmap to Achieving Forecast - B (£6,320 Revenue | £16.88 Blended CPA | 1.66x ROAS)")

add_h1("1. Executive Summary & Audit Overview")
add_p("A rigorous forensic audit was conducted across Pet Mode's advertising accounts (Google Ads and Meta Ads) and Shopify storefront analytics (148 order transactions, customer records, and Shopify Email setup). The audit identified clear operational root causes for previous performance plateaus and establishes an evidence-based roadmap to achieve the 3-month Forecast - B targets.")

add_callout("Key Strategic Takeaway", 
    "Pet Mode does not suffer from product-market fit or fundamental creative fatigue. Performance has been suppressed by approximately £2,300+ in preventable spend bleeders across Meta vanity posts and Reels, Google Performance Max non-converting search queries, and multi-market Merchant Center feed settings. Eliminating these bleeders instantly stabilizes account CPA under £17.00.")

doc.add_paragraph().paragraph_format.space_before = Pt(6)
doc.add_picture(chart_path, width=Inches(6.5))

add_h1("2. Forensic Meta Ads Findings: Eliminating £2,300+ in Inefficiencies")

add_h2("2.1 Massive Waste on Boosted Engagement Posts (£1,306.80 Burned | 0 Purchases)")
add_p("• Analysis: ", "A staggering 24.5% of total Meta spend (£1,306.80 out of £5,342.66) was directed toward boosting organic posts, founder interviews, and lifestyle videos (e.g. 'With Simon Squibb' £203.25, 'UK getaway with pet' £280.03, 'Max Saturday plans' £192.27, 'Max has two speeds' £108.63). These delivered zero purchases.")
add_p("• Fixation Action: ", "Immediately terminate all page post boosts, video views, and post engagement campaigns. Every pound of Meta spend must be directed strictly to Advantage+ / Sales Conversion campaigns with the Purchase objective.")

add_h2("2.2 Placement Disparity: Feeds Delivering Profit vs. Reels Burning Cash")
add_p("• Facebook Feed (Hero Placement): ", "Spent £3,270.39 and generated 73 purchases (77.7% of all account purchases) with consistent conversion volume.")
add_p("• Standalone Reels Placements (Severe Bleeder): ", "Facebook Reels spent £634.33 for only 5 purchases (CPA £126.87, ROAS 0.14x), while Instagram Reels burned £358.77 for exactly 0 purchases.")
add_p("• Fixation Action: ", "Restrict Advantage+ ad set placements to Facebook Feed and Instagram Feed until dedicated short-form TikTok/Reels UGC creatives are scripted and produced.")

add_h2("2.3 Demographic Concentration: Women Aged 45+ Drive 64% of Purchases")
add_p("• Women 45+: ", "Accounted for £3,140.19 in spend (58.8%) and delivered 61 out of 95 purchases (64.2%).")
add_p("• Men 18–34: ", "Spent £198.62 with zero purchases. Younger age brackets (18–24) showed sub-0.5% click-to-purchase intent.")
add_p("• Fixation Action: ", "Exclude ages 18–24 and tighten creative hooks toward women aged 35–65+ who manage pet care purchasing decisions in the household.")

add_h2("2.4 Proven Winning Funnels")
add_p("• High-Performing Creative: ", "'Test - New Sales Ad Molar Stick' generated 25 purchases at £26.43 CPA; 'Trimer' generated 8 purchases at £29.44 CPA.")
add_p("• Recent Campaign Momentum: ", "The new '[TE]Sales 8.5.26' campaign achieved £16.23 CPA and 1.62x ROAS in mid-September, validating that direct-response purchase targeting achieves Forecast - B benchmarks.")

add_h1("3. Forensic Google Ads & Merchant Center Findings")

add_h2("3.1 Google Merchant Center Feed Hygiene & 'Limited' Status Resolution")
add_p("• Finding: ", "In Google Merchant Center, product listings are currently flagged with yellow 'Limited' eligibility status. In the Shopify Google & YouTube channel, multi-country publishing is enabled across international markets where local shipping rates have not been configured, generating thousands of unserviced variant entries and 'Missing shipping info in some countries' warnings.")
add_p("• Impact: ", "Google Shopping algorithms favor clean feeds with 100% compliant shipping data. Multi-market warnings fragment crawl budget and dampen Shopping impression share.")
add_p("• Fixation Action: ", "In Shopify Admin > Google & YouTube app > Settings, restrict targeted country feeds strictly to United Kingdom (GBP). This immediately clears the 'Limited' status warnings, purges unserviced variant entries, and consolidates all product algorithm history onto active UK listings.")

add_h2("3.2 Performance Max Query Bleeders (£432.60 / 42.7% of Spend on Irrelevant Queries)")
add_p("• Analysis: ", "The single active campaign ('Sales-Performance Max-15.5.26') spent £981.40 for 24 conversions (CPA £40.89). However, over £430 was consumed by non-converting search queries:")
add_p("  - Competitor Brand Queries: ", "'costco poo bags' (Costco), 'gulpup' (direct competitor), '3 peaks running dog lead' (Pets at Home brand).")
add_p("  - Irrelevant / Misaligned Queries: ", "'dog shock collar', 'barking shock collar'. Pet Mode sells humane smart automatic sound/vibration collars; shoppers seeking high-voltage electric shock collars bounce immediately upon landing.")
add_p("• Fixation Action: ", "Build an account-level negative keyword list containing competitor brand terms, controversial keywords ('shock', 'electric'), and low-intent terms ('free', 'wholesale', 'cheap').")

add_h2("3.3 Hero SKU Allocation in Shopping / PMax")
add_p("• Analysis: ", "Pet Mode's #1 organic volume driver on Shopify (3-in-1 Dog Dental Chew Toy) received only £7.86 in Google spend and 15 clicks over the audited period, while lower-margin items absorbed majority budget.")
add_p("• High-Performing Converters: ", "When traffic hits specific targeted products, Google Ads converts efficiently: Anti-Barking Dog Collar (CPA £22.78), Dog Car Seat Bed (CPA £23.43), and Self-Adhesive Cat Scratching Carpet (CPA £4.93).")
add_p("• Fixation Action: ", "Restructure PMax into dedicated Asset Groups: Asset Group 1 (Hero Dental Care), Asset Group 2 (Humane Anti-Bark Training), and Asset Group 3 (Comfort & Travel Beds/Mats).")

add_h1("4. Shopify Storefront, Email & Basket Size Economics")
add_p("• Repeat Purchase Rate: ", "Currently at 3.6% (139 unique customers, 5 repeat orders). Pet supplies are naturally replenishable, representing an immediate retention opportunity.")
add_p("• Single-Item Basket Bottleneck: ", "89.2% of orders contain exactly 1 item (average basket size: 1.15 items). Customers pay £5.97 shipping on single items, increasing price sensitivity.")
add_p("• Automated Email Gap: ", "While Shopify Email is connected, automated abandoned checkout recovery flows and post-purchase replenishment flows are not fully deployed.")
add_p("• Fixation Action: ", "Deploy a 3-part abandoned checkout flow with a 10% coupon ('PUPPY10'), establish a £35 Free UK Shipping threshold, and introduce a 2-Pack Dental Defense Bundle at £26.99 to elevate AOV from £21 to £28+.")

add_h1("5. The 4-Phase Operational Fixation Plan")

add_h2("Phase 1: Immediate Bleeder Elimination (Days 1–3)")
add_p("1. Terminate Meta Vanity Boosts: Immediately pause all boosted organic posts, video view boosts, and blog promotion ads. Reallocate 100% of Meta daily spend into Purchase-conversion campaigns.")
add_p("2. Placement Lockdown: Disable standalone Facebook Reels and Instagram Reels ad sets. Restrict Advantage+ placements to Facebook Feed and Instagram Feed.")
add_p("3. Audience Refinement: Exclude ages 18–24 and refine target demographics to women aged 35–65+ in the United Kingdom.")

add_h2("Phase 2: Google Merchant Center & Shopping Feed Repair (Days 3–7)")
add_p("1. Country & Shipping Feed Cleanup: In Shopify Google & YouTube app settings, restrict targeted country feeds strictly to United Kingdom (GBP) to eliminate foreign market 'Limited' shipping warnings and unserviced variants.")
add_p("2. Negative Keyword Inclusions: Apply account-level negative keywords for competitor brands (Costco, Gulpup, 3 Peaks, Pets at Home) and off-product queries (shock collar, electric collar, free, cheap).")
add_p("3. Segment PMax Asset Groups: Build distinct asset groups for Hero Dental Care, Anti-Bark Training, and Beds/Mats with dedicated lifestyle imagery and benefit-driven copy.")

add_h2("Phase 3: Shopify Email Automation & AOV Engine (Days 7–14)")
add_p("1. 3-Part Abandoned Checkout Flow: Set up automated triggers in Shopify Email at 1 hour (reminder), 24 hours (10% discount code 'PUPPY10'), and 48 hours (expiry urgency). Expected recovery: 5–8 orders/month at zero ad cost.")
add_p("2. Free Shipping Threshold: Establish Free UK Shipping at £35.00 to encourage multi-item baskets.")
add_p("3. Hero Product Bundling: Create a 2-Pack Dental Defense Bundle at £26.99 and a 'New Pet Parent Care Kit' to drive AOV above £28.00.")

add_h2("Phase 4: Q4 Holiday & Black Friday Scaling (October – December 2026)")
add_p("1. October Foundation: Stabilize spend at £1,100 (£500 Google, £600 Meta). Target 57 orders at £19.15 blended CPA and £1,493 revenue.")
add_p("2. November BFCM Scaling: Ramp spend to £1,300 (£600 Google, £700 Meta) to capture peak conversion rates (3.8% Meta, 2.7% Google). Deliver 80 orders, £2,252 revenue at £16.16 blended CPA.")
add_p("3. December Holiday Sprint: Front-load budget into Weeks 1–3 (£1,400 total spend) ahead of December 18–20 UK delivery deadlines. Deliver 87 orders, £2,575 revenue at £16.04 blended CPA and 1.84x ROAS.")

add_h1("6. Channel-by-Channel Monthly Forecast - B KPI Targets")

# Add KPI Table
kpi_table = doc.add_table(rows=5, cols=7)
kpi_table.alignment = WD_TABLE_ALIGNMENT.CENTER

headers = ["Month", "Total Spend", "Total Orders", "Blended CPA", "Total Revenue", "Blended ROAS", "Key Milestones"]
col_widths = [Inches(0.9), Inches(0.9), Inches(0.8), Inches(0.9), Inches(0.9), Inches(0.9), Inches(1.7)]

# Format Header Row
hdr_cells = kpi_table.rows[0].cells
for i, title in enumerate(headers):
    hdr_cells[i].text = title
    set_cell_background(hdr_cells[i], "1E3A8A")
    set_cell_margins(hdr_cells[i], top=100, bottom=100, left=100, right=100)
    p = hdr_cells[i].paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in p.runs:
        run.font.name = 'Calibri'
        run.font.size = Pt(8.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)

table_data = [
    ["October 2026", "£1,100.00", "57.4", "£19.15", "£1,493.44", "1.36x", "Cut vanity spend; fix GMC feed; launch email flows"],
    ["November 2026", "£1,300.00", "80.4", "£16.16", "£2,251.69", "1.73x", "BFCM promotion surge; scale Dental Bundle & Feed ads"],
    ["December 2026", "£1,400.00", "87.3", "£16.04", "£2,574.62", "1.84x", "Front-load spend Weeks 1-3; Christmas gift sets"],
    ["3-Month Total", "£3,800.00", "225.1", "£16.88", "£6,319.75", "1.66x", "£6,320 Revenue, 225 Orders achieved profitably"]
]

for row_idx, row_values in enumerate(table_data, start=1):
    row_cells = kpi_table.rows[row_idx].cells
    bg_color = "F1F5F9" if row_idx % 2 == 1 else "FFFFFF"
    if row_idx == 4:
        bg_color = "DBEAFE" # Highlight total row
    for col_idx, val in enumerate(row_values):
        row_cells[col_idx].text = val
        set_cell_background(row_cells[col_idx], bg_color)
        set_cell_margins(row_cells[col_idx], top=80, bottom=80, left=100, right=100)
        p = row_cells[col_idx].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx < 6 else WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.font.name = 'Calibri'
            run.font.size = Pt(8.5)
            if row_idx == 4 or col_idx == 0:
                run.font.bold = True
            if row_idx == 4:
                run.font.color.rgb = RGBColor(30, 58, 138)

doc.add_paragraph().paragraph_format.space_before = Pt(10)

doc_path = "reports/Pet_Mode_Forensic_Audit_and_Fixation_Plan.docx"
doc.save(doc_path)
print(f"Successfully generated updated Word report: {doc_path}")
