import requests
from bs4 import BeautifulSoup

BASE_URL = "https://barfits.ru"

def get_product_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for a_tag in soup.find_all('a', class_='product__link-hidden'):
        link = a_tag.get('href')
        if link:
            full_link = f"{BASE_URL}{link}"
            links.append(full_link)
    return links


urls_and_files = [
    ('https://barfits.ru/catalog/kardiotrenazher/ellipticheskie-trenazhyery/', 'ellipticheskie_trenazhery.txt'),
    ('https://barfits.ru/catalog/kardiotrenazher/velotrenazhery/', 'velotrenazhery.txt'),
    ('https://barfits.ru/catalog/kardiotrenazher/begovye-dorozhki/', 'begovye_dorozhki.txt')
]


for url, filename in urls_and_files:
    product_links = get_product_links(url)
    with open(filename, 'w', encoding='utf-8') as file:
        for link in product_links:
            file.write(f"{link}\n")
    print(f"Ссылки с {url} сохранены в {filename}")

