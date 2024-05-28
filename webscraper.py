import os
import time
import random
from dotenv import load_dotenv
# from fake_useragent import UserAgent
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# ua = UserAgent()
load_dotenv()


class Scraper:

    @staticmethod
    def send_telegram_notification(message):
        chat_id = os.environ.get('MY_CHAT_ID')
        token = os.environ.get('TELEGRAM_TOKEN')
        message = message
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}"
        print(requests.get(url).json())

    def __init__(self):
        # self.embassy_link = os.getenv('italian_embassy_link')
        # self.login = os.getenv('login')
        # self.password = os.getenv('password')
        # self.user_agent = os.getenv('user_agent')
        self.embassy_link = os.environ.get('italian_embassy_link')
        self.login = os.environ.get('login')
        self.password = os.environ.get('password')
        self.user_agent = os.environ.get('user_agent')
        self.driver = None
        self.options = None

    def run_the_webdriver(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--headless=new')
        self.options.add_argument(f'user-agent={self.user_agent}')
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--window-size=1420,1080')
        self.options.add_argument('--disable-gpu')

        self.options.add_argument('--disable-dev-shm-usage')
        self.options.add_argument('--start-maximized')
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.options.add_experimental_option("useAutomationExtension", False)

        self.driver = webdriver.Chrome(options=self.options)
        self.driver.delete_all_cookies()
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.driver.get(self.embassy_link)


    def authentication(self):
        # message = 'Начало авторизации!'
        # self.send_telegram_notification(message=message)
        WebDriverWait(self.driver, 10)
        login_element = self.driver.find_element("id", "login-email")
        login_element.send_keys(self.login)
        time.sleep(random.randint(2,5))
        password_element = self.driver.find_element("id", "login-password")
        password_element.send_keys(self.password)
        time.sleep(random.randint(2,5))
        click_button = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button.primary.g-recaptcha[data-callback='onSubmit']")))
        click_button.click()

    def find_the_book_section(self):
        # message = 'Поиск раздела с ссылками на бронь'
        # self.send_telegram_notification(message=message)
        # self.send_telegram_notification(message=self.driver.current_url)
        print(self.driver.current_url)
        try:
            time.sleep(random.randint(2,5))
            book = self.driver.find_element("id", "advanced")
            book.click()
        except NoSuchElementException:
            message = 'Авторизация неуспешная! Внутренняя ошибка!'
            self.send_telegram_notification(message=message)

    def check_free_registrations(self):
        time.sleep(random.randint(4, 10))
        print(self.driver.current_url)
        try:
            book_links = self.driver.find_element(By.XPATH, '//*[@id="dataTableServices"]/tbody')
            time.sleep(random.randint(1,3))
            touristic_link = book_links.find_element(By.XPATH, '//*[@id="dataTableServices"]/tbody/tr[4]/td[4]')
            touristic_link.click()
        except NoSuchElementException:
            message = 'Ссылка не найдена!'
            self.send_telegram_notification(message=message)

    def get_the_message(self):
        time.sleep(random.randint(4,8))
        try:
            message = self.driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div/div/div/div/div/div/div/div[3]")
            self.send_telegram_notification(message=message.text)
        except NoSuchElementException:
            message = 'Сообщение об отсутствии слотов не найдено! \nВозможно, появилось окно на запись'
            self.send_telegram_notification(message=message)
        if self.driver.current_url != 'https://prenotami.esteri.it/Services':
            message = 'Произошел переход по другой ссылке в окно \nзаписи на туристическую визу!'
            self.send_telegram_notification(message=message)

    def run_the_scraper(self):
        self.run_the_webdriver()
        self.authentication()
        self.find_the_book_section()
        self.check_free_registrations()
        self.get_the_message()

# https://prenotami.esteri.it/Services


