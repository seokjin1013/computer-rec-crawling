from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

options = ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://prod.danawa.com/info/?pcode=16756757')

print('Crawling start')
element = driver.find_element(By.ID, 'space space')
print(element.text)
element = driver.find_element(By.ID, 'nonspace')
print(element.text)
# element = driver.find_element(By.CLASS_NAME, 'space space')
# print(element.text)
element = driver.find_element(By.CLASS_NAME, 'nonspace')
print(element.text)
# element = driver.find_element(By.CSS_SELECTOR, '#space space')
# print(element.text)
element = driver.find_element(By.CSS_SELECTOR, '#nonspace')
print(element.text)
# element = driver.find_element(By.CSS_SELECTOR, '.space space')
# print(element.text)
element = driver.find_element(By.CSS_SELECTOR, '.nonspace')
print(element.text)
element = driver.find_element(By.XPATH, "//*[@id='space space']")
print(element.text)
element = driver.find_element(By.XPATH, "//*[@id='nonspace']")
print(element.text)
element = driver.find_element(By.XPATH, "//*[@class='space space']")
print(element.text)
element = driver.find_element(By.XPATH, "//*[@class='nonspace']")
print(element.text)
print('Crawling end')

driver.quit()