import requests
import pandas as pd
from bs4 import BeautifulSoup
import time
import random
import re
url = "https://www.cian.ru/snyat-pomeshenie-svobodnogo-naznachenija-moskva-novokosino-0466/"

user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:128.0) Gecko/20100101 Firefox/128.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"
]
# это нужно для обхода блокировок сайта при превышении лимита запросов, взяты с https://pypi.org/project/latest-user-agents/

session = requests.Session()

def get_html(url):
    for i in range(10):
        headers = {
            "User-Agent": random.choice(user_agents),
            "Referer": "https://www.google.com/",
            "Accept-Language": "ru-RU,ru;q=0.9"
        }
        try:
            response = session.get(url, headers=headers, timeout=10)
            if response.status_code == 429: # если ошибочки
                wait_time = random.uniform(30, 60)
                print(f"Получена ошибка 429, ждем {wait_time:.1f}с")
                time.sleep(wait_time)
                continue  # продолжение попыток
            return response.text
        except requests.RequestException as e:
            print(f"Ошибка: {e}")
            time.sleep(random.uniform(5, 10))
    return None

html = get_html(url)
if not html:
    print("Ошибка при получении страницы списка объявлений")
    exit()

soup = BeautifulSoup(html, "html.parser")

offers = soup.find_all("div", class_="_32bbee5fda--container--N0wtY", limit=15)

links = []
for offer in offers:
    link_tag = offer.find("a", class_="_32bbee5fda--header-link--RFvxs _32bbee5fda--common--IHoo5")
    if link_tag and "href" in link_tag.attrs:
        links.append(link_tag["href"])

with open("cian_links.txt", "w", encoding="utf-8") as file:
    for link in links:
        file.write(link + "\n") # по одной ссылке на каждой строчке для удобства


data_list = []
with open("cian_links.txt", "r", encoding="utf-8") as file:
    links = [line.strip() for line in file.readlines()]

for index, link in enumerate(links):
    wait_time = random.uniform(5, 15)
    print(f"[{index+1}/{len(links)}] Обрабатывается: {link}")
    time.sleep(wait_time)

    html = get_html(link)
    if not html:
        print(f"Ошибка загрузки {link}")
        continue

    soup = BeautifulSoup(html, "html.parser")

    metro_tag = soup.find("a", class_="a10a3f92e9--underground_link--VnUVj")
    metro = metro_tag.text.strip() if metro_tag else "Нет данных"

    address_tags = soup.find("div", class_="a10a3f92e9--address-line--GRDTb")
    address = " ".join(a.text.strip() for a in address_tags.find_all("a")) if address_tags else "Нет данных"

    area_tag = soup.find("span", class_="a10a3f92e9--color_text-primary-default--vSRPB a10a3f92e9--lineHeight_6u--cedXD a10a3f92e9--fontWeight_bold--BbhnX a10a3f92e9--fontSize_16px--QNYmt a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY")
    area = area_tag.text.strip().replace("м²", "").strip() if area_tag else "Нет данных"

    price_tag = soup.find("span", class_="a10a3f92e9--color_text-primary-default--vSRPB a10a3f92e9--lineHeight_9u--limEs a10a3f92e9--fontWeight_bold--BbhnX a10a3f92e9--fontSize_28px--P1gR4 a10a3f92e9--display_block--KYb25 a10a3f92e9--text--e4SBY")
    if price_tag:
        price = re.sub(r"[^\d]", "", price_tag.text)  # убираем все кроме цифр
    else:
        price = "Нет данных"
    data_list.append({"Метро": metro, "Адрес": address, "Площадь (м²)": area, "Цена (руб/мес)": price})

df = pd.DataFrame(data_list)
df.to_excel("cian_data.xlsx", index=False)