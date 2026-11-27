import json
import os

def build_dashboard():
    json_path = r'c:\Users\test\Videos\Office\data\dashboard_data.json'
    out_html = r'c:\Users\test\Videos\Office\reports\kuri_user_dashboard.html'

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    json_str = json.dumps(data)

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kuri E-Commerce Analytics & Customer Intelligence</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- FontAwesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #0f172a;
            color: #f8fafc;
        }}
        .glass-card {{
            background: rgba(30, 41, 59, 0.7);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 1rem;
        }}
        .glass-card:hover {{
            border-color: rgba(255, 255, 255, 0.15);
        }}
        .custom-scrollbar::-webkit-scrollbar {{
            width: 6px;
            height: 6px;
        }}
        .custom-scrollbar::-webkit-scrollbar-track {{
            background: #1e293b;
        }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{
            background: #475569;
            border-radius: 3px;
        }}
    </style>
</head>
<body class="min-h-screen p-4 md:p-8 custom-scrollbar">

    <!-- Dashboard Container -->
    <div class="max-w-7xl mx-auto space-y-6">

        <!-- Header -->
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 glass-card p-6">
            <div>
                <div class="flex items-center space-x-3">
                    <div class="p-2.5 bg-indigo-600/20 text-indigo-400 rounded-xl">
                        <i class="fa-solid fa-chart-pie text-2xl"></i>
                    </div>
                    <div>
                        <h1 class="text-2xl md:text-3xl font-bold tracking-tight text-white">Kuri Customer Intelligence Dashboard</h1>
                        <p class="text-sm text-slate-400 mt-1">Dataset: <span class="text-indigo-400 font-mono">kuri-users-2026-08-19.xlsx</span> (2,515 Users • 57 Fields)</p>
                    </div>
                </div>
            </div>
            <div class="flex items-center space-x-3">
                <button onclick="exportFilteredCSV()" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm rounded-lg transition-all shadow-lg shadow-indigo-600/20 flex items-center space-x-2">
                    <i class="fa-solid fa-download"></i>
                    <span>Export Full Data (CSV)</span>
                </button>
            </div>
        </div>

        <!-- Quick Insights Banners -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="glass-card p-4 flex items-center space-x-4 border-l-4 border-indigo-500">
                <div class="p-3 bg-indigo-500/10 text-indigo-400 rounded-full">
                    <i class="fa-solid fa-users text-xl"></i>
                </div>
                <div>
                    <h4 class="text-xs uppercase font-bold text-indigo-400 tracking-wider">User Growth Peak</h4>
                    <p class="text-sm text-slate-300 mt-0.5"><span class="font-bold text-white">2,515 registered users</span>. Peak acquisition occurred in <span class="font-bold text-indigo-300">April 2026 (672 new users)</span>.</p>
                </div>
            </div>
            <div class="glass-card p-4 flex items-center space-x-4 border-l-4 border-amber-500">
                <div class="p-3 bg-amber-500/10 text-amber-400 rounded-full">
                    <i class="fa-solid fa-cart-arrow-down text-xl"></i>
                </div>
                <div>
                    <h4 class="text-xs uppercase font-bold text-amber-400 tracking-wider">Checkout Abandonment</h4>
                    <p class="text-sm text-slate-300 mt-0.5"><span class="font-bold text-amber-300" id="banner-abandon-checkout">344 users</span> started checkout but didn't complete. Prime SMS retargeting cohort!</p>
                </div>
            </div>
            <div class="glass-card p-4 flex items-center space-x-4 border-l-4 border-emerald-500">
                <div class="p-3 bg-emerald-500/10 text-emerald-400 rounded-full">
                    <i class="fa-solid fa-mobile-screen-button text-xl"></i>
                </div>
                <div>
                    <h4 class="text-xs uppercase font-bold text-emerald-400 tracking-wider">Mobile-First Authentication</h4>
                    <p class="text-sm text-slate-300 mt-0.5"><span class="font-bold text-white">86% of users (2,164)</span> register via <span class="font-bold text-emerald-300">Phone OTP</span>, followed by Guest Checkout (7.6%).</p>
                </div>
            </div>
        </div>

        <!-- KPI Summary Cards -->
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-4">
            <div class="glass-card p-5">
                <div class="text-slate-400 text-xs font-medium uppercase tracking-wider">Total Revenue</div>
                <div class="text-xl md:text-2xl font-bold text-emerald-400 mt-2" id="kpi-revenue">₹0</div>
                <div class="text-xs text-slate-400 mt-1" id="kpi-orders-sub">1,685 Total Orders</div>
            </div>
            <div class="glass-card p-5">
                <div class="text-slate-400 text-xs font-medium uppercase tracking-wider">Total Users</div>
                <div class="text-xl md:text-2xl font-bold text-indigo-400 mt-2" id="kpi-users">2,515</div>
                <div class="text-xs text-slate-400 mt-1" id="kpi-active-sub">1,585 Active Buyers</div>
            </div>
            <div class="glass-card p-5">
                <div class="text-slate-400 text-xs font-medium uppercase tracking-wider">Checkout Starters</div>
                <div class="text-xl md:text-2xl font-bold text-cyan-400 mt-2" id="kpi-started-checkout">1,962</div>
                <div class="text-xs text-slate-400 mt-1" id="kpi-completed-sub">1,618 Completed</div>
            </div>
            <div class="glass-card p-5">
                <div class="text-slate-400 text-xs font-medium uppercase tracking-wider">Checkout Abandoned</div>
                <div class="text-xl md:text-2xl font-bold text-rose-400 mt-2" id="kpi-abandoned-checkout">344</div>
                <div class="text-xs text-slate-400 mt-1">Started vs Completed</div>
            </div>
            <div class="glass-card p-5">
                <div class="text-slate-400 text-xs font-medium uppercase tracking-wider">Cart Leads</div>
                <div class="text-xl md:text-2xl font-bold text-amber-400 mt-2" id="kpi-cart-leads">0</div>
                <div class="text-xs text-slate-400 mt-1" id="kpi-cart-sub">1,008 Cart Items</div>
            </div>
            <div class="glass-card p-5">
                <div class="text-slate-400 text-xs font-medium uppercase tracking-wider">Avg Order Value</div>
                <div class="text-xl md:text-2xl font-bold text-purple-400 mt-2" id="kpi-aov">₹0</div>
                <div class="text-xs text-slate-400 mt-1">Per Order Average</div>
            </div>
        </div>

        <!-- Monthly Acquisition & Revenue Growth Grid -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Monthly Acquisition Chart -->
            <div class="glass-card p-6">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <h3 class="font-semibold text-lg text-white">Monthly User Acquisition Growth</h3>
                        <p class="text-xs text-slate-400">New registered users per month</p>
                    </div>
                    <span class="px-2 py-1 bg-indigo-500/20 text-indigo-300 text-xs rounded font-mono">User Growth</span>
                </div>
                <div class="h-64">
                    <canvas id="chartAcquisition"></canvas>
                </div>
            </div>

            <!-- Monthly Revenue Trend Chart -->
            <div class="glass-card p-6">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <h3 class="font-semibold text-lg text-white">Monthly Revenue Performance (₹)</h3>
                        <p class="text-xs text-slate-400">Gross spend INR trend timeline</p>
                    </div>
                    <span class="px-2 py-1 bg-emerald-500/20 text-emerald-300 text-xs rounded font-mono">Revenue Trend</span>
                </div>
                <div class="h-64">
                    <canvas id="chartMonthlyRevenue"></canvas>
                </div>
            </div>
        </div>

        <!-- Location & Auth Intelligence Section -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <!-- Top Cities Chart -->
            <div class="glass-card p-6">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <h3 class="font-semibold text-lg text-white">Top Cities by Order Volume</h3>
                        <p class="text-xs text-slate-400">Total orders generated per city / metro market</p>
                    </div>
                    <span class="px-2 py-1 bg-indigo-500/20 text-indigo-300 text-xs rounded font-mono">Cities</span>
                </div>
                <div class="h-64">
                    <canvas id="chartTopCities"></canvas>
                </div>
            </div>

            <!-- Auth Provider Breakdown -->
            <div class="glass-card p-6">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <h3 class="font-semibold text-lg text-white">Authentication & Login Methods</h3>
                        <p class="text-xs text-slate-400">User sign-in method distribution</p>
                    </div>
                    <span class="px-2 py-1 bg-cyan-500/20 text-cyan-300 text-xs rounded font-mono">Auth Methods</span>
                </div>
                <div class="h-64">
                    <canvas id="chartAuth"></canvas>
                </div>
            </div>
        </div>

        <!-- Top Pincodes Detailed Table -->
        <div class="glass-card p-6">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-4">
                <div>
                    <h3 class="font-semibold text-lg text-white">Top 15 Hotspot Pincodes in India</h3>
                    <p class="text-xs text-slate-400">Pincodes generating the highest order volume and revenue</p>
                </div>
                <span class="text-xs text-slate-400 font-mono">Sorted by Total Orders</span>
            </div>
            <div class="overflow-x-auto custom-scrollbar">
                <table class="w-full text-left text-sm text-slate-300">
                    <thead class="bg-slate-800/80 text-xs uppercase text-slate-400 tracking-wider">
                        <tr>
                            <th class="py-3 px-4">Rank</th>
                            <th class="py-3 px-4">Pincode</th>
                            <th class="py-3 px-4">City / Metro</th>
                            <th class="py-3 px-4">District</th>
                            <th class="py-3 px-4 text-center">User Count</th>
                            <th class="py-3 px-4 text-center">Total Orders</th>
                            <th class="py-3 px-4 text-right">Total Spend</th>
                        </tr>
                    </thead>
                    <tbody id="pincodeTableBody" class="divide-y divide-slate-800/60 font-mono text-xs">
                        <!-- Populated by JS -->
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Customer Directory Data Table Section -->
        <div class="glass-card p-6">
            <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 mb-6">
                <div>
                    <h3 class="font-semibold text-xl text-white">Customer Master Directory</h3>
                    <p class="text-xs text-slate-400 mt-1">Filter, search, and export all 2,515 customer profiles.</p>
                </div>
                <div class="flex flex-wrap items-center gap-3">
                    <!-- Search Input -->
                    <div class="relative">
                        <i class="fa-solid fa-magnifying-glass absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-sm"></i>
                        <input type="text" id="searchInput" oninput="onFilterChange()" placeholder="Search name, city, pin, phone, email..." 
                               class="pl-9 pr-4 py-2 bg-slate-900/80 border border-slate-700 rounded-lg text-sm text-white placeholder-slate-500 focus:outline-none focus:border-indigo-500 w-64">
                    </div>
                    <!-- City Filter Dropdown -->
                    <select id="cityFilter" onchange="onFilterChange()" class="px-3 py-2 bg-slate-900/80 border border-slate-700 rounded-lg text-sm text-slate-200 focus:outline-none focus:border-indigo-500">
                        <option value="ALL">All Cities</option>
                        <option value="Mumbai (MMR)">Mumbai (MMR)</option>
                        <option value="Bengaluru">Bengaluru</option>
                        <option value="Hyderabad">Hyderabad</option>
                        <option value="Delhi (NCR)">Delhi (NCR)</option>
                        <option value="Pune">Pune</option>
                        <option value="Chennai">Chennai</option>
                        <option value="Noida / Ghaziabad (NCR)">Noida / Ghaziabad</option>
                        <option value="Gurugram (NCR)">Gurugram</option>
                    </select>
                    <!-- Segment Filter Dropdown -->
                    <select id="segmentFilter" onchange="onFilterChange()" class="px-3 py-2 bg-slate-900/80 border border-slate-700 rounded-lg text-sm text-slate-200 focus:outline-none focus:border-indigo-500">
                        <option value="ALL">All Buyers / Leads</option>
                        <option value="ACTIVE_BUYERS">Active Buyers (1,585)</option>
                        <option value="CART_ABANDON">Cart Abandoners (789)</option>
                        <option value="REPEAT_BUYERS">Repeat Buyers (91)</option>
                        <option value="VIP">VIP Spenders (₹3,000+)</option>
                        <option value="NON_BUYERS">Registered Non-Buyers (930)</option>
                    </select>
                </div>
            </div>

            <!-- Customer Table -->
            <div class="overflow-x-auto custom-scrollbar">
                <table class="w-full text-left text-sm text-slate-300">
                    <thead class="bg-slate-800/80 text-xs uppercase text-slate-400 tracking-wider">
                        <tr>
                            <th class="py-3 px-4">Customer Name</th>
                            <th class="py-3 px-4">Auth Method</th>
                            <th class="py-3 px-4">City / Metro</th>
                            <th class="py-3 px-4">Pincode</th>
                            <th class="py-3 px-4">Email</th>
                            <th class="py-3 px-4">Phone</th>
                            <th class="py-3 px-4 text-center">Orders</th>
                            <th class="py-3 px-4 text-right">Total Spend</th>
                            <th class="py-3 px-4 text-center">Cart</th>
                            <th class="py-3 px-4 font-sans">Joined</th>
                        </tr>
                    </thead>
                    <tbody id="userTableBody" class="divide-y divide-slate-800/60 font-mono text-xs">
                        <!-- Rendered dynamically -->
                    </tbody>
                </table>
            </div>

            <!-- Pagination Footer -->
            <div class="flex flex-col sm:flex-row items-center justify-between gap-4 mt-4 pt-4 border-t border-slate-800 text-xs text-slate-400">
                <div id="tableSummary">Showing 1 to 20 of 2,515 entries</div>
                <div class="flex items-center space-x-2" id="paginationControls">
                    <!-- Dynamic pagination -->
                </div>
            </div>
        </div>

    </div>

    <!-- Data Injection -->
    <script>
        const rawData = {json_str};
        let filteredUsers = [...rawData.users];
        let currentPage = 1;
        const pageSize = 20;

        function initDashboard() {{
            renderKPIs();
            renderTopPincodes();
            renderCharts();
            onFilterChange();
        }}

        function renderKPIs() {{
            const k = rawData.kpis;
            document.getElementById('kpi-revenue').innerText = '₹' + k.total_spend.toLocaleString('en-IN');
            document.getElementById('kpi-users').innerText = k.total_users.toLocaleString('en-IN');
            document.getElementById('kpi-aov').innerText = '₹' + k.avg_aov.toLocaleString('en-IN');
            document.getElementById('kpi-cart-leads').innerText = k.users_with_cart.toLocaleString('en-IN');
            document.getElementById('kpi-started-checkout').innerText = k.started_checkout.toLocaleString('en-IN');
            document.getElementById('kpi-abandoned-checkout').innerText = k.abandoned_checkout.toLocaleString('en-IN');
            
            document.getElementById('banner-abandon-checkout').innerText = k.abandoned_checkout + ' users';
        }}

        function renderTopPincodes() {{
            const tbody = document.getElementById('pincodeTableBody');
            tbody.innerHTML = '';
            const top15 = rawData.pincode_stats.slice(0, 15);
            top15.forEach((p, idx) => {{
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-800/40 transition-colors';
                tr.innerHTML = `
                    <td class="py-3 px-4 font-bold text-slate-500">#${{idx + 1}}</td>
                    <td class="py-3 px-4 font-mono font-bold text-indigo-400">${{p.pincode_str}}</td>
                    <td class="py-3 px-4 font-sans font-medium text-white">${{p.city}}</td>
                    <td class="py-3 px-4 font-sans text-slate-400">${{p.district}}</td>
                    <td class="py-3 px-4 text-center text-slate-300">${{p.user_count}}</td>
                    <td class="py-3 px-4 text-center font-bold text-emerald-400">${{p.total_orders}}</td>
                    <td class="py-3 px-4 text-right font-bold text-emerald-400">₹${{p.total_revenue.toLocaleString('en-IN')}}</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        function renderCharts() {{
            Chart.defaults.color = '#94a3b8';
            Chart.defaults.font.family = 'Inter';

            // Monthly Acquisition Chart
            const ma = rawData.monthly_acquisitions;
            new Chart(document.getElementById('chartAcquisition'), {{
                type: 'line',
                data: {{
                    labels: Object.keys(ma),
                    datasets: [{{
                        label: 'New Registrations',
                        data: Object.values(ma),
                        borderColor: '#6366f1',
                        backgroundColor: 'rgba(99, 102, 241, 0.15)',
                        fill: true,
                        tension: 0.3,
                        borderWidth: 3
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        y: {{ grid: {{ color: '#334155' }} }},
                        x: {{ grid: {{ display: false }} }}
                    }}
                }}
            }});

            // Monthly Revenue Chart
            const mr = rawData.monthly_revenue;
            new Chart(document.getElementById('chartMonthlyRevenue'), {{
                type: 'bar',
                data: {{
                    labels: Object.keys(mr),
                    datasets: [{{
                        label: 'Revenue (₹)',
                        data: Object.values(mr),
                        backgroundColor: '#10b981',
                        borderRadius: 6
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        y: {{ grid: {{ color: '#334155' }} }},
                        x: {{ grid: {{ display: false }} }}
                    }}
                }}
            }});

            // Top Cities Chart
            const cs = rawData.city_stats.slice(0, 10);
            new Chart(document.getElementById('chartTopCities'), {{
                type: 'bar',
                data: {{
                    labels: cs.map(c => c.city),
                    datasets: [{{
                        label: 'Total Orders',
                        data: cs.map(c => c.total_orders),
                        backgroundColor: '#818cf8',
                        borderRadius: 6
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        y: {{ grid: {{ color: '#334155' }} }},
                        x: {{ grid: {{ display: false }} }}
                    }}
                }}
            }});

            // Auth Provider Doughnut Chart
            const auth = rawData.auth_counts;
            new Chart(document.getElementById('chartAuth'), {{
                type: 'doughnut',
                data: {{
                    labels: Object.keys(auth),
                    datasets: [{{
                        data: Object.values(auth),
                        backgroundColor: ['#10b981', '#3b82f6', '#ea580c', '#a855f7', '#64748b'],
                        borderWidth: 0
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {{ legend: {{ position: 'right' }} }}
                }}
            }});
        }}

        function onFilterChange() {{
            const search = document.getElementById('searchInput').value.toLowerCase().trim();
            const city = document.getElementById('cityFilter').value;
            const segment = document.getElementById('segmentFilter').value;

            filteredUsers = rawData.users.filter(u => {{
                // Search filter
                const matchesSearch = !search || 
                    u.name.toLowerCase().includes(search) || 
                    u.email.toLowerCase().includes(search) || 
                    u.phone.includes(search) || 
                    u.pincode.includes(search) ||
                    u.city.toLowerCase().includes(search) ||
                    u.district.toLowerCase().includes(search);

                if (!matchesSearch) return false;

                // City filter
                if (city !== 'ALL' && u.city !== city) return false;

                // Segment filter
                if (segment === 'ACTIVE_BUYERS') return u.orders > 0;
                if (segment === 'CART_ABANDON') return u.cart > 0;
                if (segment === 'REPEAT_BUYERS') return u.orders >= 2;
                if (segment === 'VIP') return u.spend >= 3000;
                if (segment === 'NON_BUYERS') return u.orders === 0;

                return true;
            }});

            currentPage = 1;
            renderTable();
        }}

        function renderTable() {{
            const tbody = document.getElementById('userTableBody');
            tbody.innerHTML = '';

            const start = (currentPage - 1) * pageSize;
            const pageUsers = filteredUsers.slice(start, start + pageSize);

            if (pageUsers.length === 0) {{
                tbody.innerHTML = `<tr><td colspan="10" class="py-8 text-center text-slate-500 font-sans">No matching customers found.</td></tr>`;
            }} else {{
                pageUsers.forEach(u => {{
                    const tr = document.createElement('tr');
                    tr.className = 'hover:bg-slate-800/40 transition-colors';

                    let authBadge = `<span class="px-2 py-0.5 rounded text-[10px] bg-slate-800 text-slate-300 font-sans">${{u.auth}}</span>`;
                    if (u.auth === 'Phone') authBadge = `<span class="px-2 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 font-sans">Phone OTP</span>`;
                    else if (u.auth === 'Google') authBadge = `<span class="px-2 py-0.5 rounded text-[10px] bg-blue-500/20 text-blue-300 border border-blue-500/30 font-sans">Google</span>`;

                    tr.innerHTML = `
                        <td class="py-3 px-4 font-sans font-medium text-white">${{u.name}}</td>
                        <td class="py-3 px-4">${{authBadge}}</td>
                        <td class="py-3 px-4 font-sans font-medium text-indigo-300">${{u.city}}</td>
                        <td class="py-3 px-4 font-mono text-slate-400">${{u.pincode}}</td>
                        <td class="py-3 px-4 text-slate-400">${{u.email !== 'N/A' ? u.email : '<span class="text-slate-600">N/A</span>'}}</td>
                        <td class="py-3 px-4 text-slate-400">${{u.phone !== 'N/A' ? u.phone : '<span class="text-slate-600">N/A</span>'}}</td>
                        <td class="py-3 px-4 text-center font-bold ${{u.orders > 1 ? 'text-amber-400' : (u.orders === 1 ? 'text-emerald-400' : 'text-slate-500')}}">${{u.orders}}</td>
                        <td class="py-3 px-4 text-right font-bold text-emerald-400">₹${{u.spend.toLocaleString('en-IN')}}</td>
                        <td class="py-3 px-4 text-center">${{u.cart > 0 ? `<span class="px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 font-bold">${{u.cart}}</span>` : '<span class="text-slate-600">0</span>'}}</td>
                        <td class="py-3 px-4 text-slate-400 font-sans text-[11px]">${{u.joined}}</td>
                    `;
                    tbody.appendChild(tr);
                }});
            }}

            const total = filteredUsers.length;
            const end = Math.min(start + pageSize, total);
            document.getElementById('tableSummary').innerText = total === 0 ? 'Showing 0 entries' : `Showing ${{start + 1}} to ${{end}} of ${{total.toLocaleString('en-IN')}} entries`;

            const maxPages = Math.ceil(total / pageSize) || 1;
            const nav = document.getElementById('paginationControls');
            nav.innerHTML = `
                <button onclick="changePage(-1)" ${{currentPage === 1 ? 'disabled' : ''}} class="px-3 py-1 bg-slate-800 hover:bg-slate-700 disabled:opacity-40 disabled:hover:bg-slate-800 rounded text-slate-300 transition-all">Prev</button>
                <span class="px-2 font-mono text-slate-400">${{currentPage}} / ${{maxPages}}</span>
                <button onclick="changePage(1)" ${{currentPage === maxPages ? 'disabled' : ''}} class="px-3 py-1 bg-slate-800 hover:bg-slate-700 disabled:opacity-40 disabled:hover:bg-slate-800 rounded text-slate-300 transition-all">Next</button>
            `;
        }}

        function changePage(delta) {{
            currentPage += delta;
            renderTable();
        }}

        function exportFilteredCSV() {{
            if (filteredUsers.length === 0) return alert('No data to export!');
            const headers = ['Name', 'Auth Method', 'City', 'Pincode', 'District', 'State', 'Email', 'Phone', 'Orders', 'Spend (INR)', 'AOV', 'Cart Items', 'Tier', 'Joined Date'];
            const rows = filteredUsers.map(u => [
                `"${{u.name.replace(/"/g, '""')}}"`,
                `"${{u.auth}}"`,
                `"${{u.city}}"`,
                `"${{u.pincode}}"`,
                `"${{u.district}}"`,
                `"${{u.state}}"`,
                `"${{u.email}}"`,
                `"${{u.phone}}"`,
                u.orders,
                u.spend,
                u.aov,
                u.cart,
                `"${{u.tier}}"`,
                `"${{u.joined}}"`
            ]);

            const csvContent = 'data:text/csv;charset=utf-8,' + [headers.join(','), ...rows.map(e => e.join(','))].join('\\n');
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement('a');
            link.setAttribute('href', encodedUri);
            link.setAttribute('download', `kuri_full_customer_export_${{new Date().toISOString().slice(0,10)}}.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }}

        document.addEventListener('DOMContentLoaded', initDashboard);
    </script>
</body>
</html>
"""

    os.makedirs(os.path.dirname(out_html), exist_ok=True)
    with open(out_html, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML Dashboard successfully re-compiled to {out_html}")

if __name__ == '__main__':
    build_dashboard()
