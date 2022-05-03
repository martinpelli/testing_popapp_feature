from ast import Pass
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
            
        ORDER_ITEMS_COUNT_FULL_XPATH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[2]/div[2]/div/p"
        TOTAL_LABEL_FULL_XPATH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[2]/div[4]/div/h6"
        CONTINUE_BUTTON_FULL_XPATH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[2]/div[6]/atom-button/button"
        
        self.testCases = []
        self.realResult = ""
        pdfHeader = ["Id","Product","Quantity","Observation","Price","Expected Result"]
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


    def addProductsToOrder(self):

        QUANTITY_INPUT_FULL_XPATH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[1]/div[3]/div[2]/app-tablaproductos/app-modal-agregar-producto/div[2]/div/div/form/div[1]/div[2]/div[1]/atom-input/div/input"
        OBSERVATIONS_INPUT_FULL_XPATH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[1]/div[3]/div[2]/app-tablaproductos/app-modal-agregar-producto/div[2]/div/div/form/div[1]/div[2]/div[3]/textarea"
        ADD_TO_ORDER_BUTTON_FULL_XPATH = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[1]/div[3]/div[2]/app-tablaproductos/app-modal-agregar-producto/div[2]/div/div/form/div[2]/atom-button/button"

       
        productLabel = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[2]/div[3]/app-detalle-desplegable/div/div/div/div/ngb-accordion/div/div/button/p[1]/span"
        productPrice = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[2]/div[3]/app-detalle-desplegable/div/div/div/div/ngb-accordion/div/div/button/p[2]"
                            #/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[2]/div[3]/app-detalle-desplegable/div/div/div/div/ngb-accordion/div[1]/div/button/p[2]
                           # /html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[2]/div[3]/app-detalle-desplegable/div/div/div/div/ngb-accordion/div[2]/div/button/p[2]
        productQuantity = "/html/body/app-root/div[2]/app-crear-pedido/app-nuevo-pedido-desktop/div/div/div/div[2]/div[3]/app-detalle-desplegable/div/div/div/div/ngb-accordion/div/div/button/p[1]/strong"

        previousId = "CP1"


        for i in range(0, len(self.testCases)):
            if previousId == self.testCases[i].id:
                indexOfProduct = self.productsLabels.index(self.testCases[i].product)

                addProductButton = self.productsButtons[indexOfProduct]
                addProductButton.click()
                quantityInput = self.driver.find_element(by=By.XPATH, value=QUANTITY_INPUT_FULL_XPATH)
                observationsInput = self.driver.find_element(by=By.XPATH, value=OBSERVATIONS_INPUT_FULL_XPATH)
                addToOrderButton = self.driver.find_element(by=By.XPATH, value=ADD_TO_ORDER_BUTTON_FULL_XPATH)
                quantityInput.clear()
                quantityInput.send_keys(self.testCases[i].quantity)
                observationsInput.send_keys(self.testCases[i].observations)
                addToOrderButton.click()

            else:
                #comprobar items, total, precio, cantidad
                time.sleep(1000)
                print("aca termina el pedido")
            previousId = self.testCases[i].id



    def testAddOrderScreen(self):
        self.addProductsToOrder()
        #for testCase in self.testCases:
            


    def tearDown(self):
        fileName = 'AddOrderScreenTestCasesResults.pdf'
        pathToSaveFile = '/home/pelli/Documents/Popapp/data/'
        title = 'Add Order Screen Automated Tests'
        testerName = 'Martín Pellicer'
        self.pdfWriter.writeToPDF(fileName, pathToSaveFile, title, testerName)


if __name__ == "__main__":
    unittest.main()        
