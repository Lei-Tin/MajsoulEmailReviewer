"""
This file is for Window usage
"""
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import os
from config import *

from typing import Tuple

# For email
import poplib
import smtplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

LOG_TO_ACTOR = {}
ADDRESS_TO_LINK = {}
RECEIVED = []
SENT = []

def download_log(link: str) -> None:
    """Downloads the json file for the log"""
    options = webdriver.ChromeOptions()
    options.add_argument('user-data-dir=' + USER_DATA_DIR)

    user_agent = ('Mozilla/5.0 (Windows NT 4.0; WOW64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/37.0.2049.0 Safari/537.36')
    options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(options=options)

    driver.get(link)

    # Wait for 30 seconds for the log to load, then download it by pressing "s"
    sleep(30)

    with open('downloadlogs.js', encoding="utf8") as file:
        script = ''.join(file.readlines())

    driver.execute_script(script)

    elm = driver.find_element(By.TAG_NAME, "html")
    elm.send_keys("s")

    sleep(5)

    driver.close()

    print('Download complete')


def review_log(filename: str, actor: str) -> None:
    """Reviews the log given by filename and actor"""
    # Calls the review.bat file that I have written earlier
    subprocess.call(['C:\\Users\\leit\\Desktop\\Akochan\\review.bat',
                     filename,
                     actor])

    print('Analysis complete')

def scan_directory() -> None:
    """Scans current directory and start analyzing all logs that we haven't analyzed yet

    Generates all the logs we want at the moment
    """

    files = os.listdir('Logs')

    read = []

    with open('read', encoding='UTF8') as f:
        for line in f:
            read.append(line.strip())

    newfiles = []
    for file in files:
        if file not in read and file[-5:] != '.html':
            review_log(os.getcwd() + file, LOG_TO_ACTOR[file])
            newfiles.append(file)

    with open('read', 'w', encoding='UTF8') as f:
        f.writelines(read + newfiles)

def parse_email() -> None:
    """Parses the email inputs we receive"""
    print('Connecting through POP3')

    email_server = poplib.POP3_SSL(host=POP_SERVER_HOST, port=POP_SERVER_PORT, timeout=300)

    email_server.user(SENDER_EMAIL)

    email_server.pass_(EMAIL_CODE)

    print('Connected through POP3')

    resp, mails, octets = email_server.list()
    num, total_size = email_server.stat()

    index = len(mails)

    # The mails go from index 1 to len(mails), index 0 is nothing
    for i in range(index, 0, -1):
        resp, lines, octets = email_server.retr(i)
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        msg = Parser().parsestr(msg_content)

        header = parser_email_header(msg)[0].split()

        # if len(header) == 2:
        #     if header[0][:5] == 'https':
        print(header)

    email_server.quit()


def parser_email_header(msg) -> Tuple[str, str]:
    """Parses the email header and returns the title of the email and the sender's address"""
    subject = msg['Subject']
    value, charset = decode_header(subject)[0]
    if charset:
        value = value.decode(charset)

    hdr, addr = parseaddr(msg['From'])

    return value, addr



def send_email() -> None:
    """Sends the emails needed back to them"""
    pass

if __name__ == '__main__':

    parse_email()
