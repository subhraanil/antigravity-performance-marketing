---
name: wordpress-blog-publishing-sop
description: >-
  End-to-end SOP to research, outline, write, format, publish via WordPress REST API or Admin UI, and immediately submit articles for Google Search Console indexing across Paid Media World and client sites.
---

# Automated WordPress Blog Publishing & Indexing SOP

## Overview
A production standard operating procedure to research, outline, write, format, publish via the WordPress REST API (or Admin UI fallback), and submit new articles for immediate Google Search Console indexing.

---

## Trigger Conditions
- Weekly content publishing schedule.
- High-priority trending keyword or industry breaking news ("Information Gain" opportunity).
- Pillar-and-spoke topical cluster expansion.

---

## Step-by-Step SOP

### Step 1: Trending Research & Topic Discovery
1. **Source Discovery**: Audit recent posts and trending topics from industry RSS feeds and authoritative blogs:
   - Google Search Central Blog (`https://blog.google/rss/`)
   - Search Engine Land (`https://searchengineland.com/feed/`)
   - Search Engine Journal (`https://www.searchenginejournal.com/feed/`)
   - Ahrefs Blog (`https://ahrefs.com/blog/feed/`)
2. **Information Gain Filter**: Propose 3–5 expert topic angles that add original data, fresh commentary, or proprietary workflows not already saturated in the SERP.
3. **Keyword Selection**: Pair each concept with 1 primary intent keyword and 3–5 semantic secondary keywords.

---

### Step 2: Content Architecture & Drafting
1. **Structure & Formatting Requirements**:
   - **Catchy, Keyword-Rich Title**: H1 containing the primary keyword.
   - **Meta Description**: 150–160 characters, high-CTR hook with primary keyword.
   - **Word Count**: Comprehensive long-form (1,200–2,500+ words) tailored to search intent.
   - **Heading Hierarchy**: Semantic H2/H3 tags with direct answers placed in first 50 words under each H2.
   - **Key Takeaways Box**: Placed directly after the introduction.
   - **Comparison Table / Steps**: At least one Markdown table or ordered action checklist.
   - **Call-to-Action (CTA)**: Contextual hyperlinked CTA pointing to contact or lead capture page.
   - **Taxonomy**: 1–2 primary Categories and 5–8 relevant Tags.

---

### Step 3: WordPress Publishing

#### Method A: Headless REST API (Recommended)
1. Read target credentials from environment (`WP_URL`, `WP_USER`, `WP_APP_PASSWORD`).
2. Post article with proper JSON payload:
   ```python
   import requests
   
   headers = {'Content-Type': 'application/json'}
   payload = {
       'title': article_title,
       'content': html_body,
       'status': 'publish',
       'categories': [category_id],
       'tags': tag_ids,
       'meta': {'_yoast_wpseo_metadesc': meta_description}
   }
   res = requests.post(f"{wp_url}/wp-json/wp/v2/posts", json=payload, auth=(wp_user, wp_app_pass), headers=headers)
   live_url = res.json().get('link')
   ```

#### Method B: Browser Subagent Admin UI (Fallback)
1. Navigate to `/wp-admin/` and authenticate with user credentials.
2. Go to **Posts > Add New**.
3. Inject Title, Gutenberg/HTML content, Categories, and Tags.
4. Set Featured Image and Meta Description via SEO plugin box (Yoast / RankMath).
5. Click **Publish** and capture the live permalink URL.

---

### Step 4: Instant Google Indexing Submission
Immediately push the new live post URL to Googlebot for instant crawling:
```powershell
python scripts/submit_indexing.py --url "LIVE_POST_URL"
```

---

### Step 5: Verification & Social Syndication
1. Verify live URL responds with HTTP 200 and schema renders cleanly.
2. Queue snippet for LinkedIn lead generation and newsletter syndication.
