import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import win32com.client
import pythoncom
import pypdf
import os

doc = docx.Document()
for s in doc.sections:
    s.top_margin = Inches(0.48)
    s.bottom_margin = Inches(0.48)
    s.left_margin = Inches(0.58)
    s.right_margin = Inches(0.58)

def add_h1(text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(3.0)
    h.paragraph_format.space_after = Pt(1.5)
    r = h.add_run(text)
    r.font.name = 'Georgia'
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(16, 44, 87)
    return h

def add_h2(text):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(2.5)
    h.paragraph_format.space_after = Pt(1.0)
    r = h.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(8.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(31, 78, 120)
    return h

def add_body(text, bold_prefix='', space_after=1.0, font_size=6.8):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.02
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.name = 'Calibri'
        rb.font.size = Pt(font_size)
        rb.font.bold = True
        rb.font.color.rgb = RGBColor(20, 20, 20)
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(font_size)
    r.font.color.rgb = RGBColor(40, 40, 40)
    return p

def add_bullet(text, bold_prefix='', space_after=1.0, font_size=6.7):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.02
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.name = 'Calibri'
        rb.font.size = Pt(font_size)
        rb.font.bold = True
        rb.font.color.rgb = RGBColor(20, 20, 20)
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(font_size)
    r.font.color.rgb = RGBColor(40, 40, 40)
    return p

# Page 7 content
add_h2('Three observations that shape the plan')
add_bullet("From December 2025 to August 2026, spend grew more than tenfold and Gross Store ROAS adjusted from 7.01x to 2.32x. Some decline is the normal cost of scaling into colder audiences, and we treat 2.5x–3.5x as the realistic operating baseline for ₹30–45 Lakhs of monthly spend.", bold_prefix="• 1. Efficiency adjusted as spend scaled: ")
add_bullet("Spend was cut by 87% due to campaign pauses and verification delays, so the 6.61x ratio reflects natural organic and repeat demand that continued without ad spend; it did not represent genuine operational efficiency.", bold_prefix="• 2. September was not an efficiency gain: ")
add_bullet("April (₹608) and June (₹626) were higher. October ROAS (2.85x) and November (3.82x) were well above August (2.32x), driven by strong order values (₹1,320+ AOV).", bold_prefix="• 3. October CPA was not a record: ")
add_body("The Festival of Lights (Diwali) fell on 8 November in 2026, so festive demand straddles October and November. The November run-rate includes festive uplift and is not used as an unadjusted December baseline.")

add_h1('6.3 Google Ads Audit')
add_body("Google Ads spend during the audit period (1 September – 18 November 2026) totaled ₹34.84 Lakhs. Findings from the change history, asset group, product and search term reports:")
add_bullet("The change history shows the 'Purchase-2026' conversion action was deleted by an administrator account (Exhibit A). Smart Bidding lost its main learning signal. September Google spend was ₹3.18 Lakhs for 42 attributed orders (₹7,569 CPA). Because 17 days of the month preceded the deletion and post-deletion sales may be unattributed, the true cost per sale is likely lower than this figure, and we will validate it against Shopify UTM data.", bold_prefix="• 1. Primary purchase conversion deleted (18 Sep): ")
add_bullet("Several asset groups (T4 Pro/Salon, T3 Premium, Pilgrim, YS24) contained headlines and descriptions promoting a different brand name (Exhibit B). All were rated 'Poor' for Ad Strength.", bold_prefix="• 2. Another brand's copy in live Performance Max asset groups: ")
add_bullet("Merchant Center shows 216 ineligible products: 110 with 'page unavailable' (404) and 70 with promotional overlay violations. At least ₹80,285 was spent on affected products with zero conversions (for example, one serum SKU spent ₹1,614 on 480 clicks into a 404 page).", bold_prefix="• 3. 110 broken product pages: ")
add_bullet("Daily budgets were changed 140 times in under 60 days (74 increases, 66 decreases). We cannot isolate the effect on delivery, but constant changes make Smart Bidding performance harder to read and slower to stabilize.", bold_prefix="• 4. Frequent budget changes: ")
add_bullet("A campaign named 'Search-Brand' used broad match and triggered queries unrelated to beauty (for example, gym equipment and a badminton ankle support). The spend on these queries is not yet quantified; it will be after a full search terms export.", bold_prefix="• 5. Off-category search queries: ")

add_h1('6.4 Meta Ads Audit')
add_body("Meta spend during the audit period (1 September – 18 November 2026) totaled ₹32.99 Lakhs.")
add_bullet("'Retargeting — DPA - Fabb6' spent ₹9.50 Lakhs for 1,850 purchases at ₹513.70 CPA (peaking at ₹570.31 in October), against ₹479.53 for cold prospecting, with frequency of 3.21 and no past-purchaser exclusions. Excess cost against the cold-prospecting CPA is about ₹63,000.", bold_prefix="• 1. Retargeting more expensive than prospecting: ")
add_bullet("Three Advantage+ Shopping campaigns ran at the same time without product exclusions, so they competed in the same auctions. Account CPM rose from ₹56.15 in August to ₹104.17 in October (+85%) and ₹137.03 in November (+144%). Q4 festive demand raises CPMs for all advertisers, so part of this rise is seasonal. Consolidation to one master Advantage+ campaign will let us measure the effect cleanly.", bold_prefix="• 2. Overlapping Advantage+ Shopping campaigns: ")
add_bullet("₹50,214 across 8.32 million impressions produced 1,02,322 link clicks, 28 landing page views and 0 purchases (99.97% drop-off between click and page view).", bold_prefix="• 3. 'IG-Traffic' link-click campaign: ")
add_bullet("The iOS campaign spent ₹19,161 at frequency 13.18 with 0 sales. The Android campaign spent about ₹1.38 Lakhs at ₹1,082 CPA.", bold_prefix="• 4. App install campaigns: ")
add_bullet("Meta reported 7,34,064 link clicks but only 3,01,798 landing page views on Shopify: a 58.9% gap (52.2% excluding IG-Traffic). Likely causes are mobile page speed, accidental clicks, and pixel or Conversions API (CAPI) misfires. We will diagnose these in the first two weeks.", bold_prefix="• 5. Click-to-landing-page gap: ")

tpath = r'C:\Users\test\Videos\Office\reports\test_p7.docx'
tpdf = r'C:\Users\test\Videos\Office\reports\test_p7.pdf'
doc.save(tpath)

pythoncom.CoInitialize()
w = win32com.client.Dispatch('Word.Application')
w.Visible = False
w.DisplayAlerts = 0
d = w.Documents.Open(os.path.abspath(tpath))
d.SaveAs(os.path.abspath(tpdf), FileFormat=17)
d.Close()
w.Quit()
pythoncom.CoUninitialize()

r = pypdf.PdfReader(tpdf)
print('Page 7 test page count:', len(r.pages))
