from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Настройки для Selenium
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # Запуск в фоновом режиме
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

# Указываем путь к chromedriver
driver = webdriver.Chrome(options=options)

# Ссылки на категории батончиков
category_urls = {
    'Strong': 'https://proteinrex.com/strong',
    'Extra': 'https://proteinrex.com/extra',
    'Gym': 'https://proteinrex.com/gym'
}

# Создаем пустой DataFrame для хранения данных
columns = ['Категория', 'Вкус', 'Белки (г)', 'Жиры (г)', 'Углеводы (г)', 'Ккал', 'Вес (г)']
data = []

# Парсим данные для каждой категории
for category, url in category_urls.items():
    print(f"Переход на страницу: {url}")
    driver.get(url)
    time.sleep(3)  # Ждем загрузки страницы

    # Ожидание появления элементов
    wait = WebDriverWait(driver, 10)

    # Находим все элементы с названиями вкусов и ссылками
    products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'js-store-prod-name')))
    print(f"Найдено {len(products)} продуктов")

    for product in products:
        try:
            # Извлекаем название вкуса
            name = product.text.strip()

            # Находим ссылку на страницу продукта
            link = product.find_element(By.XPATH, './ancestor::a').get_attribute('href')
            print(f"Переход на страницу продукта: {link}")

            # Переходим на страницу продукта
            driver.get(link)
            time.sleep(3)  # Ждем загрузки страницы

            # Извлекаем данные о пищевой ценности и весе
            charcs = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'js-store-prod-all-charcs')))
            charcs_text = charcs.text.strip()

            # Извлекаем данные
            proteins = charcs_text.split('Белки:')[1].split()[0]
            fats = charcs_text.split('Жиры:')[1].split()[0]
            carbs = charcs_text.split('Углеводы:')[1].split()[0]
            kcal = charcs_text.split('Ккал:')[1].split()[0]
            weight = charcs_text.split('Вес:')[1].split()[0].replace('&nbsp;', ' ')

            # Добавляем данные в список
            data.append([category, name, proteins, fats, carbs, kcal, weight])
            print(f"Добавлен продукт: {name} (Вес: {weight})")

            # Возвращаемся на страницу категории
            driver.back()
            time.sleep(3)  # Ждем загрузки страницы
        except Exception as e:
            print(f"Ошибка при парсинге продукта: {e}")

# Закрываем браузер
driver.quit()

# Создаем DataFrame
df = pd.DataFrame(data, columns=columns)

# Сохраняем данные в CSV
df.to_csv('1bars.csv', index=False, encoding='utf-8-sig')  # encoding для поддержки кириллицы

print("Данные успешно сохранены в файл '1bars.csv'")