import openpyxl

file16m = r"C:\Users\test\Videos\Personal\data\Paid Media World\https___paidmediaworld.com_-Performance-on-Search-2026-10-13 (1).xlsx"
file7d = r"C:\Users\test\Videos\Personal\data\Paid Media World\https___paidmediaworld.com_-Performance-on-Search-2026-10-13.xlsx"

print("==================== 16-MONTH GSC PERFORMANCE SUMMARY ====================")
wb16 = openpyxl.load_workbook(file16m, data_only=True)

# 1. Total Clicks & Impressions from Chart sheet
chart_sheet = wb16['Chart']
rows = list(chart_sheet.iter_rows(values_only=True))[1:]
total_clicks_16m = sum(float(r[1]) for r in rows if r[1] is not None and str(r[1]).strip() != '')
total_impressions_16m = sum(float(r[2]) for r in rows if r[2] is not None and str(r[2]).strip() != '')
overall_ctr_16m = (total_clicks_16m / total_impressions_16m) * 100 if total_impressions_16m > 0 else 0

print(f"Total Clicks (16 Months): {int(total_clicks_16m)}")
print(f"Total Impressions (16 Months): {int(total_impressions_16m):,}")
print(f"Overall CTR (16 Months): {overall_ctr_16m:.2f}%")

# 2. Top 10 Pages
print("\n--- TOP 10 PAGES BY IMPRESSIONS (16 Months) ---")
pages_sheet = wb16['Pages']
page_rows = list(pages_sheet.iter_rows(values_only=True))[1:]
sorted_pages = sorted(page_rows, key=lambda x: float(x[2]) if x[2] is not None else 0, reverse=True)
for r in sorted_pages[:10]:
    url = r[0]
    clicks = int(r[1]) if r[1] is not None else 0
    impr = int(r[2]) if r[2] is not None else 0
    ctr = (clicks / impr * 100) if impr > 0 else 0
    pos = f"{float(r[4]):.1f}" if len(r) > 4 and r[4] is not None else "N/A"
    print(f"  {url}\n    Impr: {impr:,} | Clicks: {clicks} | CTR: {ctr:.2f}% | Avg Pos: {pos}")

# 3. Top 10 Queries
print("\n--- TOP 10 QUERIES BY IMPRESSIONS (16 Months) ---")
queries_sheet = wb16['Queries']
query_rows = list(queries_sheet.iter_rows(values_only=True))[1:]
sorted_queries = sorted(query_rows, key=lambda x: float(x[2]) if x[2] is not None else 0, reverse=True)
for r in sorted_queries[:10]:
    q = str(r[0]).replace('\n', ' ').strip()
    clicks = int(r[1]) if r[1] is not None else 0
    impr = int(r[2]) if r[2] is not None else 0
    ctr = (clicks / impr * 100) if impr > 0 else 0
    pos = f"{float(r[4]):.1f}" if len(r) > 4 and r[4] is not None else "N/A"
    print(f"  Query: '{q[:70]}...'\n    Impr: {impr:,} | Clicks: {clicks} | CTR: {ctr:.2f}% | Avg Pos: {pos}")

print("\n==================== 7-DAY GSC PERFORMANCE SUMMARY ====================")
wb7 = openpyxl.load_workbook(file7d, data_only=True)
chart_7 = wb7['Chart']
rows7 = list(chart_7.iter_rows(values_only=True))[1:]
clicks_7 = sum(float(r[1]) for r in rows7 if r[1] is not None and str(r[1]).strip() != '')
impr_7 = sum(float(r[2]) for r in rows7 if r[2] is not None and str(r[2]).strip() != '')
ctr_7 = (clicks_7 / impr_7 * 100) if impr_7 > 0 else 0
print(f"7-Day Clicks: {int(clicks_7)}")
print(f"7-Day Impressions: {int(impr_7):,}")
print(f"7-Day CTR: {ctr_7:.2f}%")
