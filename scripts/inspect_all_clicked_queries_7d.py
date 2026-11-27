import openpyxl

f_7d = r"data/Pet Mode/Search terms report (1).xlsx"
wb = openpyxl.load_workbook(f_7d, data_only=True)
ws = wb.active
rows = list(ws.iter_rows(values_only=True))

print("=== ALL QUERIES WITH CLICKS > 0 IN LAST 7 DAYS (OCT 15 - OCT 21) ===")
clicked_queries = []
for r in rows[3:]:
    term = r[0]
    if not term or not isinstance(term, str) or term.startswith("Total:") or term == "Search term":
        continue
    clicks = float(r[5]) if r[5] is not None and r[5] != '--' else 0.0
    cost = float(r[10]) if r[10] is not None and r[10] != '--' else 0.0
    conv = float(r[13]) if r[13] is not None and r[13] != '--' else 0.0
    impr = float(r[6]) if r[6] is not None and r[6] != '--' else 0.0
    cpc = float(r[9]) if r[9] is not None and r[9] != '--' else 0.0
    
    if clicks > 0:
        clicked_queries.append({
            'term': term, 'clicks': clicks, 'impr': impr,
            'cost': cost, 'conv': conv, 'cpc': cpc
        })

print(f"Total clicked queries: {len(clicked_queries)}")
print("\nSorted by spend descending:")
for q in sorted(clicked_queries, key=lambda x: x['cost'], reverse=True):
    conv_str = f"*** CONV: {q['conv']} ***" if q['conv'] > 0 else ""
    print(f"  £{q['cost']:<6.2f} | Clicks: {q['clicks']:<3.0f} | CPC: £{q['cpc']:<5.2f} | Impr: {q['impr']:<5.0f} | {q['term']:<40} {conv_str}")
