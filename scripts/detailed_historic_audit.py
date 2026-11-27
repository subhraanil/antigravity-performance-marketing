import openpyxl

excel_path = r'data/fabb6/Historic Data and Forecast.xlsx'
wb = openpyxl.load_workbook(excel_path, data_only=True)
ws = wb.active

print("=== HISTORIC DATA VERIFICATION (Rows 19-27) ===")
for r in range(19, 28):
    m = ws.cell(row=r, column=1).value
    ord_shp = ws.cell(row=r, column=2).value
    rev_shp = ws.cell(row=r, column=3).value
    ret_rate = ws.cell(row=r, column=4).value
    aov_shp = ws.cell(row=r, column=5).value
    
    g_ord = ws.cell(row=r, column=7).value
    g_rev = ws.cell(row=r, column=8).value
    g_bud = ws.cell(row=r, column=9).value
    g_cpa = ws.cell(row=r, column=10).value
    g_roas = ws.cell(row=r, column=12).value
    
    m_ord = ws.cell(row=r, column=13).value
    m_rev = ws.cell(row=r, column=14).value
    m_bud = ws.cell(row=r, column=15).value
    m_cpa = ws.cell(row=r, column=16).value
    m_roas = ws.cell(row=r, column=18).value
    
    p_ord = ws.cell(row=r, column=19).value
    p_rev = ws.cell(row=r, column=20).value
    p_bud = ws.cell(row=r, column=21).value
    p_cpa = ws.cell(row=r, column=22).value
    p_roas = ws.cell(row=r, column=23).value
    
    print(f"{m}: Shopify {ord_shp} ord (INR {rev_shp:,.2f}) | Google {g_ord:.1f} ord, INR {g_bud:,.2f} spend, CPA INR {g_cpa:.2f}, ROAS {g_roas:.2f}x | Meta {m_ord:.1f} ord, INR {m_bud:,.2f} spend, CPA INR {m_cpa:.2f}, ROAS {m_roas:.2f}x | Paid Total: {p_ord:.1f} ord, CPA INR {p_cpa:.2f}, ROAS {p_roas:.2f}x")

print("\nRow 28 Note:", ws.cell(row=28, column=1).value)
