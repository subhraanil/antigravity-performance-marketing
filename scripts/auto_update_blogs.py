import os
import json
import time
import subprocess
import requests
import sys
import re
from dotenv import load_dotenv

# Force UTF-8 output on Windows to avoid cp1252 encoding errors
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

load_dotenv()

# Use Environment Variables or Defaults
WP_URL = "https://paidmediaworld.com/wp-json/wp/v2"
WP_USERNAME = os.getenv("WP_USERNAME", "subhranil")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://paidmediaworld.com/",
}

def fetch_post_content_by_slug(slug):
    url = f"{WP_URL}/posts?slug={slug}"
    try:
        resp = requests.get(url, auth=(WP_USERNAME, WP_APP_PASSWORD), headers=HEADERS, timeout=30)
        if resp.status_code == 200:
            posts = resp.json()
            if posts:
                return posts[0]
        else:
            print(f"  [WARN] Fetch status {resp.status_code} for slug '{slug}'")
    except Exception as e:
        print(f"  [ERROR] Fetching slug '{slug}': {e}")
    return None

def rewrite_content_with_gemini(original_title, original_html):
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    
    prompt = f"""
    You are a Senior PPC Strategist and Digital Marketing Expert specializing in the Indian Market (B2B/SMBs).
    Rewrite the following blog post into a 2026 E-E-A-T and Information Gain powerhouse (target 1200+ words).
    
    Current Title: {original_title}
    
    Rules for the Output:
    1. Reply with ONLY raw HTML markup (starting with <p> or <h2>), do NOT wrap in ```html markdown blocks. Do not add a <body> or <html> tag.
    2. Write in an authoritative, data-backed, conversational tone.
    3. Include Localized Indian Reality Checks (e.g., Tier-2 search behavior, UPI, GST if applicable, local pricing, WhatsApp marketing, Hindi/Bengali search intent).
    4. Provide "Information Gain" (a unique perspective, a myth busted, or a Pro-Tip box).
    5. No <hr> tags. Use <h2> and <h3> followed by substantial paragraphs. Include a <table> or <ul> for pattern interrupt.
    6. Ensure high semantic density (use terms like 'Performance Max', 'ROAS', 'CPA', 'LTV', 'GA4', 'First-Party Data').
    7. CRITICAL: Never add manual newlines (\\n) within <p>, <li>, <td>, <h2>, or <h3> tags. Keep each sentence/paragraph as a continuous line within its tag.
    8. Suggest 2-3 image placements using this exact tag: [IMAGE_PROMPT: description of a premium digital marketing graphic for this section].
    9. CRITICAL: NEVER use markdown bolding (**) in the content. For HTML emphasis, use <strong>.
    10. CRITICAL: NEVER use em-dashes (—). Use plain dashes (-), commas, or colons instead.
    11. Avoid typical AI artifacts like excessive bullet points at the very beginning or ending phrases that summarize what was just said.
    
    Original Content:
    {original_html}
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.5}
    }
    
    resp = requests.post(endpoint, json=payload, timeout=60)
    if resp.status_code == 200:
        data = resp.json()
        try:
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except KeyError:
            print("Gemini response format error:", data)
            return None
    else:
        print("Gemini API Error:", resp.status_code, resp.text)
        return None

def update_post_in_wp(post_id, new_content):
    url = f"{WP_URL}/posts/{post_id}"
    payload = {"content": new_content}
    update_headers = {**HEADERS, "Content-Type": "application/json"}
    try:
        resp = requests.post(url, auth=(WP_USERNAME, WP_APP_PASSWORD), headers=update_headers, json=payload, timeout=60)
        return resp.status_code == 200, resp.json().get('link', '') if resp.status_code == 200 else resp.text
    except Exception as e:
        return False, str(e)

def main():
    report_file = "blog_analysis_report.json"
    if not os.path.exists(report_file):
        print("No report file found.")
        return

    with open(report_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Re-run for ALL blogs as requested by user
    log_file = "reports/auto_update_log_full_refresh.json"
    processed_links = []
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as f:
            processed_links = json.load(f)

    print(f"Starting FULL automated update for {len(data)} blogs...")
    count = 0
    
    for idx, post in enumerate(data):
        link = post["link"]
        slug = link.strip("/").split("/")[-1]
        
        # Check if already processed in THIS full refresh run
        if link in processed_links:
            continue
            
        title = post["title"]
        print(f"\n==============================================")
        print(f"[{idx+1}/{len(data)}] Refreshing: {title}")
        
        # 1. Fetch WP Post
        wp_post = fetch_post_content_by_slug(slug)
        if not wp_post:
            print("-> Could not fetch post ID from WordPress. Skipping.")
            continue
            
        post_id = wp_post["id"]
        original_html = wp_post["content"]["rendered"]
        
        # 2. Gemini Rewrite with strict formatting
        print("-> Generating premium content (No ** or —)...")
        new_html = rewrite_content_with_gemini(title, original_html)
        
        if not new_html:
            print("-> Gemini rewrite failed. Skipping.")
            continue
            
        # Clean potential markdown wrapping
        new_html = re.sub(r'^```html\n', '', new_html)
        new_html = re.sub(r'\n```$', '', new_html)
        new_html = new_html.strip()
        
        # Check for image prompts
        image_prompts = re.findall(r'\[IMAGE_PROMPT: (.*?)\]', new_html)
        if image_prompts:
            print(f"-> Found {len(image_prompts)} image prompts.")
            
        # 3. Update WP
        print("-> Pushing updated content to WordPress...")
        success, live_url = update_post_in_wp(post_id, new_html)
        
        if success:
            print(f"-> SUCCESS: {live_url}")
            # 4. Submit Indexing
            subprocess.run(["python", "scripts/submit_indexing.py", "--url", live_url], check=False, capture_output=True)
            
            processed_links.append(link)
            os.makedirs("reports", exist_ok=True)
            with open(log_file, "w", encoding="utf-8") as f:
                json.dump(processed_links, f, indent=2)
                
            count += 1
            time.sleep(2)
        else:
            print(f"-> FAILED: {live_url}")
            
    print(f"\nFull update session completed! Processed {count} blogs.")

if __name__ == "__main__":
    main()
