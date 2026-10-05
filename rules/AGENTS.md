# Performance Marketing Agent Workspace

This workspace is configured with the **Performance Marketing Operating System**, integrating the open-source [digital-marketing-pro](https://github.com/indranilbanerjee/digital-marketing-pro) framework, dedicated marketing subagents, and strict campaign guardrails.

## Quick Links
- **Global Project Rules**: [.antigravity/rules](file:///C:/Users/test/.gemini/antigravity/scratch/digital-marketing/.antigravity/rules)
- **Agent Rules**: [.agents/rules/performance-marketing.md](file:///C:/Users/test/.gemini/antigravity/scratch/digital-marketing/.agents/rules/performance-marketing.md)
- **Workflows**: [workflows/](file:///C:/Users/test/.gemini/antigravity/scratch/digital-marketing/workflows/)
- **Templates**: [templates/](file:///C:/Users/test/.gemini/antigravity/scratch/digital-marketing/templates/)

## Key Campaign Constraints
1. **Safety Creation Gate**: All campaigns, ad sets, and ads are generated in `PAUSED` status.
2. **Budget Pacing**: Scaling is capped at ≤ 20% increases every 72 hours per campaign.
3. **Audience Hygiene**: Strict negative exclusions for past 30-day purchasers and customer lists.
4. **Compliance**: EU AI Act Article 50 disclosures and C2PA provenance required on AI assets.

## Target CPAs & Benchmarks
- **DTC E-Commerce**: CPA \$22–\$42, ROAS 3.2x–4.5x
- **B2B SaaS**: Trial CPA \$35–\$75, PQL \$110–\$240, CAC \$450–\$950
- **Lead Gen**: CPL \$65–\$160, SQL \$350–\$850

## Subagent Loop
Delegations are automatically handled via dedicated specialist subagents:
- `media_buyer`: Meta Ads, Google Ads, bid strategies, pacing, and execution.
- `marketing_strategist`: 12-Part Strategy Flow, GTM planning, and positioning.
- `growth_engineer`: PLG, loops, activation funnels, and unit economics.
- `seo_specialist`: Technical SEO, AEO/GEO (Google AI Mode), and schema.
- `analytics_analyst`: Attribution, reporting, and incrementality.
- `brand_guardian`: Compliance, C2PA, and EU AI Act Article 50.
