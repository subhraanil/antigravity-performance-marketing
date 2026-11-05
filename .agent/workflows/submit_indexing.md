---
description: Submit URLs to Google Indexing API for crawling and indexing
---

This workflow allows you to notify Google when you add or remove pages from your site, submitting them directly to the Google Indexing API. This is faster than waiting for Googlebot to crawl your sitemap.

### Prerequisites

1.  **Service Account**: You must have a Google Cloud Service Account with the "Indexing API" enabled.
2.  **Key File**: Download the JSON key file for your service account and place it in your project root (e.g., `service_account.json`), or specify its path when running the script.
3.  **Search Console Verification**: Verify ownership of your site in Google Search Console using the SAME service account email address as an "Owner".

### How to run

Run the `submit_indexing.py` script with the URL you want to index.

**Arguments:**

*   `--url`: (Required) The full URL to submit (e.g., `https://www.example.com/new-page`).
*   `--action`: (Optional) `URL_UPDATED` (default) or `URL_DELETED`. Use `URL_UPDATED` for new or modified pages, and `URL_DELETED` for removed pages.
*   `--key-file`: (Optional) Path to your service account JSON key file. Defaults to `service_account.json` in the current directory.

**Example Usage:**

To submit a new or updated URL:

```bash
python scripts/submit_indexing.py --url "https://www.example.com/my-new-page"
```

To remove a URL from the index:

```bash
python scripts/submit_indexing.py --url "https://www.example.com/old-page" --action URL_DELETED
```

**Troubleshooting:**

*   **403 Permission Denied**: Ensure you have added the service account email (client_email in the JSON file) as a delegated owner in Google Search Console for the property.
*   **404 Not Found**: Ensure the Indexing API is enabled in your Google Cloud Console project.

---
**Note**: If finding relevant images from Google is getting difficult for you during any step, you can just generate those relevant images using **Google nano banana** (via the `generate_image` tool).
