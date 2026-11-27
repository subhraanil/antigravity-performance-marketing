import re

with open('data/storiai/bundle.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Look for assets
assets = re.findall(r'["\'](/assets/[^"\']+)["\']', text)
print("Assets starting with /assets/:", set(assets))

# Look for other js files
js_files = re.findall(r'["\']([^"\']+\.js)["\']', text)
print("JS files:", set(js_files))

# Look for css files
css_files = re.findall(r'["\']([^"\']+\.css)["\']', text)
print("CSS files:", set(css_files))

# Look for API calls or fetch
fetches = re.findall(r'fetch\([\'"]([^\'"]+)[\'"]', text)
print("Fetch calls:", set(fetches))

# Look for baseUrl or axios
base_urls = re.findall(r'baseURL\s*:\s*["\']([^"\']+)["\']', text)
print("baseURL:", set(base_urls))

# Search for any string containing Child or Story
stories = re.findall(r'["\'][^"\']*(?:child|emotion|story|stories)[^"\']*["\']', text, re.IGNORECASE)
print(f"Strings mentioning child/emotion/story ({len(stories)}):")
for s in list(set(stories))[:20]:
    print("  *", s)
