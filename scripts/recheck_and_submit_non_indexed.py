import xml.etree.ElementTree as ET
import requests
import json
import time
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES_READ = ['https://www.googleapis.com/auth/webmasters.readonly']
SCOPES_INDEX = ['https://www.googleapis.com/auth/indexing']
INDEXING_ENDPOINT = 'https://indexing.googleapis.com/v3/urlNotifications:publish'

site_url = 'https://www.promotionalproductsnow.au/'
sitemap_url = 'https://www.promotionalproductsnow.au/sitemap-categories.xml'

headers = {'User-Agent': 'Mozilla/5.0'}

print("=== STEP 1: FETCHING LATEST CATEGORY URLS FROM SITEMAP ===", flush=True)
resp = requests.get(sitemap_url, headers=headers, timeout=10)
root = ET.fromstring(resp.content)
category_urls = [el.text.strip() for el in root.findall('.//{*}loc') if el.text]

print(f"Total category URLs found: {len(category_urls)}\n", flush=True)

def inspect_worker(item):
    idx, url = item
    creds = service_account.Credentials.from_service_account_file('service_account.json', scopes=SCOPES_READ)
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

print("=== STEP 2: RE-INSPECTING ALL CATEGORY URLS VIA GSC API ===", flush=True)
results = []
items = [(i+1, u) for i, u in enumerate(category_urls)]

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = [executor.submit(inspect_worker, item) for item in items]
    for future in as_completed(futures):
        results.append(future.result())

results.sort(key=lambda x: x['url'])

with open('data/category_indexing_status_aug27.json', 'w') as f:
    json.dump(results, f, indent=2)

indexed_list = [r for r in results if r['is_indexed']]
not_indexed_list = [r for r in results if not r['is_indexed']]

print(f"\n================ INSPECTION RESULTS ================", flush=True)
print(f"Total Category URLs: {len(results)}", flush=True)
print(f"Currently INDEXED: {len(indexed_list)} ({len(indexed_list)/len(results)*100:.1f}%)", flush=True)
print(f"Currently NOT INDEXED: {len(not_indexed_list)} ({len(not_indexed_list)/len(results)*100:.1f}%)", flush=True)
print("===================================================\n", flush=True)

print("=== STEP 3: SUBMITTING NON-INDEXED PAGES TO GOOGLE INDEXING API ===", flush=True)

if not_indexed_list:
    creds_idx = service_account.Credentials.from_service_account_file('service_account.json', scopes=SCOPES_INDEX)
    creds_idx.refresh(Request())

    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {creds_idx.token}"})

    submission_results = []
    success_count = 0
    error_count = 0

    for idx, item in enumerate(not_indexed_list, 1):
        target_url = item['url']
        payload = {"url": target_url, "type": "URL_UPDATED"}
        try:
            res = session.post(INDEXING_ENDPOINT, json=payload, timeout=10)
            if res.status_code == 200:
                success_count += 1
                submission_results.append({'url': target_url, 'status': '200 OK'})
                print(f"[{idx}/{len(not_indexed_list)}] SUBMITTED (200 OK) | {target_url}", flush=True)
            else:
                error_count += 1
                submission_results.append({'url': target_url, 'status': f'Error {res.status_code}'})
                print(f"[{idx}/{len(not_indexed_list)}] ERROR {res.status_code} | {target_url}", flush=True)
        except Exception as e:
            error_count += 1
            submission_results.append({'url': target_url, 'status': f'Exception: {e}'})
            print(f"[{idx}/{len(not_indexed_list)}] EXCEPTION | {target_url} | {e}", flush=True)

    with open('data/non_indexed_submission_results.json', 'w') as f:
        json.dump(submission_results, f, indent=2)

    print(f"\n================ SUBMISSION SUMMARY ================", flush=True)
    print(f"Total Non-Indexed URLs Pushed to API: {len(not_indexed_list)}", flush=True)
    print(f"Successfully Queued (200 OK): {success_count}", flush=True)
    print(f"Failed: {error_count}", flush=True)
    print("====================================================\n", flush=True)
else:
    print("All category pages are already indexed in Google Search! No submissions needed.", flush=True)
