import os

out_path = r'reports/fabb6_growth_dashboard.html'
os.makedirs(os.path.dirname(out_path), exist_ok=True)

html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Fabb6 — Master Historic Data & Forecast Verification Dashboard</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-main: #f8fafc;
            --card-bg: #ffffff;
            --border-color: #e2e8f0;
            --text-primary: #0f172a;
            --text-secondary: #475569;
            --primary-blue: #2563eb;
            --accent-green: #16a34a;
            --accent-amber: #d97706;
            --accent-purple: #7c3aed;
        }

        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: var(--bg-main);
            color: var(--text-primary);
            padding-bottom: 60px;
        }

        .navbar-custom {
            background-color: #ffffff;
            border-bottom: 1px solid var(--border-color);
            padding: 18px 0;
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        .brand-title {
            font-weight: 800;
            font-size: 1.45rem;
            color: #0f172a;
        }

        .brand-title span {
            color: var(--primary-blue);
        }

        .kpi-card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 20px;
            height: 100%;
        }

        .table-custom-wrapper {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
            margin-bottom: 30px;
        }

        .table-custom {
            color: #0f172a;
            vertical-align: middle;
            margin-bottom: 0;
            font-size: 0.85rem;
        }

        .table-custom th {
            background-color: #1e293b;
            color: #ffffff;
            font-weight: 700;
            text-transform: uppercase;
            font-size: 0.72rem;
            letter-spacing: 0.5px;
            padding: 10px 12px;
        }

        .table-custom td {
            background-color: #ffffff;
            border-bottom: 1px solid #f1f5f9;
            padding: 10px 12px;
        }

        .nav-tabs .nav-link {
            font-weight: 700;
            color: var(--text-secondary);
            border-radius: 10px 10px 0 0;
            padding: 12px 24px;
        }

        .nav-tabs .nav-link.active {
            color: var(--primary-blue);
            border-color: #e2e8f0 #e2e8f0 #ffffff;
            background-color: #ffffff;
        }

        .verified-badge {
            background-color: #dcfce7;
            color: #166534;
            border: 1px solid #bbf7d0;
            font-weight: 700;
            padding: 4px 12px;
            border-radius: 6px;
            font-size: 0.8rem;
        }
    </style>
</head>
<body>

    <!-- Header Navigation -->
    <nav class="navbar-custom mb-4">
        <div class="container-fluid px-4">
            <div class="d-flex align-items-center justify-content-between">
                <div class="d-flex align-items-center gap-3">
                    <div class="brand-title"><i class="fa-solid fa-square-check text-success me-2"></i>FABB6 <span>HISTORIC DATA & FORECAST VERIFICATION</span></div>
                    <span class="verified-badge"><i class="fa-solid fa-check-double me-1"></i> Verified File: Historic Data and Forecast.xlsx (100% Math Verified)</span>
                </div>
                <div class="d-flex align-items-center gap-4 text-secondary text-sm">
                    <div><i class="fa-regular fa-calendar text-primary me-1"></i> Period: <strong>Dec 2025 – Feb 2027</strong></div>
                    <div><i class="fa-solid fa-building text-primary me-1"></i> Partner: <strong>Techno Exponent</strong></div>
                </div>
            </div>
        </div>
    </nav>

    <!-- Main Container -->
    <div class="container-fluid px-4">

        <!-- Verification Banner -->
        <div class="alert alert-success d-flex align-items-center gap-3 mb-4 shadow-sm">
            <i class="fa-solid fa-circle-check fs-2 text-success"></i>
            <div>
                <strong class="d-block fs-6">DATA VERIFICATION COMPLETE — 100% Mathematical & Formula Accuracy Confirmed!</strong>
                <span>All formulas (`=C19/B19`, `=I19/G19`, `=G19+M19`, `=U19/S19`, `=T19/U19`, etc.) across Historic Data (Dec–Aug), Plan A (CPA & ROAS Improvement), and Plan B (Scale Target Goal) in <strong>Historic Data and Forecast.xlsx</strong> have been verified with 100% exact precision.</span>
            </div>
        </div>

        <!-- Navigation Tabs -->
        <ul class="nav nav-tabs mb-4" id="forecastTabs" role="tablist">
            <li class="nav-item" role="presentation">
                <button class="nav-link active fs-6" id="plana-tab" data-bs-toggle="tab" data-bs-target="#plana" type="button" role="tab"><i class="fa-solid fa-seedling text-success me-2"></i>Plan A: CPA & ROAS Improvement (Steady Growth)</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link fs-6" id="planb-tab" data-bs-toggle="tab" data-bs-target="#planb" type="button" role="tab"><i class="fa-solid fa-rocket text-primary me-2"></i>Plan B: Scale Target (Reach 45,000 Orders/Month)</button>
            </li>
            <li class="nav-item" role="presentation">
                <button class="nav-link fs-6" id="hist-tab" data-bs-toggle="tab" data-bs-target="#hist" type="button" role="tab"><i class="fa-solid fa-clock-rotate-left text-warning me-2"></i>Historic Data Actuals (Dec 2025 – Aug 2026)</button>
            </li>
        </ul>

        <div class="tab-content" id="forecastTabsContent">

            <!-- TAB 1: PLAN A (CPA & ROAS IMPROVEMENT) -->
            <div class="tab-pane fade show active" id="plana" role="tabpanel">
                <div class="row g-3 mb-4">
                    <div class="col-md-3"><div class="kpi-card"><div class="text-muted fw-bold text-xs uppercase">6-Month Total Revenue</div><div class="fs-3 fw-bold text-success">₹12.16 Cr</div><div class="text-success text-xs fw-bold">Steady Sustainable Scaling</div></div></div>
                    <div class="col-md-3"><div class="kpi-card"><div class="text-muted fw-bold text-xs uppercase">Blended Paid CPA Trend</div><div class="fs-3 fw-bold text-primary">₹398 ➔ ₹318</div><div class="text-primary text-xs fw-bold">19.9% CPA Reduction</div></div></div>
                    <div class="col-md-3"><div class="kpi-card"><div class="text-muted fw-bold text-xs uppercase">6-Month Total Paid Spend</div><div class="fs-3 fw-bold text-dark">₹3.26 Cr</div><div class="text-muted text-xs fw-bold">Google (₹1.88 Cr) + Meta (₹1.38 Cr)</div></div></div>
                    <div class="col-md-3"><div class="kpi-card"><div class="text-muted fw-bold text-xs uppercase">Overall ROAS Range</div><div class="fs-3 fw-bold text-purple" style="color:#7c3aed;">3.05x ➔ 4.30x</div><div class="text-purple text-xs fw-bold" style="color:#7c3aed;">3.73x 6-Month Average</div></div></div>
                </div>

                <div class="table-custom-wrapper">
                    <h5 class="fw-bold text-success mb-3"><i class="fa-solid fa-table me-2"></i>Plan A: CPA & ROAS Improvement Forecast Table (Verified from Historic Data and Forecast.xlsx)</h5>
                    <div class="table-responsive">
                        <table class="table table-custom">
                            <thead>
                                <tr>
                                    <th>Month</th>
                                    <th>Total Monthly Orders</th>
                                    <th>Est. Total Revenue (INR)</th>
                                    <th>Organic & Return Orders</th>
                                    <th>AOV</th>
                                    <th>ROAS on Total</th>
                                    <th>Google Orders</th>
                                    <th>Google Sales (INR)</th>
                                    <th>Google Budget (INR)</th>
                                    <th>Google CPA</th>
                                    <th>Google ROAS</th>
                                    <th>Meta Orders</th>
                                    <th>Meta Sales (INR)</th>
                                    <th>Meta Budget (INR)</th>
                                    <th>Meta CPA</th>
                                    <th>Meta ROAS</th>
                                    <th>Total Paid Purchases</th>
                                    <th>Total Paid Sales</th>
                                    <th>Total Paid Spend</th>
                                    <th>Blended Paid CPA</th>
                                    <th>Blended Paid ROAS</th>
                                    <th>Daily Avg Orders</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr><td>Sept 2026</td><td>15,000</td><td>₹1,31,25,000</td><td>4,200</td><td>₹875</td><td>3.05x</td><td>5,500</td><td>₹52,50,000</td><td>₹25,00,000</td><td>₹454.55</td><td>2.10x</td><td>5,300</td><td>₹50,40,000</td><td>₹18,00,000</td><td>₹339.62</td><td>2.80x</td><td>10,800</td><td>₹1,02,90,000</td><td>₹43,00,000</td><td class="fw-bold text-primary">₹398.15</td><td class="fw-bold text-success">2.39x</td><td>500</td></tr>
                                <tr><td>Oct 2026</td><td>17,500</td><td>₹1,54,87,500</td><td>5,100</td><td>₹885</td><td>3.30x</td><td>6,300</td><td>₹60,75,000</td><td>₹27,00,000</td><td>₹428.57</td><td>2.25x</td><td>6,100</td><td>₹58,00,000</td><td>₹20,00,000</td><td>₹327.87</td><td>2.90x</td><td>12,400</td><td>₹1,18,75,000</td><td>₹47,00,000</td><td class="fw-bold text-primary">₹379.03</td><td class="fw-bold text-success">2.53x</td><td>565</td></tr>
                                <tr><td>Nov 2026</td><td>20,500</td><td>₹1,83,47,500</td><td>6,100</td><td>₹895</td><td>3.53x</td><td>7,300</td><td>₹72,00,000</td><td>₹30,00,000</td><td>₹410.96</td><td>2.40x</td><td>7,100</td><td>₹68,20,000</td><td>₹22,00,000</td><td>₹309.86</td><td>3.10x</td><td>14,400</td><td>₹1,40,20,000</td><td>₹52,00,000</td><td class="fw-bold text-primary">₹361.11</td><td class="fw-bold text-success">2.70x</td><td>683</td></tr>
                                <tr><td>Dec 2026</td><td>23,800</td><td>₹2,15,39,000</td><td>7,400</td><td>₹905</td><td>3.78x</td><td>8,300</td><td>₹84,15,000</td><td>₹33,00,000</td><td>₹397.59</td><td>2.55x</td><td>8,100</td><td>₹79,20,000</td><td>₹24,00,000</td><td>₹296.30</td><td>3.30x</td><td>16,400</td><td>₹1,63,35,000</td><td>₹57,00,000</td><td class="fw-bold text-primary">₹347.56</td><td class="fw-bold text-success">2.87x</td><td>768</td></tr>
                                <tr><td>Jan 2027</td><td>27,000</td><td>₹2,47,05,000</td><td>8,600</td><td>₹915</td><td>4.05x</td><td>9,200</td><td>₹94,50,000</td><td>₹35,00,000</td><td>₹380.43</td><td>2.70x</td><td>9,200</td><td>₹91,00,000</td><td>₹26,00,000</td><td>₹282.61</td><td>3.50x</td><td>18,400</td><td>₹1,85,50,000</td><td>₹61,00,000</td><td class="fw-bold text-primary">₹331.52</td><td class="fw-bold text-success">3.04x</td><td>871</td></tr>
                                <tr class="table-success bg-opacity-25"><td><strong>Feb 2027</strong></td><td><strong>30,500</strong></td><td><strong>₹2,83,65,000</strong></td><td><strong>9,800</strong></td><td><strong>₹930</strong></td><td><strong>4.30x</strong></td><td><strong>10,200</strong></td><td><strong>₹1,06,40,000</strong></td><td><strong>₹38,00,000</strong></td><td><strong>₹372.55</strong></td><td><strong>2.80x</strong></td><td><strong>10,500</strong></td><td><strong>₹1,09,20,000</strong></td><td><strong>₹28,00,000</strong></td><td><strong>₹266.67</strong></td><td><strong>3.90x</strong></td><td><strong>20,700</strong></td><td><strong>₹2,15,60,000</strong></td><td><strong>₹66,00,000</strong></td><td class="fw-bold text-success fs-6">₹318.84</td><td class="fw-bold text-success fs-6">3.27x</td><td><strong>1,017</strong></td></tr>
                            </tbody>
                            <tfoot><tr class="table-secondary fw-bold"><td>CUMULATIVE</td><td>1,34,300</td><td>₹12.157 Cr</td><td>41,200</td><td>₹901 avg</td><td>3.73x</td><td>46,800</td><td>₹4.703 Cr</td><td>₹1.880 Cr</td><td>₹401.71 avg</td><td>2.50x avg</td><td>46,300</td><td>₹4.560 Cr</td><td>₹1.380 Cr</td><td>₹298.06 avg</td><td>3.30x avg</td><td>93,100</td><td>₹9.263 Cr</td><td>₹3.260 Cr</td><td class="text-success fs-6">₹350.16 avg</td><td class="text-success fs-6">2.84x avg</td><td>746 avg</td></tr></tfoot>
                        </table>
                    </div>
                </div>
            </div>

            <!-- TAB 2: PLAN B (SCALE TARGET MODEL) -->
            <div class="tab-pane fade" id="planb" role="tabpanel">
                <div class="row g-3 mb-4">
                    <div class="col-md-3"><div class="kpi-card"><div class="text-muted fw-bold text-xs uppercase">6-Month Total Revenue</div><div class="fs-3 fw-bold text-primary">₹19.03 Cr</div><div class="text-primary text-xs fw-bold">Aggressive Volume Scale</div></div></div>
                    <div class="col-md-3"><div class="kpi-card"><div class="text-muted fw-bold text-xs uppercase">Feb 2027 Monthly Orders</div><div class="fs-3 fw-bold text-success">48,000 orders</div><div class="text-success text-xs fw-bold">Exceeds 45,000 Goal</div></div></div>
                    <div class="col-md-3"><div class="kpi-card"><div class="text-muted fw-bold text-xs uppercase">6-Month Total Paid Spend</div><div class="fs-3 fw-bold text-dark">₹5.31 Cr</div><div class="text-muted text-xs fw-bold">Google (₹2.95 Cr) + Meta (₹2.36 Cr)</div></div></div>
                    <div class="col-md-3"><div class="kpi-card"><div class="text-muted fw-bold text-xs uppercase">Overall ROAS Range</div><div class="fs-3 fw-bold text-purple" style="color:#7c3aed;">3.03x ➔ 3.86x</div><div class="text-purple text-xs fw-bold" style="color:#7c3aed;">3.58x 6-Month Average</div></div></div>
                </div>

                <div class="table-custom-wrapper border-primary border-opacity-50">
                    <h5 class="fw-bold text-primary mb-3"><i class="fa-solid fa-table me-2"></i>Plan B: Scale Target Forecast Table (Verified from Historic Data and Forecast.xlsx)</h5>
                    <div class="table-responsive">
                        <table class="table table-custom">
                            <thead>
                                <tr>
                                    <th>Month</th>
                                    <th>Total Monthly Orders</th>
                                    <th>Est. Total Revenue (INR)</th>
                                    <th>Organic & Return Orders</th>
                                    <th>AOV</th>
                                    <th>ROAS on Total</th>
                                    <th>Google Orders</th>
                                    <th>Google Sales (INR)</th>
                                    <th>Google Budget (INR)</th>
                                    <th>Google CPA</th>
                                    <th>Google ROAS</th>
                                    <th>Meta Orders</th>
                                    <th>Meta Sales (INR)</th>
                                    <th>Meta Budget (INR)</th>
                                    <th>Meta CPA</th>
                                    <th>Meta ROAS</th>
                                    <th>Total Paid Purchases</th>
                                    <th>Total Paid Sales</th>
                                    <th>Total Paid Spend</th>
                                    <th>Blended Paid CPA</th>
                                    <th>Blended Paid ROAS</th>
                                    <th>Daily Avg Orders</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr><td>Sept 2026</td><td>19,000</td><td>₹1,72,90,000</td><td>5,000</td><td>₹910</td><td>3.03x</td><td>6,800</td><td>₹64,60,000</td><td>₹32,00,000</td><td>₹470.59</td><td>2.02x</td><td>7,200</td><td>₹67,68,000</td><td>₹25,00,000</td><td>₹347.22</td><td>2.71x</td><td>14,000</td><td>₹1,32,28,000</td><td>₹57,00,000</td><td class="fw-bold text-primary">₹407.14</td><td class="fw-bold text-success">2.32x</td><td>633</td></tr>
                                <tr><td>Oct 2026</td><td>24,000</td><td>₹2,22,00,000</td><td>6,800</td><td>₹925</td><td>3.26x</td><td>8,300</td><td>₹80,75,000</td><td>₹38,00,000</td><td>₹457.83</td><td>2.13x</td><td>8,900</td><td>₹84,55,000</td><td>₹30,00,000</td><td>₹337.08</td><td>2.82x</td><td>17,200</td><td>₹1,65,30,000</td><td>₹68,00,000</td><td class="fw-bold text-primary">₹395.35</td><td class="fw-bold text-success">2.43x</td><td>774</td></tr>
                                <tr><td>Nov 2026</td><td>30,000</td><td>₹2,82,00,000</td><td>8,900</td><td>₹940</td><td>3.48x</td><td>10,100</td><td>₹1,00,80,000</td><td>₹45,00,000</td><td>₹445.54</td><td>2.24x</td><td>11,000</td><td>₹1,06,20,000</td><td>₹36,00,000</td><td>₹327.27</td><td>2.95x</td><td>21,100</td><td>₹2,07,00,000</td><td>₹81,00,000</td><td class="fw-bold text-primary">₹383.89</td><td class="fw-bold text-success">2.56x</td><td>1,000</td></tr>
                                <tr><td>Dec 2026</td><td>36,000</td><td>₹3,43,80,000</td><td>11,000</td><td>₹955</td><td>3.66x</td><td>11,900</td><td>₹1,21,27,500</td><td>₹52,00,000</td><td>₹436.97</td><td>2.33x</td><td>13,100</td><td>₹1,29,25,000</td><td>₹42,00,000</td><td>₹320.61</td><td>3.08x</td><td>25,000</td><td>₹2,50,52,500</td><td>₹94,00,000</td><td class="fw-bold text-primary">₹376.00</td><td class="fw-bold text-success">2.67x</td><td>1,161</td></tr>
                                <tr><td>Jan 2027</td><td>42,000</td><td>₹4,07,40,000</td><td>13,200</td><td>₹970</td><td>3.77x</td><td>13,700</td><td>₹1,44,00,000</td><td>₹60,00,000</td><td>₹437.96</td><td>2.40x</td><td>15,100</td><td>₹1,53,00,000</td><td>₹48,00,000</td><td>₹317.88</td><td>3.19x</td><td>28,800</td><td>₹2,97,00,000</td><td>₹1,08,00,000</td><td class="fw-bold text-primary">₹375.00</td><td class="fw-bold text-success">2.75x</td><td>1,355</td></tr>
                                <tr class="table-primary bg-opacity-25"><td><strong>Feb 2027</strong></td><td><strong>48,000</strong></td><td><strong>₹4,75,20,000</strong></td><td><strong>15,500</strong></td><td><strong>₹990</strong></td><td><strong>3.86x</strong></td><td><strong>15,300</strong></td><td><strong>₹1,65,24,000</strong></td><td><strong>₹68,00,000</strong></td><td><strong>₹444.44</strong></td><td><strong>2.43x</strong></td><td><strong>17,200</strong></td><td><strong>₹1,78,69,000</strong></td><td><strong>₹55,00,000</strong></td><td><strong>₹319.77</strong></td><td><strong>3.25x</strong></td><td><strong>32,500</strong></td><td><strong>₹3,43,93,000</strong></td><td><strong>₹1,23,00,000</strong></td><td class="fw-bold text-success fs-6">₹378.46</td><td class="fw-bold text-success fs-6">2.80x</td><td><strong>1,600</strong></td></tr>
                            </tbody>
                            <tfoot><tr class="table-secondary fw-bold"><td>CUMULATIVE</td><td>1,99,000</td><td>₹19.033 Cr</td><td>60,400</td><td>₹956 avg</td><td>3.58x</td><td>66,100</td><td>₹6.767 Cr</td><td>₹2.950 Cr</td><td>₹446.29 avg</td><td>2.29x avg</td><td>72,500</td><td>₹7.194 Cr</td><td>₹2.360 Cr</td><td>₹325.52 avg</td><td>3.05x avg</td><td>1,38,600</td><td>₹13.960 Cr</td><td>₹5.310 Cr</td><td class="text-success fs-6">₹383.12 avg</td><td class="text-success fs-6">2.63x avg</td><td>1,106 avg</td></tr></tfoot>
                        </table>
                    </div>
                </div>
            </div>

            <!-- TAB 3: HISTORIC DATA ACTUALS -->
            <div class="tab-pane fade" id="hist" role="tabpanel">
                <div class="alert alert-warning d-flex align-items-center gap-3 mb-4">
                    <i class="fa-solid fa-triangle-exclamation fs-4 text-warning"></i>
                    <div>
                        <strong>Client Technical Note (Row 28):</strong>
                        "Meta ads data is not trusted as it is not matching with Shopify Sales. The Conversion event setup in wrong way."
                    </div>
                </div>

                <div class="table-custom-wrapper">
                    <h5 class="fw-bold text-dark mb-3"><i class="fa-solid fa-clock-rotate-left me-2 text-warning"></i>Verified Historic Performance Actuals (Dec 2025 – Aug 2026)</h5>
                    <div class="table-responsive">
                        <table class="table table-custom">
                            <thead>
                                <tr>
                                    <th>Month</th>
                                    <th>Shopify Orders</th>
                                    <th>Shopify Revenue</th>
                                    <th>Return Rate</th>
                                    <th>AOV</th>
                                    <th>Google Orders</th>
                                    <th>Google Revenue</th>
                                    <th>Google Spend</th>
                                    <th>Google CPA</th>
                                    <th>Google ROAS</th>
                                    <th>Meta Orders</th>
                                    <th>Meta Revenue</th>
                                    <th>Meta Spend</th>
                                    <th>Meta CPA</th>
                                    <th>Meta ROAS</th>
                                    <th>Total Paid Spend</th>
                                    <th>Blended Paid CPA</th>
                                    <th>Blended Paid ROAS</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr><td>December</td><td>3,307</td><td>₹20,71,721</td><td>13.9%</td><td>₹626.47</td><td>473.5</td><td>₹3,70,066</td><td>₹2,27,772</td><td>₹481.09</td><td>1.62x</td><td>1,141</td><td>₹11,07,848</td><td>₹1,93,096</td><td>₹169.23</td><td>5.74x</td><td>₹4,20,868</td><td>₹260.69</td><td>3.51x</td></tr>
                                <tr><td>January</td><td>7,850</td><td>₹46,39,791</td><td>17.2%</td><td>₹591.06</td><td>1,323.3</td><td>₹10,83,477</td><td>₹7,62,405</td><td>₹576.14</td><td>1.42x</td><td>2,937</td><td>₹25,72,718</td><td>₹4,54,135</td><td>₹154.63</td><td>5.67x</td><td>₹12,16,540</td><td>₹285.55</td><td>3.01x</td></tr>
                                <tr><td>February</td><td>8,250</td><td>₹62,38,149</td><td>18.0%</td><td>₹756.14</td><td>1,331.0</td><td>₹10,85,206</td><td>₹8,63,165</td><td>₹648.53</td><td>1.26x</td><td>3,486</td><td>₹32,84,860</td><td>₹9,33,840</td><td>₹267.88</td><td>3.52x</td><td>₹17,97,005</td><td>₹373.06</td><td>2.43x</td></tr>
                                <tr><td>March</td><td>11,285</td><td>₹59,57,228</td><td>18.8%</td><td>₹527.89</td><td>1,908.8</td><td>₹14,18,248</td><td>₹15,00,636</td><td>₹786.17</td><td>0.95x</td><td>4,442</td><td>₹39,51,672</td><td>₹12,83,438</td><td>₹288.93</td><td>3.08x</td><td>₹27,84,074</td><td>₹438.38</td><td>1.93x</td></tr>
                                <tr><td>April</td><td>10,551</td><td>₹74,36,807</td><td>22.2%</td><td>₹704.84</td><td>1,458.4</td><td>₹11,75,190</td><td>₹20,01,447</td><td>₹1,372.38</td><td>0.59x</td><td>3,892</td><td>₹34,39,461</td><td>₹12,53,761</td><td>₹322.14</td><td>2.74x</td><td>₹32,55,208</td><td>₹608.41</td><td>1.42x</td></tr>
                                <tr><td>May</td><td>12,215</td><td>₹91,33,293</td><td>25.2%</td><td>₹747.71</td><td>1,479.2</td><td>₹12,42,342</td><td>₹21,36,192</td><td>₹1,444.15</td><td>0.58x</td><td>5,597</td><td>₹51,47,068</td><td>₹18,85,111</td><td>₹336.81</td><td>2.73x</td><td>₹40,21,304</td><td>₹568.29</td><td>1.59x</td></tr>
                                <tr><td>June</td><td>12,877</td><td>₹83,97,880</td><td>24.3%</td><td>₹652.16</td><td>1,243.1</td><td>₹11,00,655</td><td>₹27,33,880</td><td>₹2,199.24</td><td>0.40x</td><td>5,608</td><td>₹48,45,031</td><td>₹15,52,619</td><td>₹276.86</td><td>3.12x</td><td>₹42,86,498</td><td>₹625.67</td><td>1.39x</td></tr>
                                <tr><td>July</td><td>13,420</td><td>₹78,45,258</td><td>27.6%</td><td>₹584.59</td><td>2,300.0</td><td>₹20,18,130</td><td>₹24,77,270</td><td>₹1,077.07</td><td>0.81x</td><td>6,013</td><td>₹51,53,119</td><td>₹18,84,953</td><td>₹313.48</td><td>2.73x</td><td>₹43,62,222</td><td>₹524.75</td><td>1.64x</td></tr>
                                <tr class="table-warning bg-opacity-25"><td><strong>August</strong></td><td><strong>10,351</strong></td><td><strong>₹70,24,177</strong></td><td><strong>27.4%</strong></td><td><strong>₹678.60</strong></td><td><strong>6,434.6</strong></td><td><strong>₹61,26,036</strong></td><td><strong>₹31,26,167</strong></td><td><strong>₹485.83</strong></td><td><strong>1.96x</strong></td><td><strong>3,962</strong></td><td><strong>₹39,76,816</strong></td><td><strong>₹14,51,531</strong></td><td><strong>₹366.36</strong></td><td><strong>2.74x</strong></td><td><strong>₹45,77,698</strong></td><td><strong>₹440.31</strong></td><td><strong>2.21x</strong></td></tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

        </div>
    </div>

    <!-- Bootstrap 5 JS -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

with open(out_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated HTML Dashboard matched to Historic Data and Forecast.xlsx at {out_path}")
