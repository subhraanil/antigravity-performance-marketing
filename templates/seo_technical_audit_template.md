# Technical SEO, AEO & Generative Discovery Audit

**Client / Domain:** {{domain}}  
**Audit Date:** {{date}}  
**Overall SEO Health Score:** {{score}} / 100  

---

## 1. Executive Summary & Critical Findings

| Audit Pillar | Score | Critical Findings | Action Priority |
| :--- | :--- | :--- | :--- |
| **Crawlability & Indexing** | {{crawl_score}}/100 | {{crawl_summary}} | High |
| **Generative AEO / GEO (Google AI Mode)** | {{aeo_score}}/100 | {{aeo_summary}} | Urgent |
| **On-Page & Schema Markup** | {{schema_score}}/100 | {{schema_summary}} | Medium |
| **Core Web Vitals & Speed** | {{cwv_score}}/100 | {{cwv_summary}} | Medium |

---

## 2. Generative Search & AI Mode Readiness (AEO/GEO)

With Google AI Mode and AI Overviews processing multimodal user intents, visibility requires structured entity alignment:

- [ ] **AI Crawler Permissions (RFC 9309)**: `robots.txt` explicitly allows or configures tokens for `Google-Extended`, `GPTBot`, `PerplexityBot`, and `ClaudeBot`.
- [ ] **JavaScript-Free Content Render**: Key content, headings, and product specifications render cleanly in static HTML without requiring client-side JS hydration.
- [ ] **Schema Entity Graph**: Comprehensive JSON-LD implemented (`Organization`, `Product`, `Review`, `FAQPage`, `MedicalWebPage` / `FinancialService`).
- [ ] **Fact & Claim Clarity**: Direct answer definitions positioned within the first 100 words of topical pillar pages.

---

## 3. Technical Crawl Defect Checklist

- **Broken Links & Redirect Chains**: {{broken_links_count}} 404 errors, {{redirect_chains_count}} 301 redirect chains identified.
- **Canonical Hygiene**: Ensure 100% self-referential canonicals on primary indexable URLs.
- **Duplicate Titles & H1s**: Resolved on {{duplicate_h1_count}} template pages.

---

## 4. Priority Implementation Roadmap

1. **Sprint 1 (Days 1–7)**: Fix critical crawl blockers, update robots.txt, and eliminate 4xx/5xx errors.
2. **Sprint 2 (Days 8–14)**: Deploy schema.org entity graph and optimize page speed (LCP < 2.5s).
3. **Sprint 3 (Days 15–30)**: Structure content clusters for Google AI Mode direct citation answerability.
