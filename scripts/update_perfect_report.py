import os
import shutil
import pypdf

def update_report_script():
    src_file = r'C:\Users\test\Videos\Office\scripts\build_perfect_report.py'
    with open(src_file, 'r', encoding='utf-8') as f:
        code = f.read()

    # 1. Update Executive summary on Page 1
    old_p1_text = 'on a planned ad spend of \u20b991.1 Lakhs, the Recommended Plan delivers \u20b93.56 Cr of Gross Sales (3.91x blended Gross ROAS; \u20b92.85 Cr net @ 80% realization) across 31,574 store orders (\u20b9288.53 spend per store order). The plan is powered by 21,621 paid ad orders (2.68x Paid ROAS) and 9,954 orders from others (31.5% of total volume) driven by automated WhatsApp and email replenishment workflows at zero incremental media spend. Flanked by Base Plan (\u20b970.0L / \u20b92.87 Cr / 25,488 orders) and Aggressive Plan (\u20b9112.5L / \u20b94.17 Cr / 36,871 orders).'
    new_p1_text = 'The Recommended Plan paces media spend from \u20b930.00L in December to \u20b935.00L in January and \u20b940.00L in February, delivering confirmed Gross Sales of \u20b993.06L (3.10x ROAS), \u20b9121.25L (3.46x ROAS), and \u20b9164.42L (4.11x ROAS) across 9,178, 10,992, and 13,346 monthly store orders. The plan is powered by front-end paid acquisition (6,082, 7,680, and 9,801 monthly orders) and low-cost retention flows (3,096, 3,313, and 3,545 monthly orders) driven by GoKwik and automated WhatsApp/email replenishment workflows at zero incremental media spend. Flanked by a Moderate Plan (Dec \u20b935L, Jan \u20b941L, Feb \u20b947L) and an Aggressive Plan (Dec \u20b940L, Jan \u20b948L, Feb \u20b955L).'
    assert old_p1_text in code, "old_p1_text not found"
    code = code.replace(old_p1_text, new_p1_text)

    # 2. Update Section 7.1 text
    old_71_text = 'Planned spend follows the agreed ramp: \u20b926.0L in December, \u20b931.0L in January and \u20b934.1L in February (\u20b991.1L in total). Performance is powered by dual revenue engines: front-end paid acquisition (21,621 orders @ 2.68x Paid ROAS) and zero-incremental-media-cost retention flows (9,954 orders from others), generating a combined 3.91x Store ROAS.'
    new_71_text = 'Planned spend follows the official model: \u20b930.00L in December, \u20b935.00L in January, and \u20b940.00L in February. Performance is powered by dual revenue engines: front-end paid acquisition (6,082, 7,680, and 9,801 monthly orders) and zero-incremental-media-cost retention flows (3,096, 3,313, and 3,545 monthly orders from others), driving monthly Store ROAS from 3.10x to 3.46x and 4.11x.'
    assert old_71_text in code, "old_71_text not found"
    code = code.replace(old_71_text, new_71_text)

    # 3. Update Section 7.2 table
    old_base_table = '''    base_table_data = [
        ["Month", "Total Ad Spend", "Google Spend", "Meta Spend", "Paid Orders", "Orders from Others*", "Total Store Orders", "Gross Sales Revenue", "Spend / Store Order", "Confirmed Gross ROAS"],
        ["Dec 2026", "₹26.00L", "₹16.00L", "₹10.00L", "5,778", "3,096", "8,874", "₹89.98L", "₹293.00", "3.46x"],
        ["Jan 2027", "₹31.00L", "₹20.00L", "₹11.00L", "7,334", "3,313", "10,647", "₹117.43L (~₹1.17 Cr)", "₹291.17", "3.79x"],
        ["Feb 2027", "₹34.10L", "₹22.00L", "₹12.10L", "8,509", "3,545", "12,053", "₹148.50L (~₹1.48 Cr)", "₹282.91", "4.35x"],
        ["Total Q1", "₹91.10L", "₹58.00L", "₹33.10L", "21,621", "9,954", "31,574", "₹355.91L (~₹3.56 Cr)", "₹288.53", "3.91x"]
    ]'''

    new_base_table = '''    base_table_data = [
        ["Month", "Total Ad Spend", "Google Spend", "Meta Spend", "Paid Orders", "Orders from Others*", "Total Store Orders", "Gross Sales Revenue", "Spend / Store Order", "Confirmed Gross ROAS"],
        ["Dec 2026", "₹30.00L", "₹19.00L", "₹11.00L", "6,082", "3,096", "9,178", "₹93.06L", "₹326.87", "3.10x"],
        ["Jan 2027", "₹35.00L", "₹22.00L", "₹13.00L", "7,680", "3,313", "10,992", "₹121.25L (~₹1.21 Cr)", "₹318.40", "3.46x"],
        ["Feb 2027", "₹40.00L", "₹25.00L", "₹15.00L", "9,801", "3,545", "13,346", "₹164.42L (~₹1.64 Cr)", "₹299.72", "4.11x"]
    ]'''
    assert old_base_table in code, "old_base_table not found"
    code = code.replace(old_base_table, new_base_table)

    old_72_body = 'Spend per total store order averages \u20b9288.53 across Q1 (\u20b9293 in Dec to \u20b9283 in Feb). With 25% wholesale gross margin on ex-GST product value, media break-even is 4.00x on ex-GST revenue, or 4.72x on GST-inclusive total receipts / Shopify Gross Sales. Repeat replenishment workflows drive 31.5% of store orders at zero incremental media spend.'
    new_72_body = 'Spend per total store order improves from \u20b9326.87 in Dec to \u20b9318.40 in Jan and \u20b9299.72 in Feb. With 25% wholesale gross margin on ex-GST product value, media break-even is 4.00x on ex-GST revenue, or 4.72x on GST-inclusive total receipts / Shopify Gross Sales. Repeat replenishment workflows drive 3,096 to 3,545 monthly store orders at zero incremental media spend.'
    assert old_72_body in code, "old_72_body not found"
    code = code.replace(old_72_body, new_72_body)

    # 4. Update Section 7.3 table
    old_scen_table = '''    scen_table_data = [
        ["Scenario", "Dec Spend", "Jan Spend", "Feb Spend", "Total Spend", "Gross ROAS", "Gross Sales", "Paid Orders", "Orders Others*", "Total Orders", "Spend / Order"],
        ["Plan 1: Base", "₹20.0L", "₹24.0L", "₹26.0L", "₹70.0L", "4.10x flat", "₹287.2L (~₹2.87 Cr)", "17,129", "8,359", "25,488", "₹274.64"],
        ["Plan 2: Recommended", "₹26.0L", "₹31.0L", "₹34.1L", "₹91.1L", "3.46x / 3.79x / 4.35x", "₹355.9L (~₹3.56 Cr)", "21,621", "9,954", "31,574", "₹288.53"],
        ["Plan 3: Aggressive", "₹30.0L", "₹38.0L", "₹44.5L", "₹112.5L", "3.33x / 3.59x / 4.06x", "₹416.8L (~₹4.17 Cr)", "25,833", "11,038", "36,871", "₹305.12"]
    ]'''

    new_scen_table = '''    scen_table_data = [
        ["Strategic Plan", "Month", "Ad Budget", "Google / Meta", "Paid Orders", "Others*", "Store Orders", "Gross Sales", "Store ROAS"],
        ["Plan 1: Recommended", "Dec 2026", "₹30.00L", "₹19.0L / ₹11.0L", "6,082", "3,096", "9,178", "₹93.06L", "3.10x"],
        ["Plan 1: Recommended", "Jan 2027", "₹35.00L", "₹22.0L / ₹13.0L", "7,680", "3,313", "10,992", "₹121.25L", "3.46x"],
        ["Plan 1: Recommended", "Feb 2027", "₹40.00L", "₹25.0L / ₹15.0L", "9,801", "3,545", "13,346", "₹164.42L", "4.11x"],
        ["Plan 2: Moderate", "Dec 2026", "₹35.00L", "₹22.0L / ₹13.0L", "6,950", "3,096", "10,046", "₹103.50L", "2.96x"],
        ["Plan 2: Moderate", "Jan 2027", "₹41.00L", "₹26.0L / ₹15.0L", "8,800", "3,313", "12,113", "₹136.50L", "3.33x"],
        ["Plan 2: Moderate", "Feb 2027", "₹47.00L", "₹29.5L / ₹17.5L", "11,250", "3,545", "14,795", "₹184.20L", "3.92x"],
        ["Plan 3: Aggressive", "Dec 2026", "₹40.00L", "₹25.0L / ₹15.0L", "7,750", "3,096", "10,846", "₹113.20L", "2.83x"],
        ["Plan 3: Aggressive", "Jan 2027", "₹48.00L", "₹30.5L / ₹17.5L", "10,050", "3,313", "13,363", "₹151.20L", "3.15x"],
        ["Plan 3: Aggressive", "Feb 2027", "₹55.00L", "₹34.5L / ₹20.5L", "12,850", "3,545", "16,395", "₹204.50L", "3.72x"]
    ]'''
    assert old_scen_table in code, "old_scen_table not found"
    code = code.replace(old_scen_table, new_scen_table)

    old_scen_body = 'Plan 1 is the defensive baseline. Moving from Plan 1 to Plan 2 invests an incremental \u20b921.10L in media to generate \u20b968.70L in gross sales (3.26x marginal ROAS, acquiring 6,086 incremental store orders at \u20b9346.70 spend/order). Moving from Plan 2 to Plan 3 adds \u20b921.40L in media spend for \u20b960.92L gross sales (2.85x marginal ROAS, acquiring 5,297 incremental orders at \u20b9404.00 spend/order).'
    new_scen_body = 'Moving from Recommended to Moderate commits \u20b95.0L to \u20b97.0L additional monthly spend, capturing 868 to 1,449 incremental orders. Moving from Moderate to Aggressive commits \u20b95.0L to \u20b98.0L further monthly spend for 800 to 1,600 incremental orders, reflecting normal diminishing marginal returns.'
    assert old_scen_body in code, "old_scen_body not found"
    code = code.replace(old_scen_body, new_scen_body)

    # 5. Update Section 7.4 channel guardrails table (remove Total row)
    old_chan_table = '''    chan_table_data = [
        ["Month", "Google spend (64%)", "Google CPA target", "Google orders", "Meta spend (36%)", "Meta CPA target", "Meta orders", "Combined paid orders"],
        ["Dec 2026", "₹16.00L (61.5%)", "₹450.00", "3,556", "₹10.00L (38.5%)", "₹450.00", "2,222", "5,778"],
        ["Jan 2027", "₹20.00L (64.5%)", "₹430.00", "4,651", "₹11.00L (35.5%)", "₹410.00", "2,683", "7,334"],
        ["Feb 2027", "₹22.00L (64.5%)", "₹410.00", "5,366", "₹12.10L (35.5%)", "₹385.00", "3,143", "8,509"],
        ["Total", "₹58.00L", "₹427.32", "13,573", "₹33.10L", "₹411.28", "8,048", "21,621"]
    ]'''

    new_chan_table = '''    chan_table_data = [
        ["Month", "Google Spend (63%)", "Google CPA Target", "Google Orders", "Meta Spend (37%)", "Meta CPA Target", "Meta Orders", "Combined Paid Orders"],
        ["Dec 2026", "₹19.00L (63.3%)", "₹480.00", "3,958", "₹11.00L (36.7%)", "₹518.00", "2,124", "6,082"],
        ["Jan 2027", "₹22.00L (62.9%)", "₹451.00", "4,878", "₹13.00L (37.1%)", "₹464.00", "2,802", "7,680"],
        ["Feb 2027", "₹25.00L (62.5%)", "₹407.00", "6,143", "₹15.00L (37.5%)", "₹410.00", "3,659", "9,801"]
    ]'''
    assert old_chan_table in code, "old_chan_table not found"
    code = code.replace(old_chan_table, new_chan_table)

    old_chan_body = 'Paid orders represent 68.5% of total store orders across Q1. Paid CPA improves by 4% monthly in Google (\u20b9450 \u2192 \u20b9410) and Meta (\u20b9450 \u2192 \u20b9385). Three distinct CPA metrics govern execution: (1) Spend per Store Order (Blended CPA, \u20b9283\u2013\u20b9293): Primary business KPI; (2) Platform Paid CPA (Google \u20b9410\u2013\u20b9450, Meta \u20b9385\u2013\u20b9450): Operational check; (3) Bidding CPA Ceilings: Algorithm caps.'
    new_chan_body = 'Paid orders represent 66% to 73% of monthly store orders. Paid CPA improves monthly in Google (\u20b9480 \u2192 \u20b9407) and Meta (\u20b9518 \u2192 \u20b9410). Three distinct CPA metrics govern execution: (1) Spend per Store Order (Blended CPA, \u20b9299\u2013\u20b9327): Primary business KPI; (2) Platform Paid CPA (Google \u20b9407\u2013\u20b9480, Meta \u20b9410\u2013\u20b9518): Operational check; (3) Bidding CPA Ceilings: Algorithm caps.'
    assert old_chan_body in code, "old_chan_body not found"
    code = code.replace(old_chan_body, new_chan_body)

    # 6. Update Section 7.5 bullet
    old_75_bullet = 'Orders from Others compounds at +7% monthly in Plan 2 (3,096 in Dec, 3,313 in Jan, 3,545 in Feb; Total 9,954 orders), representing repeat buyers and organic traffic.'
    new_75_bullet = 'Orders from Others compounds at +7% monthly in Recommended Plan (3,096 in Dec, 3,313 in Jan, 3,545 in Feb), representing repeat buyers and organic traffic.'
    assert old_75_bullet in code, "old_75_bullet not found"
    code = code.replace(old_75_bullet, new_75_bullet)

    with open(src_file, 'w', encoding='utf-8') as f:
        f.write(code)

    print('Updated build_perfect_report.py successfully.')

if __name__ == '__main__':
    update_report_script()
