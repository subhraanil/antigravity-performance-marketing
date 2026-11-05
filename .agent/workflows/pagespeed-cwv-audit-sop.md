# Workflow: Core Web Vitals & PageSpeed Diagnostics SOP

## Overview
A rapid diagnostic procedure to fetch real-world mobile and desktop performance metrics using the Google PageSpeed Insights API, evaluate Core Web Vitals (LCP, INP, CLS), and inspect DOM render-blocking bottlenecks.

---

## Trigger Conditions
- Pre-launch client website technical onboarding.
- Sudden conversion rate drop on mobile landing pages.
- Preparing technical audit deliverables and speed optimization roadmaps.

---

## Step-by-Step SOP

### Step 1: Automated PageSpeed Insights Query
1. Run API query for mobile performance:
   ```powershell
   $targetUrl = "https://example.com/"
   $response = Invoke-RestMethod -Uri "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=$targetUrl&strategy=mobile"
   ```
2. Extract Lighthouse Performance Score:
   ```powershell
   $score = [math]::Round($response.lighthouseResult.categories.performance.score * 100)
   Write-Host "Mobile Performance Score: $score / 100"
   ```

### Step 2: Core Web Vitals (CWV) Benchmark Evaluation
Evaluate against official Google thresholds:

| Metric | Full Name | Good (Passing) | Needs Improvement | Poor (Failing) |
|---|---|---|---|---|
| **LCP** | Largest Contentful Paint | $\le 2.5\text{ s}$ | $2.5\text{ s} - 4.0\text{ s}$ | $> 4.0\text{ s}$ |
| **INP** | Interaction to Next Paint | $\le 200\text{ ms}$ | $200\text{ ms} - 500\text{ ms}$ | $> 500\text{ ms}$ |
| **CLS** | Cumulative Layout Shift | $\le 0.1$ | $0.1 - 0.25$ | $> 0.25$ |
| **TTFB** | Time to First Byte | $\le 800\text{ ms}$ | $800\text{ ms} - 1800\text{ ms}$ | $> 1800\text{ ms}$ |

### Step 3: Diagnostic Root-Cause Inspection
1. **Render-Blocking CSS/JS**: Check opportunities list for unminified bundles, external fonts blocking paint, or heavy third-party tags (GTM, Hotjar, Meta Pixel).
2. **Image Optimization**: Identify uncompressed PNGs/JPEGs without WebP/AVIF modern formats and images missing explicit `width` and `height` attributes (primary cause of CLS).
3. **DOM Inspection**: Inspect raw HTML via browser source view to verify SSR content vs client-side JavaScript hydration lag:
   ```powershell
   Start-Process "chrome" "view-source:$targetUrl"
   ```

### Step 4: Engineering Remediation Hand-Off
Generate a concise developer ticket highlighting:
- Exact measured LCP element (image vs H1 heading).
- Third-party scripts requiring deferred loading (`defer` or `async`).
- CDN caching / server response time optimizations.
