import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=60, bottom=60, left=80, right=80):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_styled_table(doc, data, header_bg="102C57", zebra=True, center_cols=[], right_cols=[]):
    table = doc.add_table(rows=len(data), cols=len(data[0]))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    for r_idx, row_vals in enumerate(data):
        row = table.rows[r_idx]
        is_header = (r_idx == 0)
        is_total = (r_idx == len(data) - 1 and ("Total" in str(row_vals[0]) or "Upper bound" in str(row_vals[0])))
        
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.text = str(val)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(3)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.line_spacing = 1.05
            
            if c_idx in center_cols:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif c_idx in right_cols:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            for run in p.runs:
                run.font.name = "Calibri"
                if is_header:
                    run.font.size = Pt(8.5)
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(255, 255, 255)
                elif is_total:
                    run.font.size = Pt(8.5)
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(16, 44, 87)
                else:
                    run.font.size = Pt(8.0)
                    run.font.color.rgb = RGBColor(30, 30, 30)
                    
            if is_header:
                set_cell_background(cell, header_bg)
            elif is_total:
                set_cell_background(cell, "EAECEE")
            else:
                if zebra and r_idx % 2 == 1:
                    set_cell_background(cell, "F9FAFB")
            set_cell_margins(cell, top=55, bottom=55, left=65, right=65)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_docx_report(output_docx_path):
    doc = docx.Document()
    
    # Page setup
    sections = doc.sections
    for s in sections:
        s.top_margin = Inches(0.8)
        s.bottom_margin = Inches(0.8)
        s.left_margin = Inches(0.8)
        s.right_margin = Inches(0.8)
        
        # Header
        header = s.header
        hp = header.paragraphs[0]
        hp.text = "FABB6 Performance Audit, Turnaround Plan & Dec 2026 – Feb 2027 Forecast"
        hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in hp.runs:
            run.font.name = "Calibri"
            run.font.size = Pt(8)
            run.font.color.rgb = RGBColor(120, 120, 120)

    # Document Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    run_t = p_title.add_run("FABB6 Performance Audit, Turnaround Plan\n& Dec 2026 – Feb 2027 Forecast")
    run_t.font.name = "Georgia"
    run_t.font.size = Pt(20)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(26, 36, 43)

    # Subtitle
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(14)
    run_sub = p_sub.add_run("Techno Exponent | Performance Marketing & Enterprise Growth Practice Prepared for\nFABB6 (Glanzzkart Private Limited) · Data through 18 November 2026 · Confidential")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(9.5)
    run_sub.font.color.rgb = RGBColor(80, 80, 80)

    # Helper function for headings
    def add_h1(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(14)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.name = "Georgia"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(16, 44, 87)
        return h

    def add_h2(text):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(10)
        h.paragraph_format.space_after = Pt(3)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = RGBColor(31, 78, 120)
        return h

    def add_body(text, bold_prefix=""):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = "Calibri"
            rb.font.size = Pt(9.5)
            rb.font.bold = True
            rb.font.color.rgb = RGBColor(30, 30, 30)
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(40, 40, 40)
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(1)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = "Calibri"
            rb.font.size = Pt(9.5)
            rb.font.bold = True
            rb.font.color.rgb = RGBColor(30, 30, 30)
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.color.rgb = RGBColor(40, 40, 40)
        return p

    # 1. Executive Summary
    add_h1("1. Executive Summary")
    add_body("This report reviews Google Ads and Meta Ads performance from December 2025 to 18 November 2026, audits the account state we inherited from the interim agency (SilverXis, September to November 2026), and sets out a stabilization plan and a forecast for December 2026 to February 2027.")
    
    add_h2("What the numbers say")
    add_bullet("In August 2026, FABB6 recorded ₹95.64 Lakhs of Shopify gross sales across 11,069 orders on ₹47.91 Lakhs of ad spend (2.00x gross sales ÷ ad spend).")
    add_bullet("Between 1 September and 18 November 2026, ad spend was ₹67.83 Lakhs (Google ₹34.84L, Meta ₹32.99L) against Shopify gross sales of ₹1.95 Cr.")
    add_bullet("Headline efficiency in October (2.49x) and November to date (2.79x) was in line with or better than June to August (2.00x–2.42x). Paid CPA in October (₹582) was 33% above August (₹437), but average order value rose by a similar amount (₹864 to ₹1,156).")
    add_bullet("The most serious disruption was September: ad spend fell 87% against August and Shopify orders fell 72% to 3,112.")

    add_h2("What the audit found")
    add_body("The problems are in account hygiene, tracking and structure rather than in a collapse of headline efficiency. Each is documented in the change history and exports (Exhibits A–F):")
    add_bullet("The primary Google purchase conversion action ('Purchase-2026') was deleted on 18 September.")
    add_bullet("Live Performance Max asset groups contained copy referencing another brand.")
    add_bullet("110 products pointed to unavailable (404) pages in Merchant Center.")
    add_bullet("Meta retargeting (DPA) ran more expensively than cold prospecting, three Advantage+ Shopping campaigns ran concurrently, and about ₹1.5 Lakhs was spent on campaigns with zero orders.")
    add_body(" between ₹1.50 Lakhs (spend with zero orders, provable) and ₹7.47 Lakhs (total spend in the affected campaigns, upper bound). Our central estimate of excess spend is about ₹5.9 Lakhs (Section 5).", bold_prefix="Quantified waste:")
    add_body(" on a planned ad spend of ₹91.1 Lakhs, the base case delivers about ₹2.51 Cr of Shopify gross sales (2.75x), with a range of ₹2.10 Cr (conservative) to ₹2.83 Cr (stretch). The forecast is built on observed Shopify gross-to-spend ratios, not platform-attributed revenue (Section 7).", bold_prefix="Forecast (Dec 2026 – Feb 2027):")

    # 2. Twelve-Month Performance Reconciliation
    add_h1("2. Twelve-Month Performance Reconciliation")
    add_body("August 2026 Google Ads spend had been overstated in earlier raw exports (₹67.07 Lakhs, caused by a reporting glitch). The reconciled figure is ₹32.23 Lakhs. All figures below use the reconciled data.")
    
    hist_table_data = [
        ["Month", "Managed by", "Total spend", "Paid orders (platform)", "Paid CPA", "Shopify orders", "Shopify gross", "Gross ÷ spend"],
        ["Dec 2025", "Prior agency", "₹4.21L", "1,614", "₹261", "3,307", "₹26.38L", "6.27x"],
        ["Jan 2026", "Prior agency", "₹12.17L", "4,260", "₹286", "7,850", "₹55.52L", "4.56x"],
        ["Feb 2026", "Prior agency", "₹17.97L", "4,817", "₹373", "8,250", "₹64.10L", "3.57x"],
        ["Mar 2026", "Prior agency", "₹27.84L", "6,351", "₹438", "11,285", "₹85.32L", "3.06x"],
        ["Apr 2026", "Prior agency", "₹32.55L", "5,350", "₹608", "10,551", "₹84.73L", "2.60x"],
        ["May 2026", "Prior agency", "₹40.21L", "7,076", "₹568", "12,215", "₹100.96L", "2.51x"],
        ["Jun 2026", "Prior agency", "₹42.86L", "6,851", "₹626", "12,877", "₹103.89L", "2.42x"],
        ["Jul 2026", "Prior agency", "₹43.62L", "8,313", "₹525", "13,420", "₹103.64L", "2.38x"],
        ["Aug 2026", "Prior agency", "₹47.91L", "10,965", "₹437", "11,069", "₹95.64L", "2.00x"],
        ["Sep 2026", "SilverXis", "₹6.27L", "801", "₹783", "3,112", "₹36.02L", "5.74x"],
        ["Oct 2026", "SilverXis", "₹42.47L", "7,298", "₹582", "9,143", "₹105.67L", "2.49x"],
        ["Nov 2026 (to 18 Nov)", "SilverXis", "₹19.09L", "4,310", "₹443", "4,638", "₹53.18L", "2.79x"],
    ]
    create_styled_table(doc, hist_table_data, header_bg="102C57", center_cols=[3, 5, 7], right_cols=[2, 4, 6])
    
    add_body("Gross ÷ spend = Shopify gross sales ÷ total Google and Meta spend. Paid orders are platform-attributed and overlap with Shopify orders.")
    add_h2("Three observations that shape the plan")
    add_bullet("From December 2025 to August 2026, spend grew more than tenfold and gross ÷ spend fell from 6.3x to 2.0x. Some decline is the normal cost of scaling into colder audiences, and we treat 2.0x–2.8x as the realistic operating band for ₹25–45 Lakhs of monthly spend.", bold_prefix="1. Efficiency fell as spend scaled: ")
    add_bullet("Spend was cut by 87%, so the ratio reflects the organic and repeat demand that continued without paid support.", bold_prefix="2. September's 5.74x is not an efficiency gain: ")
    add_bullet("April (₹608) and June (₹626) were higher. October's issue was a CPA 33% above August, partly offset by higher order value.", bold_prefix="3. October CPA was not a record: ")
    add_body("The Festival of Lights (Diwali) fell on 8 November in 2026, so the festive demand window straddles October and November. The November run-rate therefore includes festive uplift and is not used as a December baseline.")

    # 3. Google Ads Audit
    add_h1("3. Google Ads Audit")
    add_body("Google Ads spend during the interim period totaled ₹34.84 Lakhs. Findings from the change history, asset group, product and search term reports:")
    add_bullet("The change history shows the 'Purchase-2026' conversion action was deleted by an administrator account on the SilverXis side (Exhibit A). Smart Bidding lost its main learning signal. September Google spend was ₹3.18 Lakhs for 42 attributed orders (₹7,569 CPA). Because 17 days of the month preceded the deletion and post-deletion sales may be unattributed, the true cost per sale is likely lower than this figure, and we will validate it against Shopify UTM data.", bold_prefix="1. Primary purchase conversion deleted (18 Sep): ")
    add_bullet("Several asset groups (T4 Pro/Salon, T3 Premium, Pilgrim, YS24) contained headlines and descriptions promoting a different brand name (Exhibit B). All were rated 'Poor' for Ad Strength.", bold_prefix="2. Another brand's copy in live Performance Max asset groups: ")
    add_bullet("Merchant Center shows 216 ineligible products: 110 with 'page unavailable' (404) and 70 with promotional overlay violations. At least ₹80,285 was spent on affected products with zero conversions (for example, one serum SKU spent ₹1,614 on 480 clicks into a 404 page).", bold_prefix="3. 110 broken product pages: ")
    add_bullet("Daily budgets were changed 140 times in under 60 days (74 increases, 66 decreases). We cannot isolate the effect on delivery, but constant changes make Smart Bidding performance harder to read and slower to stabilize.", bold_prefix="4. Frequent budget changes: ")
    add_bullet("A campaign named 'Search-Brand' used broad match and triggered queries unrelated to beauty (for example, gym equipment and a badminton ankle support). The spend on these queries is not yet quantified; it will be after a full search terms export.", bold_prefix="5. Off-category search queries: ")

    # 4. Meta Ads Audit
    add_h1("4. Meta Ads Audit")
    add_body("Meta spend during the interim period totaled ₹32.99 Lakhs.")
    add_bullet("'Retargeting — DPA - Fabb6' spent ₹9.50 Lakhs for 1,850 purchases at ₹513.70 CPA (peaking at ₹570.31 in October), against ₹479.53 for cold prospecting, with frequency of 3.21 and no past-purchaser exclusions. Excess cost against the cold-prospecting CPA is about ₹63,000.", bold_prefix="1. Retargeting more expensive than prospecting: ")
    add_bullet("Three Advantage+ Shopping campaigns ran at the same time without product exclusions, so they competed in the same auctions. Account CPM rose from ₹56.15 in August to ₹104.17 in October (+85%) and ₹137.03 in November (+144%). Q4 festive demand raises CPMs for all advertisers, so part of this rise is seasonal. Consolidation to one master campaign will let us measure the effect cleanly.", bold_prefix="2. Overlapping Advantage+ Shopping campaigns: ")
    add_bullet("₹50,214 across 8.32 million impressions produced 1,02,322 link clicks, 28 landing page views and 0 purchases (99.97% drop-off between click and page view).", bold_prefix="3. 'IG-Traffic' link-click campaign: ")
    add_bullet("The iOS campaign spent ₹19,161 at frequency 13.18 with 0 sales. The Android campaign spent about ₹1.38 Lakhs at ₹1,082 CPA.", bold_prefix="4. App install campaigns: ")
    add_bullet("Meta reported 7,34,064 link clicks but only 3,01,798 landing page views on Shopify: a 58.9% gap (52.2% excluding IG-Traffic). Likely causes are mobile page speed, accidental clicks, and pixel or Conversions API (CAPI) misfires. We will diagnose these in the first two weeks.", bold_prefix="5. Click-to-landing-page gap: ")

    # 5. Avoidable Spend: A Range, Not a Single Number
    add_h1("5. Avoidable Spend: A Range, Not a Single Number")
    
    waste_table_data = [
        ["Measure", "Amount", "Basis"],
        ["Provable floor: spend with zero orders", "₹1,49,660", "404 products (₹80,285), IG-Traffic (₹50,214), iOS app campaign (₹19,161)"],
        ["Central estimate: excess spend versus benchmark CPA", "about ₹5.87 Lakhs", "Floor, plus Google September excess against the August Google CPA of ₹480 (₹2.98L), Android app excess (about ₹0.77L), DPA excess against cold CPA (about ₹0.63L)"],
        ["Upper bound: total spend in affected campaigns", "₹7,46,558", "Google September ₹3,17,895; 404 products ₹80,285; IG-Traffic ₹50,214; app campaigns ₹1,57,302; DPA ₹1,40,862"]
    ]
    create_styled_table(doc, waste_table_data, header_bg="102C57", center_cols=[1], right_cols=[])
    add_body("The upper bound counts all spend in affected campaigns, including spend that did produce some orders, and should not be read as pure loss. The Google September figure may include sales that went unattributed after the conversion action was deleted.")

    # 6. Turnaround Plan
    add_h1("6. Turnaround Plan")
    add_body("Admin access has been verified across Google Ads, Meta Business Suite, Google Merchant Center and Shopify. Shopify is the source of truth for revenue and orders throughout.")
    
    add_h2("Phase 1: Immediate triage (hours 0 – 48)")
    add_bullet("Pause 'IG-Traffic' and the iOS and Android app install campaigns.")
    add_bullet("Remove foreign-brand copy from all Performance Max asset groups.")
    add_bullet("Exclude the 110 unavailable (404) products in Merchant Center and fix or remove the overlay violations.")
    add_bullet("Confirm a single primary Purchase conversion action is active in Google Ads and matches Shopify order counts. Verify Enhanced Conversions, and test Meta CAPI deduplication.")
    add_bullet("Export search terms and add negative keywords for off-category queries.")

    add_h2("Phase 2: Restructure and stabilize (December 2026)")
    add_bullet("Segment Performance Max into Hero Best-Sellers (60% of budget), Long-Tail Catalog (20%) and Search/Brand (20%).")
    add_bullet("Consolidate Meta into one master Advantage+ Shopping campaign with a 20% existing-customer budget cap.")
    add_bullet("Add 30-day and 180-day purchaser exclusions to DPA, with frequency capped at 2.2 or below.")
    add_bullet("Launch 10 new creator (UGC) assets focused on winter skincare routines and gifting.")
    add_bullet("Diagnose the click-to-landing-page gap (page speed, pixel and CAPI audit).")

    add_h2("Phase 3: Profitable scaling (January – February 2027)")
    add_bullet("Increase budgets by no more than 20% every 72 hours per campaign.")
    add_bullet("Expand high-intent non-brand Google search for hero categories (serums, brightening, anti-aging).")
    add_bullet("Launch post-purchase replenishment flows (email and WhatsApp) at 30, 45 and 60 days. Retention revenue is treated as upside and is not included in the forecast.")
    add_body("scale a step only if trailing seven-day gross ÷ spend is at least 2.5x and CPA is within target. Hold between 2.3x and 2.5x. Roll back the last increase if the ratio stays below 2.3x for seven days.", bold_prefix="Scaling decision rule: ")

    # 7. Forecast: December 2026 – February 2027
    add_h1("7. Forecast: December 2026 – February 2027")
    add_h2("7.1 Approach")
    add_body("The forecast is built on Shopify gross sales divided by ad spend, the measure that can be reconciled to the store. Platform-attributed revenue overlaps with store revenue and is used only for channel-level CPA guardrails. Planned spend follows the agreed ramp: ₹26.0L in December, ₹31.0L in January and ₹34.1L in February (₹91.1L in total). The December spend is below the November run-rate (about ₹31.8L) because we are removing waste and restructuring before scaling.")
    add_body("₹31.8L spend, about 7,730 orders (258/day), ₹88.6L gross, average order value ₹1,147, 2.79x. This includes festive uplift.", bold_prefix="Reference run-rate (1 – 18 November, extrapolated to 30 days): ")

    add_h2("7.2 Base case")
    base_table_data = [
        ["Month", "Ad spend (Google / Meta)", "Store orders", "Orders per day", "AOV", "Shopify gross", "Spend per order", "Gross ÷ spend"],
        ["Dec 2026", "₹26.0L (₹16.0L / ₹10.0L)", "6,382", "206", "₹1,100", "₹70.2L", "₹407", "2.70x"],
        ["Jan 2027", "₹31.0L (₹20.0L / ₹11.0L)", "7,750", "250", "₹1,100", "₹85.3L", "₹400", "2.75x"],
        ["Feb 2027", "₹34.1L (₹22.0L / ₹12.1L)", "8,680", "310", "₹1,100", "₹95.5L", "₹393", "2.80x"],
        ["Total", "₹91.1L", "22,812", "253", "₹1,100", "₹250.9L (₹2.51 Cr)", "₹399", "2.75x"]
    ]
    create_styled_table(doc, base_table_data, header_bg="102C57", center_cols=[2, 3, 7], right_cols=[4, 5, 6])
    add_body("Spend per order (₹393–₹407) is consistent with the ₹412 observed in November to date.")

    add_h2("7.3 Scenarios")
    scen_table_data = [
        ["Scenario", "Gross ÷ spend (Dec / Jan / Feb)", "Dec gross", "Jan gross", "Feb gross", "Quarter total", "Quarter ratio"],
        ["Conservative", "2.30x / 2.30x / 2.30x", "₹59.8L", "₹71.3L", "₹78.4L", "₹209.5L (₹2.10 Cr)", "2.30x"],
        ["Base", "2.70x / 2.75x / 2.80x", "₹70.2L", "₹85.3L", "₹95.5L", "₹250.9L (₹2.51 Cr)", "2.75x"],
        ["Stretch", "3.00x / 3.10x / 3.20x", "₹78.0L", "₹96.1L", "₹109.1L", "₹283.2L (₹2.83 Cr)", "3.11x"]
    ]
    create_styled_table(doc, scen_table_data, header_bg="102C57", center_cols=[1, 6], right_cols=[2, 3, 4, 5])
    add_body("The conservative case matches July to August efficiency (2.0x–2.4x). The base case sits between October (2.49x) and November to date (2.79x). The stretch case requires the waste removal and restructuring to lift efficiency above anything achieved at this spend level since March.")

    add_h2("7.4 Channel-level guardrails (platform-attributed)")
    chan_table_data = [
        ["Month", "Google spend", "Google CPA target", "Google orders", "Meta spend", "Meta CPA target", "Meta orders", "Combined paid orders"],
        ["Dec 2026", "₹16.0L", "₹450", "3,556", "₹10.0L", "₹450", "2,222", "5,778"],
        ["Jan 2027", "₹20.0L", "₹430", "4,651", "₹11.0L", "₹410", "2,683", "7,334"],
        ["Feb 2027", "₹22.0L", "₹410", "5,366", "₹12.1L", "₹385", "3,143", "8,509"]
    ]
    create_styled_table(doc, chan_table_data, header_bg="102C57", center_cols=[3, 6, 7], right_cols=[1, 2, 4, 5])
    add_body("Combined paid orders equal about 91% (Dec), 95% (Jan) and 98% (Feb) of base-case store orders, against a historical range of 80%–99%. The February CPA targets are the most demanding part of the plan.")

    add_h2("7.5 Key assumptions and risks")
    add_bullet("Average order value of ₹1,100 sits below the October and November level (about ₹1,150) and above the July to August level (₹770–₹860). A 10% change in AOV moves base-case gross by about ₹25 Lakhs.")
    add_bullet("Gross sales include orders later cancelled or returned (including COD returns to origin). Monthly reconciliation is made against Shopify net revenue.")
    add_bullet("Higher spend lowers marginal efficiency. The scaling decision rule in Section 6 is the control.")
    add_bullet("Retention flows are upside and not in the numbers.")
    add_bullet("Seasonal effects (winter, wedding season, post-festive slowdown) are not modelled separately.")

    # 8. Operating Guardrails
    add_h1("8. Operating Guardrails")
    add_bullet("New campaigns, ad sets and creatives are created paused and go live only after tracking, UTM parameters and margin review are confirmed.", bold_prefix="1. Paused-first creation: ")
    add_bullet("Increases are capped at 20% every 72 hours per campaign.", bold_prefix="2. Budget pacing: ")
    add_bullet("Prospecting campaigns exclude 30-day purchasers and customer lists. Retargeting excludes purchasers.", bold_prefix="3. Audience hygiene: ")
    add_bullet("Automated daily scans of Merchant Center and Shopify disapprove products with dead URLs or no stock.", bold_prefix="4. Daily feed checks: ")
    add_bullet("A daily pacing update by WhatsApp or Slack, a weekly performance review, and a monthly reconciliation against Shopify net revenue.", bold_prefix="5. Reporting cadence: ")

    # Appendix A
    add_h1("Appendix A: Evidence Exhibits to Attach")
    add_bullet("Google Ads change history showing deletion of 'Purchase-2026' (18 Sep).", bold_prefix="Exhibit A: ")
    add_bullet("Performance Max asset group report showing foreign-brand copy and Ad Strength ratings.", bold_prefix="Exhibit B: ")
    add_bullet("Merchant Center product diagnostics (404 and overlay violations).", bold_prefix="Exhibit C: ")
    add_bullet("Google Ads budget change log and search terms report.", bold_prefix="Exhibit D: ")
    add_bullet("Meta campaign exports (DPA, Advantage+ Shopping, IG-Traffic, app campaigns), with CPM and frequency by month.", bold_prefix="Exhibit E: ")
    add_bullet("Meta link clicks versus Shopify landing page views.", bold_prefix="Exhibit F: ")

    # Appendix B
    add_h1("Appendix B: Definitions")
    add_bullet("Shopify gross sales divided by total Google and Meta spend for the month.", bold_prefix="Gross ÷ spend: ")
    add_bullet("orders attributed by Google and Meta, and spend divided by those orders. Attribution windows overlap, so these are not additive to Shopify orders.", bold_prefix="Paid orders and paid CPA: ")
    add_bullet("total ad spend divided by total Shopify orders.", bold_prefix="Spend per order: ")
    add_bullet("1 – 18 November 2026 (18 days), extrapolated to 30 days for the reference run-rate only.", bold_prefix="November to date: ")

    os.makedirs(os.path.dirname(output_docx_path), exist_ok=True)
    doc.save(output_docx_path)
    print(f"Successfully generated DOCX at: {output_docx_path}")

if __name__ == "__main__":
    report_docx = r"C:\Users\test\Videos\Office\reports\FABB6_Final_Performance_Audit_Strategy_and_Forecast_Report.docx"
    case_study_docx = r"C:\Users\test\Videos\Office\case-studies\fabb6\FABB6_Final_Performance_Audit_Strategy_and_Forecast_Report.docx"
    artifact_docx = r"C:\Users\test\.gemini\antigravity\brain\29f77e0a-5ed5-4d24-842c-443d9957274c\FABB6_Final_Performance_Audit_Strategy_and_Forecast_Report.docx"
    
    build_docx_report(report_docx)
    shutil.copyfile(report_docx, case_study_docx)
    shutil.copyfile(report_docx, artifact_docx)
    print("All DOCX files successfully synchronized.")
