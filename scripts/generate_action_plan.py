import os
import pandas as pd

def generate_action_plan():
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
    csv_files = [f for f in os.listdir(reports_dir) if f.startswith('KPI_Analysis_') and f.endswith('.csv')]
    
    report_lines = [
        "# Campaign Action Plan",
        "Based on historical data pacing, below is the immediate action plan to stabilize lead flow, ensure at least 1 lead per day, and fix month-end budget throttling.",
        "",
        "## Budget & Bidding Adjustments",
        "| Campaign | Current Avg Daily Spend (₹) | **Proposed Daily Budget (₹)** | Target CPA Goal (₹) | Rationale |",
        "| :--- | :--- | :--- | :--- | :--- |"
    ]
    
    actions = []
    
    for file in csv_files:
        campaign_name = file.replace('KPI_Analysis_', '').replace('.csv', '')
        
        # Skip new campaign as requested
        if 'New-French-Bangalore' in campaign_name:
            continue
            
        df = pd.read_csv(os.path.join(reports_dir, file))
        if len(df) == 0: continue
            
        total_leads = df['Leads'].sum()
        total_cost = df['Cost'].sum()
        total_clicks = df['Clicks'].sum()
        total_days = len(df)
        
        if total_days == 0 or total_cost == 0: continue
            
        avg_cpa = total_cost / total_leads if total_leads > 0 else 0
        avg_daily_spend = total_cost / total_days
        
        ideal_budget = avg_cpa * 1.5 if avg_cpa > 0 else avg_daily_spend * 2
        
        # Determine pacing issue
        split_idx = int(total_days * 0.7)
        early_spend = df.iloc[:split_idx]['Cost'].mean() if split_idx > 0 else 0
        late_spend = df.iloc[split_idx:]['Cost'].mean() if (total_days - split_idx) > 0 else 0
        pacing_issue = late_spend < (early_spend * 0.8)
        
        zero_lead_days = len(df[df['Leads'] == 0])
        
        rationale = []
        if pacing_issue:
            rationale.append("Fix month-end throttle.")
        if zero_lead_days > 0:
            rationale.append(f"Prevent {zero_lead_days} zero-lead days.")
            
        rationale_str = " ".join(rationale) if rationale else "Maintain stable lead flow."
        
        report_lines.append(f"| **{campaign_name}** | {avg_daily_spend:.2f} | **{ideal_budget:.2f}** | {avg_cpa:.2f} | {rationale_str} |")
        
        actions.append(f"### {campaign_name}")
        actions.append(f"- **Action 1 (Budget):** Increase daily budget from ~₹{avg_daily_spend:.0f} to **₹{ideal_budget:.0f}**. This guarantees you can afford 1.5x your historical CPA (₹{avg_cpa:.0f}) every single day.")
        
        if pacing_issue:
            actions.append("- **Action 2 (Pacing):** Move this campaign to a **Shared Budget** or adjust the monthly limit. Data shows Google aggressively throttles spend in the final week due to hitting caps.")
            
        if zero_lead_days > (total_days * 0.15):
            actions.append("- **Action 3 (Bidding):** Switch to or adjust Target CPA (tCPA). Set the tCPA slightly above ₹{avg_cpa:.0f} initially to let the algorithm breathe, then slowly reduce it once daily leads stabilize.")
        actions.append("")
        
    report_lines.append("")
    report_lines.append("## Campaign-Specific Execution Steps")
    report_lines.extend(actions)
    
    report_lines.extend([
        "---",
        "> [!IMPORTANT]",
        "> **Next Steps for Implementation:**",
        "> 1. Log into Google Ads.",
        "> 2. Apply the **Proposed Daily Budgets** to the campaigns immediately to stop the zero-lead days.",
        "> 3. Monitor for 7 days. Once daily leads hit >=1 consistently, we can begin lowering the Target CPA goals by 5% week-over-week."
    ])

    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports', 'Campaign_Action_Plan.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
        
    print(f"Action plan generated at {output_path}")

if __name__ == '__main__':
    generate_action_plan()
