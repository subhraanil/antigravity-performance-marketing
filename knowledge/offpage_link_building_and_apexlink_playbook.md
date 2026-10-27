# Off-Page Link Building & ApexLink Pro Playbook

## Executive Overview

**ApexLink Pro** is an enterprise-grade, Penguin-safe autonomous link building and off-page authority framework. Rather than engaging in black-hat PBNs, link farms, or paid link schemes that risk manual actions and algorithmic penalties, ApexLink operates strictly on **legitimate white-hat digital PR, high-authority curated platform directories, zero-leak linkable statistics assets, and competitor link gap reclamation**.

---

## 1. Multi-Source Backlink Profile Intelligence & Health Scoring (0–100)

ApexLink calculates an objective 0–100 Backlink Health Score across 7 critical dimensions with confidence-weighted multi-source data:

$$\text{Weighted Score} = \frac{\sum (\text{factor\_score} \times \text{factor\_weight} \times \text{confidence})}{\sum (\text{factor\_weight} \times \text{confidence})}$$

### Seven Evaluated Dimensions:
1. **Referring Domain Volume & Velocity (Weight: 20%)**: Steady, organic link velocity without unnatural spikes.
2. **Domain Rating / Authority Distribution (Weight: 20%)**: Proportional distribution across DR tiers (Tier 1: DR 80+, Tier 2: DR 60–79, Tier 3: DR 40–59, Tier 4: DR < 40).
3. **Anchor Text Naturalness (Weight: 20%)**: Compliance with Penguin-proof anchor distributions.
4. **Toxic Link & Link Farm Ratio (Weight: 15%)**: Detection of automated spam, link schemes, and casino/pharma injections.
5. **Dofollow vs Nofollow Ratio (Weight: 10%)**: Natural balance (optimal: 65%–85% dofollow).
6. **Domain Diversity (Weight: 10%)**: Backlink-to-referring-domain ratio (< 5:1 preferred).
7. **TLD Diversity (Weight: 5%)**: Healthy geographic distribution (.com, .org, .io, country-specific ccTLDs).

### Benchmark Anchor Distribution (Penguin-Proof)
- **Branded (Company, Product, Founder):** 35% – 55%
- **Naked URL (`https://...`):** 15% – 25%
- **Generic ("click here", "visit website"):** 10% – 20%
- **Exact-Match Target Keywords:** 2% – 8% (*Over-optimization flag triggered if > 15%*)
- **Partial-Match Keywords:** 8% – 18%
- **Natural Longtail / Citations:** 5% – 15%

---

## 2. 30-Pattern Toxic Link Remediation & Disavow Engine

When unnatural backlink profiles are detected, ApexLink enforces automated remediation:
- **Scan Triggers**: Link farm density (>1,000 outbound links/page), deindexed domains, burner site footprints, compromised pharma/casino injections, unmoderated blog comments, and Chinese/Russian PBN networks.
- **Remediation Threshold**: If toxic domains exceed 2% of total referring domains, auto-generate a sanitized Google Disavow file:
```text
# ApexLink Penguin-Safe Disavow List - Generated 2026-10-27
domain:spamsite1.xyz
domain:linkfarm2.net
domain:badpbnnetwork.ru
```
- **Execution Script**: `python seo/link-building/scripts/link_audit.py --input <backlinks.csv> --disavow disavow.txt`

---

## 3. Curated 745+ Master Platform & High-Authority Directory Database

Pre-verified database located at [`seo/link-building/data/master_directories.json`](file:///C:/Users/test/.gemini/antigravity/scratch/antigravity-performance-marketing/seo/link-building/data/master_directories.json):
- **Tier 1 (DR 80+): 47 Mega-Authority Platforms**:
  - G2, Crunchbase, GitHub, Medium, Substack, Linktree, Devpost, AlternativeTo, Trustpilot, ProvenExpert, StackShare, Brownbook, etc.
- **Tier 2 (DR 60–79): 56 High-Authority Niche Platforms**:
  - Product Hunt, SaaSHub, Futurepedia, TopAI.tools, Pitchwall, DokeyAI, Dang.ai, StartupStash, FutureTools, etc.
- **Tier 3 (DR 40–59): 32 Verified Directory Engines**:
  - Uneed, Devhunt, Supertools, FiveTaco, SpotSaaS.
- **Tier 4 (DR < 40): 533 Curated Directories**:
  - Long-tail vertical & regional business indexes.
- **102 Verified Dofollow Sources** passing direct PageRank equity.

### Dual-Track Submission Protocol:
- **Track A (High-Throughput Batch)**: Automated URL normalization, hash-based idempotency keys, verification-first preflight (isolating CAPTCHAs into a dedicated human queue without blocking the batch).
  - CLI: `python seo/link-building/scripts/directory_engine.py shard --product-id <id> --shard-size 10`
- **Track B (High-Trust Quality Editorial)**: Micro-batches of $\le 10$ sites, 7-point editorial quality screening, and human authorization checkpoints (inspect $\to$ register $\to$ fill $\to$ agree $\to$ submit).

---

## 4. Digital PR & Journalist Pitching Engine (Qwoted, HARO, Connectively)

Connects to journalist request ecosystems using a 4-stage playbook:

### Stage-3 Linkable Asset Heuristic Scoring:
Every journalist query is scored before pitching:
- Broad topic with public data available: **+2**
- User's business directly touches topic: **+2**
- Request explicitly asks for statistics, data, or research: **+3**
- Deadline $\ge 24$ hours: **+1**
- Tight deadline (<12 hours): **-3**
- Founder personal anecdote / opinion only: **-3**
- Paid / sponsored listing: **-2**

**Rule:** Score $\ge 2$ triggers **BUILD_STATS_PAGE**; Score $< 2$ triggers **PITCH_DIRECTLY**.
- CLI: `python seo/link-building/scripts/pr_pitch_engine.py --topic <topic> --ask <ask> --framework data_anchor`

---

## 5. The "Juice-Hoarding" Linkable Asset Engine (Zero-Leak Statistics Pages)

Journalists and industry bloggers consistently search for `"[industry] statistics [current year]"` to cite in their articles. Citing your statistics page creates high-DR, permanent editorial backlinks.

### Architectural Rules for Statistics Assets:
1. **Zero External Outbound Links**: Keep PageRank equity completely internal; do not leak link juice to external sources.
2. **Proprietary Research & Visual Charts**: Include interactive charts (Chart.js), data cards, and key takeaways.
3. **Structured Dataset & WebPage Schema**: Rich JSON-LD markup allowing Google Dataset Search and search engine knowledge graphs to parse data points directly.
4. **Copy Citation Snippets**: Provide one-click "Copy Citation" buttons formatted in APA, MLA, and web markdown formats.
- CLI: `python seo/link-building/scripts/stats_asset_generator.py --topic <topic> --brand <name> --url <url>`

---

## 6. Competitor Link Gap & 404 Broken-Link Reclamation

1. **Competitor Intersect Algorithm**:
   - Compares referring domains of top 3 search competitors against target domain.
   - Filters for domains linking to $\ge 2$ competitors but *not* your brand.
   - Calculates Priority Score based on DR, competitor intersect count, and relevance.
   - CLI: `python seo/link-building/scripts/competitor_gap.py --target target_links.csv --competitors comp1.csv comp2.csv`
2. **Broken Link Poaching**:
   - Crawl competitor backlink profiles for target URLs returning HTTP 404 or 410.
   - Reach out to linking webmasters offering your superior, active asset as a drop-in replacement.

---

## 7. Deterministic Live Verification Crawler

Verifies that submitted or outreach backlinks are live, indexable, and passing equity:
- Verifies HTTP 200 OK status.
- Inspects DOM for `<a>` tags targeting domain.
- Validates anchor text and detects `rel="nofollow"`, `rel="sponsored"`, `rel="ugc"`, or dofollow equity.
- Verifies meta robots tag does not include `noindex`.
- CLI: `python seo/link-building/scripts/link_verifier.py --source <page_url> --target <your_domain>`
