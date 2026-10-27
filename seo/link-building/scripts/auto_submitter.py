#!/usr/bin/env python3
"""
ApexLink Autonomous Submissions Bot (Playwright Engine)
Automates directory account creation and submission form filling.
Supports headless execution or visible headful mode for live observation.
"""

import os
import sys
import json
import time
import argparse
from playwright.sync_api import sync_playwright

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "campaigns", "campaign_config.json")

def load_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Configuration file missing at {CONFIG_PATH}")
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def run_submission_bot(target_name, headless=False):
    config = load_config()
    binfo = config["business_info"]
    creds = config["submission_credentials"]

    print(f"\n============================================================")
    print(f"  LAUNCHING AUTONOMOUS BOT: {target_name.upper()}")
    print(f"  Target Website: {binfo['canonical_url']}")
    print(f"  Submission Email: {creds['submission_email']}")
    print(f"  Browser Mode: {'Headless' if headless else 'Visible (Headful)'}")
    print(f"============================================================\n")

    with sync_playwright() as p:
        # Launch browser with user-agent mimicking real desktop
        browser = p.chromium.launch(
            headless=headless,
            args=["--disable-blink-features=AutomationControlled", "--start-maximized"]
        )
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        try:
            if target_name == "sortlist":
                print("[BOT] Navigating to Sortlist claim agency portal...")
                page.goto("https://www.sortlist.com/claim/agency", timeout=60000)
                page.wait_for_timeout(3000)
                print(f"[BOT] Page loaded: '{page.title()}'")
                
                # Try finding agency name input
                name_input = page.locator("input[name*='name'], input[placeholder*='agency'], input[placeholder*='name'], input[type='text']").first
                if name_input.is_visible():
                    print("[BOT] Filling agency name: Paid Media World")
                    name_input.fill(binfo["brand_name"])
                    page.wait_for_timeout(1000)

            elif target_name == "techbehemoths":
                print("[BOT] Navigating to TechBehemoths get-listed...")
                page.goto("https://techbehemoths.com/companies/get-listed", timeout=60000)
                page.wait_for_timeout(3000)
                print(f"[BOT] Page loaded: '{page.title()}'")

            elif target_name == "provenexpert":
                print("[BOT] Navigating to ProvenExpert registration...")
                page.goto("https://www.provenexpert.com/", timeout=60000)
                page.wait_for_timeout(3000)
                print(f"[BOT] Page loaded: '{page.title()}'")

            else:
                print(f"[BOT] Custom target '{target_name}' requested. Testing navigation...")
                page.goto(target_name if target_name.startswith("http") else f"https://{target_name}", timeout=60000)
                page.wait_for_timeout(3000)
                print(f"[BOT] Page loaded: '{page.title()}'")

            print("\n[BOT] Autonomous form phase complete. Browser session active.")
            if not headless:
                print("[BOT] Keeping session open for 15 seconds so you can inspect...")
                page.wait_for_timeout(15000)

        except Exception as e:
            print(f"[!] Bot execution error: {e}")
        finally:
            browser.close()
            print("[BOT] Finished and closed session.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Link Building Bot")
    parser.add_argument("--target", default="sortlist", help="Target platform (sortlist, techbehemoths, provenexpert, or URL)")
    parser.add_argument("--headless", action="store_true", help="Run without UI window")
    args = parser.parse_args()
    run_submission_bot(args.target, headless=args.headless)
