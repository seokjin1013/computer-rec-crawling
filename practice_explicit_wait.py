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
driver.get('file:///D:/Coding/crawling/practice_explicit_wait.html')
# Explicit wait
WebDriverWait(driver, timeout=10).until(lambda driver: driver.execute_script("return completed"))
print('Crawling start')
element = driver.find_element(By.TAG_NAME, 'p')
print(element.text)
print('Crawling end')

driver.quit()