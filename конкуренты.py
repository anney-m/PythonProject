# -*- coding: utf-8 -*-
"""конкуренты

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1jT9_zngIo1WTRNsVMoc38b_OduJ3Hq9I
"""

# спарсим первый сайт, посмотрим на цены и виды тренировок
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = "https://wsstudio.info/tseny/"
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

price_items = soup.find_all('span', class_='elementor-price-list-price')
services_items = soup.find_all('span', class_='elementor-price-list-title')

services = []
prices = []

fetched_items = list(zip( services_items, price_items))

for fetched_service, fetched_price in fetched_items:
    services.append(fetched_service.text.strip())
    prices.append(fetched_price.text)

df = pd.DataFrame({
    'Название услуги': services,
    'Цена': prices
})

print(df)

with pd.ExcelWriter('services_data1.xlsx') as writer:
    df.to_excel(writer, sheet_name='Services', index=False)

# второй сайт по такой же логике
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

url = "https://moyfit.com/?ysclid=m8c5kffnqy385506837#rec778251736"
response = requests.get(url)
html_content = response.text

soup = BeautifulSoup(html_content, 'html.parser')

price_items = soup.find_all('div', class_='t1072__price t-title t-title_xs')
services_items = soup.find_all('div', class_='t-card__title t-name t-name_md')
membership_items = soup.find_all('div', class_='t-card__title t-name t-name_lg')
services = []
prices = []
memberships = []

fetched_items = list(zip( membership_items, price_items))

for fetched_membership, fetched_price in fetched_items:
    memberships.append(fetched_membership.text.strip())
    prices.append(fetched_price.text)

for service in services_items:
    services.append(service.text.strip())

df = pd.DataFrame({
    'Вид абонемента': memberships,
    'Цена': prices
})
df1 = pd.DataFrame({
    'Название услуги': services,
})
print(df)
print(df1)

with pd.ExcelWriter('services_data2.xlsx') as writer:
    df.to_excel(writer, sheet_name='Memberships', index=False)
    df1.to_excel(writer, sheet_name='Services', index=False)

