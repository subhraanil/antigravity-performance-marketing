---
name: seo-gsc-audit
description: >-
  Extract Search Console performance data via API or CSV, diagnose query cannibalization, extract striking-distance quick wins, and execute forensic ranking remediations.
---

# Google Search Console (GSC) Performance & Forensic Audit SOP

## Overview
A systematic standard operating procedure to extract, diagnose, and remediate organic search query inefficiencies using Google Search Console API data, automated query analysis (`gsc_performance.py`), and forensic optimization engines (`gsc_analyzer.py`).

---

## Trigger Conditions
- Bi-weekly or monthly organic performance review.
- Identifying sudden ranking stalls or unexpected click drops.
- Mining quick-win SEO sprint opportunities for high-intent landing pages.

---

## Step-by-Step SOP

### Phase 1: Data Extraction & API Access

#### Option A: Direct API Performance Query (`gsc_performance.py`)
1. Ensure `credentials.json` or `service_account.json` is configured in the root directory.
2. Run performance queries with specific dimensions:
   ```powershell
   # Top queries by impressions and clicks (last 28 days)
   python scripts/gsc_performance.py \
     --site-url "https://example.com/" \
     --start-date "2026-10-01" \
     --end-date "2026-10-28" \
     --dimensions "query" \
     --limit 500
   ```
   ```powershell
   # Page-level performance breakdown
   python scripts/gsc_performance.py \
     --site-url "https://example.com/" \
     --start-date "2026-10-01" \
     --end-date "2026-10-28" \
     --dimensions "page,query" \
     --limit 1000
   ```

#### Option B: Manual CSV Export / MCP Integration
1. Open Google Search Console -> Performance -> Search Results.
2. Select Date Range: Last 28 Days (or 3 Months).
3. Export full report as `gsc_data.csv` with dimensions: `Query`, `Page`, `Clicks`, `Impressions`, `CTR`, `Position`.

---

### Phase 2: Query Cannibalization Analysis

1. Run the Cannibalization Detector:
   ```powershell
   python seo/seo-suite/gsc/gsc_analyzer.py --input gsc_data.csv --cannibalization
   ```
2. For every flagged conflict with $\ge 2,500$ impressions at stake:
   - Identify the **Primary Page** (highest historical clicks and superior intent match).
   - Review competing secondary pages against the **Remediation Decision Matrix**:
     - **301 Redirect**: If competing secondary page is thin, redundant, or obsolete.
     - **Canonical Tag**: If secondary page must remain accessible for UX/campaigns.
     - **De-optimization / Intent Splitting**: If secondary page targets a distinct sub-topic, update its title/H1 and remove competing anchor texts.

---

### Phase 3: Striking-Distance Quick-Win Extraction

1. Run the Quick-Wins Engine:
   ```powershell
   python seo/seo-suite/gsc/gsc_analyzer.py --input gsc_data.csv --quick-wins
   ```
2. Filter for queries with **Opportunity Score $\ge 100$** (Positions 11.0–20.0 with CTR $< 3\%$):
3. Execute the **4-Step On-Page Boost**:
   - **Title Tag**: Front-load target query in `<title>` (first 35 characters).
   - **H2 & Body**: Integrate natural keyword variation into first H2 and opening 100 words.
   - **Internal Linking**: Add 3 contextual internal links with exact/partial anchor text from authoritative parent pages.
   - **Direct Answer FAQ**: Add a structured FAQ block answering the query in $\le 50$ words.

---

### Phase 4: Re-Indexing & Verification
1. Submit updated URLs for re-indexing via the URL Inspection tool or `sitemap-indexing-automation`.
2. Monitor position delta after 14–21 days; target migration from Page 2 into Top 5 rankings.
