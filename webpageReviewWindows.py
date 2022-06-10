"""
This file is for Window usage
"""
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
import subprocess
import os
from os.path import basename
from config import *

from typing import Tuple

# For POP, receiving email
import poplib
from email.parser import Parser
from email.header import Header, decode_header
from email.utils import parseaddr

# For SMTP, sending email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

LINK_TO_ACTOR = {}  # Dictionary mapping email address to actor index
LINK_TO_ADDRESS = {}  # Maps Link to address
SENT = {}  # Dictionary that maps from links to email addresses sent


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

    print('Download log complete')


def review_log(filename: str, actor: str) -> None:
    """Reviews the log given by filename and actor"""
    # Calls the review.bat file that I have written earlier
    subprocess.call(['C:\\Users\\leit\\Desktop\\WebpageReview\\review.bat',
                     f'C:\\Users\\leit\\Desktop\\WebpageReview\\Logs\\{filename}',
                     actor])

    print('Analysis complete')


def scan_log_directory() -> set:
    """Scans current directory and returns the files in the current log directory
    """

    files = os.listdir('Logs')

    return set(files)


def parse_email() -> None:
    """Parses the email inputs we receive"""
    print('Connecting through POP3')

    email_server = poplib.POP3_SSL(host=POP_SERVER_HOST, port=POP_SERVER_PORT, timeout=None)

    email_server.user(SENDER_EMAIL)

    email_server.pass_(EMAIL_CODE)

    print('Connected through POP3')

    resp, mails, octets = email_server.list()
    num, total_size = email_server.stat()

    index = len(mails)

    diff = len(mails) - len(LINK_TO_ADDRESS)

    # The mails go from index 1 to len(mails), index 0 is nothing
    for i in range(index, index - diff, -1):
        resp, lines, octets = email_server.retr(i)
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        msg = Parser().parsestr(msg_content)

        subject, email = parser_email_header(msg)

        header = subject.split()

        if len(header) == 2:
            if header[0][:5] == 'https' and header[0] not in SENT:
                print(f'Parsing email: {header[0]}')
                LINK_TO_ADDRESS[header[0]] = email
                LINK_TO_ACTOR[header[0]] = header[1]

    print(f'Number of new emails parsed: {diff}')

    print('Quitting POP3')

    email_server.quit()


def parser_email_header(msg) -> Tuple[str, str]:
    """Parses the email header and returns the title of the email and the sender's address"""
    subject = msg['Subject']
    value, charset = decode_header(subject)[0]
    if charset:
        value = value.decode(charset)

    hdr, addr = parseaddr(msg['From'])

    return value, addr


def send_email(email: str, filename: str) -> None:
    """Sends the emails with the analysis back to them"""

    print('Connecting through SMTP')

    email_server = smtplib.SMTP_SSL(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT, timeout=None)

    email_server.connect(host=SMTP_SERVER_HOST, port=SMTP_SERVER_PORT)

    email_server.login(user=SENDER_EMAIL, password=EMAIL_CODE)

    print('Connected through SMTP')

    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    message['To'] = email
    message['Subject'] = Header(f'{filename}', 'utf-8')

    with open(f'./Logs/{filename}', 'rb') as f:
        att = MIMEApplication(f.read(), Name=basename(filename))
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = f'attachment; filename="{filename}"'

    message.attach(att)

    print('Sending email')

    email_server.sendmail(SENDER_EMAIL, email, message.as_string())

    print('Email sent, closing SMTP connection')

    email_server.close()


if __name__ == '__main__':
    while True:
        parse_email()

        with open('sent', 'r', encoding='utf8') as f:
            for line in f:
                link, email = line.strip().split(',')
                SENT[link] = email

        for link in set(LINK_TO_ADDRESS.keys()).difference(set(SENT.keys())):
            email = LINK_TO_ADDRESS[link]
            actor_id = LINK_TO_ACTOR[link]

            print(f'Processing {link}, for {email}')

            old_files = scan_log_directory()

            download_log(link)

            new_files = scan_log_directory()

            review_log(new_files.difference(old_files).__iter__().__next__(), actor_id)

            new_analysis_files = scan_log_directory()

            # This is the filename we want to send back
            filename = new_analysis_files.difference(new_files).__iter__().__next__()

            send_email(email, filename)

            with open('sent', 'a', encoding='utf8') as f:
                f.write(f'{link},{email}\n')

        # When no logs are being processed, sleep for 300 seconds.
        print('No more logs to process, sleeping for 5 minutes...')
        sleep(300)
