import xml.etree.ElementTree as ET
import requests
import json
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
site_url = 'https://www.promotionalproductsnow.au/'
sitemap_url = 'https://www.promotionalproductsnow.au/sitemap-categories.xml'

headers = {'User-Agent': 'Mozilla/5.0'}

print("Fetching latest category URLs from sitemap...", flush=True)
resp = requests.get(sitemap_url, headers=headers, timeout=10)
root = ET.fromstring(resp.content)
category_urls = [el.text.strip() for el in root.findall('.//{*}loc') if el.text]

print(f"Found {len(category_urls)} category URLs to inspect.\n", flush=True)

def inspect_worker(item):
    idx, url = item
    creds = service_account.Credentials.from_service_account_file('service_account.json', scopes=SCOPES)
    service = build('searchconsole', 'v1', credentials=creds)
    
    req_body = {
        'inspectionUrl': url,
        'siteUrl': site_url
    }
    
    verdict = "UNKNOWN"
    coverage_state = "Unknown State"
    last_crawl = "Never Crawled"
    is_indexed = False
    
    for attempt in range(3):
        try:
            res = service.urlInspection().index().inspect(body=req_body).execute()
            idx_res = res.get('inspectionResult', {}).get('indexStatusResult', {})
            
            verdict = idx_res.get('verdict', 'UNKNOWN')
            coverage_state = idx_res.get('coverageState', 'Unknown State')
            last_crawl = idx_res.get('lastCrawlTime', 'Never Crawled')
            
            is_indexed = (coverage_state.lower() == 'submitted and indexed' or verdict.lower() == 'pass')
            break
        except Exception as e:
            if '429' in str(e) or 'Quota' in str(e):
                time.sleep(1.5 * (attempt + 1))
            else:
                coverage_state = f"Error: {e}"
                break
                
    status_label = "Indexed in Google" if is_indexed else f"Not Indexed ({coverage_state})"
    print(f"[{idx}/{len(category_urls)}] {'INDEXED' if is_indexed else 'NOT INDEXED'} | {url} | {coverage_state}", flush=True)
    
    return {
        'url': url,
        'is_indexed': is_indexed,
        'verdict': verdict,
        'coverage_state': coverage_state,
        'last_crawl_time': last_crawl,
        'status_label': status_label
    }

results = []
items = [(i+1, u) for i, u in enumerate(category_urls)]

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = [executor.submit(inspect_worker, item) for item in items]
    for future in as_completed(futures):
        results.append(future.result())

results.sort(key=lambda x: x['url'])

with open('data/category_indexing_status_sep01.json', 'w') as f:
    json.dump(results, f, indent=2)

indexed_count = sum(1 for r in results if r['is_indexed'])
not_indexed_count = len(results) - indexed_count

print(f"\n================ SEPTEMBER 1 INSPECTION SUMMARY ================", flush=True)
print(f"Total Category URLs: {len(results)}", flush=True)
print(f"Indexed in Google: {indexed_count}", flush=True)
print(f"Not Indexed: {not_indexed_count}", flush=True)
print(f"Indexing Rate: {indexed_count / len(results) * 100:.1f}%", flush=True)
print("=================================================================\n", flush=True)
