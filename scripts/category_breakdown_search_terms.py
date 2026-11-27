import openpyxl
import re
from collections import defaultdict

f_14d = r"data/Pet Mode/Search terms report.xlsx"
f_7d = r"data/Pet Mode/Search terms report (1).xlsx"

def analyze_report(fname, name):
    wb = openpyxl.load_workbook(fname, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    
    total_spend = 0.0
    total_clicks = 0
    total_impr = 0
    total_conv = 0.0
    
    categories = defaultdict(lambda: {'queries': 0, 'clicks': 0, 'cost': 0.0, 'impr': 0, 'conv': 0.0, 'terms': []})
    
    # Categorization regex rules
    cat_rules = [
        ('Barking / Collars', re.compile(r'\b(bark|barking|collar|vibrat|ultrasonic|citronella)\b', re.I)),
        ('Dog Car Seat / Travel', re.compile(r'\b(car seat|car bed|booster|seat belt|car harness|travel bed|travel)\b', re.I)),
        ('Dog Beds (General / Ortho / Large)', re.compile(r'\b(bed|beds|mattress|sofa|cooling|orthopedic|orthopaedic|donut|bolster|cot|raised bed|xxl|xl|waterproof)\b', re.I)),
        ('Cat Products (Scratch / Trees / Litter / Toilet)', re.compile(r'\b(cat|cats|kitten|scratch|scratcher|climbing|shelves|litter|toilet)\b', re.I)),
        ('Grooming & Brushes', re.compile(r'\b(groom|grooming|brush|steam|comb|deshedding)\b', re.I)),
        ('Dental / Chews / Toys', re.compile(r'\b(molar|stick|dental|chew|toy|toys|ball)\b', re.I)),
        ('Trackers / GPS / AirTag (Leakage)', re.compile(r'\b(airtag|air tag|gps|tracker|tracking)\b', re.I)),
        ('Food / Treats / Medical (Leakage)', re.compile(r'\b(food|treat|treats|trachea|ear|wound|injured|recovery|bandage|medicine)\b', re.I)),
        ('Competitor Brands (Leakage)', re.compile(r'\b(pawcify|luther bennett|pawrade|pets at home|petkit|omlet|furbo|tractive|pitpat)\b', re.I)),
        ('Leads / Harnesses / Apparel', re.compile(r'\b(lead|leads|harness|collar|leash|coat|jacket|jumper)\b', re.I)),
    ]
    
    account_totals = {}
    
    for r in rows:
        term = r[0]
        if not term or not isinstance(term, str):
            continue
        if term.startswith("Total:"):
            account_totals[term] = {
                'clicks': float(r[5]) if r[5] != '--' and r[5] is not None else 0,
                'impr': float(r[6]) if r[6] != '--' and r[6] is not None else 0,
                'cost': float(r[10]) if r[10] != '--' and r[10] is not None else 0,
                'conv': float(r[13]) if r[13] != '--' and r[13] is not None else 0,
            }
            continue
            
    for r in rows[3:]:
        term = r[0]
        if not term or not isinstance(term, str):
            continue
        if term.startswith("Total:") or term == "Search term":
            continue
            
        clicks = float(r[5]) if r[5] is not None and r[5] != '--' else 0.0
        impr = float(r[6]) if r[6] is not None and r[6] != '--' else 0.0
        cost = float(r[10]) if r[10] is not None and r[10] != '--' else 0.0
        conv = float(r[13]) if r[13] is not None and r[13] != '--' else 0.0
        
        total_spend += cost
        total_clicks += clicks
        total_impr += impr
        total_conv += conv
        
        # Determine category
        matched_cat = 'Other / Miscellaneous'
        for cat_name, pattern in cat_rules:
            if pattern.search(term):
                matched_cat = cat_name
                break
                
        categories[matched_cat]['queries'] += 1
        categories[matched_cat]['clicks'] += clicks
        categories[matched_cat]['cost'] += cost
        categories[matched_cat]['impr'] += impr
        categories[matched_cat]['conv'] += conv
        if clicks > 0 or conv > 0:
            categories[matched_cat]['terms'].append((term, clicks, cost, conv))
            
    print(f"\n{'='*30} {name} {'='*30}")
    print("ACCOUNT TOTALS:")
    for k, v in account_totals.items():
        print(f"  {k}: Clicks: {v['clicks']}, Impr: {v['impr']}, Cost: £{v['cost']:.2f}, Conv: {v['conv']}")
        
    print(f"\nDISCLOSED QUERIES CATEGORY BREAKDOWN (Total Spend: £{total_spend:.2f}, Clicks: {total_clicks}, Conv: {total_conv}):")
    print(f"{'Category':<35} | {'Queries':<7} | {'Clicks':<6} | {'Cost (£)':<9} | {'Avg CPC':<7} | {'Conv':<5} | {'CPA (£)':<8} | {'% Spend':<7}")
    print("-" * 95)
    
    sorted_cats = sorted(categories.items(), key=lambda x: x[1]['cost'], reverse=True)
    for cat, data in sorted_cats:
        cpc = data['cost'] / data['clicks'] if data['clicks'] > 0 else 0.0
        cpa = data['cost'] / data['conv'] if data['conv'] > 0 else 0.0
        pct_spend = (data['cost'] / total_spend * 100) if total_spend > 0 else 0.0
        cpa_str = f"£{cpa:.2f}" if data['conv'] > 0 else "-"
        print(f"{cat:<35} | {data['queries']:<7} | {data['clicks']:<6.0f} | £{data['cost']:<8.2f} | £{cpc:<6.2f} | {data['conv']:<5.1f} | {cpa_str:<8} | {pct_spend:<6.1f}%")

    return categories, account_totals

cat_14d, tot_14d = analyze_report(f_14d, "LAST 14 DAYS (OCT 8 - OCT 21)")
cat_7d, tot_7d = analyze_report(f_7d, "LAST 7 DAYS (OCT 15 - OCT 21)")

