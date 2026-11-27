import re

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pet Mode — Performance Forecast & Weekly Analysis Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root {
            --bg-primary: #0F172A;
            --bg-card: #1E293B;
            --bg-card-hover: #334155;
            --text-primary: #F8FAFC;
            --text-secondary: #94A3B8;
            --accent-blue: #3B82F6;
            --accent-emerald: #10B981;
            --accent-amber: #F59E0B;
            --accent-rose: #F43F5E;
            --border-color: #334155;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; }
        body { background-color: var(--bg-primary); color: var(--text-primary); padding: 24px; line-height: 1.5; }
        .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color); padding-bottom: 20px; margin-bottom: 24px; }
        .header h1 { font-size: 24px; font-weight: 700; color: #FFFFFF; display: flex; align-items: center; gap: 10px; }
        .header h1 span { background: var(--accent-blue); font-size: 12px; padding: 4px 10px; border-radius: 9999px; text-transform: uppercase; letter-spacing: 0.05em; }
        .header p { color: var(--text-secondary); font-size: 14px; margin-top: 4px; }
        .badge-date { background: #1E293B; border: 1px solid var(--border-color); padding: 6px 14px; border-radius: 8px; font-size: 13px; color: var(--text-secondary); }
        
        .scenario-nav { display: flex; gap: 12px; margin-bottom: 24px; background: #1E293B; padding: 6px; border-radius: 12px; border: 1px solid var(--border-color); width: fit-content; }
        .scenario-btn { background: transparent; border: none; color: var(--text-secondary); padding: 10px 20px; border-radius: 8px; font-size: 14px; font-weight: 600; cursor: pointer; transition: all 0.2s ease; }
        .scenario-btn:hover { color: #FFFFFF; background: rgba(255,255,255,0.05); }
        .scenario-btn.active { background: var(--accent-blue); color: #FFFFFF; box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3); }
        
        .metrics-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; margin-bottom: 24px; }
        .card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 14px; padding: 20px; transition: transform 0.2s ease, border-color 0.2s ease; }
        .card:hover { border-color: #475569; transform: translateY(-2px); }
        .card-label { font-size: 12px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-secondary); margin-bottom: 8px; }
        .card-value { font-size: 28px; font-weight: 700; color: #FFFFFF; }
        .card-subtext { font-size: 13px; margin-top: 6px; display: flex; align-items: center; gap: 6px; }
        .text-emerald { color: var(--accent-emerald); }
        .text-amber { color: var(--accent-amber); }
        .text-blue { color: var(--accent-blue); }
        .text-rose { color: var(--accent-rose); }
        
        .charts-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(480px, 1fr)); gap: 20px; margin-bottom: 24px; }
        .chart-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 14px; padding: 20px; }
        .chart-header { font-size: 16px; font-weight: 600; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; }
        
        .table-card { background: var(--bg-card); border: 1px solid var(--border-color); border-radius: 14px; padding: 20px; margin-bottom: 24px; overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; text-align: left; font-size: 13px; }
        th { background: #0F172A; color: var(--text-secondary); padding: 12px 14px; font-weight: 600; text-transform: uppercase; font-size: 11px; letter-spacing: 0.05em; border-bottom: 1px solid var(--border-color); }
        td { padding: 12px 14px; border-bottom: 1px solid #283548; color: #E2E8F0; }
        tr:hover td { background: var(--bg-card-hover); }
        .bold { font-weight: 600; color: #FFFFFF; }
        .pill { padding: 3px 8px; border-radius: 6px; font-size: 11px; font-weight: 600; display: inline-block; }
        .pill-blue { background: rgba(59, 130, 246, 0.15); color: #60A5FA; border: 1px solid rgba(59, 130, 246, 0.3); }
        .pill-amber { background: rgba(245, 158, 11, 0.15); color: #FBBF24; border: 1px solid rgba(245, 158, 11, 0.3); }
        .pill-emerald { background: rgba(16, 185, 129, 0.15); color: #34D399; border: 1px solid rgba(16, 185, 129, 0.3); }
        
        .callout { background: rgba(59, 130, 246, 0.1); border-left: 4px solid var(--accent-blue); padding: 14px 18px; border-radius: 8px; margin-bottom: 24px; font-size: 13.5px; }
        .callout-title { font-weight: 700; color: #FFFFFF; margin-bottom: 4px; display: flex; align-items: center; gap: 6px; }
        
        .footer { text-align: center; color: var(--text-secondary); font-size: 12px; margin-top: 40px; padding-top: 20px; border-top: 1px solid var(--border-color); }
    </style>
</head>
<body>
    <div class="header">
        <div>
            <h1>Pet Mode <span>Forecast & Weekly Analytics</span></h1>
            <p>Evaluating Forecast - A (User Draft) vs. Forecast - B (Realistic Best) with Weekly Ad Metrics</p>
        </div>
        <div class="badge-date">
            Data Current as of Sep 25, 2026 | GBP (£)
        </div>
    </div>

    <div class="callout">
        <div class="callout-title">⚡ Weekly Performance Insight (Sep 18 – Sep 24, 2026)</div>
        In the most recent week, Pet Mode achieved a breakthrough week: <b>12 total orders</b> (Meta: 9 orders at <b>£19.93 CPA</b>, Google: 3 orders at <b>£23.68 CPA</b>). The core sales campaign on Meta (<code>[TE]Sales 8.5.26</code>) delivered 5 orders at <b>£16.23 CPA and 1.62x ROAS</b>, while the newly launched Bundle campaign delivered 4 orders at <b>£24.55 CPA</b>. Both channels are already inside the target KPI ranges!
    </div>

    <div class="scenario-nav">
        <button class="scenario-btn active" onclick="switchScenario('forecastB')">Forecast - B (Realistic Best)</button>
        <button class="scenario-btn" onclick="switchScenario('forecastA')">Forecast - A (User Draft)</button>
        <button class="scenario-btn" onclick="switchScenario('weekly')">Recent Weekly Actuals</button>
    </div>

    <div class="metrics-grid">
        <div class="card">
            <div class="card-label">3-Month Total Revenue</div>
            <div class="card-value" id="card-revenue">£6,320</div>
            <div class="card-subtext text-emerald" id="card-sub-revenue">Profitable Q4 Growth</div>
        </div>
        <div class="card">
            <div class="card-label">3-Month Total Ad Spend</div>
            <div class="card-value" id="card-spend">£3,800</div>
            <div class="card-subtext text-blue" id="card-sub-spend">Identical spend in A & B</div>
        </div>
        <div class="card">
            <div class="card-label">Total Projected Orders</div>
            <div class="card-value" id="card-orders">225 Orders</div>
            <div class="card-subtext text-emerald" id="card-sub-orders">187 Paid + 38 Organic</div>
        </div>
        <div class="card">
            <div class="card-label">Blended CPA</div>
            <div class="card-value" id="card-cpa">£16.88</div>
            <div class="card-subtext text-emerald" id="card-sub-cpa">Below £20 target in all months</div>
        </div>
        <div class="card">
            <div class="card-label">Blended ROAS</div>
            <div class="card-value" id="card-roas">1.66x</div>
            <div class="card-subtext text-emerald" id="card-sub-roas">High Front-End Profitability</div>
        </div>
    </div>

    <div class="charts-grid">
        <div class="chart-card">
            <div class="chart-header">
                <span>Monthly Revenue: Forecast - A vs Forecast - B</span>
                <span class="pill pill-blue">Q4 Comparison</span>
            </div>
            <canvas id="revChart" height="260"></canvas>
        </div>
        <div class="chart-card">
            <div class="chart-header">
                <span>Blended CPA Comparison</span>
                <span class="pill pill-emerald">Unit Economics</span>
            </div>
            <canvas id="cpaChart" height="260"></canvas>
        </div>
    </div>

    <div class="table-card">
        <div class="chart-header">
            <span id="table-title">Shopify Storefront Forecast — Forecast - B (Realistic Best)</span>
            <span class="pill pill-emerald" id="table-pill">Active View</span>
        </div>
        <table>
            <thead>
                <tr id="table-head">
                    <th>Month</th>
                    <th>Spend (£)</th>
                    <th>Paid Order</th>
                    <th>Other order</th>
                    <th>Total Orders</th>
                    <th>Paid CPA (£)</th>
                    <th>Blended CPA (£)</th>
                    <th>Total Revenue (£)</th>
                    <th>AOV (£)</th>
                    <th>ROAS</th>
                </tr>
            </thead>
            <tbody id="table-body">
                <!-- Dynamically populated -->
            </tbody>
        </table>
    </div>

    <div class="footer">
        Pet Mode Performance Marketing & E-Commerce Forecasting • Confidential & Proprietary • Powered by Office
    </div>

    <script>
        const appData = {
            forecastB: {
                title: "Shopify Storefront Forecast — Forecast - B (Realistic Best)",
                pill: "Realistic Best",
                revenue: "£6,320",
                spend: "£3,800",
                orders: "225 Orders",
                cpa: "£16.88",
                roas: "1.66x",
                subRevenue: "Profitable Q4 Growth",
                subSpend: "Identical spend in A & B (£3,800)",
                subOrders: "187.1 Paid + 38.0 Organic",
                subCpa: "Below £20 target in every month",
                subRoas: "Sustainable, grounded assumptions",
                rows: [
                    { month: "October 2026", spend: "£1,100.00", paid_ord: "47.4", other_ord: "10.0", tot_ord: "57.4", paid_cpa: "£23.19", blended_cpa: "£19.15", rev: "£1,493.14", aov: "£26.00", roas: "1.36x" },
                    { month: "November 2026 (BFCM)", spend: "£1,300.00", paid_ord: "66.4", other_ord: "14.0", tot_ord: "80.4", paid_cpa: "£19.57", blended_cpa: "£16.16", rev: "£2,252.10", aov: "£28.00", roas: "1.73x" },
                    { month: "December 2026", spend: "£1,400.00", paid_ord: "73.3", other_ord: "14.0", tot_ord: "87.3", paid_cpa: "£19.11", blended_cpa: "£16.04", rev: "£2,574.56", aov: "£29.50", roas: "1.84x" },
                    { month: "3-Month Total / Avg", spend: "£3,800.00", paid_ord: "187.1", other_ord: "38.0", tot_ord: "225.1", paid_cpa: "£20.31", blended_cpa: "£16.88", rev: "£6,319.80", aov: "£28.07", roas: "1.66x" }
                ]
            },
            forecastA: {
                title: "Shopify Storefront Forecast — Forecast - A (User Draft)",
                pill: "User Draft",
                revenue: "£6,718",
                spend: "£3,800",
                orders: "235 Orders",
                cpa: "£16.16",
                roas: "1.77x",
                subRevenue: "Heavy December Skew",
                subSpend: "Spend: £3,800",
                subOrders: "198.1 Paid + 37.0 Other",
                subCpa: "Drops to £12.17 in Dec",
                subRoas: "Dec ROAS 2.46x (Aggressive)",
                rows: [
                    { month: "October 2026", spend: "£1,100.00", paid_ord: "37.3", other_ord: "10.0", tot_ord: "47.3", paid_cpa: "£29.46", blended_cpa: "£23.24", rev: "£1,230.67", aov: "£26.00", roas: "1.12x" },
                    { month: "November 2026", spend: "£1,300.00", paid_ord: "60.8", other_ord: "12.0", tot_ord: "72.8", paid_cpa: "£21.39", blended_cpa: "£17.86", rev: "£2,037.54", aov: "£28.00", roas: "1.57x" },
                    { month: "December 2026", spend: "£1,400.00", paid_ord: "100.0", other_ord: "15.0", tot_ord: "115.0", paid_cpa: "£14.00", blended_cpa: "£12.17", rev: "£3,450.00", aov: "£30.00", roas: "2.46x" },
                    { month: "3-Month Total / Avg", spend: "£3,800.00", paid_ord: "198.1", other_ord: "37.0", tot_ord: "235.1", paid_cpa: "£19.18", blended_cpa: "£16.16", rev: "£6,718.21", aov: "£28.58", roas: "1.77x" }
                ]
            },
            weekly: {
                title: "Recent Weekly Actual Performance (August – September 2026)",
                pill: "Actuals",
                revenue: "£1,349",
                spend: "£1,440",
                orders: "58 Orders",
                cpa: "£24.83",
                roas: "0.94x",
                subRevenue: "Last 6 Weeks Tracked",
                subSpend: "Spend ~£240/week",
                subOrders: "Sep 18-24 hit 12 orders",
                subCpa: "Sep 18-24 Meta CPA £19.93",
                subRoas: "Sep 18-24 ROAS > 1.25x",
                rows: [
                    { month: "Aug 14 - Aug 20", spend: "£212.26", paid_ord: "9.0", other_ord: "2.0", tot_ord: "11.0", paid_cpa: "£23.58", blended_cpa: "£19.30", rev: "£299.71", aov: "£22.34", roas: "1.41x" },
                    { month: "Aug 21 - Aug 27", spend: "£263.16", paid_ord: "5.0", other_ord: "2.0", tot_ord: "7.0", paid_cpa: "£52.63", blended_cpa: "£37.59", rev: "£196.15", aov: "£23.74", roas: "0.75x" },
                    { month: "Aug 28 - Sep 3", spend: "£237.31", paid_ord: "9.0", other_ord: "1.0", tot_ord: "10.0", paid_cpa: "£26.37", blended_cpa: "£23.73", rev: "£327.33", aov: "£29.13", roas: "1.38x" },
                    { month: "Sep 4 - Sep 10", spend: "£249.27", paid_ord: "7.0", other_ord: "4.0", tot_ord: "11.0", paid_cpa: "£35.61", blended_cpa: "£22.66", rev: "£275.72", aov: "£26.64", roas: "1.11x" },
                    { month: "Sep 11 - Sep 17", spend: "£251.48", paid_ord: "7.0", other_ord: "0.0", tot_ord: "7.0", paid_cpa: "£35.93", blended_cpa: "£35.93", rev: "£181.93", aov: "£18.77", roas: "0.72x" },
                    { month: "Sep 18 - Sep 24 (Breakthrough)", spend: "£250.38", paid_ord: "12.0", other_ord: "3.0", tot_ord: "15.0", paid_cpa: "£20.87", blended_cpa: "£16.69", rev: "£404.12", aov: "£26.94", roas: "1.61x" }
                ]
            }
        };

        let revChart, cpaChart;

        function initCharts() {
            const ctx1 = document.getElementById('revChart').getContext('2d');
            revChart = new Chart(ctx1, {
                type: 'bar',
                data: {
                    labels: ["Oct '26", "Nov '26 (BFCM)", "Dec '26"],
                    datasets: [
                        {
                            label: 'Forecast - A (User Draft)',
                            data: [1231, 2038, 3450],
                            backgroundColor: '#94A3B8'
                        },
                        {
                            label: 'Forecast - B (Realistic Best)',
                            data: [1493, 2252, 2575],
                            backgroundColor: '#3B82F6'
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { labels: { color: '#F8FAFC' } } },
                    scales: {
                        y: {
                            grid: { color: '#334155' },
                            ticks: { color: '#94A3B8', callback: v => '£' + v.toLocaleString() }
                        },
                        x: { grid: { color: '#334155' }, ticks: { color: '#94A3B8' } }
                    }
                }
            });

            const ctx2 = document.getElementById('cpaChart').getContext('2d');
            cpaChart = new Chart(ctx2, {
                type: 'line',
                data: {
                    labels: ["Oct '26", "Nov '26 (BFCM)", "Dec '26"],
                    datasets: [
                        {
                            label: 'Forecast - A Blended CPA (£)',
                            data: [23.24, 17.86, 12.17],
                            borderColor: '#F43F5E',
                            borderDash: [4, 4],
                            tension: 0.3,
                            pointRadius: 5
                        },
                        {
                            label: 'Forecast - B Blended CPA (£)',
                            data: [19.15, 16.16, 16.04],
                            borderColor: '#10B981',
                            tension: 0.3,
                            pointRadius: 5
                        }
                    ]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { labels: { color: '#F8FAFC' } } },
                    scales: {
                        y: {
                            grid: { color: '#334155' },
                            ticks: { color: '#94A3B8', callback: v => '£' + v.toFixed(2) }
                        },
                        x: { grid: { color: '#334155' }, ticks: { color: '#94A3B8' } }
                    }
                }
            });
        }

        function switchScenario(key) {
            const data = appData[key];
            document.querySelectorAll('.scenario-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');

            document.getElementById('card-revenue').innerText = data.revenue;
            document.getElementById('card-spend').innerText = data.spend;
            document.getElementById('card-orders').innerText = data.orders;
            document.getElementById('card-cpa').innerText = data.cpa;
            document.getElementById('card-roas').innerText = data.roas;

            document.getElementById('card-sub-revenue').innerText = data.subRevenue;
            document.getElementById('card-sub-spend').innerText = data.subSpend;
            document.getElementById('card-sub-orders').innerText = data.subOrders;
            document.getElementById('card-sub-cpa').innerText = data.subCpa;
            document.getElementById('card-sub-roas').innerText = data.subRoas;

            document.getElementById('table-title').innerText = data.title;
            document.getElementById('table-pill').innerText = data.pill;

            const tbody = document.getElementById('table-body');
            tbody.innerHTML = '';
            data.rows.forEach(r => {
                const isTotal = r.month.includes('Total');
                tbody.innerHTML += `
                    <tr style="${isTotal ? 'background: #283548; font-weight: bold;' : ''}">
                        <td class="${isTotal ? 'bold' : ''}">${r.month}</td>
                        <td>${r.spend}</td>
                        <td>${r.paid_ord}</td>
                        <td>${r.other_ord}</td>
                        <td class="bold">${r.tot_ord}</td>
                        <td>${r.paid_cpa}</td>
                        <td class="bold text-emerald">${r.blended_cpa}</td>
                        <td class="bold text-blue">${r.rev}</td>
                        <td>${r.aov}</td>
                        <td class="bold">${r.roas}</td>
                    </tr>
                `;
            });
        }

        window.onload = function() {
            initCharts();
            switchScenario('forecastB');
        };
    </script>
</body>
</html>
"""

with open("reports/Pet_Mode_Forecast_Dashboard.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Updated reports/Pet_Mode_Forecast_Dashboard.html successfully.")
