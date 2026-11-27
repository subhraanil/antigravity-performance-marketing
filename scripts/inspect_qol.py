import requests
from bs4 import BeautifulSoup
import sys
if sys.stdout.encoding != 'utf-8': sys.stdout.reconfigure(encoding='utf-8')

r = requests.get('https://makemealabel.com/products/100mm-x-152mm-6-by-4-direct-thermal-roll-labels', headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(r.text, 'html.parser')

qol = soup.find(class_=lambda x: x and 'quick-order-list' in x)
if qol:
    print("=== QUICK ORDER LIST FOUND ===")
    print("Class:", qol.get("class"))
    print("Content preview:")
    print(qol.get_text("\n", strip=True)[:1000])
else:
    print("No quick-order-list element found")
