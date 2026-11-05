import os
import re

def verify_no_newlines():
    tmp_dir = ".tmp"
    files = [f for f in os.listdir(tmp_dir) if f.endswith(".html")]
    
    tags = ['p', 'li', 'td', 'h2', 'h3']
    total_issues = 0
    
    for filename in files:
        filepath = os.path.join(tmp_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        file_issues = 0
        for tag in tags:
            pattern = f'<{tag}[^>]*>(.*?)<\/{tag}>'
            matches = re.findall(pattern, content, re.DOTALL)
            for match in matches:
                if '\n' in match:
                    file_issues += 1
        
        if file_issues > 0:
            print(f"File {filename} has {file_issues} tags with newlines.")
            total_issues += file_issues
            
    if total_issues == 0:
        print("CONFIRMED: All blog posts are clean of manual line breaks within sentences.")
    else:
        print(f"TOTAL ISSUES FOUND: {total_issues}")

if __name__ == "__main__":
    verify_no_newlines()
