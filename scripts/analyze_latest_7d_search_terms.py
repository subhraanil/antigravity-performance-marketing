import openpyxl

fname = r"data/Pet Mode/Search terms report.xlsx"
wb = openpyxl.load_workbook(fname, data_only=True)
ws = wb.active
rows = list(ws.iter_rows(values_only=True))

converting = []
clicked = []

for r in rows[3:]:
    term = r[0]
    if not term or not isinstance(term, str) or term.startswith("Total:") or term == "Search term":
        continue
    clicks = float(r[5]) if r[5] is not None and r[5] != '--' else 0.0
    impr = float(r[6]) if r[6] is not None and r[6] != '--' else 0.0
    cpc = float(r[9]) if r[9] is not None and r[9] != '--' else 0.0
    cost = float(r[10]) if r[10] is not None and r[10] != '--' else 0.0
    conv = float(r[13]) if r[13] is not None and r[13] != '--' else 0.0
    cost_conv = float(r[14]) if r[14] is not None and r[14] != '--' else 0.0
    
    item = {
        'term': term, 'clicks': clicks, 'impr': impr,
        'cpc': cpc, 'cost': cost, 'conv': conv, 'cost_conv': cost_conv
    }
    
    if conv > 0:
        converting.append(item)
    if clicks > 0:
        clicked.append(item)

print(f"=== CONVERTING SEARCH TERMS ({len(converting)} queries) ===")
for c in sorted(converting, key=lambda x: x['conv'], reverse=True):
    print(f"  • \"{c['term']}\" | Conv: {c['conv']} | Clicks: {c['clicks']:.0f} | Impr: {c['impr']:.0f} | Cost: £{c['cost']:.2f} | CPA: £{c['cost_conv']:.2f} | CPC: £{c['cpc']:.2f}")

print(f"\n=== TOP 30 CLICKED / SPEND SEARCH TERMS ===")
for q in sorted(clicked, key=lambda x: x['cost'], reverse=True)[:30]:
    conv_tag = f"*** CONV: {q['conv']} (CPA: £{q['cost_conv']:.2f}) ***" if q['conv'] > 0 else ""
    print(f"  £{q['cost']:<6.2f} | Clicks: {q['clicks']:<3.0f} | CPC: £{q['cpc']:<5.2f} | Impr: {q['impr']:<5.0f} | {q['term']:<42} {conv_tag}")

