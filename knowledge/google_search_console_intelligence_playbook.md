# Google Search Console (GSC) Intelligence Playbook

## Executive Overview

Google Search Console is the definitive single source of truth for organic search performance. This playbook outlines automated analytical procedures to resolve **keyword cannibalization**, capture **striking-distance quick-wins (positions 11.0–20.0)**, and monitor **period-over-period search variance**.

---

## 1. GSC Python MCP Server Architecture

The workspace integrates a standalone Google Search Console MCP Server located at [`seo/mcp-gsc/gsc_server.py`](file:///C:/Users/test/.gemini/antigravity/scratch/antigravity-performance-marketing/seo/mcp-gsc/gsc_server.py):
- **Server Name:** `mcp-search-console`
- **Supported Capabilities:**
  - `gsc_query_performance`: Clicks, impressions, CTR, and average position filtered by date range, query, page, device, and country.
  - `gsc_inspect_url`: Real-time indexation status, mobile usability, canonical status, and AMP validity.
  - `gsc_list_sites`: List all verified web properties in the connected Google account.
- **Standalone Command Alternative:**
  - `python seo/seo-suite/gsc/gsc_analyzer.py --sample`
  - `python seo/seo-suite/gsc/gsc_analyzer.py --input <gsc_export.csv> --cannibalization --quick-wins`

---

## 2. Keyword Cannibalization Detection & Remediation Engine

Keyword cannibalization occurs when multiple URLs on the same root domain compete in Google's index for identical search queries, splitting link equity, confusing search crawlers, and suppressing maximum rank potential.

### Detection Algorithm:
1. Group GSC search data by `query`.
2. Filter for queries where `unique(page_url) >= 2`.
3. Compute total impressions at stake:
   $$\text{Impressions At Stake} = \sum_{i=1}^{n} \text{Impressions}(Page_i)$$
4. Identify `Primary Page` (page with highest clicks or lowest average position) and `Competing Page(s)`.
5. Classify Severity:
   - **Critical:** Impressions at stake $\ge 10,000$ and top position between 4.0 and 15.0.
   - **High:** Impressions at stake between 2,500 and 9,999.
   - **Medium:** Impressions at stake $< 2,500$.

### Remediation Decision Matrix:

```
                  Does competing page provide unique business value?
                                    /               \
                                  YES                NO
                                  /                    \
              Do intents fundamentally differ?     Is competing page redundant?
                     /               \                         |
                   YES                NO                      YES
                   /                    \                      |
           Differentiate Content    Consolidate / Canonical   301 Permanent Redirect
          Target distinct queries    Keep page live, point     Pass 100% PageRank
          Update internal links      rel="canonical" to        equity to primary page
                                     Primary URL
```

1. **301 Permanent Redirect:**
   - Use when the competing page has no unique conversion purpose and represents duplicate or outdated coverage.
2. **Canonical Tag (`rel="canonical"`):**
   - Use when the competing page must remain visible to users (e.g. promotional landing page or variant) but Google should only index the primary hub.
3. **Intent Differentiation & De-optimization:**
   - Adjust H1, title tag, and body copy on the secondary page to target a separate long-tail sub-topic, removing exact-match target anchors pointing to it.

---

## 3. Striking-Distance Quick-Wins (Positions 11.0–20.0)

Keywords ranking on Page 2 of Google SERPs represent low-hanging fruit. Moving from Position 12 to Position 4 can increase CTR by 500% to 1,200% with minimal resource expenditure.

### The Opportunity Score Formula:
ApexLink prioritizes queries using the **Expected Click Capture Potential**:

$$\text{Opportunity Score} = \text{Impressions} \times \left(0.05 - \text{CTR}\right)$$

*Where:*
- $\text{Position} \in [11.0, 20.0]$
- $\text{Impressions} \ge 100$
- $\text{CTR} < 3\%$

### 4-Step Striking Distance Escalation Protocol:
1. **Title & Meta Tag Refresh**: Insert exact query in the first 30 characters of the `<title>` tag.
2. **First 100-Word Injection**: Include query naturally in the opening paragraph and under an `<h2>` heading.
3. **Internal Link Boost**: Point 3–5 internal contextual links from high-authority existing pages (e.g., homepage or top-ranking blog posts) with exact or partial match anchor text.
4. **Rich Content Expansion**: Add a concise FAQ or data table directly addressing the query to win Featured Snippets / AI Overviews.

---

## 4. Period-over-Period Performance Comparison

Compare current 28 days vs previous 28 days (or year-over-year) to isolate systemic ranking movements from seasonal demand shifts:
- **Click Velocity ($\Delta Clicks$):** $\frac{\text{Clicks}_{\text{current}} - \text{Clicks}_{\text{previous}}}{\text{Clicks}_{\text{previous}}} \times 100$
- **Impression Delta ($\Delta Impressions$):** Measures changes in overall search visibility and indexation.
- **Position Stability ($\Delta Position$):** Flag any query dropping by $\ge 3.0$ positions for immediate forensic inspection.
