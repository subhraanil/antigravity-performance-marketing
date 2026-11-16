---
name: pagespeed-cwv-audit-sop
description: >-
  Execute rapid Core Web Vitals (CWV) diagnostics and full Lighthouse audits using the Google PageSpeed Insights API, evaluate real-world field metrics (LCP, INP, CLS), and isolate DOM render-blocking bottlenecks.
---

# Core Web Vitals & PageSpeed Insights Diagnostic SOP

## Overview
A comprehensive diagnostic procedure to fetch mobile and desktop performance metrics using the Google PageSpeed Insights API, evaluate Core Web Vitals against Google ranking thresholds, and inspect DOM render-blocking bottlenecks.

---

## Trigger Conditions
- Pre-launch client website technical onboarding.
- Sudden conversion rate drops or bounce rate spikes on mobile landing pages.
- Preparing SEO technical audit deliverables and speed optimization roadmaps.

---

## Step-by-Step Diagnostic SOP

### Step 1: Rapid API Query (Mobile & Desktop)

**PowerShell Quick Query (Mobile)**:
```powershell
$targetUrl = "https://example.com/"
$response = Invoke-RestMethod -Uri "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=$targetUrl&strategy=mobile"
$score = [math]::Round($response.lighthouseResult.categories.performance.score * 100)
Write-Host "Mobile Performance Score: $score / 100"
```

**PowerShell Quick Query (Desktop)**:
```powershell
$responseDesktop = Invoke-RestMethod -Uri "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=$targetUrl&strategy=desktop"
$scoreDesktop = [math]::Round($responseDesktop.lighthouseResult.categories.performance.score * 100)
Write-Host "Desktop Performance Score: $scoreDesktop / 100"
```

**cURL Alternative**:
```bash
curl -s "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=https://example.com/&strategy=mobile" | grep -o '"performance":{[^}]*'
```

---

### Step 2: Core Web Vitals (CWV) Official Thresholds

Evaluate field data and Lighthouse metrics against Google Search ranking criteria:

| Metric | Full Name | Good (Passing) | Needs Improvement | Poor (Failing) | Primary Root Causes |
|---|---|---|---|---|---|
| **LCP** | Largest Contentful Paint | $\le 2.5\text{ s}$ | $2.5\text{ s} - 4.0\text{ s}$ | $> 4.0\text{ s}$ | Unoptimized hero images, slow TTFB, client-side JS rendering |
| **INP** | Interaction to Next Paint | $\le 200\text{ ms}$ | $200\text{ ms} - 500\text{ ms}$ | $> 500\text{ ms}$ | Heavy main-thread JS execution, long tasks ($>50\text{ms}$) |
| **CLS** | Cumulative Layout Shift | $\le 0.1$ | $0.1 - 0.25$ | $> 0.25$ | Images/ads without dimensions, late-injected dynamic banners, web fonts (FOUT) |
| **TTFB** | Time to First Byte | $\le 800\text{ ms}$ | $800\text{ ms} - 1800\text{ ms}$ | $> 1800\text{ ms}$ | Slow origin server response, lack of edge CDN caching |

---

### Step 3: Diagnostic Root-Cause Inspection

1. **Render-Blocking CSS/JS**:
   - Inspect `lighthouseResult.audits['render-blocking-resources']`.
   - Identify render-blocking Google Fonts, unbundled stylesheets, or synchronous analytics scripts.
2. **Image Optimization & Layout Dimensions**:
   - Check uncompressed PNG/JPEG files missing WebP/AVIF modern variants.
   - Verify every `<img>` and `<iframe>` contains explicit `width` and `height` attributes to prevent CLS.
3. **DOM Inspection & SSR vs Hydration**:
   - Inspect raw source HTML to verify whether content is statically rendered or requires JavaScript execution:
     ```powershell
     Start-Process "chrome" "view-source:$targetUrl"
     ```

---

### Step 4: Engineering Remediation Ticket

Generate an actionable developer ticket structured as follows:
- **Observed CWV Metrics**: Exact measured numbers for LCP, INP, CLS, and TTFB.
- **Specific Offending Elements**: URL of slowest assets or CSS selectors of LCP elements.
- **Actionable Technical Fix**: Specific directives (`loading="lazy"`, `fetchpriority="high"`, `defer`, CDN edge cache rule).
