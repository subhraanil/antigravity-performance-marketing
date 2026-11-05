# Workflow: Automated WordPress Blog Publishing & Indexing SOP

## Overview
A production standard operating procedure to research, outline, write, format, publish via the WordPress REST API, and submit new articles for immediate Google Search Console indexing.

---

## Trigger Conditions
- Weekly content publishing schedule.
- High-priority trending keyword or industry breaking news ("Information Gain" opportunity).
- Pillar-and-spoke topical cluster expansion.

---

## Step-by-Step SOP

### Step 1: Trending Research & Topic Selection
1. **Source Discovery**: Audit recent posts and trending topics from industry RSS feeds and authoritative blogs:
   - Google Search Central Blog (`https://blog.google/rss/`)
   - Search Engine Land (`https://searchengineland.com/feed/`)
   - Search Engine Journal (`https://www.searchenginejournal.com/feed/`)
2. **Information Gain Proposal**: Formulate 3–5 specific topic proposals addressing gaps in existing competitor coverage.
3. **Keyword Mapping**: Define primary target keyword, 3–5 secondary semantic keywords, and search intent (Informational / Commercial).

### Step 2: Competitor Reverse-Engineering & Content Depth
1. Inspect the top 10 search results on Google for the primary keyword.
2. Audit competitor content metrics:
   - Average word count and reading grade level.
   - Heading architecture (H2/H3 distribution).
   - Media richness (diagrams, tables, infographics, original data).
3. **Target Word Count**:
   - *Low Competition*: $\ge 1,200$ words.
   - *Medium Competition*: $\ge 2,000$ words.
   - *High Competition*: $3,000 - 5,000+$ words.
4. **Information Gain Standard**: Ensure article includes original data, verified case studies, or a proprietary framework not present on competing URLs.

### Step 3: Drafting & 2026 SEO Formatting Rules
1. **Title Tag**: $< 60$ characters, front-loaded with primary keyword, high CTR modifier.
2. **Meta Description**: 140–160 characters with primary keyword, core benefit, and action-oriented CTA.
3. **Body Architecture**:
   - Do NOT include an `<h1>` in the body HTML (the WordPress theme automatically renders the title as H1).
   - Begin with a direct answer or problem summary within the first 60 words.
   - Insert Table of Contents (TOC) with anchor jump links.
   - Structure H2 sections following the flow: **Problem $\to$ Technical Explanation $\to$ Actionable Solution $\to$ Field Example $\to$ Expert Pro-Tip**.
4. **HTML Hygiene**:
   - Use `<strong>` and `<em>` tags instead of raw markdown `**`.
   - Ensure `<p>`, `<li>`, `<td>`, and `<h2>` elements contain clean, continuous HTML strings.
   - Add 5–15 internal links pointing to relevant cluster articles (1 link every 400–600 words).
   - Embed 5–10 structured FAQs at the bottom with valid `FAQPage` JSON-LD schema.

### Step 4: WordPress REST API Publishing
1. Authenticate via Application Passwords or OAuth (stored in `.env` as `WP_APP_USER` and `WP_APP_PASSWORD`):
   ```bash
   python execution/wp_api_publisher.py \
     --title "POST_TITLE" \
     --slug "post-slug-url" \
     --content-file "temp_blog_post.html" \
     --categories "Digital Marketing,SEO" \
     --tags "meta ads,performance marketing,growth" \
     --featured-image "assets/featured_hero.png" \
     --status "publish"
   ```
2. Capture the returned live post URL.

### Step 5: Immediate Search Console Indexing Submission
1. Submit the new live URL directly to the Google Indexing API / Search Console:
   ```bash
   python tools/indexing/submit_indexing.py --url "https://domain.com/blog/new-post-slug/"
   ```
2. Confirm HTTP 200 response from Indexing API.
