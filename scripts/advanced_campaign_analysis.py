import os
import pandas as pd
import numpy as np

def analyze_daily_patterns():
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
    csv_files = [f for f in os.listdir(reports_dir) if f.startswith('KPI_Analysis_') and f.endswith('.csv')]
    
    report_lines = [
        "# Campaign-wise Deep Dive & Recommendations",
        "Based on the daily data patterns, here is a detailed analysis of each campaign, focusing on budget pacing, zero-lead days, and ideal daily budgets.",
        ""
    ]
    
    for file in csv_files:
        campaign_name = file.replace('KPI_Analysis_', '').replace('.csv', '')
        df = pd.read_csv(os.path.join(reports_dir, file))
        
        if len(df) == 0:
            continue
            
        # Convert date to datetime if possible
        try:
            df['Date'] = pd.to_datetime(df['Date'])
            df = df.sort_values('Date')
        except:
            pass # Keep as is if parsing fails
            
        total_leads = df['Leads'].sum()
        total_cost = df['Cost'].sum()
        total_clicks = df['Clicks'].sum()
        total_days = len(df)
        
        if total_days == 0 or total_cost == 0:
            continue
            
        avg_cpa = total_cost / total_leads if total_leads > 0 else 0
        avg_cpc = total_cost / total_clicks if total_clicks > 0 else 0
        avg_daily_spend = total_cost / total_days
        conv_rate = (total_leads / total_clicks) if total_clicks > 0 else 0
        
        # Zero lead days analysis
        zero_lead_days = df[df['Leads'] == 0]
        lead_days = df[df['Leads'] > 0]
        
        avg_spend_zero = zero_lead_days['Cost'].mean() if len(zero_lead_days) > 0 else 0
        avg_spend_lead = lead_days['Cost'].mean() if len(lead_days) > 0 else 0
        
        # Pacing analysis (first 20 days vs remaining days)
        # Assuming typical month length, we just split the data 70/30
        split_idx = int(total_days * 0.7)
        early_spend = df.iloc[:split_idx]['Cost'].mean() if split_idx > 0 else 0
        late_spend = df.iloc[split_idx:]['Cost'].mean() if (total_days - split_idx) > 0 else 0
        
        # Recommendations
        ideal_budget = avg_cpa * 1.5 if avg_cpa > 0 else avg_daily_spend * 2
        clicks_needed_per_lead = (1 / conv_rate) if conv_rate > 0 else 0
        
        pacing_issue = late_spend < (early_spend * 0.8) # Spend dropped by 20% or more at end of period
        
        report_lines.append(f"## {campaign_name}")
        report_lines.append(f"**Performance Baseline:**")
        report_lines.append(f"- **Avg CPA (Cost per Lead):** ₹{avg_cpa:.2f}")
        report_lines.append(f"- **Avg Daily Spend:** ₹{avg_daily_spend:.2f}")
        report_lines.append(f"- **Avg Clicks needed per Lead:** {clicks_needed_per_lead:.1f} clicks")
        report_lines.append("")
        
        report_lines.append(f"**Daily Volatility & 0-Lead Days:**")
        report_lines.append(f"- Out of {total_days} days, **{len(zero_lead_days)} days** had 0 leads ({(len(zero_lead_days)/total_days)*100:.1f}%).")
        if len(zero_lead_days) > 0:
            report_lines.append(f"- Avg spend on 0-lead days: ₹{avg_spend_zero:.2f} | Avg spend on >0-lead days: ₹{avg_spend_lead:.2f}")
            if avg_spend_zero < (avg_cpa * 0.8):
                report_lines.append("  - *Insight:* The spend on 0-lead days is lower than your average CPA. The budget on these days isn't high enough to competitively win the clicks needed for a conversion.")
            else:
                report_lines.append("  - *Insight:* Spend is happening, but conversion rate is dropping on these days. This suggests search intent volatility or ad rank fluctuations during certain days of the week.")
        report_lines.append("")
        
        report_lines.append(f"**Budget Pacing (Early vs. Late Period):**")
        report_lines.append(f"- Early period avg spend: ₹{early_spend:.2f}/day | Late period avg spend: ₹{late_spend:.2f}/day")
        if pacing_issue:
            report_lines.append("- ⚠️ *Alert:* Spend throttles significantly towards the end of the period. Google is heavily restricting delivery to avoid exceeding the monthly budget.")
        else:
            report_lines.append("- *Good:* Spend pacing looks relatively stable across the period.")
        report_lines.append("")
        
        report_lines.append(f"**💡 Recommendations:**")
        report_lines.append(f"1. **Ideal Daily Budget:** Set the daily budget to at least **₹{ideal_budget:.2f}**. This is ~1.5x your CPA, ensuring Google has enough room to optimize and capture at least 1 lead every day without capping out mid-day.")
        report_lines.append(f"2. **To Fix 0-Lead Days:** We need to guarantee roughly **{clicks_needed_per_lead:.0f} clicks per day** to get 1 lead. At ₹{avg_cpc:.2f}/click, that requires ₹{(clicks_needed_per_lead * avg_cpc):.2f}/day minimum.")
        
        if pacing_issue:
            report_lines.append(f"3. **Pacing Solution:** Since the campaign hits budget limits late in the month, either increase the monthly total or use a *Shared Budget* across similar cities to balance under-spending days in one city with over-spending in another.")
        report_lines.append("---")
        report_lines.append("")

    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports', 'Detailed_Campaign_Insights.md')
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
        
    print(f"Analysis generated at {output_path}")

if __name__ == '__main__':
    analyze_daily_patterns()
