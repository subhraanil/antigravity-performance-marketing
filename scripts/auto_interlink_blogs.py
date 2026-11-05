import os
import re
import json
import random

def load_interlinking_map():
    with open("reports/internal_linking_data.json", "r") as f:
        primary_map = json.load(f)["interlinking_map"]
    
    with open("reports/short_keywords.json", "r") as f:
        short_map = json.load(f)
        
    # Merge maps
    merged_items = []
    for item in primary_map:
        merged_items.append({"url": item["url"], "anchors": item["anchor_texts"]})
    
    for item in short_map:
        # Avoid duplicate URLs, just add keywords to existing if any
        found = False
        for m in merged_items:
            if m["url"] == item["url"]:
                m["anchors"].extend(item["keywords"])
                found = True
                break
        if not found:
            merged_items.append({"url": item["url"], "anchors": item["keywords"]})
            
    return merged_items

def interlink_content(html_content, interlinking_map, current_post_url):
    # Flatten map for easier processing
    all_pairs = []
    
    # BLACKLIST of terms to NEVER link (e.g. brand name)
    BLACKLIST = ["Paid Media World", "Paid Media"]
    
    for item in interlinking_map:
        if item["url"].strip('/').lower() == current_post_url.strip('/').lower():
            continue
        for anchor in item["anchors"]:
            if anchor in BLACKLIST:
                continue
            all_pairs.append((anchor, item["url"]))
    
    # Sort map by anchor text length (longest first) to avoid partial matching issues
    all_pairs.sort(key=lambda x: len(x[0]), reverse=True)
    
    links_added = 0
    max_links = 5
    linked_urls = set()
    
    # Regex to find text nodes outside tags
    # This is a robust approach: replace only in text parts
    def replace_in_text(text):
        nonlocal links_added
        if links_added >= max_links:
            return text
            
        for anchor, url in all_pairs:
            if links_added >= max_links:
                break
            if url in linked_urls:
                continue
            
            # Use word boundary and case insensitive
            # Addition: Negative lookahead to ensure we don't catch "Paid Media" inside "Paid Media World"
            if anchor.lower() == "paid media":
                # Don't match if followed by " World"
                pattern = re.compile(r'\b(' + re.escape(anchor) + r')\b(?!\sWorld)', re.IGNORECASE)
            else:
                pattern = re.compile(r'\b(' + re.escape(anchor) + r')\b', re.IGNORECASE)
            
            if pattern.search(text):
                # Replace only the first occurrence
                text = pattern.sub(f'<a href="{url}">\\1</a>', text, count=1)
                links_added += 1
                linked_urls.add(url)
                
        return text

    # Split HTML into tags and text
    parts = re.split(r'(<[^>]+>)', html_content)
    new_parts = []
    in_link = False
    in_heading = False
    
    for part in parts:
        if part.startswith('<'):
            tag_name = part.lower()
            if '<a ' in tag_name: in_link = True
            if '</a>' in tag_name: in_link = False
            if re.match(r'<(h1|h2|h3)', tag_name): in_heading = True
            if re.match(r'</(h1|h2|h3)', tag_name): in_heading = False
            new_parts.append(part)
        else:
            if not in_link and not in_heading and part.strip():
                # This is plain text, safe to interlink
                new_parts.append(replace_in_text(part))
            else:
                new_parts.append(part)
                
    return "".join(new_parts)

def process_all_blogs():
    tmp_dir = ".tmp"
    files = [f for f in os.listdir(tmp_dir) if f.endswith(".html")]
    
    interlinking_map = load_interlinking_map()
    
    # Filename -> Slug -> URL logic
    # We'll read from reports/auto_update_log.json to be 100% accurate on URLs
    with open("reports/auto_update_log.json", "r") as f:
        log_urls = json.load(f)
    
    file_to_url = {}
    for f in files:
        slug = f.replace(".html", "").replace("_", "-")
        # Direct matching based on slug
        for url in log_urls:
            if slug in url or url.rstrip('/').split('/')[-1] == slug:
                file_to_url[f] = url
                break
        
        # Manual fallback overrides
        if f == "google_ads_SMBs.html": file_to_url[f] = "https://paidmediaworld.com/google-ads-guide/"
        if "iaol" in f: file_to_url[f] = "https://paidmediaworld.com/iaol/"

    for filename in files:
        filepath = os.path.join(tmp_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        current_url = file_to_url.get(filename, "")
        updated_content = interlink_content(content, interlinking_map, current_url)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        
        print(f"Interlinked {filename} (Final count for file)")

if __name__ == "__main__":
    process_all_blogs()
