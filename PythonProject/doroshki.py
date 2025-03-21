import time
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

chrome_options = Options()
chrome_options.add_argument("--start-maximized")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

input_file = "begovye_dorozhki.txt"
output_file = "dorozhki.xlsx"

with open(input_file, "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f.readlines()]

data = []
for index, url in enumerate(urls):
    driver.get(url)
    time.sleep(2)

    try:
        title = driver.find_element(By.CLASS_NAME, "product-detail__title").text.strip()
    except:
        title = "Нет данных"

    try:
        price = driver.find_element(By.CSS_SELECTOR, "p[data-cost]").text.strip()
    except:
        price = "Нет данных"

    try:
        tabs = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "product-descr__tabs"))
        )
        tab_buttons = tabs.find_elements(By.TAG_NAME, "li")

        if len(tab_buttons) >= 3:
            button = tab_buttons[2].find_element(By.TAG_NAME, "button")

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            time.sleep(1)

            driver.execute_script("arguments[0].click();", button)
            time.sleep(2)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-toggle='product-descr-2']"))
            )
            print({url})
        else:
            print(f"- {url}")
    except Exception as e:
        print({e})

    try:
        description_block = driver.find_element(By.CSS_SELECTOR, "div[data-toggle='product-descr-2']").text
        print({description_block})

        lines = [line.strip() for line in description_block.split("\n") if line.strip()]
        weight = "-"
        motor = "-"
        size = "-"
        has_colon_format = any(":" in line for line in lines)

        if has_colon_format:
            for line in lines:
                if re.search(r"Макс\.?\s*вес\s*пользователя", line, re.IGNORECASE) or re.search(r"Максимальный\.?\s*вес\s*пользователя", line, re.IGNORECASE):
                    weight = line.split(":")[-1].strip()
                elif re.search(r"Двигатель", line, re.IGNORECASE):
                    motor = line.split(":")[-1].strip()
                elif re.search(r"Размеры\s*бегового\s*полотна", line, re.IGNORECASE):
                    size = line.split(":")[-1].strip()

        # Обработка для второго формата (без двоеточий)
        else:
            for i in range(0, len(lines), 2):
                key = lines[i].strip()
                value = lines[i + 1].strip() if i + 1 < len(lines) else ""

                if re.search(r"Макс\.?\s*вес\s*пользователя", key, re.IGNORECASE) or re.search(r"Максимальный\.?\s*вес\s*пользователя", key, re.IGNORECASE):
                    weight = value
                elif re.search(r"Двигатель", key, re.IGNORECASE):
                    motor = value
                elif re.search(r"Размеры\s*бегового\s*полотна", key, re.IGNORECASE):
                    size = value

        size = re.sub(r"\s{2,}", " ", size).strip()

        print(f" Характеристики: {weight}, {motor}, {size}")

    except Exception as e:
        print({e})
        weight, motor, size = "-", "-", "-"
    data.append([title, url, price, weight, motor, size])

    print(f"{title} - {url} - {price}")

driver.quit()

df = pd.DataFrame(data, columns=["Название", "Ссылка", "Цена", "Макс вес", "Двигатель", "Размер полотна"])
df.to_excel(output_file, index=False, engine="openpyxl")

print({output_file})