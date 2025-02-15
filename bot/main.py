import re
from dotenv import load_dotenv
import os
import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from crontab import CronTab
from typing import Optional
import cloudscraper
from bs4 import BeautifulSoup
import random
import smtplib
from email.mime.text import MIMEText

load_dotenv()

GMAIL_USER=os.getenv("GMAIL_USERNAME")
GMAIL_PASSWORD=os.getenv("GMAIL_PASSWORD")
RECIPIENT_USER = 'koshish62@gmail.com'


def get_random_quote(author:Optional[str]=None,topics:Optional[str]= None):

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Runs without opening a browser
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


    if author:
        author_name=re.sub(r"\s+", "-", author.strip())
        url=f"https://www.brainyquote.com/authors/{author_name}-quotes"
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        # }

    elif topics:
        topic_name=re.sub(r"\s+", "-", topics.strip())
        url=f"https://www.brainyquote.com/topics/{topics}-quotes"
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        # }

    driver.get(url)

    quotes = [elem.text for elem in driver.find_elements(By.CLASS_NAME, "b-qt")]

    driver.quit() 
    return random.choice(quotes) if quotes else "STAY HARD !!"



def send_mail():

    author='david goggins'
    quote=get_random_quote(author=author)
    body = f"Good Morning!! \n\n Here's your quote of the day: \n\n '{quote}' - {author} \n\n Have a great day !"

    msg=MIMEText(body)

    msg['Subject'] = 'Quote of the DAY'
    msg['From'] = GMAIL_USER
    msg ['To'] = RECIPIENT_USER

    try:
        s = smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        print("before login")
        s.login(GMAIL_USER,GMAIL_PASSWORD)
        print("check check ")
        s.sendmail(GMAIL_USER, RECIPIENT_USER, msg.as_string())
        print("check check check")
        s.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Failed to send email", e)


if __name__=="__main__":
    send_mail()