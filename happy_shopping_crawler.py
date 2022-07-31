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
import pandas as pd
import numpy as np
from tqdm import tqdm

class HappyShoppingCrawler:
    QUENTITY_PER_PAGE = 90 # 30 or 60 or 90
    TIMEOUT_LIMIT = 200
    CATEGORY_URL = {
        'CPU'	:'https://shopping.pping.kr/list/1010100000',
        'MBoard'	:'https://shopping.pping.kr/list/1010200000',
        'RAM'	:'https://shopping.pping.kr/list/1010300000',
        'VGA'	:'https://shopping.pping.kr/list/1010600000',
        'SSD'	:'https://shopping.pping.kr/list/1010500000',
        'HDD'	:'https://shopping.pping.kr/list/1010400000',
        'Case'	:'https://shopping.pping.kr/list/1010800000',
        'Power'	:'https://shopping.pping.kr/list/1010900000',
        'Cooler'	:'https://shopping.pping.kr/list/1011000000',
        'Keyboard'	:'https://shopping.pping.kr/list/1011100000',
        'Mouse'	:'https://shopping.pping.kr/list/1011200000',
    }
    DETAIL_PAGE_URL = 'https://shopping.pping.kr/detail/'
    SAVE_DIR = './happy_shopping_crawling_data.h5'
    SAVE_INTERVAL = 5


    def get_url_tail(self, idx):
        return f'/srch/total/list/{idx}/rank/{self.QUENTITY_PER_PAGE}/null'


    def __init__(self):
        assert self.QUENTITY_PER_PAGE in [30, 60, 90]
        options = ChromeOptions()
        options.add_argument('--start-maximized')
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
        product_area = self.find_element_or_wait(self.driver, '//*[@class="sc-fznMAR gSVBBi"]')
        while True:
            child_count = len(product_area.find_elements(By.XPATH, '*'))
            if product_area.find_element(By.XPATH, f'*[{child_count}]').get_attribute('class') == 'sc-fznWOq jImGKC item_wrap':
                break
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')        


    def crawling(self):
        for category_title, category_link in self.CATEGORY_URL.items():
            df = pd.DataFrame(columns=['id', 'name', 'price'])
            df.set_index('id', inplace=True)
            df.to_hdf(self.SAVE_DIR, category_title)

            progress = 0
            while True:
                df = pd.read_hdf(self.SAVE_DIR, category_title)
                self.driver.get(category_link)
                try:
                    product_count = int(self.find_element_or_wait(self.driver, '//*[@class="sc-AxmLO gmtmqV"]//*[@class="num"]').text)
                    page_count = (product_count + self.QUENTITY_PER_PAGE - 1) // self.QUENTITY_PER_PAGE
                    
                    for page_num in tqdm(range(progress, page_count), category_title, initial=progress, total=page_count):
                        self.driver.get(category_link + self.get_url_tail(page_num + 1))
                        self.scroll_down()
                        products = self.driver.find_elements(By.XPATH, '//*[@class="sc-fznWOq jImGKC item_wrap"]/*[@class="sc-fzoLag BNtsP item  list"]')
                        for product in products:
                            id = product.find_element(By.XPATH, './/*[@class="title"]/a').get_property('href')
                            id = int(id[id.rfind('/') + 1:])
                            name = product.find_element(By.XPATH, './/*[@class="title"]').text
                            price = self.find_element_or_none(product, './/*[@class="price"]/*[@class="num"]')
                            price = int(price.text.replace(',', '')) if price else np.NaN
                            df.loc[id] = [name, price]

                        if (page_num + 1) % self.SAVE_INTERVAL == 0 or (page_num + 1) == page_count:
                            df.to_hdf(self.SAVE_DIR, f'{category_title}')
                            progress = page_num + 1

                except Exception as e:
                    print(e)
                    print(f'Restart from {progress} page')
                else:
                    df.to_hdf(self.SAVE_DIR, f'{category_title}')
                    break



HappyShoppingCrawler().crawling()