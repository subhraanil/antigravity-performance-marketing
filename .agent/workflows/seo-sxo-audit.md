# Workflow: Search Experience Optimization (SXO) Audit SOP

## Overview
A structured diagnostic process to identify and rectify intent and page-type mismatches that prevent technically optimized pages from ranking in Google's top 3 organic positions.

---

## Trigger Conditions
- Page ranks between position 8.0 and 25.0 despite strong backlink equity and zero technical crawl errors.
- High organic impressions accompanied by high bounce rates or low conversion rates.
- Post-Core Update traffic degradation.

---

## Step-by-Step SOP

### Phase 1: Identify Target & Query
1. Isolate the target URL and its highest-impression query in Google Search Console.
2. Record current organic position, CTR, and monthly impression volume.

### Phase 2: SERP Reverse-Engineering
1. Search the target query in Google (incognito / clean proxy).
2. Tally page types across the Top 10 organic results:
   - Tool / Calculator / SaaS app
   - Product / Category Page (eCommerce)
   - Comparison / Alternatives roundup
   - How-to / Informational blog post
3. Identify the dominant format. If $\ge 70\%$ are comparison matrices and your page is an informational blog post, an intent mismatch exists.

### Phase 3: Multi-Persona Evaluation
Evaluate the landing page from three persona perspectives:
1. **Time-Crunched Operator:** Does the first screen give the definitive answer immediately?
2. **Analytical Scrutinizer:** Are specifications, pros/cons, and data points cleanly formatted in tables?
3. **Skeptical Buyer:** Are third-party validation badges, real user reviews, and clear CTA options visible?

### Phase 4: Wireframe Transformation (IST to SOLL)
1. Draft the SOLL (future state) wireframe reorganizing page elements according to user intent.
2. Front-load interactive or summary elements above the fold.
3. Deploy changes, update publication date, and submit URL for re-indexing in GSC.
