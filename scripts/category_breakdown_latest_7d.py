import openpyxl
import re
from collections import defaultdict

fname = r"data/Pet Mode/Search terms report.xlsx"
wb = openpyxl.load_workbook(fname, data_only=True)
ws = wb.active
rows = list(ws.iter_rows(values_only=True))

cat_rules = [
    ('Barking / Anti-Bark', re.compile(r'\b(bark|barking|collar|vibrat|ultrasonic|citronella)\b', re.I)),
    ('Dog Car Seat / Travel Beds', re.compile(r'\b(car seat|car bed|booster|seat belt|car harness|travel bed|travel|car)\b', re.I)),
    ('Dog Beds (General / Ortho / Raised)', re.compile(r'\b(bed|beds|mattress|sofa|cooling|orthopedic|orthopaedic|donut|bolster|cot|raised bed|xxl|xl|waterproof)\b', re.I)),
    ('Cat Products (Scratch / Trees / Toys)', re.compile(r'\b(cat|cats|kitten|scratch|scratcher|climbing|shelves|litter|toilet)\b', re.I)),
    ('Grooming & Nail Care', re.compile(r'\b(groom|grooming|brush|steam|comb|deshedding|clippers|grinder|nail)\b', re.I)),
    ('Leads / Harnesses / Belts', re.compile(r'\b(lead|leads|harness|collar|leash|waist|bungee|double lead)\b', re.I)),
    ('Water Fountains / Bowls', re.compile(r'\b(fountain|water|dispenser|bowl|bowls)\b', re.I)),
    ('Competitor Brands (Leakage)', re.compile(r'\b(pawcify|luther bennett|pawrade|pets at home|petkit|omlet|furbo|tractive|pitpat|violets and paws|my fluffy friend|jacko and co|wagging rights)\b', re.I)),
    ('Irrelevant / Electronics / Food (Leakage)', re.compile(r'\b(smartwatch|watch|trachea|jerky|food|treat|treats|blanket|heated blanket|footstool|for humans)\b', re.I)),
]

categories = defaultdict(lambda: {'queries': 0, 'clicks': 0, 'cost': 0.0, 'impr': 0, 'conv': 0.0, 'terms': []})

for r in rows[3:]:
    term = r[0]
    if not term or not isinstance(term, str) or term.startswith("Total:") or term == "Search term":
        continue
    clicks = float(r[5]) if r[5] is not None and r[5] != '--' else 0.0
    impr = float(r[6]) if r[6] is not None and r[6] != '--' else 0.0
    cost = float(r[10]) if r[10] is not None and r[10] != '--' else 0.0
    conv = float(r[13]) if r[13] is not None and r[13] != '--' else 0.0
    
    matched_cat = 'Other / Miscellaneous'
    for cat_name, pat in cat_rules:
        if pat.search(term):
            matched_cat = cat_name
            break
            
    categories[matched_cat]['queries'] += 1
    categories[matched_cat]['clicks'] += clicks
    categories[matched_cat]['cost'] += cost
    categories[matched_cat]['impr'] += impr
    categories[matched_cat]['conv'] += conv
    if clicks > 0 or conv > 0:
        categories[matched_cat]['terms'].append((term, clicks, cost, conv))

print(f"{'Category':<38} | {'Queries':<7} | {'Clicks':<6} | {'Spend (£)':<9} | {'Avg CPC':<7} | {'Conv':<5} | {'CPA (£)':<8} | {'% Spend'}")
print("-" * 100)

tot_spend = sum(c['cost'] for c in categories.values())
for cat, d in sorted(categories.items(), key=lambda x: x[1]['cost'], reverse=True):
    cpc = d['cost'] / d['clicks'] if d['clicks'] > 0 else 0
    cpa = d['cost'] / d['conv'] if d['conv'] > 0 else 0
    cpa_str = f"£{cpa:.2f}" if d['conv'] > 0 else "-"
    pct = (d['cost'] / tot_spend * 100) if tot_spend > 0 else 0
    print(f"{cat:<38} | {d['queries']:<7} | {d['clicks']:<6.0f} | £{d['cost']:<8.2f} | £{cpc:<6.2f} | {d['conv']:<5.1f} | {cpa_str:<8} | {pct:<5.1f}%")

