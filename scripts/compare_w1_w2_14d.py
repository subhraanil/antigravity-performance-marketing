import openpyxl

f_14d = r"data/Pet Mode/Search terms report.xlsx"
f_7d = r"data/Pet Mode/Search terms report (1).xlsx"

# Load 14d
wb_14 = openpyxl.load_workbook(f_14d, data_only=True)
ws_14 = wb_14.active
r_14 = list(ws_14.iter_rows(values_only=True))

# Load 7d
wb_7 = openpyxl.load_workbook(f_7d, data_only=True)
ws_7 = wb_7.active
r_7 = list(ws_7.iter_rows(values_only=True))

def get_totals(rows):
    res = {}
    for r in rows:
        if r[0] and isinstance(r[0], str) and r[0].startswith("Total:"):
            res[r[0]] = {
                'clicks': float(r[5]) if r[5] != '--' and r[5] is not None else 0,
                'impr': float(r[6]) if r[6] != '--' and r[6] is not None else 0,
                'ctr': float(r[7]) if r[7] != '--' and r[7] is not None else 0,
                'cpc': float(r[9]) if r[9] != '--' and r[9] is not None else 0,
                'cost': float(r[10]) if r[10] != '--' and r[10] is not None else 0,
                'conv_rate': float(r[12]) if r[12] != '--' and r[12] is not None else 0,
                'conv': float(r[13]) if r[13] != '--' and r[13] is not None else 0,
                'cpa': float(r[14]) if r[14] != '--' and r[14] is not None else 0,
            }
    return res

tot_14 = get_totals(r_14)
tot_7 = get_totals(r_7)

# Calculate Week 1 (Oct 8 - Oct 14) by difference: 14d - 7d
# Note: PMax attribution can shift slightly, but this gives the exact differential
tot_w1 = {}
for k in tot_14:
    if k in tot_7:
        c14 = tot_14[k]['cost']
        c7 = tot_7[k]['cost']
        cl14 = tot_14[k]['clicks']
        cl7 = tot_7[k]['clicks']
        im14 = tot_14[k]['impr']
        im7 = tot_7[k]['impr']
        co14 = tot_14[k]['conv']
        co7 = tot_7[k]['conv']
        
        diff_cost = c14 - c7
        diff_cl = cl14 - cl7
        diff_im = im14 - im7
        diff_conv = co14 - co7
        
        diff_cpc = diff_cost / diff_cl if diff_cl > 0 else 0
        diff_ctr = diff_cl / diff_im if diff_im > 0 else 0
        diff_cpa = diff_cost / diff_conv if diff_conv > 0 else 0
        diff_cr = diff_conv / diff_cl if diff_cl > 0 else 0
        
        tot_w1[k] = {
            'clicks': diff_cl,
            'impr': diff_im,
            'ctr': diff_ctr,
            'cpc': diff_cpc,
            'cost': diff_cost,
            'conv_rate': diff_cr,
            'conv': diff_conv,
            'cpa': diff_cpa
        }

print("=== COMPARATIVE PERFORMANCE BREAKDOWN ===")
for seg in ['Total: Account', 'Total: Search terms', 'Total: Other search terms']:
    print(f"\n--- {seg} ---")
    t14 = tot_14.get(seg, {})
    tw1 = tot_w1.get(seg, {})
    t7 = tot_7.get(seg, {})
    
    print(f"{'Metric':<18} | {'Week 1 (Oct 8-14)':<18} | {'Week 2 (Oct 15-21)':<18} | {'Change (W2 vs W1)':<18} | {'14-Day Total (Oct 8-21)':<22}")
    print("-" * 105)
    
    metrics = [
        ('Spend (£)', 'cost', '£{:.2f}', True),
        ('Impressions', 'impr', '{:,.0f}', False),
        ('Clicks', 'clicks', '{:,.0f}', False),
        ('Avg CPC (£)', 'cpc', '£{:.2f}', True),
        ('CTR (%)', 'ctr', '{:.2%}', False),
        ('Conversions', 'conv', '{:.1f}', False),
        ('Conversion Rate (%)', 'conv_rate', '{:.2%}', False),
        ('Cost / Conv (CPA) (£)', 'cpa', '£{:.2f}', True)
    ]
    
    for lbl, field, fmt, is_curr in metrics:
        v_w1 = tw1.get(field, 0)
        v_7 = t7.get(field, 0)
        v_14 = t14.get(field, 0)
        
        s_w1 = fmt.format(v_w1)
        s_7 = fmt.format(v_7)
        s_14 = fmt.format(v_14)
        
        if v_w1 > 0:
            pct_chg = ((v_7 - v_w1) / v_w1) * 100
            diff_str = f"{pct_chg:+.1f}%"
        else:
            diff_str = "N/A"
            
        print(f"{lbl:<18} | {s_w1:<18} | {s_7:<18} | {diff_str:<18} | {s_14:<22}")

