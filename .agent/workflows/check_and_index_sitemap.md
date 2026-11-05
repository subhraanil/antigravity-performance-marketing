---
description: Check GSC indexing status for all sitemap URLs and submit unindexed ones to Google Indexing API
---

This workflow automates the process of checking which URLs from a sitemap are already indexed in Google Search Console and then submitting any unindexed URLs to the Google Indexing API for faster indexing.

### Prerequisites

1.  **Service Account**: You must have a Google Cloud Service Account with BOTH the "Indexing API" and the "Search Console API" enabled.
2.  **Key File**: Download the JSON key file for your service account and place it in your project root (e.g., `service_account.json`).
3.  **Search Console Verification**: 
    - Verify ownership of your site in Google Search Console.
    - Add the service account email (found in the JSON key file) as a **Temporary Owner** or **Owner** in Google Search Console to allow it to inspect URLs.

### How to run

Run the `check_and_index_sitemap.py` script.

**Arguments:**

*   `--sitemap`: (Required) The full URL of the sitemap XML (e.g., `https://paidmediaworld.com/post-sitemap.xml`).
*   `--site-url`: (Required) The GSC property URL (e.g., `https://paidmediaworld.com/`).
*   `--key-file`: (Optional) Path to your service account JSON key file. Defaults to `service_account.json` in the current directory.
*   `--dry-run`: (Optional) If set, the script will only check indexing status but will NOT submit to the Indexing API.
*   `--delay`: (Optional) Seconds to wait between API calls to avoid rate-limiting. Default is 1.5.

**Example Usage:**

To check and submit unindexed URLs:

// turbo
```bash
python scripts/check_and_index_sitemap.py --sitemap "https://paidmediaworld.com/post-sitemap.xml" --site-url "https://paidmediaworld.com/"
```

To just check status (dry-run):

```bash
python scripts/check_and_index_sitemap.py --sitemap "https://paidmediaworld.com/post-sitemap.xml" --site-url "https://paidmediaworld.com/" --dry-run
```

### Outputs

- **Console Output**: A live table showing each URL and its status (`[INDEXED]` or `[NOT INDEXED]`).
- **Summary**: A count of total, indexed, and unindexed URLs.
- **Report**: A detailed JSON report is saved to `reports/indexing_report.json`.
