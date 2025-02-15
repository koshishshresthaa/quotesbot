import re
from dotenv import load_dotenv
import os
import base64
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from crontab import CronTab
from typing import Optional
import tempfile
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
    # options.add_argument("--headless=new")
    options.add_argument("-no-sandbox")
    options.add_argument("-disable-dev-shm-usage")
    options.add_argument('-window-size=1920,1080')
    # options.add_argument("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")


    # Create a unique temporary directory for Chrome's user data
    temp_dir = tempfile.mkdtemp()
    options.add_argument(f"--user-data-dir={temp_dir}")
    
    driver = webdriver.Chrome(options=options)


    if author:
        author_name=re.sub(r"\s+", "-", author.strip())
        url=f"https://www.brainyquote.com/authors/{author_name}-quotes"
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        # }

    elif topics:
        topic_name=re.sub(r"\s+", "-", topics.strip())
        url=f"https://www.brainyquote.com/topics/{topic_name}-quotes"
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        # }f

    driver.get(url)

    
    quote_elements = driver.find_elements(By.CLASS_NAME, "b-qt")
    quotes = [elem.text.strip() for elem in quote_elements if elem.text.strip()]

    driver.quit() 

    return quotes
    # return random.choice(quotes) if quotes else "STAY HARD !!"

print(get_random_quote(author="david goggins"))

# def send_mail():

#     author='david goggins'
#     quote=get_random_quote(author=author)
#     body = f"Good Morning!! \n\n Here's your quote of the day: \n\n '{quote}' - {author} \n\n Have a great day !"

#     msg=MIMEText(body)

#     msg['Subject'] = 'Quote of the DAY'
#     msg['From'] = GMAIL_USER
#     msg ['To'] = RECIPIENT_USER

#     try:
#         s = smtplib.SMTP('smtp.gmail.com',587)
#         s.starttls()
#         s.login(GMAIL_USER,GMAIL_PASSWORD)
#         s.sendmail(GMAIL_USER, RECIPIENT_USER, msg.as_string())
#         s.quit()
#         print("Email sent successfully")
#     except Exception as e:
#         print("Failed to send email", e)


# if __name__=="__main__":
#     send_mail()