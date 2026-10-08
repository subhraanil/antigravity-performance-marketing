# Generative Engine Optimization (GEO) & AI Search (AEO) Playbook
# Scope: Google AI Mode, Google AI Overviews, Perplexity, ChatGPT Search, Claude Search

## 1. The Generative Search Landscape
Generative AI search engines do not merely rank links; they synthesize answers by retrieving semantic facts and entity graphs. Optimizing for AI discovery (AEO/GEO) requires both technical crawlability and dense conceptual clarity.

### Primary AI Search Surfaces:
1. **Google AI Mode**: Full generative conversational interface (distinct from AI Overviews). Renders interactive cards, comparisons, and follow-up prompts.
2. **Google AI Overviews (AIO)**: Featured at the top of traditional SERPs for complex, multi-part, or informational queries.
3. **Perplexity AI**: Academic/live search citations directly referencing primary web sources.
4. **ChatGPT Search**: OpenAI's search engine utilizing live web synthesis and citation chips.

---

## 2. Technical Crawl & AI Crawler Tokens (RFC 9309)

Your `robots.txt` must explicitly govern modern AI crawler user-agents. Disallowing them blocks generative indexing while preserving or harming traditional rankings depending on the crawler.

```txt
# Recommended robots.txt for AI Search Indexing
User-agent: Googlebot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: GPTBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Amazonbot
Allow: /
```

> [!IMPORTANT]
> **JavaScript-Free Content Render**: AI crawlers often do not execute heavy JavaScript bundles during rapid semantic ingestion. Key specifications, pricing, FAQs, and definitions **must** render in the raw initial HTML.

---

## 3. On-Page Content Architecture for AI Answers

### A. The 60-Word Direct Answer Rule
- Position a concise, factual answer within the first 60 words directly beneath the H2 question.
- Avoid preamble phrases like *"In today's fast-paced digital world..."* or *"When it comes to X..."*.
- Format: `[Entity] is [Category Definition] that [Primary Mechanism] to achieve [Specific Outcome].`

### B. Structural Fact Density
- **Comparison Tables**: Use Markdown or semantic HTML `<table>` for head-to-head competitor comparisons. AI engines extract table rows with 80%+ higher citation probability than prose.
- **Unambiguous Numbers & Benchmarks**: Cite exact metrics, percentages, dates, and dosages rather than vague qualifiers like *"significantly faster"* or *"highly effective"*.
- **Ordered Lists for Processes**: Numbered steps (1, 2, 3...) for procedural, how-to, or diagnostic queries.

---

## 4. Schema.org Entity Graph Deployment

Every page should connect into a unified JSON-LD entity graph referencing authoritative Wikidata or Wikipedia URIs:

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://example.com/#organization",
      "name": "Brand Name",
      "url": "https://example.com",
      "sameAs": [
        "https://www.wikidata.org/wiki/Q...",
        "https://www.linkedin.com/company/example"
      ]
    },
    {
      "@type": "Product",
      "@id": "https://example.com/product#product",
      "name": "Product Name",
      "offers": {
        "@type": "Offer",
        "price": "45.00",
        "priceCurrency": "USD",
        "availability": "https://schema.org/InStock"
      },
      "manufacturer": { "@id": "https://example.com/#organization" }
    }
  ]
}
```

---

## 5. AEO/GEO Measurement & Tracking Reality

- **Google Search Console**: The Search Console AI report provides **Impressions only**. It currently *excludes* Clicks and Click-Through Rate (CTR) for AI Overviews.
- **Google Analytics 4**: GA4's default "AI Assistant" referral channel *excludes* native Google AI Mode and AI Overviews. Track generative referrals via custom regex filters on referrer URLs (`chatgpt.com`, `perplexity.ai`, `claude.ai`).
