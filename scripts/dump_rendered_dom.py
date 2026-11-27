import subprocess
import os

chrome = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
cmd = [
    chrome,
    '--headless=new',
    '--disable-gpu',
    '--dump-dom',
    '--virtual-time-budget=10000',
    'https://storiai.ai/'
]

try:
    res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore', timeout=20)
    rendered_html = res.stdout
    print(f"Rendered HTML length: {len(rendered_html)}")
    with open('data/storiai/rendered_home.html', 'w', encoding='utf-8') as f:
        f.write(rendered_html)
    print("Saved rendered_home.html")
except Exception as e:
    print("Error:", e)
