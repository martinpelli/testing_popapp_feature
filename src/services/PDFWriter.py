from reportlab.lib import colors
from reportlab.lib.pagesizes import landscape, A3
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph,\
    PageTemplate, FrameBreak, NextPageTemplate, Image, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import  TA_CENTER
from reportlab.pdfgen.canvas import Canvas
from datetime import datetime

class PDFWriter:

    rowNumber = 1
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

    def __init__(self, header):
        self.table = [header]


    def addRowAndStyleToTable(self, testCase, isTestOK):
        row = [[*testCase]]
        self.table.extend(row)
        self.tableStyle.append(('BACKGROUND', (0, self.rowNumber), (-1, self.rowNumber), colors.lightblue if isTestOK else colors.lightcoral))
        self.rowNumber += 1


    def writeToPDF(self, fileName, pathToSaveFile, title, testerName):
        actualDate = datetime.now().strftime('%d/%m/%Y')
       
        canvas = Canvas(fileName, pagesize=landscape(A3))
        doc = BaseDocTemplate(pathToSaveFile + fileName, pagesize=landscape(A3))
        contents =[]
        width,height = landscape(A3)
        
        firstPage = PageTemplate(id='firstPage',frames=[self.createLeftHeaderFrame(height), self.createRightHeaderFrame(height, width), self.createFrameTable(height, width)])
        nextPages = PageTemplate(id='nextPages',frames=[self.createFrameWithoutHeader(height, width)])

        contents.append(NextPageTemplate('firstPage'))
        
        contents.append(self.createLogo())
        contents.append(FrameBreak())

        styleSheet = getSampleStyleSheet()
        canvas.setTitle(title)
        contents.append(Paragraph(title,  self.createTitleStyle(styleSheet)))
        contents.append(Paragraph(actualDate, self.createDateStyle(styleSheet)))
        contents.append(Paragraph(testerName, self.createDataStyle(styleSheet)))
        contents.append(FrameBreak())
        
        contents.append(NextPageTemplate('nextPages'))
        table = Table(self.table)
        table.setStyle(TableStyle(self.tableStyle))
        contents.append(table)
        
        doc.addPageTemplates([firstPage,nextPages])
        doc.build(contents)


    def createLeftHeaderFrame(self, height):
        return Frame(
            0.2*inch, 
            height-1.2*inch, 
            2*inch, 
            1*inch
            )

    def createRightHeaderFrame(self, height, width):
        return Frame(
            2.2*inch, 
            height-1.2*inch, 
            width-2.5*inch, 
            1*inch,id='normal'
            )

    def createFrameTable(aelf, height, width):
        return Frame(
            0.2*inch, 
            0.7*inch, 
            (width-0.6*inch)+0.17*inch, 
            height-2*inch,
            leftPadding = 0, 
            topPadding=0, 
            id='col'
            )

    def createFrameWithoutHeader(self, height, width):
        return Frame(
            0.2*inch, 
            0.6*inch, 
            (width-0.6*inch)+0.17*inch, 
            height-1*inch,
            leftPadding = 0, 
            topPadding=0, 
            id='col'
            )

    
    def createLogo(self):
        PATH_TO_LOGO = '/home/pelli/Documents/Popapp/assets/Logo.png'
        logoLeft = Image(PATH_TO_LOGO)
        logoLeft._restrictSize(1.5*inch, 1.5*inch)
        logoLeft.hAlign = 'CENTER'
        logoLeft.vAlign = 'CENTER'
        return logoLeft

    def createTitleStyle(self, styleSheet):
        titleStyle = styleSheet['Heading1']
        titleStyle.fontSize = 20 
        titleStyle.fontName = 'Helvetica-Bold'
        titleStyle.alignment=TA_CENTER
        return titleStyle

    def createDateStyle(self, styleSheet):
        dateStyle = styleSheet['Normal']
        dateStyle.fontSize = 14
        dateStyle.fontName = 'Helvetica'
        dateStyle.alignment=TA_CENTER
        return dateStyle
        
    def createDataStyle(self, styleSheet):
        dataStyle = styleSheet['Normal']
        dataStyle.fontSize = 16 
        dataStyle.fontName = 'Helvetica'
        dataStyle.alignment=TA_CENTER
        return dataStyle
