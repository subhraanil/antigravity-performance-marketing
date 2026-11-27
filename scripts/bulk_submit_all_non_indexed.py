import json
import requests
import xml.etree.ElementTree as ET
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# Load latest category inspection data from Sep 01
with open('data/category_indexing_status_sep01.json', 'r') as f:
    cat_data = json.load(f)

non_indexed_categories = [item['url'] for item in cat_data if not item['is_indexed']]

# Also fetch main sitemap URLs (sitemap.xml)
sitemap_main_url = 'https://www.promotionalproductsnow.au/sitemap.xml'
headers = {'User-Agent': 'Mozilla/5.0'}

main_urls = []
try:
    resp = requests.get(sitemap_main_url, headers=headers, timeout=10)
    root = ET.fromstring(resp.content)
    main_urls = [el.text.strip() for el in root.findall('.//{*}loc') if el.text]
except Exception as e:
    print(f"Error fetching main sitemap: {e}")

# Combine all target non-indexed and key site URLs
urls_to_submit = list(dict.fromkeys(non_indexed_categories + main_urls))

print(f"Total Non-Indexed Category & Main URLs to submit: {len(urls_to_submit)}", flush=True)

SCOPES = ["https://www.googleapis.com/auth/indexing"]
ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"

creds = service_account.Credentials.from_service_account_file("service_account.json", scopes=SCOPES)
creds.refresh(Request())

session = requests.Session()
session.headers.update({"Authorization": f"Bearer {creds.token}"})

success_count = 0
error_count = 0
results = []

for idx, url in enumerate(urls_to_submit, 1):
    payload = {"url": url, "type": "URL_UPDATED"}
    try:
        res = session.post(ENDPOINT, json=payload, timeout=10)
        if res.status_code == 200:
            success_count += 1
            results.append({'url': url, 'status': '200 OK'})
            print(f"[{idx}/{len(urls_to_submit)}] SUCCESS (200 OK) | {url}", flush=True)
        else:
            error_count += 1
            results.append({'url': url, 'status': f'Error {res.status_code}'})
            print(f"[{idx}/{len(urls_to_submit)}] ERROR {res.status_code} | {url} | {res.text}", flush=True)
    except Exception as e:
        error_count += 1
        results.append({'url': url, 'status': f'Exception: {e}'})
        print(f"[{idx}/{len(urls_to_submit)}] EXCEPTION | {url} | {e}", flush=True)

with open('data/final_submission_log.json', 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n================ FINAL BULK SUBMISSION SUMMARY ================", flush=True)
print(f"Total URLs Processed: {len(urls_to_submit)}", flush=True)
print(f"Successful (200 OK): {success_count}", flush=True)
print(f"Failed: {error_count}", flush=True)
print("===============================================================\n", flush=True)
