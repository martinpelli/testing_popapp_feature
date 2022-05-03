class OrderTypeModel:


    def __init__(self, testId, orderType, name, address, telephone,expectedResult):
        self.id = testId
        self.orderType = orderType
        self.inputs = [name, address, telephone]
        self.expectedResult = expectedResult
