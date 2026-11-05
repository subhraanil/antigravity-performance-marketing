import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# --- COLOR PALETTE DEFINITIONS ---
C_BG_DARK = RGBColor(10, 25, 47)       # Deep Navy #0A192F
C_CARD_DARK = RGBColor(17, 34, 64)     # Card Navy #112240
C_CARD_HOVER = RGBColor(23, 42, 69)    # Slightly lighter navy #172A45
C_GOLD = RGBColor(182, 140, 90)        # Official Brand Accent #B68C5A
C_GOLD_LIGHT = RGBColor(218, 185, 142)  # Soft Gold #DAB98E
C_CYAN = RGBColor(56, 189, 248)        # Accent Cyan #38BDF8
C_WHITE = RGBColor(255, 255, 255)      # Pure White #FFFFFF
C_TEXT_LIGHT = RGBColor(241, 245, 249) # Off-White #F1F5F9
C_TEXT_MUTED = RGBColor(148, 163, 184) # Slate Muted #94A3B8
C_BORDER_SLATE = RGBColor(30, 41, 59)  # Slate Border #1E293B
C_BORDER_GOLD = RGBColor(182, 140, 90) # Gold Border

FONT_HEADING = "Calibri"
FONT_BODY = "Calibri"

def set_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = C_BG_DARK

def add_header(slide, category, title, subtitle=None, logo_path=None):
    tx_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8.5), Inches(0.35))
    tf = tx_box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = category.upper()
    p.font.name = FONT_HEADING
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_GOLD
    
    tx_box2 = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(8.5), Inches(0.65))
    tf2 = tx_box2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0
    p2 = tf2.paragraphs[0]
    p2.text = title
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(24)
    p2.font.bold = True
    p2.font.color.rgb = C_WHITE

    if subtitle:
        p_sub = tf2.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(12)
        p_sub.font.color.rgb = C_TEXT_MUTED

    if logo_path and os.path.exists(logo_path):
        slide.shapes.add_picture(logo_path, Inches(9.8), Inches(0.45), width=Inches(2.7))

def add_footer(slide, current_slide, total_slides=12):
    line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(7.05), Inches(11.733), Inches(0.015))
    line.fill.solid()
    line.fill.fore_color.rgb = C_BORDER_SLATE
    line.line.color.rgb = C_BORDER_SLATE

    tx_left = slide.shapes.add_textbox(Inches(0.8), Inches(7.1), Inches(7.0), Inches(0.3))
    tf_l = tx_left.text_frame
    tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0
    p_l = tf_l.paragraphs[0]
    p_l.text = "THE INTERNATIONAL ARBITRATOR | www.theinternationalarbitrator.com"
    p_l.font.name = FONT_BODY
    p_l.font.size = Pt(9)
    p_l.font.color.rgb = C_TEXT_MUTED

    tx_right = slide.shapes.add_textbox(Inches(10.5), Inches(7.1), Inches(2.0), Inches(0.3))
    tf_r = tx_right.text_frame
    tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0
    p_r = tf_r.paragraphs[0]
    p_r.alignment = PP_ALIGN.RIGHT
    p_r.text = f"{current_slide:02d} / {total_slides:02d}"
    p_r.font.name = FONT_BODY
    p_r.font.size = Pt(9)
    p_r.font.bold = True
    p_r.font.color.rgb = C_GOLD

def create_card(slide, left, top, width, height, title=None, bg_color=C_CARD_DARK, border_color=C_BORDER_SLATE):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1)

    if title:
        tx_box = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), Inches(0.4))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = FONT_HEADING
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = C_GOLD_LIGHT
    return card

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_slide_layout = prs.slide_layouts[6]
    
    asset_dir = os.path.abspath('data/content for PPT/images')
    hero_img = os.path.join(asset_dir, 'hero_no_flame_perfect.jpg')
    divergence_img = os.path.join(asset_dir, 'pricing_divergence_chart.png')
    lng_img = os.path.join(asset_dir, 'lng_vessel_global_trade_1788447510919.jpg')
    chamber_img = os.path.join(asset_dir, 'arbitration_hearing_chamber_1788447528651.jpg')
    logo_light = os.path.join(asset_dir, 'logo_light.png')

    # ==========================================
    # SLIDE 1: COVER
    # ==========================================
    s1 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s1)

    if os.path.exists(hero_img):
        s1.shapes.add_picture(hero_img, Inches(6.4), Inches(0.6), width=Inches(6.1), height=Inches(6.2))

    if os.path.exists(logo_light):
        s1.shapes.add_picture(logo_light, Inches(0.8), Inches(0.8), width=Inches(3.8))

    tbox = s1.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(5.3), Inches(4.5))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p_badge = tf.paragraphs[0]
    p_badge.text = "EXECUTIVE BRIEFING & OFF-PAGE INSIGHTS"
    p_badge.font.name = FONT_HEADING
    p_badge.font.size = Pt(11)
    p_badge.font.bold = True
    p_badge.font.color.rgb = C_GOLD
    p_badge.space_after = Pt(14)

    p_title = tf.add_paragraph()
    p_title.text = "Gas Price Disputes &\nInternational Arbitration"
    p_title.font.name = FONT_HEADING
    p_title.font.size = Pt(32)
    p_title.font.bold = True
    p_title.font.color.rgb = C_WHITE
    p_title.space_after = Pt(14)

    p_sub = tf.add_paragraph()
    p_sub.text = "Navigating Long-Term Contracts, Market Volatility, Formula Reviews, and Multi-Billion Dollar Cross-Border Claims."
    p_sub.font.name = FONT_BODY
    p_sub.font.size = Pt(13)
    p_sub.font.color.rgb = C_TEXT_MUTED
    p_sub.space_after = Pt(28)

    p_auth = tf.add_paragraph()
    p_auth.text = "Harshavardhan Sancheti"
    p_auth.font.name = FONT_HEADING
    p_auth.font.size = Pt(14)
    p_auth.font.bold = True
    p_auth.font.color.rgb = C_GOLD_LIGHT

    p_desig = tf.add_paragraph()
    p_desig.text = "Independent International Commercial Arbitrator\nLondon | New York | Geneva | New Delhi"
    p_desig.font.name = FONT_BODY
    p_desig.font.size = Pt(10.5)
    p_desig.font.color.rgb = C_TEXT_MUTED

    add_footer(s1, 1)

    # ==========================================
    # SLIDE 2: THE CORE CONFLICT
    # ==========================================
    s2 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s2)
    add_header(s2, "01. The Economic Root Cause", "The Clash: Contract Permanence vs. Market Volatility",
               "Why rigid 15-25 year take-or-pay sales contracts structurally collide with rapid market liberalization.", logo_light)

    create_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(2.5), "The Take-or-Pay Infrastructure Guarantee")
    tbox = s2.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(1.8))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p1 = tf.paragraphs[0]
    p1.text = "• Massive Upfront Capital: Pipelines and LNG liquefaction facilities require billions in capital, secured by 15-25 year take-or-pay volume commitments."
    p1.font.size = Pt(11.5)
    p1.font.color.rgb = C_TEXT_LIGHT
    p1.space_after = Pt(8)
    p2 = tf.add_paragraph()
    p2.text = "• Rigid Volume Assurances: Buyers must pay for minimum annual volumes regardless of actual demand or off-take capacity."
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = C_TEXT_LIGHT

    create_card(s2, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.5), "The Shift: Oil Indexation to Hub Pricing")
    tbox = s2.shapes.add_textbox(Inches(1.0), Inches(4.9), Inches(5.2), Inches(1.8))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p1 = tf.paragraphs[0]
    p1.text = "• Historical Oil Anchors: Contracts traditionally tied prices to crude and heating fuel baskets as substitute energy sources."
    p1.font.size = Pt(11.5)
    p1.font.color.rgb = C_TEXT_LIGHT
    p1.space_after = Pt(8)
    p2 = tf.add_paragraph()
    p2.text = "• Liquid Hub Divergence: The emergence of liquid hubs (TTF, NBP, Henry Hub) decoupled gas values from oil, creating multi-billion dollar price gaps."
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = C_TEXT_LIGHT

    if os.path.exists(divergence_img):
        s2.shapes.add_picture(divergence_img, Inches(6.6), Inches(1.6), width=Inches(5.9), height=Inches(5.2))

    add_footer(s2, 2)

    # ==========================================
    # SLIDE 3: ANATOMY OF A GAS PRICE DISPUTE
    # ==========================================
    s3 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s3)
    add_header(s3, "02. Contractual Triggers", "Anatomy of a Gas Price Dispute",
               "Disputes rarely stem from simple non-payment; they emerge from four core contractual adjustment mechanisms.", logo_light)

    cards_data_s3 = [
        ("Take-or-Pay Volume Deficits", 
         "• Financial Shock: When downstream demand collapses, buyers face ruinous penalties for un-taken contract volumes.\n• Project Debt Dependency: Upstream producers depend on guaranteed off-take cash flows to service extraction and pipeline debt.",
         Inches(0.8), Inches(1.6)),
        ("Price Review & Reopener Clauses", 
         "• Open-Textured Triggers: Triggered by 'unforeseen substantial changes' or to mirror 'fair netback market value'.\n• Valuation Impasse: The ambiguity of these clauses creates wide divergence between buyer and seller econometric models.",
         Inches(6.8), Inches(1.6)),
        ("Indexation Mismatch & Decoupling", 
         "• Fuel Substitution Decoupling: Brent crude spikes while local gas hub spot prices plummet, rendering oil formulas untenable.\n• Formula Revision Demands: Buyers demand transition to gas-on-gas hub pricing; sellers defend original contract bargains.",
         Inches(0.8), Inches(4.3)),
        ("LNG Destination & Cargo Diversion", 
         "• Arbitrage Barriers: Sellers historically barred buyers from reselling cargoes outside designated ports to defend price tiers.\n• Antitrust & Profit Sharing: Buyers challenge destination bans as anti-competitive, demanding global cargo diversion rights.",
         Inches(6.8), Inches(4.3))
    ]

    for title, desc, left, top in cards_data_s3:
        create_card(s3, left, top, Inches(5.7), Inches(2.45), title)
        tbox = s3.shapes.add_textbox(left + Inches(0.2), top + Inches(0.65), Inches(5.3), Inches(1.65))
        tf = tbox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = desc
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_LIGHT
        p.line_spacing = 1.25

    add_footer(s3, 3)

    # ==========================================
    # SLIDE 4: WHY NEGOTIATIONS ESCALATE
    # ==========================================
    s4 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s4)
    add_header(s4, "03. Commercial Friction", "Why Commercial Renegotiations Break Down",
               "Most price reviews settle amicably, but high-stakes structural barriers often force parties into formal arbitration.", logo_light)

    c_w = Inches(7.5)
    c_h = Inches(1.55)
    reasons = [
        ("Massive Financial Stakes", "A price variance of mere cents per MMBtu across multi-billion cubic meter deliveries compounds into hundreds of millions to billions of dollars over a contract cycle."),
        ("Irreconcilable Economic Methodologies", "Parties retain top-tier econometric experts who reach vastly contradictory valuations from identical market datasets, creating an unbridgeable bargaining impasse."),
        ("Dangerous Precedent & Sovereign Constraints", "Conceding a price reduction to one utility creates domino pressure from all other buyers. Furthermore, state-linked energy entities face political blowback if they compromise out of court.")
    ]

    top_pos = Inches(1.6)
    for title, desc in reasons:
        create_card(s4, Inches(0.8), top_pos, c_w, c_h, title)
        tbox = s4.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.55), c_w - Inches(0.4), Inches(0.9))
        tf = tbox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = desc
        p.font.size = Pt(11.5)
        p.font.color.rgb = C_TEXT_LIGHT
        p.line_spacing = 1.2
        top_pos += Inches(1.75)

    create_card(s4, Inches(8.6), Inches(1.6), Inches(3.9), Inches(5.05), "Key Industry Reality", bg_color=C_CARD_HOVER, border_color=C_BORDER_GOLD)
    tbox_r = s4.shapes.add_textbox(Inches(8.85), Inches(2.3), Inches(3.4), Inches(4.1))
    tf_r = tbox_r.text_frame
    tf_r.word_wrap = True
    tf_r.margin_left = tf_r.margin_top = tf_r.margin_right = tf_r.margin_bottom = 0

    p_r1 = tf_r.paragraphs[0]
    p_r1.text = "\"Arbitration is not an admission of commercial failure in the energy sector - it is the planned, structured forum to test complex valuation models.\""
    p_r1.font.size = Pt(13)
    p_r1.font.bold = True
    p_r1.font.color.rgb = C_GOLD_LIGHT
    p_r1.space_after = Pt(16)

    p_r2 = tf_r.add_paragraph()
    p_r2.text = "When upstream project finance and sovereign stakeholders are involved, an independent arbitral award provides the legal cover and finality required by boards and regulatory auditors."
    p_r2.font.size = Pt(11.5)
    p_r2.font.color.rgb = C_TEXT_LIGHT
    p_r2.line_spacing = 1.25

    add_footer(s4, 4)

    # ==========================================
    # SLIDE 5: WHY ARBITRATION OVER LITIGATION
    # ==========================================
    s5 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s5)
    add_header(s5, "04. Strategic Forum Selection", "Why Arbitration Dominates Over National Courts",
               "Key structural factors that make international commercial arbitration the gold standard for cross-border gas disputes.", logo_light)

    table_shape = s5.shapes.add_table(7, 3, Inches(0.8), Inches(1.6), Inches(11.733), Inches(5.1))
    table = table_shape.table
    table.columns[0].width = Inches(2.6)
    table.columns[1].width = Inches(4.566)
    table.columns[2].width = Inches(4.566)

    headers = ["Strategic Factor", "International Arbitration", "National Court Litigation"]
    for col_idx, text in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = C_CARD_HOVER
        p = cell.text_frame.paragraphs[0]
        p.text = text
        p.font.name = FONT_HEADING
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = C_GOLD_LIGHT

    rows_data = [
        ("Confidentiality", "Proceedings, pricing formulas, margins, and awards remain strictly private.", "Public filings, open hearings, and media scrutiny compromise trade secrets."),
        ("Decision-Maker Expertise", "Parties select arbitrators with specialized energy economics and engineering fluency.", "Randomly assigned generalist judges rarely possess deep energy market expertise."),
        ("Neutral Forum", "Eliminates perceived 'home-court' judicial bias between foreign and state-owned entities.", "One party faces litigation on the foreign counterparty's domestic home turf."),
        ("Global Enforceability", "Awards enforceable worldwide across 170+ member states via the New York Convention.", "Judgments face a fragmented, unreliable patchwork of bilateral enforcement treaties."),
        ("Procedural Flexibility", "Timetables, bifurcation (liability vs. quantum), and expert hot-tubbing tailored to fit.", "Rigid, inflexible civil procedure rules unsuitable for intricate multi-year modeling."),
        ("Finality & Speed", "Final, binding resolution with strictly limited grounds for annulment or appeal.", "Multi-tiered court appeals can paralyze commercial contracts for 5 to 10+ years.")
    ]

    for row_idx, data in enumerate(rows_data, start=1):
        bg = C_CARD_DARK if row_idx % 2 == 1 else C_BG_DARK
        for col_idx, text in enumerate(data):
            cell = table.cell(row_idx, col_idx)
            cell.fill.solid()
            cell.fill.fore_color.rgb = bg
            p = cell.text_frame.paragraphs[0]
            p.text = text
            p.font.name = FONT_BODY
            p.font.size = Pt(10.5)
            p.font.color.rgb = C_WHITE if col_idx == 0 else C_TEXT_LIGHT
            if col_idx == 0:
                p.font.bold = True

    add_footer(s5, 5)

    # ==========================================
    # SLIDE 6: LEADING ARBITRAL INSTITUTIONS
    # ==========================================
    s6 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s6)
    add_header(s6, "05. Institutional Architecture", "Leading Arbitral Institutions in Gas Disputes",
               "The choice of institution reflects the governing law, geographic flow, and specific regional market nuances.", logo_light)

    inst_cards = [
        ("ICC (Paris)", "Global Energy Standard", 
         "The preeminent choice for high-value cross-border energy disputes worldwide. Known for its rigorous award scrutiny process ensuring maximum cross-border enforceability.", Inches(0.8), Inches(1.6)),
        ("SCC (Stockholm)", "Pipeline Gas Heritage", 
         "Historic hub for Eastern European, Russian, and Eurasian pipeline gas disputes. Deep track record managing multi-billion dollar transit and take-or-pay proceedings.", Inches(4.8), Inches(1.6)),
        ("LCIA (London)", "English Law Dominance", 
         "Preferred forum for contracts governed by English law. Known for highly efficient case management, procedural rigor, and leading specialist energy arbitrators.", Inches(8.8), Inches(1.6)),
        ("SIAC & HKIAC (Asia)", "The LNG Growth Engine", 
         "Crucial centers for Asia-Pacific LNG trade, portfolio supply agreements, and Chinese/Southeast Asian long-term off-take contracts with rapid emergency arbitrator mechanisms.", Inches(0.8), Inches(4.3)),
        ("UNCITRAL (Ad Hoc)", "Bespoke Party Autonomy", 
         "Frequently chosen in legacy sovereign contracts and pipeline treaties where state parties demand full procedural control without permanent institutional administration.", Inches(6.8), Inches(4.3))
    ]

    for idx, (title, tag, desc, left, top) in enumerate(inst_cards):
        width = Inches(3.7) if idx < 3 else Inches(5.7)
        create_card(s6, left, top, width, Inches(2.45), title)
        tbox = s6.shapes.add_textbox(left + Inches(0.2), top + Inches(0.6), width - Inches(0.4), Inches(1.7))
        tf = tbox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_tag = tf.paragraphs[0]
        p_tag.text = tag.upper()
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = C_CYAN
        p_tag.space_after = Pt(6)

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = C_TEXT_LIGHT
        p_desc.line_spacing = 1.25

    add_footer(s6, 6)

    # ==========================================
    # SLIDE 7: PRECEDENTS & CASE TRENDS
    # ==========================================
    s7 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s7)
    add_header(s7, "06. Landmark Precedents", "Case Trends Shaping the Global Gas Industry",
               "Though proceedings remain confidential, public awards and disclosures have transformed global contractual standards.", logo_light)

    left_w = Inches(6.2)
    top_pos = Inches(1.6)
    cases = [
        ("European Price Reviews (ICC & Ad Hoc)", 
         "During the early 2010s, Continental European utilities triggered widespread arbitrations as spot hub prices plummeted below oil formulas. Tribunals ordered sweeping retroactive price adjustments and mandated hybrid hub-indexation formulas."),
        ("Historic Transit & Take-or-Pay Claims (SCC)", 
         "Landmark SCC proceedings between national energy giants resolved massive decade-long pipeline transit tariffs and billions in take-or-pay claims, proving arbitration's unique capacity to handle geopolitically explosive disputes."),
        ("Dismantling LNG Destination Clauses", 
         "Arbitral challenges combined with antitrust scrutiny successfully dismantled rigid destination restrictions, granting LNG buyers freedom to divert cargoes to whichever market offers peak netback returns.")
    ]

    for title, desc in cases:
        create_card(s7, Inches(0.8), top_pos, left_w, Inches(1.6), title)
        tbox = s7.shapes.add_textbox(Inches(1.0), top_pos + Inches(0.55), left_w - Inches(0.4), Inches(0.95))
        tf = tbox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = desc
        p.font.size = Pt(11)
        p.font.color.rgb = C_TEXT_LIGHT
        p.line_spacing = 1.2
        top_pos += Inches(1.75)

    if os.path.exists(lng_img):
        s7.shapes.add_picture(lng_img, Inches(7.3), Inches(1.6), width=Inches(5.2), height=Inches(5.05))

    add_footer(s7, 7)

    # ==========================================
    # SLIDE 8: EXPERT EVIDENCE & QUANTUM
    # ==========================================
    s8 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s8)
    add_header(s8, "07. The True Battleground", "The Decisive Role of Expert Evidence & Quantum",
               "Gas price arbitrations are won or lost on expert testimony. Legal rights are clear; economic quantum is disputed.", logo_light)

    if os.path.exists(chamber_img):
        s8.shapes.add_picture(chamber_img, Inches(0.8), Inches(1.6), width=Inches(5.4), height=Inches(5.1))

    right_w = Inches(6.0)
    right_l = Inches(6.5)
    
    create_card(s8, right_l, Inches(1.6), right_w, Inches(3.2), "Three Vital Categories of Experts")
    tbox = s8.shapes.add_textbox(right_l + Inches(0.25), Inches(2.2), right_w - Inches(0.5), Inches(2.5))
    tf = tbox.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

    p1 = tf.paragraphs[0]
    p1.text = "1. Market & Econometric Experts: Construct netback valuations, analyze substitute fuel baskets, and establish fair market value benchmarks."
    p1.font.size = Pt(11.5)
    p1.font.color.rgb = C_TEXT_LIGHT
    p1.space_after = Pt(8)

    p2 = tf.add_paragraph()
    p2.text = "2. Technical & Gas Engineers: Address calorific variations, pipeline transit bottlenecks, liquefaction boil-off, and terminal capacity constraints."
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = C_TEXT_LIGHT
    p2.space_after = Pt(8)

    p3 = tf.add_paragraph()
    p3.text = "3. Quantum & Financial Forensic Experts: Model complex retroactive adjustments, tax implications, and compounded interest across multi-year delivery periods."
    p3.font.size = Pt(11.5)
    p3.font.color.rgb = C_TEXT_LIGHT

    create_card(s8, right_l, Inches(5.0), right_w, Inches(1.7), "Tribunal Technique: 'Hot-Tubbing' (Concurrent Evidence)", bg_color=C_CARD_HOVER, border_color=C_BORDER_GOLD)
    tbox_ht = s8.shapes.add_textbox(right_l + Inches(0.25), Inches(5.55), right_w - Inches(0.5), Inches(1.0))
    tf_ht = tbox_ht.text_frame
    tf_ht.word_wrap = True
    tf_ht.margin_left = tf_ht.margin_top = tf_ht.margin_right = tf_ht.margin_bottom = 0
    p_ht = tf_ht.paragraphs[0]
    p_ht.text = "Tribunals frequently place opposing party-appointed experts together in a single witness box, questioning them simultaneously to strip away partisan rhetoric and isolate genuine economic disagreements."
    p_ht.font.size = Pt(11)
    p_ht.font.color.rgb = C_TEXT_LIGHT
    p_ht.line_spacing = 1.2

    add_footer(s8, 8)

    # ==========================================
    # SLIDE 9: STRATEGIC CONTRACT DRAFTING & VECTOR ESCALATION FLOW
    # ==========================================
    s9 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s9)
    add_header(s9, "08. Risk Mitigation & Protocol", "Key Procedural & Drafting Safeguards",
               "Proactive contractual drafting determines whether a dispute is settled swiftly or devolves into protracted litigation.", logo_light)

    c_w = Inches(2.75)
    chk_cards = [
        ("Seat vs. Substantive Law", "Clearly separate substantive governing law from the arbitral seat. Confusing supervisory court jurisdiction is a critical drafting error.", Inches(0.8)),
        ("Express Confidentiality", "Never assume privacy is automatic. Explicitly specify confidentiality of documents, hearings, and pricing awards in the arbitration clause.", Inches(3.8)),
        ("Emergency Arbitrator", "Ensure institutional rules provide rapid emergency relief (within days) to preserve delivery flows and cash escrow during active proceedings.", Inches(6.8)),
        ("Retroactivity Limits", "Explicitly establish time limits for price review clawbacks and define applicable interest rates on retroactive balance settlements.", Inches(9.8))
    ]

    for title, desc, left in chk_cards:
        create_card(s9, left, Inches(1.6), c_w, Inches(2.1), title)
        tbox = s9.shapes.add_textbox(left + Inches(0.15), Inches(2.15), c_w - Inches(0.3), Inches(1.45))
        tf = tbox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = desc
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_TEXT_LIGHT
        p.line_spacing = 1.2

    # NATIVE PPTX VECTOR ESCALATION FLOW (Bottom Section)
    flow_steps = [
        ("Phase 01: Direct Talks", "C-Suite & Commercial Teams\nNotice of Price Review\nWindow: 30-60 Days", C_CARD_DARK, C_BORDER_SLATE),
        ("Phase 02: Mediation", "Neutral Evaluator / Expert\nJoint Valuation Assessment\nWindow: 45-90 Days", C_CARD_DARK, C_BORDER_SLATE),
        ("Phase 03: Emergency Relief", "Emergency Arbitrator\nInterim Supply & Escrow\nRelief Within 14 Days", C_CARD_HOVER, C_CYAN),
        ("Phase 04: Full Arbitration", "Tribunal Constitution\nQuantum & Netback Award\nFinal & Globally Enforceable", C_CARD_HOVER, C_BORDER_GOLD)
    ]

    box_w = Inches(2.75)
    for i, (f_title, f_desc, bg_col, bdr_col) in enumerate(flow_steps):
        bx = Inches(0.8) + i * Inches(3.0)
        card = create_card(s9, bx, Inches(4.0), box_w, Inches(2.75), bg_color=bg_col, border_color=bdr_col)
        
        # Step Badge Pill
        badge = s9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx + Inches(0.2), Inches(4.2), Inches(0.7), Inches(0.32))
        badge.fill.solid()
        badge.fill.fore_color.rgb = C_GOLD if i == 3 else C_BORDER_SLATE
        badge.line.color.rgb = C_BORDER_GOLD if i == 3 else C_BORDER_SLATE
        badge.text_frame.margin_left = badge.text_frame.margin_top = badge.text_frame.margin_right = badge.text_frame.margin_bottom = 0
        bp = badge.text_frame.paragraphs[0]
        bp.alignment = PP_ALIGN.CENTER
        bp.text = f"0{i+1}"
        bp.font.size = Pt(11)
        bp.font.bold = True
        bp.font.color.rgb = C_WHITE

        # Step Title & Desc
        tx_box = s9.shapes.add_textbox(bx + Inches(0.2), Inches(4.7), box_w - Inches(0.4), Inches(1.9))
        tf = tx_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p_t = tf.paragraphs[0]
        p_t.text = f_title
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(13)
        p_t.font.bold = True
        p_t.font.color.rgb = C_GOLD_LIGHT if i == 3 else C_WHITE
        p_t.space_after = Pt(8)

        p_d = tf.add_paragraph()
        p_d.text = f_desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(10.5)
        p_d.font.color.rgb = C_TEXT_LIGHT
        p_d.line_spacing = 1.25

        # Right arrow connector
        if i < 3:
            arr = s9.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, bx + Inches(2.78), Inches(5.1), Inches(0.18), Inches(0.25))
            arr.fill.solid()
            arr.fill.fore_color.rgb = C_GOLD
            arr.line.color.rgb = C_GOLD

    add_footer(s9, 9)

    # ==========================================
    # SLIDE 10: EMERGING HORIZONS (2026+)
    # ==========================================
    s10 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s10)
    add_header(s10, "09. Future Outlook", "Emerging Horizons in Gas Dispute Resolution",
               "Decarbonization, geopolitical sanctions, and portfolio LNG trading are reshaping the dispute landscape.", logo_light)

    cols_data = [
        ("The Energy Transition & Stranded Assets",
         "Decarbonization Commitments",
         "• Declining Power Demand: Shift to renewables reduces long-term baseload gas demand, triggering buyer hardship claims.\n\n• Carbon Pricing Mechanisms: Escalating ETS and border carbon adjustments (CBAM) disrupt traditional netback economics.\n\n• Contract Renegotiation: Legacy 20-year contracts are increasingly challenged as stranded assets or commercially frustrated.",
         Inches(0.8)),
        ("Sanctions & Geopolitical Force Majeure",
         "Sovereign & Regulatory Friction",
         "• Export Bans & Pipeline Cuts: Geopolitical sanctions abruptly halt physical flows and freeze cross-border banking rails.\n\n• Force Majeure Testing: Tribunals face unprecedented claims evaluating whether state sanctions constitute genuine contractual force majeure.\n\n• Award Enforcement Hurdles: Heightened scrutiny under public policy exceptions when enforcing awards involving sanctioned entities.",
         Inches(4.8)),
        ("Rise of Flexible Portfolio LNG",
         "Market Liquidity Evolution",
         "• Short-Term & Spot Contracting: Transition from 20-year bilateral pipeline pacts to 1-3 year flexible cargo portfolios.\n\n• Cargo Scheduling Conflicts: Volatile spot spikes create disputes over loading windows, cancellations, and boil-off liabilities.\n\n• New Pricing Formulas: Hybrid pricing pegged to Brent, TTF, and JKM requires sophisticated multi-hub econometric arbitration.",
         Inches(8.8))
    ]

    for title, subtitle, desc, left in cols_data:
        create_card(s10, left, Inches(1.6), Inches(3.7), Inches(5.1), title)
        tbox = s10.shapes.add_textbox(left + Inches(0.2), Inches(2.3), Inches(3.3), Inches(4.2))
        tf = tbox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p_sub = tf.paragraphs[0]
        p_sub.text = subtitle.upper()
        p_sub.font.size = Pt(10)
        p_sub.font.bold = True
        p_sub.font.color.rgb = C_CYAN
        p_sub.space_after = Pt(10)

        p_desc = tf.add_paragraph()
        p_desc.text = desc
        p_desc.font.size = Pt(11)
        p_desc.font.color.rgb = C_TEXT_LIGHT
        p_desc.line_spacing = 1.25

    add_footer(s10, 10)

    # ==========================================
    # SLIDE 11: ABOUT THE ARBITRATOR
    # ==========================================
    s11 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s11)
    add_header(s11, "10. Arbitrator Profile", "Harshavardhan Sancheti | International Arbitrator",
               "Triple-qualified independent arbitrator experienced in high-stakes energy, infrastructure, and commercial disputes.", logo_light)

    create_card(s11, Inches(0.8), Inches(1.6), Inches(6.0), Inches(5.1), "Professional Qualifications & Track Record", bg_color=C_CARD_DARK)
    tbox_bio = s11.shapes.add_textbox(Inches(1.05), Inches(2.2), Inches(5.5), Inches(4.3))
    tf_b = tbox_bio.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0

    p = tf_b.paragraphs[0]
    p.text = "• Triple-Qualified Legal Practitioner: Admitted to practice in the United States (New York Bar, District of Columbia Bar), England & Wales (Solicitor), and India (Advocate)."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_LIGHT
    p.space_after = Pt(8)

    p = tf_b.add_paragraph()
    p.text = "• Elite Institutional Background: Former Special Legal Consultant at the International Centre for Settlement of Investment Disputes (ICSID) at the World Bank Group in Washington D.C."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_LIGHT
    p.space_after = Pt(8)

    p = tf_b.add_paragraph()
    p.text = "• High-Value Energy & Gas Exposure: Extensive background in multi-billion dollar cross-border disputes, including national gas pipeline concessions, PSC cost recovery, and long-term supply arbitrations."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_LIGHT
    p.space_after = Pt(8)

    p = tf_b.add_paragraph()
    p.text = "• Institutional Appointments: Accepted as sole arbitrator, co-arbitrator, and tribunal member across proceedings in London, New York, Geneva, and India under ICC, LCIA, SIAC, and UNCITRAL rules."
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_LIGHT

    create_card(s11, Inches(7.1), Inches(1.6), Inches(5.4), Inches(2.4), "Core Energy Industry Competencies")
    tbox_r1 = s11.shapes.add_textbox(Inches(7.35), Inches(2.2), Inches(4.9), Inches(1.7))
    tf_r1 = tbox_r1.text_frame
    tf_r1.word_wrap = True
    tf_r1.margin_left = tf_r1.margin_top = tf_r1.margin_right = tf_r1.margin_bottom = 0
    p = tf_r1.paragraphs[0]
    p.text = "✓ Gas & LNG Sale and Purchase Agreements (SPAs)\n✓ Take-or-Pay volume shortfalls & force majeure claims\n✓ Formula price review reopeners & hub-netback valuation\n✓ Upstream PSCs, Joint Operating Agreements (JOAs) & transit"
    p.font.size = Pt(11.5)
    p.font.color.rgb = C_TEXT_LIGHT
    p.line_spacing = 1.3

    create_card(s11, Inches(7.1), Inches(4.3), Inches(5.4), Inches(2.4), "Why Parties Appoint Harshavardhan Sancheti", bg_color=C_CARD_HOVER, border_color=C_BORDER_GOLD)
    tbox_r2 = s11.shapes.add_textbox(Inches(7.35), Inches(4.9), Inches(4.9), Inches(1.7))
    tf_r2 = tbox_r2.text_frame
    tf_r2.word_wrap = True
    tf_r2.margin_left = tf_r2.margin_top = tf_r2.margin_right = tf_r2.margin_bottom = 0
    p = tf_r2.paragraphs[0]
    p.text = "Unites civil law and common law procedural mastery with deep fluency in complex econometric modeling. Provides robust, enforceable awards under the New York Convention without procedural delays."
    p.font.size = Pt(12)
    p.font.color.rgb = C_TEXT_LIGHT
    p.line_spacing = 1.3

    add_footer(s11, 11)

    # ==========================================
    # SLIDE 12: GLOBAL DIRECTORY & CONTACT (CTA)
    # ==========================================
    s12 = prs.slides.add_slide(blank_slide_layout)
    set_slide_background(s12)
    add_header(s12, "11. Connect & Appoint", "Global Presence & Direct Contact Information",
               "Available for arbitrator appointments, panel nominations, and confidential inquiries across primary global seats.", logo_light)

    offices = [
        ("United Kingdom", "17 Falmouth House, Clarendon Place\nLondon W2 2NT, UK\n\nDirect: +44 7471 190790", Inches(0.8)),
        ("United States", "1452 Highwood Drive\nMcLean, VA 22101, USA\n\nWashington D.C. / New York Seats", Inches(3.8)),
        ("Switzerland", "Junker Strasse CH-8238\nBüsingen, Schaffhausen\n\nGeneva / Zurich Arbitration Seats", Inches(6.8)),
        ("India", "Aditya Ranjana Apts, Gagan Mahal\nLower Tank Bund Road, Hyderabad\n\nDirect: +91 82503 80218", Inches(9.8))
    ]

    for country, addr, left in offices:
        create_card(s12, left, Inches(1.6), Inches(2.75), Inches(2.4), country)
        tbox = s12.shapes.add_textbox(left + Inches(0.15), Inches(2.2), Inches(2.45), Inches(1.7))
        tf = tbox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = addr
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_TEXT_LIGHT
        p.line_spacing = 1.2

    create_card(s12, Inches(0.8), Inches(4.3), Inches(11.733), Inches(2.4), "Appointment Inquiries & Institutional Nominations", bg_color=C_CARD_HOVER, border_color=C_BORDER_GOLD)
    tbox_bot = s12.shapes.add_textbox(Inches(1.1), Inches(4.9), Inches(11.1), Inches(1.6))
    tf_b = tbox_bot.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0

    p1 = tf_b.paragraphs[0]
    p1.text = "Direct Communications & Conflicts Checking:"
    p1.font.size = Pt(12)
    p1.font.bold = True
    p1.font.color.rgb = C_GOLD_LIGHT
    p1.space_after = Pt(4)

    p2 = tf_b.add_paragraph()
    p2.text = "• Primary Email: info@theinternationalarbitrator.com  |  Direct: hvs@theinternationalarbitrator.com\n• Website & Inquiry Portal: www.theinternationalarbitrator.com/contact-us/\n• Global Telephone: +44 7471 190790 (London)  /  +91 82503 80218 (India)"
    p2.font.size = Pt(11.5)
    p2.font.color.rgb = C_WHITE
    p2.space_after = Pt(8)

    p3 = tf_b.add_paragraph()
    p3.text = "All appointment inquiries and conflict checks are reviewed personally by Mr. Sancheti's office with confirmation within one business day."
    p3.font.size = Pt(10.5)
    p3.font.color.rgb = C_TEXT_MUTED

    add_footer(s12, 12)

    out_path = 'data/content for PPT/Gas_Price_Disputes_and_Arbitration_Presentation.pptx'
    prs.save(out_path)
    print(f"Presentation saved successfully to {out_path}")

if __name__ == '__main__':
    build_presentation()
