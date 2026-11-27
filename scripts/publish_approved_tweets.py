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
        "id": "pmax",
        "text": "Google Ads finally added native channel-level reporting for Performance Max.\n\nAudits show up to 34% of spend quietly siphons into junk mobile app Display placements.\n\nHere is how to audit your channel split & kill the bleed:\nhttps://paidmediaworld.com/google-ads-pmax-channel-level-reporting-display-waste/ #GoogleAds #PPC"
    },
    {
        "id": "schema",
        "text": "Traditional SEO earned blue links. Generative Engine Optimization (GEO) earns AI Overviews.\n\nIf your site uses flat schema tags, AI engines cite competitors instead.\n\nHere is our nested JSON-LD @graph blueprint with Wikidata linking:\nhttps://paidmediaworld.com/entity-schema-graph-google-ai-overviews-citations/ #SEO #AEO #GEO"
    },
    {
        "id": "gsc",
        "text": "Stuck with 'Discovered - currently not indexed' in Google Search Console?\n\nStop clicking 'Request Indexing'. It's not a sitemap bug—it's domain quality throttling & click depth.\n\nHere is our 5-day forensic triage to force indexing:\nhttps://paidmediaworld.com/google-search-console-discovered-currently-not-indexed-triage/ #SEO #TechSEO"
    },
    {
        "id": "miner",
        "text": "Checking Google Ads search terms once a week burns 20% of your budget during holiday inflation.\n\nWe built a Python agent that extracts queries nightly, classifies intent via LLM, and auto-quarantines waste:\nhttps://paidmediaworld.com/autonomous-negative-keyword-miner-google-ads-agent/ #GoogleAds #Python"
    }
]

def post_tweet(text):
    url = "https://api.twitter.com/2/tweets"
    headers = {"Content-Type": "application/json"}
    payload = {"text": text}
    
    resp = requests.post(url, auth=auth, headers=headers, json=payload)
    return resp.status_code, resp.json()

if __name__ == "__main__":
    print(f"[*] Ready to post {len(tweets)} tweets to @paidmediaworld...")
    for idx, t in enumerate(tweets, 1):
        print(f"\n--- Posting Tweet {idx} ({t['id']}) ---")
        code, res = post_tweet(t["text"])
        print(f"Status: {code}")
        print(f"Response: {res}")
