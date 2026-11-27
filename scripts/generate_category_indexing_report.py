import json

with open('data/category_indexing_status.json', 'r') as f:
    data = json.load(f)

indexed_count = sum(1 for item in data if item['is_indexed'])
not_indexed_count = len(data) - indexed_count

report_content = f"""# Google Search Console Indexing Report: Category Pages

**Website:** `https://www.promotionalproductsnow.au/`  
**Sitemap:** `https://www.promotionalproductsnow.au/sitemap-categories.xml`  
**Total Category Pages Audited:** {len(data)}  
**Indexed Pages:** {indexed_count} ({indexed_count/len(data)*100:.1f}%)  
**Not Indexed Pages:** {not_indexed_count} ({not_indexed_count/len(data)*100:.1f}%)  

---

## 1. Summary of Indexing Statuses

| Indexing Remark / State | Count | Description |
| :--- | :--- | :--- |
| **Indexed in Google (Submitted and indexed)** | **{indexed_count}** | Page is live and indexed in Google search results. |
| **Crawled - currently not indexed** | **{sum(1 for d in data if d['coverage_state'] == 'Crawled - currently not indexed')}** | Google crawled the page but decided not to index it yet. |
| **Discovered - currently not indexed** | **{sum(1 for d in data if d['coverage_state'] == 'Discovered - currently not indexed')}** | Google knows about the page but hasn't crawled it yet. |
| **Duplicate without user-selected canonical** | **{sum(1 for d in data if d['coverage_state'] == 'Duplicate without user-selected canonical')}** | Google detected duplicate content without a clear canonical. |
| **URL is unknown to Google** | **{sum(1 for d in data if d['coverage_state'] == 'URL is unknown to Google')}** | URL has never been seen or processed by Google yet. |

---

## 2. Category Pages Indexing Status Table (All 157 URLs)

| # | Category Page URL | Status | Remark | Last Crawl Date |
| :--- | :--- | :--- | :--- | :--- |
"""

for i, item in enumerate(data, 1):
    status_tag = "✅ **Indexed**" if item['is_indexed'] else "❌ **Not Indexed**"
    last_crawl = item['last_crawl_time'][:10] if item['last_crawl_time'] != 'Never Crawled' and 'T' in item['last_crawl_time'] else item['last_crawl_time']
    report_content += f"| {i} | [{item['url']}]({item['url']}) | {status_tag} | {item['remark']} | {last_crawl} |\n"

report_path = r'C:\Users\test\.gemini\antigravity\brain\4eb3ec65-bf45-4286-847e-91bd9af0530e\category_indexing_report.md'

with open(report_path, 'w', encoding='utf-8') as f:
    f.write(report_content)

print(f"Report written to {report_path}")
