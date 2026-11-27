import openpyxl
import os

f_14d = r"data/Pet Mode/Search terms report.xlsx"
f_7d = r"data/Pet Mode/Search terms report (1).xlsx"

for fname, label in [(f_14d, "Last 14 Days (Oct 8 - Oct 21)"),
                     (f_7d, "Last 7 Days (Oct 15 - Oct 21)")]:
    print(f"\n{'='*25} {label} {'='*25}")
    wb = openpyxl.load_workbook(fname, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    headers = rows[2]
    
    total_queries = 0
    total_clicks = 0
    total_cost = 0.0
    converting = []
    non_converting = []
    
    for r in rows[3:]:
        term = r[0]
        if not term or not isinstance(term, str):
            continue
        if term.startswith("Total:"):
            continue
            
        clicks = float(r[5]) if r[5] is not None and r[5] != '--' else 0.0
        impr = float(r[6]) if r[6] is not None and r[6] != '--' else 0.0
        cpc = float(r[9]) if r[9] is not None and r[9] != '--' else 0.0
        cost = float(r[10]) if r[10] is not None and r[10] != '--' else 0.0
        conv = float(r[13]) if r[13] is not None and r[13] != '--' else 0.0
        cost_conv = float(r[14]) if r[14] is not None and r[14] != '--' else 0.0
        
        total_queries += 1
        total_clicks += clicks
        total_cost += cost
        
        item = {
            'term': term, 'clicks': clicks, 'impr': impr,
            'cpc': cpc, 'cost': cost, 'conv': conv, 'cost_conv': cost_conv
        }
        
        if conv > 0:
            converting.append(item)
        elif clicks > 0:
            non_converting.append(item)
            
    print(f"Total Disclosed Queries: {total_queries}")
    print(f"Total Disclosed Clicks: {total_clicks:.0f} | Total Disclosed Cost: £{total_cost:.2f}")
    print(f"\n--- CONVERTING SEARCH TERMS ({len(converting)} queries) ---")
    for c in sorted(converting, key=lambda x: x['conv'], reverse=True):
        print(f"  • \"{c['term']}\": Conv: {c['conv']} | Clicks: {c['clicks']:.0f} | Impr: {c['impr']:.0f} | Cost: £{c['cost']:.2f} | CPA: £{c['cost_conv']:.2f} | CPC: £{c['cpc']:.2f}")
        
    print(f"\n--- TOP 25 NON-CONVERTING SPEND QUERIES (WASTED SPEND) ---")
    top_wasted = sorted(non_converting, key=lambda x: x['cost'], reverse=True)[:25]
    for w in top_wasted:
        print(f"  • \"{w['term']}\": Clicks: {w['clicks']:.0f} | Impr: {w['impr']:.0f} | Cost: £{w['cost']:.2f} | CPC: £{w['cpc']:.2f}")

