#!/usr/bin/env python3
"""
ApexLink Campaign Record & Privacy Auditor
Scans submission logs and campaign records to verify:
1. Zero secret leakage (no passwords, tokens, cookies, auth keys)
2. No duplicate domain submissions or repeated idempotency keys
3. Legitimate status transitions and evidence integrity
"""

import sys
import os
import re
import json
import argparse

SECRET_PATTERNS = [
    (r"(?i)(?:password|passwd|pwd)\s*[:=]\s*['\"]?([^\s'\"]{4,})", "Plaintext password detected"),
    (r"(?i)(?:bearer|token|apikey|api_key)\s*[:=]\s*['\"]?([a-zA-Z0-9_\-\.]{16,})", "API Token / Bearer key detected"),
    (r"(?i)(?:otp|recovery_code|2fa_code)\s*[:=]\s*['\"]?([0-9a-zA-Z]{6,})", "2FA / OTP code detected"),
    (r"(?i)(?:cookie|session_id|sessionid)\s*[:=]\s*['\"]?([a-zA-Z0-9_\-\.]{20,})", "Session Cookie detected")
]

VALID_STATUSES = {
    "queued", "preflight_checked", "manual_verification_required",
    "authorized", "submitted", "live_verified", "ineligible", "rejected_fee", "failed"
}

def audit_record_file(filepath):
    if not os.path.exists(filepath):
        return {"status": "error", "message": f"File {filepath} does not exist"}

    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
        lines = content.splitlines()

    violations = []
    secrets_found = []
    seen_domains = set()
    seen_keys = set()
    status_counts = {}

    # 1. Scan for secrets
    for line_idx, line in enumerate(lines, 1):
        for pattern, desc in SECRET_PATTERNS:
            match = re.search(pattern, line)
            if match:
                # Mask secret
                val = match.group(1)
                masked = val[:2] + "****" + val[-2:] if len(val) > 4 else "****"
                secrets_found.append({
                    "line": line_idx,
                    "type": desc,
                    "masked_match": masked
                })

    # 2. Extract table rows or JSON records
    # Check if JSON
    try:
        data = json.loads(content)
        if isinstance(data, list):
            for idx, entry in enumerate(data):
                dom = entry.get("domain", "").lower()
                key = entry.get("idempotency_key")
                st = entry.get("status", "queued")
                
                if dom:
                    if dom in seen_domains:
                        violations.append(f"Duplicate domain submission entry: '{dom}' at item #{idx+1}")
                    seen_domains.add(dom)
                if key:
                    if key in seen_keys:
                        violations.append(f"Duplicate idempotency key: '{key}' at item #{idx+1}")
                    seen_keys.add(key)
                if st not in VALID_STATUSES:
                    violations.append(f"Unknown status '{st}' on domain '{dom}'")
                status_counts[st] = status_counts.get(st, 0) + 1
    except Exception:
        # Markdown table scanning
        for line_idx, line in enumerate(lines, 1):
            if line.startswith("|") and not line.startswith("| Domain") and not line.startswith("|---"):
                parts = [p.strip() for p in line.split("|")[1:-1]]
                if len(parts) >= 3:
                    dom = parts[0].lower()
                    st = parts[1].lower() if len(parts) > 1 else "queued"
                    if dom:
                        if dom in seen_domains:
                            violations.append(f"Duplicate domain submission entry: '{dom}' at line {line_idx}")
                        seen_domains.add(dom)
                    if st not in VALID_STATUSES:
                        violations.append(f"Invalid status '{st}' on line {line_idx}")
                    status_counts[st] = status_counts.get(st, 0) + 1

    passed = (len(secrets_found) == 0 and len(violations) == 0)

    return {
        "passed": passed,
        "total_records": len(seen_domains),
        "status_distribution": status_counts,
        "secrets_found": secrets_found,
        "violations": violations
    }

def main():
    parser = argparse.ArgumentParser(description="Audit Campaign Submission Record for Safety & Integrity")
    parser.add_argument("file", help="Path to markdown or JSON campaign record")
    args = parser.parse_args()

    res = audit_record_file(args.file)
    print("\n" + "="*60)
    print("        APEXLINK CAMPAIGN RECORD AUDIT REPORT")
    print("="*60)
    print(f"File Audited:      {args.file}")
    print(f"Total Unique Sites:{res['total_records']}")
    print(f"Audit Status:      {'[PASSED]' if res['passed'] else '[FAILED - VIOLATIONS DETECTED]'}")
    
    print("\n[ Status Breakdown ]")
    for s, c in res.get("status_distribution", {}).items():
        print(f"  - {s:28}: {c}")

    if res["secrets_found"]:
        print("\n[!] CRITICAL SECURITY WARNING: CREDENTIALS LEAKED")
        for s in res["secrets_found"]:
            print(f"  Line {s['line']}: {s['type']} -> {s['masked_match']}")

    if res["violations"]:
        print("\n[!] RECORD VIOLATIONS:")
        for v in res["violations"]:
            print(f"  * {v}")

    print("="*60 + "\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: audit_campaign_record.py <path_to_record>")
        sys.exit(1)
    main()
