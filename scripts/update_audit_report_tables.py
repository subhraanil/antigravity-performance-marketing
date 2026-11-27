import os
import shutil
import pypdf

def update_audit_report():
    src_file = r'C:\Users\test\Videos\Office\scripts\build_perfect_report.py'
    with open(src_file, 'r', encoding='utf-8') as f:
        code = f.read()

    old_sec_73_block = '''    # ==================== PAGE 7 ====================
    add_h2("7.3 Scenarios (Sensitivities on Gross & Net Realization)", page_break_before=True)
    scen_table_data = [
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
    ]
    create_styled_table(doc, scen_table_data, header_bg="102C57", center_cols=[1, 2, 4, 5, 6, 7, 8], right_cols=[3])
    add_body("Moving from Recommended to Moderate commits ₹5.0L to ₹7.0L additional monthly spend, capturing 868 to 1,449 incremental orders. Moving from Moderate to Aggressive commits ₹5.0L to ₹8.0L further monthly spend for 800 to 1,600 incremental orders, reflecting normal diminishing marginal returns.")'''

    new_sec_73_block = '''    # ==================== PAGE 7 ====================
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
    create_styled_table(doc, p3_data, header_bg="203764", center_cols=[0, 1, 2, 3, 4, 5, 7], right_cols=[6], col_widths=col_w_8_rep)'''

    assert old_sec_73_block in code, "old_sec_73_block not found"
    code = code.replace(old_sec_73_block, new_sec_73_block)

    with open(src_file, 'w', encoding='utf-8') as f:
        f.write(code)

    print("Updated build_perfect_report.py with 3 separate tables successfully.")

if __name__ == '__main__':
    update_audit_report()
