import urllib.request
import ssl
import re

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = 'https://labelitsolutions.co.uk/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
    html = resp.read().decode('utf-8', errors='replace')
    head_match = re.search(r'<head[^>]*>(.*?)</head>', html, re.DOTALL)
    if head_match:
        head = head_match.group(1)
        print('Head length:', len(head))
        links = re.findall(r'<link\s+[^>]*>', head)
        print('Total link tags:', len(links))
        for l in links[:15]:
            print(' ', l)
        
        # Check canonical
        has_canon = any('canonical' in l.lower() for l in links)
        print('Has canonical tag?:', has_canon)
        
        # Check generator
        gen = re.findall(r'<meta\s+name="generator"[^>]*>', head)
        print('Generators:', gen)

print("\n--- CHECKING A PDP HEAD FOR CANONICAL AND SCHEMA ---")
pdp_url = 'https://labelitsolutions.co.uk/product/cardboard-cores-13mm-internal-diameter/'
req2 = urllib.request.Request(pdp_url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req2, context=ctx, timeout=10) as resp:
    html2 = resp.read().decode('utf-8', errors='replace')
    head2 = re.search(r'<head[^>]*>(.*?)</head>', html2, re.DOTALL).group(1)
    links2 = re.findall(r'<link\s+[^>]*>', head2)
    has_canon2 = any('canonical' in l.lower() for l in links2)
    print('PDP Has canonical tag?:', has_canon2)
    
    # Check if rel_canonical was removed
    # In WP, rel_canonical is hooked to wp_head. If an SEO plugin was uninstalled or theme functions.php has:
    # remove_action('wp_head', 'rel_canonical');
    # it silences canonicals.
