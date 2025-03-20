from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36') # помощь зала

driver = webdriver.Chrome(options=options)
category_urls = {
    'Strong': 'https://proteinrex.com/strong',
    'Extra': 'https://proteinrex.com/extra',
    'Gym': 'https://proteinrex.com/gym'}

columns = ['Категория', 'Вкус', 'Белки (г)', 'Жиры (г)', 'Углеводы (г)', 'Ккал', 'Вес (г)']
data = []
for category, url in category_urls.items():
    print({url})
    driver.get(url)
    time.sleep(3)
    wait = WebDriverWait(driver, 10)

    products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'js-store-prod-name')))
    print(f"Найдено {len(products)} продуктов")

    for product in products:
        try:
            name = product.text.strip()
            link = product.find_element(By.XPATH, './ancestor::a').get_attribute('href')
            print(f"Переход на страницу продукта: {link}")
            driver.get(link)
            time.sleep(3)

            charcs = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'js-store-prod-all-charcs')))
            charcs_text = charcs.text.strip()
            proteins = charcs_text.split('Белки:')[1].split()[0]
            fats = charcs_text.split('Жиры:')[1].split()[0]
            carbs = charcs_text.split('Углеводы:')[1].split()[0]
            kcal = charcs_text.split('Ккал:')[1].split()[0]
            weight = charcs_text.split('Вес:')[1].split()[0].replace('&nbsp;', ' ')
            data.append([category, name, proteins, fats, carbs, kcal, weight])
            print(f"Добавлен продукт: {name} (Вес: {weight})")


            driver.back()
            time.sleep(3)
        except Exception as e:
            print(f"Ошибка {e}")

driver.quit()

df = pd.DataFrame(data, columns=columns)

df.to_csv('1bars.csv', index=False, encoding='utf-8-sig')  # encoding для поддержки кириллицы

print()