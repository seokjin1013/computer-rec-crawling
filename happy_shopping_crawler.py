from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
import pandas as pd
import numpy as np
import re
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
    def get_url_tail(self, idx):
        return f'/srch/total/list/{idx}/rank/{self.QUENTITY_PER_PAGE}/null'


    def __init__(self):
        assert self.QUENTITY_PER_PAGE in [30, 60, 90]
        options = ChromeOptions()
        options.add_argument('--start-maximized')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        service = ChromeService(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=options)


    def __del__(self):
        self.driver.quit()


    def wait(self):
        WebDriverWait(self.driver, self.TIMEOUT_LIMIT).until(EC.invisibility_of_element((By.CLASS_NAME, 'sc-fzqBkg fCkJVF')))

    
    def scroll_down(self):
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')


    def crawling(self):
        for category_title, category_link in self.CATEGORY_URL.items():
            df = pd.DataFrame(columns=['id', 'name', 'price'])
            df.set_index('id', inplace=True)

            self.driver.get(category_link)
            self.wait()
            WebDriverWait(self.driver, self.TIMEOUT_LIMIT).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="sc-AxmLO gmtmqV"]//*[@class="num"]')))
            product_count = int(self.driver.find_element(By.XPATH, '//*[@class="sc-AxmLO gmtmqV"]//*[@class="num"]').text)
            page_count = (product_count + self.QUENTITY_PER_PAGE - 1) // self.QUENTITY_PER_PAGE
            
            for page_num in tqdm(range(page_count), category_title):
                self.driver.get(category_link + self.get_url_tail(page_num + 1))
                self.wait()
                mid_ad = self.driver.find_elements(By.XPATH, '//*[@class="sc-fznWOq iUFflb"]')
                if mid_ad:
                    self.scroll_down()
                    WebDriverWait(self.driver, self.TIMEOUT_LIMIT).until(lambda _ : len(self.driver.find_elements(By.XPATH, '//*[@class="sc-fznWOq jImGKC item_wrap"]')) == 2)
                products = self.driver.find_elements(By.XPATH, '//*[@class="sc-fznWOq jImGKC item_wrap"]/*[@class="sc-fzoLag BNtsP item  list"]')
                for product in products:
                    id = product.find_element(By.XPATH, './/*[@class="title"]/a').get_property('href')
                    id = int(id[id.rfind('/') + 1:])
                    name = product.find_element(By.XPATH, './/*[@class="title"]').text
                    price = product.find_elements(By.XPATH, './/*[@class="price"]/*[@class="num"]')
                    price = int(price[0].text.replace(',', '')) if price else np.NaN
                    df.loc[id] = [name, price]

            df.to_hdf(self.SAVE_DIR, f'{category_title}')


HappyShoppingCrawler().crawling()

