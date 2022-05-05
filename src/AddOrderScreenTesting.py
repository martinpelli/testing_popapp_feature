import time
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
import undetected_chromedriver.v2 as uc
from selenium.common.exceptions import NoSuchElementException

import services.PDFWriter as dataWriter
import services.CSVReader as dataReader
from services.CutLargeText import cutLargeText
from services.EmojiSender import sendSpecialText



class FindElements(unittest.TestCase):

    def setUp(self):
        PROFILE_COOKIES_PATH = "home/pelli/Documents/Popapp/profile"
        
        self.ORDER_PRODUCTS_FULL_XPATH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[2]/div[3]/app-detalle-desplegable/div/div/div/div/ngb-accordion/div"
        
        self.testCases = []
        self.realResult = ""
        self.totalPrice = 0
        pdfHeader = ["Id","Product","Quantity","Observation","Expected Result", "Real Result"]
        self.pdfWriter = dataWriter.PDFWriter(pdfHeader)
        options = uc.ChromeOptions()
        options.user_data_dir = PROFILE_COOKIES_PATH
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        self.driver = uc.Chrome(options=options, version_main=100)
        
        self.testCases = dataReader.readCSVAndSetTestCases("AddOrder")
        self.driver.get('https://test.popapp.io/ponline/pedido/keyLeandroDrazic3/new')
        self.referenceProductsFromProductsList()


    def referenceProductsFromProductsList(self):
        PRODUCTS_FULL_XAPTH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[1]/div[3]/div[2]/app-tablaproductos/div"
        PRODUCT_LABEL_FULL_XPATH = "/div/p"
        PRODUCT_PRICE_FULL_XPATH = "/div/div/p"
        PRODUCT_BUTTON_ADD_FULL_XPATH =  "/div/div/atom-button/button/i"

        thereIsAnyProduct = True
        self.productsLabels = []
        self.productsPrices = []
        self.productsButtons = []
        index = 1
        wait = WebDriverWait(self.driver, 20)
        wait.until(Ec.visibility_of_element_located((By.XPATH, PRODUCTS_FULL_XAPTH + "[1]" + PRODUCT_LABEL_FULL_XPATH))).text
        while thereIsAnyProduct:
            try:
                productLabel = self.driver.find_element(by=By.XPATH, value=PRODUCTS_FULL_XAPTH + "[" + str(index) + "]" + PRODUCT_LABEL_FULL_XPATH)
                productPrice = self.driver.find_element(by=By.XPATH, value=PRODUCTS_FULL_XAPTH + "[" + str(index) + "]" + PRODUCT_PRICE_FULL_XPATH)
                productButton = self.driver.find_element(by=By.XPATH, value=PRODUCTS_FULL_XAPTH + "[" + str(index) + "]" + PRODUCT_BUTTON_ADD_FULL_XPATH)
            except:
                thereIsAnyProduct = False
            else:
                self.productsLabels.append(productLabel.text)
                self.productsPrices.append(productPrice.text[1:])
                self.productsButtons.append(productButton)
            finally:
                index += 1


    def testAddOrderScreen(self):
        previousId = "CP1"
        amountOfProducts = {}
        for i in range(0, len(self.testCases)):
            
            try:
                labelProduct = self.testCases[i].product 
                if (previousId == self.testCases[i].id and (len(self.testCases)-1 != i)):
                    if labelProduct in amountOfProducts: amountOfProducts[labelProduct] += 1
                    else: amountOfProducts[labelProduct] = 1
                else:
                    self.deleteOrderToMakeNewOne(len(amountOfProducts))
                    self.totalPrice = 0
                    amountOfProducts = {}
                    amountOfProducts[labelProduct] = 1

                indexOfXpath = list(amountOfProducts.keys()).index(labelProduct)+1
                indexOfProduct = self.productsLabels.index(labelProduct)
            except:
                amountOfProducts[labelProduct] -= 1
                if amountOfProducts[labelProduct] <= 0: del amountOfProducts[labelProduct]
                self.realResult = "*Producto no encontrado"
                isTestOK = self.realResult == self.testCases[i].expectedResult
            else:
                self.addProductToOrder(i, indexOfProduct)
                isTestOK = self.isProductAddedCorrectlyToOrder(i,indexOfXpath, indexOfProduct,amountOfProducts)
            
            self.writeTestResultInFile(self.testCases[i], isTestOK)
            previousId = self.testCases[i].id
        

    def addProductToOrder(self, indexOfTestCase, indexOfProduct):
        QUANTITY_INPUT_FULL_XPATH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[1]/div[3]/div[2]/app-tablaproductos/app-modal-agregar-producto/div[2]/div/div/form/div[1]/div[2]/div[1]/atom-input/div/input"
        OBSERVATIONS_INPUT_FULL_XPATH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[1]/div[3]/div[2]/app-tablaproductos/app-modal-agregar-producto/div[2]/div/div/form/div[1]/div[2]/div[3]/textarea"
        ADD_TO_ORDER_BUTTON_FULL_XPATH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[1]/div[3]/div[2]/app-tablaproductos/app-modal-agregar-producto/div[2]/div/div/form/div[2]/atom-button/button"

        self.productsButtons[indexOfProduct].click()
        quantityInput = self.driver.find_element(by=By.XPATH, value=QUANTITY_INPUT_FULL_XPATH)
        observationsInput = self.driver.find_element(by=By.XPATH, value=OBSERVATIONS_INPUT_FULL_XPATH)
        addToOrderButton = self.driver.find_element(by=By.XPATH, value=ADD_TO_ORDER_BUTTON_FULL_XPATH)
        quantityInput.clear()
        try:
            quantityInput.send_keys(self.testCases[indexOfTestCase].quantity)
            observationsInput.send_keys(self.testCases[indexOfTestCase].observations)
        except:
            jsQuantityText = sendSpecialText()  
            jsObservationsText = sendSpecialText()
            self.driver.execute_script(jsQuantityText, quantityInput, self.testCases[indexOfTestCase].quantity)
            self.driver.execute_script(jsObservationsText, observationsInput, self.testCases[indexOfTestCase].observations)
        addToOrderButton.click()


    def isProductAddedCorrectlyToOrder(self,indexOfTestCase, indexOfXpath, indexOfProduct, amountOfProducts):
        QUIT_BUTTON_PRODUCT_TO_ADD_FULL_XPATH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[1]/div[3]/div[2]/app-tablaproductos/app-modal-agregar-producto/div[2]/div/div/div/i"
        labelProduct = self.testCases[indexOfTestCase].product

        if self.isScreenShowingLabelError(): 
            self.driver.find_element(by=By.XPATH, value=QUIT_BUTTON_PRODUCT_TO_ADD_FULL_XPATH).click()
            amountOfProducts[labelProduct] -= 1
            if amountOfProducts[labelProduct] <= 0: del amountOfProducts[labelProduct]
            return self.testCases[indexOfTestCase].expectedResult == self.realResult
        
        self.realResult = "Correcto"
        isTestOK = self.isProductOrderLabelCorrect(indexOfXpath, indexOfTestCase)
        if isTestOK: isTestOK = self.isProductOrderPriceCorrect(indexOfXpath, indexOfProduct, indexOfTestCase, amountOfProducts[labelProduct])
        if isTestOK: isTestOK = self.isProductOrderQuantityCorrect(indexOfXpath, indexOfTestCase, amountOfProducts[labelProduct])
        if isTestOK: isTestOK = self.isTotalPriceLabelCorrect()
        if isTestOK: isTestOK = self.isItemCountCorrect(len(amountOfProducts))
        return isTestOK

    
    def isProductOrderLabelCorrect(self, indexOfXpath, indexOfTestCase):
        LABEL_ORDER_PRODUCT_FULL_XPATH = "/div/button/p[1]/span"
        "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[2]/div[3]/app-detalle-desplegable/div/div/div/div/ngb-accordion/div[5]/div/button/p[1]/span"
        "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[2]/div[3]/app-detalle-desplegable/div/div/div/div/ngb-accordion/div/div/button/p[1]/span"
        orderProductLabel = self.driver.find_element(by=By.XPATH, value=self.ORDER_PRODUCTS_FULL_XPATH + "[" +str(indexOfXpath)  + "]" + LABEL_ORDER_PRODUCT_FULL_XPATH).text
        if (self.testCases[indexOfTestCase].product != orderProductLabel):
            self.realResult = "*Nombre incorrecto" 
            return False
        return True


    def isProductOrderPriceCorrect(self, indexOfXpath, indexOfProduct, indexOfTestCase,amountOfProduct):
        PRICE_ORDER_PRODUCT_FULL_XPATH = "/div/button/p[2]"
        
        try:
            orderProductPrice = int(self.driver.find_element(by=By.XPATH, value=self.ORDER_PRODUCTS_FULL_XPATH + "[" +str(indexOfXpath)  + "]" + PRICE_ORDER_PRODUCT_FULL_XPATH).text[1:])
            if (int(self.productsPrices[indexOfProduct]) * int(self.testCases[indexOfTestCase].quantity)) * amountOfProduct !=  orderProductPrice:
                self.realResult = "*Precio incorrecto"
                return False
            self.totalPrice += int(self.productsPrices[indexOfProduct]) * int(self.testCases[indexOfTestCase].quantity)
            return True
        except:
            self.realResult = "*Precio incorrecto"
            return False


    def isProductOrderQuantityCorrect(self, indexOfXpath, indexOfTestCase,amountOfProduct):
        QUANTITY_ORDER_PRODUCT_FULL_XPATH = "/div/button/p[1]/strong"

        try:
            orderProductQuantity = self.driver.find_element(by=By.XPATH, value=self.ORDER_PRODUCTS_FULL_XPATH + "[" +str(indexOfXpath)  + "]" + QUANTITY_ORDER_PRODUCT_FULL_XPATH).text
            if (str(int(self.testCases[indexOfTestCase].quantity) * amountOfProduct)  + " x  " != orderProductQuantity):
                self.realResult = "*Cantidad incorrecta"
                return False
            return True
        except:
            self.realResult = "*Cantidad incorrecta"
            return False


    def isTotalPriceLabelCorrect(self):
        TOTAL_LABEL_FULL_XPATH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[2]/div[4]/div/h6"
        
        totalPriceLabel =  self.driver.find_element(by=By.XPATH, value=TOTAL_LABEL_FULL_XPATH).text.replace(".", "",1)
        indexOfComma = totalPriceLabel.find(",",9)
        totalPriceLabel = int(totalPriceLabel[9:indexOfComma])
        if self.totalPrice != totalPriceLabel:
            self.realResult = "*Precio total incorrecto"
            return False
        return True


    def isItemCountCorrect(self, amountOfProducts):
        ORDER_ITEMS_COUNT_LABEL_FULL_XPATH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[2]/div[2]/div/p"

        itemsCountLabel = self.driver.find_element(by=By.XPATH, value=ORDER_ITEMS_COUNT_LABEL_FULL_XPATH).text
        if itemsCountLabel != "Items "+ str(amountOfProducts):
            self.realResult = "*Cantidad de items incorrecto"
            return False
        return True


    def isScreenShowingLabelError(self):
        INVALID_ERROR_LABEL_FULL_XPATH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[1]/div[3]/div[2]/app-tablaproductos/app-modal-agregar-producto/div[2]/div/div/form/div[1]/div[2]/div[1]/small"
                                        
        wait = WebDriverWait(self.driver, 1)
        if self.checkIfElementExistsByXpath(INVALID_ERROR_LABEL_FULL_XPATH):
            self.realResult = wait.until(Ec.visibility_of_element_located((By.XPATH, INVALID_ERROR_LABEL_FULL_XPATH))).text
            return True
        return False
    

    def checkIfElementExistsByXpath(self, elementXpath):
        try:
            self.driver.find_element(by=By.XPATH, value=elementXpath)
        except NoSuchElementException:
            return False
        return True


    def deleteOrderToMakeNewOne(self, indexOfXpath):
        PANEL_BUTTON_ORDER_FULL_XPATH = "/div/button"
        DELETE_PRODUCT_ORDER_FULL_XPATH = "/div[2]/div/div/div/button[2]"
        
        for j in range(indexOfXpath, 0, -1):
            self.driver.find_element(by=By.XPATH, value=self.ORDER_PRODUCTS_FULL_XPATH + "[" +str(j)  + "]" + PANEL_BUTTON_ORDER_FULL_XPATH).click()
            self.driver.find_element(by=By.XPATH, value=self.ORDER_PRODUCTS_FULL_XPATH + "[" +str(j)  + "]" + DELETE_PRODUCT_ORDER_FULL_XPATH).click()


    def writeTestResultInFile(self, testCase, isTestOK):
        testCase = [
            testCase.id, 
            cutLargeText(testCase.product), 
            cutLargeText(testCase.quantity),
            cutLargeText(testCase.observations),
            cutLargeText(testCase.expectedResult),
            cutLargeText(self.realResult)
            ]
        self.pdfWriter.addRowAndStyleToTable(testCase,isTestOK)


    def tearDown(self):
        fileName = 'AddOrderScreenTestCasesResults.pdf'
        pathToSaveFile = '/home/pelli/Documents/Popapp/data/'
        title = 'Add Order Screen Automated Tests'
        testerName = 'Martín Pellicer'
        self.pdfWriter.writeToPDF(fileName, pathToSaveFile, title, testerName)


if __name__ == "__main__":
    unittest.main()        
