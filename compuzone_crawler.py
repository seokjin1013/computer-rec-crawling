from typing import Union
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeDriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchWindowException
import pandas as pd
import numpy as np
from tqdm import tqdm

class CompuzoneCrawler:
    TIMEOUT_LIMIT = 200
    CATEGORY_URL = {
        'CPU'	:'https://www.compuzone.co.kr/product/product_list.htm?BigDivNo=4&MediumDivNo=1012&PageCount=9999999',
        'MBoard'	:'https://www.compuzone.co.kr/product/product_list.htm?BigDivNo=4&MediumDivNo=1013&PageCount=9999999',
        'RAM'	:'https://www.compuzone.co.kr/product/product_list.htm?BigDivNo=4&MediumDivNo=1014&PageCount=9999999',
        'SSD'	:'https://www.compuzone.co.kr/product/product_list.htm?BigDivNo=4&MediumDivNo=1276&PageCount=9999999',
        'HDD'	:'https://www.compuzone.co.kr/product/product_list.htm?BigDivNo=4&MediumDivNo=1015&PageCount=9999999',
        'VGA'	:'https://www.compuzone.co.kr/product/product_list.htm?BigDivNo=4&MediumDivNo=1016&PageCount=9999999',
        'ODD'	:'https://www.compuzone.co.kr/product/product_list.htm?BigDivNo=4&MediumDivNo=1017&PageCount=9999999',
        'Case'	:'https://www.compuzone.co.kr/product/product_list.htm?BigDivNo=4&MediumDivNo=1147&PageCount=9999999',
        'Power'	:'https://www.compuzone.co.kr/product/product_list.htm?BigDivNo=4&MediumDivNo=1148&PageCount=9999999',
        'Cooler'	:'https://www.compuzone.co.kr/product/product_list.htm?BigDivNo=4&MediumDivNo=1020&PageCount=9999999',
        'DSP'	:'https://www.compuzone.co.kr/product/product_list.htm?BigDivNo=4&MediumDivNo=1199&PageCount=9999999',
        'CLC'	:'https://www.compuzone.co.kr/product/product_list.htm?BigDivNo=4&MediumDivNo=1289&PageCount=9999999',
    }
    DETAIL_PAGE_URL = 'https://www.compuzone.co.kr/product/product_detail.htm?ProductNo='
    SAVE_DIR = './compuzone_crawling_data.h5'
    SAVE_INTERVAL = 90


    def __init__(self):
        options = ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-setuid-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        service = ChromeService(ChromeDriverManager().install())
        self.driver = ChromeDriver(service=service, options=options)


    def __del__(self):
        self.driver.quit()

    
    def find_element_or_wait(self, element : Union[WebDriver, WebElement], xpath):
        WebDriverWait(element, self.TIMEOUT_LIMIT).until(EC.visibility_of_element_located((By.XPATH, xpath)))
        return element.find_element(By.XPATH, xpath)


    def find_element_or_none(self, element : Union[WebDriver, WebElement], xpath):
        ret = element.find_elements(By.XPATH, xpath)
        return ret[0] if ret else None


    def scroll_down(self):
        product_area = self.find_element_or_wait(self.driver, '//*[@id="product_list_ul"]')
        while not self.find_element_or_none(product_area, '*[@id="IsMaxPageing"]'):
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')


    def crawling(self):
        for category_title, category_link in self.CATEGORY_URL.items():
            df = pd.DataFrame(columns=['id', 'name', 'price'])
            df.set_index('id', inplace=True)
            df.to_hdf(self.SAVE_DIR, category_title)

            progress = 0
            while True:
                df = pd.read_hdf(self.SAVE_DIR, category_title)
                try:
                    self.driver.get(category_link)
                    self.scroll_down()
                    products = self.driver.find_elements(By.XPATH, '//*[@id="product_list_ul"]/li')
                    for prod_num in tqdm(range(progress, len(products)), category_title, initial=progress, total=len(products)):
                        product = products[prod_num]
                        id = product.find_element(By.XPATH, '*[@pno]').get_attribute('pno')
                        name = product.find_element(By.XPATH, './/*[@class="prd_info_name prdTxt"]').text
                        price = self.find_element_or_none(product, './/*[@class="right_bx"]/*[@class="prd_price"]')
                        price = int(price.get_attribute('data-price').replace(',', '')) if price else np.NaN
                        df.loc[id] = [name, price]

                        if (prod_num + 1) % self.SAVE_INTERVAL == 0 or (prod_num + 1) == len(products):
                            df.to_hdf(self.SAVE_DIR, category_title)
                            progress = prod_num + 1

                except NoSuchWindowException:
                    print('Window already closed')
                    print(f'Current page is {progress}')
                    exit(-1)
                except Exception as e:
                    print(e)
                    print(f'Restart from {progress} page')
                else:
                    df.to_hdf(self.SAVE_DIR, category_title)
                    break


CompuzoneCrawler().crawling()

