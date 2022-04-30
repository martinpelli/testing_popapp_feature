from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph,PageBreak, \
    PageTemplate, FrameBreak, NextPageTemplate, Image
from reportlab.lib.pagesizes import letter,A3
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import  TA_CENTER
from reportlab.pdfgen.canvas import Canvas
from datetime import datetime


class PDFWriter:

    rowNumber = 1
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
    

    def addRowAndStyleToTable(self, testCase, realResult, isTestOK):
        row = [[testCase.id, testCase.orderType, self.checkTextLength(testCase.inputs[0]), self.checkTextLength(testCase.inputs[1]), self.checkTextLength(testCase.inputs[2]), self.checkTextLength(testCase.expectedResult), self.checkTextLength(realResult)]]
        self.table.extend(row)
        self.tableStyle.append(('BACKGROUND', (0, self.rowNumber), (-1, self.rowNumber), colors.lightblue if isTestOK else colors.lightcoral))
        self.rowNumber += 1

    def checkTextLength(self, text):
        textLength = len(text)
        if textLength < 40:
            return text
        if textLength >= 40 and textLength < 80:
            firstHalf = text[:textLength//2]
            secondHalf = text[textLength//2:]
            firstHalf += '-\n'
            return firstHalf + secondHalf
        return "Too large text"
        

    def finishTable(self):

        fileName = 'OrderTypeScreenTestCasesResults.pdf'
        title = 'Order Type Screen Automated Tests'
        testerName = 'Martín Pellicer'
        actualDate = datetime.now().strftime('%d/%m/%Y')


        canvas = Canvas(fileName, pagesize=landscape(A3))

        doc = BaseDocTemplate(fileName, pagesize=landscape(A3))
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
            id='col'
            )

        frame_table= Frame(
            0.2*inch, 
            0.7*inch, 
            (width-0.6*inch)+0.17*inch, 
            height-2*inch,
            leftPadding = 0, 
            topPadding=0, 
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
        contents.append(FrameBreak())
        contents.append(NextPageTemplate('laterpages'))

        table = Table(self.table)
        table.setStyle(TableStyle(self.tableStyle))
        contents.append(table)
        #doc = SimpleDocTemplate('TestCasesResults.pdf', pagesize=landscape(A3))
        #page = []
        #page.append(table)
        #doc.build(page)
        doc.addPageTemplates([firstpage,laterpages])
        doc.build(contents)

