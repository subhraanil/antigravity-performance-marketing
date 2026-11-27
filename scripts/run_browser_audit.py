import json
import time
from playwright.sync_api import sync_playwright

urls_to_test = [
    "https://victoryhcspl.com/",
    "https://victoryhcspl.com/healthcare-training/",
    "https://victoryhcspl.com/about-us/",
    "https://victoryhcspl.com/contact-us/"
]

results = {}

with sync_playwright() as p:
    # 1. Desktop test
    browser = p.chromium.launch(headless=True)
    
    for url in urls_to_test:
        print(f"\nTesting Desktop: {url}")
        context = browser.new_context(viewport={"width": 1366, "height": 768}, user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
        page = context.new_page()
        
        requests_log = []
        page.on("request", lambda req: requests_log.append({
            "url": req.url,
            "resource_type": req.resource_type
        }))
        
        t0 = time.time()
        response = page.goto(url, wait_until="networkidle", timeout=45000)
        total_time = round(time.time() - t0, 3)
        
        # Navigation timing
        timing = page.evaluate("""() => {
            const perf = performance.getEntriesByType('navigation')[0];
            const paint = performance.getEntriesByType('paint');
            let fcp = null;
            let fp = null;
            for (const p of paint) {
                if (p.name === 'first-paint') fp = p.startTime;
                if (p.name === 'first-contentful-paint') fcp = p.startTime;
            }
            return {
                ttfb: perf ? Math.round(perf.responseStart - perf.requestStart) : null,
                domInteractive: perf ? Math.round(perf.domInteractive) : null,
                domContentLoaded: perf ? Math.round(perf.domContentLoadedEventEnd) : null,
                loadEvent: perf ? Math.round(perf.loadEventEnd) : null,
                firstPaint: fp ? Math.round(fp) : null,
                firstContentfulPaint: fcp ? Math.round(fcp) : null
            };
        }""")
        
        # DOM statistics
        dom_stats = page.evaluate("""() => {
            return {
                totalElements: document.querySelectorAll('*').length,
                h1Count: document.querySelectorAll('h1').length,
                h1Text: Array.from(document.querySelectorAll('h1')).map(e => e.innerText.trim()),
                images: document.querySelectorAll('img').length,
                imagesNoAlt: Array.from(document.querySelectorAll('img')).filter(e => !e.getAttribute('alt') || !e.getAttribute('alt').trim()).length,
                forms: document.querySelectorAll('form').length,
                links: document.querySelectorAll('a').length
            };
        }""")
        
        context.close()
        
        results[f"desktop_{url}"] = {
            "url": url,
            "device": "desktop",
            "load_time_sec": total_time,
            "timing": timing,
            "dom_stats": dom_stats,
            "requests_count": len(requests_log),
            "by_type": {t: sum(1 for r in requests_log if r['resource_type'] == t) for t in set(r['resource_type'] for r in requests_log)}
        }
        print(f"  Desktop Loaded in {total_time}s | TTFB: {timing.get('ttfb')}ms | FCP: {timing.get('firstContentfulPaint')}ms | Load: {timing.get('loadEvent')}ms")
        print(f"  Requests: {len(requests_log)} | Elements: {dom_stats.get('totalElements')}")

    # 2. Mobile emulation test (Pixel 7)
    pixel7 = p.devices['Pixel 7']
    for url in [urls_to_test[0], urls_to_test[1]]:
        print(f"\nTesting Mobile: {url}")
        context_m = browser.new_context(**pixel7)
        page_m = context_m.new_page()
        
        t0 = time.time()
        response_m = page_m.goto(url, wait_until="networkidle", timeout=45000)
        total_time_m = round(time.time() - t0, 3)
        
        timing_m = page_m.evaluate("""() => {
            const perf = performance.getEntriesByType('navigation')[0];
            const paint = performance.getEntriesByType('paint');
            let fcp = null;
            for (const p of paint) {
                if (p.name === 'first-contentful-paint') fcp = p.startTime;
            }
            return {
                ttfb: perf ? Math.round(perf.responseStart - perf.requestStart) : null,
                domContentLoaded: perf ? Math.round(perf.domContentLoadedEventEnd) : null,
                loadEvent: perf ? Math.round(perf.loadEventEnd) : null,
                fcp: fcp ? Math.round(fcp) : null
            };
        }""")
        
        # Check viewport and horizontal overflow
        overflow = page_m.evaluate("""() => {
            return {
                scrollWidth: document.documentElement.scrollWidth,
                clientWidth: document.documentElement.clientWidth,
                hasHorizontalOverflow: document.documentElement.scrollWidth > document.documentElement.clientWidth
            };
        }""")
        
        context_m.close()
        results[f"mobile_{url}"] = {
            "url": url,
            "device": "mobile",
            "load_time_sec": total_time_m,
            "timing": timing_m,
            "overflow": overflow
        }
        print(f"  Mobile Loaded in {total_time_m}s | TTFB: {timing_m.get('ttfb')}ms | FCP: {timing_m.get('fcp')}ms | Overflow: {overflow}")

    browser.close()

with open("website audit/victoryhcspl.com/browser_audit_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\nBrowser audit complete! Results saved to browser_audit_results.json")
