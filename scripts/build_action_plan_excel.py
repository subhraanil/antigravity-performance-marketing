import os
import shutil
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Output paths
dest_action_plan = "data/Pet Mode/Pet_Mode_Action_Plan.xlsx"
mirror_action_plan = "reports/Pet_Mode_Action_Plan.xlsx"
forecast_file = "data/Pet Mode/Forecast - 25 Sept - Pet Mode.xlsx"

wb = openpyxl.Workbook()

# Styling definitions
title_font = Font(name="Calibri", size=14, bold=True, color="1E3A8A")
title_sub_font = Font(name="Calibri", size=10, italic=True, color="64748B")
header_font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid") # Deep Navy

subhdr_font = Font(name="Calibri", size=11, bold=True, color="1E3A8A")
subhdr_fill = PatternFill(start_color="DBEAFE", end_color="DBEAFE", fill_type="solid") # Soft Blue

regular_font = Font(name="Calibri", size=9.5)
bold_font = Font(name="Calibri", size=9.5, bold=True)
total_font = Font(name="Calibri", size=10, bold=True, color="0F172A")
total_fill = PatternFill(start_color="E2E8F0", end_color="E2E8F0", fill_type="solid") # Light Slate

zebra_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
white_fill = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

p0_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid") # Light red
p0_font = Font(name="Calibri", size=9.5, bold=True, color="991B1B")

p1_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid") # Light amber
p1_font = Font(name="Calibri", size=9.5, bold=True, color="92400E")

p2_fill = PatternFill(start_color="E0F2FE", end_color="E0F2FE", fill_type="solid") # Light sky
p2_font = Font(name="Calibri", size=9.5, bold=True, color="075985")

thin_border_side = Side(border_style="thin", color="CBD5E1")
cell_border = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
total_top_side = Side(border_style="thin", color="1E3A8A")
total_bot_side = Side(border_style="double", color="1E3A8A")
total_border = Border(left=thin_border_side, right=thin_border_side, top=total_top_side, bottom=total_bot_side)

align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
align_left = Alignment(horizontal="left", vertical="center", wrap_text=True)
align_right = Alignment(horizontal="right", vertical="center", wrap_text=True)
align_top_left = Alignment(horizontal="left", vertical="top", wrap_text=True)
align_top_center = Alignment(horizontal="center", vertical="top", wrap_text=True)

currency_fmt = "[$£-809]#,##0.00"
number_fmt = "#,##0"
percent_fmt = "0.00%"
decimal_fmt = "0.00"

# =============================================================
# 1. TAB 1: OPERATIONAL ACTION PLAN (MASTER TABLE)
# =============================================================
ws1 = wb.active
ws1.title = "Operational Action Plan"
ws1.views.sheetView[0].showGridLines = True

# Title block
ws1["A1"] = "PET MODE — 90-DAY OPERATIONAL ACTION PLAN MATRIX"
ws1["A1"].font = title_font
ws1["A2"] = "Action plan to eliminate £2,300+ in wasted spend and achieve Forecast - B (£6,320 Revenue | 224 Orders | £16.96 Blended CPA)"
ws1["A2"].font = title_sub_font

headers_tab1 = ["Phase & Timeline", "Channel / Area", "Action Item", "Step-by-Step Implementation", "Expected Impact & KPI Target", "Priority", "Owner"]
for col_idx, h in enumerate(headers_tab1, start=1):
    c = ws1.cell(row=4, column=col_idx, value=h)
    c.font = header_font
    c.fill = header_fill
    c.alignment = align_center
    c.border = cell_border
ws1.row_dimensions[4].height = 28

action_plan_data = [
    # Phase 1
    ("Phase 1 (Days 1–3)", "Meta Ads", "Terminate Boosted Posts Waste",
     "• Immediately pause all boosted engagement posts, blog promotions, and video views ('With Simon Squibb', 'UK getaway', 'Max Saturday plans', 'Max has two speeds').\n• Reallocate 100% of Meta daily spend exclusively to Advantage+ / Sales campaigns with the Purchase objective.",
     "Eliminates £250–£300/month in zero-conversion waste; stabilizes Meta CPA at £21.00–£22.00.",
     "P0 (Immediate)", "Paid Media Lead"),
     
    ("Phase 1 (Days 1–3)", "Meta Ads", "Lock Down Ad Placements",
     "• Disable standalone Facebook Reels and Instagram Reels ad sets.\n• Restrict delivery strictly to Facebook Feed and Instagram Feed where 77%+ of account purchases occur.",
     "Stops placement budget burn (standalone Reels previously burned £993 with £198+ CPA and 0.14x ROAS).",
     "P0 (Immediate)", "Paid Media Lead"),
     
    ("Phase 1 (Days 1–3)", "Meta Ads", "Demographic & Geo Filtering",
     "• Exclude age bracket 18–24.\n• Focus ad copy and creative hooks toward Women aged 35–65+ in the United Kingdom (who generate 64.2% of all purchases).",
     "Eliminates spend on non-converting male 18–34 segments; lifts click-to-purchase intent.",
     "P1 (High)", "Paid Media Lead"),

    # Phase 2
    ("Phase 2 (Days 3–7)", "Google Ads / GMC", "Feed Country & Shipping Hygiene",
     "• In Shopify Admin > Apps > Google & YouTube > Settings > Manage availability for countries: Deselect international markets; set strictly to United Kingdom (GBP).\n• Confirm in Merchant Center that products transition from yellow 'Limited' to green 'Approved'.",
     "Eliminates ~7,000 unserviced variant rows and 'Missing shipping info' warnings; unblocks Google Shopping algorithm.",
     "P0 (Immediate)", "eCommerce Specialist"),
     
    ("Phase 2 (Days 3–7)", "Google Ads", "Negative Keyword Exclusion List",
     "• Create and apply an account-level negative keyword list in Google Ads.\n• Add competitor brands: costco, gulpup, 3 peaks, pets at home.\n• Add controversial/negative terms: shock, electric, free, wholesale, cheap.",
     "Stops £430+ in non-converting query spend (42.7% of PMax spend); cuts Google CPA from £40.89 to £25.00.",
     "P0 (Immediate)", "Search Specialist"),
     
    ("Phase 2 (Days 3–7)", "Google Ads", "PMax Asset Group Restructuring",
     "• Re-segment Sales-Performance Max into 3 dedicated asset groups:\n  1. Hero Dental Care: Dog Toothbrush Molar Stick & Chew Toys.\n  2. Humane Training: Anti-Bark Collar (highlighting humane vibration/sound).\n  3. Comfort & Travel: Dog Car Seat Bed & Velvet Mats.",
     "Allocates paid impressions to Pet Mode's #1 organic volume driver (£16.99 Chew Toy received only £7.86 spend previously).",
     "P1 (High)", "Search Specialist"),

    # Phase 3
    ("Phase 3 (Days 7–14)", "Shopify Email", "Deploy 3-Part Abandoned Cart Flow",
     "• Configure automated workflow in Shopify Email:\n  - Email 1 (1 hr): 'Did your pup forget something?' (Clean visual reminder).\n  - Email 2 (24 hrs): 10% voucher code PUPPY10 + customer reviews.\n  - Email 3 (48 hrs): 'Final hours: Your voucher expires tonight'.",
     "Recovers 5–8 lost orders/month (~£150–£220 net revenue) at £0 marginal media cost.",
     "P0 (High)", "CRM / Email Lead"),
     
    ("Phase 3 (Days 7–14)", "Shopify CRO", "Free Shipping Threshold at £35",
     "• Update Shopify shipping settings to offer Free UK Shipping on orders over £35.00 (currently flat £5.97 shipping on single items).\n• Add an announcement bar banner: 'Free UK Delivery on orders over £35'.",
     "Removes checkout friction; motivates shoppers to add a second product to cart to waive shipping.",
     "P1 (High)", "Store Manager"),
     
    ("Phase 3 (Days 7–14)", "Shopify Storefront", "Launch Hero Bundles & Kits",
     "• Create a 2-Pack Dental Defense Bundle SKU at £26.99 (saving customer ~£7 vs two single items).\n• Create a New Pet Parent Care Kit (Chew Toy + Grooming Brush + Mat).",
     "Directly addresses single-item bottleneck (89.2% of orders have only 1 item); lifts AOV from £21 to £28+.",
     "P1 (High)", "Store Manager"),
     
    ("Phase 3 (Days 7–14)", "Shopify Email", "Post-Purchase Replenishment Flow",
     "• Automated email triggered 14 days after order delivery:\n  - Care tips for their new product.\n  - 15% VIP discount code for replacement chew sticks or grooming tools.",
     "Increases repeat customer rate from baseline 3.6% to 8–10%, generating compounding organic orders.",
     "P2 (Medium)", "CRM / Email Lead"),

    # Phase 4
    ("Phase 4 (October)", "Omnichannel", "October Foundation Execution",
     "• Hold total ad spend at £1,100 (£500 Google / £600 Meta).\n• Monitor CPA stabilization under £20.\n• Weekly tracking against target of 57 orders (47 paid, 10 email/organic).",
     "October Target: 57 Orders | £1,493 Revenue | £19.30 Blended CPA | 1.36x ROAS.",
     "P0 (Ongoing)", "Paid Media Lead"),
     
    ("Phase 4 (November)", "Omnichannel", "November Black Friday (BFCM) Sprint",
     "• Scale total spend to £1,300 (£600 Google / £700 Meta).\n• Launch Early BFCM promo on 2-Pack Dental Bundles.\n• Capitalize on seasonal conversion surge (Meta CR 3.8%, Google CR 2.7%).",
     "November Target: 80 Orders | £2,252 Revenue | £16.25 Blended CPA | 1.73x ROAS.",
     "P0 (Ongoing)", "Paid Media Lead"),
     
    ("Phase 4 (December)", "Omnichannel", "December Holiday Gifting Sprint",
     "• Front-load £1,400 spend into Weeks 1–3 (Dec 1–18).\n• Display site-wide urgency badge: 'Order by Dec 18 for Guaranteed Christmas Delivery'.\n• Scale back ad spend Dec 21–31 to protect delivery satisfaction.",
     "December Target: 87 Orders | £2,575 Revenue | £16.09 Blended CPA | 1.84x ROAS.",
     "P0 (Ongoing)", "Paid Media Lead")
]

for row_idx, r_data in enumerate(action_plan_data, start=5):
    fill_to_use = zebra_fill if (row_idx % 2 == 1) else white_fill
    for col_idx, val in enumerate(r_data, start=1):
        cell = ws1.cell(row=row_idx, column=col_idx, value=val)
        cell.font = regular_font
        cell.fill = fill_to_use
        cell.border = cell_border
        
        if col_idx in [1, 2, 7]:
            cell.alignment = align_top_center if col_idx != 3 else align_top_left
            if col_idx == 1: cell.font = bold_font
        elif col_idx in [3, 4, 5]:
            cell.alignment = align_top_left
            if col_idx == 3: cell.font = bold_font
        elif col_idx == 6: # Priority badge
            cell.alignment = align_top_center
            if "P0" in val:
                cell.fill = p0_fill
                cell.font = p0_font
            elif "P1" in val:
                cell.fill = p1_fill
                cell.font = p1_font
            elif "P2" in val:
                cell.fill = p2_fill
                cell.font = p2_font
    ws1.row_dimensions[row_idx].height = 58

# Set specific column widths for Tab 1
col_widths_tab1 = {1: 20, 2: 18, 3: 28, 4: 55, 5: 38, 6: 16, 7: 18}
for c_idx, w in col_widths_tab1.items():
    ws1.column_dimensions[get_column_letter(c_idx)].width = w


# =============================================================
# 2. TAB 2: WEEKLY EXECUTION CHECKLIST
# =============================================================
ws2 = wb.create_sheet("Weekly Execution Checklist")
ws2.views.sheetView[0].showGridLines = True

ws2["A1"] = "PET MODE — WEEKLY EXECUTION CHECKLIST & MILESTONES"
ws2["A1"].font = title_font
ws2["A2"] = "Chronological roadmap of weekly operational deliverables and success verification gates"
ws2["A2"].font = title_sub_font

headers_tab2 = ["Week & Dates", "Target Focus", "Concrete Deliverables", "Success Gate / Verification Milestone", "Status"]
for col_idx, h in enumerate(headers_tab2, start=1):
    c = ws2.cell(row=4, column=col_idx, value=h)
    c.font = header_font
    c.fill = header_fill
    c.alignment = align_center
    c.border = cell_border
ws2.row_dimensions[4].height = 28

weekly_data = [
    ("Week 1 (Sep 28 – Oct 4)", "Bleeder Elimination & Feed Fix",
     "• Pause all Meta boosted engagement posts.\n• Restrict Meta ad sets strictly to Feed placements.\n• In Shopify Google App, restrict countries to UK only.\n• Apply negative keyword list in Google Ads.",
     "1. Zero spend on boosted vanity posts.\n2. Google Merchant Center products turn green 'Approved'.\n3. Search terms report shows no competitor impressions.",
     "Pending"),
     
    ("Week 2 (Oct 5 – Oct 11)", "Email Flows & Bundling",
     "• Build & activate 3-part abandoned checkout flow in Shopify Email.\n• Publish 2-Pack Dental Bundle SKU at £26.99 on Shopify.\n• Set Free Shipping threshold at £35.00.",
     "1. Test abandoned cart email triggered successfully.\n2. Bundle live and featured on homepage.\n3. Free shipping banner visible on mobile & desktop.",
     "Pending"),
     
    ("Week 3 (Oct 12 – Oct 18)", "Asset Groups & Creative Rotation",
     "• Restructure Google PMax into 3 dedicated asset groups.\n• Refresh Meta Feed ads with high-performing Molar Stick creatives ('Test - New Sales Ad Molar Stick').",
     "1. Google PMax impressions shifting toward Dental Stick.\n2. Meta CPA trending under £22.00.",
     "Pending"),
     
    ("Week 4 (Oct 19 – Oct 25)", "Mid-Month Review & Tuning",
     "• Review October actuals vs forecast (target: ~28 orders by mid-month).\n• Fine-tune demographic exclusions and ad scheduling.",
     "1. Month-to-date blended CPA <= £19.30.\n2. Email flows generating 10%+ of total store orders.",
     "Pending"),
     
    ("Weeks 5–8 (Nov 1 – Nov 30)", "Black Friday Scaling",
     "• Ramp weekly spend to £300–£325/week.\n• Scale winning bundle ad sets on Meta & Google.\n• Send 2 dedicated BFCM campaign emails to customer list.",
     "1. November delivery of 80 total orders.\n2. Revenue reaching £2,252 at 1.73x ROAS.",
     "Pending"),
     
    ("Weeks 9–12 (Dec 1 – Dec 20)", "Christmas Delivery Sprint",
     "• Front-load ad spend (£350–£400/week) through Dec 18.\n• Promote Christmas gift sets and guaranteed shipping deadline.\n• Taper ad spend down after Dec 20 shipping cutoff.",
     "1. December delivery of 87 total orders.\n2. Revenue reaching £2,575 at 1.84x ROAS.",
     "Pending")
]

for row_idx, r_data in enumerate(weekly_data, start=5):
    fill_to_use = zebra_fill if (row_idx % 2 == 1) else white_fill
    for col_idx, val in enumerate(r_data, start=1):
        cell = ws2.cell(row=row_idx, column=col_idx, value=val)
        cell.font = regular_font
        cell.fill = fill_to_use
        cell.border = cell_border
        
        if col_idx == 1:
            cell.alignment = align_top_center
            cell.font = bold_font
        elif col_idx in [2, 3, 4]:
            cell.alignment = align_top_left
            if col_idx == 2: cell.font = bold_font
        elif col_idx == 5:
            cell.alignment = align_top_center
            cell.font = p1_font
            cell.fill = p1_fill
    ws2.row_dimensions[row_idx].height = 65

col_widths_tab2 = {1: 22, 2: 26, 3: 48, 4: 48, 5: 14}
for c_idx, w in col_widths_tab2.items():
    ws2.column_dimensions[get_column_letter(c_idx)].width = w


# =============================================================
# 3. TAB 3: Q4 MILESTONE TARGETS (FORECAST - B SUMMARY)
# =============================================================
ws3 = wb.create_sheet("Q4 Milestone Targets")
ws3.views.sheetView[0].showGridLines = True

ws3["A1"] = "PET MODE — Q4 2026 FORECAST - B TARGET SUMMARY"
ws3["A1"].font = title_font
ws3["A2"] = "Channel breakdown and monthly run-rate targets supporting the 4-phase action plan"
ws3["A2"].font = title_sub_font

headers_tab3 = ["Month", "Total Spend", "Google Orders", "Meta Orders", "Email / Organic", "Total Orders", "Blended CPA", "Total Revenue", "Blended ROAS", "Key Milestone"]
for col_idx, h in enumerate(headers_tab3, start=1):
    c = ws3.cell(row=4, column=col_idx, value=h)
    c.font = header_font
    c.fill = header_fill
    c.alignment = align_center
    c.border = cell_border
ws3.row_dimensions[4].height = 28

kpi_summary_data = [
    ("October 2026", 1100.00, 20, 27, 10, "=C5+D5+E5", "=B5/F5", 1493.00, "=H5/B5", "Bleeders cut; GMC feed fixed; email flows live"),
    ("November 2026", 1300.00, 26, 40, 14, "=C6+D6+E6", "=B6/F6", 2252.00, "=H6/B6", "BFCM surge; Dental Bundle & Feed ads scaled"),
    ("December 2026", 1400.00, 29, 44, 14, "=C7+D7+E7", "=B7/F7", 2575.00, "=H7/B7", "Spend front-loaded; Christmas gift sets"),
    ("3-Month Total", "=SUM(B5:B7)", "=SUM(C5:C7)", "=SUM(D5:D7)", "=SUM(E5:E7)", "=SUM(F5:F7)", "=B8/F8", "=SUM(H5:H7)", "=H8/B8", "224 orders, £6,320 revenue, delivered profitably")
]

for row_idx, r_data in enumerate(kpi_summary_data, start=5):
    is_tot = (row_idx == 8)
    fill_to_use = total_fill if is_tot else (zebra_fill if row_idx % 2 == 1 else white_fill)
    border_to_use = total_border if is_tot else cell_border
    
    for col_idx, val in enumerate(r_data, start=1):
        cell = ws3.cell(row=row_idx, column=col_idx, value=val)
        cell.font = total_font if is_tot else regular_font
        cell.fill = fill_to_use
        cell.border = border_to_use
        
        if col_idx == 1:
            cell.alignment = align_left
            cell.font = total_font if is_tot else bold_font
        elif col_idx in [2, 7, 8]:
            cell.alignment = align_right
            cell.number_format = currency_fmt
        elif col_idx in [3, 4, 5, 6]:
            cell.alignment = align_right
            cell.number_format = number_fmt
        elif col_idx == 9:
            cell.alignment = align_right
            cell.number_format = decimal_fmt
        elif col_idx == 10:
            cell.alignment = align_left
            if is_tot: cell.font = total_font
    ws3.row_dimensions[row_idx].height = 25

col_widths_tab3 = {1: 18, 2: 15, 3: 15, 4: 15, 5: 16, 6: 14, 7: 15, 8: 16, 9: 15, 10: 42}
for c_idx, w in col_widths_tab3.items():
    ws3.column_dimensions[get_column_letter(c_idx)].width = w

# Save standalone Action Plan workbook
wb.save(dest_action_plan)
print(f"Saved standalone Action Plan workbook to: {dest_action_plan}")

shutil.copyfile(dest_action_plan, mirror_action_plan)
print(f"Mirrored standalone Action Plan workbook to: {mirror_action_plan}")


# =============================================================
# 4. ALSO EMBED 'Operational Action Plan' INTO FORECAST WORKBOOK
# =============================================================
if os.path.exists(forecast_file):
    wb_forecast = openpyxl.load_workbook(forecast_file)
    if "Operational Action Plan" in wb_forecast.sheetnames:
        del wb_forecast["Operational Action Plan"]
        
    ws_embedded = wb_forecast.create_sheet("Operational Action Plan")
    ws_embedded.views.sheetView[0].showGridLines = True
    
    from copy import copy
    # Copy from ws1
    for r in range(1, ws1.max_row + 1):
        ws_embedded.row_dimensions[r].height = ws1.row_dimensions[r].height
        for c in range(1, ws1.max_column + 1):
            src_cell = ws1.cell(r, c)
            dest_cell = ws_embedded.cell(r, c, src_cell.value)
            if src_cell.has_style:
                dest_cell.font = copy(src_cell.font)
                dest_cell.fill = copy(src_cell.fill)
                dest_cell.border = copy(src_cell.border)
                dest_cell.alignment = copy(src_cell.alignment)
                dest_cell.number_format = copy(src_cell.number_format)
            
    for col_idx in range(1, ws1.max_column + 1):
        col_letter = get_column_letter(col_idx)
        ws_embedded.column_dimensions[col_letter].width = ws1.column_dimensions[col_letter].width
        
    wb_forecast.save(forecast_file)
    print(f"Embedded 'Operational Action Plan' into: {forecast_file}")
    
    mirror_forecast = "reports/Forecast - 25 Sept.xlsx"
    shutil.copyfile(forecast_file, mirror_forecast)
    print(f"Mirrored forecast to: {mirror_forecast}")

print("All Excel Action Plan deliverables successfully generated!")
