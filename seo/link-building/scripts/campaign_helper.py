#!/usr/bin/env python3
"""
ApexLink Campaign Manager & Live Status Tracker
Automates campaign overview, progress tracking, and live verification integration across all shards.
"""

import os
import sys
import re
import argparse
from datetime import datetime
from link_verifier import verify_single_backlink

CAMPAIGNS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "campaigns")

def get_campaign_shards():
    if not os.path.exists(CAMPAIGNS_DIR):
        return []
    shards = []
    for f in sorted(os.listdir(CAMPAIGNS_DIR)):
        if f.startswith("paidmediaworld_shard_") and f.endswith(".md"):
            shards.append(os.path.join(CAMPAIGNS_DIR, f))
    return shards

def summarize_campaigns():
    shards = get_campaign_shards()
    print("\n" + "="*70)
    print("      PAID MEDIA WORLD — MASTER LINK BUILDING STATUS")
    print("="*70)
    
    total_sites = 0
    status_counts = {"queued": 0, "submitted": 0, "live_verified": 0}
    dr_tiers = {"Tier 1 (DR 80+)": 0, "Tier 2 (DR 60-79)": 0}

    for s_path in shards:
        fname = os.path.basename(s_path)
        with open(s_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        shard_rows = []
        for line in lines:
            if line.startswith("|") and not line.startswith("| Domain") and not line.startswith("|---"):
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 4:
                    dom = parts[0]
                    st = parts[1]
                    try:
                        dr = float(parts[2])
                    except:
                        dr = 0
                    fol = parts[3]
                    shard_rows.append({"dom": dom, "status": st, "dr": dr, "follow": fol})
                    status_counts[st] = status_counts.get(st, 0) + 1
                    total_sites += 1
                    if dr >= 80:
                        dr_tiers["Tier 1 (DR 80+)"] += 1
                    else:
                        dr_tiers["Tier 2 (DR 60-79)"] += 1

        print(f"\n[ {fname} ] -> {len(shard_rows)} Targets")
        for r in shard_rows:
            badge = "[LIVE]" if r["status"] == "live_verified" else ("[SENT]" if r["status"] == "submitted" else "[QUEUED]")
            print(f"  {badge:8} {r['dom']:<26} | DR {r['dr']:<4} | {r['follow']:<10}")

    print("\n" + "-"*70)
    print(f"Total Targets Across All Shards: {total_sites}")
    print(f"  - Queued:        {status_counts.get('queued', 0)}")
    print(f"  - Submitted:     {status_counts.get('submitted', 0)}")
    print(f"  - Live Verified: {status_counts.get('live_verified', 0)}")
    print(f"Authority Profile:")
    print(f"  - Tier 1 (DR 80+):  {dr_tiers['Tier 1 (DR 80+)']} platforms")
    print(f"  - Tier 2 (DR 60-79): {dr_tiers['Tier 2 (DR 60-79)']} platforms")
    print("="*70 + "\n")

def verify_and_update(source_url, target_domain="paidmediaworld.com"):
    print(f"\n[VERIFY] Probing {source_url} for active link to {target_domain}...")
    res = verify_single_backlink(source_url, target_domain)
    
    if res["link_found"]:
        print(f"[SUCCESS] Live backlink confirmed!")
        print(f"  - Anchor Text: '{res['anchor_text']}'")
        print(f"  - Rel Type:    {res['rel']} ({'DOFOLLOW' if res['is_dofollow'] else 'NOFOLLOW'})")
        print(f"  - Destination: {res['primary_href']}")
        
        # Search which shard contains this domain and update table
        clean_src = source_url.lower()
        shards = get_campaign_shards()
        updated = False
        today = datetime.now().strftime("%Y-%m-%d")

        for s_path in shards:
            with open(s_path, "r", encoding="utf-8") as f:
                content = f.read()

            lines = content.splitlines()
            new_lines = []
            for line in lines:
                if line.startswith("|") and not line.startswith("| Domain") and not line.startswith("|---"):
                    parts = [p.strip() for p in line.split("|")[1:-1]]
                    if len(parts) >= 8:
                        dom = parts[0].lower()
                        if dom in clean_src:
                            # Update status, live URL, and date
                            parts[1] = "live_verified"
                            parts[5] = source_url
                            parts[7] = today
                            new_line = "| " + " | ".join(parts) + " |"
                            new_lines.append(new_line)
                            updated = True
                            continue
                new_lines.append(line)

            if updated:
                with open(s_path, "w", encoding="utf-8") as f:
                    f.write("\n".join(new_lines) + "\n")
                print(f"[UPDATED] Marked '{source_url}' as live_verified in {os.path.basename(s_path)}")
                break
    else:
        print(f"[!] Link verification check returned: {res['status']}")
        print(f"    Check error / status: {res.get('error', 'Anchor matching target not found in rendered DOM')}")

def main():
    parser = argparse.ArgumentParser(description="Paid Media World Campaign Helper")
    parser.add_argument("--status", action="store_true", help="Print status overview of all shards")
    parser.add_argument("--verify", help="Live profile URL to verify and mark as live_verified")
    parser.add_argument("--target", default="paidmediaworld.com", help="Target domain")
    args = parser.parse_args()

    if args.verify:
        verify_and_update(args.verify, args.target)
    else:
        summarize_campaigns()

if __name__ == "__main__":
    main()
