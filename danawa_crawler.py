from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
import pandas as pd
import re

class DanawaCrawler:
    QUENTITY_PER_PAGE = 90 # 30 or 60 or 90
    PAGE_NUM = 10
    CATEGORY_URL = {
        # 'CPU'	:'http://prod.danawa.com/list/?cate=112747',
        # 'RAM'	:'http://prod.danawa.com/list/?cate=112752',
        # 'VGA'	:'http://prod.danawa.com/list/?cate=112753',
        # 'MBoard'	:'http://prod.danawa.com/list/?cate=112751',
        'SSD'	:'http://prod.danawa.com/list/?cate=112760',
        # 'HDD'	:'http://prod.danawa.com/list/?cate=112763',
        # 'Power'	:'http://prod.danawa.com/list/?cate=112777',
        # 'Cooler'	:'http://prod.danawa.com/list/?cate=11236855',
        # 'Case'	:'http://prod.danawa.com/list/?cate=112775',
        # 'Monitor'	:'http://prod.danawa.com/list/?cate=112757',
        # 'Speaker'	:'http://prod.danawa.com/list/?cate=112808',
        # 'Headphone'	:'http://prod.danawa.com/list/?cate=113837',
        # 'Earphone'	:'http://prod.danawa.com/list/?cate=113838',
        # 'Headset'	:'http://prod.danawa.com/list/?cate=11225097',
        # 'Keyboard'	:'http://prod.danawa.com/list/?cate=112782',
        # 'Mouse'	:'http://prod.danawa.com/list/?cate=112787',
        # 'Laptop'	:'http://prod.danawa.com/list/?cate=112758',
    }
    DETAIL_PAGE_URL = 'https://prod.danawa.com/info/?pcode='


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
        WebDriverWait(self.driver, 10).until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))


    def crawling(self):
        # self.crawling_primary_key()
        self.crawling_details()


    def crawling_primary_key(self):
        for category_title, category_link in self.CATEGORY_URL.items():
            df = pd.DataFrame(columns=['id', 'id_validator'])
            df.set_index('id', inplace=True)

            self.driver.get(category_link)
            self.wait()

            product_list_area = self.driver.find_element(By.XPATH, '//*[@id="productListArea"]')
            qnt_selector = product_list_area.find_element(By.XPATH, './/select[@class="qnt_selector"]')
            qnt_selector = Select(qnt_selector)
            qnt_selector.select_by_value(str(self.QUENTITY_PER_PAGE))
            self.wait()
            product_count = product_list_area.find_element(By.XPATH, './/*[@id="totalProductCount"]')
            product_count = product_count.get_property('value')
            product_count = int(product_count.replace(',', ''))
            page_count = (product_count + self.QUENTITY_PER_PAGE - 1) // self.QUENTITY_PER_PAGE

            for page_num in range(page_count):
                if page_num > 0 and page_num % 10 == 0:
                    product_list_area.find_element(By.XPATH, f'.//*[@class="edge_nav nav_next"]').click()
                    self.wait()
                product_list_area.find_element(By.XPATH, f'.//*[@class="number_wrap"]/*[{page_num % self.PAGE_NUM + 1}]').click()
                self.wait()
                
                products = product_list_area.find_elements(By.XPATH, './/*[@class="main_prodlist main_prodlist_list"]//*[@class="prod_pricelist "]/*[1]/*')
                for product in products:
                    id = product.get_property('id')
                    id_validator = re.match(r'^productInfoDetail_\d+$', id) is not None
                    if id_validator:
                        id = id[len('productInfoDetail_'):]
                    df.loc[id] = [id_validator]
                break
            df.columns = pd.MultiIndex.from_product([['basic'], df.columns])
            df.to_pickle(f'{category_title}.pkl')


    def crawling_details(self):
        for category_title in self.CATEGORY_URL.keys():
            df = pd.read_pickle(f'{category_title}.pkl')
            for idx in df.loc[df[('basic', 'id_validator')] == True].index:
                self.driver.get(self.DETAIL_PAGE_URL + idx)
                self.wait()

                # price crawling
                price = self.driver.find_element(By.XPATH, '//*[@id="intMinFee"]').get_property('value')
                price = int(price.replace(',', ''))
                df.loc[idx, ('basic', 'price')] = price

                # spec crawling
                spec_area = self.driver.find_elements(By.XPATH, '//*[@class="spec_tbl"]/tbody/*/*')
                division = ''
                key = None
                value = None
                for element in spec_area:
                    if element.get_attribute('class') == 'tit':
                        key = element.text
                    elif element.get_attribute('class') == 'dsc':
                        value = element.text
                    else:
                        division = element.text
                    if key != None and value != None:
                        if key != '':
                            complete_key = division + key
                            df.loc[idx, ('spec', complete_key)] = value
                            print(complete_key, value)
                        key = None
                        value = None

                # review crawling
                
                break
            
            df.to_pickle(f'{category_title}2.pkl')


DanawaCrawler().crawling()

