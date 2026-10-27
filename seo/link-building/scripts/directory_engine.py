#!/usr/bin/env python3
"""
ApexLink Directory Engine
Search, filter, shard, and prepare directory submission queues from the 745+ platform master database.
Supports DR tier filtering, category tagging, dofollow isolation, and idempotent sharding.
"""

import sys
import os
import json
import csv
import hashlib
import argparse

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "master_directories.json")

def load_db():
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database not found at {DB_PATH}")
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_idempotency_key(domain, product_id, route="submit"):
    raw = f"{domain.lower()}:{product_id.lower()}:{route.lower()}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

def filter_directories(db, category=None, min_dr=0, max_dr=100, dofollow_only=False, free_only=True, exclude_dead=True, search_term=None):
    results = []
    for item in db:
        if exclude_dead and item.get("status") == "dead/shut_down":
            continue
        if free_only and (item.get("requires_fee", False) or not item.get("free_tier", True)):
            continue
        if dofollow_only and item.get("follow_type") != "dofollow":
            continue
        
        dr = float(item.get("dr", 0) or 0)
        if dr < min_dr or dr > max_dr:
            continue

        if category:
            cat_lower = category.lower()
            item_cat = item.get("category", "").lower()
            if cat_lower not in item_cat:
                continue

        if search_term:
            term = search_term.lower()
            combined = f"{item.get('name', '')} {item.get('domain', '')} {item.get('category', '')} {item.get('notes', '')}".lower()
            if term not in combined:
                continue

        results.append(item)
    return results

def shard_queue(items, product_id, shard_size=15):
    """
    Partitions directory candidates into execution shards with idempotency tracking.
    """
    shards = []
    current_shard = []
    shard_num = 1

    for item in items:
        key = generate_idempotency_key(item["domain"], product_id)
        enriched = dict(item)
        enriched["idempotency_key"] = key
        enriched["queue_status"] = "queued"
        current_shard.append(enriched)

        if len(current_shard) >= shard_size:
            shards.append({
                "shard_id": f"SHARD_{shard_num:02d}",
                "count": len(current_shard),
                "items": current_shard
            })
            current_shard = []
            shard_num += 1

    if current_shard:
        shards.append({
            "shard_id": f"SHARD_{shard_num:02d}",
            "count": len(current_shard),
            "items": current_shard
        })

    return shards

def main():
    parser = argparse.ArgumentParser(description="Query and shard the Master Directory Database")
    subparsers = parser.add_subparsers(dest="command")

    # Command: list
    list_p = subparsers.add_parser("list", help="List directories matching criteria")
    list_p.add_argument("--category", help="Filter by category substring (AI, SaaS, Startup, Developer, Review, Web 2.0)")
    list_p.add_argument("--min-dr", type=float, default=0, help="Minimum Domain Rating")
    list_p.add_argument("--dofollow", action="store_true", help="Only dofollow sources")
    list_p.add_argument("--search", help="Keyword search in name/domain/notes")
    list_p.add_argument("--limit", type=int, default=25, help="Number of records to display")

    # Command: shard
    shard_p = subparsers.add_parser("shard", help="Generate execution shards for a product")
    shard_p.add_argument("--product-id", required=True, help="Canonical product identifier (e.g. 'my-ai-tool')")
    shard_p.add_argument("--category", help="Target category (e.g. 'AI', 'SaaS')")
    shard_p.add_argument("--min-dr", type=float, default=20, help="Minimum DR threshold")
    shard_p.add_argument("--shard-size", type=int, default=10, help="Number of sites per shard")
    shard_p.add_argument("--output", help="Path to write shards JSON")

    # Command: stats
    stats_p = subparsers.add_parser("stats", help="Show overview statistics of directory database")

    args = parser.parse_args()
    db = load_db()

    if args.command == "stats" or not args.command:
        active = [d for d in db if d.get("status") != "dead/shut_down"]
        dr80 = [d for d in active if d.get("dr", 0) >= 80]
        dr60 = [d for d in active if 60 <= d.get("dr", 0) < 80]
        dr40 = [d for d in active if 40 <= d.get("dr", 0) < 60]
        dofollow = [d for d in active if d.get("follow_type") == "dofollow"]
        
        print("\n" + "="*60)
        print("          APEXLINK MASTER DIRECTORY DATABASE STATS")
        print("="*60)
        print(f"Total Database Entries:      {len(db)}")
        print(f"Active Operational Entries:  {len(active)}")
        print(f"Verified Dofollow Sources:   {len(dofollow)}")
        print(f"Tier 1 Platforms (DR 80+):   {len(dr80)}")
        print(f"Tier 2 Platforms (DR 60-79): {len(dr60)}")
        print(f"Tier 3 Platforms (DR 40-59): {len(dr40)}")
        print(f"Tier 4 Platforms (DR < 40):  {len(active) - len(dr80) - len(dr60) - len(dr40)}")
        print("="*60 + "\n")

    elif args.command == "list":
        filtered = filter_directories(
            db,
            category=args.category,
            min_dr=args.min_dr,
            dofollow_only=args.dofollow,
            search_term=args.search
        )
        print(f"\n[MATCHES: {len(filtered)} platforms | Showing top {min(args.limit, len(filtered))}]\n")
        print(f"{'Domain':<26} | {'DR':<4} | {'Follow':<10} | {'Category'}")
        print("-" * 75)
        for item in filtered[:args.limit]:
            print(f"{item['domain']:<26} | {item['dr']:<4} | {item['follow_type']:<10} | {item['category']}")
        print("\n")

    elif args.command == "shard":
        filtered = filter_directories(
            db,
            category=args.category,
            min_dr=args.min_dr
        )
        shards = shard_queue(filtered, args.product_id, shard_size=args.shard_size)
        print(f"\n[SHARDING COMPLETE]")
        print(f"Product ID:     {args.product_id}")
        print(f"Eligible Sites: {len(filtered)}")
        print(f"Total Shards:   {len(shards)}")
        print(f"Shard Size:     {args.shard_size} sites per shard\n")
        
        for s in shards[:5]:
            print(f"  -> {s['shard_id']}: {s['count']} sites (e.g., {', '.join([x['domain'] for x in s['items'][:3]])}...)")
        if len(shards) > 5:
            print(f"  ... and {len(shards) - 5} more shards.")

        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(shards, f, indent=2)
            print(f"\nShards exported to: {args.output}\n")

if __name__ == "__main__":
    main()
