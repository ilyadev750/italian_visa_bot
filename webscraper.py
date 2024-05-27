import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


load_dotenv()


class Scraper:

    def __init__(self):
        self.embassy_link = os.getenv('italian_embassy_link')
        self.login = os.getenv('login')
        self.password = os.getenv('password')
        self.driver = None
        self.options = None

    def run_the_webdriver(self):
        self.options = webdriver.ChromeOptions()
        user_agent = os.getenv('user_agent')
        self.options.add_argument('--headless=new')
        self.options.add_argument(f'user-agent={user_agent}')
        self.driver = webdriver.Chrome(options=self.options)
        self.driver.get(self.embassy_link)
        self.driver.maximize_window()

    def authentication(self):
        WebDriverWait(self.driver, 10)
        login_element = self.driver.find_element("id", "login-email")
        login_element.send_keys(self.login)
        password_element = self.driver.find_element("id", "login-password")
        password_element.send_keys(self.password)
        click_button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.primary.g-recaptcha[data-callback='onSubmit']")))
       
        # if login_element:
        #     print('True 1')
        # if password_element:
        #     print('True 2')
        # if click_button:
        #     print('True 3')

        click_button.click()

    def find_the_book_button(self):
        print(self.driver.current_url)
        book = self.driver.find_element("id", "advanced")
        if book:
            book.click()
            print('Element is found!')
            print(self.driver.current_url)

    def run_the_scraper(self):
        self.run_the_webdriver()
        self.authentication()
        self.find_the_book_button()


if __name__ == "__main__":
    scraper = Scraper()
    scraper.run_the_scraper()
    scraper.driver.quit()

