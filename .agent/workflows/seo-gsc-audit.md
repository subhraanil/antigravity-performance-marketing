# Workflow: Google Search Console (GSC) Forensic Audit

## Overview
A systematic standard operating procedure to extract, diagnose, and remediate organic search query inefficiencies using Google Search Console data and the `gsc_analyzer.py` engine.

---

## Trigger Conditions
- Bi-weekly organic performance review.
- Identifying traffic drops or unexpected ranking stalls.
- Prioritizing quick-win SEO sprint items.

---

## Step-by-Step SOP

### Phase 1: Data Extraction
1. Open Google Search Console or connect via `mcp-search-console` / API.
2. Select target verified property.
3. Export **Search Results** covering the last 28 days (or last 3 months) with dimensions: `Query`, `Page`, `Clicks`, `Impressions`, `CTR`, `Position`.
4. Save as `gsc_data.csv` or pass directly to the analyzer.

### Phase 2: Cannibalization Analysis
1. Run the Cannibalization Detector:
   ```powershell
   python seo/seo-suite/gsc/gsc_analyzer.py --input gsc_data.csv --cannibalization
   ```
2. For every flagged conflict with $\ge 2,500$ impressions at stake:
   - Identify the `Primary Page` (highest click volume / best rank).
   - Review competing secondary pages against the **Remediation Decision Matrix** ([`google_search_console_intelligence_playbook.md`](file:///C:/Users/test/.gemini/antigravity/scratch/antigravity-performance-marketing/knowledge/google_search_console_intelligence_playbook.md)).
   - Implement either:
     - **301 Redirect** (if competing page is obsolete).
     - **Canonicalization** (if page must remain live for UX).
     - **De-optimization / Intent Differentiation** (if targeting distinct sub-topics).

### Phase 3: Striking-Distance Quick-Win Extraction
1. Run the Quick-Wins Engine:
   ```powershell
   python seo/seo-suite/gsc/gsc_analyzer.py --input gsc_data.csv --quick-wins
   ```
2. Filter for queries with **Opportunity Score $\ge 100$** (Positions 11.0–20.0, CTR $< 3\%$).
3. Execute the 4-Step On-Page Boost:
   - Front-load query into `<title>` (first 30 characters).
   - Natural inclusion in H2 header and opening 100 words.
   - Point 3 internal contextual links from high-authority pages on domain.
   - Add concise FAQ answering query directly.

### Phase 4: Verification & Monitoring
1. Request re-indexing via GSC URL Inspection tool.
2. Track position delta after 14 days; expect movement into Top 10 positions.
