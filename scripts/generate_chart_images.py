import matplotlib.pyplot as plt
import json
import os

def create_charts():
    json_path = r'c:\Users\test\Videos\Office\data\dashboard_data.json'
    out_dir = r'c:\Users\test\Videos\Office\reports'
    os.makedirs(out_dir, exist_ok=True)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    plt.style.use('dark_background')
    fig_bg = '#0f172a'
    card_bg = '#1e293b'

    # Chart 1: Monthly Acquisition Trend
    ma = data['monthly_acquisitions']
    fig, ax = plt.subplots(figsize=(9, 4.5), facecolor=fig_bg)
    ax.set_facecolor(card_bg)
    ax.plot(list(ma.keys()), list(ma.values()), color='#6366f1', marker='o', linewidth=3.5, markersize=8)
    ax.fill_between(list(ma.keys()), list(ma.values()), color='#6366f1', alpha=0.15)
    ax.set_title('Monthly User Registration Growth', fontsize=14, fontweight='bold', color='white', pad=15)
    ax.set_ylabel('New User Registrations', fontsize=11, color='#94a3b8')
    plt.xticks(rotation=25, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    for x, y in zip(list(ma.keys()), list(ma.values())):
        ax.annotate(f'{y}', xy=(x, y), xytext=(0, 6), textcoords="offset points", ha='center', fontsize=9, fontweight='bold', color='#818cf8')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'monthly_acquisitions.png'), dpi=150)
    plt.close()

    # Chart 2: Monthly Revenue Trend
    mr = data['monthly_revenue']
    fig, ax = plt.subplots(figsize=(9, 4.5), facecolor=fig_bg)
    ax.set_facecolor(card_bg)
    bars = ax.bar(list(mr.keys()), [v/1000 for v in mr.values()], color='#10b981', width=0.55)
    ax.set_title('Monthly Revenue Performance (₹ In Thousands)', fontsize=14, fontweight='bold', color='white', pad=15)
    ax.set_ylabel('Revenue (₹ Thousands)', fontsize=11, color='#94a3b8')
    plt.xticks(rotation=25, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'₹{height:.1f}k', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#34d399')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'monthly_revenue.png'), dpi=150)
    plt.close()

    # Chart 3: Top Cities
    cs = data['city_stats'][:10]
    cities = [c['city'] for c in cs]
    orders = [c['total_orders'] for c in cs]
    revenues = [c['total_revenue'] for c in cs]

    fig, ax = plt.subplots(figsize=(10, 5), facecolor=fig_bg)
    ax.set_facecolor(card_bg)
    bars = ax.bar(cities, orders, color='#6366f1', width=0.55)
    ax.set_title('Top Metro Cities by Total Order Volume', fontsize=14, fontweight='bold', color='white', pad=15)
    ax.set_ylabel('Total Completed Orders', fontsize=11, color='#94a3b8')
    plt.xticks(rotation=25, ha='right')
    ax.grid(axis='y', linestyle='--', alpha=0.3)
    for bar, rev in zip(bars, revenues):
        height = bar.get_height()
        ax.annotate(f'{height} orders\n(₹{rev/1000:.1f}k)', xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4), textcoords="offset points", ha='center', va='bottom', fontsize=9, fontweight='bold', color='#818cf8')
    plt.tight_layout()
    plt.savefig(os.path.join(out_dir, 'top_cities_orders.png'), dpi=150)
    plt.close()

    print("Updated chart images generated successfully in reports/")

if __name__ == '__main__':
    create_charts()
