---
name: sitemap-indexing-automation
description: >-
  Audit GSC indexing status for sitemap URLs, submit unindexed URLs in bulk, and instantly notify Google Indexing API for single or updated URLs.
---

# Sitemap Indexing Audit & Google Indexing Automation

This unified skill automates Google indexing across two primary operational modes:
1. **Mode A (Sitemap Bulk Audit & Sync)**: Audits all URLs in a sitemap against Google Search Console and submits all unindexed URLs in batches.
2. **Mode B (Instant URL Notification & Removal)**: Immediately notifies the Google Indexing API of newly published or updated individual URLs (`URL_UPDATED`) or deleted URLs (`URL_DELETED`).

---

### Prerequisites & Google Cloud Setup

1. **Google Cloud Project**: Enable both the **Webmaster Tools / Search Console API** and the **Google Indexing API** in your Google Cloud Console.
2. **Service Account Key**: Download your service account JSON key file and place it in the project root as `service_account.json` (or specify `--key-file`).
3. **Search Console Delegated Ownership**:
   - Open [Google Search Console](https://search.google.com/search-console).
   - Navigate to **Settings > Users and permissions**.
   - Add the service account email (from your JSON key) as an **Owner** or **Full User** for the target property.

---

### Mode A: Sitemap Audit & Batch Indexing

Scan a sitemap XML, check the live indexing status of each URL via the GSC URL Inspection API, and submit unindexed pages:

```powershell
python scripts/check_and_index_sitemap.py \
  --sitemap "https://example.com/sitemap.xml" \
  --site-url "https://example.com/" \
  --delay 1.5
```

**CLI Arguments**:
- `--sitemap`: (Required) Full URL to the sitemap XML (e.g. `https://example.com/post-sitemap.xml`).
- `--site-url`: (Required) The verified GSC property URL (e.g. `https://example.com/`).
- `--dry-run`: (Optional) Inspect and report indexing status without submitting to the Indexing API.
- `--delay <seconds>`: Interval between API calls (default: `1.5`s) to avoid rate limits.
- `--key-file <path>`: Path to service account JSON (default: `service_account.json`).

**Outputs**:
- Console progress table: `[INDEXED]` vs `[NOT INDEXED]`.
- Summary statistics: Total, Indexed, Unindexed, and Submitted counts.
- Detailed JSON export: `reports/indexing_report.json`.

---

### Mode B: Direct URL Instant Notification & Removal

Instantly push individual high-priority or newly published URLs to Googlebot for immediate crawling:

**Submit or Update URL**:
```powershell
python scripts/submit_indexing.py --url "https://example.com/new-article"
```

**Remove Deleted URL from Index**:
```powershell
python scripts/submit_indexing.py --url "https://example.com/old-page" --action URL_DELETED
```

---

### Troubleshooting
- **403 Permission Denied**: The service account email is not added as an Owner/Delegated Owner in Google Search Console for that property.
- **404 Not Found**: Ensure the Indexing API is enabled in your Google Cloud Console project.
- **Quota Exceeded**: Google Indexing API default quota is 200 URLs/day per project. Use `--delay` and prioritize high-intent URLs.
