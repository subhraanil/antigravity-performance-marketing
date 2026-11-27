import os
import sys
import json
import requests
from requests_oauthlib import OAuth1
from dotenv import load_dotenv

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# Load .env
env_path = r"C:\Users\test\Videos\Personal\.env"
load_dotenv(env_path)

CK = os.getenv("TWITTER_CONSUMER_KEY")
CS = os.getenv("TWITTER_CONSUMER_SECRET")
AT = os.getenv("TWITTER_ACCESS_TOKEN")
ATS = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

if not all([CK, CS, AT, ATS]):
    print("[-] Missing Twitter API credentials in .env")
    sys.exit(1)

auth = OAuth1(CK, CS, AT, ATS)

tweets = [
    {
        "slot": "Slot 1 (Morning Prime - Performance Paid Ads)",
        "id": "meta-bid-cap-vs-cost-cap",
        "topic": "Meta Ads Bid Cap vs. Cost Cap Scaling: Navigating Peak Holiday Auction Spikes Without Bleeding Margin",
        "text": "With Black Friday 5 days away, Meta CPMs surged 60%+.\n\nIf your campaigns run on default 'Highest Volume' bidding, you are handing Meta a blank check to burn budgets by 2 PM.\n\nHere is our guide to Cost Caps, Bid Caps & the 3-Tier Bid Ladder:\nhttps://paidmediaworld.com/meta-ads-bid-cap-vs-cost-cap-scaling-holiday/ #MetaAds #PPC #BFCM"
    },
    {
        "slot": "Slot 2 (Midday Tactical - Technical Tracking & Analytics)",
        "id": "meta-capi-emq-optimization",
        "topic": "Meta Conversions API (CAPI) 8.5+ Event Match Quality: Eliminating Blindspots in Q4 Signal Attribution",
        "text": "If your Meta Event Match Quality (EMQ) score is under 7.0, you are flying blind on 30% of your conversions.\n\nLow EMQ directly inflates CPAs and breaks retargeting.\n\nHere is how to hit 8.5+ with full server-side hashing & deduplication:\nhttps://paidmediaworld.com/meta-conversions-api-event-match-quality-optimization/ #CAPI #MetaAds #GA4"
    },
    {
        "slot": "Slot 3 (Evening Authority - AI Search & Generative Engine Optimization)",
        "id": "princeton-kdd-geo-framework",
        "topic": "Generative Engine Optimization (GEO): Implementing Princeton KDD 2024 Levers for +40% AI Overviews Visibility",
        "text": "Traditional SEO keyword stuffing hurts rankings in Google AI Overviews & Perplexity.\n\nLandmark Princeton research (KDD '24) proved that Generative Engine Optimization (GEO) boosts citations by up to +41%.\n\nHere is how to optimize for RAG:\nhttps://paidmediaworld.com/generative-engine-optimization-princeton-kdd-framework/ #SEO #GEO #AIOverviews"
    },
    {
        "slot": "Bonus Slot (Marketing Automation & Ops)",
        "id": "autonomous-google-ads-spend-anomaly",
        "topic": "Autonomous Google Ads Spend Anomaly Detection: Open-Source Python Agent for Real-Time PPC Alerts",
        "text": "Google Ads can legally spend up to 200% of your daily budget on surge days.\n\nDuring holiday spikes or site checkout crashes, automated bidding ruthlessly burns cash.\n\nWe built an open-source Python agent that monitors spend velocity & pings Slack:\nhttps://paidmediaworld.com/automate-google-ads-spend-anomaly-detection-python-agent/ #GoogleAds #Python #PPC"
    }
]

def post_tweet(text):
    url = "https://api.twitter.com/2/tweets"
    headers = {"Content-Type": "application/json"}
    payload = {"text": text}
    
    resp = requests.post(url, auth=auth, headers=headers, json=payload)
    return resp.status_code, resp.json()

if __name__ == "__main__":
    print(f"[*] Publishing all Nov 22 scheduled slots at once to Twitter/X (@paidmediaworld)...")
    results = []
    success_count = 0
    for idx, t in enumerate(tweets, 1):
        print(f"\n--- Publishing {t['slot']}: {t['id']} ---")
        code, res = post_tweet(t["text"])
        print(f"HTTP Status: {code}")
        print(f"Response: {res}")
        if code == 201:
            tweet_id = res.get("data", {}).get("id")
            tweet_url = f"https://x.com/paidmediaworld/status/{tweet_id}"
            print(f"[SUCCESS] Live URL: {tweet_url}")
            t["live_url"] = tweet_url
            t["status"] = "PUBLISHED"
            success_count += 1
        else:
            t["status"] = f"FAILED ({code})"
            t["error"] = res
        results.append(t)
    
    log_file = r"C:\Users\test\Videos\Personal\reports\publish_nov22_log.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[*] Finished publishing run: {success_count}/{len(tweets)} successful. Log written to {log_file}")
