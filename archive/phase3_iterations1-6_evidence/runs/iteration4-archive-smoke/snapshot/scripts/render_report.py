#!/usr/bin/env python3
"""Optional PDF visual QA, using PDFium when system Poppler is unavailable."""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'build/pdf-render'))
import pypdfium2 as pdfium
from PIL import Image, ImageDraw, ImageOps

pdf = pdfium.PdfDocument(ROOT / 'submission/Phase3_Test_Report.pdf')
files = []
for index in range(len(pdf)):
    page = pdf[index]
    target = ROOT / f'build/phase3-page-{index+1:02}.png'
    page.render(scale=1.6).to_pil().save(target)
    files.append(target)
    page.close()
pdf.close()
if not files:
    raise RuntimeError('No PDF pages rendered')
sheet = Image.new('RGB', (1200, 450 * ((len(files)+3)//4)), '#cccccc')
draw = ImageDraw.Draw(sheet)
for index, path in enumerate(files):
    sheet.paste(ImageOps.contain(Image.open(path), (290,410)),
                ((index%4)*300, 30+(index//4)*450))
    draw.text(((index%4)*300+10, (index//4)*450+10), path.stem, fill='black')
sheet.save(ROOT / 'build/phase3-contact.png')
print(f'Rendered {len(files)} pages and contact sheet')
