from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

options = ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get('https://prod.danawa.com/info/?pcode=13190519')

print('Crawling start')
review_area = driver.find_element(By.XPATH, '//*[@class="danawa_review"]')
button = review_area.find_element(By.XPATH, '//*[@class="rdo_tab"]/*[2]/*[1]')
button.send_keys(Keys.ENTER)
print(button.tag_name, button.text)
print('Crawling end')
import time
time.sleep(100)
driver.quit()