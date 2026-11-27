import os
import sys
import json
import csv
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

# Ensure scripts directory is in sys.path
sys.path.append(r"C:\Users\test\Videos\Office\scripts")
from generate_issue_only_report_engine import build_docx_report, build_pdf_report

out_dir = r"C:\Users\test\Videos\Office\website audit\storiai.ai"
os.makedirs(out_dir, exist_ok=True)
os.makedirs(r"website audit/storiai.ai", exist_ok=True)

print("Engine imported successfully. Ready to build StoriAI audit.")
