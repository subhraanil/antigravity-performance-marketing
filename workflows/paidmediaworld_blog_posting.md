---
description: Automated blog generation, publishing, and indexing workflow for Paid Media World
---

This workflow defines the end-to-end process of researching, analyzing, writing, formatting, publishing, and indexing high-quality, Google-compliant blog posts on Paid Media World.

---

## Workflow Steps

### Step 1: Trending Research & Topic Selection
*   **RSS & Sitemap Auditing:** Use `read_url_content` to fetch recent posts and trending topics from:
    *   Google Blog: `https://blog.google/rss/`
    *   Search Engine Land: `https://searchengineland.com/feed/`
    *   Search Engine Journal: `https://www.searchenginejournal.com/feed/`
    *   Ahrefs: `https://ahrefs.com/blog/feed/`
*   **Topic Suggestion:** Propose 3-5 expert topic ideas based on "Information Gain" opportunities. Include a targeted primary keyword for each.
*   **Approval:** Wait for the user to select the target topic before proceeding.

### Step 2: Competitor Gap Analysis
*   Search the target primary keyword on Google.
*   **Top 10 Analysis:** Read the top 10 search results using `search_web` or `read_url_content`.
*   **Audit Metrics:** Check word count, heading structures, image count, FAQs, internal/external links, and content depth.
*   **Gap Identification:** Note missing details, technical data points, or unanswered questions.
*   **Target Length:** Identify the competition level:
    *   *Low Competition:* Aim for 1,200+ words.
    *   *Medium Competition:* Aim for 2,000+ words.
    *   *High Competition:* Aim for 3,000–5,000+ words.
*   **Goal:** Design an article structure **20% to 30% better** than the best competitor.

### Step 3: Content Structure & Formatting (The 2026 SEO Blog Template)
*   **Title & Slug:** Title must be under 60 characters, CTR-focused, starting with the primary keyword. Slug must be lowercase, short, evergreen, and exclude dates or stop words.
*   **Meta Description:** 140-160 characters, containing the primary keyword + value proposition + CTA.
*   **No H1 in Body:** The theme automatically renders the title as H1. Begin the body directly with the intro paragraph or an `<h2>` heading.
*   **No Inline Featured Image:** Do not place the header image in the body HTML. Pass it via the publisher script API.
*   **No Internal Newlines:** Keep `<p>`, `<li>`, `<td>`, and `<h2>` elements as single continuous lines in the code.
*   **No Markdown Bolding:** Never use `**`. Use `<strong>` for bold text and `<em>` for italics.
*   **No Em-Dashes:** Never use `—`. Use plain dashes `-`, commas, or colons.
*   **SEO Keywords:** Keep primary keyword density at **0.8% - 1.5%**. Integrate 10+ LSI/semantic terms per 1,000 words.
*   **Linking:** Add 5-15 internal links (1 every 400-600 words) and 2-5 authoritative external links.
*   **Layout:** Below the introduction, insert a Table of Contents (TOC). Structure the body using H2 headings that target secondary keywords, and write sections using the **Problem ➔ Explanation ➔ Solution ➔ Example ➔ Expert Tip** flow.
*   **FAQ & Schema:** Add 5-10 FAQs at the end. Prepare FAQ and Article schema markup to embed on the page.

### Step 4: WordPress Publishing (API)
*   Create a temporary HTML file (e.g., `.tmp/temp_blog_post.html`) containing the template-structured payload.
*   **Featured Image Check:** If the post is an update to an existing article, check if a featured image is set. If the featured image is missing (featured media ID is 0) or you are publishing a new post, you must generate a featured image using `generate_image`, upload it, and specify the path in the `--image` parameter of the publisher script.
*   Run the publisher script:
    ```bash
    python execution/wp_api_publisher.py \
      --title "POST_TITLE" \
      --content-file ".tmp/temp_blog_post.html" \
      --slug "evergreen-slug-no-dates-or-years" \
      --image "path/to/featured_image.png" \
      --category "CATEGORY_NAME" \
      --tags "TAG1,TAG2,TAG3" \
      --update # Add if updating an existing post
    ```
*   **Cleanup:** Delete the temporary file immediately after publishing.

### Step 5: Indexing Submission
*   Submit the live URL to Google Indexing API:
    ```bash
    python scripts/submit_indexing.py --url "NEW_POST_URL"
    ```

### Step 6: Reporting
*   Provide the live URL and confirm indexing.
*   Summarize the target keywords, final word count, E-E-A-T elements, internal links, and the FAQ setup used.