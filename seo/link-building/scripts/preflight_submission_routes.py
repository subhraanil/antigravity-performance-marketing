#!/usr/bin/env python3
"""
ApexLink Submission Route Preflight & Dispatcher
Probes the submission routes in Shard 01, verifies HTTP status, detects forms,
and generates direct submission payloads.
"""

import os
import sys
import json
import urllib.request
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
}

SHARD_01_ROUTES = [
    {"name": "Clutch.co", "domain": "clutch.co", "url": "https://clutch.co/get-listed", "dr": 91, "auth": "Business Email / LinkedIn"},
    {"name": "Sortlist", "domain": "sortlist.com", "url": "https://www.sortlist.com/claim/agency", "dr": 80, "auth": "Direct Form / Agency Claim"},
    {"name": "Crunchbase", "domain": "crunchbase.com", "url": "https://www.crunchbase.com/add-new", "dr": 90, "auth": "User Account / Free Signup"},
    {"name": "ProvenExpert", "domain": "provenexpert.com", "url": "https://www.provenexpert.com/", "dr": 91, "auth": "Free Business Account"},
    {"name": "TechBehemoths", "domain": "techbehemoths.com", "url": "https://techbehemoths.com/companies/get-listed", "dr": 72, "auth": "Company Registration Form"},
    {"name": "Brownbook", "domain": "brownbook.net", "url": "https://www.brownbook.net/register/", "dr": 79, "auth": "User Registration Form"},
    {"name": "Callupcontact", "domain": "callupcontact.com", "url": "https://www.callupcontact.com/active/register/register.php?", "dr": 76, "auth": "Free Business Submission"},
    {"name": "Bizcommunity", "domain": "bizcommunity.com", "url": "https://www.bizcommunity.com/Signin.aspx", "dr": 78, "auth": "Free Account Sign-in"},
    {"name": "Cybo", "domain": "cybo.com", "url": "https://www.cybo.com/add-business/", "dr": 74, "auth": "Free Business Listing Form"},
    {"name": "Linktree", "domain": "linktr.ee", "url": "https://linktr.ee/register/select-plan", "dr": 94, "auth": "Free Bio-Link Signup"}
]

def probe_routes():
    print("\n" + "="*70)
    print("      APEXLINK PREFLIGHT INSPECTION: SHARD 01 SUBMISSION ROUTES")
    print("="*70)
    
    results = []
    for item in SHARD_01_ROUTES:
        req = urllib.request.Request(item["url"], headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                status = resp.status
                html = resp.read(15000).decode("utf-8", errors="ignore")
                soup = BeautifulSoup(html, "html.parser")
                
                # Check for forms and inputs
                forms = soup.find_all("form")
                has_captcha = "recaptcha" in html.lower() or "turnstile" in html.lower() or "hcaptcha" in html.lower()
                
                badge = "[ONLINE 200]" if status == 200 else f"[HTTP {status}]"
                cap_note = " (Native CAPTCHA Detected)" if has_captcha else ""
                print(f"  {badge:<14} {item['name']:<18} | DR {item['dr']:<3} | Forms: {len(forms)}{cap_note}")
                
                results.append({
                    "name": item["name"],
                    "domain": item["domain"],
                    "url": item["url"],
                    "status": "online",
                    "http_code": status,
                    "has_captcha": has_captcha,
                    "auth": item["auth"]
                })
        except Exception as e:
            print(f"  [ERROR]       {item['name']:<18} | DR {item['dr']:<3} | {e}")
            results.append({
                "name": item["name"],
                "domain": item["domain"],
                "url": item["url"],
                "status": "check_manual",
                "error": str(e),
                "auth": item["auth"]
            })

    print("="*70 + "\n")
    return results

if __name__ == "__main__":
    probe_routes()
