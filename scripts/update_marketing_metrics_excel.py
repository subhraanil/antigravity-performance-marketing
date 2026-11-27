import openpyxl
from openpyxl.styles import Alignment
import os

excel_path = r'reports/Marketing metrics.xlsx'

wb = openpyxl.load_workbook(excel_path)
ws = wb['Target metrics']

# Social Media metrics updated with authentic baselines from client screenshots:
# FB: 3.3K baseline -> 7.5K
# Insta: 24.3K baseline -> 40.0K
# YT / Subscriptions: 12 subscribers baseline -> 1,200

social_data_map = {
    42: ['15K', '18K', '24K', '32K', '40K', '50K'],            # Monthly Traffic or likes
    43: ['3.6K', '4.1K', '4.8K', '5.6K', '6.5K', '7.5K'],     # Social Media users (FB) - Baseline 3.3K
    44: ['25.5K', '27.2K', '29.5K', '32.4K', '35.8K', '40.0K'], # Social Media users (Insta) - Baseline 24.3K
    45: ['50', '120', '250', '450', '750', '1,200']             # Social Media subscription (YT) - Baseline 12
}

for row_idx, val_list in social_data_map.items():
    for col_idx, val in enumerate(val_list, start=3):
        cell = ws.cell(row=row_idx, column=col_idx)
        cell.value = val
        cell.alignment = Alignment(horizontal='center', vertical='center')

wb.save(excel_path)
print("Successfully updated authentic Social Media followers in 'Marketing metrics.xlsx'!")
