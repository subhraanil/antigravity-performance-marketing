import os

out_dir = 'reports'
os.makedirs(out_dir, exist_ok=True)

# 1. PLAN A HTML DASHBOARD (fabb6_plan_a_dashboard.html)
plan_a_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fabb6 — Plan A Growth Dashboard (Volume Target)</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root { --bg-main: #f8fafc; --card-bg: #ffffff; --border-color: #e2e8f0; --primary-blue: #2563eb; }
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: var(--bg-main); color: #0f172a; padding-bottom: 40px; }
        .navbar-custom { background: #ffffff; border-bottom: 1px solid var(--border-color); padding: 15px 0; }
        .kpi-card { background: #ffffff; border: 1px solid var(--border-color); border-radius: 14px; padding: 20px; }
        .table-custom { color: #0f172a; vertical-align: middle; }
        .table-custom th { background: #f8fafc; color: #1e293b; font-size: 0.75rem; text-transform: uppercase; }
        .pct-pill { background: #f1f5f9; color: #1e293b; font-weight: 700; font-size: 0.75rem; padding: 2px 6px; border-radius: 4px; }
    </style>
</head>
<body>
    <nav class="navbar-custom sticky-top mb-4">
        <div class="container-fluid px-4 d-flex justify-content-between align-items-center">
            <div class="fw-bold fs-5 text-primary"><i class="fa-solid fa-bullseye me-2"></i>FABB6 — PLAN A DASHBOARD <span class="text-dark fs-6">(Aggressive Volume Target: 1,500 Orders/Day)</span></div>
            <a href="fabb6_side_by_side_comparison.html" class="btn btn-sm btn-outline-primary fw-bold"><i class="fa-solid fa-columns me-1"></i> View Side-by-Side Comparison</a>
        </div>
    </nav>

    <div class="container-fluid px-4">
        <!-- KPIs -->
        <div class="row g-3 mb-4">
            <div class="col-md-3"><div class="kpi-card"><div class="text-muted fw-bold text-xs uppercase">6-Month Total Sales</div><div class="fs-3 fw-bold text-dark">₹18.55 Cr</div><div class="text-success text-xs fw-bold">Target Scaling</div></div></div>
            <div class="col-md-3"><div class="kpi-card"><div class="text-muted fw-bold text-xs uppercase">Total Orders</div><div class="fs-3 fw-bold text-primary">2,01,750</div><div class="text-primary text-xs fw-bold">1,500 orders/day target</div></div></div>
            <div class="col-md-3"><div class="kpi-card"><div class="text-muted fw-bold text-xs uppercase">6-Month Paid Spend</div><div class="fs-3 fw-bold text-warning">₹4.88 Cr</div><div class="text-muted text-xs fw-bold">Google + Meta</div></div></div>
            <div class="col-md-3"><div class="kpi-card"><div class="text-muted fw-bold text-xs uppercase">Blended ROAS</div><div class="fs-3 fw-bold text-purple" style="color:#7c3aed;">3.80x</div><div class="text-purple text-xs fw-bold" style="color:#7c3aed;">Multi-channel average</div></div></div>
        </div>

        <!-- Table -->
        <div class="card border-0 shadow-sm rounded-4 p-4 mb-4">
            <h5 class="fw-bold mb-3"><i class="fa-solid fa-table text-primary me-2"></i>Plan A — Complete 6-Month Channel Forecast</h5>
            <div class="table-responsive">
                <table class="table table-custom border">
                    <thead>
                        <tr>
                            <th>Month</th>
                            <th>Total Spend</th>
                            <th>Paid Sales Only (% Share)</th>
                            <th>Google Ads Sales (% Share)</th>
                            <th>Meta Ads Sales (% Share)</th>
                            <th>Organic Sales</th>
                            <th>Return Customer Sales</th>
                            <th>Total Monthly Sales</th>
                            <th>Total Orders</th>
                            <th>Daily Avg</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>Sept 2026</td><td>₹54.00 L</td><td class="fw-bold text-primary">₹1.220 Cr <span class="pct-pill">63.4%</span></td><td>₹62.00 L <span class="pct-pill">32.2%</span></td><td>₹60.00 L <span class="pct-pill">31.2%</span></td><td>₹32.30 L</td><td>₹38.00 L</td><td class="fw-bold">₹1.923 Cr</td><td>21,450</td><td>715 / day</td></tr>
                        <tr><td>Oct 2026</td><td>₹64.00 L</td><td class="fw-bold text-primary">₹1.470 Cr <span class="pct-pill">63.8%</span></td><td>₹76.00 L <span class="pct-pill">33.0%</span></td><td>₹71.00 L <span class="pct-pill">30.8%</span></td><td>₹36.10 L</td><td>₹47.50 L</td><td class="fw-bold">₹2.306 Cr</td><td>25,400</td><td>820 / day</td></tr>
                        <tr><td>Nov 2026</td><td>₹77.00 L</td><td class="fw-bold text-primary">₹1.780 Cr <span class="pct-pill">62.8%</span></td><td>₹92.00 L <span class="pct-pill">32.5%</span></td><td>₹86.00 L <span class="pct-pill">30.3%</span></td><td>₹44.50 L</td><td>₹61.00 L</td><td class="fw-bold">₹2.835 Cr</td><td>31,000</td><td>1,033 / day</td></tr>
                        <tr><td>Dec 2026</td><td>₹90.00 L</td><td class="fw-bold text-primary">₹2.090 Cr <span class="pct-pill">60.5%</span></td><td>₹108.00 L <span class="pct-pill">31.2%</span></td><td>₹101.00 L <span class="pct-pill">29.2%</span></td><td>₹57.60 L</td><td>₹79.00 L</td><td class="fw-bold">₹3.456 Cr</td><td>37,500</td><td>1,210 / day</td></tr>
                        <tr><td>Jan 2027</td><td>₹98.00 L</td><td class="fw-bold text-primary">₹2.290 Cr <span class="pct-pill">59.9%</span></td><td>₹118.00 L <span class="pct-pill">30.8%</span></td><td>₹111.00 L <span class="pct-pill">29.0%</span></td><td>₹60.60 L</td><td>₹93.00 L</td><td class="fw-bold">₹3.826 Cr</td><td>41,400</td><td>1,335 / day</td></tr>
                        <tr class="table-primary bg-opacity-10"><td><strong>Feb 2027</strong></td><td><strong>₹1.050 Cr</strong></td><td class="fw-bold text-primary">₹2.480 Cr <span class="pct-pill">59.0%</span></td><td><strong>₹128.00 L</strong> <span class="pct-pill">30.5%</span></td><td><strong>₹120.00 L</strong> <span class="pct-pill">28.6%</span></td><td><strong>₹65.90 L</strong></td><td><strong>₹106.10 L</strong></td><td class="fw-bold text-success fs-6">₹4.200 Cr</td><td class="fw-bold text-success">45,000</td><td class="fw-bold text-success">1,500 / day</td></tr>
                    </tbody>
                    <tfoot><tr class="table-secondary fw-bold"><td>CUMULATIVE</td><td>₹4.880 Cr</td><td>₹11.333 Cr <span class="pct-pill">61.1%</span></td><td>₹5.843 Cr</td><td>₹5.490 Cr</td><td>₹2.970 Cr</td><td>₹4.246 Cr</td><td class="text-success">₹18.546 Cr</td><td>2,01,750</td><td>1,102 avg</td></tr></tfoot>
                </table>
            </div>
        </div>
    </div>
</body>
</html>"""

with open(r'reports/fabb6_plan_a_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(plan_a_html)

# 2. PLAN B HTML DASHBOARD (fabb6_plan_b_dashboard.html)
plan_b_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fabb6 — Plan B Growth Dashboard (CPA Efficiency)</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root { --bg-main: #f0fdf4; --card-bg: #ffffff; --border-color: #bbf7d0; --accent-green: #16a34a; }
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8fafc; color: #0f172a; padding-bottom: 40px; }
        .navbar-custom { background: #ffffff; border-bottom: 1px solid #bbf7d0; padding: 15px 0; }
        .kpi-card { background: #ffffff; border: 1px solid #bbf7d0; border-radius: 14px; padding: 20px; }
        .table-custom { color: #0f172a; vertical-align: middle; }
        .table-custom th { background: #f0fdf4; color: #166534; font-size: 0.75rem; text-transform: uppercase; }
        .pct-pill { background: #dcfce7; color: #166534; font-weight: 700; font-size: 0.75rem; padding: 2px 6px; border-radius: 4px; }
    </style>
</head>
<body>
    <nav class="navbar-custom sticky-top mb-4">
        <div class="container-fluid px-4 d-flex justify-content-between align-items-center">
            <div class="fw-bold fs-5 text-success"><i class="fa-solid fa-chart-line me-2"></i>FABB6 — PLAN B DASHBOARD <span class="text-dark fs-6">(CPA Reduction & Remarketing Model)</span></div>
            <a href="fabb6_side_by_side_comparison.html" class="btn btn-sm btn-outline-success fw-bold"><i class="fa-solid fa-columns me-1"></i> View Side-by-Side Comparison</a>
        </div>
    </nav>

    <div class="container-fluid px-4">
        <!-- KPIs -->
        <div class="row g-3 mb-4">
            <div class="col-md-3"><div class="kpi-card"><div class="text-muted fw-bold text-xs uppercase">6-Month Total Sales</div><div class="fs-3 fw-bold text-success">₹18.49 Cr</div><div class="text-success text-xs fw-bold">High Profitability</div></div></div>
            <div class="col-md-3"><div class="kpi-card"><div class="text-muted fw-bold text-xs uppercase">Blended Paid CPA Reduction</div><div class="fs-3 fw-bold text-primary">₹308 ➔ ₹260</div><div class="text-primary text-xs fw-bold">15.5% CPA Improvement</div></div></div>
            <div class="col-md-3"><div class="kpi-card"><div class="text-muted fw-bold text-xs uppercase">6-Month Paid Spend</div><div class="fs-3 fw-bold text-dark">₹3.82 Cr</div><div class="text-success text-xs fw-bold">Saves ₹1.06 Cr Ad Spend</div></div></div>
            <div class="col-md-3"><div class="kpi-card"><div class="text-muted fw-bold text-xs uppercase">Blended ROAS</div><div class="fs-3 fw-bold text-purple" style="color:#7c3aed;">4.84x</div><div class="text-purple text-xs fw-bold" style="color:#7c3aed;">vs 3.80x in Plan A</div></div></div>
        </div>

        <!-- Table -->
        <div class="card border-0 shadow-sm rounded-4 p-4 mb-4 border-success">
            <h5 class="fw-bold mb-3 text-success"><i class="fa-solid fa-table me-2"></i>Plan B — Complete 6-Month Channel Forecast (CPA Efficiency Model)</h5>
            <div class="table-responsive">
                <table class="table table-custom border">
                    <thead>
                        <tr>
                            <th>Month</th>
                            <th>Total Spend</th>
                            <th>Paid Sales Only (% Share)</th>
                            <th>Google Ads Sales (% Share)</th>
                            <th>Meta Ads Sales (% Share)</th>
                            <th>Organic Sales</th>
                            <th>Return Customer Sales</th>
                            <th>Total Monthly Sales</th>
                            <th>Blended CPA</th>
                            <th>Overall ROAS</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td>Sept 2026</td><td>₹45.00 L</td><td class="fw-bold text-primary">₹1.325 Cr <span class="pct-pill">77.2%</span></td><td>₹63.92 L <span class="pct-pill">37.2%</span></td><td>₹68.60 L <span class="pct-pill">39.9%</span></td><td>₹22.50 L</td><td>₹16.72 L</td><td class="fw-bold">₹1.717 Cr</td><td class="fw-bold text-danger">₹308.22</td><td class="fw-bold text-success">3.82x</td></tr>
                        <tr><td>Oct 2026</td><td>₹52.00 L</td><td class="fw-bold text-primary">₹1.658 Cr <span class="pct-pill">73.4%</span></td><td>₹74.10 L <span class="pct-pill">32.8%</span></td><td>₹91.67 L <span class="pct-pill">40.6%</span></td><td>₹27.00 L</td><td>₹32.98 L</td><td class="fw-bold">₹2.258 Cr</td><td class="fw-bold text-warning">₹287.29</td><td class="fw-bold text-success">4.34x</td></tr>
                        <tr><td>Nov 2026</td><td>₹60.00 L</td><td class="fw-bold text-primary">₹1.999 Cr <span class="pct-pill">71.8%</span></td><td>₹88.32 L <span class="pct-pill">31.7%</span></td><td>₹111.60 L <span class="pct-pill">40.1%</span></td><td>₹34.96 L</td><td>₹43.68 L</td><td class="fw-bold">₹2.786 Cr</td><td class="fw-bold text-success">₹277.78</td><td class="fw-bold text-success">4.64x</td></tr>
                        <tr><td>Dec 2026</td><td>₹68.00 L</td><td class="fw-bold text-primary">₹2.348 Cr <span class="pct-pill">69.9%</span></td><td>₹103.79 L <span class="pct-pill">30.9%</span></td><td>₹131.04 L <span class="pct-pill">39.0%</span></td><td>₹44.64 L</td><td>₹56.42 L</td><td class="fw-bold">₹3.359 Cr</td><td class="fw-bold text-success">₹270.92</td><td class="fw-bold text-success">4.94x</td></tr>
                        <tr><td>Jan 2027</td><td>₹75.00 L</td><td class="fw-bold text-primary">₹2.668 Cr <span class="pct-pill">68.6%</span></td><td>₹119.56 L <span class="pct-pill">30.7%</span></td><td>₹147.20 L <span class="pct-pill">37.8%</span></td><td>₹51.70 L</td><td>₹70.50 L</td><td class="fw-bold">₹3.890 Cr</td><td class="fw-bold text-success">₹265.96</td><td class="fw-bold text-success">5.19x</td></tr>
                        <tr class="table-success bg-opacity-25"><td><strong>Feb 2027</strong></td><td><strong>₹82.00 L</strong></td><td class="fw-bold text-success">₹3.013 Cr <span class="pct-pill">67.2%</span></td><td><strong>₹137.61 L</strong> <span class="pct-pill">30.7%</span></td><td><strong>₹163.68 L</strong> <span class="pct-pill">36.5%</span></td><td><strong>₹58.90 L</strong></td><td><strong>₹88.20 L</strong></td><td class="fw-bold text-success fs-6">₹4.484 Cr</td><td class="fw-bold text-success fs-6">₹260.32</td><td class="fw-bold text-success fs-6">5.47x</td></tr>
                    </tbody>
                    <tfoot><tr class="table-secondary fw-bold"><td>CUMULATIVE</td><td>₹3.820 Cr</td><td>₹11.333 Cr <span class="pct-pill">61.1%</span></td><td>₹5.843 Cr</td><td>₹5.490 Cr</td><td>₹2.970 Cr</td><td>₹4.246 Cr</td><td class="text-success">₹18.493 Cr</td><td class="text-success">₹271.50 avg</td><td class="text-success">4.84x ROAS</td></tr></tfoot>
                </table>
            </div>
        </div>
    </div>
</body>
</html>"""

with open(r'reports/fabb6_plan_b_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(plan_b_html)

# 3. SIDE-BY-SIDE MASTER COMPARISON HTML (fabb6_side_by_side_comparison.html)
side_by_side_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fabb6 — Side-by-Side Model Comparison (Plan A vs Plan B)</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8fafc; color: #0f172a; }
        .header-box { background: #ffffff; border-bottom: 1px solid #e2e8f0; padding: 20px 0; }
        .comp-card { background: #ffffff; border-radius: 16px; border: 1px solid #e2e8f0; padding: 24px; height: 100%; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }
        .badge-plana { background: #eff6ff; color: #1e40af; border: 1px solid #bfdbfe; font-size: 0.85rem; padding: 6px 14px; border-radius: 8px; font-weight: 700; }
        .badge-planb { background: #f0fdf4; color: #166534; border: 1px solid #bbf7d0; font-size: 0.85rem; padding: 6px 14px; border-radius: 8px; font-weight: 700; }
        .table-mini { font-size: 0.82rem; }
        .table-mini th { background: #f8fafc; text-transform: uppercase; font-size: 0.72rem; }
        .iframe-container { height: 750px; border: 1px solid #e2e8f0; border-radius: 12px; overflow: hidden; }
        iframe { width: 100%; height: 100%; border: none; }
    </style>
</head>
<body>
    <div class="header-box mb-4">
        <div class="container-fluid px-4 d-flex justify-content-between align-items-center">
            <div>
                <h3 class="fw-bold mb-1"><i class="fa-solid fa-columns text-primary me-2"></i>FABB6 — SIDE-BY-SIDE FORECAST MODEL COMPARISON</h3>
                <p class="text-secondary mb-0 text-sm">Compare <strong>Plan A (Aggressive Volume Scaling)</strong> vs. <strong>Plan B (CPA Reduction & Funnel Remarketing)</strong></p>
            </div>
            <div class="d-flex gap-2">
                <a href="fabb6_plan_a_dashboard.html" target="_blank" class="btn btn-outline-primary fw-bold"><i class="fa-solid fa-external-link me-1"></i> Open Plan A Full Screen</a>
                <a href="fabb6_plan_b_dashboard.html" target="_blank" class="btn btn-outline-success fw-bold"><i class="fa-solid fa-external-link me-1"></i> Open Plan B Full Screen</a>
            </div>
        </div>
    </div>

    <div class="container-fluid px-4">
        <!-- Summary Comparison Cards -->
        <div class="row g-4 mb-4">
            <div class="col-md-6">
                <div class="comp-card border-primary border-opacity-50">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h4 class="fw-bold text-primary mb-0"><i class="fa-solid fa-bullseye me-2"></i>PLAN A: Volume Target Model</h4>
                        <span class="badge-plana">1,500 Orders / Day Goal</span>
                    </div>
                    <div class="row g-2 mb-3 text-center">
                        <div class="col-3"><div class="p-2 bg-light rounded"><div class="text-muted text-xs">Revenue</div><strong class="fs-6">₹18.55 Cr</strong></div></div>
                        <div class="col-3"><div class="p-2 bg-light rounded"><div class="text-muted text-xs">Orders</div><strong class="fs-6 text-primary">2,01,750</strong></div></div>
                        <div class="col-3"><div class="p-2 bg-light rounded"><div class="text-muted text-xs">Paid Spend</div><strong class="fs-6 text-warning">₹4.88 Cr</strong></div></div>
                        <div class="col-3"><div class="p-2 bg-light rounded"><div class="text-muted text-xs">ROAS</div><strong class="fs-6 text-purple" style="color:#7c3aed;">3.80x</strong></div></div>
                    </div>
                    <p class="text-secondary text-sm mb-0"><strong>Strategy:</strong> Aggressively scales paid ad budgets on Google + Meta to force daily volume growth to 1,500 orders/day by February 2027.</p>
                </div>
            </div>

            <div class="col-md-6">
                <div class="comp-card border-success border-opacity-50">
                    <div class="d-flex justify-content-between align-items-center mb-3">
                        <h4 class="fw-bold text-success mb-0"><i class="fa-solid fa-chart-line me-2"></i>PLAN B: CPA Reduction Model</h4>
                        <span class="badge-planb">High ROAS Efficiency</span>
                    </div>
                    <div class="row g-2 mb-3 text-center">
                        <div class="col-3"><div class="p-2 bg-light rounded"><div class="text-muted text-xs">Revenue</div><strong class="fs-6 text-success">₹18.49 Cr</strong></div></div>
                        <div class="col-3"><div class="p-2 bg-light rounded"><div class="text-muted text-xs">Paid CPA</div><strong class="fs-6 text-success">₹308 ➔ ₹260</strong></div></div>
                        <div class="col-3"><div class="p-2 bg-light rounded"><div class="text-muted text-xs">Paid Spend</div><strong class="fs-6 text-success">₹3.82 Cr</strong></div></div>
                        <div class="col-3"><div class="p-2 bg-light rounded"><div class="text-muted text-xs">ROAS</div><strong class="fs-6 text-purple" style="color:#7c3aed;">4.84x</strong></div></div>
                    </div>
                    <p class="text-secondary text-sm mb-0"><strong>Strategy:</strong> Segments campaigns into New Acquisition (higher CPA), Remarketing (lower CPA), and Re-orders (ultra-low CPA) to drop blended CPA and save ₹1.06 Cr in ad spend!</p>
                </div>
            </div>
        </div>

        <!-- Live Side-by-Side Dual View -->
        <div class="row g-4 mb-4">
            <div class="col-md-6">
                <div class="fw-bold text-primary mb-2"><i class="fa-solid fa-desktop me-1"></i> Plan A Live Interactive View</div>
                <div class="iframe-container shadow-sm">
                    <iframe src="fabb6_plan_a_dashboard.html"></iframe>
                </div>
            </div>
            <div class="col-md-6">
                <div class="fw-bold text-success mb-2"><i class="fa-solid fa-desktop me-1"></i> Plan B Live Interactive View</div>
                <div class="iframe-container shadow-sm">
                    <iframe src="fabb6_plan_b_dashboard.html"></iframe>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""

with open(r'reports/fabb6_side_by_side_comparison.html', 'w', encoding='utf-8') as f:
    f.write(side_by_side_html)

print("Generated Plan A Dashboard, Plan B Dashboard, and Side-by-Side Comparison HTML successfully!")
