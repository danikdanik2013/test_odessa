import time
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations_with_replacement
import string
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from before_start import check
from config import RANGE
from config import THREADS_COUNT
from utils.sql import connect_to_db
from utils.сhrome import start_chrome


class Selenium:
    def __init__(self, client_inp, count):
        self.client = client_inp
        self.count = count

    @staticmethod
    def parse_page(driver):
        """
        Parsing function for html template
        :param driver: chrome env for emulation browser
        :return: data with div
        """
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        head = soup.find('div', class_='search-result__content')
        return head

    @staticmethod
    def parse_data(head):
        """
        Function for parsing data in page
        :param head: data about page
        :return: dict with data
        """
        heads = {}
        for i in head.find_all('ul'):
            for z in i.find_all('a'):
                heads[z.get('title')] = z.get('href')
        return heads

    def upload_data(self, cur, heads: dict):
        """
        Function for uploading data into database
        :param cur: sqlite cursor
        :param heads: dict with data
        :return:
        """
        for key, value in heads.items():
            cur.execute(
                f"INSERT INTO allo (name, link, varification, counter) VALUES('{key}', '{value}', 'True', '{self.count}')")

    def get_data(self):
        driver = start_chrome()
        cur, conn = connect_to_db()
        try:
            driver.wait.until(EC.presence_of_element_located(
                (By.ID, "search-form__input")))
            z = driver.find_element_by_id("search-form__input")
            z.send_keys(self.client)
            z.click()
        except:
            # if browser have some delay
            time.sleep(3)
            driver.wait.until(EC.presence_of_element_located(
                (By.ID, "search-form__input")))
            z = driver.find_element_by_id("search-form__input")
            z.send_keys(self.client)
            z.click()
        try:
            driver.wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "search-result__content")))
            head = self.parse_page(driver=driver)
        except Exception as e:
            print('Looks like nothing founded')
            return None

        heads = self.parse_data(head=head)
        self.upload_data(cur=cur, heads=heads)
        print(f'published {self.client} to the database')
        driver.close()
        conn.commit()
        conn.close()


def input_check(client_input: str):
    """
    Validation for input
    :param client_input: input from form
    :return: None
    """
    if not client_input.isdigit() or int(client_input) not in range(1, 3):
        print('Invalid value')
        exit()



def main():
    check()
    count = 0
    client_inp = input("Continue or new. 1 or 2: ")
    words = []
    for x in list(combinations_with_replacement(string.ascii_lowercase, r=RANGE)):
        words.append(''.join(x))
    cur, conn = connect_to_db()
    input_check(client_input=client_inp)
    if int(client_inp) == 1:
        cur.execute("SELECT counter FROM allo ORDER BY id DESC LIMIT 1")
        last = [int(record[0]) for record in cur.fetchall()][0]
        if last:
            words = words[last:]
        count = last
    cur.execute(
        "CREATE TABLE IF NOT EXISTS allo(id INTEGER PRIMARY KEY AUTOINCREMENT, name text, link text, varification text, counter INTEGER)"
    )
    with ThreadPoolExecutor(max_workers=THREADS_COUNT) as executor:
        for word in words:
            count += 1
            sel = Selenium(word, count)
            executor.submit(sel.get_data)


if __name__ == '__main__':
    try:
        main()
    except:
        print('Exit from programm')
