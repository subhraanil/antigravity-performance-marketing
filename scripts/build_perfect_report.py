import win32com.client
import pythoncom
import pypdf
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

def set_cell_margins(cell, top=35, bottom=35, left=45, right=45):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def create_styled_table(doc, data, header_bg="102C57", zebra=True, center_cols=[], right_cols=[], col_widths=None):
    table = doc.add_table(rows=len(data), cols=len(data[0]))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    header_tr = table.rows[0]._tr.get_or_add_trPr()
    header_tr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
    
    for r_idx, row_vals in enumerate(data):
        row = table.rows[r_idx]
        trPr = row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        is_header = (r_idx == 0)
        is_total = (r_idx == len(data) - 1 and any(k in str(row_vals[0]) for k in ["Total", "Upper bound", "Plan 3"]))
        
        for c_idx, val in enumerate(row_vals):
            cell = row.cells[c_idx]
            cell.text = str(val)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(1.5)
            p.paragraph_format.space_after = Pt(1.5)
            p.paragraph_format.line_spacing = 1.02
            
            if c_idx in center_cols:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            elif c_idx in right_cols:
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            else:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                
            for run in p.runs:
                run.font.name = "Calibri"
                if is_header:
                    run.font.size = Pt(7.5)
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(255, 255, 255)
                elif is_total and "Total" in str(row_vals[0]):
                    run.font.size = Pt(7.5)
                    run.font.bold = True
                    run.font.color.rgb = RGBColor(16, 44, 87)
                else:
                    run.font.size = Pt(7.0)
                    run.font.color.rgb = RGBColor(30, 30, 30)
                    
            if is_header:
                set_cell_background(cell, header_bg)
            elif is_total and "Total" in str(row_vals[0]):
                set_cell_background(cell, "EAECEE")
            else:
                if zebra and r_idx % 2 == 1:
                    set_cell_background(cell, "F9FAFB")
            set_cell_margins(cell, top=30, bottom=30, left=40, right=40)

    if col_widths:
        for row in table.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Inches(width)

    return table

def build_perfect_report(docx_path):
    doc = docx.Document()
    
    for s in doc.sections:
        s.top_margin = Inches(0.65)
        s.bottom_margin = Inches(0.65)
        s.left_margin = Inches(0.65)
        s.right_margin = Inches(0.65)
        
        header = s.header
        hp = header.paragraphs[0]
        hp.text = "FABB6 Performance Audit, Turnaround Plan & Dec 2026 – Feb 2027 Forecast"
        hp.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in hp.runs:
            run.font.name = "Calibri"
            run.font.size = Pt(7.5)
            run.font.color.rgb = RGBColor(128, 128, 128)

    def add_h1(text, page_break_before=False):
        if page_break_before:
            doc.add_page_break()
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(2.0)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.name = "Georgia"
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = RGBColor(16, 44, 87)
        return h

    def add_h2(text, page_break_before=False):
        if page_break_before:
            doc.add_page_break()
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(5)
        h.paragraph_format.space_after = Pt(1.5)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(9.2)
        r.font.bold = True
        r.font.color.rgb = RGBColor(31, 78, 120)
        return h

    def add_body(text, bold_prefix=""):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2.5)
        p.paragraph_format.line_spacing = 1.08
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = "Calibri"
            rb.font.size = Pt(8.4)
            rb.font.bold = True
            rb.font.color.rgb = RGBColor(30, 30, 30)
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(8.4)
        r.font.color.rgb = RGBColor(40, 40, 40)
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0.5)
        p.paragraph_format.space_after = Pt(1.8)
        p.paragraph_format.line_spacing = 1.08
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.font.name = "Calibri"
            rb.font.size = Pt(8.4)
            rb.font.bold = True
            rb.font.color.rgb = RGBColor(30, 30, 30)
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(8.4)
        r.font.color.rgb = RGBColor(40, 40, 40)
        return p

    # ==================== PAGE 1 ====================
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    run_t = p_title.add_run("FABB6 Performance Audit, Turnaround Plan\n& Dec 2026 – Feb 2027 Forecast")
    run_t.font.name = "Georgia"
    run_t.font.size = Pt(18)
    run_t.font.bold = True
    run_t.font.color.rgb = RGBColor(26, 36, 43)

    p_byline1 = doc.add_paragraph()
    p_byline1.paragraph_format.space_before = Pt(0)
    p_byline1.paragraph_format.space_after = Pt(2)
    r_b1 = p_byline1.add_run("Techno Exponent | Performance Marketing & Enterprise Growth Practice")
    r_b1.font.name = "Calibri"
    r_b1.font.size = Pt(9.0)
    r_b1.font.bold = True
    r_b1.font.color.rgb = RGBColor(70, 70, 70)

    p_byline2 = doc.add_paragraph()
    p_byline2.paragraph_format.space_before = Pt(0)
    p_byline2.paragraph_format.space_after = Pt(8)
    r_b2 = p_byline2.add_run("Prepared for FABB6 (Glanzzkart Private Limited) · Data through 18 November 2026 · Confidential")
    r_b2.font.name = "Calibri"
    r_b2.font.size = Pt(8.0)
    r_b2.font.color.rgb = RGBColor(100, 100, 100)

    add_h1("1. Executive Summary")
    add_body("This report reviews Google Ads and Meta Ads performance from December 2025 to 18 November 2026, audits the account state we inherited from the interim agency (SilverXis, September to November 2026), and sets out a stabilization plan and a forecast for December 2026 to February 2027.")

    add_h2("What the numbers say")
    add_bullet("In August 2026, FABB6 recorded ₹95.80 Lakhs of Gross Sales and ₹74.76 Lakhs of Total Sales Revenue across 11,069 orders on ₹47.91 Lakhs of ad spend (2.00x Gross ROAS / 1.56x Net ROAS).")
    add_bullet("Between 1 September and 18 November 2026, ad spend was ₹67.83 Lakhs (Google ₹34.84L, Meta ₹32.99L) against Total Sales Revenue of ₹1.61 Cr and Gross Sales of ₹1.97 Cr.")
    add_bullet("October Gross ROAS (2.49x) was in line with June–July (2.51x–2.37x) and well above August (2.00x), while November to date (2.79x) reflects early festive uplift driven by stronger order values (October gross AOV was ₹1,156; November gross run-rate is ₹1,147).")
    add_bullet("The most serious disruption occurred in September: ad spend fell 87% against August (to ₹6.27L) and Shopify orders fell 72% to 3,112. Cause under review; change logs show campaign delivery reductions alongside the September 18 tracking deletion.")

    add_h2("What the audit found")
    add_body("The problems are in account hygiene, tracking and structure rather than in a collapse of headline efficiency. Each is documented in the change history and exports (Exhibits A–G):")
    add_bullet("The primary Google purchase conversion action ('Purchase-2026') was deleted on 18 September.")
    add_bullet("Live Performance Max asset groups contained copy referencing another brand.")
    add_bullet("110 products pointed to unavailable (404) pages in Merchant Center.")
    add_bullet("Meta retargeting (DPA) ran more expensively than cold prospecting, three Advantage+ Shopping campaigns ran concurrently, and about ₹1.5 Lakhs was spent on campaigns with zero orders.")
    add_body(" between ₹1.50 Lakhs (spend with zero orders, provable) and ₹7.47 Lakhs (total spend in the affected campaigns, upper bound). Our central estimate of excess spend is about ₹5.87 Lakhs (Section 5).", bold_prefix="Quantified waste:")
    add_body(" The Recommended Plan paces media spend from ₹30.00L in December to ₹35.00L in January and ₹40.00L in February, delivering confirmed Gross Sales of ₹93.06L (3.10x ROAS), ₹121.25L (3.46x ROAS), and ₹164.42L (4.11x ROAS) across 9,178, 10,992, and 13,346 monthly store orders. The plan is powered by front-end paid acquisition (6,082, 7,680, and 9,801 monthly orders) and low-cost retention flows (3,096, 3,313, and 3,545 monthly orders) driven by GoKwik and automated WhatsApp/email replenishment workflows at zero incremental media spend. Flanked by a Moderate Plan (Dec ₹35L, Jan ₹41L, Feb ₹47L) and an Aggressive Plan (Dec ₹40L, Jan ₹48L, Feb ₹55L).", bold_prefix="Forecast (Dec 2026 – Feb 2027):")

    # ==================== PAGE 2 ====================
    add_h1("2. Twelve-Month Performance Reconciliation", page_break_before=True)
    add_body("August 2026 Google Ads spend had been overstated in earlier raw exports (₹67.07 Lakhs, caused by a reporting glitch). The reconciled figure is ₹32.23 Lakhs. All figures below use reconciled data, showing both Shopify Confirmed Gross Sales and Total Sales Revenue (Net recognized sales) side-by-side.")

    hist_table_data = [
        ["Month", "Total spend", "Paid orders", "Shopify orders", "Gross Sales", "Gross ROAS", "Total Sales (Net)", "Net ROAS"],
        ["Dec 2025", "₹4.21L", "1,614", "3,307", "₹26.45L", "6.28x", "₹20.72L", "4.92x"],
        ["Jan 2026", "₹12.17L", "4,260", "7,850", "₹56.34L", "4.63x", "₹46.40L", "3.81x"],
        ["Feb 2026", "₹17.97L", "4,817", "8,250", "₹75.52L", "4.20x", "₹62.38L", "3.47x"],
        ["Mar 2026", "₹27.84L", "6,351", "11,285", "₹85.24L", "3.06x", "₹59.57L", "2.14x"],
        ["Apr 2026", "₹32.55L", "5,350", "10,551", "₹98.45L", "3.02x", "₹74.37L", "2.28x"],
        ["May 2026", "₹40.21L", "7,076", "12,215", "₹115.20L", "2.87x", "₹91.33L", "2.27x"],
        ["Jun 2026", "₹42.86L", "6,851", "12,877", "₹107.50L", "2.51x", "₹83.98L", "1.96x"],
        ["Jul 2026", "₹43.62L", "8,313", "13,420", "₹103.20L", "2.37x", "₹78.45L", "1.80x"],
        ["Aug 2026", "₹47.91L", "10,965", "11,069", "₹95.80L", "2.00x", "₹74.76L", "1.56x"],
        ["Sep 2026 (Interim)", "₹6.27L", "801", "3,112", "₹38.50L", "6.14x", "₹28.50L", "4.54x"],
        ["Oct 2026 (Interim)", "₹42.47L", "7,298", "9,143", "₹105.70L", "2.49x", "₹90.99L", "2.14x"],
        ["Nov 2026 (to 18th)", "₹19.09L", "4,316", "4,638", "₹53.18L", "2.79x", "₹42.00L", "2.20x"],
    ]
    create_styled_table(doc, hist_table_data, header_bg="102C57", center_cols=[2, 3, 5, 7], right_cols=[1, 4, 6])
    add_body("Gross Sales represents Shopify confirmed orders. Total Sales Revenue represents actual net recognized store revenue from Shopify (after discounts and returns, including taxes and shipping). Net sales averaged ~80% of gross sales across the full 12-month period (79% Jun–Nov, 78% Dec–Nov; 83.7% in Oct–Nov festive period).")

    add_h2("Three observations that shape the plan")
    add_bullet("From Dec 2025 to Aug 2026, spend grew tenfold and Gross ROAS adjusted from 6.28x to 2.00x (Net ROAS 4.92x to 1.56x). Some decline is the normal cost of scaling into colder audiences; we treat 2.0x–2.8x Gross ROAS (1.7x–2.3x Net ROAS) as the realistic operating baseline for ₹25–45 Lakhs of monthly spend.", bold_prefix="1. Efficiency adjusted as spend scaled: ")
    add_bullet("Spend was cut by 87% in September (cause under review; change logs show campaign delivery reductions alongside the September 18 tracking deletion), so the ratio reflects organic and repeat demand that continued without paid support.", bold_prefix="2. September's 6.14x Gross / 4.54x Net is not an efficiency gain: ")
    add_bullet("October Gross ROAS (2.49x) was in line with June–July (2.51x–2.37x) and well above August (2.00x), while November to date (2.79x) reflects early festive uplift driven by stronger order values (October gross AOV was ₹1,156; November gross run-rate is ₹1,147).", bold_prefix="3. October CPA was not a record: ")
    add_body("The Festival of Lights (Diwali) fell on 8 November in 2026, so the festive demand window straddles October and November. The November run-rate therefore includes festive uplift and is not used as an unadjusted December baseline.")

    # ==================== PAGE 3 ====================
    add_h1("3. Google Ads Audit & Merchant Center Automation", page_break_before=True)
    add_body("Google Ads spend during the interim period totaled ₹34.84 Lakhs. Findings from the change history, asset group, product and search term reports:")
    add_bullet("The change history shows the 'Purchase-2026' conversion action was deleted by an administrator account on the SilverXis side (Exhibit A). Smart Bidding lost its main learning signal. September Google spend was ₹3.18 Lakhs for 42 attributed orders (₹7,569 CPA). Because 17 days of the month preceded the deletion and post-deletion sales may be unattributed, the true cost per sale is likely lower than this figure, and we will validate it against Shopify UTM data.", bold_prefix="1. Primary purchase conversion deleted (18 Sep): ")
    add_bullet("Several asset groups (T4 Pro/Salon, T3 Premium, Pilgrim, YS24) contained headlines and descriptions promoting a different brand name (Exhibit B). All were rated 'Poor' for Ad Strength.", bold_prefix="2. Another brand's copy in live Performance Max asset groups: ")
    add_bullet("Merchant Center shows 216 ineligible products: 110 with 'page unavailable' (404) and 70 with promotional overlay violations. At least ₹80,285 was spent on affected products with zero conversions (for example, one serum SKU spent ₹1,614 on 480 clicks into a 404 page). Active products must have URLs repaired in the Shopify feed.", bold_prefix="3. 110 broken product pages: ")
    add_bullet("Daily budgets were changed 140 times in under 60 days (74 increases, 66 decreases). Constant changes make Smart Bidding performance harder to read and slower to stabilize.", bold_prefix="4. Frequent budget changes: ")
    add_bullet("A campaign named 'Search-Brand' used broad match and triggered queries unrelated to beauty (for example, gym equipment and a badminton ankle support). The spend on these queries is not yet quantified; it will be after a full search terms export.", bold_prefix="5. Off-category search queries: ")
    add_bullet("Official Merchant Center performance exports (Sep 1 – Nov 19) across 3,411 SKUs show 6.14 Crore impressions and 6,29,968 clicks. The 48.77 tracked purchases reflect an unlinked free/organic listing tracking artifact currently under technical review, whereas Google Ads and Meta recorded 7,298 conversions in October and Shopify confirmed 9,143 store orders. Crucially, 10 of the top 15 SKUs by clicks are high_28plus hero products (e.g. Floractive Nanoplastia ₹5,500, Loreal Absolut Repair). They must NOT be blanket-excluded. Exclusions are strictly restricted to negative unit margin items (standalone ₹69 single sachets where ~₹45 shipping exceeds ₹37 gross margin) and EXCLUDE_lowmargin (<15%) tags (Exhibit G).", bold_prefix="6. Merchant Center catalog distribution & high-click SKU forensics: ")

    gmc_table_data = [
        ["Top High-Volume Catalog SKU", "Price / Tier", "Margin Class", "Impressions", "Clicks", "Forensic Routing"],
        ["Raaga Professional De-Tan Cream single use", "₹69 (T1 Entry)", "mid_20_28", "1,261,144", "27,648", "Negative Unit Margin (Exclude)"],
        ["DOT & KEY Strawberry Dew Tinted Sunscreen 50ml", "₹549 (T2 Core)", "mid_20_28", "669,332", "17,485", "Core Volume (Route to mid_20_28)"],
        ["Loreal Paris Hair Spa Deep Nourish 490g", "₹650 (T2 Core)", "mid_20_28", "766,242", "13,249", "Core Volume (Route to mid_20_28)"],
        ["Matrix Mega Smooth Masque 500g", "₹750 (T2 Core)", "mid_20_28", "810,808", "9,192", "Core Volume (Route to mid_20_28)"],
        ["Loreal Majirel 3.0 Combo + Developer 1000ml", "₹755 (T2 Core)", "high_28plus", "673,069", "9,142", "Hero SKU (Route to high_28plus)"],
        ["Floractive Professional W One Nanoplastia 1000ml", "₹5,500 (T4 Pro)", "high_28plus", "1,357,589", "6,921", "Hero SKU (Route to T4 Pro/Salon)"],
        ["Total Top 6 Analyzed Catalog SKUs", "—", "—", "5,538,184", "83,637", "Dedicated Campaign Segmentation"]
    ]
    create_styled_table(doc, gmc_table_data, header_bg="102C57", center_cols=[1, 2], right_cols=[3, 4])
    add_body("Tool Solution: Deploy Simprosys Google Shopping Feed (Shopify app, ~$20/mo) to automate real-time inventory sync via Shopify webhooks to Google Content API, halting ads on out-of-stock items within minutes and automatically suppressing 404 broken URLs.")

    # ==================== PAGE 4 ====================
    add_h1("4. Meta Ads Audit & 5. Avoidable Spend", page_break_before=True)
    add_body("Meta spend during the interim period totaled ₹32.99 Lakhs.")
    add_bullet("'Retargeting — DPA - Fabb6' spent ₹9.50 Lakhs for 1,850 purchases at ₹513.70 CPA (peaking at ₹570.31 in October), against ₹479.53 for cold prospecting, with frequency of 3.21 and no past-purchaser exclusions. Excess cost against the cold-prospecting CPA is about ₹63,000.", bold_prefix="1. Retargeting more expensive than prospecting: ")
    add_bullet("Three Advantage+ Shopping campaigns ran at the same time without product exclusions, so they competed in the same auctions. Account CPM rose from ₹56.15 in August to ₹104.17 in October (+85%) and ₹137.03 in November (+144%). Consolidation to one master Advantage+ campaign will eliminate auction overlap.", bold_prefix="2. Overlapping Advantage+ Shopping campaigns: ")
    add_bullet("₹50,214 across 8.32 million impressions produced 1,02,322 link clicks, 28 landing page views and 0 purchases (99.97% drop-off between click and page view).", bold_prefix="3. 'IG-Traffic' link-click campaign: ")
    add_bullet("The iOS campaign spent ₹19,161 at frequency 13.18 with 0 sales. The Android campaign spent about ₹1.38 Lakhs at ₹1,082 CPA.", bold_prefix="4. App install campaigns: ")
    add_bullet("Meta reported 7,34,064 link clicks but only 3,01,798 landing page views on Shopify: a 58.9% gap (52.2% excluding IG-Traffic). Likely causes are mobile page speed, accidental clicks, and pixel or Conversions API (CAPI) misfires. We will diagnose these in the first two weeks.", bold_prefix="5. Click-to-landing-page gap: ")

    add_h1("5. Avoidable Spend: A Range, Not a Single Number")
    waste_table_data = [
        ["Measure", "Amount", "Basis"],
        ["Provable floor: spend with zero orders", "₹1,49,660", "404 products (₹80,285), IG-Traffic (₹50,214), iOS app campaign (₹19,161)"],
        ["Central estimate: excess spend versus benchmark CPA", "about ₹5.87 Lakhs", "Floor, plus Google September excess against the August Google CPA of ₹480 (₹2.98L), Android app excess (about ₹0.77L), DPA excess against cold CPA (about ₹0.63L)"],
        ["Upper bound: total spend in affected campaigns", "₹7,46,558", "Google September ₹3,17,895; 404 products ₹80,285; IG-Traffic ₹50,214; app campaigns ₹1,57,302; DPA ₹1,40,862"]
    ]
    create_styled_table(doc, waste_table_data, header_bg="102C57", center_cols=[1], right_cols=[])
    add_body("The upper bound counts all spend in affected campaigns, including spend that did produce some orders, and should not be read as pure loss. The Google September figure may include sales that went unattributed after the conversion action was deleted.")

    # ==================== PAGE 5 ====================
    add_h1("6. Turnaround Plan", page_break_before=True)
    add_body("Admin access has been verified across Google Ads, Meta Business Suite, Google Merchant Center and Shopify. Shopify is the source of truth for revenue and orders throughout.")

    add_h2("Phase 1: Immediate triage (hours 0 – 48)")
    add_bullet("Pause 'IG-Traffic' and the iOS and Android app install campaigns.")
    add_bullet("Deploy Simprosys Google Shopping Feed app to instantly eliminate 404 broken URLs and stop ad spend on 0-stock products.")
    add_bullet("Exclude negative unit margin SKUs (standalone ₹69 single-use sachets) and EXCLUDE_lowmargin (<15%) tags via automated feed custom labels.")
    add_bullet("Remove foreign-brand copy from all Performance Max asset groups.")
    add_bullet("Confirm a single primary Purchase conversion action is active in Google Ads and matches Shopify order counts. Verify Enhanced Conversions, and test Meta CAPI deduplication.")

    add_h2("Phase 2: Restructure and stabilize (December 2026)")
    add_bullet("Segment Google into High Margin Heroes (60% budget), Core Volume (20%), Category Search (13%), and Brand Search (7%).")
    add_bullet("Consolidate Meta into one master Advantage+ Shopping campaign (70% budget) with a 15% existing-customer budget cap.")
    add_bullet("Add 30-day and 180-day purchaser exclusions to DPA (15% budget), with frequency capped at 2.2 or below.")
    add_bullet("Deploy GoKwik (https://www.gokwik.co/) on Shopify for 1-click checkout, automated abandoned cart recovery, and COD RTO risk reduction, alongside automated WhatsApp (Interakt/Wati) and email replenishment workflows timed to 30, 45, and 60 days (~₹35k–₹50k/mo software cost, zero incremental media spend).", bold_prefix="Checkout & Retention Engine: ")

    add_h2("Phase 3: Profitable scaling (January – February 2027)")
    add_bullet("Increase budgets by no more than 20% every 72 hours per campaign.")
    add_bullet("Expand high-intent non-brand Google search for hero categories (serums, brightening, anti-aging).")
    add_bullet("Scale automated replenishment CRM flows to capture high-margin repeat replenishment revenue.")
    add_body("scale a step only if trailing 7-day confirmed Gross ROAS is at least 2.50x and CPA is within target. Hold spend between 2.30x and 2.50x. Roll back the last increase if Gross ROAS stays below 2.30x for 7 consecutive days. All planned budget expansions in Section 7 are strictly conditional on maintaining this performance threshold.", bold_prefix="Scaling decision rule: ")

    # ==================== PAGE 6 ====================
    add_h1("7. Forecast: December 2026 – February 2027", page_break_before=True)
    add_h2("7.1 Approach")
    add_body("The forecast is built on the client's official target financial model, flanking it with a conservative Base Plan and an Aggressive Plan. Planned spend follows the official model: ₹30.00L in December, ₹35.00L in January, and ₹40.00L in February. Performance is powered by dual revenue engines: front-end paid acquisition (6,082, 7,680, and 9,801 monthly orders) and zero-incremental-media-cost retention flows (3,096, 3,313, and 3,545 monthly orders from others), driving monthly Store ROAS from 3.10x to 3.46x and 4.11x.")

    add_h2("7.2 Master Turnaround Forecast (Recommended Plan)")
    base_table_data = [
        ["Month", "Total Ad Spend", "Google Spend", "Meta Spend", "Paid Orders", "Orders from Others*", "Total Store Orders", "Gross Sales Revenue", "Spend / Store Order", "Confirmed Gross ROAS"],
        ["Dec 2026", "₹30.00L", "₹19.00L", "₹11.00L", "6,082", "3,096", "9,178", "₹93.06L", "₹326.87", "3.10x"],
        ["Jan 2027", "₹35.00L", "₹22.00L", "₹13.00L", "7,680", "3,313", "10,992", "₹121.25L (~₹1.21 Cr)", "₹318.40", "3.46x"],
        ["Feb 2027", "₹40.00L", "₹25.00L", "₹15.00L", "9,801", "3,545", "13,346", "₹164.42L (~₹1.64 Cr)", "₹299.72", "4.11x"]
    ]
    create_styled_table(doc, base_table_data, header_bg="102C57", center_cols=[1, 2, 3, 4, 5, 6, 8, 9], right_cols=[7])
    add_body("Spend per total store order improves from ₹326.87 in Dec to ₹318.40 in Jan and ₹299.72 in Feb. With 25% wholesale gross margin on ex-GST product value, media break-even is 4.00x on ex-GST revenue, or 4.72x on GST-inclusive total receipts / Shopify Gross Sales. Repeat replenishment workflows drive 3,096 to 3,545 monthly store orders at zero incremental media spend.")

    # ==================== PAGE 7 ====================
    add_h2("7.3 Three Strategic Performance Scenarios (Month-by-Month Schedules)", page_break_before=True)
    col_w_8_rep = [0.9, 1.0, 1.3, 0.75, 0.65, 0.75, 1.15, 0.7]
    p1_headers = ["Month", "Ad Budget", "Google / Meta Split", "Paid Orders", "Others*", "Store Orders", "Gross Sales", "Store ROAS"]
    
    add_body("Plan 1: Recommended Plan (Official Client Target Turnaround Model)", bold_prefix="")
    p1_data = [p1_headers,
        ["Dec 2026", "₹30.00L", "₹19.00L / ₹11.00L", "6,082", "3,096", "9,178", "₹93.06L", "3.10x"],
        ["Jan 2027", "₹35.00L", "₹22.00L / ₹13.00L", "7,680", "3,313", "10,992", "₹121.25L", "3.46x"],
        ["Feb 2027", "₹40.00L", "₹25.00L / ₹15.00L", "9,801", "3,545", "13,346", "₹164.42L", "4.11x"]]
    create_styled_table(doc, p1_data, header_bg="102C57", center_cols=[0, 1, 2, 3, 4, 5, 7], right_cols=[6], col_widths=col_w_8_rep)

    add_body("Plan 2: Moderate Plan (Accelerated Scale Scenario)", bold_prefix="")
    p2_data = [p1_headers,
        ["Dec 2026", "₹35.00L", "₹22.00L / ₹13.00L", "6,950", "3,096", "10,046", "₹103.50L", "2.96x"],
        ["Jan 2027", "₹41.00L", "₹26.00L / ₹15.00L", "8,800", "3,313", "12,113", "₹136.50L", "3.33x"],
        ["Feb 2027", "₹47.00L", "₹29.50L / ₹17.50L", "11,250", "3,545", "14,795", "₹184.20L", "3.92x"]]
    create_styled_table(doc, p2_data, header_bg="1F4E78", center_cols=[0, 1, 2, 3, 4, 5, 7], right_cols=[6], col_widths=col_w_8_rep)

    add_body("Plan 3: Aggressive Plan (High Scale / Market Dominance Scenario)", bold_prefix="")
    p3_data = [p1_headers,
        ["Dec 2026", "₹40.00L", "₹25.00L / ₹15.00L", "7,750", "3,096", "10,846", "₹113.20L", "2.83x"],
        ["Jan 2027", "₹48.00L", "₹30.50L / ₹17.50L", "10,050", "3,313", "13,363", "₹151.20L", "3.15x"],
        ["Feb 2027", "₹55.00L", "₹34.50L / ₹20.50L", "12,850", "3,545", "16,395", "₹204.50L", "3.72x"]]
    create_styled_table(doc, p3_data, header_bg="203764", center_cols=[0, 1, 2, 3, 4, 5, 7], right_cols=[6], col_widths=col_w_8_rep)

    add_h2("7.4 Channel-level guardrails (platform-attributed)")
    chan_table_data = [
        ["Month", "Google Spend (63%)", "Google CPA Target", "Google Orders", "Meta Spend (37%)", "Meta CPA Target", "Meta Orders", "Combined Paid Orders"],
        ["Dec 2026", "₹19.00L (63.3%)", "₹480.00", "3,958", "₹11.00L (36.7%)", "₹518.00", "2,124", "6,082"],
        ["Jan 2027", "₹22.00L (62.9%)", "₹451.00", "4,878", "₹13.00L (37.1%)", "₹464.00", "2,802", "7,680"],
        ["Feb 2027", "₹25.00L (62.5%)", "₹407.00", "6,143", "₹15.00L (37.5%)", "₹410.00", "3,659", "9,801"]
    ]
    create_styled_table(doc, chan_table_data, header_bg="102C57", center_cols=[1, 2, 3, 4, 5, 6, 7], right_cols=[])
    add_body("Paid orders represent 66% to 73% of monthly store orders. Paid CPA improves monthly in Google (₹480 → ₹407) and Meta (₹518 → ₹410). Three distinct CPA metrics govern execution: (1) Spend per Store Order (Blended CPA, ₹299–₹327): Primary business KPI; (2) Platform Paid CPA (Google ₹407–₹480, Meta ₹410–₹518): Operational check; (3) Bidding CPA Ceilings: Algorithm caps.")

    # ==================== PAGE 8 ====================
    add_h2("7.5 Key assumptions and risks", page_break_before=True)
    add_bullet("Shopify Confirmed Gross Sales serves as the primary forecast and scaling governance basis.")
    add_bullet("Repeat retention and checkout optimization are powered by GoKwik (https://www.gokwik.co/) for abandoned cart remarketing and automated WhatsApp/email notification subscriptions (30, 45, 60 days) at ~₹35k–₹50k/month operational cost with zero incremental media spend.")
    add_bullet("Orders from Others compounds at +7% monthly in Recommended Plan (3,096 in Dec, 3,313 in Jan, 3,545 in Feb), representing repeat buyers and organic traffic.")
    add_bullet("Break-even ROAS is 4.00x on wholesale ex-GST revenue (25% margin), and 4.72x on GST-inclusive total receipts / Shopify Gross Sales (accounting for 18% GST).")
    add_bullet("Scaling Decision Gates: Scale only if trailing 7-day Gross ROAS is ≥ 2.50x. Hold spend between 2.30x and 2.50x. Roll back if < 2.30x for 7 consecutive days.")

    add_h1("8. Operating Guardrails")
    add_bullet("New campaigns, ad sets and creatives are created paused and go live only after tracking, UTM parameters and margin review are confirmed.", bold_prefix="1. Paused-first creation: ")
    add_bullet("Increases are capped at 20% every 72 hours per campaign.", bold_prefix="2. Budget pacing: ")
    add_bullet("Prospecting campaigns exclude 30-day purchasers and customer lists. Retargeting excludes purchasers.", bold_prefix="3. Audience hygiene: ")
    add_bullet("Automated real-time scans via Simprosys Google Shopping Feed immediately suppress products with dead URLs or zero inventory.", bold_prefix="4. Daily feed checks: ")
    add_bullet("A daily pacing update by WhatsApp or Slack, a weekly performance review, and a monthly reconciliation against Shopify net revenue.", bold_prefix="5. Reporting cadence: ")

    # ==================== PAGE 9 ====================
    add_h1("Appendix A: Evidence Exhibits to Attach", page_break_before=True)
    add_bullet("Google Ads change history showing deletion of 'Purchase-2026' (18 Sep).", bold_prefix="Exhibit A: ")
    add_bullet("Performance Max asset group report showing foreign-brand copy and Ad Strength ratings.", bold_prefix="Exhibit B: ")
    add_bullet("Merchant Center product diagnostics (404 and overlay violations).", bold_prefix="Exhibit C: ")
    add_bullet("Google Ads budget change log and search terms report.", bold_prefix="Exhibit D: ")
    add_bullet("Meta campaign exports (DPA, Advantage+ Shopping, IG-Traffic, app campaigns), with CPM and frequency by month.", bold_prefix="Exhibit E: ")
    add_bullet("Meta link clicks versus Shopify landing page views.", bold_prefix="Exhibit F: ")
    add_bullet("Google Merchant Center product performance export (Sep 1 – Nov 19, 2026) and catalog audit showing click concentration across high-volume heroes and low-ticket single units.", bold_prefix="Exhibit G: ")

    add_h1("Appendix B: Definitions")
    add_bullet("Confirmed orders from Shopify before deductions. Primary planning and weekly performance gating metric.", bold_prefix="Shopify Confirmed Gross Sales: ")
    add_bullet("Actual net recognized sales revenue from Shopify (after discounts and returns, including taxes and shipping). Averages ~80% of gross sales across baseline.", bold_prefix="Total Sales Revenue (Net): ")
    add_bullet("Shopify Confirmed Gross Sales divided by total ad spend. Account targets: 3.46x Dec, 3.79x Jan, 4.35x Feb (3.91x Q1 blended).", bold_prefix="Confirmed Gross ROAS: ")
    add_bullet("Total ad spend divided by total Shopify store orders (₹293 Dec, ₹291 Jan, ₹283 Feb; Q1 avg ₹288.53). Primary governing business unit metric.", bold_prefix="Spend per Store Order (Blended CPA): ")
    add_bullet("Ad-attributed orders and platform-specific acquisition cost. Target improves by 4% monthly (Google ₹450 → ₹410, Meta ₹450 → ₹385).", bold_prefix="Paid orders and platform CPA: ")
    add_bullet("1 – 18 November 2026 (18 days), extrapolated to 30 days for reference run-rate comparison.", bold_prefix="November to date: ")

    os.makedirs(os.path.dirname(docx_path), exist_ok=True)
    doc.save(docx_path)
    print(f"Successfully generated perfect DOCX at: {docx_path}")

def convert_docx_to_pdf(docx_path, pdf_path):
    pythoncom.CoInitialize()
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    try:
        doc = word.Documents.Open(os.path.abspath(docx_path))
        doc.SaveAs(os.path.abspath(pdf_path), FileFormat=17)
        doc.Close()
        print(f"Successfully converted DOCX to PDF at: {pdf_path}")
    finally:
        word.Quit()
        pythoncom.CoUninitialize()

if __name__ == "__main__":
    report_docx = r"C:\Users\test\Videos\Office\reports\FABB6_Final_Performance_Audit_Strategy_and_Forecast_Report.docx"
    case_study_docx = r"C:\Users\test\Videos\Office\case-studies\fabb6\FABB6_Final_Performance_Audit_Strategy_and_Forecast_Report.docx"
    artifact_docx = r"C:\Users\test\.gemini\antigravity\brain\29f77e0a-5ed5-4d24-842c-443d9957274c\FABB6_Final_Performance_Audit_Strategy_and_Forecast_Report.docx"
    
    report_pdf = r"C:\Users\test\Videos\Office\reports\FABB6_Final_Performance_Audit_Strategy_and_Forecast_Report.pdf"
    case_study_pdf = r"C:\Users\test\Videos\Office\case-studies\fabb6\FABB6_Final_Performance_Audit_Strategy_and_Forecast_Report.pdf"
    artifact_pdf = r"C:\Users\test\.gemini\antigravity\brain\29f77e0a-5ed5-4d24-842c-443d9957274c\FABB6_Final_Performance_Audit_Strategy_and_Forecast_Report.pdf"
    
    build_perfect_report(report_docx)
    shutil.copyfile(report_docx, case_study_docx)
    shutil.copyfile(report_docx, artifact_docx)
    print("All DOCX files successfully synchronized.")
    
    convert_docx_to_pdf(report_docx, report_pdf)
    shutil.copyfile(report_pdf, case_study_pdf)
    shutil.copyfile(report_pdf, artifact_pdf)
    print("All PDF files successfully generated and synchronized.")
