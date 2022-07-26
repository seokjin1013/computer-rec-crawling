from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

options = ChromeOptions()
options.add_argument('--start-maximized')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.get('file:///D:/Coding/crawling/practice_xpath2.html')

print('Crawling start')
element = driver.find_element(By.XPATH, 'html/body/div[3]/*[1]')
print(element.text)
print('Crawling end')

driver.quit()