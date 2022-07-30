from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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


    def __init__(self):
        options = ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)


    def __del__(self):
        self.driver.quit()


    def scroll_down(self):
        WebDriverWait(self.driver, self.TIMEOUT_LIMIT).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="product_list_ul"]')))
        product_area = self.driver.find_element(By.XPATH, '//*[@id="product_list_ul"]')
        while True:
            isMaxPaging = product_area.find_elements(By.XPATH, '*[@id="IsMaxPageing"]')
            if isMaxPaging:
                break
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')


    def crawling(self):
        for category_title, category_link in self.CATEGORY_URL.items():
            df = pd.DataFrame(columns=['id', 'name', 'price'])
            df.set_index('id', inplace=True)

            self.driver.get(category_link)

            self.scroll_down()
            products = self.driver.find_elements(By.XPATH, '//*[@id="product_list_ul"]/li')
            for product in tqdm(products, category_title):
                id = product.find_element(By.XPATH, '*[@pno]').get_attribute('pno')
                name = product.find_element(By.XPATH, './/*[@class="prd_info_name prdTxt"]').text
                price = product.find_elements(By.XPATH, './/*[@class="right_bx"]/*[@class="prd_price"]')
                price = int(price[0].get_attribute('data-price').replace(',', '')) if price else np.NaN
                df.loc[id] = [name, price]

            df.to_hdf(self.SAVE_DIR, f'{category_title}')


CompuzoneCrawler().crawling()

