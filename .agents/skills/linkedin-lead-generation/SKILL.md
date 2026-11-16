---
name: linkedin-lead-generation
description: >-
  Automate daily B2B lead generation, connection management, and feed opportunity scouting for Google and Meta Ads services.
---

# Daily LinkedIn Lead Generation & Connection Management

This workflow automates the process of checking your LinkedIn for invitations, scouting the feed for Google/Meta Ads intent opportunities, and queueing personalized outreach.

---

### Prerequisites
1. Ensure the `.env` file contains a valid `GOOGLE_API_KEY`.
2. Ensure Playwright is installed:
   ```powershell
   pip install playwright
   playwright install
   ```

### Execution Steps

1. **Run the Automation Scout**:
   ```powershell
   python linkedin_leads.py
   ```

2. **First-Time Authentication**:
   - If not authenticated, a browser window will open automatically.
   - Log in manually to your LinkedIn account.
   - The session state is saved to `.linkedin_profile` for headless automated subsequent runs.

3. **Lead Review & Outbound Engagement**:
   - Once the scan finishes, open `linkedin_report.html` in your browser.
   - Review personalized message drafts generated for high-intent posts.
   - Posts identified as warm leads are automatically liked to initiate social proximity.
   - Click links directly from the report to verify profiles and send curated outreach messages.

### Safety Guardrails
- **Rate-Limiting**: Low-volume execution (top results across 5 priority keywords) respecting LinkedIn terms of service.
- **Cadence**: Maximum 1–2 automated runs per calendar day.
