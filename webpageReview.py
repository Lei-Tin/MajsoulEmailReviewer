"""
This file will be responsible to emulate a browser and run the User Script to download the file
"""
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from config import *

USER_DATA_DIR = '/Users/leit/Library/Application Support/Google/Chrome/Default'
LINK = 'https://game.maj-soul.com/1/?paipu=220607-7cd9be85-a5b8-4158-a4ca-e7bfacd166c5_a9330108'


def review_log(link: str) -> None:
    """Downloads the json file for the log"""
    # Start Chrome driver
    options = webdriver.ChromeOptions()
    options.add_argument('user-data-dir=' + USER_DATA_DIR)

    user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/83.0.4103.53 Safari/537.36')
    options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(options=options)

    driver.get(link)

    sleep(30)

    with open('downloadlogs.js') as file:
        script = ''.join(file.readlines())

    driver.execute_script(script)

    elm = driver.find_element(By.TAG_NAME, "html")
    elm.send_keys("s")

    sleep(5)

    driver.close()


if __name__ == '__main__':
    review_log(LINK)
