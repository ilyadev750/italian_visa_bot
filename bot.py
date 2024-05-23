from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time


options = webdriver.ChromeOptions()
options.add_argument('--headless=new')
driver = webdriver.Chrome(options=options)


driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element(By.NAME, "q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
print('SUCCESS')
driver.close()