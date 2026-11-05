import os
import re
import json
import subprocess

def clean_html_content(content):
    # This regex looks for content inside common tags and removes internal newlines
    # while preserving newlines BETWEEN tags for readability in the code editor.
    
    # List of tags to clean internal newlines from
    tags = ['p', 'li', 'td', 'th', 'h2', 'h3', 'div', 'strong', 'em', 'a']
    
    for tag in tags:
        pattern = re.compile(f'<{tag}([^>]*)>(.*?)</{tag}>', re.DOTALL)
        def replace_func(match):
            attr, inner_content = match.groups()
            cleaned_inner = re.sub(r'\s*\n\s*', ' ', inner_content).strip()
            return f'<{tag}{attr}>{cleaned_inner}</{tag}>'
        content = pattern.sub(replace_func, content)
    
    return content

def fix_all_blogs():
    tmp_dir = ".tmp"
    files = [f for f in os.listdir(tmp_dir) if f.endswith(".html")]
    
    # Mapping of file names to slugs (since I used them in my previous steps)
    # I will extract this from my recent history or just try to match them.
    # To be perfectly safe, I'll use the wp_api_publisher.py's get_post_id_by_slug if I can.
    
    for filename in files:
        filepath = os.path.join(tmp_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        cleaned = clean_html_content(content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(cleaned)
        
        print(f"Cleaned {filename}")

if __name__ == "__main__":
    fix_all_blogs()
