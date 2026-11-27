import os
import shutil

excel_script_path = r"C:\Users\test\Videos\Office\scripts\build_formula_driven_master_excel.py"
with open(excel_script_path, "r", encoding="utf-8") as f:
    text = f.read()

# Let's find Section 3 and update it
old_marker = '# Section 3: Retention & Payback Note'
idx = text.find(old_marker)
if idx != -1:
    end_idx = text.find('col_w_1 = [', idx)
    new_sec3_block = '''    # Section 3: Month-Wise Media Budget Allocation by Channel & Strategy
    sub_navy_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    ws1.cell(row=17, column=1, value="3. Month-Wise Media Budget Allocation by Channel & Strategy (Dec 2026 – Feb 2027)").font = section_font
    m_headers = ["Planning Horizon / Month", "Plan 1: Base (Google / Meta / Total)", "Plan 2: Recommended (Google / Meta / Total)", "Plan 3: Aggressive (Google / Meta / Total)"]
    for c_idx, h in enumerate(m_headers):
        cell = ws1.cell(row=18, column=c_idx+1, value=h)
        cell.fill = sub_navy_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = thin_border

    m_rows = [
        ["December 2026", "₹12.40L / ₹7.60L (Total: ₹20.00L)", "₹16.00L / ₹10.00L (Total: ₹26.00L)", "₹19.20L / ₹10.80L (Total: ₹30.00L)"],
        ["January 2027", "₹15.00L / ₹9.00L (Total: ₹24.00L)", "₹20.00L / ₹11.00L (Total: ₹31.00L)", "₹24.50L / ₹13.50L (Total: ₹38.00L)"],
        ["February 2027", "₹16.10L / ₹9.90L (Total: ₹26.00L)", "₹22.00L / ₹12.10L (Total: ₹34.10L)", "₹28.80L / ₹15.70L (Total: ₹44.50L)"],
        ["Total Q1 Allocation", "₹43.50L / ₹26.50L (Total: ₹70.00L)", "₹58.00L / ₹33.10L (Total: ₹91.10L)", "₹72.50L / ₹40.00L (Total: ₹112.50L)"]
    ]

    for r_idx, r_vals in enumerate(m_rows):
        curr_r = 19 + r_idx
        for c_idx, val in enumerate(r_vals):
            cell = ws1.cell(row=curr_r, column=c_idx+1, value=val)
            cell.border = thin_border
            is_tot = (r_idx == len(m_rows) - 1)
            cell.font = body_font_bold if (is_tot or c_idx == 0) else body_font
            cell.alignment = Alignment(horizontal="center" if c_idx > 0 else "left", vertical="center")
            if is_tot: cell.fill = total_fill
            elif r_idx % 2 == 1: cell.fill = zebra_fill

    # Section 4: Retention & Payback Note
    ws1.cell(row=24, column=1, value="4. Zero Incremental Media Spend Retention Engine & LTV Replenishment Economics").font = section_font
    payback_note = "Repeat retention is driven primarily by automated WhatsApp and email replenishment workflows timed to hair spa, shampoo, and color usage cycles (30, 45, and 60 days). While retention software and messaging incurs operational costs (~₹35,000–₹50,000/month), it requires zero incremental media spend. This zero-media-cost retention engine unlocks 9,954 'Orders from Others' in Plan 2 (31.5% of total store volume), driving blended spend per store order down to ₹288.53 and elevating account efficiency from a 2.68x paid ROAS to a 3.91x blended store ROAS. First-order media deficits are fully recovered as customers replenish over their 60–180 day salon care usage cycle."
    ws1.merge_cells("A25:K27")
    cell_pn = ws1.cell(row=25, column=1, value=payback_note)
    cell_pn.font = Font(name=font_name, size=9.0, italic=True, color="333333")
    cell_pn.alignment = Alignment(wrap_text=True, vertical="top")
    cell_pn.fill = accent_fill

    '''
    text = text[:idx] + new_sec3_block + text[end_idx:]
    with open(excel_script_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Successfully patched build_formula_driven_master_excel.py")
else:
    print("old_marker not found in text")
