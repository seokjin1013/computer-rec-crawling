from math import ceil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select

class DanawaCrawler:
    QUENTITY_PER_PAGE = '90' # 30 or 60 or 90
    PAGE_NUM = 10
    CATEGORY = {
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


    def __init__(self):
        assert self.QUENTITY_PER_PAGE in '30 60 90'.split()
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
        for category_title, category_link in self.CATEGORY.items():
            self.driver.get(category_link)
            self.wait()

            product_code = []
            product_list_area = self.driver.find_element(By.XPATH, '//*[@id="productListArea"]')
            qnt_selector = Select(product_list_area.find_element(By.XPATH, './/select[@class="qnt_selector"]'))
            qnt_selector.select_by_value(self.QUENTITY_PER_PAGE)
            self.wait()
            product_count = product_list_area.find_element(By.XPATH, './/*[@id="totalProductCount"]').get_property('value')
            product_count = int(product_count.replace(',', ''))
            page_count = (product_count + int(self.QUENTITY_PER_PAGE) - 1) // int(self.QUENTITY_PER_PAGE)
            for page_num in range(page_count):
                if page_num > 0 and page_num % 10 == 0:
                    product_list_area.find_element(By.XPATH, f'.//*[@class="edge_nav nav_next"]').click()
                    self.wait()
                product_list_area.find_element(By.XPATH, f'.//*[@class="number_wrap"]/*[{page_num % self.PAGE_NUM + 1}]').click()
                self.wait()
                product_code += product_list_area.find_element(By.XPATH, './/*[@id="productCodeListForContent"]').get_property('value').split(',')
            product_code = list(map(int, product_code))

            with open(f'./{category_title}.txt', 'w') as f:
                f.write(str(product_code))

DanawaCrawler().crawling()

