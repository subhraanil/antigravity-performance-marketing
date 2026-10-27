#!/usr/bin/env python3
"""
ApexLink Batch Browser Launcher
Opens target directory submission URLs in your default Windows browser
in controlled batches with pre-filled clipboard or terminal guidance.
"""

import sys
import os
import webbrowser
import argparse

TARGETS = {
    "shard1": [
        {"name": "Sortlist (DR 80 Dofollow)", "url": "https://www.sortlist.com/claim/agency"},
        {"name": "ProvenExpert (DR 91 Dofollow)", "url": "https://www.provenexpert.com/"},
        {"name": "TechBehemoths (DR 72 Dofollow)", "url": "https://techbehemoths.com/companies/get-listed"},
        {"name": "Linktree (DR 94 Dofollow)", "url": "https://linktr.ee/register/select-plan"},
        {"name": "Cybo (DR 74 Dofollow)", "url": "https://www.cybo.com/add-business/"},
        {"name": "Callupcontact (DR 76 Dofollow)", "url": "https://www.callupcontact.com/active/register/register.php?"},
        {"name": "Brownbook (DR 79 Dofollow)", "url": "https://www.brownbook.net/register/"},
        {"name": "Bizcommunity (DR 78 Dofollow)", "url": "https://www.bizcommunity.com/Signin.aspx?fa=15&l=196&c=1&menu=134&ru=https%3a%2f%2fwww.bizcommunity.com%2fMyAccount%2fCompanies.aspx"},
        {"name": "Clutch.co (DR 91 Nofollow Authority)", "url": "https://clutch.co/get-listed"},
        {"name": "Crunchbase (DR 90 Nofollow Entity)", "url": "https://www.crunchbase.com/add-new"}
    ],
    "shard2": [
        {"name": "Substack (DR 93 Dofollow)", "url": "https://substack.com"},
        {"name": "AlternativeTo (DR 81 Dofollow)", "url": "https://alternativeto.net/manage-item/"},
        {"name": "Devpost (DR 86 Dofollow)", "url": "https://devpost.com/software/new"},
        {"name": "FeaturedCustomers (DR 71 Dofollow)", "url": "https://www.featuredcustomers.com/"},
        {"name": "G2 (DR 98 Nofollow Authority)", "url": "https://www.g2.com/products/new"},
        {"name": "Medium (DR 94 Nofollow Profile)", "url": "https://medium.com/"},
        {"name": "F6S (DR 86 Nofollow Entity)", "url": "https://www.f6s.com"},
        {"name": "PRLog (DR 83 Nofollow PR)", "url": "https://www.prlog.org/pub/login.html"},
        {"name": "OpenPR (DR 81 Nofollow PR)", "url": "https://www.openpr.com/news/submit.html"},
        {"name": "Startup88 (DR 88 Nofollow Directory)", "url": "https://startup88.typeform.com/to/CRjWqM"}
    ],
    "shard3": [
        {"name": "GoodFirms (DR 83 Dofollow)", "url": "https://www.goodfirms.co/get-listed"},
        {"name": "The Manifest (DR 82 Dofollow via Clutch)", "url": "https://themanifest.com/"},
        {"name": "DesignRush (DR 81 Dofollow)", "url": "https://www.designrush.com/agency-signup"},
        {"name": "Digital Agency Network (DR 75 Dofollow)", "url": "https://digitalagencynetwork.com/membership/"},
        {"name": "GrowthHackers (DR 79 Dofollow)", "url": "https://growthhackers.com/"},
        {"name": "Indie Hackers (DR 86 Dofollow)", "url": "https://www.indiehackers.com/products/new"},
        {"name": "AgencySpotter (DR 65 Dofollow)", "url": "https://www.agencyspotter.com/agencies/new"},
        {"name": "AllMyFaves (DR 73 Dofollow)", "url": "https://allmyfaves.com/"},
        {"name": "UpCity (DR 81 Nofollow)", "url": "https://upcity.com/join"},
        {"name": "SaaSHub (DR 73 Nofollow)", "url": "https://www.saashub.com/submit"}
    ],
    "tier1_fast": [
        {"name": "Sortlist (DR 80 Dofollow)", "url": "https://www.sortlist.com/claim/agency"},
        {"name": "Linktree (DR 94 Dofollow)", "url": "https://linktr.ee/register/select-plan"},
        {"name": "ProvenExpert (DR 91 Dofollow)", "url": "https://www.provenexpert.com/"},
        {"name": "GoodFirms (DR 83 Dofollow)", "url": "https://www.goodfirms.co/get-listed"},
        {"name": "TechBehemoths (DR 72 Dofollow)", "url": "https://techbehemoths.com/companies/get-listed"}
    ],
    "tier1_authority": [
        {"name": "Clutch.co (DR 91)", "url": "https://clutch.co/get-listed"},
        {"name": "Crunchbase (DR 90)", "url": "https://www.crunchbase.com/add-new"},
        {"name": "G2 (DR 98)", "url": "https://www.g2.com/products/new"},
        {"name": "AlternativeTo (DR 81 Dofollow)", "url": "https://alternativeto.net/manage-item/"},
        {"name": "Substack (DR 93 Dofollow)", "url": "https://substack.com"}
    ]
}

def open_batch(batch_name):
    batch_key = batch_name.lower().replace(" ", "_")
    sites = TARGETS.get(batch_key)
    if not sites:
        print(f"Unknown batch '{batch_name}'. Available batches: {list(TARGETS.keys())}")
        return

    print(f"\n============================================================")
    print(f"  LAUNCHING: {len(sites)} Submission Portals for '{batch_key}'")
    print(f"============================================================")
    for s in sites:
        print(f"  -> Opening {s['name']}: {s['url']}")
        try:
            webbrowser.open_new_tab(s["url"])
        except Exception as e:
            print(f"     [Error opening browser]: {e}")
    print("\n[SUCCESS] Batch opened in default browser.")
    print("Copy details from your campaign shard to submit each profile.\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launch directory submission batches")
    parser.add_argument("--batch", choices=list(TARGETS.keys()), default="tier1_fast", help="Batch to launch")
    args = parser.parse_args()
    open_batch(args.batch)
