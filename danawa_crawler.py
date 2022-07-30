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

class DanawaCrawler:
    QUENTITY_PER_PAGE = 90 # 30 or 60 or 90
    TIMEOUT_LIMIT = 200
    CATEGORY_URL = {
        'CPU'	:'http://prod.danawa.com/list/?cate=112747',
        'RAM'	:'http://prod.danawa.com/list/?cate=112752',
        'VGA'	:'http://prod.danawa.com/list/?cate=112753',
        'MBoard'	:'http://prod.danawa.com/list/?cate=112751',
        'SSD'	:'http://prod.danawa.com/list/?cate=112760',
        'HDD'	:'http://prod.danawa.com/list/?cate=112763',
        'Power'	:'http://prod.danawa.com/list/?cate=112777',
        'Cooler'	:'http://prod.danawa.com/list/?cate=11236855',
        'Case'	:'http://prod.danawa.com/list/?cate=112775',
        'Monitor'	:'http://prod.danawa.com/list/?cate=112757',
        'Speaker'	:'http://prod.danawa.com/list/?cate=112808',
        'Headphone'	:'http://prod.danawa.com/list/?cate=113837',
        'Earphone'	:'http://prod.danawa.com/list/?cate=113838',
        'Headset'	:'http://prod.danawa.com/list/?cate=11225097',
        'Keyboard'	:'http://prod.danawa.com/list/?cate=112782',
        'Mouse'	:'http://prod.danawa.com/list/?cate=112787',
        'Laptop'	:'http://prod.danawa.com/list/?cate=112758',
    }
    DETAIL_PAGE_URL = 'https://prod.danawa.com/info/?pcode='
    SAVE_DIR = './danawa_crawling_data.h5'


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
        WebDriverWait(self.driver, self.TIMEOUT_LIMIT).until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))


    def crawling(self):
        print('Crawl primary keys')
        self.crawling_primary_key()
        # print('Crawl details')
        # self.crawling_detail()
        print('Crawl reviews')
        self.crawling_review()


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

            for page_num in tqdm(range(page_count), category_title):
                if page_num > 0 and page_num % 10 == 0:
                    product_list_area.find_element(By.XPATH, f'.//*[@class="edge_nav nav_next"]').click()
                    self.wait()
                WebDriverWait(self.driver, self.TIMEOUT_LIMIT).until(EC.visibility_of_element_located((By.XPATH, f'.//*[@class="number_wrap"]/*[{page_num % 10 + 1}]')))
                product_list_area.find_element(By.XPATH, f'.//*[@class="number_wrap"]/*[{page_num % 10 + 1}]').click()
                self.wait()
                
                products = product_list_area.find_elements(By.XPATH, './/*[@class="main_prodlist main_prodlist_list"]//*[@class="prod_pricelist "]/*[1]/*')
                for product in products:
                    id = product.get_property('id')
                    id_validator = re.match(r'^productInfoDetail_\d+$', id) is not None
                    if id_validator:
                        id = id[len('productInfoDetail_'):]
                    df.loc[id] = [id_validator]

            df.to_hdf(self.SAVE_DIR, f'{category_title}')


    def crawling_detail(self):
        for category_title in self.CATEGORY_URL.keys():
            indices = pd.read_hdf(self.SAVE_DIR, f'{category_title}')
            indices = indices.loc[indices['id_validator'] == True].index
            df = pd.DataFrame(index=indices)
            for idx in tqdm(indices, category_title):
                self.driver.get(self.DETAIL_PAGE_URL + idx)
                self.wait()

                # name crawling
                name = self.driver.find_element(By.XPATH, '//*[@class="top_summary"]/h3').text
                df.loc[idx, 'name'] = name

                # image crawling
                image = self.driver.find_element(By.XPATH, '//*[@id="baseImage"]').get_attribute('src')
                df.loc[idx, 'image'] = image

                # price crawling
                price_area = self.driver.find_elements(By.XPATH, '//*[@class="high_list"]/*[@class="lowest"]')
                if price_area:
                    price_area = price_area[0]
                    price = price_area.find_element(By.XPATH, '*[@class="price"]/*[1]/*[@class="txt_prc"]/*[1]').text
                    price = int(price.replace(',', ''))
                    shop_link = price_area.find_element(By.XPATH, '*[@class="mall"]/*[1]/*[1]').get_attribute('href')
                    shop_image = price_area.find_elements(By.XPATH, '*[@class="mall"]/*[1]/*[1]/*[1]')
                    df.loc[idx, 'price'] = price
                    df.loc[idx, 'shop_link'] = shop_link
                    if shop_image:
                        shop_image = shop_image[0]
                        shop_name = shop_image.get_attribute('alt')
                        shop_logo = shop_image.get_attribute('src')
                        df.loc[idx, 'shop_name'] = shop_name
                        df.loc[idx, 'shop_logo'] = shop_logo
                    else:
                        shop_name = price_area.find_element(By.XPATH, '*[@class="mall"]/*[1]/*[1]').get_attribute('title')
                        df.loc[idx, 'shop_name'] = shop_name

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
                            df.loc[idx, complete_key] = value
                        key = None
                        value = None

            df.to_hdf(self.SAVE_DIR, f'{category_title}_detail')


    def crawling_review(self):
        for category_title in self.CATEGORY_URL.keys():
            indices = pd.read_hdf(self.SAVE_DIR, f'{category_title}')
            indices = indices.loc[indices['id_validator'] == True].index
            df = pd.DataFrame(columns=['id', 'sentence', 'time', 'good', 'bad'])
            for idx in tqdm(indices, category_title):
                self.driver.get(self.DETAIL_PAGE_URL + idx)
                self.wait()

                filter_button_xpaths = []
                filter_button_xpaths.append('.//*[@id="danawa-prodBlog-productOpinion-button-leftMenu-23"]')
                filter_button_xpaths.append('.//*[@id="danawa-prodBlog-productOpinion-button-leftMenu-83"]')
                for filter_button_xpath in filter_button_xpaths:
                    WebDriverWait(self.driver, self.TIMEOUT_LIMIT).until(EC.visibility_of_element_located((By.XPATH, '//*[@class="danawa_review"]')))
                    review_area = self.driver.find_element(By.XPATH, '//*[@class="danawa_review"]')
                    review_area.find_element(By.XPATH, filter_button_xpath).click()
                    WebDriverWait(self.driver, self.TIMEOUT_LIMIT).until(EC.staleness_of(review_area))
                    review_area = self.driver.find_element(By.XPATH, '//*[@class="danawa_review"]')

                    while True:
                        page_count = len(review_area.find_elements(By.XPATH, './/*[@class="page_nav_area"]/*[2]/*'))
                        if page_count == 0:
                            break
                        for page_num in range(page_count):
                            if page_num > 0:
                                WebDriverWait(self.driver, self.TIMEOUT_LIMIT).until(EC.element_to_be_clickable((By.XPATH, f'.//*[@class="page_nav_area"]/*[2]/*[{page_num + 1}]')))
                                review_area.find_element(By.XPATH, f'.//*[@class="page_nav_area"]/*[2]/*[{page_num + 1}]').click()
                                WebDriverWait(self.driver, self.TIMEOUT_LIMIT).until(EC.staleness_of(review_area))
                                review_area = self.driver.find_element(By.XPATH, '//*[@class="danawa_review"]')

                            reviews = review_area.find_elements(By.XPATH, './/*[@class="cmt_list"]/*[@class="cmt_item"]')
                            for review in reviews:
                                sentence = review.find_element(By.XPATH, './/*[@class="danawa-prodBlog-productOpinion-clazz-content"]/input').get_attribute('value')
                                time = review.find_element(By.XPATH, './/*[@class="date"]').text
                                good = review.find_elements(By.XPATH, './/*[@class="btn_like"]/*[2]')
                                good = good[0].text if good else np.NaN
                                bad = review.find_elements(By.XPATH, './/*[@class="btn_dislike"]/*[2]')
                                bad = bad[0].text if bad else np.NaN
                                df.loc[len(df.index)] = [idx, sentence, time, good, bad]
                        next_button = review_area.find_element(By.XPATH, './/*[@class="page_nav_area"]/*[3]')
                        if next_button.get_attribute('class') == 'nav_edge nav_edge_next nav_edge_off':
                            break
                        next_button.click()
                        WebDriverWait(self.driver, self.TIMEOUT_LIMIT).until(EC.staleness_of(review_area))
                        review_area = self.driver.find_element(By.XPATH, '//*[@class="danawa_review"]')
                
            df.to_hdf(self.SAVE_DIR, f'{category_title}_review')


DanawaCrawler().crawling()

