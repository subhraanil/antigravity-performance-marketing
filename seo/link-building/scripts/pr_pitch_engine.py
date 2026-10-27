#!/usr/bin/env python3
"""
ApexLink Digital PR & Journalist Pitch Engine
Automates journalist opportunity qualification, Stage-3 linkable asset heuristic scoring,
high-converting pitch generation (4 frameworks), and outbound duplicate tracking.
Inspired by Qwoted, HARO, Connectively, and Featured workflows.
"""

import sys
import os
import json
import argparse
from datetime import datetime

SENT_LOG_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sent_pitches.json")

def score_pr_opportunity(request_data):
    """
    Applies the Stage-3 Heuristic to determine whether to build a dedicated statistics page.
    """
    topic = request_data.get("topic", "")
    ask = request_data.get("ask", "").lower()
    deadline_hours = float(request_data.get("deadline_hours", 48))
    is_personal_anecdote = request_data.get("is_anecdote", False)
    is_paid_placement = request_data.get("is_paid", False)

    score = 0
    reasons = []

    # Heuristic 1: Broad topic with public data available
    broad_keywords = ["ai", "marketing", "saas", "seo", "e-commerce", "remote", "cybersecurity", "productivity", "cloud", "sales", "finance"]
    if any(k in topic.lower() for k in broad_keywords):
        score += 2
        reasons.append("+2: Broad high-interest topic with rich industry benchmarks")

    # Heuristic 2: Asks for data / numbers / statistics / trends
    if any(term in ask for term in ["stat", "data", "number", "research", "trend", "survey", "report", "benchmark"]):
        score += 3
        reasons.append("+3: Journalist explicitly requested statistics, research, or numerical trends")

    # Heuristic 3: Deadline buffer
    if deadline_hours >= 24:
        score += 1
        reasons.append("+1: Ample deadline (>=24h) allows building a high-authority asset")
    elif deadline_hours < 12:
        score -= 3
        reasons.append("-3: Tight deadline (<12h) requires immediate direct pitch")

    # Heuristic 4: Personal anecdote / founder story only
    if is_personal_anecdote or any(term in ask for term in ["personal story", "how you started", "founder journey"]):
        score -= 3
        reasons.append("-3: Pure narrative or founder story; data asset not required")

    if is_paid_placement:
        score -= 2
        reasons.append("-2: Paid / sponsored opportunity")

    recommendation = "BUILD_STATS_PAGE" if score >= 2 else "PITCH_DIRECTLY"

    return {
        "score": score,
        "recommendation": recommendation,
        "reasons": reasons,
        "rationale": "High-leverage linkable asset recommended. Pitching with a comprehensive statistics hub will yield recurring citations for months." if score >= 2 else "Direct expert soundbite recommended to capture immediate quote."
    }

def format_pitch(framework, expert_name, expert_title, company_name, hook_content, asset_url=None):
    """
    Generates a journalist-ready pitch based on 4 proven frameworks.
    """
    greetings = f"Hi,\n\nI saw your query regarding this topic and wanted to share a concise, data-backed perspective from our work at {company_name}."

    if framework == "data_anchor":
        pitch_body = f"""{greetings}

Here are the key findings and benchmarks from our recent industry research:
- {hook_content}

We compiled the full breakdown of verified benchmarks and primary data here for reference: {asset_url if asset_url else '[LINKABLE_ASSET_URL]'}

Happy to provide additional commentary or unpack any specific metric if helpful for your story!

Best regards,
{expert_name}
{expert_title} | {company_name}
"""
    elif framework == "contrarian_hook":
        pitch_body = f"""{greetings}

While most discussions around this focus on conventional wisdom, our data shows the opposite reality:
- {hook_content}

The primary reason this happens is that teams conflate vanity metrics with downstream pipeline velocity.

Happy to provide the background data and attribution details if you'd like to quote this in your piece.

Best regards,
{expert_name}
{expert_title} | {company_name}
"""
    elif framework == "case_study_metric":
        pitch_body = f"""{greetings}

We recently tracked this exact scenario across our customer cohort. Here is what the numbers showed:
- {hook_content}

The single biggest lever that moved the needle was focusing on high-intent workflows rather than raw top-of-funnel traffic.

Feel free to use this quote and data point directly in your article!

Best regards,
{expert_name}
{expert_title} | {company_name}
"""
    else: # executive_soundbite
        pitch_body = f"""{greetings}

Here is a quick, quote-ready soundbite you can drop straight into your article:

"{hook_content}"

If you need any follow-up clarification, headshot, or LinkedIn/company attribution, feel free to reply directly.

Best regards,
{expert_name}
{expert_title} | {company_name}
"""
    return pitch_body.strip()

def record_sent_pitch(opportunity_id, publication, journalist, expert_name, pitch_text):
    os.makedirs(os.path.dirname(SENT_LOG_PATH), exist_ok=True)
    history = []
    if os.path.exists(SENT_LOG_PATH):
        try:
            with open(SENT_LOG_PATH, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []

    # Check duplicate
    for p in history:
        if p.get("opportunity_id") == opportunity_id:
            return {"status": "blocked", "message": f"Duplicate pitch detected! Opportunity '{opportunity_id}' was already pitched on {p.get('sent_at')}."}

    entry = {
        "opportunity_id": opportunity_id,
        "publication": publication,
        "journalist": journalist,
        "expert_name": expert_name,
        "pitch_preview": pitch_text[:120] + "...",
        "sent_at": datetime.now().isoformat()
    }
    history.append(entry)

    with open(SENT_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2)

    return {"status": "recorded", "entry": entry}

def main():
    parser = argparse.ArgumentParser(description="Digital PR Opportunity Evaluator & Pitch Generator")
    parser.add_argument("--topic", default="B2B SaaS AI Automation", help="Opportunity topic")
    parser.add_argument("--ask", default="Looking for recent statistics and data on AI adoption in marketing", help="The journalist request prompt")
    parser.add_argument("--deadline", type=float, default=48, help="Hours until deadline")
    parser.add_argument("--expert", default="Alex Rivera", help="Expert persona name")
    parser.add_argument("--title", default="VP of Growth", help="Expert persona title")
    parser.add_argument("--company", default="ApexEngine", help="Company name")
    parser.add_argument("--framework", choices=["data_anchor", "contrarian_hook", "case_study_metric", "executive_soundbite"], default="data_anchor")
    parser.add_argument("--hook", default="Over 68% of marketing teams reported a 2.4x increase in workflow throughput after automating first-touch research in 2026.", help="The core data hook or quote")
    parser.add_argument("--asset-url", default="https://apexengine.io/research/ai-marketing-statistics-2026", help="Linkable statistics asset URL")
    parser.add_argument("--log-send", action="store_true", help="Record to sent_pitches.json")
    parser.add_argument("--opp-id", default="opp_sample_101", help="Opportunity ID")
    args = parser.parse_args()

    # Step 1: Score Opportunity
    eval_res = score_pr_opportunity({
        "topic": args.topic,
        "ask": args.ask,
        "deadline_hours": args.deadline
    })

    print("\n" + "="*65)
    print("         APEXLINK DIGITAL PR OPPORTUNITY EVALUATION")
    print("="*65)
    print(f"Topic:          {args.topic}")
    print(f"Journalist Ask: {args.ask}")
    print(f"Deadline:       {args.deadline} hours")
    print(f"Stage-3 Score:  {eval_res['score']} -> {eval_res['recommendation']}")
    print(f"Strategy:       {eval_res['rationale']}")
    print("\n[ Scoring Factors ]")
    for r in eval_res["reasons"]:
        print(f"  * {r}")

    # Step 2: Generate Pitch
    pitch = format_pitch(args.framework, args.expert, args.title, args.company, args.hook, args.asset_url)
    print("\n" + "-"*65)
    print(f"  GENERATED PITCH ({args.framework.upper()})")
    print("-" * 65)
    print(pitch)
    print("="*65 + "\n")

    if args.log_send:
        res = record_sent_pitch(args.opp_id, "Tech Publication", "Journalist", args.expert, pitch)
        print(f"[STATUS] {res['status']}: {res.get('message', 'Pitch recorded successfully.')}\n")

if __name__ == "__main__":
    main()
