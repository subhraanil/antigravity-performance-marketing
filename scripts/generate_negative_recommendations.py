import openpyxl

f_14d = r"data/Pet Mode/Search terms report.xlsx"
wb_14 = openpyxl.load_workbook(f_14d, data_only=True)
ws_14 = wb_14.active
r_14 = list(ws_14.iter_rows(values_only=True))

f_7d = r"data/Pet Mode/Search terms report (1).xlsx"
wb_7 = openpyxl.load_workbook(f_7d, data_only=True)
ws_7 = wb_7.active
r_7 = list(ws_7.iter_rows(values_only=True))

# Collect all non-converting spend queries across both
all_leakage = []

# Rules for negative keyword recommendations
neg_patterns = [
    # Category, Keyword to add, Match Type, Reason, regex/trigger
    ("Dog Food & Edible Treats", "trachea", "Phrase", "Pet Mode sells toys & dental sticks, not edible meat treats/chews"),
    ("Dog Food & Edible Treats", "jerky", "Phrase", "Pet Mode does not sell beef jerky or meat treats"),
    ("Dog Food & Edible Treats", "dog food", "Phrase", "Pet Mode does not sell pet food"),
    ("Competitor Brands", "pawcify", "Phrase", "Direct competitor brand name; £2.92 single click waste"),
    ("Competitor Brands", "luther bennett", "Phrase", "High-end dog bed competitor brand (£2.05 wasted)"),
    ("Competitor Brands", "pawrade", "Phrase", "Competitor brand name (£1.89 wasted)"),
    ("Competitor Brands", "jacko and co", "Phrase", "Competitor pet brand"),
    ("Competitor Brands", "wagging rights", "Phrase", "Competitor car bed brand"),
    ("Human & Furniture Items", "for humans", "Phrase", "Searches for human-sized pet beds (e.g., Plufl)"),
    ("Human & Furniture Items", "footstool", "Phrase", "Pet Mode does not sell furniture footstool beds (£1.49 wasted)"),
    ("Human & Furniture Items", "heated blanket", "Phrase", "Pet Mode does not sell electric/heated blankets (£2.26 wasted)"),
    ("Human & Furniture Items", "dog sofa", "Phrase", "Pet Mode does not sell dog sofas/couches (£2.00+ wasted)"),
    ("Human & Furniture Items", "dog couch", "Phrase", "Pet Mode does not sell dog couches"),
    ("Size Mismatch (XXL/Giant)", "xxl", "Phrase", "Pet Mode does not stock XXL sizes (£4.56 wasted across 2 clicks)"),
    ("Size Mismatch (XXL/Giant)", "giant dog bed", "Phrase", "Pet Mode beds are for standard/medium/large breeds, not giant breeds"),
    ("ISOFIX Car Mechanism", "isofix", "Phrase", "Car Booster Bed secures via seatbelts & headrest straps, not ISOFIX rigid latches"),
    ("Heavy Metal Chains", "cuban", "Phrase", "High-cost searches for luxury cuban link gold chains"),
    ("Heavy Metal Chains", "necklace", "Phrase", "Jewelry intent rather than pet functional collars"),
]

import re
leakage_summary = {}

for cat, kw, mtype, reason in neg_patterns:
    leakage_summary[kw] = {
        'category': cat,
        'keyword': kw,
        'match_type': mtype,
        'reason': reason,
        'clicks_14d': 0,
        'cost_14d': 0.0,
        'impr_14d': 0,
        'clicks_7d': 0,
        'cost_7d': 0.0,
        'impr_7d': 0,
        'matched_queries': set()
    }

pattern_compiled = {kw: re.compile(r'\b' + re.escape(kw) + r'\b', re.I) for _, kw, _, _ in neg_patterns}

# Scan 14d
for r in r_14[3:]:
    term = r[0]
    if not term or not isinstance(term, str) or term.startswith("Total:") or term == "Search term":
        continue
    clicks = float(r[5]) if r[5] is not None and r[5] != '--' else 0.0
    cost = float(r[10]) if r[10] is not None and r[10] != '--' else 0.0
    impr = float(r[6]) if r[6] is not None and r[6] != '--' else 0.0
    conv = float(r[13]) if r[13] is not None and r[13] != '--' else 0.0
    
    # Only non-converting
    if conv == 0:
        for kw, pat in pattern_compiled.items():
            if pat.search(term):
                leakage_summary[kw]['clicks_14d'] += clicks
                leakage_summary[kw]['cost_14d'] += cost
                leakage_summary[kw]['impr_14d'] += impr
                if clicks > 0:
                    leakage_summary[kw]['matched_queries'].add(term)

# Scan 7d
for r in r_7[3:]:
    term = r[0]
    if not term or not isinstance(term, str) or term.startswith("Total:") or term == "Search term":
        continue
    clicks = float(r[5]) if r[5] is not None and r[5] != '--' else 0.0
    cost = float(r[10]) if r[10] is not None and r[10] != '--' else 0.0
    impr = float(r[6]) if r[6] is not None and r[6] != '--' else 0.0
    conv = float(r[13]) if r[13] is not None and r[13] != '--' else 0.0
    
    if conv == 0:
        for kw, pat in pattern_compiled.items():
            if pat.search(term):
                leakage_summary[kw]['clicks_7d'] += clicks
                leakage_summary[kw]['cost_7d'] += cost
                leakage_summary[kw]['impr_7d'] += impr

print("=== RECOMMENDED NEGATIVE KEYWORDS SUMMARY ===")
print(f"{'Category':<25} | {'Keyword':<18} | {'Match':<8} | {'7d Spend':<9} | {'14d Spend':<10} | {'14d Clicks':<10} | {'Matched Queries'}")
print("-" * 120)

tot_leak_7d = 0.0
tot_leak_14d = 0.0

for kw, data in sorted(leakage_summary.items(), key=lambda x: x[1]['cost_14d'], reverse=True):
    tot_leak_7d += data['cost_7d']
    tot_leak_14d += data['cost_14d']
    q_sample = ", ".join(list(data['matched_queries'])[:2]) if data['matched_queries'] else "Impression only"
    kw_str = f'"{kw}"'
    print(f"{data['category']:<25} | {kw_str:<18} | {data['match_type']:<8} | £{data['cost_7d']:<8.2f} | £{data['cost_14d']:<9.2f} | {data['clicks_14d']:<10.0f} | {q_sample}")

print("-" * 120)
print(f"Total Identified Leakage in 14-Day Window: £{tot_leak_14d:.2f}")
print(f"Total Identified Leakage in Last 7 Days:   £{tot_leak_7d:.2f}")
