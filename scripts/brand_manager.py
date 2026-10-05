#!/usr/bin/env python3
"""
Brand Manager CLI for Antigravity Performance Marketing Workspace.
Quickly retrieve, list, or validate brand profiles.
"""
import argparse
import json
import os
import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE_ROOT = os.path.dirname(SCRIPT_DIR)
BRANDS_DIR = os.path.join(WORKSPACE_ROOT, "brands")

def list_brands():
    if not os.path.exists(BRANDS_DIR):
        print("No brands directory found.")
        return
    brands = [f.replace(".json", "") for f in os.listdir(BRANDS_DIR) if f.endswith(".json") and not f.startswith("_")]
    print(f"Found {len(brands)} active brand profile(s):")
    for b in sorted(brands):
        with open(os.path.join(BRANDS_DIR, f"{b}.json"), "r", encoding="utf-8") as fp:
            data = json.load(fp)
            name = data.get("brand_name", b)
            vertical = data.get("industry_vertical", "General")
            cpa = data.get("unit_economics", {}).get("target_cpa", "N/A")
            currency = data.get("currency", "$")
            print(f"  • {b} ({name}) — {vertical} | Target CPA: {currency}{cpa}")

def get_brand(slug):
    file_path = os.path.join(BRANDS_DIR, f"{slug}.json")
    if not os.path.exists(file_path):
        print(f"Brand '{slug}' not found in {BRANDS_DIR}")
        sys.exit(1)
    with open(file_path, "r", encoding="utf-8") as fp:
        print(fp.read())

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage brand profiles")
    parser.add_argument("--list", action="store_true", help="List all configured brand profiles")
    parser.add_argument("--get", type=str, help="Print brand profile JSON by slug")
    args = parser.parse_args()

    if args.list or len(sys.argv) == 1:
        list_brands()
    elif args.get:
        get_brand(args.get)
