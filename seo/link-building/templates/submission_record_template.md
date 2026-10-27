# ApexLink Campaign Submission Ledger

**Campaign Name:** [CAMPAIGN_NAME]  
**Target Product / Brand:** [PRODUCT_NAME]  
**Canonical Destination URL:** [https://example.com]  
**Operator Alias:** [OPERATOR_NAME]  
**Created Date:** [YYYY-MM-DD]  
**Batch Shard:** [SHARD_01]  

---

## Campaign Execution Guidelines
1. **Never store real credentials, OTPs, recovery codes, or passwords** in this file.
2. **Anchor Strategy:** Use strictly Brand Name, Product Name, or Naked URL. Never use commercial exact-match anchors on directories.
3. **Execution State Transition:**
   `queued` &rarr; `preflight_checked` &rarr; `authorized` &rarr; `submitted` &rarr; `live_verified`

---

## Submission Tracking Matrix

| Domain | Status | DR | Follow Type | Submission URL | Live Link URL | Idempotency Key | Verified Date | Notes |
|---|---|---|---|---|---|---|---|---|
| crunchbase.com | submitted | 90 | nofollow | https://www.crunchbase.com/add-new | — | a1b2c3d4e5f6 | — | Company profile created |
| alternativeto.net | live_verified | 81 | dofollow | https://alternativeto.net/manage-item/ | https://alternativeto.net/software/example | c7d8e9f0a1b2 | 2026-10-27 | Approved and live |
| devpost.com | submitted | 86 | dofollow | https://devpost.com/software/new | — | e3f4a5b6c7d8 | — | Pending hackathon showcase review |
| g2.com | preflight_checked | 98 | nofollow | https://www.g2.com/products/new | — | f9a0b1c2d3e4 | — | Claiming profile via business email |
| producthunt.com | queued | 91 | dofollow | https://www.producthunt.com | — | b5c6d7e8f9a0 | — | Scheduled for launch week |

---

## Audit Verification Command

To verify integrity, secret absence, and duplicate status:
```bash
python scripts/audit_campaign_record.py path/to/this-record.md
```
