import sqlite3
import threading
import time
from itertools import permutations

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

client_inp = input("Enter name: ")
if not client_inp or len(client_inp) > 4:
    exit()


def get_data(client_inp):
    driver = webdriver.Chrome('./chromedriver')

    driver.get('https://allo.ua/ru/')
    driver.wait = WebDriverWait(driver, 5)
    print(client_inp)
    conn = sqlite3.connect('fist', check_same_thread=False)
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS allo(id INTEGER PRIMARY KEY AUTOINCREMENT, name text, link text, varification text)"
    )
    try:
        driver.wait.until(EC.presence_of_element_located(
            (By.ID, "search-form__input")))
        z = driver.find_element_by_id("search-form__input")
        z.send_keys(client_inp)
        z.click()
    except:
        time.sleep(3)
        driver.wait.until(EC.presence_of_element_located(
            (By.ID, "search-form__input")))
        z = driver.find_element_by_id("search-form__input")
        z.send_keys(client_inp)
        z.click()
    try:
        driver.wait.until(EC.presence_of_element_located(
            (By.CLASS_NAME, "search-result__content")))
    except:
        print('Looks like nothing founded')
        return None
    html = driver.page_source
    try:

        soup = BeautifulSoup(html, "html.parser")

        head = soup.find('div', class_='search-result__content')
    except Exception as err:
        print(f'Not found {client_inp}')
        return None

    heads = {}
    for i in head.find_all('ul'):
        for z in i.find_all('a'):
            heads[z.get('title')] = z.get('href')
    print(heads)
    for key, value in heads.items():
        cur.execute(f"INSERT INTO allo (name, link, varification) VALUES('{key}', '{value}', 'True')")
    driver.close()
    conn.commit()
    conn.close()


# driver.close()


def main():
    words = []
    for x in list(permutations(client_inp, r=len(client_inp))):
        words.append(''.join(x))
    for word in words:
        x = threading.Thread(target=get_data, args=(word,))
        x.start()


if __name__ == '__main__':
    try:
        main()
    except:
        print('err')
