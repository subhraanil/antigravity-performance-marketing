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
        "slot": "Slot 1 (Morning Prime)",
        "id": "mcp-marketing-ops",
        "topic": "Model Context Protocol (MCP) for Marketing Ops: Building Autonomous Campaign Auditing Agents",
        "text": "Checking 6 ad dashboards for budget pacing & search term bleed is obsolete.\n\nWith Model Context Protocol (MCP), our AI coding assistant audits Meta & Google Ads via local tools in seconds.\n\nHere is our open-source Python MCP server:\nhttps://paidmediaworld.com/model-context-protocol-marketing-automation-mcp-agents/ #MCP #GoogleAds"
    },
    {
        "slot": "Slot 2 (Midday Tactical)",
        "id": "ga4-fragment-tracking",
        "topic": "GA4 Fragment Tracking (#:~:text=): Pinpointing Exact AI Overview Citation Clicks",
        "text": "When Google AI Overviews cites your site, Chrome adds a Scroll-to-Text fragment (#:~:text=).\n\nBy default, GA4 strips this, hiding which sentences win citations.\n\nHere is our 5-min GTM setup & BigQuery SQL to track every AI quote:\nhttps://paidmediaworld.com/ga4-text-fragment-tracking-google-ai-overviews/ #GA4 #SEO #AEO"
    }
]

def post_tweet(text):
    url = "https://api.twitter.com/2/tweets"
    headers = {"Content-Type": "application/json"}
    payload = {"text": text}
    
    resp = requests.post(url, auth=auth, headers=headers, json=payload)
    return resp.status_code, resp.json()

if __name__ == "__main__":
    print(f"[*] Publishing Slot 1 and Slot 2 to Twitter/X (@paidmediaworld)...")
    results = []
    for idx, t in enumerate(tweets, 1):
        print(f"\n--- Publishing {t['slot']}: {t['id']} ---")
        code, res = post_tweet(t["text"])
        print(f"HTTP Status: {code}")
        print(f"Response: {res}")
        if code == 201:
            tweet_id = res.get("data", {}).get("id")
            tweet_url = f"https://x.com/paidmediaworld/status/{tweet_id}"
            print(f"[SUCCESS] Live URL: {tweet_url}")
            results.append({"slot": t["slot"], "topic": t["topic"], "id": tweet_id, "url": tweet_url, "status": "LIVE"})
        else:
            print(f"[FAIL] Error posting tweet {t['id']}")
            results.append({"slot": t["slot"], "topic": t["topic"], "status": "FAILED", "error": res})

    output_path = r"C:\Users\test\Videos\Personal\reports\live_posts_slot_1_2.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"\n[DONE] Results written to {output_path}")
