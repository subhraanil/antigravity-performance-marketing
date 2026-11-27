import re

with open('data/storiai/chunks/App-XFfRbN91.js', 'r', encoding='utf-8') as f:
    code = f.read()

print(f"App-XFfRbN91.js length: {len(code)} characters")

# Check for routes / paths
routes = set()
# Search for path: "..."
for m in re.finditer(r'path\s*:\s*["\']([^"\']+)["\']', code):
    routes.add(m.group(1))

# Search for <Route path="..."
for m in re.finditer(r'path\s*=\s*["\']([^"\']+)["\']', code):
    routes.add(m.group(1))

print(f"\nAll Defined Routes ({len(routes)} found):")
for r in sorted(routes):
    print(f"  * {r}")

# Search for navigation items / menu items
nav_matches = re.findall(r'["\'](?:Home|Pricing|Features|About|Contact|FAQ|Privacy|Terms|Stories|Blog|Dashboard|Login|Signup|Sign Up|Register)["\']', code, re.IGNORECASE)
print(f"\nNavigation-like labels found: {set(nav_matches)}")

# Search for image URLs
images = set(re.findall(r'["\']([^"\']+\.(?:png|jpg|jpeg|webp|svg|gif))["\']', code, re.IGNORECASE))
print(f"\nImages referenced in App ({len(images)} found):")
for img in sorted(images)[:25]:
    print(f"  - {img}")

# Search for external scripts / SDKs / Analytics
sdks = set(re.findall(r'https?://[a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,}(?:/[^\s"\'<>]*)?', code))
print(f"\nExternal URLs / SDKs ({len(sdks)} found):")
for s in sorted(sdks):
    if any(k in s.lower() for k in ['google', 'facebook', 'stripe', 'mixpanel', 'clarity', 'hotjar', 'crisp', 'sentry', 'ably', 'aws', 'api']):
        print(f"  - {s}")
