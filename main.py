from webscraper import Scraper

import time

if __name__ == "__main__":
    while True:
        scraper = Scraper()
        scraper.run_the_scraper()
        scraper.driver.quit()
        time.sleep(600)
