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

driver.get('file:///D:/Coding/crawling/practice_xpath.html')

print('Crawling start')
element = driver.find_elements(By.XPATH, 'html/body/div[1]')
for e in element:
    print(e.text)
print('Crawling end')

driver.quit()