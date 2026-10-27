---
description: Daily LinkedIn Lead Generation & Connection Management
---

This workflow automates the process of checking your LinkedIn for invitations and scouting the feed for Google/Meta Ads opportunities.

### Steps:

1. **Check Prerequisites**:
   - Ensure the `.env` file has a valid `GOOGLE_API_KEY`.
   - Ensure `playwright` is installed (`pip install playwright`).

2. **Run the Automation**:
// turbo
   ```powershell
   python linkedin_leads.py
   ```

3. **Handle First-Time Login**:
   - If the script detects you are not logged in, it will open a browser window.
   - **Log in manually** to your LinkedIn account.
   - The script saves your session in the `.linkedin_profile` folder, so you won't need to log in again.

4. **Review and Reach Out**:
   - After the script finishing, open `linkedin_report.html` in your browser.
   - Review the generated personalized messages.
   - The script automatically "Likes" the posts it identifies as leads.
   - You can manually click the links in the report to send the draft messages or verify the leads.

### Safety Note:
This script is designed to be low-volume (checking top results for 5 keywords) to respect LinkedIn's rate limits. Do not run it more than 1-2 times per day.
