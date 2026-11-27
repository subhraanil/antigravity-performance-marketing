# Keyword Research Directive

## Objective
To identify high-volume, semantically relevant keywords for a target seed topic, analyze competitor rankings, and structure keywords into topical clusters to establish Google Search authority.

---

## Inputs
1. **Seed Keyword:** The primary search topic (e.g., "PMax campaigns").
2. **Location:** Target geographic location (defaults to "United States").
3. **Competitor Domain (Optional):** Competitor URL to analyze for content gaps and keyword overlaps.
4. **Drive Folder Link (Optional):** Destination Google Drive folder to store the final report.

---

## Process Flow

### 1. Keyword Retrieval
*   Run the script `execution/keyword_planner.py` using:
    ```
    python execution/keyword_planner.py --seed "[Seed Keyword]" --location "[Location]" --competitor "[Competitor Domain]"
    ```
*   The script queries Google Ads Bid Simulator, Search Console, and Google Trends APIs to fetch related keywords, search volume, CPC, and competition density metrics.

### 2. Intent & LSI Clustering
Group retrieved keywords into search intent buckets to align with Google's Helpful Content guidelines:
*   **Informational (AEO/GEO target):** Questions like "How does Performance Max work?"
*   **Commercial (PPC target):** Comparison terms like "PMax vs Search campaign ROAS."
*   **Transactional (Shopping target):** Direct purchase terms like "PMax optimization services."
Identify semantic (LSI) terms to group keywords into **Topical Clusters** rather than single target keywords.

### 3. Report Generation
*   Run `execution/sheet_handler.py` to create a structured Google Sheet named: `Keyword Research - [Seed Keyword]`.
*   Include the following columns:
    1.  **Keyword:** The target search term.
    2.  **Intent Category:** Informational, Commercial, or Transactional.
    3.  **Avg. Monthly Searches:** Volume indicator.
    4.  **Competition Index:** Bidding density.
    5.  **Low Bid / High Bid:** CPC range indicators.
    6.  **Topical Cluster:** Semantic group identifier.

### 4. File Delivery
*   Output the direct link to the Google Sheet.
*   If `Drive Folder Link` is provided, move the spreadsheet to the specified folder.

---

## Error Handling & Fallbacks
*   **API Quota Limit:** If the Google Ads API threshold is reached, save retrieved data to `.tmp/keywords_[timestamp].csv` and notify the user immediately.
*   **Invalid Location:** If the target location is unrecognized, default to "United States" and warn the user in the output logs.
