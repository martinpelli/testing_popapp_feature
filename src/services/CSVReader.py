import csv
import models.OrderTypeModel as OrderTypeModel
import models.AddOrderModel as AddOrderModel
 

def readCSVAndSetTestCases(screen):
    testCases = []
    PATH_TO_DATA = '/home/pelli/Documents/Popapp/data/' + screen + 'TestCasesV2.csv'

    with open(PATH_TO_DATA, mode ='r')as file:

        csvFile = csv.reader(file)
        HEADER_OFFSET = 3
    
        for line in (l for i, l in enumerate(csvFile) if HEADER_OFFSET<=i):
            testCase = screenDataToRead(screen, line)()
            testCases.append(testCase)
    return testCases


def screenDataToRead(screen, line):
    return {
        'OrderType': lambda: OrderTypeModel.OrderTypeModel(line[0], line[2], line[3], line[4], line[5], line[6]),
        'AddOrder': lambda: AddOrderModel.AddOrderModel(line[1], line[2], line[3], line[4], line[5]),
    }.get(screen, lambda: None)