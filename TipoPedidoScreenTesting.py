import time
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver.v2 as uc

import TestCasesController as controller
import TestCaseModel as model




class FindElements(unittest.TestCase):

    def setUp(self):
        PROFILE_COOKIES_PATH = "home\\pelli\\Documents\\profile"
        ARE_YOU_THERE_FULL_XPATH =  "/html/body/app-root/div[2]/ng-component/div/blur-message/div/atom-button/button"
        NEW_ORDER_FULL_XPATH = "/html/body/app-root/div[2]/ng-component/div/div/div[1]/div[2]/atom-button/button"
        BAR_BUTTON_FULL_XPATH = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[1]/div[1]/img"
        DELIVERY_BUTTON_FULL_XPATH = "//html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[1]/div[2]/img"
        TAKE_AWAY_BUTTON_FULL_XPATH = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[1]/div[3]/img"
        NAME_INPUT_FULL_XPATH = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[2]/atom-input/div/input"
        ADDRESS_INPUT_FULL_XPATH = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[3]/atom-input/div/input"
        PHONE_INPUT_FULL_XPATH = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[4]/atom-input/div/input"
        self.CONTINUE_BUTTON_FULL_XPATH = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[3]/atom-button/button"
        PHONE_ERROR_LETTERS_TEXT = "*El telefono no puede tener letras"
        PHONE_ERROR_EXTENSIVE_TEXT = "*El telefono no puede ser tan extenso"
        OBLIGATORY_ADDRESS_ERROR_LABEL = "*La direccion es obligatoria"
        INVALID_ERROR_LABEL_FULL_XPATH_1 = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[4]/small"
        INVALID_ERROR_LABEL_FULL_XPATH_2 = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[4]/small[2]"
        OBLIGATORY_ERROR_ADDRESS_LABEL_FULL_XPATH = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[3]/small"
        self.CANCEL_ORDER_BUTTON_FULL_XPATH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/app-cancelar-nuevopedido/div[2]/div/div/div[2]/div/atom-button[2]/button"
        self.GO_BACK_WEB_PATH = "window.history.go(-1)"
        options = uc.ChromeOptions()
        options.user_data_dir = PROFILE_COOKIES_PATH
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        self.driver = uc.Chrome(options=options, version_main=100)
        self.driver.get('https://test.popapp.io/ponline/pedidos/keyLeandroDrazic3/pendientes')
        
        self.ordersTypeXpaths = {
            "Mostrador": BAR_BUTTON_FULL_XPATH, 
            "Delivery": DELIVERY_BUTTON_FULL_XPATH, 
            "Take Away": TAKE_AWAY_BUTTON_FULL_XPATH}
        self.inputsXpaths = [NAME_INPUT_FULL_XPATH, ADDRESS_INPUT_FULL_XPATH, PHONE_INPUT_FULL_XPATH]
        self.labelErrorsXpaths = [INVALID_ERROR_LABEL_FULL_XPATH_1, INVALID_ERROR_LABEL_FULL_XPATH_2, OBLIGATORY_ERROR_ADDRESS_LABEL_FULL_XPATH]
        self.labelErrorsTexts = [PHONE_ERROR_LETTERS_TEXT, PHONE_ERROR_EXTENSIVE_TEXT, OBLIGATORY_ADDRESS_ERROR_LABEL]
        self.newOrderButton = Ec.visibility_of_element_located((By.XPATH, NEW_ORDER_FULL_XPATH))
        self.realResult = ""
        areYouThereButton = Ec.visibility_of_element_located((By.XPATH, ARE_YOU_THERE_FULL_XPATH))
        wait = WebDriverWait(self.driver, 20)
        wait.until(areYouThereButton).click()
        wait.until(self.newOrderButton).click()


    def testOrderTypeScreen(self):

        for testCase in controller.testCases:
            
            try:
                orderTypeXpath = self.ordersTypeXpaths[testCase.orderType]
            except:
                pass

            if not self.checkIfElementExistsByXpath(orderTypeXpath):
                self.pageBackAndClickNewOrder()
            
            self.pressTypeOfOrder(orderTypeXpath)
            self.setTextInInputs(testCase)
            self.pressContinueOrder()
            
            isTestOk = self.isTestOK(testCase.expectedResult)
            self.writeTestResultInFile(testCase, isTestOk)


    def tearDown(self):
        pass
        #self.file.close()
        #self.driver.quit()


    def pressTypeOfOrder(self, orderTypeXpath):
        orderTypeSelected = self.driver.find_element(by=By.XPATH, value=orderTypeXpath)
        orderTypeSelected.click()


    def pageBackAndClickNewOrder(self):
        self.driver.execute_script(self.GO_BACK_WEB_PATH)
        wait = WebDriverWait(self.driver, 10)
        wait.until(Ec.visibility_of_element_located((By.XPATH, self.CANCEL_ORDER_BUTTON_FULL_XPATH))).click()
        wait.until(self.newOrderButton).click()


    def checkIfElementExistsByXpath(self, labelErrorXpath):
        try:
            self.driver.find_element(by=By.XPATH, value=labelErrorXpath)
        except NoSuchElementException:
            return False
        return True


    def setTextInInputs(self, testCase):        
        for index in range(0, len(self.inputsXpaths)):
            inputSelected = self.driver.find_element(by=By.XPATH, value=self.inputsXpaths[index])
            inputSelected.clear()
            text = testCase.inputs[index]
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
        continueButton = self.driver.find_element(by=By.XPATH, value=self.CONTINUE_BUTTON_FULL_XPATH)
        if continueButton.is_enabled():
            continueButton.click()
            self.realResult = "Correcto"


    def isTestOK(self, expectedResult):
        if self.isExpectedResultAnErrorLabel(expectedResult):
            return self.checkIfScreenIsShowingLabelError(expectedResult)
        return self.realResult == expectedResult


    def isExpectedResultAnErrorLabel(self, expectedResult):
        try:
            self.labelErrorsTexts.index(expectedResult)
        except:
            return False
        else:
            return True


    def checkIfScreenIsShowingLabelError(self, expectedResult):
        isTestOK = False
        wait = WebDriverWait(self.driver, 1)
        for labelErrorXpath in self.labelErrorsXpaths:
            if self.checkIfElementExistsByXpath(labelErrorXpath):
                self.realResult += wait.until(Ec.visibility_of_element_located((By.XPATH, labelErrorXpath))).text
                isTestOK = self.realResult == expectedResult
        return isTestOK

            


    def writeTestResultInFile(self, testCase, isTestOK):
        print("")
        print("Test case: " + testCase.id + " Tipo de Pedido: " + testCase.orderType + " ")
        print("Nombre: " + testCase.inputs[0] + " Dirección: " + testCase.inputs[1] + " Telefono: " + testCase.inputs[2] + " ")
        print("Resultado Esperado: " + testCase.expectedResult + " Resultado Real: " + self.realResult)
        print("Test OK" if isTestOK else "Test FAILED")


if __name__ == "__main__":
    unittest.main()        
