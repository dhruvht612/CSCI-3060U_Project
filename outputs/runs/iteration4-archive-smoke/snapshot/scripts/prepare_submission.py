#!/usr/bin/env python3
"""Render the report and package reproducible Phase 3 review artifacts.

Requires ReportLab/pypdf only for report authoring. Test execution stays dependency
free. ZIP scripts retain executable modes. No external submission or Git mutation.
"""
import hashlib
import html
from pathlib import Path
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'build/report-deps'))


def inline(text):
    text = text.replace('–', '-').replace('—', '-').replace('→', '->')
    text = html.escape(text)
    text = re.sub(r'`([^`]+)`', r'<font name="Courier">\1</font>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    return text


def render_pdf(output):
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted, LongTable, TableStyle, KeepTogether
    from pypdf import PdfReader

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle('BodyPhase3',fontName='Helvetica',fontSize=9.5,leading=13,spaceAfter=7))
    styles.add(ParagraphStyle('TablePhase3',fontName='Helvetica',fontSize=8,leading=10,spaceAfter=0))
    styles.add(ParagraphStyle('CodePhase3',fontName='Courier',fontSize=7,leading=10,spaceAfter=9))
    styles['Title'].fontSize=22; styles['Title'].leading=27
    styles['Heading2'].fontSize=13; styles['Heading2'].leading=17
    styles['Heading2'].spaceBefore=14; styles['Heading2'].spaceAfter=7
    styles['Heading2'].keepWithNext=True
    lines=(ROOT/'docs/Phase3_Test_Report.md').read_text(encoding='utf-8').splitlines()
    story=[]; i=0
    while i<len(lines):
        line=lines[i]
        if not line.strip(): i+=1; continue
        if line.startswith('```'):
            block=[]; i+=1
            while i<len(lines) and not lines[i].startswith('```'):
                block.append(lines[i]); i+=1
            story.append(Preformatted('\n'.join(block),styles['CodePhase3'])); i+=1; continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                cells=[x.strip() for x in lines[i].strip('|').split('|')]
                if not all(re.fullmatch(r'[-:]+',x) for x in cells): rows.append(cells)
                i+=1
            if rows[0][0]=='Test ID':
                # Preserve all six columns as labeled, readable entries in PDF;
                # Markdown retains the required six-column failure-log table.
                for row in rows[1:]:
                    entry=[Paragraph(inline(row[0]+' - '+row[1]),styles['Heading3'])]
                    for label,cell in zip(rows[0][2:],row[2:]):
                        entry.append(Paragraph('<b>'+inline(label)+':</b> '+inline(cell),styles['BodyPhase3']))
                    story.append(KeepTogether(entry))
                continue
            widths=[468/len(rows[0])]*len(rows[0])
            if rows[0][0]=='Execution': widths=[118,140,115,95]
            content=[[Paragraph(('<font color="#ffffff"><b>'+inline(c)+'</b></font>') if r==0 else inline(c),
                                styles['TablePhase3']) for c in row] for r,row in enumerate(rows)]
            table=LongTable(content,colWidths=widths,repeatRows=1,hAlign='LEFT')
            table.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#17324d')),
                ('TEXTCOLOR',(0,0),(-1,0),colors.white),
                ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),
                ('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),6),
                ('BOTTOMPADDING',(0,0),(-1,-1),6),
                ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f1f4f7')]),
                ('LINEBELOW',(0,0),(-1,0),0.5,colors.HexColor('#17324d')),
            ]))
            story.extend([table,Spacer(1,10)]); continue
        if line.startswith('# '):
            story.append(Paragraph(inline(line[2:]),styles['Title'])); i+=1; continue
        if line.startswith('## '):
            story.append(Paragraph(inline(line[3:]),styles['Heading2'])); i+=1; continue
        block=[line]; i+=1
        while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','```','- ')):
            block.append(lines[i]); i+=1
        story.append(Paragraph(inline(' '.join(block)),styles['BodyPhase3']))

    def footer(canvas,doc):
        canvas.setStrokeColor(colors.HexColor('#ccd4dc'))
        canvas.line(72,45,540,45)
        canvas.setFont('Helvetica',8); canvas.setFillColor(colors.HexColor('#526273'))
        canvas.drawString(72,32,'CSCI 3060U | Phase 3 | Review package - October 31, 2026')
        canvas.drawRightString(540,32,str(doc.page))

    doc=SimpleDocTemplate(str(output),pagesize=letter,leftMargin=72,rightMargin=72,
                          topMargin=54,bottomMargin=60,title='Phase 3 - Front End Requirements Testing',
                          author='CSCI 3060U Project Team (names pending)')
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    reader=PdfReader(output)
    full='\n'.join(page.extract_text() for page in reader.pages)
    for phrase in ['Introduction','Complete failure log','H01','S21','TC46','Conclusion']:
        if phrase not in full: raise ValueError('PDF missing content: '+phrase)
    print(f'PDF: {len(reader.pages)} pages; required text present')


def package():
    target=ROOT/'submission'; target.mkdir(exist_ok=True)
    pdf=target/'Phase3_Test_Report.pdf'
    render_pdf(pdf)
    note='''Phase 3 review package - CSCI 3060U Games Distribution System

Read docs/Phase3_Execution_Guide.md first. Build/test dependencies: C++17, Bash,
Python 3.9+ standard library. Git metadata is optional. Original fixtures remain unchanged.

Evidence: baseline 30/46, corrections 46/46, regression 46/46;
supplemental baseline 7/21, corrections/regression 21/21.

Outstanding before Canvas hand-in: team/member metadata, actual Phase 3 handout
review, TA format decisions, human review of terminal assertions, and complete
AI conversation export. AI_USAGE_LOG.md is not the complete transcript.

The six-column Markdown failure log is presented as labeled entries in the PDF
to keep the full details legible. Source tables are retained under docs/.

SUBMISSION_MANIFEST.sha256 lists the SHA-256 of every packaged file other than
the manifest itself. No binaries/dependency downloads/Git internals are included.
Nothing was submitted to Canvas or merged into main.
'''
    (target/'README.txt').write_text(note,encoding='utf-8')
    selected=[]
    for folder in ['src','include','inputs','expected','data','docs','Project_Docs','scripts','tests','outputs']:
        selected.extend(p for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
    selected.extend(ROOT/name for name in ['README.md','.gitignore','.gitattributes',
                    'CSCI 3060U - Phase 1_ Test Plan.md','Phase2_AI_use.docx'])
    contents={p.relative_to(ROOT).as_posix():p.read_bytes() for p in sorted(selected)}
    contents['Phase3_Test_Report.pdf']=pdf.read_bytes()
    contents['SUBMISSION_README.txt']=note.encode()
    manifest=''.join(hashlib.sha256(data).hexdigest()+'  '+name+'\n' for name,data in sorted(contents.items()))
    contents['SUBMISSION_MANIFEST.sha256']=manifest.encode()
    (target/'SHA256SUMS.txt').write_text(manifest,encoding='utf-8')
    archive=target/'CSCI3060U_Phase3_Review.zip'
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED) as z:
        for name,data in sorted(contents.items()):
            info=zipfile.ZipInfo(name); info.create_system=3
            info.external_attr=((0o100755 if name.endswith('.sh') else 0o100644)<<16)
            info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,data)
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for name,data in contents.items(): assert z.read(name)==data
        for name in ['scripts/run_tests.sh','scripts/validate_tests.sh']:
            assert (z.getinfo(name).external_attr>>16)&0o111
    print(f'ZIP verified: {len(contents)} entries, {archive.stat().st_size} bytes')


if __name__=='__main__':
    package()
