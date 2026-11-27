import os
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

# Brand colors matching Techno Exponent standards
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

r_sub = p_top.add_run('CMMI Level 5 Certified Digital Growth Partner  |  Full-Funnel E-Commerce Performance Marketing\n\n')
r_sub.font.name = 'Inter'
r_sub.font.size = Pt(9.5)
r_sub.font.color.rgb = GRAY

r_title = p_top.add_run('DIGITAL MARKETING PROPOSAL & PLAN OF ACTION\nMillie Coastal Accents\n')
r_title.font.name = 'Outfit'
r_title.font.size = Pt(22)
r_title.font.bold = True
r_title.font.color.rgb = BLUE

r_tagline = p_top.add_run('An Integrated E-Commerce Scaling Strategy via Google Ads (Shopping/PMax & Search) and Meta Ads (Advantage+ & Dynamic Catalog Retargeting)\n')
r_tagline.font.name = 'Inter'
r_tagline.font.size = Pt(11)
r_tagline.font.italic = True
r_tagline.font.color.rgb = DARK

doc.add_paragraph()

# TABLE 1: PROPOSAL METADATA
t1 = doc.add_table(rows=6, cols=2)
t1.alignment = WD_TABLE_ALIGNMENT.CENTER
t1_data = [
    ('Client Name:', 'Millie Coastal Accents (Boutique & E-Commerce Store)'),
    ('Physical Flagship:', 'Monarch Bay Plaza, 32880 Pacific Coast Hwy #36, Dana Point, CA 92629'),
    ('Digital Properties:', 'milliecoastalaccents.com | instagram.com/millieclothing | facebook.com/MILLIEMONARCH'),
    ('Prepared by:', 'Techno Exponent'),
    ('Contact:', 'sales@technoexponent.com   |   www.technoexponent.com'),
    ('Date & Version:', 'November 2026   |   Strategic E-Commerce Growth Architecture v1.0')
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

def add_bullet(text, bold_prefix=''):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = 'Inter'
        r_pre.font.size = Pt(9.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = DARK
    r = p.add_run(text)
    r.font.name = 'Inter'
    r.font.size = Pt(9.5)
    r.font.color.rgb = DARK
    return p

def add_callout(text, title=''):
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = t.rows[0].cells[0]
    set_cell_background(cell, 'F0F9FF')
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    if title:
        rt = p.add_run(title + '\n')
        rt.font.name = 'Outfit'
        rt.font.size = Pt(10.5)
        rt.font.bold = True
        rt.font.color.rgb = NAVY
    rb = p.add_run(text)
    rb.font.name = 'Inter'
    rb.font.size = Pt(9.5)
    rb.font.color.rgb = DARK
    doc.add_paragraph()

# SECTION 1: EXECUTIVE SUMMARY
add_heading('1. Executive Summary & Brand Diagnostic', 1)
add_body('Millie Coastal Accents represents a premier luxury coastal boutique based in Monarch Bay Plaza in Dana Point, California. With a deeply curated physical storefront and an expanding e-commerce presence (milliecoastalaccents.com), the boutique carries over 523 active products across 41+ prestigious contemporary designer labels—including Frank & Eileen, White + Warren, Paige, Velvet by Graham & Spencer, MISA Los Angeles, Poupette St. Barth, AG Jeans, Jellycat London, and Pampa Bay.')
add_body('While the physical boutique enjoys an affluent, high-trust local patronage along the California coast, the online e-commerce channel holds immense untapped potential. In the contemporary luxury boutique sector, Average Order Values (AOV) naturally range between $220 and $350. However, converting online traffic into profitable, predictable e-commerce revenue requires an omnichannel performance engine that bridges high-intent transactional search demand with visual social discovery.')
add_body('Techno Exponent has engineered this dedicated digital marketing proposal and plan of action to scale Millie Coastal Accents into a nationally recognized coastal lifestyle boutique destination. Our strategy orchestrates Google Ads (Google Shopping/Performance Max and High-Intent Brand Search) with Meta Ads (Advantage+ Shopping Campaigns and Dynamic Catalog Retargeting) to drive sustainable, profitable direct-to-consumer (D2C) growth.')

add_callout(
    '1. High-Value Catalog: 523+ SKUs spanning women’s designer apparel (397 items), luxury baby/children gifts (119 items), and refined coastal home goods (37 items) provide outstanding cross-selling and high AOV potential.\n'
    '2. High-Intent Demand Capture: Thousands of high-income shoppers search monthly for exact designer labels carried by Millie (e.g., Frank & Eileen shirtdresses, White + Warren cashmere wraps, Paige denim, Jellycat gifts).\n'
    '3. Visual Lifestyle Synergy: Meta (Instagram & Facebook) serves as the primary inspiration hub where coastal styling, unboxing reels, and curated outfits drive high-volume brand discovery.\n'
    '4. Cold-Start Algorithmic Ramp-Up: Acknowledging that advertising accounts require algorithmic learning, our financial model reflects realistic 3-month scaling (55% efficiency in Month 1 ramping to 100% steady state in Month 3).',
    'KEY STRATEGIC OPPORTUNITIES FOR MILLIE COASTAL ACCENTS'
)

# SECTION 2: BRAND & AUDIENCE ARCHITECTURE
add_heading('2. Brand Diagnostic & Target Buyer Personas', 1)
add_body('To maximize ad budget efficiency and avoid wasted ad spend, our campaigns will target three distinct, highly profitable buyer personas across both regional affluent hubs and nationwide coastal lifestyle markets:')

add_heading('Persona 1: The Coastal Sophisticate ("Laguna Luxury")', 2)
add_bullet('Affluent women aged 35–62 with Household Incomes (HHI) of $175,000+ residing in coastal Southern California (Orange County, Newport Beach, Laguna Beach, San Diego) and key US luxury resort markets (Hamptons NY, Palm Beach FL, Scottsdale AZ, Charleston SC).', 'Demographics & Geo: ')
add_bullet('Values effortless, understated luxury ("Quiet Luxury"), premium natural fabrics (cashmere, pure linen, fine Italian cotton, Japanese denim), and versatile day-to-evening coastal styling.', 'Psychographics: ')
add_bullet('Frank & Eileen (woven shirtdresses & button-downs, $280–$350), White + Warren (cashmere travel wraps, $350–$420), Paige & AG Jeans ($215–$280), Velvet by Graham & Spencer, MISA Los Angeles, Poupette St. Barth.', 'Core Brand Affinity: ')
add_bullet('Google Shopping/PMax for specific designer searches, Meta Instagram Reels featuring curated outfit pairings and seasonal capsule edits.', 'Primary Channel: ')

add_heading('Persona 2: The Thoughtful Gifter & Grandparent ("The Nursery Curator")', 2)
add_bullet('Women aged 38–70 purchasing luxury baby shower gifts, newborn welcome sets, christening gifts, and milestone birthday presents.', 'Demographics: ')
add_bullet('Driven by emotion, quality, and heirloom standards. Willing to spend $60–$180 on a curated gift basket combining organic clothing and collectible plush toys.', 'Psychographics: ')
add_bullet('Jellycat London (viral plush collectibles, $25–$65), Kissy Kissy (Peruvian Pima cotton layette, $45–$95), Angel Dear, Emerson & Friends, Elegant Baby, Milkbarn.', 'Core Brand Affinity: ')
add_bullet('High-converting Meta Carousel ads showcasing gift bundles ("The Ultimate Newborn Gift"), Google Search queries for "luxury baby boutique gifts" and "Jellycat retailer near me".', 'Primary Channel: ')

add_heading('Persona 3: The Coastal Homemaker & Hostess', 2)
add_bullet('Affluent homeowners and entertainers aged 30–58 seeking distinctive tabletop accessories, hostess gifts, and elegant coastal accents.', 'Demographics: ')
add_bullet('Entertains frequently, loves coastal aesthetics (driftwood, sea glass, crisp white porcelain, titanium serveware).', 'Psychographics: ')
add_bullet('Pampa Bay (tarnish-free titanium-finished porcelain), Selbrae House, Mersea (resort wraps and home scents), Indaba, Kerri Rosenthal.', 'Core Brand Affinity: ')
add_bullet('Dynamic Meta Catalog Ads and seasonal holiday gift guide campaigns.', 'Primary Channel: ')

# SECTION 3: GOOGLE ADS STRATEGY
add_heading('3. Google Ads Strategy: High-Intent Search & Shopping Dominance', 1)
add_body('Google Ads will function as Millie’s primary commercial capture engine. While social media builds desire, Google captures shoppers at the exact moment of transactional intent when they are actively searching to purchase.')

add_heading('3.1 Google Shopping & Performance Max (PMax) Campaigns', 2)
add_body('Performance Max will serve as the heavy lifter for e-commerce catalog sales, syndicating Millie’s products across Google Shopping, Search, YouTube, Gmail, and Google Display Network.')
add_bullet('We will synchronize Millie’s product catalog with Google Merchant Center, implementing rich attribute tagging (Brand, Product Type, Material, Color, Size, Gender, GTIN/MPN) and structured category taxonomy to maximize impression share.', 'Product Feed Optimization: ')
add_bullet('Instead of lumping all 523 products into a single generic campaign, we structure Asset Groups by Product Margin, Average Order Value (AOV), and Buyer Persona:', 'Tiered Asset Group Architecture: ')

# TABLE 2: ASSET GROUP ARCHITECTURE
t2 = doc.add_table(rows=4, cols=4)
t2.alignment = WD_TABLE_ALIGNMENT.CENTER
t2_headers = ['Asset Group Tier', 'Featured Brands / SKUs', 'Target AOV', 'Targeting Signals & Custom Segments']
for j, h in enumerate(t2_headers):
    t2.rows[0].cells[j].paragraphs[0].text = h
format_row(t2.rows[0], '1B365D', WHITE, bold=True, font_size=9.5)

t2_rows = [
    ('Tier 1: Hero Designer Apparel', 'Frank & Eileen, White + Warren, Paige, Velvet, MISA, Poupette St. Barth, AG Jeans', '$280 – $380', 'In-market luxury fashion shoppers, high HHI (Top 10-20%), searchers of competing luxury boutiques (Revolve, Saks, Tuckernuck)'),
    ('Tier 2: Luxury Baby & Children Gifting', 'Jellycat London, Kissy Kissy, Angel Dear, Emerson & Friends, Elegant Baby', '$65 – $140', 'In-market baby shower gifts, expectant parents, high-intent plush toy collectors, parents with toddlers (0-3 yrs)'),
    ('Tier 3: Coastal Home & Hostess', 'Pampa Bay, Mersea, Selbrae House, Indaba, scented candles & tabletop', '$85 – $180', 'Home decor enthusiasts, entertaining & gourmet dining, seasonal holiday gifting segments, wedding registry shoppers')
]
for i, row in enumerate(t2_rows, start=1):
    for j, val in enumerate(row):
        t2.rows[i].cells[j].paragraphs[0].text = val
    format_row(t2.rows[i], 'F8FAFC' if i % 2 == 1 else 'FFFFFF', DARK, font_size=9)

doc.add_paragraph()

add_heading('3.2 Google Search Campaigns (Brand Defense & Designer Keywords)', 2)
add_body('We will deploy tightly themed Search ad groups utilizing Exact Match and Phrase Match to capture high-margin transactional queries without wasting budget on broad informational searches:')
add_bullet('Protecting "Millie Coastal Accents", "Millie Clothing Dana Point", "Millie Monarch Bay" to prevent competitors or local boutiques from bidding on your brand name.', 'Campaign 1: Brand Defense Search — ')
add_bullet('Targeting exact transactional keywords where shoppers have high purchase intent: e.g., "Frank and Eileen Mary dress", "White and Warren cashmere travel wrap", "Misa Los Angeles maxi dress", "buy Paige Cindy jeans", "Jellycat official retailer online".', 'Campaign 2: High-Intent Designer Brand Search — ')
add_bullet('A pre-loaded negative keyword library containing 350+ terms blocking irrelevant traffic (e.g., "cheap", "wholesale", "used", "counterfeit", "replica", "jobs", "careers", "sewing patterns", "DIY", "review").', 'Negative Keyword Protection Shield — ')

# SECTION 4: META ADS STRATEGY
add_heading('4. Meta Ads Strategy: Visual Demand Generation & Dynamic Retargeting', 1)
add_body('Meta Ads (Instagram & Facebook) provide the visual canvas essential for fashion, lifestyle, and gifting. Our Meta strategy is designed to stop the scroll, create emotional desire, and automatically retarget warm prospects with the exact items they browsed.')

add_heading('4.1 Advantage+ Shopping Campaigns (ASC+) & Cold Prospecting (TOF)', 2)
add_body('We will leverage Meta’s advanced AI-driven Advantage+ Shopping Campaigns (ASC+) combined with structured interest and lifestyle prospecting:')
add_bullet('Targeting women aged 30–65 in the United States with interests in Contemporary Designer Apparel, Boutique Shopping, Coastal Living, Resort Wear, and Luxury Fashion.', 'Broad & Interest-Led Prospecting: ')
add_bullet('Targeting high-income zip codes across Southern California coastal towns (Dana Point, Newport Beach, Laguna Beach, San Clemente) and nationwide coastal hubs (Hamptons, Palm Beach, Naples, Santa Barbara, Carmel).', 'Geographic Affluence Layering: ')
add_bullet('Once baseline purchase data is established, we will generate 1%–2% Lookalike Audiences derived from high-value purchasers and email subscribers.', 'Lookalike Audience Expansion: ')

add_heading('4.2 The 4 E-Commerce Creative Angles', 2)
add_body('To prevent ad fatigue and resonate across different buying motivations, we will deploy four distinct creative formats:')

add_bullet('High-resolution video reels and multi-card carousels showing complete outfits styled together (e.g., Frank & Eileen crisp linen button-down paired with Paige wide-leg denim and Chan Luu accessories). Tagline: "Effortless Coastal Dressing, Curated in Dana Point."', 'Creative Angle A: "The Curated Outfit Capsule" — ')
add_bullet('Lifestyle imagery with warm California sunlight, coastal scenery, and relaxed elegance. Positions Millie not just as a store, but as an aspirational coastal lifestyle.', 'Creative Angle B: "California Coastal Living" — ')
add_bullet('Emotional, vibrant visuals featuring Jellycat plush pairings with ultra-soft Kissy Kissy Pima cotton sets. Tagline: "The Baby Shower Gift Everyone Will Remember."', 'Creative Angle C: "The Heirloom Baby Gift" — ')
add_bullet('Behind-the-scenes store walk-throughs at Monarch Bay Plaza, highlighting the care in hand-packaging online orders and personal customer service. Overcomes online trust barriers for first-time shoppers.', 'Creative Angle D: "Boutique Story & Unboxing" — ')

add_heading('4.3 Dynamic Product Ads (DPA) & Middle/Bottom of Funnel Retargeting', 2)
add_body('Over 96% of first-time website visitors do not purchase on their initial visit. Our retargeting architecture ensures zero wasted traffic:')
add_bullet('Automatically serves carousel ads showing the exact products a shopper viewed or added to cart on milliecoastalaccents.com within the last 1–14 days.', 'Dynamic Product Ads (DPA): ')
add_bullet('Targeting Instagram and Facebook page engagers and video viewers with customer testimonials, press mentions, and brand heritage messaging.', 'Social Proof Overlays: ')
add_bullet('Callouts emphasizing "Fast US Shipping", "Easy Boutique Returns", and "Complimentary Gift Wrapping" to remove final purchase hesitation.', 'Friction Reduction CTAs: ')

# SECTION 5: TRACKING & ANALYTICS ARCHITECTURE
add_heading('5. Tracking, Attribution & Analytics Infrastructure', 1)
add_body('Accurate measurement is the foundation of profitable advertising. Techno Exponent will implement a complete, robust client-side tracking architecture using Google Tag Manager:')

add_bullet('Centralized container hosting all tracking tags, ensuring fast site speed and clean code governance without slowing down page load.', 'Google Tag Manager (GTM) Container: ')
add_bullet('Full e-commerce data layer implementation tracking the entire shopper journey: view_item_list, view_item, add_to_cart, remove_from_cart, begin_checkout, add_shipping_info, add_payment_info, and purchase (with transaction revenue, tax, shipping, and product item arrays).', 'Google Analytics 4 (GA4) Enhanced E-Commerce: ')
add_bullet('Primary purchase conversion tag setup with Google Enhanced Conversions (securely hashing first-party customer data to improve conversion modeling and cross-device tracking).', 'Google Ads Conversion & Remarketing Tags: ')
add_bullet('Full event mapping (PageView, ViewContent, AddToCart, InitiateCheckout, Purchase) with Advanced Matching enabled to maximize event match quality across Safari/iOS and Chrome.', 'Meta Pixel Implementation: ')

add_callout(
    'In strict accordance with agency standards and client infrastructure capabilities, all tracking will be deployed via robust client-side GTM tagging, including GA4 Enhanced E-Commerce, Google Ads Conversion Tags with Enhanced Conversions, and Meta Pixel with Advanced Matching, ensuring complete attribution integrity and zero ongoing infrastructure fees.',
    'TRACKING SCOPE & INTEGRITY COMMITMENT'
)

# SECTION 6: 90-DAY PLAN OF ACTION
add_heading('6. Comprehensive 90-Day Plan of Action (Week-by-Week Roadmap)', 1)
add_body('Our 90-day onboarding and growth roadmap ensures a structured, transparent rollout designed to build data assets and scale revenue systematically:')

# TABLE 3: 90-DAY ROADMAP
t3 = doc.add_table(rows=5, cols=3)
t3.alignment = WD_TABLE_ALIGNMENT.CENTER
t3_headers = ['Phase & Timeline', 'Primary Strategic Focus', 'Core Deliverables & Execution Milestones']
for j, h in enumerate(t3_headers):
    t3.rows[0].cells[j].paragraphs[0].text = h
format_row(t3.rows[0], '1B365D', WHITE, bold=True, font_size=9.5)

t3_rows = [
    ('Phase 1: Setup & Foundation\n(Weeks 1 – 2 | Month 1)', 'Data Infrastructure, Feed Setup & Campaign Architecture', 
     '• GTM container setup, GA4 e-commerce data layer integration, Meta Pixel & Google Ads tags.\n• Google Merchant Center feed synchronization, product category mapping, GMC policy approval.\n• Campaign builds: Brand Defense Search, Hero Designer Apparel PMax, Meta Advantage+ Shopping.\n• Creative asset production: 4 distinct ad angles (Outfit Capsules, Coastal Living, Baby Gifting, Boutique Walkthrough).'),
    ('Phase 2: Algorithmic Learning & Cold-Start\n(Weeks 3 – 4 | Month 1)', 'Audience Discovery, Negative Mining & Baseline Calibration', 
     '• Launch campaigns under controlled daily budgets adhering to the New Ad Account Cold-Start Rule.\n• Daily search term mining to aggressively populate negative keyword lists on Google.\n• Monitor creative CTR and early Add-to-Cart velocity on Meta Ads.\n• Establish Dynamic Product Ads (DPA) retargeting loops once audience pools reach 1,000 visitors.'),
    ('Phase 3: Data Calibration & Expansion\n(Weeks 5 – 8 | Month 2)', 'SKU Optimization, Creative Refresh & Bid Transitions', 
     '• Analyze Google Shopping SKU performance: funnel 70% of spend into top 20% converting brands.\n• Rotate fresh creative variations into Meta Ads to replace fatigue-prone creatives.\n• Transition Google Search and PMax to Target ROAS (tROAS) bidding as conversion volume permits.\n• Launch Luxury Baby & Children PMax Asset Group targeting holiday/seasonal gifting.'),
    ('Phase 4: Steady-State Scaling\n(Weeks 9 – 12 | Month 3)', 'Profit Maximization, Lookalikes & Budget Scaling', 
     '• Scale winning campaigns within the <= 20% budget swing guardrail every 72 hours.\n• Deploy high-value Lookalike Audiences on Meta based on verified customer purchase data.\n• Finalize seasonal promotional campaign frameworks (Resort Collection drop, Spring preview).\n• Comprehensive 90-day executive review, ROAS audit, and Q2 growth expansion roadmap.')
]
for i, row in enumerate(t3_rows, start=1):
    for j, val in enumerate(row):
        t3.rows[i].cells[j].paragraphs[0].text = val
    format_row(t3.rows[i], 'F8FAFC' if i % 2 == 1 else 'FFFFFF', DARK, font_size=9)

doc.add_paragraph()

# SECTION 7: REALISTIC FINANCIAL FORECASTING
add_heading('7. Realistic Budget & 3-Month Performance Forecast', 1)
add_body('In performance marketing, speculative revenue guarantees create false expectations. Techno Exponent adheres to evidence-based modeling governed by the New Ad Account Cold-Start Rule:')

add_callout(
    'The New Ad Account Cold-Start Rule: In newly deployed advertising accounts, Google and Meta algorithms have zero historic pixel purchase data. Month 1 operates in algorithmic exploration (~55% efficiency) as the platforms identify high-converting buyer profiles. Month 2 achieves calibration (~80% efficiency) through negative query filtering and creative optimization. By Month 3, campaigns achieve 100% steady-state efficiency with stable Customer Acquisition Costs (CPA) and optimized ROAS.',
    'REALISTIC PERFORMANCE MODELING PRINCIPLE'
)

add_heading('7.1 Recommended Monthly Media Spend Allocation', 2)
add_body('We recommend an initial media budget of $3,000 USD / month (billed directly by Google and Meta to the client’s payment card):')
add_bullet('Allocated across Google Shopping/PMax (Tier 1 & Tier 2 Asset Groups), Brand Defense Search, and High-Intent Designer Keywords.', 'Google Ads: $1,800 USD / month (60% split) — ')
add_bullet('Allocated across Advantage+ Shopping Prospecting (Cold Traffic), Lifestyle Video Ads, and Dynamic Catalog Retargeting (DPA).', 'Meta Ads: $1,200 USD / month (40% split) — ')
add_bullet('Reflecting Millie’s premium designer price points ($150–$350 for apparel, $65–$140 for baby gifts).', 'Projected Average Order Value (AOV): $240 USD — ')

add_heading('7.2 3-Month Ramp-Up Performance Model ($3,000 / mo Media Spend)', 2)

# TABLE 4: 3-MONTH RAMP UP MODEL
t4 = doc.add_table(rows=5, cols=7)
t4.alignment = WD_TABLE_ALIGNMENT.CENTER
t4_headers = ['Month & Phase', 'Monthly Spend', 'Avg. AOV', 'Expected Orders', 'Blended CPA', 'Gross Revenue', 'Projected ROAS']
for j, h in enumerate(t4_headers):
    t4.rows[0].cells[j].paragraphs[0].text = h
format_row(t4.rows[0], '1B365D', WHITE, bold=True, font_size=9.5)

t4_rows = [
    ('Month 1 (Learning Phase ~55%)', '$3,000', '$240', '28 orders', '$107.14', '$6,720', '2.24x ROAS'),
    ('Month 2 (Calibration Phase ~80%)', '$3,000', '$240', '42 orders', '$71.43', '$10,080', '3.36x ROAS'),
    ('Month 3 (Steady-State 100%)', '$3,000', '$240', '54 orders', '$55.56', '$12,960', '4.32x ROAS'),
    ('3-Month Pilot Cumulative', '$9,000', '$240', '124 orders', '$72.58', '$29,760', '3.31x Blended')
]
for i, row in enumerate(t4_rows, start=1):
    for j, val in enumerate(row):
        t4.rows[i].cells[j].paragraphs[0].text = val
    format_row(t4.rows[i], 'F8FAFC' if i % 2 == 1 else 'FFFFFF', DARK, font_size=9)
    if i == 4:
        t4.rows[i].cells[0].paragraphs[0].runs[0].font.bold = True
        t4.rows[i].cells[5].paragraphs[0].runs[0].font.bold = True
        t4.rows[i].cells[6].paragraphs[0].runs[0].font.bold = True

doc.add_paragraph()

add_heading('7.3 Steady-State 3-Tier Scenario Matrix (Month 3+ at $3,000 / mo)', 2)
add_body('The following matrix illustrates steady-state performance across Conservative, Expected, and Aggressive conversion benchmarks:')

# TABLE 5: 3-TIER SCENARIOS
t5 = doc.add_table(rows=4, cols=7)
t5.alignment = WD_TABLE_ALIGNMENT.CENTER
t5_headers = ['Scenario Tier', 'Est. Clicks', 'Avg. CPC', 'Store CVR', 'Est. Orders', 'Gross Revenue', 'Projected ROAS']
for j, h in enumerate(t5_headers):
    t5.rows[0].cells[j].paragraphs[0].text = h
format_row(t5.rows[0], '1B365D', WHITE, bold=True, font_size=9.5)

t5_rows = [
    ('Conservative Tier', '2,500', '$1.20', '1.84%', '46 orders', '$11,040', '3.68x ROAS'),
    ('Expected Tier (Target)', '2,300', '$1.30', '2.35%', '54 orders', '$12,960', '4.32x ROAS'),
    ('Aggressive Tier', '2,100', '$1.43', '3.10%', '65 orders', '$15,600', '5.20x ROAS')
]
for i, row in enumerate(t5_rows, start=1):
    for j, val in enumerate(row):
        t5.rows[i].cells[j].paragraphs[0].text = val
    format_row(t5.rows[i], 'F8FAFC' if i % 2 == 1 else 'FFFFFF', DARK, font_size=9)
    if i == 2:
        t5.rows[i].cells[0].paragraphs[0].runs[0].font.bold = True
        t5.rows[i].cells[5].paragraphs[0].runs[0].font.bold = True

doc.add_paragraph()

# SECTION 8: COMMERCIAL RETAINER & INVESTMENT
add_heading('8. Agency Retainer & Commercial Packaging', 1)
add_body('Techno Exponent provides transparent, flat-fee monthly management with zero hidden percentage-of-spend surcharges during the initial pilot:')

# TABLE 6: PRICING
t6 = doc.add_table(rows=4, cols=4)
t6.alignment = WD_TABLE_ALIGNMENT.CENTER
t6_headers = ['Service Module', 'Included Channels & Scope', 'Standard Retainer', 'Bundled Growth Package']
for j, h in enumerate(t6_headers):
    t6.rows[0].cells[j].paragraphs[0].text = h
format_row(t6.rows[0], '1B365D', WHITE, bold=True, font_size=9.5)

t6_rows = [
    ('Google Ads Management', 'Google Shopping/PMax, Brand Defense Search, High-Intent Designer Search, Merchant Center feed hygiene, bid management.', '$600 USD / mo', 'Included in Bundle'),
    ('Meta Ads Management', 'Advantage+ Shopping Campaigns, Lifestyle Video/Reels, 4 Creative Concepts, Dynamic Product Ads (DPA) retargeting.', '$600 USD / mo', 'Included in Bundle'),
    ('Integrated Omnichannel Retainer (Google + Meta)', 'Complete full-funnel management across both platforms, GTM & GA4 e-commerce tracking, weekly sprint reports, bi-weekly strategy calls.', '$1,200 USD / mo', '$950 USD / month\n(Save $250 / mo | ~21% Discount)')
]
for i, row in enumerate(t6_rows, start=1):
    for j, val in enumerate(row):
        t6.rows[i].cells[j].paragraphs[0].text = val
    format_row(t6.rows[i], 'F8FAFC' if i % 2 == 1 else 'FFFFFF', DARK, font_size=9)
    if i == 3:
        t6.rows[i].cells[0].paragraphs[0].runs[0].font.bold = True
        t6.rows[i].cells[3].paragraphs[0].runs[0].font.bold = True
        t6.rows[i].cells[3].paragraphs[0].runs[0].font.color.rgb = BLUE

doc.add_paragraph()

add_bullet('Zero Setup Fees: Technical onboarding, GTM data layer setup, and Google Merchant Center feed synchronization ($750 value) are waived on a 3-month commitment.', 'Complimentary Technical Setup: ')
add_bullet('Direct Ad Billing: Media ad spend ($3,000/mo recommended) is billed directly by Google and Meta to Millie’s business credit card, ensuring complete financial transparency and points accrual.', 'Transparent Billing: ')
add_bullet('No Long-Term Lock-in: Initial 3-month pilot agreement to navigate the cold-start learning phase, transitioning to a month-to-month rolling agreement thereafter with 30-day notice.', 'Flexible Terms: ')

# SECTION 9: REPORTING & WAYS OF WORKING
add_heading('9. Reporting, Governance & Terms of Engagement', 1)
add_body('As a CMMI Level-5 certified organization, Techno Exponent upholds rigorous operational standards and proactive communication:')

add_bullet('A customized, real-time dashboard displaying ad spend, impressions, clicks, purchases, CPA, and ROAS across Google and Meta, accessible 24/7.', 'Live 24/7 Looker Studio Dashboard: ')
add_bullet('Weekly performance summary emails detailing completed optimizations, search term mining results, and upcoming creative tests.', 'Weekly Performance Sprints: ')
add_bullet('Scheduled 30-minute Zoom meetings with your dedicated Senior Media Buyer and Account Strategist to review results and align with in-store inventory.', 'Bi-Weekly Strategic Reviews: ')
add_bullet('Direct access via a dedicated Slack or Skype channel for instant communication, quick creative approvals, and inventory coordination.', 'Direct Agency Slack/Skype Channel: ')
add_bullet('Millie Coastal Accents retains 100% full ownership of all advertising accounts, Google Merchant Center feeds, GTM containers, GA4 properties, and Meta Pixels. If engagement ceases, all data remains client property.', 'Client Data Ownership: ')

doc.add_paragraph()
add_heading('10. Next Steps & Launch Roadmap', 1)
add_bullet('Millie confirms acceptance of the proposed 3-month pilot strategy and bundled retainer ($950/mo).', 'Step 1: Formal Proposal Sign-Off — ')
add_bullet('Techno Exponent provides a standardized, simple Master Services Agreement (MSA) and onboarding invoice.', 'Step 2: Agreement & Onboarding Invoice — ')
add_bullet('Granting partner-level access to Google Ads, Google Merchant Center, Meta Business Manager, and Shopify/CMS.', 'Step 3: Asset Access & Kickoff Workshop — ')
add_bullet('Sprint 1 commences immediately: GTM/GA4/Pixel tracking deployment, Google Merchant Center sync, and creative production.', 'Step 4: Sprint 1 Launch (Within 5 Business Days) — ')

# Output path
out_path_1 = os.path.abspath('data/Proposal/Digital_Marketing_Proposal_Millie_Coastal_Accents_Techno_Exponent.docx')
out_dir = os.path.dirname(out_path_1)
if not os.path.exists(out_dir):
    os.makedirs(out_dir, exist_ok=True)
doc.save(out_path_1)
print(f'Successfully generated Word proposal at: {out_path_1}')
