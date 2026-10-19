# Search Terms Forensic Audit & Query Mining Playbook
# Proven Methodology Derived from Multi-Year Lead Gen & E-Commerce Search Audits

## 1. The Core Search Terms Principle
Advertisers do not pay for keywords; they pay for the actual **search terms** triggered by user queries. A high-performing keyword often masks significant budget waste when phrase or broad match types allow non-converting query bleeding.

---

## 2. The 4-Tier Search Query Classification Framework

Every audited search term must be classified into one of four distinct tiers:

```
+-----------------------------------------------------------------------------+
|                     4-TIER QUERY CLASSIFICATION MATRIX                      |
+-----------------------------------------------------------------------------+
| Tier 1: Alpha Winners        --> High CVR, Low CPA. Promote to Exact Match  |
| Tier 2: Beta Discovery       --> Relevant, moderate CTR. Maintain in Phrase |
| Tier 3: Low-Intent Info      --> High clicks, zero conversion. Down-bid/Neg |
| Tier 4: Irrelevant Waste     --> Immediate Negative Exact / Negative Phrase |
+-----------------------------------------------------------------------------+
```

### Detailed Classification Rules:

1. **Tier 1 (Alpha Winners - Exact Promotion)**:
   - Criteria: $\ge 3$ conversions over 90 days with CPA $\le$ Target CPA benchmark.
   - Action: Promote to dedicated [SEARCH-ALPHA] exact match ad group with pinned RSA copy. Add as negative exact to Beta discovery campaign.
2. **Tier 2 (Beta Discovery - Query Mining)**:
   - Criteria: Commercial intent keywords generating clicks with acceptable CTR (> 3.5%).
   - Action: Keep in [SEARCH-BETA] phrase match; monitor until reaching statistical conversion significance.
3. **Tier 3 (Informational / Low-Intent Mismatches)**:
   - Examples: Queries containing *"free"*, *"rules"*, *"meaning"*, *"calculator"*, *"salary"*, *"pdf"*.
   - Action: Add term-level negative keywords to prevent burning transaction budgets on educational seekers.
4. **Tier 4 (Irrelevant / Brand Leakage)**:
   - Examples: Misdirected competitor searches, unrelated job searches, wrong geographic inquiries.
   - Action: Immediate negative keyword addition.

---

## 3. Negative Keyword List Architecture

Never apply negative keywords haphazardly at the ad group level. Use structured account-level negative lists:

### Account-Level Shared Negative Lists:
1. **Universal B2B / Transactional Blocklist**:
   - `free`, `torrent`, `crack`, `pirated`, `diy`, `jobs`, `salary`, `internship`, `careers`, `reddit`, `wikipedia`, `course`, `tutorial`.
2. **Support & Existing Customer Blocklist**:
   - `login`, `sign in`, `customer service number`, `portal`, `app download`, `refund status`, `complaint`.
3. **Competitor Cross-Negatives**:
   - Maintain a curated list of direct competitors. If running generic search campaigns, exclude competitor brands to maintain generic CPA targets.

---

## 4. Weekly Search Terms Audit Runbook

Follow this weekly protocol to continuously lower blended CPA:

1. **Export 30-Day Search Terms Report**: Include Search Term, Keyword, Match Type, Clicks, Cost, Conversions, Cost / Conv.
2. **Filter by Waste Threshold**:
   - Filter for terms with Cost $>$ (1.5 $\times$ Target CPA) and Conversions $= 0$.
   - Sort descending by Spend.
3. **Action Items**:
   - Add top 15 wasted spend terms as **Negative Exact** (`[search term]`).
   - If a recurring unhelpful pattern exists (e.g. users searching for *"sample"* across 20 queries), add as **Negative Phrase** (`"sample"`).
4. **Cross-Pollinate Alpha Negatives**:
   - Every time a query is promoted to Alpha Exact, immediately add that query as a negative exact to the Beta campaign to eliminate internal auction cannibalization.
