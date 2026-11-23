# Technical SEO & Comprehensive Website Audit Playbook
# Standard Operating Procedure (SOP) & Reusable Audit Framework
# Integrates Screaming Frog Remediation, SSR Inspection & Issues-Only Reporting

This playbook standardizes the end-to-end Technical SEO & Website Audit workflow for B2B SaaS, lead generation, healthcare, education, and e-commerce websites.

---

## 1. Overview & Core Philosophy

Every technical audit delivered under this framework adheres to the **Evidence-Based "Issues-Only" Standard**:
- **Zero Hallucinated Metrics**: Every finding names the specific URL(s) affected, the observed state, the expected standard, business impact, and technical priority.
- **Issues-Only Presentation**: Executive summaries focus exclusively on defects, root causes, business risks, and prioritized roadmaps—avoiding clutter from unrequested boilerplate code.
- **Framework Depth**: Evaluates traditional CMS platforms (WordPress) and modern headless JavaScript architectures (Next.js, Nuxt, SvelteKit, React SSR).

---

## 2. Screaming Frog Crawl Severity Hierarchy

When auditing a domain using Screaming Frog SEO Spider or headless crawlers, categorize defects by algorithmic severity:

```
+-----------------------------------------------------------------------------+
|                          CRAWL SEVERITY HIERARCHY                           |
+-----------------------------------------------------------------------------+
| [CRITICAL: P0] --> 5xx Server Errors, Broken Canonical Tags, Infinite Loops |
| [HIGH: P1]     --> 404 Internal Broken Links, Missing H1, Noindex on Money  |
|                    Pages, Duplicate Title Tags, Soft 404s                   |
| [MEDIUM: P2]   --> Missing Meta Descriptions, Images > 100KB, Redirect     |
|                    Chains (<= 2 hops), Missing Schema Entities               |
| [LOW: P3]      --> Title Tag Length (> 60 chars), Minor Orphan Pages         |
+-----------------------------------------------------------------------------+
```

---

## 3. The 9-Phase Technical Audit Checklist

### Phase 1: Protocol & Crawlability
- Verify single canonical protocol (`https://` without `http://` or mixed content).
- Check `robots.txt` permissions for Googlebot, Bingbot, and AI crawlers (`Google-Extended`, `GPTBot`, `PerplexityBot`, `ClaudeBot`).
- Validate XML sitemaps: clean of 404s, redirects, or noindexed URLs.

### Phase 2: HTTP Status & Redirect Hygiene
- Ensure zero 301 redirect chains or loops.
- Confirm all internal links resolve directly with HTTP 200.

### Phase 3: JavaScript Framework & SSR Hydration
- Compare raw HTML source vs. client-rendered DOM.
- Verify core content, titles, specifications, and internal links exist before JavaScript execution.

### Phase 4: Core Web Vitals (CWV)
- Mobile & Desktop evaluation against Google thresholds:
  - **LCP** $\le 2.5\text{ s}$
  - **INP** $\le 200\text{ ms}$
  - **CLS** $\le 0.1$
  - **TTFB** $\le 800\text{ ms}$

### Phase 5: On-Page Architecture & Semantic Depth
- Single unique `<h1>` per indexable page.
- Descriptive `<title>` tags ($\le 60$ characters) and persuasive meta descriptions (150–160 characters).
- Structured heading hierarchy (`h1` -> `h2` -> `h3`) with direct answers placed in first 50 words under each H2.

### Phase 6: Schema Entity Graph Verification
- Validate JSON-LD markup: `@type: Organization` with `sameAs` Wikidata/social links.
- `@type: Product` or `Service` with pricing, availability, and aggregate rating.
- `@type: FAQPage` on key conversion pages.

### Phase 7: Mobile Usability & Viewport
- Responsive scaling across Mobile (375px), Tablet (768px), and Desktop (1440px).
- Tap targets $\ge 48\text{px} \times 48\text{px}$ with adequate padding.

### Phase 8: Conversion Rate Optimization (CRO) Friction
- Above-the-fold CTA visibility on mobile devices.
- Simplified lead capture forms ($\le 4$ fields on initial inquiry).
- Prominent click-to-call and WhatsApp instant contact buttons.

### Phase 9: Backlink & Security Hygiene
- SSL certificate validity and HSTS headers.
- Toxic backlink footprint detection and anchor text distribution check.

---

## 4. Standard Deliverables Package

Every client audit produces:
1. `[Client]_SEO_Audit_Report.pdf`: Executive-styled PDF report compiled via Playwright.
2. `[Client]_SEO_Audit_Report.docx`: Editable executive Word report.
3. `01_screaming_frog_crawl_raw.csv`: Complete raw crawl inventory.
4. `02_internal_404_and_broken_links.csv`: Actionable link repair queue.
5. `03_redirect_chains_and_loops.csv`: Permanent 301 cleanup list.
6. `04_pagespeed_cwv_audit_results.csv`: Mobile and desktop field metrics.
7. `05_schema_validation_log.csv`: Structured data audit findings.
8. `06_metadata_rewrites.csv`: Optimized titles, meta descriptions, and H1s for top pages.
