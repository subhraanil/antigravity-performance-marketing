# Workflow: ApexLink Pro Backlink Campaign SOP

## Overview
A repeatable, compliant procedure for building high-authority white-hat backlinks using curated directories, Digital PR journalist queries, and zero-leak linkable statistics assets.

---

## Trigger Conditions
- New site launch requiring foundation domain authority.
- Competitor domain rating gap $> 15$ points.
- Core commercial keywords stalled on Page 2 due to referring domain deficit.

---

## Step-by-Step SOP

### Phase 1: Baseline Backlink Profile Health Audit
1. Run multi-source backlink audit:
   ```powershell
   python seo/link-building/scripts/link_audit.py --input <backlinks_export.csv> --disavow disavow.txt
   ```
2. Verify Health Score $\ge 70/100$.
3. Check Penguin Anchor Text distribution:
   - Branded: 35%–55%
   - Naked URL: 15%–25%
   - Generic: 10%–20%
   - Exact-Match: $\le 8\%$ (Alert if $> 15\%$)
4. If toxic ratio $> 2\%$, export generated `disavow.txt` and upload to Google Search Console Disavow Tool.

### Phase 2: High-Authority Foundation Directories (Track A & Track B)
1. Query relevant high-DR platforms from the 745+ database:
   ```powershell
   python seo/link-building/scripts/directory_engine.py list --category AI --min-dr 60
   ```
2. Split targets into execution shards of 10 platforms:
   ```powershell
   python seo/link-building/scripts/directory_engine.py shard --product-id <brand_name> --shard-size 10
   ```
3. Execute micro-batches with human authorization checkpoints: inspect $\to$ register $\to$ fill profile $\to$ verify link.

### Phase 3: Digital PR Journalist Pitching (Qwoted / HARO / Connectively)
1. Monitor journalist requests matching brand vertical.
2. Run Pitch Heuristic Scorer:
   ```powershell
   python seo/link-building/scripts/pr_pitch_engine.py --topic <topic> --ask <ask> --framework data_anchor
   ```
3. If Score $\ge 2$, trigger **BUILD_STATS_PAGE**:
   ```powershell
   python seo/link-building/scripts/stats_asset_generator.py --topic <topic> --brand <name> --url <url>
   ```
4. Submit concise, data-driven quote directly to journalist before deadline.

### Phase 4: Deterministic Live Verification
1. Crawl published URLs to confirm link presence and equity:
   ```powershell
   python seo/link-building/scripts/link_verifier.py --source <publisher_url> --target <brand_domain>
   ```
2. Confirm HTTP 200, valid anchor, and dofollow or nofollow status recorded in campaign ledger.
