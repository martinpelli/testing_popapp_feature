from multiprocessing.connection import wait
import time
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
from selenium.common.exceptions import NoSuchElementException
import undetected_chromedriver.v2 as uc





class FindElements(unittest.TestCase):

    def setUp(self):
        PROFILE_COOKIES_PATH = "home\\pelli\\Documents\\profile"
        NUEVO_PEDIDO_XPATH = "/html/body/app-root/div[2]/ng-component/div/div/div[1]/div[2]/atom-button/button"
        MOSTRADOR_BUTTON_FULL_XPATH = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[1]/div[1]/img"
        DELIVERY_BUTTON_FULL_XPATH = "//html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[1]/div[2]/img"
        TAKE_AWAY_BUTTON_FULL_XPATH = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[1]/div[3]/img"
        NOMBRE_INPUT_FULL_XPATH = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[2]/atom-input/div/input"
        DIRECCION_INPUT_FULL_XPATH = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[3]/atom-input/div/input"
        TELEFONO_INPUT_FULL_XPATH = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[4]/atom-input/div/input"
        self.CONTINUAR_BUTTON_FULL_XPATH = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[3]/atom-button/button"
        TELEFONO_ERROR_LETRAS_TEXT = "*El telefono no puede tener letras"
        TELEFONO_ERROR_EXTENSO_TEXT = "*El telefono no puede ser tan extenso"
        INVALID_ERROR_LABEL_FULL_XPATH_1 = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[4]/small"
        INVALID_ERROR_LABEL_FULL_XPATH_2 = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[4]/small[1]"
        INVALID_ERROR_LABEL_FULL_XPATH_3 = "/html/body/app-root/div[2]/ng-component/app-modal-tipoycliente/div[2]/div/div/div[2]/div[4]/small[2]"
        self.CANCELAR_PEDIDO_BUTTON_FULL_XPATH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/app-cancelar-nuevopedido/div[2]/div/div/div[2]/div/atom-button[2]/button"
        self.GO_BACK_WEB_PATH = "window.history.go(-1)"
        options = uc.ChromeOptions()
        options.user_data_dir = PROFILE_COOKIES_PATH
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        self.driver = uc.Chrome(options=options, version_main=100)
        self.driver.get('https://test.popapp.io/ponline/pedidos/keyLeandroDrazic3/pendientes')
        self.tipoPedidosXpaths = [ MOSTRADOR_BUTTON_FULL_XPATH, DELIVERY_BUTTON_FULL_XPATH, TAKE_AWAY_BUTTON_FULL_XPATH]
        self.inputsXpaths = [NOMBRE_INPUT_FULL_XPATH, DIRECCION_INPUT_FULL_XPATH,TELEFONO_INPUT_FULL_XPATH]
        self.labelErrorsXpaths = [INVALID_ERROR_LABEL_FULL_XPATH_1, INVALID_ERROR_LABEL_FULL_XPATH_2, INVALID_ERROR_LABEL_FULL_XPATH_3]
        self.labelErrorsTexts = [TELEFONO_ERROR_LETRAS_TEXT, TELEFONO_ERROR_EXTENSO_TEXT]
        self.nuevoPedidoButton = Ec.visibility_of_element_located((By.XPATH, NUEVO_PEDIDO_XPATH))
        wait = WebDriverWait(self.driver, 20)
        wait.until(self.nuevoPedidoButton).click()
        self.expectedResult = TELEFONO_ERROR_LETRAS_TEXT
        self.realResult = ""

    def testTipoPedido(self):

        for tipoPedidoXpath in self.tipoPedidosXpaths:
            if self.checkIfElementExistsByXpath(tipoPedidoXpath):
                
                self.setTextInInputsAndPressContinue(tipoPedidoXpath)
                self.isTestOK()
                
            else:
                self.driver.execute_script(self.GO_BACK_WEB_PATH)
                wait = WebDriverWait(self.driver, 10)
                wait.until(Ec.visibility_of_element_located((By.XPATH, self.CANCELAR_PEDIDO_BUTTON_FULL_XPATH))).click()
                wait.until(self.nuevoPedidoButton).click()
                
                self.setTextInInputsAndPressContinue(tipoPedidoXpath)
                self.isTestOK()



    def tearDown(self):
        pass
        #self.file.close()
        #self.driver.quit()


    def checkIfElementExistsByXpath(self, labelErrorXpath):
        try:
            self.driver.find_element(by=By.XPATH, value=labelErrorXpath)
        except NoSuchElementException:
            return False
        return True


    def setTextInInputsAndPressContinue(self, tipoPedidoXpath):
        tipoPedidoSelected = self.driver.find_element(by=By.XPATH, value=tipoPedidoXpath)
        tipoPedidoSelected.click()
        
        for inputXpath in self.inputsXpaths:
            inputSelected = self.driver.find_element(by=By.XPATH, value=inputXpath)
            inputSelected.clear()
            inputSelected.send_keys("-")
        
        continuarButton = self.driver.find_element(by=By.XPATH, value=self.CONTINUAR_BUTTON_FULL_XPATH)
        continuarButton.click()


    def isTestOK(self):
        isTestOk = None
        if self.isExpectedResultAnErrorLabel():
            isTestOk = self.checkIfScreenIsShowingLabelError()
            print(isTestOk)


    def isExpectedResultAnErrorLabel(self):
        return self.labelErrorsTexts.index(self.expectedResult) != -1


    def checkIfScreenIsShowingLabelError(self):
        try:
            wait = WebDriverWait(self.driver, 1)
            for labelErrorXpath in self.labelErrorsXpaths:
                if self.checkIfElementExistsByXpath(labelErrorXpath):
                    self.realResult = wait.until(Ec.visibility_of_element_located((By.XPATH, labelErrorXpath))).text
        except:
            return False
        else:
            return self.realResult == self.expectedResult






if __name__ == "__main__":
    unittest.main()        
