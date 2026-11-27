import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    shading_xml = f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'
    cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def format_row(row, bg_hex, text_color, bold=False, font_size=9.5):
    for cell in row.cells:
        set_cell_background(cell, bg_hex)
        set_cell_margins(cell)
        for p in cell.paragraphs:
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            for r in p.runs:
                r.font.name = 'Inter'
                r.font.size = Pt(font_size)
                r.font.bold = bold
                r.font.color.rgb = text_color

doc = docx.Document()

# Page Margins
for s in doc.sections:
    s.top_margin = Inches(0.9)
    s.bottom_margin = Inches(0.9)
    s.left_margin = Inches(0.9)
    s.right_margin = Inches(0.9)

# Brand colors
NAVY = RGBColor(27, 54, 93)     # #1b365d
BLUE = RGBColor(35, 97, 168)    # #2361a8
CYAN = RGBColor(0, 174, 239)    # #00aeef
DARK = RGBColor(15, 23, 42)     # #0f172a
GRAY = RGBColor(100, 116, 139)  # #64748b
WHITE = RGBColor(255, 255, 255)

# HEADER BLOCK
p_top = doc.add_paragraph()
r_co = p_top.add_run('TECHNO EXPONENT\n')
r_co.font.name = 'Outfit'
r_co.font.size = Pt(13)
r_co.font.bold = True
r_co.font.color.rgb = NAVY

r_sub = p_top.add_run('CMMI Level 5 Certified Digital Growth Partner  |  Performance Marketing & Student Acquisition\n\n')
r_sub.font.name = 'Inter'
r_sub.font.size = Pt(9.5)
r_sub.font.color.rgb = GRAY

r_title = p_top.add_run('DIGITAL MARKETING PROPOSAL\nOBA Nursing Academy\n')
r_title.font.name = 'Outfit'
r_title.font.size = Pt(22)
r_title.font.bold = True
r_title.font.color.rgb = BLUE

r_tagline = p_top.add_run('A Phased Student Acquisition Strategy for In-Country International Nurses via Google Ads (Search & Remarketing) and Meta Ads (Engagement & Lead Ads)\n')
r_tagline.font.name = 'Inter'
r_tagline.font.size = Pt(11)
r_tagline.font.italic = True
r_tagline.font.color.rgb = DARK

doc.add_paragraph()

# TABLE 1: PROPOSAL METADATA
t1 = doc.add_table(rows=5, cols=2)
t1.alignment = WD_TABLE_ALIGNMENT.CENTER
t1_data = [
    ('Prepared for:', 'Sandra Thorp, RN BN — Founder & CEO, OBA Nursing Academy (obana.com.au)'),
    ('Prepared by:', 'Techno Exponent'),
    ('Contact:', 'sales@technoexponent.com   |   www.technoexponent.com'),
    ('Date:', 'October 2026'),
    ('Target Audience:', '100% Focus on In-Country International Nurses (Currently Living & Working in Australia)')
]
for i, (k, v) in enumerate(t1_data):
    t1.rows[i].cells[0].paragraphs[0].text = k
    t1.rows[i].cells[1].paragraphs[0].text = v
    format_row(t1.rows[i], 'F8FAFC' if i % 2 == 0 else 'FFFFFF', DARK, font_size=9.5)
    t1.rows[i].cells[0].paragraphs[0].runs[0].font.bold = True
    t1.rows[i].cells[0].paragraphs[0].runs[0].font.color.rgb = NAVY

doc.add_paragraph()

def add_heading(text, level=1):
    h = doc.add_paragraph()
    h.paragraph_format.space_before = Pt(16)
    h.paragraph_format.space_after = Pt(6)
    h.paragraph_format.keep_with_next = True
    r = h.add_run(text)
    r.font.name = 'Outfit'
    r.font.bold = True
    if level == 1:
        r.font.size = Pt(14)
        r.font.color.rgb = NAVY
    elif level == 2:
        r.font.size = Pt(12)
        r.font.color.rgb = BLUE
    else:
        r.font.size = Pt(10.5)
        r.font.color.rgb = DARK
    return h

def add_body(text, bold_prefix=''):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Inter'
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
        r_pre.font.color.rgb = DARK
    r = p.add_run(text)
    r.font.name = 'Inter'
    r.font.size = Pt(10)
    r.font.color.rgb = DARK
    return p

# 1. EXECUTIVE SUMMARY
add_heading('1. Executive summary', 1)
add_body('OBA Nursing Academy has built an elite clinical training pathway in Currumbin, Queensland, dedicated to helping internationally qualified nurses clear the two-stage Outcome-Based Assessment (OBA) for AHPRA registration. Led by experienced registered nurse Sandra Thorp, OBANA provides comprehensive NCLEX-RN preparation alongside a purpose-built simulation facility covering all 39 NMBA clinical assessment stations.')

add_body('This proposal is focused 100% on In-Country International Nurses — qualified nurses and healthcare professionals already residing and working in Australia on temporary visas (Graduate 485, Student 500, Working Holiday 417/462, and TSS 482 partner visas). Many currently work in residential aged care or community disability support as Assistants in Nursing (AINs) or Personal Care Assistants (PCAs) earning A$28–A$35 per hour. Their overseas degree represents immediate earning potential of A$85,000 to A$115,000+ once registered with AHPRA, alongside clear pathways to Permanent Residency (PR). Because they already reside in Australia, they possess local earning power, immediate urgency before visa deadlines, and the physical ability to attend OBANA\'s simulation training in Currumbin.')

add_body('To capture this high-intent in-country audience, we recommend a focused three-month pilot deploying Google Ads (Search campaigns for bottom-funnel intent capture, plus Remarketing campaigns across Display and YouTube) and Meta Advertising (Engagement campaigns showcasing the simulation lab and founder authority, paired with Lead Ads via native Instant Lead Forms).')

add_body('Because this pilot launches through a brand-new advertising account with no prior pixel history or conversion data, the advertising algorithms require an initial calibration and learning period. Our forecast models this realistically: Month 1 is the learning phase (~55% efficiency), Month 2 calibrates search terms and creatives (~80% efficiency), and Month 3 achieves steady-state performance. Over the three-month pilot at a sensible advertising spend of A$2,500 per month (A$1,500 Google + A$1,000 Meta), we forecast 70 to 118 qualified student leads, generating an estimated 13 to 24 enrolled students and A$15,600 to A$28,800 in initial course revenue.')

# 2. WHAT WE HEARD FROM YOU & BUSINESS OVERVIEW
add_heading('2. What we heard from you and business overview', 1)
add_body('Based on our review of OBA Nursing Academy\'s published offerings and digital presence, the core operational facts guiding this plan are:')

t_bus = doc.add_table(rows=7, cols=2)
t_bus.alignment = WD_TABLE_ALIGNMENT.CENTER
t_bus_data = [
    ('Business name', 'OBA Nursing Academy (ABN: 38 015 879 575)'),
    ('Founder & Leadership', 'Sandra Thorp, RN BN — Founder & Chief Executive Officer'),
    ('Head Office & Lab', 'Currumbin QLD 4223, Australia'),
    ('Target Audience', '100% Dedicated to In-Country International Nurses living and working in Australia'),
    ('Core Course Catalog', '2026 NCLEX-RN/PN Prep, OSCE Simulation Intensive, Comprehensive Nursing Pathway (RN/EN), Midwife Pathway, AMC Standard Pathway'),
    ('Published Pricing', '4-Week ($349 AUD), 8-Week ($869 AUD), 12-Week ($1,230 AUD), 16-Week Mastery ($1,700 AUD); OSCE Intensive (~$2,450–$3,200 AUD)'),
    ('Primary Differentiators', 'All 39 NMBA OSCE simulation stations in real clinical lab; practicing RN leadership; integrated Employer Readiness Program for Australian job placement')
]
for i, (k, v) in enumerate(t_bus_data):
    t_bus.rows[i].cells[0].paragraphs[0].text = k
    t_bus.rows[i].cells[1].paragraphs[0].text = v
    format_row(t_bus.rows[i], 'F8FAFC' if i % 2 == 0 else 'FFFFFF', DARK, font_size=9.5)
    t_bus.rows[i].cells[0].paragraphs[0].runs[0].font.bold = True
    t_bus.rows[i].cells[0].paragraphs[0].runs[0].font.color.rgb = NAVY

doc.add_paragraph()

# 3. WEBSITE AND DIGITAL PRESENCE AUDIT
add_heading('3. Website and digital presence audit', 1)
add_body('An independent audit of obana.com.au conducted in October 2026 highlights several strong foundation assets along with clear marketing gaps:')

t_audit = doc.add_table(rows=5, cols=3)
t_audit.alignment = WD_TABLE_ALIGNMENT.CENTER
t_audit_headers = ['Area Audited', 'What We Found', 'What We Will Do in the Pilot']
for j, h in enumerate(t_audit_headers):
    t_audit.rows[0].cells[j].paragraphs[0].text = h
format_row(t_audit.rows[0], '1B365D', WHITE, bold=True, font_size=9.5)

audit_data = [
    ('Google Search Footprint', 'The site is indexed for branded searches (\"OBA Nursing Academy\"), but has negligible search presence for non-brand terms like \"nclex prep australia\" or \"osce course gold coast\". Competitors in Sydney and Melbourne capture this traffic.', 'Launch targeted Google Search campaigns focused on high-intent transactional search queries for NCLEX and OSCE courses across Queensland, NSW, Victoria, and WA.'),
    ('Tracking and Analytics Setup', 'Basic Google Analytics is in place, but conversion goals, Google Ads conversion tracking, and Meta Pixel event tracking are not configured to measure course inquiries or checkout starts.', 'Deploy client-side Google Tag Manager (GTM), GA4 custom conversion events, Google Ads Conversion & Remarketing Tags, and the browser-based Meta Pixel to track all lead actions accurately.'),
    ('Paid Advertising Activity', 'No active search ads or social ads were found in public ad libraries. Competitors like Nurse Assist International and IHM are actively bidding and capturing prospective nurses daily.', 'Build and launch targeted Google Search & Remarketing campaigns and Meta Engagement & Lead Ads highlighting the Currumbin lab and student testimonials.'),
    ('Lead Capture Mechanism', 'Prospective students must navigate multi-step contact pages; there is no zero-friction mobile capture mechanism or direct enquiry form.', 'Implement native Meta Instant Forms that auto-fill verified user contact details and capture key qualifiers (visa status, nursing degree, exam target date).')
]
for i, row in enumerate(audit_data):
    for j, val in enumerate(row):
        t_audit.rows[i+1].cells[j].paragraphs[0].text = val
    format_row(t_audit.rows[i+1], 'F8FAFC' if i % 2 == 0 else 'FFFFFF', DARK, font_size=9.0)

doc.add_paragraph()

# 4. MARKET UNDERSTANDING & IN-COUNTRY CANDIDATE PROFILES
add_heading('4. Market understanding: 100% Focus on In-Country International Nurses', 1)
add_body('Unlike generic programs that attempt to market internationally, this strategy focuses 100% of the advertising budget on internationally qualified nurses currently living and working in Australia. These candidates possess high urgency, immediate purchasing power, and the ability to travel to Currumbin for hands-on simulation training. They divide into three actionable sub-segments:')

add_body(' Qualified nurses currently working in residential aged care facilities, hospitals, or community disability care earning A$28–A$35/hour. They already possess practical patient care experience in Australia, know the healthcare terminology, and have strong financial motivation to complete their OBA to unlock A$85k–A$115k RN salaries.', 'Sub-Segment A — Aged Care & Disability Care Workers (AINs / PCWs) (~50% of In-Country Demand):')
add_body(' International nursing graduates on 485 Temporary Graduate visas or Subclass 500 student visas facing fixed visa expiry deadlines. They urgently require AHPRA registration to submit their Expression of Interest (EOI) for skilled migration visas (Subclass 189, 190, 491). Delaying registration risks visa expiration.', 'Sub-Segment B — Temporary Visa Holders Facing Visa Deadlines (~35% of In-Country Demand):')
add_body(' In-country nurses who previously attempted the NCLEX or OSCE after using unstructured question banks and did not pass. They are seeking structured clinical judgment coaching and realistic clinical simulation to guarantee a pass on their next attempt.', 'Sub-Segment C — Repeat Candidates Seeking Structured Clinical Reasoning (~15% of In-Country Demand):')

# 5. COMPETITOR LANDSCAPE
add_heading('5. Competitor landscape in Australia', 1)
add_body('A review of direct preparation providers active in the Australian market:')

t_comp = doc.add_table(rows=6, cols=3)
t_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
comp_headers = ['Competitor', 'Market Footprint', 'Gap OBANA Can Exploit']
for j, h in enumerate(comp_headers):
    t_comp.rows[0].cells[j].paragraphs[0].text = h
format_row(t_comp.rows[0], '1B365D', WHITE, bold=True, font_size=9.5)

comp_data = [
    ('Nurse Assist International (NAI)', 'Sydney & Melbourne; heavy Google & Meta advertising footprint', 'High package costs ($4,000+); large, crowded cohorts. OBANA offers high-touch trainer support and boutique simulation in Currumbin.'),
    ('Institute of Health & Management (IHM)', 'Melbourne, Sydney, Perth; established higher-education institute', 'Rigid academic semester intakes and slower enrollment processes. OBANA offers flexible, self-paced starts and rolling live weekly support.'),
    ('Menzies Institute of Technology', 'Melbourne-based CRICOS provider', 'Outdated web presentation; minimal video storytelling. OBANA\'s practicing RN leadership and student video reviews build stronger emotional credibility.'),
    ('Spectraa High', 'Melbourne & Adelaide; focused on OSCE simulation', 'No physical training lab in Queensland. OBANA commands the Gold Coast, Brisbane, and Northern NSW catchment area.'),
    ('Signet Institute of Australia', 'Melbourne & Adelaide test packages', 'Generic course marketing without prominent founder clinical authority. Sandra Thorp\'s RN background creates an immediate trust advantage.')
]
for i, row in enumerate(comp_data):
    for j, val in enumerate(row):
        t_comp.rows[i+1].cells[j].paragraphs[0].text = val
    format_row(t_comp.rows[i+1], 'F8FAFC' if i % 2 == 0 else 'FFFFFF', DARK, font_size=9.0)

doc.add_paragraph()

# 6. RECOMMENDED STRATEGY
add_heading('6. Recommended strategy: Google Ads & Meta Ads Architecture', 1)
add_body('We recommend an integrated strategy tailored specifically to in-country nurses across Australia, utilizing Google Ads for Search and Remarketing, and Meta Ads for Engagement and Lead Ads:')

t_strat = doc.add_table(rows=5, cols=3)
t_strat.alignment = WD_TABLE_ALIGNMENT.CENTER
strat_headers = ['Campaign Type', 'Role in the In-Country Pilot', 'Why Now']
for j, h in enumerate(strat_headers):
    t_strat.rows[0].cells[j].paragraphs[0].text = h
format_row(t_strat.rows[0], '1B365D', WHITE, bold=True, font_size=9.5)

strat_data = [
    ('Google Ads: Search Campaigns\nSpend: A$1,100 / month', 'Captures in-country nurses actively searching on Google for \"nclex prep australia\", \"oba course fees\", \"osce training gold coast\", and \"ahpra registration course\". High-intent exact and phrase match ad groups ensure budget targets bottom-funnel candidates.', 'In-country nurses actively search Google when ready to book. Bidding on high-intent terms captures them at the exact moment of commercial consideration.'),
    ('Google Ads: Remarketing Campaigns\nSpend: A$400 / month', 'Re-engages website visitors across the Google Display Network and YouTube who visited course pages or initiated checkout but did not complete enrollment. Delivers student pass testimonials and intake countdowns.', 'Professional course purchases have a 7–21 day consideration cycle. Remarketing keeps OBANA top of mind and recovers high-intent visitors at low incremental cost.'),
    ('Meta Ads: Engagement Campaigns\nSpend: A$400 / month', 'Deploys video reels and carousel ads showcasing Sandra Thorp RN, the Currumbin simulation lab (all 39 NMBA stations), and student milestone celebrations. Maximizes post shares, saves, and comments across nurse community groups in Australia.', 'Builds deep trust, community engagement, and establishes OBANA as the premier clinical training facility, creating warm audience pools for retargeting.'),
    ('Meta Ads: Lead Ads (Instant Forms)\nSpend: A$600 / month', 'Deploys native Meta Instant Lead Forms targeting healthcare workers, AINs, and international nurse groups in Australia. Forms auto-fill user details and qualify visa status, current role, and target exam date with zero mobile friction.', 'Over 80% of in-country nurses browse Instagram and Facebook during shift breaks. Native forms eliminate slow mobile page load drop-off, capturing leads at A$25–A$40 CPL.')
]
for i, row in enumerate(strat_data):
    for j, val in enumerate(row):
        t_strat.rows[i+1].cells[j].paragraphs[0].text = val
    format_row(t_strat.rows[i+1], 'F8FAFC' if i % 2 == 0 else 'FFFFFF', DARK, font_size=9.0)

doc.add_paragraph()

add_body('Client-Side Tracking Setup: We will implement standard client-side tracking using Google Tag Manager (GTM), Google Analytics 4 (GA4) custom conversion events, Google Ads Conversion & Remarketing Tags, and the browser-based Meta Pixel. Clean tracking ensures both Google and Meta algorithms learn which audiences actually submit inquiries and enroll, avoiding wasted spend.')

# 7. THREE-MONTH PILOT PLAN
add_heading('7. Three-month pilot plan', 1)
add_body('Because this campaign launches in a new advertising account, performance will develop across three distinct operational phases:')

t_pilot = doc.add_table(rows=4, cols=3)
t_pilot.alignment = WD_TABLE_ALIGNMENT.CENTER
pilot_headers = ['Month', 'Google Ads Activity (Search & Remarketing)', 'Meta Advertising Activity (Engagement & Lead Ads)']
for j, h in enumerate(pilot_headers):
    t_pilot.rows[0].cells[j].paragraphs[0].text = h
format_row(t_pilot.rows[0], '1B365D', WHITE, bold=True, font_size=9.5)

pilot_data = [
    ('Month 1: Setup, Baseline & Learning Phase', 'Set up GTM, GA4 events, Google Ads tag, and Meta Pixel. Build negative keyword master list (blocking free dumps, jobs, university degrees). Launch Exact Match Search campaigns for NCLEX-RN and OSCE. Launch initial Display Remarketing to site visitors.', 'Produce 4–6 static and video ad creatives highlighting Sandra Thorp RN, the Currumbin simulation lab, and student results. Launch Meta Engagement video reels to build custom audience pools. Launch native Meta Lead Ads for in-country nurses.'),
    ('Month 2: Calibration & Negative Search Mining', 'Review search term reports weekly to isolate winning search queries and prune non-converting terms. A/B test ad headlines and descriptions. Expand YouTube video remarketing to nurses who visited course pages.', 'Refresh creative angles based on initial engagement. Test student pass scorecards against lab simulation tours. Optimize Lead Ad qualifying questions. Introduce click-to-WhatsApp direct inquiry options for mobile users.'),
    ('Month 3: Steady-State Optimization & Scale', 'Transition mature search ad groups to smart bidding (Maximize Conversions with target CPA limits) as conversion volume stabilizes. Expand remarketing frequency caps to maintain high top-of-mind recall.', 'Scale ad spend on top-performing creative sets within controlled budget limits. Target high-density healthcare postcodes in Brisbane, Gold Coast, Sydney, Melbourne, and Perth with tailored local messaging.')
]
for i, row in enumerate(pilot_data):
    for j, val in enumerate(row):
        t_pilot.rows[i+1].cells[j].paragraphs[0].text = val
    format_row(t_pilot.rows[i+1], 'F8FAFC' if i % 2 == 0 else 'FFFFFF', DARK, font_size=9.0)

doc.add_paragraph()

add_heading('Success measures reviewed monthly', 2)
add_body('Qualified In-Country Student Inquiries (Leads): Verified inquiries submitted by nurses residing in Australia, split between Google Search/Remarketing and Meta Lead Ads.')
add_body('Cost per Qualified Lead (CPL): Total ad spend divided by verified in-country leads, tracked separately for Google Ads and Meta Ads.')
add_body('Engagement Rate & Video Completion: Engagement metrics on Meta reels (shares, saves, 50%+ video watch time) measuring brand trust and community resonance.')
add_body('Lead-to-Enrollment Conversion Rate: Percentage of inquiries that complete enrollment into the 4-week, 8-week, 12-week, 16-week, or OSCE courses.')

# 8. FORECAST
add_heading('8. Forecast and expected outcomes', 1)
add_body('We modelled three performance scenarios for a combined monthly advertising budget of A$2,500 (A$1,500 Google Ads Search & Remarketing + A$1,000 Meta Engagement & Lead Ads), focused 100% on in-country international nurses.')

add_body('Important Note on New Ad Accounts: In a brand-new advertising account with no historical pixel data or conversion track record, the advertising algorithms undergo an initial calibration and learning period. Accordingly, our forecast models Month 1 at roughly 55% of steady-state efficiency, Month 2 at roughly 80% as search term mining and negative lists eliminate wasted spend, and Month 3 reaching full steady state.')

t_fore = doc.add_table(rows=8, cols=5)
t_fore.alignment = WD_TABLE_ALIGNMENT.CENTER
fore_headers = ['Metric (Monthly / Pilot)', 'Conservative', 'Base Case', 'Optimistic', 'Basis']
for j, h in enumerate(fore_headers):
    t_fore.rows[0].cells[j].paragraphs[0].text = h
format_row(t_fore.rows[0], '1B365D', WHITE, bold=True, font_size=9.5)

fore_data = [
    ('Monthly Ad Spend (Google + Meta)', 'A$2,500', 'A$2,500', 'A$2,500', 'A$1,500 Google + A$1,000 Meta'),
    ('Blended Cost per Click (CPC)', 'A$3.85', 'A$3.35', 'A$2.95', 'Australian healthcare benchmarks'),
    ('Monthly Clicks Generated', '649', '746', '847', 'Budget divided by blended CPC'),
    ('Blended Conversion Rate (Steady State)', '4.8%', '5.8%', '7.0%', 'Landing page & native form benchmarks'),
    ('Steady-State Leads (Month 3)', '31 leads', '43 leads', '59 leads', 'Clicks multiplied by conversion rate'),
    ('Cost per Lead at Steady State', 'A$80.65', 'A$58.14', 'A$42.37', 'Budget divided by steady-state leads'),
    ('Total Qualified Leads Over 3-Month Pilot', '70 leads', '97–102 leads', '133 leads', 'Ramp-up: Mo 1 (55%), Mo 2 (80%), Mo 3 (100%)')
]
for i, row in enumerate(fore_data):
    for j, val in enumerate(row):
        t_fore.rows[i+1].cells[j].paragraphs[0].text = val
    format_row(t_fore.rows[i+1], 'F8FAFC' if i % 2 == 0 else 'FFFFFF', DARK, font_size=9.0)

doc.add_paragraph()

add_heading('Month-by-month pilot ramp-up projection (Base Case)', 2)

t_ramp = doc.add_table(rows=5, cols=5)
t_ramp.alignment = WD_TABLE_ALIGNMENT.CENTER
ramp_headers = ['Pilot Month', 'Stage & Operational Focus', 'Ad Spend', 'Expected Leads', 'Cost per Lead']
for j, h in enumerate(ramp_headers):
    t_ramp.rows[0].cells[j].paragraphs[0].text = h
format_row(t_ramp.rows[0], '1B365D', WHITE, bold=True, font_size=9.5)

ramp_data = [
    ('Month 1', 'Account Setup & Algorithmic Learning Phase (~55% efficiency)', 'A$2,500', '24 leads', 'A$104.17'),
    ('Month 2', 'Data Calibration & Search Term Optimization (~80% efficiency)', 'A$2,500', '35 leads', 'A$71.43'),
    ('Month 3', 'Steady-State Performance & Optimization (100% steady state)', 'A$2,500', '43 leads', 'A$58.14'),
    ('Total 3-Month Pilot', 'Three-Month Cumulative Pilot Results', 'A$7,500', '102 leads', 'A$73.53 (Blended)')
]
for i, row in enumerate(ramp_data):
    for j, val in enumerate(row):
        t_ramp.rows[i+1].cells[j].paragraphs[0].text = val
    bg = 'D1FAE5' if i == 3 else ('F8FAFC' if i % 2 == 0 else 'FFFFFF')
    tc = RGBColor(6, 95, 70) if i == 3 else DARK
    format_row(t_ramp.rows[i+1], bg, tc, bold=(i == 3), font_size=9.0)

doc.add_paragraph()

add_heading('Reality check on payback and course revenue', 2)
add_body('At an average course value of A$1,200 (reflecting a mix of 4-week, 8-week, 12-week, and 16-week enrollments):')
add_body(' Closing 18% of the 70 leads = 13 enrolled students. Course revenue = A$15,600 (2.08x return on ad spend).', 'Conservative:')
add_body(' Closing 20% of the 97–102 leads = 20 enrolled students. Course revenue = A$24,000 (3.20x return on ad spend).', 'Base Case:')
add_body(' Closing 22% of the 133 leads = 29 enrolled students. Course revenue = A$34,800 (4.64x return on ad spend).', 'Optimistic:')
add_body('Downstream Value: A significant share of in-country NCLEX graduates subsequently enroll in OBANA\'s OSCE Clinical Skills Intensive in Currumbin (A$2,450–A$3,200). When factoring in downstream OSCE enrollments, customer lifetime value rises above A$3,000, compounding the long-term return on advertising spend well beyond initial pilot figures.')

# 9. INVESTMENT
add_heading('9. Investment', 1)
add_body('Our management fees are structured transparently from our agency catalog, quoted in Australian Dollars (AUD):')

t_inv = doc.add_table(rows=5, cols=2)
t_inv.alignment = WD_TABLE_ALIGNMENT.CENTER
inv_data = [
    ('Service', 'Monthly Fee (Australian Dollars)'),
    ('Google Ads Management (Search & Remarketing campaigns, keyword research, negative matching, and weekly search term pruning)', 'A$600 / month'),
    ('Meta Advertising Management (Engagement & Lead Ads, Instant Form setup, creative design, and copywriting)', 'A$500 / month'),
    ('Standard Combined Total', 'A$1,100 / month'),
    ('Bundled Retainer Rate (Both channels — approximately twelve percent agency saving)', 'A$970 / month')
]
for i, (k, v) in enumerate(inv_data):
    t_inv.rows[i].cells[0].paragraphs[0].text = k
    t_inv.rows[i].cells[1].paragraphs[0].text = v
    if i == 0:
        format_row(t_inv.rows[i], '1B365D', WHITE, bold=True, font_size=9.5)
    elif i == 4:
        format_row(t_inv.rows[i], 'D1FAE5', RGBColor(6, 95, 70), bold=True, font_size=10.0)
    else:
        format_row(t_inv.rows[i], 'F8FAFC' if i % 2 == 0 else 'FFFFFF', DARK, font_size=9.5)

doc.add_paragraph()

add_body('Platform Advertising Spend: Recommended at A$2,000 to A$2,500 per month (paid directly by OBA Nursing Academy to Google and Meta). Media spend is billed to your own corporate card and is separate from the management fee above.')

# 10. COMMERCIAL NOTES & DISCLAIMER
add_heading('10. Commercial notes and disclaimer', 1)
add_body('Direct Platform Billing: Advertising platform spend is paid directly by OBA Nursing Academy to Google and Meta through your own ad accounts. Techno Exponent does not handle or mark up media spend.', '1. ')
add_body('Pilot Term & Notice: This proposal is built as a three-month pilot to allow the new ad accounts sufficient time to pass the initial learning phase and stabilize. The engagement continues month-to-month thereafter with 30 days written notice to cancel.', '2. ')
add_body('Tracking Scope: Tracking implementation covers client-side deployment via Google Tag Manager (GTM), Google Analytics 4 (GA4), Google Ads conversion tags, and browser-based Meta Pixel.', '3. ')
add_body('Inclusions: Complete ad account architecture, keyword research, negative keyword management, 4–6 custom designed ad creatives per month, weekly performance reporting, and a monthly strategy review call.', '4. ')
add_body('Creative Approval: All ad copy, visual assets, and campaign targeting will be shared for your approval before going live. Nothing is published without your sign-off.', '5. ')
add_body('Intellectual Property: OBA Nursing Academy retains full, exclusive ownership of all advertising accounts, creatives, copy, audience data, and leads generated.', '6. ')

# 11. NEXT STEPS
add_heading('11. Next Steps', 1)
add_body('1. Confirm this proposal and your preferred monthly ad spend tier (A$2,000–A$2,500 / month).')
add_body('2. Share access to Google Tag Manager, Google Analytics, and confirmation/creation of your Google Ads and Meta Business Manager accounts.')
add_body('3. Schedule a 30-minute kickoff discussion with the Techno Exponent performance marketing team to align on priority course intakes and ad creative tone.')
add_body('4. Techno Exponent initiates tracking deployment and draft creative assets within three working days of kickoff.')

p_sign = doc.add_paragraph()
p_sign.paragraph_format.space_before = Pt(20)
r_end = p_sign.add_run('Prepared by Techno Exponent\nsales@technoexponent.com   |   www.technoexponent.com')
r_end.font.name = 'Inter'
r_end.font.size = Pt(9.5)
r_end.font.italic = True
r_end.font.color.rgb = GRAY

# Save files
path_data = r'c:\Users\test\Videos\Office\data\Proposal\Digital_Marketing_Proposal_Obana_Techno_Exponent.docx'
path_prop = r'c:\Users\test\Videos\Office\Proposals\Digital_Marketing_Proposal_Obana_Techno_Exponent.docx'

doc.save(path_data)
doc.save(path_prop)
print('Successfully generated refined DOCX proposals at:')
print('  -', path_data)
print('  -', path_prop)
