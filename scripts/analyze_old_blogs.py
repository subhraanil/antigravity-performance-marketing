import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

WP_URL = "https://paidmediaworld.com/wp-json/wp/v2"
WP_USERNAME = os.getenv("WP_USERNAME")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json"
}

def fetch_all_posts():
    posts = []
    page = 1
    while True:
        resp = requests.get(f"{WP_URL}/posts?per_page=100&page={page}", auth=(WP_USERNAME, WP_APP_PASSWORD), headers=HEADERS)
        if resp.status_code != 200:
            print(f"Failed to fetch page {page}. Status: {resp.status_code}, Response: {resp.text}")
            break
        data = resp.json()
        if not data:
            break
        posts.extend(data)
        print(f"Fetched page {page} ({len(data)} posts)")
        page += 1
        
    analysis_results = []
    
    for post in posts:
        content = post.get('content', {}).get('rendered', '')
        title = post.get('title', {}).get('rendered', '')
        date = post.get('date', '')
        link = post.get('link', '')
        word_count = len(content.split())
        
        # Simple heuristics for "needs update"
        needs_update = []
        
        if word_count < 600:
            needs_update.append(f"Low word count ({word_count} words)")
            
        if "2023" in content or "2023" in title:
            needs_update.append("Contains outdated year (2023)")
            
        if "2024" in content or "2024" in title:
            needs_update.append("Contains outdated year (2024)")
            
        if "2025" in content or "2025" in title:
            needs_update.append("Contains year (2025) - might need update to 2026")

        if not '<h2' in content:
            needs_update.append("Missing H2 tags (Poor structure)")
            
        if not '<img' in content:
            needs_update.append("No images found")
            
        # specifically checking if they are old and haven't been updated recently
        if date.startswith('2023') or date.startswith('2024'):
            needs_update.append(f"Old publish date ({date.split('T')[0]})")

        analysis_results.append({
            'title': title,
            'link': link,
            'date': date.split('T')[0],
            'word_count': word_count,
            'needs_update_reasons': needs_update,
            'status': 'Needs Update' if needs_update else 'Good'
        })
        
    # Sort by ones that need update
    needs_update_list = [p for p in analysis_results if p['status'] == 'Needs Update']
    
    with open('blog_analysis_report.json', 'w', encoding='utf-8') as f:
        json.dump(needs_update_list, f, indent=4)
        
    print(f"\nTotal posts analyzed: {len(posts)}")
    print(f"Posts needing updates: {len(needs_update_list)}")
    
if __name__ == "__main__":
    fetch_all_posts()
