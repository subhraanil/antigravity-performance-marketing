import openpyxl

excel_path = r'data/fabb6/Historic Data and Forecast.xlsx'
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb.active

print("=== AUDITING PLAN A (CPA & ROAS Improvement) (Rows 32-37) ===")
for r in range(32, 38):
    m_name = ws.cell(row=r, column=1).value
    tot_ord = ws.cell(row=r, column=2).value
    tot_rev = ws.cell(row=r, column=3).value
    org_ret = ws.cell(row=r, column=4).value
    aov_tot = ws.cell(row=r, column=5).value
    roas_tot = ws.cell(row=r, column=6).value
    
    g_ord = ws.cell(row=r, column=7).value
    g_rev = ws.cell(row=r, column=8).value
    g_bud = ws.cell(row=r, column=9).value
    g_cpa = ws.cell(row=r, column=10).value
    g_aov = ws.cell(row=r, column=11).value
    g_roas = ws.cell(row=r, column=12).value
    
    m_ord = ws.cell(row=r, column=13).value
    m_rev = ws.cell(row=r, column=14).value
    m_bud = ws.cell(row=r, column=15).value
    m_cpa = ws.cell(row=r, column=16).value
    m_aov = ws.cell(row=r, column=17).value
    m_roas = ws.cell(row=r, column=18).value
    
    p_ord = ws.cell(row=r, column=19).value
    p_rev = ws.cell(row=r, column=20).value
    p_bud = ws.cell(row=r, column=21).value
    p_cpa = ws.cell(row=r, column=22).value
    p_roas = ws.cell(row=r, column=23).value
    d_avg = ws.cell(row=r, column=24).value
    
    # Verifications
    c1 = (p_ord == g_ord + m_ord)
    c2 = (org_ret == tot_ord - p_ord)
    c3 = (p_rev == g_rev + m_rev)
    c4 = (p_bud == g_bud + m_bud)
    c5 = abs(p_cpa - (p_bud / p_ord)) < 0.01
    c6 = abs(roas_tot - (tot_rev / p_bud)) < 0.01
    c7 = abs(p_roas - (p_rev / p_bud)) < 0.01
    
    print(f"Row {r} ({m_name}): PaidOrd Check={c1}, OrgRet Check={c2}, PaidRev Check={c3}, PaidBud Check={c4}, CPA Check={c5}, TotalROAS Check={c6}, PaidROAS Check={c7}")

print("\n=== AUDITING PLAN B (Scale Target Model) (Rows 41-46) ===")
for r in range(41, 47):
    m_name = ws.cell(row=r, column=1).value
    tot_ord = ws.cell(row=r, column=2).value
    tot_rev = ws.cell(row=r, column=3).value
    org_ret = ws.cell(row=r, column=4).value
    aov_tot = ws.cell(row=r, column=5).value
    roas_tot = ws.cell(row=r, column=6).value
    
    g_ord = ws.cell(row=r, column=7).value
    g_rev = ws.cell(row=r, column=8).value
    g_bud = ws.cell(row=r, column=9).value
    g_cpa = ws.cell(row=r, column=10).value
    g_aov = ws.cell(row=r, column=11).value
    g_roas = ws.cell(row=r, column=12).value
    
    m_ord = ws.cell(row=r, column=13).value
    m_rev = ws.cell(row=r, column=14).value
    m_bud = ws.cell(row=r, column=15).value
    m_cpa = ws.cell(row=r, column=16).value
    m_aov = ws.cell(row=r, column=17).value
    m_roas = ws.cell(row=r, column=18).value
    
    p_ord = ws.cell(row=r, column=19).value
    p_rev = ws.cell(row=r, column=20).value
    p_bud = ws.cell(row=r, column=21).value
    p_cpa = ws.cell(row=r, column=22).value
    p_roas = ws.cell(row=r, column=23).value
    d_avg = ws.cell(row=r, column=24).value
    
    # Verifications
    c1 = (p_ord == g_ord + m_ord)
    c2 = (org_ret == tot_ord - p_ord)
    c3 = (p_rev == g_rev + m_rev)
    c4 = (p_bud == g_bud + m_bud)
    c5 = abs(p_cpa - (p_bud / p_ord)) < 0.01
    c6 = abs(roas_tot - (tot_rev / p_bud)) < 0.01
    c7 = abs(p_roas - (p_rev / p_bud)) < 0.01
    
    print(f"Row {r} ({m_name}): PaidOrd Check={c1}, OrgRet Check={c2}, PaidRev Check={c3}, PaidBud Check={c4}, CPA Check={c5}, TotalROAS Check={c6}, PaidROAS Check={c7}")
