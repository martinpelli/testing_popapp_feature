from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


class PDFWriter:

    rowNumber = 1
    header = ["Id", "Order Type", "Name", "Address", "Phone Number", "Expected Result", "Real Result"]
    table = [header]
    tableStyle = [
            ('FONT', (0, 0), (-1, -1), 'Helvetica'),
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('INNERGRID', (0, 0), (7, 0), 0.5, colors.black),
            ('BOX', (0, 0), (-1, -1), 0.5, colors.black),
    ]
    

    def addRowAndStyleToTable(self, testCase, realResult, isTestOK):
        row = [[testCase.id, testCase.orderType, testCase.inputs[0], testCase.inputs[1], testCase.inputs[2], testCase.expectedResult, realResult]]
        self.table.extend(row)
        self.tableStyle.append(('INNERGRID', (7, self.rowNumber), (7, self.rowNumber), 0.5, colors.blue if isTestOK else colors.red))
        self.rowNumber += 1


    def finishTable(self):
        table = Table(self.table)
        table.setStyle(TableStyle(self.tableStyle))
        doc = SimpleDocTemplate('TestCasesResults.pdf', pagesize=A4)
        doc.build([table])

    