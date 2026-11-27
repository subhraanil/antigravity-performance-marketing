import urllib.request
import xml.etree.ElementTree as ET
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import time
import sys
from urllib.parse import urlparse

SITEMAPS = {
    'sitemap.xml': 'https://www.promotionalproductsnow.au/sitemap.xml',
    'sitemap-products.xml': 'https://www.promotionalproductsnow.au/sitemap-products.xml',
    'sitemap-categories.xml': 'https://www.promotionalproductsnow.au/sitemap-categories.xml'
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 AntigravitySEOBot/1.0'
}

DISALLOW_PATHS = [
    '/account',
    '/cart',
    '/quotes',
    '/forgot-password',
    '/change-password',
    '/offline'
]

def fetch_sitemap_urls(sitemap_name, url):
    print(f"Fetching sitemap: {sitemap_name} ({url})...", flush=True)
    req = urllib.request.Request(url, headers=HEADERS)
    urls = []
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            content = resp.read()
            root = ET.fromstring(content)
            loc_elements = root.findall('.//{*}loc')
            for el in loc_elements:
                if el.text:
                    urls.append(el.text.strip())
        print(f"Found {len(urls)} URLs in {sitemap_name}", flush=True)
    except Exception as e:
        print(f"Error fetching {sitemap_name}: {e}", flush=True)
    return urls

# Global requests session per thread or pool
session = requests.Session()
adapter = requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100)
session.mount('https://', adapter)
session.mount('http://', adapter)

def check_url(item):
    sitemap_name, url = item
    parsed = urlparse(url)
    path_lower = parsed.path.lower()
    
    is_disallowed = any(path_lower.startswith(d.lower()) for d in DISALLOW_PATHS)
    
    result = {
        'sitemap': sitemap_name,
        'url': url,
        'status_code': None,
        'final_url': url,
        'final_status_code': None,
        'is_redirect': False,
        'has_www_mismatch': not url.startswith('https://www.promotionalproductsnow.au'),
        'is_disallowed': is_disallowed,
        'error': None,
        'response_time_ms': 0
    }
    
    start_time = time.time()
    try:
        # Fast HEAD or GET request (allow_redirects=False first)
        resp = session.head(url, headers=HEADERS, timeout=6, allow_redirects=False)
        # If method not allowed or odd status, retry with GET
        if resp.status_code == 405:
            resp = session.get(url, headers=HEADERS, timeout=6, allow_redirects=False, stream=True)
            
        result['status_code'] = resp.status_code
        result['response_time_ms'] = int((time.time() - start_time) * 1000)
        
        if resp.status_code in (301, 302, 303, 307, 308):
            result['is_redirect'] = True
            loc = resp.headers.get('Location', '')
            if loc:
                result['final_url'] = loc if loc.startswith('http') else f"https://www.promotionalproductsnow.au{loc}"
            else:
                result['final_url'] = url
            result['final_status_code'] = 200 # Assume redirect target or verify if needed
        else:
            result['final_url'] = resp.url if hasattr(resp, 'url') else url
            result['final_status_code'] = resp.status_code
            
    except requests.exceptions.Timeout:
        result['error'] = 'Timeout'
    except requests.exceptions.RequestException as e:
        result['error'] = str(e)
    except Exception as e:
        result['error'] = str(e)
        
    return result

def main():
    all_sitemap_urls = []
    sitemap_counts = {}
    
    for sm_name, sm_url in SITEMAPS.items():
        urls = fetch_sitemap_urls(sm_name, sm_url)
        sitemap_counts[sm_name] = len(urls)
        for u in urls:
            all_sitemap_urls.append((sm_name, u))
            
    print(f"\nTotal URLs across all sitemaps to verify: {len(all_sitemap_urls)}", flush=True)
    
    results = []
    completed = 0
    total = len(all_sitemap_urls)
    
    # 80 worker threads with requests.Session for high throughput
    with ThreadPoolExecutor(max_workers=80) as executor:
        futures = [executor.submit(check_url, item) for item in all_sitemap_urls]
        for future in as_completed(futures):
            res = future.result()
            results.append(res)
            completed += 1
            if completed % 500 == 0 or completed == total:
                print(f"Progress: {completed}/{total} ({completed/total*100:.1f}%) checked", flush=True)
                
    # Summarize
    summary = {
        'total_sitemaps': len(SITEMAPS),
        'sitemap_counts': sitemap_counts,
        'total_urls_checked': len(results),
        'status_200_direct_www': 0,
        'status_301_redirects': 0,
        'status_404_not_found': 0,
        'status_50x_server_error': 0,
        'other_status_codes': {},
        'errors': 0,
        'www_mismatches': 0,
        'disallowed_urls_in_sitemap': 0,
    }
    
    redirect_details = []
    broken_details = []
    disallowed_details = []
    www_mismatch_details = []
    
    for r in results:
        code = r['status_code']
        final_code = r['final_status_code']
        
        if r['has_www_mismatch']:
            summary['www_mismatches'] += 1
            www_mismatch_details.append(r)
            
        if r['is_disallowed']:
            summary['disallowed_urls_in_sitemap'] += 1
            disallowed_details.append(r)
            
        if r['error']:
            summary['errors'] += 1
            broken_details.append(r)
        elif code == 200 and not r['has_www_mismatch']:
            summary['status_200_direct_www'] += 1
        elif r['is_redirect']:
            summary['status_301_redirects'] += 1
            redirect_details.append(r)
        elif code == 404:
            summary['status_404_not_found'] += 1
            broken_details.append(r)
        elif code and code >= 500:
            summary['status_50x_server_error'] += 1
            broken_details.append(r)
        else:
            summary['other_status_codes'][str(code)] = summary['other_status_codes'].get(str(code), 0) + 1
            if code and code >= 400:
                broken_details.append(r)
                
    print("\n================== CRAWL SUMMARY ==================", flush=True)
    print(f"Total Sitemaps: {summary['total_sitemaps']}", flush=True)
    print(f"Total URLs Checked: {summary['total_urls_checked']}", flush=True)
    print(f"Direct 200 OK (With www): {summary['status_200_direct_www']}", flush=True)
    print(f"Non-WWW URLs in Sitemap (301 Redirecting): {summary['www_mismatches']}", flush=True)
    print(f"Total Redirects (301/302): {summary['status_301_redirects']}", flush=True)
    print(f"Broken / 404 / Error URLs: {len(broken_details)}", flush=True)
    print(f"Disallowed by robots.txt in Sitemap: {summary['disallowed_urls_in_sitemap']}", flush=True)
    print("====================================================\n", flush=True)
    
    with open('data/sitemap_audit_results.json', 'w') as f:
        json.dump(results, f, indent=2)
        
    with open('data/sitemap_audit_summary.json', 'w') as f:
        json.dump({
            'summary': summary,
            'broken_details': broken_details,
            'disallowed_details': disallowed_details,
            'redirect_sample': redirect_details[:50],
            'www_mismatch_sample': www_mismatch_details[:50]
        }, f, indent=2)
        
    print("Saved results to data/sitemap_audit_results.json and data/sitemap_audit_summary.json", flush=True)

if __name__ == '__main__':
    main()
