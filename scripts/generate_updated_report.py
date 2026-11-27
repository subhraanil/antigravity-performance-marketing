import json

with open('data/category_indexing_status_latest.json', 'r') as f:
    data = json.load(f)

indexed_list = [item for item in data if item['is_indexed']]
not_indexed_list = [item for item in data if not item['is_indexed']]

indexed_count = len(indexed_list)
not_indexed_count = len(not_indexed_list)

crawled_not_indexed = sum(1 for d in data if d['coverage_state'] == 'Crawled - currently not indexed')
discovered_not_indexed = sum(1 for d in data if d['coverage_state'] == 'Discovered - currently not indexed')
duplicate_canonical = sum(1 for d in data if d['coverage_state'] == 'Duplicate without user-selected canonical')
unknown_url = sum(1 for d in data if d['coverage_state'] == 'URL is unknown to Google')

report_content = f"""# Latest Google Search & Search Console Indexing Report: Category Pages

**Website:** `https://www.promotionalproductsnow.au/`  
**Sitemap:** `https://www.promotionalproductsnow.au/sitemap-categories.xml`  
**Audit Timestamp:** August 24, 2026  
**Total Category Pages Audited:** {len(data)}  
**Indexed in Google Search:** {indexed_count} ({indexed_count/len(data)*100:.1f}%)  
**Not Indexed Yet:** {not_indexed_count} ({not_indexed_count/len(data)*100:.1f}%)  

---

## 1. Indexing Status Summary

| Status Category | Count | Status Remark in GSC | Description |
| :--- | :--- | :--- | :--- |
| **Indexed in Google Search** | **{indexed_count}** | `Submitted and indexed` | Page is indexed and active in Google Search results. |
| **Not Indexed (Crawled)** | **{crawled_not_indexed}** | `Crawled - currently not indexed` | Google crawled the URL but has not indexed it yet. |
| **Not Indexed (Discovered)** | **{discovered_not_indexed}** | `Discovered - currently not indexed` | Google knows the URL but has not crawled it yet. |
| **Not Indexed (Duplicate Canonical)** | **{duplicate_canonical}** | `Duplicate without user-selected canonical` | Google detected duplicate content or parameter variation. |
| **Not Indexed (Unknown)** | **{unknown_url}** | `URL is unknown to Google` | URL has not been discovered/processed by Googlebot yet. |

---

## 2. Full Category Pages Indexing Status Table (All 157 URLs)

| # | Category Page URL | Google Search & GSC Status | Detailed GSC Remark | Last Crawled Date |
| :--- | :--- | :--- | :--- | :--- |
"""

for i, item in enumerate(data, 1):
    status_tag = "✅ **INDEXED**" if item['is_indexed'] else "❌ **NOT INDEXED**"
    last_crawl = item['last_crawl_time'][:10] if item['last_crawl_time'] != 'Never Crawled' and 'T' in item['last_crawl_time'] else item['last_crawl_time']
    report_content += f"| {i} | [{item['url']}]({item['url']}) | {status_tag} | {item['coverage_state']} | {last_crawl} |\n"

report_path = r'C:\Users\test\.gemini\antigravity\brain\4eb3ec65-bf45-4286-847e-91bd9af0530e\category_indexing_report.md'

with open(report_path, 'w', encoding='utf-8') as f:
    f.write(report_content)

print(f"Updated report written to {report_path}")
