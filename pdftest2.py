from mmap import PAGESIZE
from reportlab.pdfgen.canvas import Canvas
from datetime import datetime, timedelta
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape, A3, A4
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, PageBreak, \
    PageTemplate, Spacer, FrameBreak, NextPageTemplate, Image
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER,TA_LEFT,TA_RIGHT


fileName = 'orderTypeTestCasesV2.pdf'
title = 'Order Type Screen Automated Tests'
testerName = 'Martín Pellicer'
actualDate = datetime.now().strftime('%d/%m/%Y')


canvas = Canvas(fileName, pagesize=landscape(A3))

doc = BaseDocTemplate(fileName , pagesize=landscape(A3))
contents =[]
width,height = landscape(A3)

left_header_frame = Frame(
    0.2*inch, 
    height-1.2*inch, 
    2*inch, 
    1*inch
    )

right_header_frame = Frame(
    2.2*inch, 
    height-1.2*inch, 
    width-2.5*inch, 
    1*inch,id='normal'
    )

frame_later = Frame(
    0.2*inch, 
    0.6*inch, 
    (width-0.6*inch)+0.17*inch, 
    height-1*inch,
    leftPadding = 0, 
    topPadding=0, 
    showBoundary = 0,
    id='col'
    )

frame_table= Frame(
    0.2*inch, 
    0.7*inch, 
    (width-0.6*inch)+0.17*inch, 
    height-2*inch,
    leftPadding = 0, 
    topPadding=0, 
    showBoundary = 0,
    id='col'
    )
laterpages = PageTemplate(id='laterpages',frames=[frame_later])

firstpage = PageTemplate(id='firstpage',frames=[left_header_frame, right_header_frame,frame_table],)

contents.append(NextPageTemplate('firstpage'))
logoleft = Image('logo.png')
logoleft._restrictSize(1.5*inch, 1.5*inch)
logoleft.hAlign = 'CENTER'
logoleft.vAlign = 'CENTER'

contents.append(logoleft)
contents.append(FrameBreak())
styleSheet = getSampleStyleSheet()
style_title = styleSheet['Heading1']
style_title.fontSize = 20 
style_title.fontName = 'Helvetica-Bold'
style_title.alignment=TA_CENTER

style_data = styleSheet['Normal']
style_data.fontSize = 16 
style_data.fontName = 'Helvetica'
style_data.alignment=TA_CENTER

style_date = styleSheet['Normal']
style_date.fontSize = 14
style_date.fontName = 'Helvetica'
style_date.alignment=TA_CENTER

canvas.setTitle(title)
contents.append(Paragraph(title, style_title))
contents.append(Paragraph(testerName, style_data))
contents.append(Paragraph(actualDate, style_date))
#contents.append(FrameBreak())

title_background = colors.fidblue


header = ["Id", "Order Type", "Name", "Address", "Phone Number", "Expected Result", "Real Result"]
# header.append([0, 0, 0, 0, 0, 0, 0, 0])
headerRow = Table(header)
tblStyle = TableStyle([
         ('BACKGROUND', (0, 0), (-1, 0), title_background),
         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
         ('ALIGN', (1, 0), (1, -1), 'CENTER'),
         ('GRID', (0, 0), (-1, -1), 1, colors.black)
     ])
headerRow.setStyle(tblStyle)

contents.append(NextPageTemplate('laterpages'))
#contents.append(headerRow)


header = ["Id", "Order Type", "Name", "Address", "Phone Number", "Expected Result", "Real Result"]
table = [header]
tableStyle = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightslategray),
        ('FONT', (0, 0), (-1, -1), 'Helvetica'),
        ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
]
for i in range(1, 100):
    row = [["id " + str(i),"orderType", "name", "address","phone", "expected result", "realResult"]]
    table.extend(row)
    tableStyle.append(('BACKGROUND', (0, i), (-1, i), colors.lightblue))
table = Table(table)
table.setStyle(TableStyle(tableStyle))
contents.append(table)
contents.append(PageBreak())

doc.addPageTemplates([firstpage,laterpages])
doc.build(contents)