---
description: Get website performance details using Google Search Console API
---

This workflow queries the Google Search Console API for performance data such as clicks, impressions, CTR, and position.

### Prerequisites

1.  **Credentials**: Ensure `credentials.json` is present in the root directory.
2.  **Authentication**: The first time you run this, a browser window will open for you to authenticate with your Google account.

### How to run

Run the `gsc_performance.py` script with the required arguments.

**Arguments:**

*   `--site-url`: The full URL of your property in Google Search Console (e.g., `https://www.example.com/` or `sc-domain:example.com`).
*   `--start-date`: Start date in `YYYY-MM-DD` format.
*   `--end-date`: End date in `YYYY-MM-DD` format.
*   `--dimensions`: (Optional) Comma-separated list of dimensions to group by. Options: `date`, `query`, `page`, `country`, `device`. Default is `date`.
*   `--limit`: (Optional) Maximum number of rows to return. Default is `1000`.

**Example Usage:**

To get the top queries for the last 7 days:

```bash
python scripts/gsc_performance.py --site-url "https://YOUR_SITE_URL" --start-date "2023-10-01" --end-date "2023-10-07" --dimensions "query" --limit 10
```

To get daily performance data:

```bash
python scripts/gsc_performance.py --site-url "https://YOUR_SITE_URL" --start-date "2023-10-01" --end-date "2023-10-07" --dimensions "date"
```
### General Note
- If finding relevant images from Google is getting difficult during any part of this workflow, you can generate them using **Google nano banana** (via the `generate_image` tool).
