# B2B LinkedIn Lead Generation & Social Prospecting Playbook

## Executive Overview

High-ticket B2B consulting, enterprise SaaS, and agency retainers are rarely won through cold mass email spam. This playbook establishes an **Account-Based Marketing (ABM) and social listening framework** that identifies active commercial intent on LinkedIn, monitors inbound connection requests, and initiates data-anchored conversations.

---

## 1. Intent-Based Feed Scouting Architecture

Rather than blasting cold connection requests to random lists, the LinkedIn Lead Scout identifies users actively experiencing marketing bottlenecks or soliciting agency/consultant support.

### High-Intent Search Queries:
- `"looking for a performance marketing agency"`
- `"recommend a media buyer for meta ads"`
- `"google ads consultant needed"`
- `"scaling paid search help"`
- `"fractional CMO for SaaS"`
- `"hire technical SEO expert"`

### Automated Lead Qualification Criteria:
1. **Commercial Trigger:** Post explicitly requests recommendations, shares a marketing frustration, or asks for agency intros.
2. **ICP Alignment:** The author is a Founder, CEO, VP of Marketing, or Growth Director at a company with $\ge 5$ employees.
3. **Engagement Recency:** Post was published within the last 48 hours to ensure first-mover outreach advantage.

---

## 2. Session Persistence & Browser Emulation

To eliminate the need for repeated manual logins and prevent security verification blocks, the scout utilizes persistent browser context:
- **Session Profile:** Saved securely in `.linkedin_profile/` using Playwright persistent storage.
- **Human Emulation:** Random delay intervals (2.5s to 6.8s) between page scrolls and profile views.
- **Safe Rate Limits:** Capped at 15–25 profile checks per day, run at most 1–2 times daily. Never run automated scrapers continuously in loops.

---

## 3. High-Converting Outreach Frameworks

### Framework 1: The Observation-to-Value Bridge
> *"Hi [First Name], saw your post about looking for assistance scaling Meta Ads for [Brand]. We recently conducted a forensic audit on a similar [Industry] account and discovered that 42% of budget was burning on Audience Network and unsegmented device placements. Happy to share our 5-point checklist if you're evaluating approaches—no pitch or obligation."*

### Framework 2: The Direct Competitor Insight
> *"Hi [First Name], noticed you're scaling [Product Category] search campaigns. We recently analyzed search query cannibalization in that space and found competitors were losing ~25% of impressions across overlapping exact-match terms. Put together a 1-page breakdown if you'd like a quick look."*

---

## 4. Operational Workflow & Execution

1. **Prerequisites Check:** Ensure `playwright` is installed.
2. **Execute Automation:**
   ```powershell
   python tools/linkedin/linkedin_leads.py
   ```
3. **HTML Deliverable:** Inspect `linkedin_report.html` to review discovered lead cards, post snippets, and generated draft messages.
4. **Manual Sign-Off:** Review and approve outreach messages manually before dispatching to maintain human relationship authenticity.
