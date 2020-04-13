from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait


def start_chrome():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome('./chromedriver', options=chrome_options)

    driver.get('https://allo.ua/ru/')
    driver.wait = WebDriverWait(driver, 5)
    return driver
