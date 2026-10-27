# SEO Drift & Regression Monitoring Playbook

## Executive Overview

**SEO Drift** refers to the unintended alteration, degradation, or complete loss of search-critical elements caused by software deployments, CMS theme updates, marketing experimentation, or redesigns. 

Just as software engineers utilize version control, unit tests, and CI/CD pipelines to prevent software bugs, modern search marketing requires **Git-style baselining and automated regression testing** across all core organic landing pages.

---

## 1. The SEO Baseline Engine: What Must Be Tracked

Every baseline captures an immutable snapshot of 10 search-critical attributes:

| Element | Field | Severity if Broken | Potential Organic Impact |
|---|---|---|---|
| **HTTP Status Code** | `status_code` | **Sev 1 (Critical)** | HTTP 404, 500, or redirect chains drop page from index immediately. |
| **Robots Directives** | `meta_robots` / `x_robots_tag` | **Sev 1 (Critical)** | Accidental `noindex`, `nofollow`, or `noarchive` de-indexes the URL. |
| **Canonical URL** | `canonical_url` | **Sev 1 (Critical)** | Canonical self-loops, pointing to staging URLs, or pointing to homepage transfers rank equity away. |
| **Title Tag** | `title` | **Sev 2 (High)** | Truncation, keyword dropping, or generic brand-only title collapses CTR and rankings. |
| **Structured Data** | `schema_json_ld` | **Sev 2 (High)** | Missing `Product`, `FAQPage`, or `Article` schema strips rich snippets in SERPs. |
| **Heading Hierarchy** | `h1`, `h2_list` | **Sev 2 (High)** | Missing H1 or scrambled header levels disrupt semantic page hierarchy. |
| **Meta Description** | `meta_description` | **Sev 3 (Medium)** | Missing or generic meta snippet hurts search snippet CTR. |
| **Hreflang Tags** | `hreflang_tags` | **Sev 2 (High)** | Missing x-default or broken country pairings causes international traffic cannibalization. |
| **Open Graph Tags** | `og_title`, `og_image` | **Sev 3 (Medium)** | Degrades social share preview and dark social distribution. |
| **Internal / External Links**| `link_counts` | **Sev 3 (Medium)** | Sudden loss of internal links destroys PageRank flow to secondary pages. |

---

## 2. Drift Detection & Diff Workflow

```
┌─────────────────────────────────┐
│  Phase 1: Baseline Capture      │  Stored as JSON in `seo_baselines/`
│  (Pre-Deployment Known Good)    │  URL, Timestamp, DOM Fingerprint, Schema
└─────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  Phase 2: Post-Deploy Diff      │  Triggered post-deployment or nightly cron
│  (Live DOM vs Stored Baseline)  │  Compares all 10 tracked elements
└─────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐
│  Phase 3: Severity Triage       │  Sev 1: Block deployment / Emergency Alert
│  & Automated Rollback Action    │  Sev 2: Auto-create remediation ticket
└─────────────────────────────────┘
```

---

## 3. Severity Classification & Triage Protocol

### Sev 1: Critical Emergency (Immediate Alert / Revert)
- **Condition:** Page returns $\ge 400$ error, `noindex` tag detected on indexable page, canonical points to external/staging domain, or `<title>` tag is completely missing.
- **Action:** Revert deployment immediately or execute hotfix within 15 minutes. Notify engineering and marketing lead.

### Sev 2: High Warning (Same-Day Fix)
- **Condition:** Structured data schema fails validation or drops types; primary H1 altered without SEO sign-off; title tag altered and stripped of core keywords; hreflang broken.
- **Action:** Restore previous title/schema within 24 hours to prevent crawler cache refreshes from logging the degraded state.

### Sev 3: Medium Drift (Review Queue)
- **Condition:** Meta description altered; minor image alt text variations; slight change in word count ($\pm 10\%$).
- **Action:** Review during regular weekly sprint.

---

## 4. Operational Commands & Integration

- Capture Baseline: `python seo/seo-suite/audit/site_auditor.py --baseline <url>`
- Compare Baseline: `python seo/seo-suite/audit/site_auditor.py --compare <url>`
- Historical Drift Log: Inspect diff history and change logs in project audit folder.
