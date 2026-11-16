---
name: seo-geo-audit
description: >-
  Comprehensive Generative Engine Optimization (GEO) & AI Search Audit SOP for Google AI Mode, Google AI Overviews, Perplexity, and ChatGPT Search using Princeton KDD 2024 levers and geo_engine.py.
---

# Generative Engine Optimization (GEO) & AI Search Audit SOP

## Executive Overview
A standard operating procedure to evaluate and optimize digital properties for AI answer engines (ChatGPT Search, Perplexity, Claude, and Google AI Overviews / AI Mode). Combines crawler protocol checks, raw HTML hydration verification, Schema entity validation, Princeton KDD 2024 citability levers, `llms.txt` generation, and automated scoring via `geo_engine.py`.

---

## Trigger Conditions
- New product, service, or high-priority landing page launch.
- Brand citation share declining in AI search summaries.
- Quarterly technical and AI search readiness review.

---

## The 6-Phase GEO/AEO Audit Protocol

### Phase 1: Automated 0–100 GEO Audit (`geo_engine.py`)
1. Fetch target HTML or save local snapshot:
   ```powershell
   python seo/seo-suite/geo/geo_engine.py --file <page.html>
   ```
2. Inspect overall Citability Score and 9-dimension rubric breakdown.
3. Target: Minimum score of **80/100** (Optimal rating band).

### Phase 2: Crawler & RFC 9309 Protocol Governance
1. Inspect the domain's `/robots.txt` file.
2. Confirm permissions for key AI retrieval and search user-agents:
   - `Google-Extended` (Google AI Overviews & Gemini training)
   - `GPTBot` & `OAI-SearchBot` (OpenAI / ChatGPT Search)
   - `PerplexityBot` (Perplexity search and citations)
   - `ClaudeBot` & `Claude-SearchBot` (Anthropic citations)
3. Ensure no blanket disallow rules (`Disallow: /`) block knowledge hubs or product catalogs.
4. Generate compliant robots.txt configuration:
   ```powershell
   python seo/seo-suite/geo/geo_engine.py --generate-robots
   ```

### Phase 3: Static Rendering & Raw HTML Hydration Check
1. Inspect the raw source HTML (without executing client-side JavaScript).
2. Verify that:
   - Product specifications, pricing, ingredients, and key value props exist in the raw DOM.
   - Core FAQ questions and answers are present in semantic `<p>` and `<li>` elements.
   - Images feature descriptive, entity-rich `alt` attributes.

### Phase 4: Schema Entity Graph Verification
1. Validate JSON-LD markup using schema validator tools.
2. Ensure interconnected entity types are properly defined:
   - `@type: Organization` with official `sameAs` links (Wikidata, LinkedIn, Wikipedia).
   - `@type: Product` or `Service` with verifiable pricing, availability, and aggregate ratings.
   - `@type: FAQPage` with direct, factual Q&A pairs.

### Phase 5: Content Citability Optimization (Princeton KDD 2024 Levers)
Apply proven academic citability optimization levers:
1. **Authoritative Source Citations (+30% to +115% boost)**: Link to authoritative third-party data (`.gov`, `.edu`, industry peer-reviewed reports).
2. **Concrete Statistics (+40% boost)**: Embed explicit numerical metrics, percentages, benchmark comparisons, and sample sizes.
3. **Attributed Expert Quotes (+30% to +40% boost)**: Feature quotes with the expert's full name, credential, and organization.
4. **Direct Answer Structuring**: Ensure the first 60 words beneath each H2 header answer the primary question concisely without promotional fluff.
5. **Comparison Tables**: Provide head-to-head comparison tables in clean Markdown or semantic `<table>` tags.

### Phase 6: `llms.txt` Generation & Live Citation Sweep
1. Generate an official specification-compliant `llms.txt` file:
   ```powershell
   python seo/seo-suite/geo/geo_engine.py --generate-llms
   ```
2. Deploy to domain root: `https://example.com/llms.txt`.
3. Conduct live verification queries across Perplexity, ChatGPT Search, and Google AI Overviews.
4. Record citation share, competitor source appearances, and model factual accuracy.
