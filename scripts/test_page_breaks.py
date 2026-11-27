import os
import win32com.client
import pythoncom
import pypdf
import docx

test_docx = r"C:\Users\test\Videos\Office\reports\test_page_breaks.docx"
test_pdf = r"C:\Users\test\Videos\Office\reports\test_page_breaks.pdf"

doc = docx.Document()
for i in range(1, 18):
    doc.add_paragraph(f"This is page {i}")
    if i < 17:
        doc.add_page_break()

doc.save(test_docx)

pythoncom.CoInitialize()
word = win32com.client.Dispatch("Word.Application")
word.Visible = False
word.DisplayAlerts = 0

doc_com = word.Documents.Open(os.path.abspath(test_docx))
doc_com.SaveAs(os.path.abspath(test_pdf), FileFormat=17) # wdFormatPDF = 17
doc_com.Close()
word.Quit()
pythoncom.CoUninitialize()

reader = pypdf.PdfReader(test_pdf)
print(f"Total pages generated: {len(reader.pages)}")
