import matplotlib.pyplot as plt
import numpy as np
import shutil
import os

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig_dpi = 300

months = ["Oct '26", "Nov '26 (BFCM)", "Dec '26"]
rev_a = [1230.67, 2037.54, 3450.00]
rev_b = [1493.14, 2252.10, 2574.56]

ord_a = [47.33, 72.77, 115.00]
ord_b = [57.43, 80.43, 87.27]

cpa_a = [23.24, 17.86, 12.17]
cpa_b = [19.15, 16.16, 16.04]

# Subplot 1: Revenue & Subplot 2: Order Volume
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8), dpi=fig_dpi)

x = np.arange(len(months))
width = 0.35

rects1 = ax1.bar(x - width/2, rev_a, width, label='Forecast - A (User Draft)', color='#94A3B8')
rects2 = ax1.bar(x + width/2, rev_b, width, label='Forecast - B (Realistic Best)', color='#2563EB')

ax1.set_title('Monthly Revenue Comparison (GBP)', fontsize=11, fontweight='bold', pad=12)
ax1.set_xticks(x)
ax1.set_xticklabels(months, fontsize=9)
ax1.yaxis.set_major_formatter('£{x:,.0f}')
ax1.legend(frameon=True, facecolor='#F8FAFC', fontsize=9)
ax1.grid(axis='y', linestyle=':', alpha=0.6)

for rect in rects1:
    h = rect.get_height()
    ax1.annotate(f'£{h:,.0f}', xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, color='#475569')

for rect in rects2:
    h = rect.get_height()
    ax1.annotate(f'£{h:,.0f}', xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#1E3A8A')

# Subplot 2: Order Volume
rects3 = ax2.bar(x - width/2, ord_a, width, label='Forecast - A (User Draft)', color='#CBD5E1')
rects4 = ax2.bar(x + width/2, ord_b, width, label='Forecast - B (Realistic Best)', color='#10B981')

ax2.set_title('Total Monthly Orders Comparison', fontsize=11, fontweight='bold', pad=12)
ax2.set_xticks(x)
ax2.set_xticklabels(months, fontsize=9)
ax2.legend(frameon=True, facecolor='#F8FAFC', fontsize=9)
ax2.grid(axis='y', linestyle=':', alpha=0.6)

for rect in rects3:
    h = rect.get_height()
    ax2.annotate(f'{h:.0f}', xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, color='#475569')

for rect in rects4:
    h = rect.get_height()
    ax2.annotate(f'{h:.0f}', xy=(rect.get_x() + rect.get_width() / 2, h),
                xytext=(0, 3), textcoords="offset points", ha='center', va='bottom', fontsize=8, fontweight='bold', color='#065F46')

plt.suptitle('Pet Mode: Forecast - A vs. Forecast - B Direct Comparison', fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()

out1 = 'reports/petmode_forecast_a_vs_b.png'
plt.savefig(out1, dpi=fig_dpi, bbox_inches='tight')
plt.close()

# Chart 2: CPA and Weekly Momentum
fig2, ax = plt.subplots(figsize=(8, 4.5), dpi=fig_dpi)
line_a = ax.plot(months, cpa_a, marker='o', color='#EF4444', linestyle='--', linewidth=2, label='Forecast - A Blended CPA')
line_b = ax.plot(months, cpa_b, marker='s', color='#2563EB', linestyle='-', linewidth=2.2, label='Forecast - B Blended CPA')

# Target line £20
ax.axhline(20.0, color='#10B981', linestyle=':', linewidth=1.5, label='Target CPA Goal (£20.00)')

ax.set_title('Blended CPA Trajectory: Forecast - A vs. Forecast - B', fontsize=11, fontweight='bold', pad=12)
ax.set_ylabel('Blended CPA (GBP)', fontsize=10, fontweight='bold')
ax.yaxis.set_major_formatter('£{x:,.2f}')
ax.set_ylim(10, 26)
ax.legend(frameon=True, facecolor='#F8FAFC', fontsize=9)
ax.grid(True, linestyle=':', alpha=0.6)

for i, txt in enumerate(cpa_a):
    ax.annotate(f'£{txt:.2f}', (months[i], txt), textcoords="offset points", xytext=(0,7), ha='center', fontsize=8.5, color='#B91C1C')

for i, txt in enumerate(cpa_b):
    ax.annotate(f'£{txt:.2f}', (months[i], txt), textcoords="offset points", xytext=(0,-14), ha='center', fontsize=8.5, fontweight='bold', color='#1D4ED8')

plt.tight_layout()
out2 = 'reports/petmode_cpa_comparison.png'
plt.savefig(out2, dpi=fig_dpi, bbox_inches='tight')
plt.close()

# Copy to artifact directory
art_dir = r'C:\Users\test\.gemini\antigravity\brain\4eb8b0c3-fb70-44b6-beb2-0fb647311113'
shutil.copyfile(out1, os.path.join(art_dir, 'petmode_forecast_a_vs_b.png'))
shutil.copyfile(out2, os.path.join(art_dir, 'petmode_cpa_comparison.png'))

print("All charts successfully generated and copied to artifact directory.")
