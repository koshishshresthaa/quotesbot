import re
from dotenv import load_dotenv
import os , requests
import cloudscraper
from typing import Optional
from bs4 import BeautifulSoup
import random
import smtplib
from email.mime.text import MIMEText

load_dotenv()

GMAIL_USER=os.getenv("GMAIL_USERNAME")
GMAIL_PASSWORD=os.getenv("GMAIL_PASSWORD")
RECIPIENT_USER = 'koshish62@gmail.com'


def get_random_quote(author:Optional[str]=None,topics:Optional[str]= None):


    scraper = cloudscraper.create_scraper()


    if author:
        author_name=re.sub(r"\s+", "-", author.strip())

        url=f"https://zenquotes.io/authors/{author_name}"

    elif topics:
        url=f"https://zenquotes.io/keywords/{topics}"

    print("Processing !!!")
    response = scraper.get(url)
    
    if response.status_code != 200:
        print(f"Error {response.status_code}: Unable to fetch page..")

    soup = BeautifulSoup(response.text, "html.parser")
    quotes = [q.text.strip() for q in soup.find_all("blockquote")]

        

    return random.choice(quotes)

def send_mail():

    topics_list=['inspiration','courage','freedom','life','living','success','work','time','truth''future']
    author=None
    topic= random.choice(topics_list)
    quote=get_random_quote(topics=topic)

    if author: 
        body = f"Good Morning!! \n\nHere's your quote of the day:\n\n\n '{quote}' - {author} \n\n\n Have a great day !"
    else:
        body=f"Good Morning!!\n\n\n Here's your quote of the day:{quote} \n\n\n Have a great day Koshish"

    msg=MIMEText(body)

    msg['Subject'] = 'Quote of the DAY'
    msg['From'] = GMAIL_USER
    msg ['To'] = RECIPIENT_USER

    try:
        s = smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        s.login(GMAIL_USER,GMAIL_PASSWORD)
        s.sendmail(GMAIL_USER, RECIPIENT_USER, msg.as_string())
        s.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Failed to send email", e)


if __name__=="__main__":
    send_mail()