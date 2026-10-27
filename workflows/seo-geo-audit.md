# Workflow: Generative Engine Optimization (GEO) & AI Search Audit

## Overview
A standard operating procedure to evaluate and optimize digital properties for AI answer engines (ChatGPT Search, Perplexity, Claude, and Google AI Overviews) using the `geo_engine.py` scoring engine.

---

## Trigger Conditions
- New product or high-priority landing page launch.
- Brand citation share declining in AI search summaries.
- Quarterly technical and AI readiness review.

---

## Step-by-Step SOP

### Phase 1: Automated 0–100 GEO Audit
1. Fetch target HTML or save local snapshot:
   ```powershell
   python seo/seo-suite/geo/geo_engine.py --file <page.html>
   ```
2. Inspect overall Citability Score and 9-dimension rubric breakdown.
3. Target: Minimum score of **80/100** (Optimal rating band).

### Phase 2: Robots.txt & Crawler Governance
1. Review domain `robots.txt` file.
2. Ensure search retrieval bots are permitted:
   ```powershell
   python seo/seo-suite/geo/geo_engine.py --generate-robots
   ```
3. Verify `OAI-SearchBot`, `PerplexityBot`, and `Claude-SearchBot` are explicitly set to `Allow: /`.

### Phase 3: Content Citability Optimization (Princeton KDD 2024 Levers)
1. **Source Citations (+30% to +115% boost):** Verify at least 3 authoritative third-party data citations (`.gov`, `.edu`, industry benchmark reports) are linked or referenced in text.
2. **Concrete Statistics (+40% boost):** Verify numerical metrics, percentages, and dates are present in key factual claims.
3. **Expert Quotes (+30% to +40% boost):** Add at least one attributed quote with full name, title, and organization.
4. **Direct Answer Box:** Ensure first 60 words under each H2 answer the primary question directly without throat-clearing fluff.

### Phase 4: `llms.txt` Generation
1. Generate an official specification-compliant `llms.txt` file:
   ```powershell
   python seo/seo-suite/geo/geo_engine.py --generate-llms
   ```
2. Deploy to domain root: `https://example.com/llms.txt`.
