# AEO / GEO (Generative Engine Optimization) Audit Workflow

Step-by-step procedure to audit any domain's readiness for Google AI Mode, Google AI Overviews, Perplexity, and ChatGPT Search.

---

## Phase 1: Crawler & RFC 9309 Protocol Check
1. Fetch and inspect target domain's `/robots.txt`.
2. Confirm permissions for:
   - `Google-Extended` (used for Google AI Overviews and Gemini training)
   - `GPTBot` (OpenAI / ChatGPT Search)
   - `PerplexityBot` (Perplexity indexing)
   - `ClaudeBot` (Anthropic citations)
3. Flag any blanket disallows (`Disallow: /`) on content folders.

---

## Phase 2: Static Rendering & Hydration Check
1. Inspect the raw source HTML (without executing client-side JavaScript).
2. Verify that:
   - Product titles, specifications, ingredients, and prices exist in the raw response.
   - Core FAQ answers and definitions are present in `<p>` and `<li>` tags.
   - Images feature descriptive `alt` attributes.

---

## Phase 3: Schema Entity Graph Verification
1. Validate JSON-LD markup using schema validator tools.
2. Ensure the following entities are present and interconnected:
   - `@type: Organization` with official `sameAs` Wikidata/social links.
   - `@type: Product` or `Service` with verifiable pricing and availability.
   - `@type: FAQPage` or `ItemAvailability` on commercial landing pages.

---

## Phase 4: Direct Answer & Comparison Table Analysis
1. Check the top 10 informational and transactional pages.
2. Ensure direct answers to common questions appear in the first 60 words beneath each H2.
3. Check for head-to-head comparison tables (`<table>` or Markdown format).

---

## Phase 5: Generative Citation Sweep
1. Query key brand queries on Perplexity and ChatGPT Search.
2. Record:
   - Is the domain cited as a primary source?
   - What competitors appear in the synthesized answer?
   - What factual inaccuracies exist in the model's summary?
3. Generate an action plan with targeted content enhancements to win high-intent citations.
