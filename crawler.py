from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

options = ChromeOptions()
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options = options)
driver.get('file:///D:/Coding/crawling/myhtml.html')

title = driver.title
current_url = driver.current_url
print('*'*18)
print(title, current_url)

vegetable = driver.find_element(By.CLASS_NAME, "apples")

print(vegetable.text)

driver.quit()