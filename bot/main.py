import re
import time
from dotenv import load_dotenv
import os , requests
import cloudscraper
from crontab import CronTab
from typing import Optional
from bs4 import BeautifulSoup
import random
import smtplib
from email.mime.text import MIMEText

load_dotenv()

GMAIL_USER=os.getenv("GMAIL_USERNAME")
GMAIL_PASSWORD=os.getenv("GMAIL_PASSWORD")
RECIPIENT_USER = 'koshish62@gmail.com'

proxies = {
    "http": "http://207.2.120.15:8080",
    "https": "http://207.2.120.15:8080"
}


def get_free_proxies():
    """
    Scrape the Geonode free proxy list and return a list of proxies in the format "http://IP:port".
    """
    url = "https://geonode.com/free-proxy-list"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    proxies = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        # Assume proxies are in a table body (<tbody>)
        tbody = soup.find("tbody")
        if tbody:
            rows = tbody.find_all("tr")
            for row in rows:
                cells = row.find_all("td")
                if len(cells) >= 2:
                    ip = cells[0].get_text(strip=True)
                    port = cells[1].get_text(strip=True)
                    proxies.append(f"http://{ip}:{port}")
    return proxies

def get_random_proxy():
    """
    Returns a proxies dict suitable for requests, using one random proxy from the scraped list.
    """
    proxies = get_free_proxies()
    if proxies:
        chosen = random.choice(proxies)
        return {"http": chosen, "https": chosen}
    return None


def get_random_quote(author:Optional[str]=None,topics:Optional[str]= None):


    # Obtain a random proxy to use for this request
    proxy = get_random_proxy()

    scraper = cloudscraper.create_scraper() 

    if author:
        author_name=re.sub(r"\s+", "-", author.strip())
        url=f"https://www.brainyquote.com/authors/{author_name}-quotes"
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }

    elif topics:
        topic_name=re.sub(r"\s+", "-", topics.strip())
        url=f"https://www.brainyquote.com/topics/{topic_name}-quotes"
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }

    
    response = scraper.get(url,headers=headers, proxies=proxy)
    # if response.status_code != 200:
    #     print(f"Error {response.status_code}: Unable to fetch page. Retrying in 3 seconds...")

    soup = BeautifulSoup(response.text, "html.parser")
    quotes = [q.text.strip() for q in soup.find_all("a", class_="b-qt")]

        # if quotes:
        #     break

    return random.choice(quotes) 

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
        s.login(GMAIL_USER,GMAIL_PASSWORD)
        s.sendmail(GMAIL_USER, RECIPIENT_USER, msg.as_string())
        s.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Failed to send email", e)


if __name__=="__main__":
    send_mail()