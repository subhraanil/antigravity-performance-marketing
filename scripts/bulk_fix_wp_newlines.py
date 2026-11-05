import os
import subprocess
import json
import re

# Load logic to extract slugs correctly
with open("reports/auto_update_log.json", "r") as f:
    urls = json.load(f)

slugs = []
for url in urls:
    match = re.search(r'paidmediaworld\.com/([^/]+)/?', url)
    if match:
        slugs.append(match.group(1))

# Improved mapping logic
BLOG_MAPPING = {
    "advantage_plus_meta.html": "beyond-the-click-why-metas-advantage-campaigns-are-the-core-of-e-commerce-growth",
    "ai_performance_marketing_startups.html": "ai-driven-performance-marketing-lead-generation-indian-startups",
    "ai_ppc_manager_skills.html": "ai-augmented-ppc-manager-skills",
    "ai_trends_2026.html": "the-future-of-ai-in-digital-marketing-5-trends-shaping-2026-for-indian-brands",
    "awareness_to_action_funnel.html": "awareness-to-action-funnel-explained",
    "b2b_lead_gen_manufacturers_kolkata.html": "b2b-lead-generation-manufacturers-kolkata",
    "beginner_ppc_mistakes.html": "common-beginner-ppc-mistakes-fix",
    "bengali_ads_west_bengal.html": "vernacular-ppc-bengali-ads-west-bengal",
    "bing_ads_guide.html": "bing-ads-guide",
    "d2c_ads_strategy_2026.html": "d2c-paid-advertising-strategies",
    "doctor_marketing_guidelines_india.html": "digital-marketing-guidelines-doctors-india-mci",
    "fb_ads_cost_india.html": "cost-of-facebook-ads-in-india-guide-benchmarks-for-leads-sales",
    "ga4_predictive_profitability.html": "predictive-profitability-ga4-ai-metrics",
    "geo_strategy_2026.html": "generative-engine-optimization-geo-guide",
    "gmc_reinstatement_guide_india.html": "google-merchant-center-reinstatement-checklist-india",
    "google_ads_SMBs.html": "google-ads-guide",
    "google_ads_auction_explained.html": "how-google-ads-auction-works",
    "google_ads_payment_tax_india.html": "google-ads-payment-issues-india",
    "google_ads_roas_gap.html": "google-ads-roas-gap-india",
    "google_ads_suspension_fix_india.html": "fix-google-ads-suspension-india",
    "google_vs_meta_india.html": "google-ads-vs-meta-ads-where-should-indian-startups-spend-first",
    "hindi_ads_power_india.html": "hindi-ad-copies-vernacular-marketing-india",
    "hinglish_regional_ppc_india.html": "mastering-hinglish-regional-ppc-india",
    "iaol_case_study.html": "iaol",
    "influencer_marketing_small_teams.html": "influencer-marketing-for-small-teams",
    "jersey_case_study.html": "jersey-blanket",
    "kahab_case_study.html": "kahab-beach-resort",
    "keyword_arbitrage_strategy_2026.html": "identify-target-low-difficulty-high-value-keywords",
    "linkedin_ads_guide.html": "linkedin-ads-guide",
    "linkedin_advertising.html": "linkedin-advertising",
    "lower_google_ads_cpl.html": "why-your-google-ads-cpl-is-so-high-5-ways-we-lower-it",
    "meta_ads_algorithm_explained.html": "how-meta-ads-algorithm-works",
    "meta_ads_guide.html": "meta-ads-guide",
    "microsoft_vs_google_pmax.html": "microsoft-vs-google-performance-max-comparison",
    "nutrabytes_case_study.html": "nutrabytes",
    "paid_marketing_kolkata.html": "paid-marketing-company-in-kolkata",
    "paid_media_guide.html": "paid-media-guide",
    "paid_media_services.html": "paid-media-services",
    "performance_marketing_definition_india.html": "performance-marketing-definition-india-business",
    "personal_voice_seo_2026.html": "human-made-content-personal-voice-seo",
    "pmax_masterclass_india.html": "master-google-pmax-lead-gen-india",
    "ppc_budgeting_beginner.html": "ppc-budgeting-beginner-guide",
    "real_estate_ppc_india.html": "ppc-real-estate-in-india-leads",
    "revive_blogs_google_discover.html": "revive-old-blogs-google-discover-traffic",
    "saas_integration_seo_strategy.html": "b2b-saas-integration-keyword-seo-strategy",
    "seo_ranking_vs_revenue.html": "seo-ranking-vs-revenue-reality-check",
    "seo_vs_ppc_2026.html": "seo-vs-ppc-for-beginners-2026",
    "seo_vs_ppc_career_stability.html": "seo-vs-ppc-career-stability",
    "share_samadhan_case_study.html": "share-samadhan",
    "vbb_pmax_optimization.html": "value-based-bidding-pmax-optimization",
    "visual_seo_guide_2026.html": "visual-seo-google-discover-image-optimization",
    "website_redesign_seo_mistakes.html": "website-redesign-mistakes-seo",
    "what_is_performance_marketing.html": "what-is-performance-marketing"
}

def bulk_update():
    for filename, slug in BLOG_MAPPING.items():
        filepath = os.path.join(".tmp", filename)
        if not os.path.exists(filepath):
            continue
        
        # Double check slug exists in our verified list
        if slug not in slugs:
             # Try a slightly different matching if it's not exact
             print(f"Warning: {slug} not found in verified URLs, checking for partial match...")
             found = False
             for v_slug in slugs:
                 if slug in v_slug or v_slug in slug:
                     slug = v_slug
                     found = True
                     break
             if not found:
                 print(f"Skipping {slug} - not found in logs.")
                 continue

        print(f"Updating {slug}...")
        cmd = [
            "python", "execution/wp_api_publisher.py",
            "--update",
            "--slug", slug,
            "--content-file", filepath
        ]
        
        try:
            # Running with shell=True on windows to handle potential issues with subprocess
            subprocess.run(" ".join(cmd), shell=True, check=True)
            import time
            time.sleep(2)
        except Exception as e:
            print(f"Error updating {slug}: {e}")

if __name__ == "__main__":
    bulk_update()
