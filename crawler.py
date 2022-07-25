from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = ChromeOptions()
options.add_argument('--start-maximized')
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://prod.danawa.com/list/?cate=112747')
# driver.get('file:///D:/Coding/crawling/myhtml.html')

# WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))
driver.implicitly_wait(3)
# prodlist = driver.find_element(By.CLASS_NAME, 'main_prodlist main_prodlist_list').get_attribute()

print('Crawling start')
# element = driver.find_element(By.CLASS_NAME, 'main_prodlist main_prodlist_list')
# element = driver.find_element(By.CSS_SELECTOR, " .main_prodlist main_prodlist_list")
element = driver.find_element(By.XPATH, '//div[@class="main_prodlist main_prodlist_list"]')
print(element.text)
print('Crawling end')

driver.quit()