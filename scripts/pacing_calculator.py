#!/usr/bin/env python3
"""
Ad Spend Budget Pacer & 72-Hour Scaling Guardrail Evaluator.
"""
import argparse
import sys

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def calculate_pacing(budget, spent, days_passed, total_days):
    if total_days <= 0 or days_passed < 0:
        print("Invalid day parameters.")
        sys.exit(1)
        
    time_pct = (days_passed / total_days) * 100.0
    spend_pct = (spent / budget) * 100.0
    expected_spend = (budget / total_days) * days_passed
    variance = spent - expected_spend
    variance_pct = (variance / expected_spend * 100.0) if expected_spend > 0 else 0.0
    projected_end_spend = (spent / days_passed) * total_days if days_passed > 0 else 0.0
    
    print("=" * 55)
    print("      AD SPEND PACING & SCALING AUDIT REPORT        ")
    print("=" * 55)
    print(f"Total Budget        : ${budget:,.2f}")
    print(f"Spend to Date       : ${spent:,.2f} ({spend_pct:.1f}% spent)")
    print(f"Timeline Elapsed    : Day {days_passed} of {total_days} ({time_pct:.1f}%)")
    print(f"Target Spend to Date: ${expected_spend:,.2f}")
    print(f"Variance            : ${variance:+,.2f} ({variance_pct:+.1f}%)")
    print(f"Projected End Spend : ${projected_end_spend:,.2f}")
    print("-" * 55)
    
    if abs(variance_pct) <= 10:
        print("Status: [ON TRACK] (Spend aligns with linear delivery)")
    elif variance_pct > 10:
        print("Status: [OVERPACING] (Burning budget too quickly - reduce bids/caps)")
    else:
        print("Status: [UNDERPACING] (Behind delivery schedule - check audience size or bids)")
    
    print("\nGuardrail Reminder: Maximum daily budget scale is ≤ 20% per 72 hours.")
    print("=" * 55)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate ad spend pacing")
    parser.add_argument("--budget", type=float, required=True, help="Total period budget in currency units")
    parser.add_argument("--spent", type=float, required=True, help="Spend to date")
    parser.add_argument("--days-passed", type=int, required=True, help="Days elapsed in period")
    parser.add_argument("--total-days", type=int, default=30, help="Total days in period (default: 30)")
    args = parser.parse_args()

    calculate_pacing(args.budget, args.spent, args.days_passed, args.total_days)
