#!/usr/bin/env python3
"""
ApexLink Autonomous Inbox Reader (cPanel Webmail Engine)
Logs into cPanel webmail using Playwright, accesses Roundcube,
searches for incoming verification emails, extracts activation links or OTPs,
and can optionally click activation links autonomously.
"""

import os
import sys
import re
import time
import json
import argparse
from playwright.sync_api import sync_playwright

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "campaigns", "campaign_config.json")

def load_credentials():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("email_automation", {})

def check_inbox_for_verification(sender_keyword=None, timeout_seconds=60, auto_click=True):
    creds = load_credentials()
    webmail_url = creds.get("webmail_url", "https://paidmediaworld.com:2096/")
    user = creds.get("user")
    pwd = creds.get("pass")

    print(f"\n[INBOX] Connecting to cPanel Webmail for {user}...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        try:
            page.goto(webmail_url, timeout=30000)
            page.fill("input#user", user)
            page.fill("input#pass", pwd)
            page.click("button#login_submit")
            page.wait_for_timeout(3000)

            # Check if Roundcube needs to be launched or is default
            if "jupiter" in page.url:
                print("[INBOX] In cPanel Jupiter interface. Launching Roundcube...")
                # Try clicking Roundcube card/button
                rc_btn = page.locator("a[href*='roundcube'], div.roundcube-card, #btnRoundcube, a:has-text('Roundcube')").first
                if rc_btn.is_visible():
                    rc_btn.click()
                    page.wait_for_timeout(3000)
                else:
                    # Direct session URL navigation
                    token_match = re.search(r'/(cpsess\d+)/', page.url)
                    if token_match:
                        token = token_match.group(1)
                        rc_direct = f"{webmail_url.rstrip('/')}/{token}/3rdparty/roundcube/index.php"
                        page.goto(rc_direct)
                        page.wait_for_timeout(3000)

            print(f"[INBOX] Current mail page: '{page.title()}'")

            # Polling for email
            start_time = time.time()
            found_email = False
            activation_link = None
            otp_code = None

            print(f"[INBOX] Polling for emails matching keyword '{sender_keyword or 'ANY'}' (Max wait: {timeout_seconds}s)...")
            while time.time() - start_time < timeout_seconds:
                # Refresh or check message list
                page.wait_for_timeout(2000)
                messages = page.locator("tr.message, table#messagelist tbody tr").all()
                
                for msg in messages:
                    text = msg.inner_text().lower()
                    if sender_keyword and sender_keyword.lower() not in text:
                        continue
                    
                    print(f"[INBOX] Found matching email: {msg.inner_text().splitlines()[0]}")
                    msg.click()
                    page.wait_for_timeout(2000)
                    found_email = True
                    break

                if found_email:
                    break

                # Click refresh icon in Roundcube if available
                refresh_btn = page.locator("a#rcmbtn101, a[title*='Check for new messages'], a.checkmail").first
                if refresh_btn.is_visible():
                    refresh_btn.click()
                time.sleep(4)

            if not found_email:
                print("[INBOX] No matching new email received within timeout window.")
                return {"success": False, "reason": "timeout"}

            # Read email body
            body_text = page.locator("#messagebody, #message-html").inner_text()
            html_content = page.locator("#messagebody, #message-html").inner_html()

            # Regex search for activation link
            links = re.findall(r'https?://[^\s"\'<>]+(?:confirm|verify|activate|token|validation)[^\s"\'<>]*', html_content, re.IGNORECASE)
            if not links:
                links = re.findall(r'https?://[^\s"\'<>]+', html_content)
                # Filter out standard images / unsubscriptions
                links = [l for l in links if not any(x in l for x in ['.png', '.jpg', 'unsubscribe', 'privacy'])]

            if links:
                activation_link = links[0]
                print(f"[INBOX] Extracted Activation Link: {activation_link}")

            # Regex search for 4-8 digit OTP code
            otp_match = re.search(r'\b(?:\d{4}|\d{6}|\d{8})\b', body_text)
            if otp_match:
                otp_code = otp_match.group(0)
                print(f"[INBOX] Extracted OTP Code: {otp_code}")

            if auto_click and activation_link:
                print(f"[INBOX] Auto-clicking activation link...")
                verify_page = context.new_page()
                verify_page.goto(activation_link, timeout=30000)
                verify_page.wait_for_timeout(4000)
                print(f"[INBOX] Verification landing page: '{verify_page.title()}'")
                verify_page.close()

            return {
                "success": True,
                "activation_link": activation_link,
                "otp": otp_code,
                "email_preview": body_text[:200]
            }

        except Exception as e:
            print(f"[!] Inbox error: {e}")
            return {"success": False, "error": str(e)}
        finally:
            browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous Inbox Reader")
    parser.add_argument("--keyword", help="Filter by sender/subject keyword")
    parser.add_argument("--timeout", type=int, default=30, help="Wait timeout in seconds")
    parser.add_argument("--no-click", action="store_true", help="Don't auto click verification links")
    args = parser.parse_args()

    res = check_inbox_for_verification(sender_keyword=args.keyword, timeout_seconds=args.timeout, auto_click=not args.no_click)
    print(json.dumps(res, indent=2))
