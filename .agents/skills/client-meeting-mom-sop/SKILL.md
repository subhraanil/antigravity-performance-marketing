---
name: client-meeting-mom-sop
description: >-
  Standard operating procedure to generate client meeting minutes (MOM), action items, and executive HTML reports post-call.
---

# Standard Operating Procedure (SOP) — Client Meeting Minutes of Meeting (MOM)

**Workflow ID:** `client-meeting-mom-sop`  
**Standard:** TechnoExponent Enterprise Delivery Standard  
**Turnaround SLA:** <= 24 Hours post-call  

---

## 1. Scope & Purpose
To guarantee accountability, transparency, and flawless execution for all client syncs, weekly pacing reviews, and technical walkthroughs across performance marketing and SEO engagements.

---

## 2. Trigger Conditions
- Weekly performance review meetings (e.g. Meta Ads, Google Ads, SEO).
- Client onboarding kickoff calls.
- Ad-hoc strategic alignment and budget escalation syncs.

---

## 3. Mandatory Output Routing
In strict compliance with workspace data rules:
- **Master Agency Report:** `reports/{Client_Name}_MOM_{Date}.md`
- **Client Case Study Archive:** `case-studies/{client-slug}/{Client_Name}_MOM_{Date}.md`
- **Executive HTML Report:** `reports/{Client_Name}_MOM_{Date}.html`

---

## 4. Execution Protocol
Execute the automated generator script:
```powershell
python scripts/generate_meeting_mom.py \
  --client "[Client Name]" \
  --domain "[domain.com]" \
  --date "[Meeting Date]" \
  --fireflies-url "[URL]" \
  --notes-file "[path_to_notes]" \
  --generate-html
```
