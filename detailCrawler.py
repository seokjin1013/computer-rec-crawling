from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://prod.danawa.com/info/?pcode=16756757')
WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.CLASS_NAME, 'product_list_cover')))

print('Crawling start')
element = driver.find_element(By.XPATH, '//*[@class="spec_tbl"]/tbody')
print(element.text)
print('Crawling end')

driver.quit()