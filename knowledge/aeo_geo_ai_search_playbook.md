# Generative Engine Optimization (GEO) & AI Search (AEO) Playbook
# Scope: Google AI Mode, Google AI Overviews, Perplexity, ChatGPT Search, Claude Search

## Strategic Objective
Position owned websites, entity records, and digital assets to be preferentially indexed, cited, and recommended by generative AI answer engines (ChatGPT Search, Perplexity, Claude, and Google AI Overviews).

---

## 1. The Princeton KDD 2024 Research Benchmarks

Based on the landmark Princeton study (*"GEO: Generative Engine Optimization"*, 10,000 query evaluation across generative engines):

| Technique | Relative Visibility Impact | Implementation Guidance |
|---|:---:|---|
| **1. Cite Authoritative Sources** | **+30% to +115%** | Reference recognized authorities (`.edu`, `.gov`, Gartner, McKinsey, Statista, official docs) |
| **2. Add Concrete Statistics** | **+40%** | Include verified figures, percentages, dates, and quantitative benchmark metrics |
| **3. Verbatim Quotation Addition** | **+30% to +40%** | Attribute verbatim quotes: `"Text" — Name, Role, Organization, Year` |
| **4. Fluency & Conceptual Clarity** | **+15% to +30%** | Direct, clear explanations; front-load direct answers in the first 30% of content |
| **5. Authoritative Tone** | **+6% to +12%** | Confident, expert framing; avoid tentative hedges ("might be", "some think") |
| **6. Keyword Stuffing** | **0% or Negative** | Strictly avoid repetition; modern LLMs detect semantic redundancy and downgrade citation probability |

---

## 2. Robots.txt: AI Search Bots vs. Training Bots

Never make the mistake of blocking all AI bots in `robots.txt` if your objective is organic AI search visibility:

```
┌──────────────────────────────────────────┬──────────────────────────────────────────┐
│        SEARCH & CITATION BOTS            │         TRAINING & HARVEST BOTS          │
│       (ALLOW for AI Discovery)           │       (DISALLOW to Protect Data)         │
├──────────────────────────────────────────┼──────────────────────────────────────────┤
│ • OAI-SearchBot (ChatGPT Search Engine)  │ • GPTBot (OpenAI Model Training)         │
│ • PerplexityBot (Perplexity Engine)      │ • ClaudeBot (Anthropic Model Training)   │
│ • Claude-SearchBot (Claude Search)       │ • Google-Extended (Gemini Model Training)│
│ • Googlebot (Google AI Overviews / Mode) │ • CCBot (Common Crawl Bulk Scraper)      │
└──────────────────────────────────────────┴──────────────────────────────────────────┘
```

### Optimal Production `robots.txt`:
```txt
# Allow Generative Search Retrieval Bots
User-agent: OAI-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Googlebot
Allow: /

# Disallow Training and Scraping Harvesters (Optional Data Protection)
User-agent: GPTBot
Disallow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Google-Extended
Disallow: /

User-agent: CCBot
Disallow: /
```

---

## 3. The `llms.txt` Standard (llmstxt.org)

Serve `/llms.txt` and `/llms-full.txt` at your domain root as a markdown site index engineered specifically for LLM ingestion:
- **Title (H1):** Brand Name
- **Blockquote:** One-sentence summary of the site and core capability
- **Sections (H2):** Thematic collections of links with descriptive context explaining the exact information available at each endpoint

```markdown
# ApexLink Pro

> The enterprise-grade performance marketing and autonomous SEO operating system.

## Documentation & Playbooks
- [/seo/geo]: Complete guide to Generative Engine Optimization benchmarks and AI search crawler access.
- [/seo/link-building]: 745+ curated platform database, Digital PR pitch frameworks, and zero-leak statistics pages.
- [/media-buying/meta]: 5-dimensional Meta Ads forensic audit protocols and scaling guardrails.
```

---

## 4. Google AI Overview (AIO) Readiness Standards

Google's AI Overviews evaluate specific machine-readable trust signals:
- **G-INDEX:** HTTP status 200, no `noindex` directives, accessible to Googlebot.
- **G-SNIPPET:** No restrictive `nosnippet` or `max-snippet:0` directives.
- **G-CANONICAL:** Single absolute canonical tag in `<head>` matching final URL.
- **G-DATES:** Visible on-page publication/update date matching `datePublished` and `dateModified` in JSON-LD.
- **G-BYLINE:** Explicit author name, title, and bio page link matching E-E-A-T credentials.
- **G-SD-VISIBLE:** Structured data `name`, `headline`, and `description` strictly match visible on-page text.

---

## 5. 0–100 GEO Scoring Rubric (Rubric v2)

ApexLink evaluates content across 9 weighted categories:
1. `google_ai` (20 pts): G-INDEX, G-SNIPPET, G-CANONICAL, G-DATES, G-BYLINE, G-LINKS
2. `robots` (14 pts): AI Search bots allowed vs training bot restrictions
3. `schema` (14 pts): JSON-LD entity graph completeness (`Article`, `FAQPage`, `Dataset`)
4. `content` (14 pts): Word count, Princeton statistics count, quote attributions
5. `brand_entity` (12 pts): Knowledge Graph presence, `sameAs` entity identifiers (Wikidata, LinkedIn)
6. `meta` (11 pts): Title, meta description, and OpenGraph clarity
7. `llms` (6 pts): `/llms.txt` presence and standard adherence
8. `signals` (6 pts): Date freshness and language declarations
9. `ai_discovery` (3 pts): Markdown negotiation endpoints

**Execution Engine:** `python seo/seo-suite/geo/geo_engine.py --file <page.html>` or `--sample`
