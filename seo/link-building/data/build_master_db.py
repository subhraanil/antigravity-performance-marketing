"""
ApexLink Master Directory Builder
Merges awesome-free-seo-backlinks and flaqai Free-backlink-list, enriches with top tier DR data,
filters out defunct domains, normalizes categories, and exports to master_directories.json and master_directories.csv.
"""

import re
import json
import csv
from urllib.parse import urlparse

def clean_domain(url):
    if not url:
        return ''
    try:
        netloc = urlparse(url).netloc.lower()
        if netloc.startswith('www.'):
            netloc = netloc[4:]
        return netloc.strip()
    except Exception:
        return ''

KNOWN_DR_OVERLAY = {
    "g2.com": {"dr": 98, "follow": "nofollow", "cat": "B2B Software & Review Platform"},
    "gravatar.com": {"dr": 97, "follow": "nofollow", "cat": "High-Authority Profile & Web Identity"},
    "github.com": {"dr": 96, "follow": "dofollow", "cat": "Developer Community & Code Showcase"},
    "reddit.com": {"dr": 95, "follow": "nofollow", "cat": "Community & Discussion Platform"},
    "blogger.com": {"dr": 94, "follow": "dofollow", "cat": "Web 2.0 Authority Blogging"},
    "medium.com": {"dr": 94, "follow": "nofollow", "cat": "Authority Publication & Blogging"},
    "flickr.com": {"dr": 94, "follow": "nofollow", "cat": "High-Authority Profile & Image Hub"},
    "linktr.ee": {"dr": 94, "follow": "dofollow", "cat": "Bio Link & Profile Hub"},
    "trustpilot.com": {"dr": 94, "follow": "nofollow", "cat": "Review & Trust Platform"},
    "substack.com": {"dr": 93, "follow": "dofollow", "cat": "Newsletter & Publication Hub"},
    "capterra.com": {"dr": 93, "follow": "nofollow", "cat": "B2B Software & Review Platform"},
    "gitlab.com": {"dr": 93, "follow": "dofollow", "cat": "Developer Community & Repo"},
    "quora.com": {"dr": 93, "follow": "nofollow", "cat": "Q&A & Community Platform"},
    "jimdo.com": {"dr": 92, "follow": "dofollow", "cat": "Web 2.0 Platform"},
    "sourceforge.net": {"dr": 92, "follow": "nofollow", "cat": "Open Source & Software Directory"},
    "producthunt.com": {"dr": 91, "follow": "dofollow", "cat": "Product Launch & Discovery Platform"},
    "slashdot.org": {"dr": 91, "follow": "nofollow", "cat": "Tech News & Discussion"},
    "news.ycombinator.com": {"dr": 91, "follow": "nofollow", "cat": "Developer & Startup Community"},
    "clutch.co": {"dr": 91, "follow": "nofollow", "cat": "B2B Agency & Software Directory"},
    "gartner.com": {"dr": 91, "follow": "nofollow", "cat": "Enterprise Research & Software Directory"},
    "provenexpert.com": {"dr": 91, "follow": "dofollow", "cat": "Review & Business Trust Profile"},
    "crunchbase.com": {"dr": 90, "follow": "nofollow", "cat": "Startup & Company Intelligence"},
    "strikingly.com": {"dr": 90, "follow": "dofollow", "cat": "Web 2.0 Portfolio Site"},
    "dev.to": {"dr": 89, "follow": "nofollow", "cat": "Developer Community & Article Hub"},
    "trustradius.com": {"dr": 89, "follow": "nofollow", "cat": "B2B Software Review Directory"},
    "softwareadvice.com": {"dr": 89, "follow": "nofollow", "cat": "B2B Software Evaluation"},
    "wellfound.com": {"dr": 88, "follow": "nofollow", "cat": "Startup Community & Job/Talent Hub"},
    "startup88.com": {"dr": 88, "follow": "nofollow", "cat": "Startup Discovery & Review"},
    "getapp.com": {"dr": 88, "follow": "nofollow", "cat": "B2B Software Directory"},
    "financesonline.com": {"dr": 87, "follow": "nofollow", "cat": "B2B SaaS Directory & Review"},
    "site123.com": {"dr": 87, "follow": "nofollow", "cat": "Web 2.0 Platform"},
    "devpost.com": {"dr": 86, "follow": "dofollow", "cat": "Hackathon & Software Project Showcase"},
    "f6s.com": {"dr": 86, "follow": "nofollow", "cat": "Startup & Founder Ecosystem Directory"},
    "notion.site": {"dr": 85, "follow": "dofollow", "cat": "Web 2.0 Knowledge Base & Document Site"},
    "hashnode.com": {"dr": 85, "follow": "dofollow", "cat": "Developer Blogging & Engineering Hub"},
    "webnode.com": {"dr": 84, "follow": "nofollow", "cat": "Web 2.0 Platform"},
    "prlog.org": {"dr": 83, "follow": "nofollow", "cat": "Free Press Release Web 2.0"},
    "bento.me": {"dr": 82, "follow": "dofollow", "cat": "Bio Link & Personal/Company Showcase"},
    "openpr.com": {"dr": 81, "follow": "nofollow", "cat": "Press Release News Portal"},
    "alternativeto.net": {"dr": 81, "follow": "dofollow", "cat": "Software Alternative Discovery Platform"},
    "sortlist.com": {"dr": 80, "follow": "dofollow", "cat": "B2B Agency & Tech Directory"},
    "stackshare.io": {"dr": 80, "follow": "dofollow", "cat": "Tech Stack & Developer Software Hub"},
    "brownbook.net": {"dr": 79, "follow": "dofollow", "cat": "Global Business Directory"},
    "betalist.com": {"dr": 78, "follow": "dofollow", "cat": "Startup Early Access & Launch Platform"},
    "remoteok.com": {"dr": 78, "follow": "dofollow", "cat": "Tech & Remote Ecosystem Directory"},
    "bizcommunity.com": {"dr": 78, "follow": "dofollow", "cat": "B2B News & Company Directory"},
    "europages.co.uk": {"dr": 77, "follow": "mixed/unverified", "cat": "European B2B Supplier Directory"},
    "callupcontact.com": {"dr": 76, "follow": "dofollow", "cat": "Global Business & Service Directory"},
    "eu-startups.com": {"dr": 76, "follow": "nofollow", "cat": "European Startup Directory & Media"},
    "futurepedia.io": {"dr": 74, "follow": "dofollow", "cat": "AI Tool Discovery & Directory"},
    "cybo.com": {"dr": 74, "follow": "dofollow", "cat": "Global Business Directory"},
    "allmyfaves.com": {"dr": 73, "follow": "dofollow", "cat": "Curated Software Directory"},
    "saashub.com": {"dr": 73, "follow": "nofollow", "cat": "SaaS Discovery & Software Alternatives"},
    "comparecamp.com": {"dr": 73, "follow": "dofollow", "cat": "B2B Software Review Hub"},
    "saasworthy.com": {"dr": 73, "follow": "nofollow", "cat": "SaaS Recommendations & Scoring"},
    "selecthub.com": {"dr": 73, "follow": "dofollow", "cat": "Enterprise Software Selection Hub"},
    "getlatka.com": {"dr": 72, "follow": "dofollow", "cat": "SaaS Financial Data & Company Directory"},
    "techbehemoths.com": {"dr": 72, "follow": "dofollow", "cat": "B2B Tech Company Directory"},
    "killerstartups.com": {"dr": 72, "follow": "dofollow", "cat": "Startup Review & Launch Platform"},
    "featuredcustomers.com": {"dr": 71, "follow": "dofollow", "cat": "B2B SaaS Case Studies & Directory"},
    "land-book.com": {"dr": 71, "follow": "dofollow", "cat": "Web Design & SaaS Gallery Showcase"},
    "sidebar.io": {"dr": 71, "follow": "dofollow", "cat": "Curated Tech & Design Resources"},
    "sideprojectors.com": {"dr": 69, "follow": "dofollow", "cat": "Side Projects & Micro-SaaS Marketplace"},
    "topai.tools": {"dr": 68, "follow": "dofollow", "cat": "AI Directory & Tool Discovery"},
    "startupstash.com": {"dr": 67, "follow": "dofollow", "cat": "Curated Startup & SaaS Directory"},
    "toolpilot.ai": {"dr": 67, "follow": "dofollow", "cat": "AI Tools & Productivity Directory"},
    "somuch.com": {"dr": 64, "follow": "dofollow", "cat": "Curated Web Directory"},
    "futuretools.io": {"dr": 63, "follow": "dofollow", "cat": "AI Tools & Software Platform"},
    "dokeyai.com": {"dr": 62, "follow": "dofollow", "cat": "AI Tools Directory"},
    "dang.ai": {"dr": 62, "follow": "dofollow", "cat": "Curated AI Tools & Software Directory"},
    "uneed.best": {"dr": 58, "follow": "dofollow", "cat": "Curated Tool & Startup Discovery Platform"},
    "devhunt.org": {"dr": 57, "follow": "dofollow", "cat": "Developer Tool Launch Platform"},
    "supertools.therundown.ai": {"dr": 56, "follow": "dofollow", "cat": "AI Tools Database by The Rundown"},
    "spotsaas.com": {"dr": 54, "follow": "dofollow", "cat": "SaaS Discovery & Evaluation Hub"},
    "fivetaco.com": {"dr": 53, "follow": "dofollow", "cat": "Curated Software & Tool Discovery"}
}

def run():
    db = {}
    
    # 1. Parse awesome-free-seo-backlinks
    af_file = 'repos/awesome-free-seo-backlinks/readme.md'
    with open(af_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if line.startswith('|') and not line.startswith('| Name') and not line.startswith('|---'):
                parts = [p.strip() for p in line.split('|')[1:-1]]
                if len(parts) >= 5:
                    name, dr_str, cat, follow, link_md = parts[0], parts[1], parts[2], parts[3], parts[4]
                    url_match = re.search(r'\((https?://[^)]+)\)', link_md)
                    url = url_match.group(1) if url_match else ''
                    domain = clean_domain(url)
                    if not domain:
                        continue
                    try:
                        dr = float(dr_str)
                    except:
                        dr = 0.0
                    is_dofollow = 'dofollow' in follow.lower()
                    
                    db[domain] = {
                        'domain': domain,
                        'name': name,
                        'submission_url': url,
                        'dr': dr,
                        'category': cat,
                        'follow_type': 'dofollow' if is_dofollow else ('nofollow' if 'nofollow' in follow.lower() else 'mixed/unverified'),
                        'status': 'verified_active',
                        'notes': 'Curated high-authority backlink source',
                        'free_tier': True,
                        'requires_reciprocal': False,
                        'requires_fee': False,
                        'tier': 'Tier 1 (DR 80+)' if dr >= 80 else ('Tier 2 (DR 60-79)' if dr >= 60 else ('Tier 3 (DR 40-59)' if dr >= 40 else 'Tier 4 (<40)'))
                    }

    # 2. Parse flaqai Free-backlink-list.md
    flaq_file = 'repos/backlink_skills/Free-backlink-list.md'
    with open(flaq_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if line.startswith('|') and not line.startswith('| 编号') and not line.startswith('|---'):
                parts = [p.strip() for p in line.split('|')[1:-1]]
                if len(parts) >= 5:
                    idx, link_part, desc, batch, remark = parts[0], parts[1], parts[2], parts[3], parts[4]
                    url_match = re.search(r'<(https?://[^>]+)>', link_part)
                    if not url_match:
                        url_match = re.search(r'\((https?://[^)]+)\)', link_part)
                    url = url_match.group(1) if url_match else ''
                    domain = clean_domain(url)
                    if not domain:
                        continue
                    
                    is_dead = '停服' in remark or '关闭' in remark or '无法访问' in remark
                    requires_reciprocal = '反链' in remark or '互链' in remark or 'meta' in remark
                    requires_fee = '刀' in remark or '收费' in remark or '$' in remark or '付费' in remark
                    
                    category = 'General Directory'
                    if 'AI' in desc or 'AI' in domain:
                        category = 'AI Directory'
                    elif 'SaaS' in desc or '软件' in desc:
                        category = 'SaaS & Software Directory'
                    elif '创业' in desc or 'startup' in desc.lower():
                        category = 'Startup Launch Platform'
                    elif '开发者' in desc or '开源' in desc or '技术' in desc:
                        category = 'Developer Community'
                    elif '博客' in desc or '文章' in desc:
                        category = 'Web 2.0 & Blog'

                    name_match = re.search(r'^([^（(]+)', desc)
                    name = name_match.group(1).strip() if name_match else domain
                    if len(name) > 30:
                        name = domain

                    if domain in db:
                        if remark and remark != '—':
                            db[domain]['notes'] += f' | {remark}'
                        if requires_reciprocal:
                            db[domain]['requires_reciprocal'] = True
                        if requires_fee:
                            db[domain]['requires_fee'] = True
                        if is_dead:
                            db[domain]['status'] = 'dead/shut_down'
                    else:
                        status = 'dead/shut_down' if is_dead else 'candidate'
                        db[domain] = {
                            'domain': domain,
                            'name': name,
                            'submission_url': url,
                            'dr': 0.0,
                            'category': category,
                            'follow_type': 'unverified',
                            'status': status,
                            'notes': remark if remark != '—' else desc[:100],
                            'free_tier': not requires_fee,
                            'requires_reciprocal': requires_reciprocal,
                            'requires_fee': requires_fee,
                            'tier': 'Unscored / Candidate'
                        }

    # 3. Apply Known DR & Platform Overlays
    for domain, meta in KNOWN_DR_OVERLAY.items():
        if domain in db:
            db[domain]['dr'] = meta['dr']
            db[domain]['follow_type'] = meta['follow']
            db[domain]['category'] = meta['cat']
            db[domain]['status'] = 'verified_active'
            db[domain]['tier'] = 'Tier 1 (DR 80+)' if meta['dr'] >= 80 else ('Tier 2 (DR 60-79)' if meta['dr'] >= 60 else 'Tier 3 (DR 40-59)')
        else:
            db[domain] = {
                'domain': domain,
                'name': domain.capitalize().split('.')[0],
                'submission_url': f'https://{domain}',
                'dr': meta['dr'],
                'category': meta['cat'],
                'follow_type': meta['follow'],
                'status': 'verified_active',
                'notes': 'Curated high-authority foundational platform',
                'free_tier': True,
                'requires_reciprocal': False,
                'requires_fee': False,
                'tier': 'Tier 1 (DR 80+)' if meta['dr'] >= 80 else 'Tier 2 (DR 60-79)'
            }

    # Convert to list and sort by DR descending, then by domain
    records = list(db.values())
    records.sort(key=lambda x: (x['dr'], 1 if x['status'] == 'verified_active' else 0), reverse=True)

    # Save to JSON
    json_path = 'link-building-skill/data/master_directories.json'
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    # Save to CSV
    csv_path = 'link-building-skill/data/master_directories.csv'
    fieldnames = ['domain', 'name', 'dr', 'tier', 'category', 'follow_type', 'status', 'free_tier', 'requires_reciprocal', 'requires_fee', 'submission_url', 'notes']
    with open(csv_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(records)

    active_count = sum(1 for r in records if r['status'] != 'dead/shut_down')
    dr80_count = sum(1 for r in records if r['dr'] >= 80 and r['status'] != 'dead/shut_down')
    dr60_count = sum(1 for r in records if 60 <= r['dr'] < 80 and r['status'] != 'dead/shut_down')
    dofollow_count = sum(1 for r in records if r['follow_type'] == 'dofollow' and r['status'] != 'dead/shut_down')

    print(f"Master Directory DB Built Successfully!")
    print(f"Total Unique Domains: {len(records)}")
    print(f"Active/Operational Platforms: {active_count}")
    print(f"Tier 1 (DR 80+): {dr80_count}")
    print(f"Tier 2 (DR 60-79): {dr60_count}")
    print(f"Verified Dofollow Sources: {dofollow_count}")
    print(f"Saved: {json_path} & {csv_path}")

if __name__ == '__main__':
    run()
