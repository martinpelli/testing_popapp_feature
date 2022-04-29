import csv
import TestCaseModel as model
 

def readCSVAndSetTestCases(testCases):


    with open('TestCases.csv', mode ='r')as file:

        csvFile = csv.reader(file)
        HEADER_OFFSET = 3
    
        for line in (l for i, l in enumerate(csvFile) if HEADER_OFFSET<=i):
            testCase = model.TestCaseModel(line[0], line[2], line[3], line[4], line[5], line[6])
            testCases.append(testCase)