# Technical SEO & Screaming Frog Crawl Remediation Playbook
# Field-Tested Remediation Guide for Next.js, WordPress, and Headless Architectures

## 1. Screaming Frog Crawl Severity Hierarchy

When auditing a domain using Screaming Frog SEO Spider, prioritize issue remediation based on algorithmic impact:

```
[CRITICAL: P0] --> 5xx Server Errors, Broken Canonical Tags, Infinite Redirect Loops
[HIGH: P1]     --> 4xx Client Errors, Missing Title/H1, Blocked Internal CSS/JS
[MEDIUM: P2]   --> Multi-hop 301 Chains, Non-indexable in Sitemap, Duplicate Titles
[LOW: P3]      --> Missing Alt Text, Overlong Meta Descriptions, External Outbound 301s
```

---

## 2. Remediation Runbooks by Defect Category

### A. 4xx Client Errors (Broken Internal Links)
- **Root Cause**: Deleted blog posts, updated product URLs without 301 redirects, or outdated navigation menus.
- **Screaming Frog Report**: `Inlinks` tab on 404 URL.
- **Fix**:
  1. If replacement URL exists: Update the internal link at the source code/template level to point directly to the destination 200 URL (never leave an internal link pointing to a redirect).
  2. Implement server-level 301 redirect in `.htaccess`, `nginx.conf`, or `next.config.js`.

### B. 3xx Redirect Chains & Loops
- **Impact**: Each redirect hop degrades crawl budget and dilutes PageRank equity by 5–10%.
- **Screaming Frog Report**: `Reports > Redirects > Redirect Chains`.
- **Fix**: Flatten all redirect hops so every internal link and canonical URL resolves directly to the final 200 destination in a single step.

### C. Canonical Tag Hygiene
- **Critical Rules**:
  - The canonical tag must always point to the **HTTPS, non-www (or www), lowercase, trailing-slash consistent** final canonical URL.
  - Never specify a 301 redirect, 404 page, or `noindex` page as a canonical URL.
  - Parameterized URLs (e.g. `?sort=price&filter=color`) must point back to the clean root category URL.

### D. Title & H1 Tag Optimization
- **Page Titles**:
  - Length: 50–60 characters (580 pixels max).
  - Format: `[Primary Target Keyword] - [Secondary Hook] | [Brand Name]`
- **H1 Tags**:
  - Exactly one H1 tag per indexable URL.
  - Match user intent and topic entity.

---

## 3. Real-Time Indexing via IndexNow API

For headless, static, or rapidly updated websites, notify search engines (Bing, Yandex, Seznam) instantly upon publishing or modifying content:

```bash
# IndexNow API Payload Example
POST https://api.indexnow.org/indexnow
Content-Type: application/json; charset=utf-8

{
  "host": "example.com",
  "key": "your_indexnow_api_key",
  "keyLocation": "https://example.com/your_indexnow_api_key.txt",
  "urlList": [
    "https://example.com/updated-page-1",
    "https://example.com/new-product-2"
  ]
}
```
