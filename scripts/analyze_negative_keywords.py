import sys
sys.stdout.reconfigure(encoding='utf-8')
import openpyxl
from collections import defaultdict, Counter
import re

wb = openpyxl.load_workbook('data/Pet Mode/Google Ads/Search terms report (11).xlsx', data_only=True)
sheet = wb.active

queries = []
for row in sheet.iter_rows(min_row=4, values_only=True):
    term = str(row[0] or '').strip()
    if not term or term.startswith('Total:'):
        continue
    clicks = float(row[5] or 0)
    impr = float(row[6] or 0)
    cost = float(row[10] or 0)
    conv = float(row[13] or 0)
    queries.append({'term': term, 'clicks': clicks, 'impr': impr, 'cost': cost, 'conv': conv})

print(f"Total user queries: {len(queries)}")

# 1. Competitors
competitors = [
    'costco', 'amazon', 'pets at home', 'petsathome', 'gulpup', '3 peaks', 'three peaks',
    'petsafe', 'pet safe', 'ruffwear', 'julius k9', 'b&m', 'home bargains', 'asda', 'tesco',
    'tk maxx', 'ebay', 'temu', 'shein', 'ali express', 'aliexpress', 'zooplus', 'vet uk',
    'viovet', 'petmeds', 'barking heads', 'scruffs', 'trixie', 'kong', 'furminator', 'halty',
    'gentle leader', 'earth rated', 'barking dog', 'john lewis', 'argos', 'dunelm', 'therapet'
]

comp_matches = defaultdict(lambda: {'count': 0, 'cost': 0.0, 'clicks': 0, 'impr': 0, 'conv': 0.0, 'terms': []})

for q in queries:
    t_lower = q['term'].lower()
    for c in competitors:
        if c in t_lower:
            comp_matches[c]['count'] += 1
            comp_matches[c]['cost'] += q['cost']
            comp_matches[c]['clicks'] += q['clicks']
            comp_matches[c]['impr'] += q['impr']
            comp_matches[c]['conv'] += q['conv']
            comp_matches[c]['terms'].append(q['term'])
            break

print("\n=== Competitor Brand Analysis in Search Terms ===")
for c, data in sorted(comp_matches.items(), key=lambda x: x[1]['cost'] + x[1]['impr']*0.01, reverse=True):
    if data['count'] > 0:
        print(f"{c:18} | Impr: {data['impr']:5.0f} | Clicks: {data['clicks']:3.0f} | Cost: £{data['cost']:6.2f} | Conv: {data['conv']:2.0f} | Count: {data['count']:3d} | Sample: {data['terms'][:3]}")

# 2. Controversial / Electric / Shock / Prong Collars
controversial = ['shock', 'electric', 'prong', 'choke', 'pinch', 'e-collar', 'ecollar', 'zap', 'citronella', 'spray', 'remote']
contra_matches = defaultdict(lambda: {'count': 0, 'cost': 0.0, 'clicks': 0, 'impr': 0, 'conv': 0.0, 'terms': []})
for q in queries:
    t_lower = q['term'].lower()
    for w in controversial:
        if re.search(r'\b' + re.escape(w) + r'\b', t_lower):
            contra_matches[w]['count'] += 1
            contra_matches[w]['cost'] += q['cost']
            contra_matches[w]['clicks'] += q['clicks']
            contra_matches[w]['impr'] += q['impr']
            contra_matches[w]['conv'] += q['conv']
            contra_matches[w]['terms'].append(q['term'])
            break

print("\n=== Controversial / Misaligned Tech Collars ===")
for w, data in sorted(contra_matches.items(), key=lambda x: x[1]['cost'] + x[1]['impr']*0.01, reverse=True):
    if data['count'] > 0:
        print(f"{w:18} | Impr: {data['impr']:5.0f} | Clicks: {data['clicks']:3.0f} | Cost: £{data['cost']:6.2f} | Conv: {data['conv']:2.0f} | Count: {data['count']:3d} | Sample: {data['terms'][:3]}")

# 3. Non-Pet / Irrelevant Species / Human Products
irrelevant = ['baby', 'toddler', 'child', 'horse', 'equine', 'bird', 'fish', 'reptile', 'rabbit', 'hamster', 'guinea pig', 'human', 'rug doctor', 'carpet cleaner machine', 'vacuum', 'bissell', 'vax']
irrel_matches = defaultdict(lambda: {'count': 0, 'cost': 0.0, 'clicks': 0, 'impr': 0, 'conv': 0.0, 'terms': []})
for q in queries:
    t_lower = q['term'].lower()
    for w in irrelevant:
        if re.search(r'\b' + re.escape(w) + r'\b', t_lower):
            irrel_matches[w]['count'] += 1
            irrel_matches[w]['cost'] += q['cost']
            irrel_matches[w]['clicks'] += q['clicks']
            irrel_matches[w]['impr'] += q['impr']
            irrel_matches[w]['conv'] += q['conv']
            irrel_matches[w]['terms'].append(q['term'])
            break

print("\n=== Irrelevant Species / Human Products ===")
for w, data in sorted(irrel_matches.items(), key=lambda x: x[1]['cost'] + x[1]['impr']*0.01, reverse=True):
    if data['count'] > 0:
        print(f"{w:18} | Impr: {data['impr']:5.0f} | Clicks: {data['clicks']:3.0f} | Cost: £{data['cost']:6.2f} | Conv: {data['conv']:2.0f} | Count: {data['count']:3d} | Sample: {data['terms'][:3]}")

# 4. Low Intent / Informational / DIY / Free / Bargain
low_intent = ['free', 'diy', 'how to', 'make your own', 'homemade', 'recipe', 'wholesale', 'cheap', 'second hand', 'used', 'ebay', 'gumtree', 'facebook marketplace', 'near me', 'hire', 'rent', 'jobs', 'careers']
low_matches = defaultdict(lambda: {'count': 0, 'cost': 0.0, 'clicks': 0, 'impr': 0, 'conv': 0.0, 'terms': []})
for q in queries:
    t_lower = q['term'].lower()
    for w in low_intent:
        if re.search(r'\b' + re.escape(w) + r'\b', t_lower):
            low_matches[w]['count'] += 1
            low_matches[w]['cost'] += q['cost']
            low_matches[w]['clicks'] += q['clicks']
            low_matches[w]['impr'] += q['impr']
            low_matches[w]['conv'] += q['conv']
            low_matches[w]['terms'].append(q['term'])
            break

print("\n=== Low Intent / Bargain / DIY ===")
for w, data in sorted(low_matches.items(), key=lambda x: x[1]['cost'] + x[1]['impr']*0.01, reverse=True):
    if data['count'] > 0:
        print(f"{w:18} | Impr: {data['impr']:5.0f} | Clicks: {data['clicks']:3.0f} | Cost: £{data['cost']:6.2f} | Conv: {data['conv']:2.0f} | Count: {data['count']:3d} | Sample: {data['terms'][:3]}")

# 5. Top 50 Zero-Conversion Terms with Cost > 0
zero_conv = [q for q in queries if q['conv'] == 0 and q['cost'] > 0]
zero_conv.sort(key=lambda x: x['cost'], reverse=True)
print(f"\nTotal zero-conversion terms with spend: {len(zero_conv)} (Total spend: £{sum(q['cost'] for q in zero_conv):.2f})")
print("\nTop 30 Zero-Conversion Terms by Spend:")
for q in zero_conv[:30]:
    print(f"£{q['cost']:6.2f} | Clicks: {q['clicks']:2.0f} | Impr: {q['impr']:4.0f} | {q['term']}")
