import openpyxl
import pandas as pd

file_path = r'c:\Users\test\Videos\Office\data\Pet Mode\Search terms report - pet mode 7 days.xlsx'
wb = openpyxl.load_workbook(file_path, data_only=True)
ws = wb.active

data = []
summary_rows = []
for r in range(4, ws.max_row + 1):
    st = ws.cell(r, 1).value
    if not st:
        continue
    if str(st).startswith('Total:'):
        summary_rows.append([ws.cell(r, c).value for c in range(1, 13)])
        continue
        
    match_type = ws.cell(r, 2).value
    added = ws.cell(r, 3).value
    clicks = float(ws.cell(r, 4).value or 0)
    impr = float(ws.cell(r, 5).value or 0)
    ctr = float(ws.cell(r, 6).value or 0)
    cpc = float(ws.cell(r, 8).value or 0)
    cost = float(ws.cell(r, 9).value or 0)
    conv_rate = float(ws.cell(r, 10).value or 0)
    conv = float(ws.cell(r, 11).value or 0)
    cpa = float(ws.cell(r, 12).value or 0)
    data.append({
        'term': str(st).strip(),
        'match_type': match_type,
        'added': added,
        'clicks': clicks,
        'impr': impr,
        'ctr': ctr,
        'cpc': cpc,
        'cost': cost,
        'conv_rate': conv_rate,
        'conv': conv,
        'cpa': cpa
    })

df = pd.DataFrame(data)

print("=== OVERALL CAMPAIGN TOTALS FOR 7 DAYS ===")
for r in summary_rows:
    print(r)

# 1. Categories
airtag_mask = df['term'].str.contains('airtag|air tag|gps|tracker|tracking|apple tag', case=False, na=False)
bark_mask = df['term'].str.contains('bark', case=False, na=False)
car_mask = df['term'].str.contains('car seat|car bed|dog car|seat cover', case=False, na=False)
bed_mask = df['term'].str.contains('dog bed|cat bed|raised bed|elevated bed|blanket', case=False, na=False)
nail_mask = df['term'].str.contains('nail|clipper|grinder', case=False, na=False)
scratch_mask = df['term'].str.contains('scratch|cat house', case=False, na=False)
lead_mask = df['term'].str.contains('lead|leash|harness|belt|collar', case=False, na=False) & ~airtag_mask & ~bark_mask
toy_mask = df['term'].str.contains('toy|ball|chew|teeth|toothbrush', case=False, na=False)
comp_mask = df['term'].str.contains('pets at home|funnyfuzzy|by teddy|speedy tail|amazon|argos|zooplus|pet planet', case=False, na=False)
info_mask = df['term'].str.contains('how|why|what|do airtags|reviews|free', case=False, na=False)

def get_stats(mask, name):
    sub = df[mask]
    clicks = sub['clicks'].sum()
    cost = sub['cost'].sum()
    impr = sub['impr'].sum()
    conv = sub['conv'].sum()
    return {
        'Category': name,
        'Terms_Count': len(sub),
        'Impressions': impr,
        'Clicks': clicks,
        'Cost (£)': round(cost, 2),
        'Conversions': conv,
        'Avg CPC (£)': round(cost/clicks, 2) if clicks>0 else 0.0
    }

cats = [
    get_stats(airtag_mask, "AirTag / GPS / Tracker Collars"),
    get_stats(car_mask, "Car Seats & Travel Beds"),
    get_stats(bark_mask, "Bark & Training Devices"),
    get_stats(bed_mask, "Beds & Blankets"),
    get_stats(nail_mask, "Nail Clippers & Grooming"),
    get_stats(scratch_mask, "Cat Scratchers & Posts"),
    get_stats(lead_mask, "Leads, Collars & Harnesses"),
    get_stats(toy_mask, "Toys & Dental Care"),
    get_stats(comp_mask, "Competitor Brand Searches"),
    get_stats(info_mask, "Informational / Question Queries")
]

cat_df = pd.DataFrame(cats).sort_values(by='Cost (£)', ascending=False)
print("\n=== SPEND & PERFORMANCE BY CATEGORY (7 DAYS) ===")
print(cat_df.to_string(index=False))

print("\n=== TOP 25 SEARCH TERMS BY COST ===")
clicked = df[df['clicks'] > 0].sort_values(by=['cost', 'clicks'], ascending=[False, False])
print(clicked[['term', 'clicks', 'impr', 'cpc', 'cost', 'conv']].head(25).to_string())

print("\n=== TOP 20 SEARCH TERMS BY IMPRESSIONS (Zero Clicks) ===")
zero_clk = df[df['clicks'] == 0].sort_values(by='impr', ascending=False)
print(zero_clk[['term', 'impr']].head(20).to_string())

print("\n=== ADDED / EXCLUDED STATUS ===")
print(df['added'].value_counts())
