import re

with open('data/storiai/chunks/App-XFfRbN91.js', 'r', encoding='utf-8') as f:
    text = f.read()

# Search for hero-home or webp
matches = re.findall(r'[^"\'\s]+hero-home[^"\'\s]*', text)
print("Hero matches:", matches)

# Search for img tags or image sources
img_srcs = re.findall(r'src:\s*["\']([^"\']+)["\']', text)
print("src matches:", set(img_srcs[:20]))

# Search for imports of images
img_imports = re.findall(r'["\'](/assets/[^"\']+\.(?:webp|png|jpg|svg))["\']', text)
print("assets images:", set(img_imports))

# Look for all occurrences of .webp, .png, .jpg
all_ext = set(re.findall(r'["\']([^"\']+\.(?:webp|png|jpg|svg))["\']', text))
print("All image paths:", all_ext)
