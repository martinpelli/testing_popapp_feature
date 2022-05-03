import time
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver.v2 as uc

import services.PDFWriter as dataWriter
import services.CSVReader as dataReader



class FindElements(unittest.TestCase):

    def setUp(self):
        PROFILE_COOKIES_PATH = "home/pelli/Documents/Popapp/profile"
        ARE_YOU_THERE_FULL_XPATH =  "/html/body/app-root/div[2]/ng-component/div/blur-message/div/atom-button/button"
        NEW_ORDER_FULL_XPATH = "/html/body/app-root/div[2]/ng-component/div/div/div[1]/div[2]/atom-button/button"
        
        self.newOrderButton = Ec.visibility_of_element_located((By.XPATH, NEW_ORDER_FULL_XPATH))
        self.realResult = ""
        pdfHeader = ["Id", "Order Type", "Name", "Address", "Phone Number", "Expected Result", "Real Result"]
        self.pdfWriter = dataWriter.PDFWriter(pdfHeader)
        self.testCases = dataReader.readCSVAndSetTestCases("OrderType")
        options = uc.ChromeOptions()
        options.user_data_dir = PROFILE_COOKIES_PATH
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        self.driver = uc.Chrome(options=options, version_main=100)
        
        self.driver.get('https://test.popapp.io/ponline/pedidos/keyLeandroDrazic3/pendientes')
        areYouThereButton = Ec.visibility_of_element_located((By.XPATH, ARE_YOU_THERE_FULL_XPATH))
        wait = WebDriverWait(self.driver, 20)
        wait.until(areYouThereButton).click()
        wait.until(self.newOrderButton).click()


    def testOrderTypeScreen(self):
        BAR_BUTTON_FULL_XPATH = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[1]/div[1]/img"
        DELIVERY_BUTTON_FULL_XPATH = "//html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[1]/div[2]/img"
        TAKE_AWAY_BUTTON_FULL_XPATH = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[1]/div[3]/img"
        ordersTypeXpaths = {
            "Mostrador": BAR_BUTTON_FULL_XPATH, 
            "Delivery": DELIVERY_BUTTON_FULL_XPATH, 
            "Take Away": TAKE_AWAY_BUTTON_FULL_XPATH}

        for testCase in self.testCases:
            
            try:
                orderTypeXpath = ordersTypeXpaths[testCase.orderType]
            except:
                pass
            if not self.checkIfElementExistsByXpath(orderTypeXpath):
                self.goPageBack()
                self.pressNewOrder()
            self.pressTypeOfOrder(orderTypeXpath)
            
            self.setTextInInputs(testCase.inputs)
            self.pressContinueOrder()
            
            isTestOk = self.isTestOK(testCase.expectedResult)
            self.writeTestResultInFile(testCase, isTestOk)


    def pressTypeOfOrder(self, orderTypeXpath):
        try:
            orderTypeSelected = self.driver.find_element(by=By.XPATH, value=orderTypeXpath)
            orderTypeSelected.click()
        except:
            self.goPageBack()
            self.pressNewOrder()


    def goPageBack(self):
        GO_BACK_WEB_PATH = "window.history.go(-1)"
        self.driver.execute_script(GO_BACK_WEB_PATH)
        

    def pressNewOrder(self):
        CANCEL_ORDER_BUTTON_FULL_XPATH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/app-cancelar-nuevopedido/div[2]/div/div/div[2]/div/atom-button[2]/button"
        wait = WebDriverWait(self.driver, 20)
        wait.until(Ec.visibility_of_element_located((By.XPATH, CANCEL_ORDER_BUTTON_FULL_XPATH))).click()
        wait.until(self.newOrderButton).click()


    def checkIfElementExistsByXpath(self, elementXpath):
        try:
            self.driver.find_element(by=By.XPATH, value=elementXpath)
        except NoSuchElementException:
            return False
        return True


    def setTextInInputs(self, testCaseInputs):
        NAME_INPUT_FULL_XPATH = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[2]/atom-input/div/input"
        ADDRESS_INPUT_FULL_XPATH = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[3]/atom-input/div/input"
        PHONE_INPUT_FULL_XPATH = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[4]/atom-input/div/input"
        inputsXpaths = [NAME_INPUT_FULL_XPATH, ADDRESS_INPUT_FULL_XPATH, PHONE_INPUT_FULL_XPATH]

        for index in range(0, len(inputsXpaths)):
            inputSelected = self.driver.find_element(by=By.XPATH, value=inputsXpaths[index])
            inputSelected.clear()
            inputSelected.send_keys(1)
            inputSelected.clear()
            text = testCaseInputs[index]
            try:
                inputSelected.send_keys(text)
            except:
                self.sendSpecialText(inputSelected, text)
                
    
    def sendSpecialText(self, inputSelected, text):
        JS_ADD_TEXT_TO_INPUT = """
        var elm = arguments[0], txt = arguments[1];
        elm.value += txt;
        elm.dispatchEvent(new Event('change'));
        """
        self.driver.execute_script(JS_ADD_TEXT_TO_INPUT, inputSelected, text)


    def pressContinueOrder(self):
        CONTINUE_BUTTON_FULL_XPATH = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[3]/atom-button/button"
        continueButton = self.driver.find_element(by=By.XPATH, value=CONTINUE_BUTTON_FULL_XPATH)
        disabled = continueButton.get_attribute('disabled')
        if disabled:
            self.realResult = "Boton Continuar deshabilitado"
        else:
            continueButton.click()
            self.realResult = "Correcto"


    def isTestOK(self, expectedResult):
        if self.isExpectedResultAnErrorLabel(expectedResult):
            return self.checkIfScreenIsShowingLabelError(expectedResult)
        return self.realResult == expectedResult


    def isExpectedResultAnErrorLabel(self, expectedResult):
        PHONE_ERROR_LETTERS_TEXT = "*El telefono no puede tener letras"
        PHONE_ERROR_EXTENSIVE_TEXT = "*El telefono no puede ser tan extenso"
        OBLIGATORY_ADDRESS_ERROR_LABEL = "*La direccion es obligatoria"
        labelErrorsTexts = [PHONE_ERROR_LETTERS_TEXT, PHONE_ERROR_EXTENSIVE_TEXT, OBLIGATORY_ADDRESS_ERROR_LABEL]

        try:
            labelErrorsTexts.index(expectedResult)
        except:
            return False
        else:
            return True


    def checkIfScreenIsShowingLabelError(self, expectedResult):
        INVALID_ERROR_LABEL_FULL_XPATH_1 = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[4]/small"
        INVALID_ERROR_LABEL_FULL_XPATH_2 = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[4]/small[2]"
        OBLIGATORY_ERROR_ADDRESS_LABEL_FULL_XPATH = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[3]/small"       
        labelErrorsXpaths = [INVALID_ERROR_LABEL_FULL_XPATH_1, INVALID_ERROR_LABEL_FULL_XPATH_2, OBLIGATORY_ERROR_ADDRESS_LABEL_FULL_XPATH]

        isTestOK = None
        wait = WebDriverWait(self.driver, 1)
        realResult = ""
        for labelErrorXpath in labelErrorsXpaths:
            if self.checkIfElementExistsByXpath(labelErrorXpath):
                realResult += wait.until(Ec.visibility_of_element_located((By.XPATH, labelErrorXpath))).text
                isTestOK = realResult == expectedResult
        if realResult:
            self.realResult = realResult
        return isTestOK


    def writeTestResultInFile(self, testCase, isTestOK):
        self.pdfWriter.addRowAndStyleToTable(testCase, self.realResult,isTestOK)


    def tearDown(self):
        fileName = 'OrderTypeScreenTestCasesResults.pdf'
        pathToSaveFile = '/home/pelli/Documents/Popapp/data/'
        title = 'Order Type Screen Automated Tests'
        testerName = 'Martín Pellicer'
        self.pdfWriter.writeToPDF(fileName, pathToSaveFile, title, testerName)


if __name__ == "__main__":
    unittest.main()        
