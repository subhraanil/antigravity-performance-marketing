import os
import json
from datetime import datetime
from pmw_article_template import build_pmw_article_html
from deploy_nov24_articles import (
    deploy_to_cpanel,
    verify_live_urls,
    submit_indexnow,
    submit_google_indexing,
)


def make_schema(title, desc, slug):
    return json.dumps({
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": title,
        "description": desc,
        "author": {"@type": "Person", "name": "Subhranil Naskar", "url": "https://paidmediaworld.com/about-us/"},
        "publisher": {
            "@type": "Organization",
            "name": "Paid Media World",
            "logo": {"@type": "ImageObject", "url": "https://paidmediaworld.com/pmw_logo_light_2026.png"},
        },
        "datePublished": "2026-11-25",
        "dateModified": "2026-11-25",
        "mainEntityOfPage": f"https://paidmediaworld.com/{slug}/",
    }, indent=2)


def generate_articles():
    # Article 1: Nov 2026 Core Update Completed + Chrome 158 XSLT Sitemap Fix
    art1_title = "Google November 2026 Core Update Completed + Chrome 158 XSLT Sitemap Fix"
    art1_slug = "google-november-2026-core-update-chrome-158-xslt-sitemap-fix"
    art1_kw = "Google November 2026 core update Chrome 158 sitemap"
    art1_cat = "Technical SEO & Core Updates"
    art1_desc = "Google's November 2026 Core Update finished on Nov 24 right alongside Chrome 158 dropping XSLT sitemap rendering. Separate real ranking shifts from BFCM seasonality and browser quirks."
    art1_body = """
<div class="callout-box">
  <div class="text-xs font-mono uppercase font-bold text-[#0E56A8] mb-2">Executive Triage — November 25, 2026</div>
  <p class="m-0 text-sm text-[#062649] font-medium">
    Google officially completed the <strong>November 2026 Core Update</strong> on <strong>November 24, 2026</strong> after a 14-day rollout (launched Nov 10). Just one week earlier, on <strong>November 17</strong>, <strong>Chrome 158</strong> removed built-in client-side XSLT support—causing WordPress XML sitemaps to render as raw XML code in browsers. Do not confuse either event with a broken site or holiday seasonality.
  </p>
</div>

<h2>1. November 2026 Core Update Timeline &amp; Volatility Signals</h2>
<p>This was Google's third broad core update of 2026 (following March and May), impacting all regions, languages, and content types globally. While Google announced the rollout on November 10, major ranking turbulence did not register clearly across tracking tools until November 13–14, concluding on November 24.</p>
<ul>
  <li><strong>AI Content Scrutiny:</strong> Early post-rollout analysis across the SEO community points to sharp visibility swings for sites that heavily scaled unedited, low-value AI-generated pages lacking original insight.</li>
  <li><strong>No Quick "Penalty Fix":</strong> As with all broad core updates, Google reiterated there is no single technical patch. Recovery depends on long-term content quality, clear intent satisfaction, and demonstrable E-E-A-T.</li>
</ul>

<h2>2. Why Chrome 158 Made Your WordPress XML Sitemap Look "Broken"</h2>
<p>On November 17, 2026, Google Chrome 158 rolled out to stable users and officially deprecated client-side <strong>XSLT (Extensible Stylesheet Language Transformations)</strong>. For years, WordPress core and plugins like Yoast SEO, Rank Math, All in One SEO, and SEOPress injected an <code>.xsl</code> stylesheet reference into <code>/wp-sitemap.xml</code> and <code>/sitemap_index.xml</code> to render raw XML as a styled HTML table.</p>
<ul>
  <li><strong>Your SEO Is 100% Unaffected:</strong> Googlebot and Bingbot read raw XML nodes (<code>&lt;loc&gt;</code>, <code>&lt;lastmod&gt;</code>) directly at the source and never execute browser-side XSLT stylesheets.</li>
  <li><strong>Verify in Google Search Console:</strong> Check <em>Indexing &gt; Sitemaps</em> in GSC and confirm status reads <strong>Success</strong> with expected discovered URL counts. WordPress and major SEO plugins are rolling out CSS/lightweight display updates so human-readable views return in modern browsers.</li>
</ul>

<h2>3. Separating Core Update Drops from Thanksgiving / BFCM Seasonality</h2>
<table>
  <thead>
    <tr><th>Diagnostic Check</th><th>What Seasonality Looks Like</th><th>What a Core Update Shift Looks Like</th></tr>
  </thead>
  <tbody>
    <tr><td><strong>Query Mix</strong></td><td>Commercial &amp; promo terms spike/dip around Nov 26–30</td><td>Evergreen informational &amp; non-branded guides drop uniformly</td></tr>
    <tr><td><strong>Comparison Window</strong></td><td>Week-over-week (WoW) looks distorted by holiday shopping</td><td>Compare non-branded evergreen pages YoY and wait 7 days post-Nov 24</td></tr>
    <tr><td><strong>Action Plan</strong></td><td>Hold steady through Cyber Monday before editing templates</td><td>Consolidate thin scaled subfolders; add primary data &amp; expert authorship</td></tr>
  </tbody>
</table>

<p>Next step: pair your post-update audit with our <a href="/gsc-generative-ai-report-geo-ai-overviews-optimization/" class="text-[#0E56A8] font-semibold underline">GSC Generative AI Report &amp; GEO Optimization Guide</a>.</p>
"""
    html1 = build_pmw_article_html(
        art1_title, art1_slug, art1_kw, art1_cat, art1_desc,
        "8 min read", "November 25, 2026", art1_body,
        featured_image="/uploads/2026/11/seo_core_update_banner.jpg",
    )

    # Article 2: Decoding GSC Generative AI Report & Optimizing for GEO / AI Overviews
    art2_title = "Decoding GSC Generative AI Reports & Optimizing Pages for GEO / AI Overviews"
    art2_slug = "gsc-generative-ai-report-geo-ai-overviews-optimization"
    art2_kw = "GSC generative AI report GEO optimization guide"
    art2_cat = "SEO & AEO / GEO"
    art2_desc = "Learn what Google Search Console's Generative AI Performance Report tracks (and hides), and structure pages to earn citations in AI Overviews and AI Mode."
    art2_body = """
<div class="callout-box">
  <div class="text-xs font-mono uppercase font-bold text-[#0E56A8] mb-2">New Search Reality</div>
  <p class="m-0 text-sm text-[#062649] font-medium">
    Google Search Console's <strong>Search Generative AI Performance Report</strong> isolates your site's visibility inside AI Overviews, AI Mode, and Discover. While zero-click answers absorb informational volume, visitors who click through from AI citations arrive with higher intent and deeper engagement.
  </p>
</div>

<h2>1. What GSC's Generative AI Report Tracks (and What It Hides)</h2>
<table>
  <thead>
    <tr><th>Dimension / Metric</th><th>Available in GSC Generative AI Report?</th><th>Operational Implication</th></tr>
  </thead>
  <tbody>
    <tr><td><strong>Impressions (AI Citations)</strong></td><td>Yes — filterable by page, country, device, date</td><td>Already bundled in total GSC impressions; isolates AI slice</td></tr>
    <tr><td><strong>Clicks, CTR &amp; Avg. Position</strong></td><td>No — not broken out separately</td><td>Measure downstream AI traffic quality via GA4 engagement &amp; conversions</td></tr>
    <tr><td><strong>Exact Triggering Queries</strong></td><td>No — query strings omitted</td><td>Cross-reference landing page URLs with standard GSC query clusters</td></tr>
  </tbody>
</table>

<h2>2. The 2026 GEO Page-Architecture Blueprint</h2>
<p>AI Overviews are grounded heavily in Google's core ranking and quality systems—pages that already rank well organically have a far higher baseline probability of being cited. Structure every commercial and informational guide for clean LLM synthesis:</p>
<ul>
  <li><strong>Direct 2–3 Sentence Answers:</strong> Place a crisp, factual summary immediately under question-framed H2 and H3 headings (<em>"What is..."</em>, <em>"How to..."</em>).</li>
  <li><strong>Scannable Data Structures:</strong> Convert dense paragraphs into bullet lists, numbered steps, and clean HTML comparison tables that RAG retrievers parse reliably.</li>
  <li><strong>E-E-A-T &amp; Schema Markup:</strong> Anchor claims with primary data, clear publication/update dates, and <code>FAQ</code>, <code>HowTo</code>, and <code>Article</code> JSON-LD schema.</li>
</ul>

<h2>3. Local &amp; Small Business AI Discovery Playbook</h2>
<p>For local service operators targeting <strong>$28–$58 Cost Per Booking</strong> and <strong>&ge; 25% booking rates</strong>, winning AI recommendations requires strong entity consensus outside your own site:</p>
<ol>
  <li>Keep your <strong>Google Business Profile</strong> active with accurate categories, services, and steady customer reviews.</li>
  <li>Publish explicit buyer-question pages on your site (pricing ranges, service areas, turnaround times).</li>
  <li>Audit your top 15 local commercial prompts monthly across Google AI Mode, ChatGPT, and Perplexity alongside GSC page-level AI impressions.</li>
</ol>

<p>Explore our <a href="/aeo-survival-guide-zero-click-search/" class="text-[#0E56A8] font-semibold underline">AEO Survival Guide for Zero-Click Search</a> and our <a href="/google-november-2026-core-update-chrome-158-xslt-sitemap-fix/" class="text-[#0E56A8] font-semibold underline">November 2026 Core Update Triage</a>.</p>
"""
    html2 = build_pmw_article_html(
        art2_title, art2_slug, art2_kw, art2_cat, art2_desc,
        "9 min read", "November 25, 2026", art2_body,
        featured_image="/uploads/2026/11/geo_ai_overview_banner.jpg",
    )

    # Article 3: Wiring Marketing MCP Servers to Google Ads, Meta Ads & GA4
    art3_title = "Wiring Marketing MCP Servers to Google Ads, Meta Ads & GA4 Safely"
    art3_slug = "wiring-marketing-mcp-servers-google-ads-meta-ga4-safety"
    art3_kw = "MCP marketing automation Google Ads Meta GA4"
    art3_cat = "AI Marketing Tools & Automation"
    art3_desc = "Connect Google Ads MCP, GA4 MCP, and Meta Ads MCP to Claude, Cursor, or n8n for instant cross-channel diagnostics—with strict read-only and human-in-the-loop budget guardrails."
    art3_body = """
<div class="callout-box">
  <div class="text-xs font-mono uppercase font-bold text-[#0E56A8] mb-2">Agentic Marketing Ops</div>
  <p class="m-0 text-sm text-[#062649] font-medium">
    <strong>Model Context Protocol (MCP)</strong>—the open standard for connecting AI models to live data sources—eliminates manual CSV exports between Google Ads, Meta Ads, and GA4. With official API-backed MCP servers, performance marketers run cross-channel diagnostics in plain English while enforcing strict financial guardrails.
  </p>
</div>

<h2>1. The 2026 Marketing MCP Ecosystem</h2>
<ul>
  <li><strong>Google Ads MCP:</strong> Officially supported and open-sourced by Google, bridging the Google Ads API via GAQL (Google Ads Query Language) to pull campaign metrics, wasted search terms, and asset/label states.</li>
  <li><strong>GA4 MCP:</strong> Queries real-time traffic, event funnels, and conversion paths directly into your AI workspace.</li>
  <li><strong>Meta Ads MCP &amp; Unified Connectors:</strong> Connects Meta Marketing API delivery/spend data alongside store/CRM platforms (such as Shopify) via self-hosted configs or unified servers like GoMarble MCP.</li>
</ul>

<h2>2. High-ROI Cross-Channel Diagnostic Prompts</h2>
<pre><code>"Pull a GAQL query via Google Ads MCP for search terms with &gt;$100 spend and 0 conversions over the last 14 days, then cross-reference Meta Ads ROAS and GA4 key events to show which channel drove the highest-value checkouts."</code></pre>
<p>Instead of building brittle one-off scripts, teams connect these servers to Claude, ChatGPT, Cursor, or n8n—deploying either via self-hosted Cloud Run / local <code>claude_desktop_config.json</code> with OAuth + developer tokens, or via hosted OAuth MCP registries.</p>

<h2>3. Non-Negotiable Budget &amp; Policy Guardrails</h2>
<table>
  <thead>
    <tr><th>Risk Area</th><th>Unsafe Pattern</th><th>Production Guardrail</th></tr>
  </thead>
  <tbody>
    <tr><td><strong>Live Budget Mutations</strong></td><td>Granting unrestricted write access to bids/budgets</td><td>Default to <strong>Read-Only</strong> or <strong>Propose-and-Confirm</strong>; stage new builds <code>PAUSED</code></td></tr>
    <tr><td><strong>Scaling Volatility</strong></td><td>Automated intraday budget swings &gt;20%</td><td>Cap scaling recommendations at <strong>&le; 20% per 72 hours</strong> per campaign</td></tr>
    <tr><td><strong>Platform Terms of Service</strong></td><td>Browser-UI scraping agents clicking Ads Manager</td><td>Use <strong>official API-backed MCP servers</strong> exclusively</td></tr>
  </tbody>
</table>

<p>Read our <a href="/google-november-2026-core-update-chrome-158-xslt-sitemap-fix/" class="text-[#0E56A8] font-semibold underline">November 2026 Core Update &amp; Sitemap Guide</a> or explore our <a href="/marketing-calculators/" class="text-[#0E56A8] font-semibold underline">Performance Marketing Calculators</a>.</p>
"""
    html3 = build_pmw_article_html(
        art3_title, art3_slug, art3_kw, art3_cat, art3_desc,
        "10 min read", "November 25, 2026", art3_body,
        featured_image="/uploads/2026/11/mcp_marketing_automation_banner.jpg",
    )

    return [
        {"slug": art1_slug, "title": art1_title, "html": html1},
        {"slug": art2_slug, "title": art2_title, "html": html2},
        {"slug": art3_slug, "title": art3_title, "html": html3},
    ]


if __name__ == "__main__":
    articles = generate_articles()
    deployment_results = deploy_to_cpanel(articles)
    verify_live_urls(deployment_results)

    live_urls = [r["url"] for r in deployment_results if r.get("verified")]
    if live_urls:
        submit_indexnow(live_urls)
        submit_google_indexing(live_urls)
        from update_blog_index import sync_blog_indexes
        sync_blog_indexes()

    log_file = r"C:\Users\test\Videos\Personal\reports\publishing-log-2026-11-25.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "deployed_articles": deployment_results,
        }, f, indent=2)
    print(f"[DONE] Log written to {log_file}")
