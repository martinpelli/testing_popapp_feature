import time
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as Ec
import undetected_chromedriver.v2 as uc

import services.PDFWriter as dataWriter
import services.CSVReader as dataReader
from services.CutLargeText import cutLargeText



class FindElements(unittest.TestCase):

    def setUp(self):
        PROFILE_COOKIES_PATH = "home/pelli/Documents/Popapp/profile"
        
        self.ORDER_PRODUCTS_FULL_XPATH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[2]/div[3]/app-detalle-desplegable/div/div/div/div/ngb-accordion/div"
        
        self.testCases = []
        self.realResult = ""
        self.totalPrice = 0
        pdfHeader = ["Id","Product","Quantity","Observation","Expected Result"]
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
                self.productsPrices.append(productPrice.text)
                self.productsButtons.append(productButton)
            finally:
                index += 1


    def testAddOrderScreen(self):
        previousId = "CP1"
        indexOfXpath = 0
        for i in range(0, len(self.testCases)):

            if (previousId == self.testCases[i].id and (len(self.testCases)-1 != i)):
                indexOfXpath += 1
            else:
                self.deleteOrderToMakeNewOne(indexOfXpath)
                self.totalPrice = 0
                indexOfXpath = 1

            indexOfProduct = self.productsLabels.index(self.testCases[i].product)
            self.addProductToOrder(i, indexOfProduct)
            isTestOK = self.isProductAddedCorrectlyToOrder(i, indexOfXpath, indexOfProduct)
            isTestOK = self.CheckIfTotalPriceAndItemsCountAreCorrect(indexOfXpath, isTestOK)
            self.writeTestResultInFile(self.testCases[i], isTestOK)

            previousId = self.testCases[i].id
        

    def addProductToOrder(self, indexOfTestCase, indexOfProduct):
        QUANTITY_INPUT_FULL_XPATH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[1]/div[3]/div[2]/app-tablaproductos/app-modal-agregar-producto/div[2]/div/div/form/div[1]/div[2]/div[1]/atom-input/div/input"
        OBSERVATIONS_INPUT_FULL_XPATH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[1]/div[3]/div[2]/app-tablaproductos/app-modal-agregar-producto/div[2]/div/div/form/div[1]/div[2]/div[3]/textarea"
        ADD_TO_ORDER_BUTTON_FULL_XPATH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[1]/div[3]/div[2]/app-tablaproductos/app-modal-agregar-producto/div[2]/div/div/form/div[2]/atom-button/button"

        addProductButton = self.productsButtons[indexOfProduct]
        addProductButton.click()
        quantityInput = self.driver.find_element(by=By.XPATH, value=QUANTITY_INPUT_FULL_XPATH)
        observationsInput = self.driver.find_element(by=By.XPATH, value=OBSERVATIONS_INPUT_FULL_XPATH)
        addToOrderButton = self.driver.find_element(by=By.XPATH, value=ADD_TO_ORDER_BUTTON_FULL_XPATH)
        quantityInput.clear()
        quantityInput.send_keys(self.testCases[indexOfTestCase].quantity)
        observationsInput.send_keys(self.testCases[indexOfTestCase].observations)
        addToOrderButton.click()


    def isProductAddedCorrectlyToOrder(self,indexOfTestCase, indexOfXpath, indexOfProduct):
        LABEL_ORDER_PRODUCT_FULL_XPATH = "/div/button/p[1]/span"
        PRICE_ORDER_PRODUCT_FULL_XPATH = "/div/button/p[2]"
        QUANTITY_ORDER_PRODUCT_FULL_XPATH = "/div/button/p[1]/strong"

        orderProductLabel = self.driver.find_element(by=By.XPATH, value=self.ORDER_PRODUCTS_FULL_XPATH + "[" +str(indexOfXpath)  + "]" + LABEL_ORDER_PRODUCT_FULL_XPATH).text
        orderProductPrice = int(self.driver.find_element(by=By.XPATH, value=self.ORDER_PRODUCTS_FULL_XPATH + "[" +str(indexOfXpath)  + "]" + PRICE_ORDER_PRODUCT_FULL_XPATH).text[1:])
        orderProductQuantity = self.driver.find_element(by=By.XPATH, value=self.ORDER_PRODUCTS_FULL_XPATH + "[" +str(indexOfXpath)  + "]" + QUANTITY_ORDER_PRODUCT_FULL_XPATH).text
        self.totalPrice += orderProductPrice

        isTestOK = True
        self.realResult = "*Producto agregado al pedido" 
        if (self.productsLabels[indexOfProduct] != orderProductLabel):
            isTestOK = False
            self.realResult = "*Nombre incorrecto" 
        if (int(self.productsPrices[indexOfProduct][1:]) * int(self.testCases[indexOfTestCase].quantity)) !=  orderProductPrice:
            isTestOK = False
            self.realResult = "*Precio incorrecto"
        if (self.testCases[indexOfTestCase].quantity + " x  " != orderProductQuantity):
            isTestOK = False
            self.realResult = "*Cantidad incorrecta"
        return isTestOK


    def CheckIfTotalPriceAndItemsCountAreCorrect(self, indexOfXpath, isTestOK):
        TOTAL_LABEL_FULL_XPATH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[2]/div[4]/div/h6"
        ORDER_ITEMS_COUNT_LABEL_FULL_XPATH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[2]/div[2]/div/p"

        totalPriceLabel =  self.driver.find_element(by=By.XPATH, value=TOTAL_LABEL_FULL_XPATH).text.replace(".", "",1)
        indexOfComma = totalPriceLabel.find(",",9)
        totalPriceLabel = int(totalPriceLabel[9:indexOfComma])
        itemsCountLabel = self.driver.find_element(by=By.XPATH, value=ORDER_ITEMS_COUNT_LABEL_FULL_XPATH).text
        
        if self.totalPrice != totalPriceLabel:
            self.realResult = "*Precio total incorrecto"
            isTestOK = False
        if itemsCountLabel != "Items "+ str(indexOfXpath):
            self.realResult = "*Cantidad de items incorrecto"
            isTestOK = False
        return isTestOK


    def deleteOrderToMakeNewOne(self, indexOfXpath):
        PANEL_BUTTON_ORDER_FULL_XPATH = "/div/button"
        DELETE_PRODUCT_ORDER_FULL_XPATH = "/div[2]/div/div[2]/div/button[2]"
        
        for j in range(indexOfXpath, 0, -1):
            self.driver.find_element(by=By.XPATH, value=self.ORDER_PRODUCTS_FULL_XPATH + "[" +str(j)  + "]" + PANEL_BUTTON_ORDER_FULL_XPATH).click()
            self.driver.find_element(by=By.XPATH, value=self.ORDER_PRODUCTS_FULL_XPATH + "[" +str(j)  + "]" + DELETE_PRODUCT_ORDER_FULL_XPATH).click()


    def writeTestResultInFile(self, testCase, isTestOK):
        testCase = [
            testCase.id, 
            testCase.product, 
            testCase.quantity,
            testCase.observations,
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
