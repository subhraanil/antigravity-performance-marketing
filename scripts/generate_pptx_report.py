import os
import pandas as pd
import matplotlib.pyplot as plt
from googleapiclient.discovery import build
from google.oauth2 import service_account
import argparse
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import requests
import io

def get_service_account_creds():
    if os.path.exists('service_account.json'):
        return service_account.Credentials.from_service_account_file(
            'service_account.json', 
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
    return None

def read_sheet_data(sheet_id, range_name):
    # Try service account first
    creds = get_service_account_creds()
    if not creds:
        # Fallback to public CSV download if possible
        print("No service account found. Attempting public download...")
        url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
        df = pd.read_csv(url)
        return df
        
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    values = result.get('values', [])
    
    if not values:
        print('No data found.')
        return None
    
    df = pd.DataFrame(values[1:], columns=values[0])
    return df

# Design Constants
COLORS = {
    'primary': RGBColor(66, 133, 244),    # Google Blue
    'success': RGBColor(52, 168, 83),    # Google Green
    'warning': RGBColor(251, 188, 5),   # Google Yellow
    'danger': RGBColor(234, 67, 53),     # Google Red
    'dark': RGBColor(32, 33, 36),        # Dark Gray for text
    'light_bg': RGBColor(248, 249, 250)  # Light gray background
}

def generate_charts(df):
    # Set global chart style
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['text.color'] = '#202124'
    plt.rcParams['axes.labelcolor'] = '#202124'
    
    # Clean data
    for col in df.columns:
        if col != 'Week':
            df[col] = df[col].astype(str).str.replace(r'[£$€%,]', '', regex=True).replace('', '0')
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    
    charts = []
    
    # Chart 1: Sales Value (Revenue)
    plt.figure(figsize=(10, 6), facecolor='#F8F9FA')
    ax = plt.gca()
    ax.set_facecolor('#FFFFFF')
    plt.plot(df['Week'], df['Sales Value'], label='Sales Value (£)', marker='o', 
             color='#4285F4', linewidth=3, markersize=8, markerfacecolor='white', markeredgewidth=2)
    plt.title('Weekly Revenue Trends', fontsize=18, fontweight='bold', pad=20)
    plt.ylabel('Value (£)', fontsize=12)
    plt.legend(frameon=False)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig('chart_revenue.png', dpi=150)
    charts.append(('Revenue Analysis', 'chart_revenue.png', 'Sales Value'))
    
    # Chart 2: Conversions
    plt.figure(figsize=(10, 6), facecolor='#F8F9FA')
    ax = plt.gca()
    ax.set_facecolor('#FFFFFF')
    bars = plt.bar(df['Week'], df['Items Sale'], color='#34A853', alpha=0.8, label='Sales')
    plt.title('Weekly Sales Performance', fontsize=18, fontweight='bold', pad=20)
    plt.legend(frameon=False)
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig('chart_sales.png', dpi=150)
    charts.append(('Sales Analysis', 'chart_sales.png', 'Items Sale'))
    
    # Chart 3: ROAS
    plt.figure(figsize=(10, 6), facecolor='#F8F9FA')
    ax = plt.gca()
    ax.set_facecolor('#FFFFFF')
    plt.plot(df['Week'], df['ROAS'], marker='^', color='#FBBC05', linewidth=4, 
             markersize=10, label='ROAS', markerfacecolor='white')
    plt.axhline(y=df['ROAS'].mean(), color='#EA4335', linestyle=':', label=f'Avg: {df["ROAS"].mean():.1f}')
    plt.title('Return on Ad Spend (ROAS)', fontsize=18, fontweight='bold', pad=20)
    plt.legend(frameon=False)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.tight_layout()
    plt.savefig('chart_roas.png', dpi=150)
    charts.append(('ROAS Performance', 'chart_roas.png', 'ROAS'))
    
    return charts

def apply_slide_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = COLORS['light_bg']

def create_pptx(title, df, charts, output_file):
    prs = Presentation()
    
    # Set Slide Size to 16:9
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(7.5)
    
    last_week = df.iloc[-1]
    prev_week = df.iloc[-2] if len(df) > 1 else last_week
    
    # 1. Title Slide (Matching User Screenshot)
    slide_layout = prs.slide_layouts[6] 
    slide = prs.slides.add_slide(slide_layout)
    
    # White background for Title Slide specifically to match screenshot
    background = slide.background
    background.fill.solid()
    background.fill.fore_color.rgb = RGBColor(255, 255, 255)
    
    # Brighter Blue for Title to match screenshot
    title_blue = RGBColor(84, 153, 255)
    
    # Decorative top bar
    top_bar = slide.shapes.add_shape(6, 0, 0, prs.slide_width, Inches(0.12))
    top_bar.fill.solid()
    top_bar.fill.fore_color.rgb = title_blue
    top_bar.line.fill.background()
    
    # Main Title
    title_w, title_h = Inches(11), Inches(1.5)
    title_left = (prs.slide_width - title_w) / 2
    title_top = (prs.slide_height - title_h) / 2 - Inches(0.6)
    
    title_box = slide.shapes.add_textbox(title_left, title_top, title_w, title_h)
    tf = title_box.text_frame
    p = tf.paragraphs[0]
    p.text = "Weekly Performance Report"
    p.font.size = Pt(50)
    p.font.bold = True
    p.font.color.rgb = title_blue
    p.alignment = 1 # Center
    
    # Subtitle matching screenshot order
    subtitle_w, subtitle_h = Inches(9), Inches(1.2)
    sub_left = (prs.slide_width - subtitle_w) / 2
    sub_top = title_top + title_h - Inches(0.2)
    
    sub_box = slide.shapes.add_textbox(sub_left, sub_top, subtitle_w, subtitle_h)
    stf = sub_box.text_frame
    sp = stf.paragraphs[0]
    sp.text = "Business Insights & Growth Analysis"
    sp.font.size = Pt(24)
    sp.font.color.rgb = COLORS['dark']
    sp.alignment = 1
    
    sp2 = stf.add_paragraph()
    sp2.text = f"({last_week['Week']})"
    sp2.font.size = Pt(24)
    sp2.font.color.rgb = COLORS['dark']
    sp2.alignment = 1
    
    # 2. Key Metrics Slide
    slide_layout = prs.slide_layouts[5]
    slide = prs.slides.add_slide(slide_layout)
    apply_slide_background(slide)
    slide.shapes.title.text = "Executive Summary: Core KPIs"
    slide.shapes.title.text_frame.paragraphs[0].font.color.rgb = COLORS['dark']
    
    metrics = [
        ('Items Sale (Ads)', last_week['Items Sale'], prev_week['Items Sale']),
        ('Sales Value', last_week['Sales Value'], prev_week['Sales Value']),
        ('ROAS', last_week['ROAS'], prev_week['ROAS']),
        ('Clicks', last_week['Clicks'], prev_week['Clicks'])
    ]
    
    left_start, top_start = Inches(0.8), Inches(1.8)
    for i, (name, current, prev) in enumerate(metrics):
        left = left_start + Inches(6.0 * (i % 2))
        top = top_start + Inches(2.2 * (i // 2))
        
        growth = ((current - prev) / prev * 100) if prev != 0 else 0
        color = COLORS['success'] if current >= prev else COLORS['danger']
        
        # Add Card-like shape
        shape = slide.shapes.add_shape(6, left, top, Inches(5.5), Inches(1.8))
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(255, 255, 255)
        shape.line.color.rgb = COLORS['primary']
        shape.line.width = Pt(1.5)
        
        textbox = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), Inches(5), Inches(1.4))
        tf = textbox.text_frame
        p = tf.add_paragraph()
        val_str = f"£{current:,.2f}" if "Value" in name else f"{current}"
        p.text = f"{name}: {val_str}"
        p.font.size = Pt(24)
        p.font.bold = True
        p.font.color.rgb = COLORS['dark']
        
        p2 = tf.add_paragraph()
        p2.text = f"{'▲' if current >= prev else '▼'} {abs(growth):.1f}% vs Previous Week"
        p2.font.size = Pt(16)
        p2.font.color.rgb = color

    # 3. Chart Slides with Side-by-Side Data
    for chart_title, img_path, col_name in charts:
        slide_layout = prs.slide_layouts[5]
        slide = prs.slides.add_slide(slide_layout)
        apply_slide_background(slide)
        slide.shapes.title.text = chart_title
        slide.shapes.title.text_frame.paragraphs[0].font.color.rgb = COLORS['primary']
        
        # Add Image on the left (with a subtle border/frame)
        left = Inches(0.5)
        top = Inches(1.5)
        width = Inches(8)
        slide.shapes.add_picture(img_path, left, top, width=width)
        
        # Add Data Table on the right
        rows, cols = len(df) + 1, 2
        t_left = Inches(9.2)
        t_top = Inches(1.5)
        t_width = Inches(3.5)
        t_height = Inches(0.3 * rows)
        
        table = slide.shapes.add_table(rows, cols, t_left, t_top, t_width, t_height).table
        
        # Table Styling
        table.cell(0, 0).text = 'Week'
        table.cell(0, 1).text = col_name
        for j in range(2):
            cell = table.cell(0, j)
            cell.fill.solid()
            cell.fill.fore_color.rgb = COLORS['primary']
            cell.text_frame.paragraphs[0].font.size = Pt(11)
            cell.text_frame.paragraphs[0].font.bold = True
            cell.text_frame.paragraphs[0].font.color.rgb = RGBColor(255, 255, 255)
            
        for i, row in df.iterrows():
            table.cell(i+1, 0).text = str(row['Week'])
            val = row[col_name]
            val_str = f"£{val:,.2f}" if "Value" in col_name else str(val)
            table.cell(i+1, 1).text = val_str
            for j in range(2):
                cell = table.cell(i+1, j)
                cell.text_frame.paragraphs[0].font.size = Pt(10)
                if i % 2 == 0:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = RGBColor(240, 240, 240)
        
    # 4. Plan of Action (Professional Layout)
    slide_layout = prs.slide_layouts[5]
    slide = prs.slides.add_slide(slide_layout)
    apply_slide_background(slide)
    
    # Matching Title Blue for consistency
    title_blue = RGBColor(84, 153, 255)
    
    slide.shapes.title.text = "Strategic Plan of Action"
    slide.shapes.title.text_frame.paragraphs[0].font.color.rgb = title_blue
    
    # Using a Rounded Rectangle (type 5) instead of Octagon (type 6)
    card = slide.shapes.add_shape(5, Inches(0.8), Inches(1.5), Inches(11.7), Inches(5.2))
    card.fill.solid()
    card.fill.fore_color.rgb = RGBColor(255, 255, 255)
    card.line.color.rgb = title_blue
    card.line.width = Pt(1.5)
    
    bullet_box = slide.shapes.add_textbox(Inches(1.2), Inches(1.9), Inches(11), Inches(4.5))
    bullet_points = bullet_box.text_frame
    bullet_points.word_wrap = True
    
    p_header = bullet_points.paragraphs[0]
    p_header.text = "Key Observations & Optimization Strategy:"
    p_header.font.bold = True
    p_header.font.size = Pt(18)
    p_header.space_after = Pt(10)
    
    # Evaluation Logic prioritizing Main KPIs
    issues = []
    if last_week['ROAS'] < 300: 
        issues.append(f"Performance Alert: ROAS is at {last_week['ROAS']}%. Strategy: Prune underperforming keywords and reallocate budget to top-selling items.")
    if last_week['Sales Value'] < prev_week['Sales Value']:
        growth_impact = ((prev_week['Sales Value'] - last_week['Sales Value']) / prev_week['Sales Value'] * 100)
        issues.append(f"Revenue Impact: Value decreased by {growth_impact:.1f}%. Strategy: Implement re-engagement campaigns and review high-ticket item conversion paths.")
    if last_week['Items Sale'] < prev_week['Items Sale']:
        issues.append(f"Volume Alert: Sales volume down. Strategy: Monitor competitor pricing/offers and optimize ad schedules for peak hours.")
        
    if not issues:
        p = bullet_points.add_paragraph()
        p.text = "KPI Status: All primary metrics are trending positive. Strategy: Maintain current optimization and look for scaling opportunities in high-growth segments."
        p.font.size = Pt(16)
    else:
        for issue in issues:
            p = bullet_points.add_paragraph()
            p.text = issue
            p.font.size = Pt(16)
            p.level = 0
            p.space_before = Pt(10)

    prs.save(output_file)
    print(f"Report saved locally as: {output_file}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--sheet_id', required=True)
    parser.add_argument('--title', default="Marketing Performance Report")
    args = parser.parse_args()
    
    print("Reading data...")
    df = read_sheet_data(args.sheet_id, 'A1:K20')
    if df is None: return
    
    print("Generating charts...")
    charts = generate_charts(df)
    
    output_filename = "Performance_Report.pptx"
    print("Creating PowerPoint...")
    create_pptx(args.title, df, charts, output_filename)
    
    # Cleanup pngs
    for _, img, _ in charts:
        if os.path.exists(img):
            os.remove(img)

if __name__ == "__main__":
    main()
