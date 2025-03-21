import time
import pandas as pd
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

input_file = "ellipticheskie_trenazhery.txt"
output_file = "ellipticheskie_trenazhery.xlsx"

with open(input_file, "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f.readlines()]

data = []

for index, url in enumerate(urls):
    driver.get(url)
    time.sleep(2)

    try:
        title = driver.find_element(By.CLASS_NAME, "product-detail__title").text.strip()
    except:
        title = "-"

    try:
        price = driver.find_element(By.CSS_SELECTOR, "p[data-cost]").text.strip()
    except:
        price = "-"

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
            print({url})
    except Exception as e:
        print({e})

    try:
        description_block = driver.find_element(By.CSS_SELECTOR, "div[data-toggle='product-descr-2']").text
        print( {description_block})
        lines = [line.strip() for line in description_block.split("\n") if line.strip()]
        weight = "-"
        levels = "-"
        programs = "-"

        if index == 0:
            for i in range(0, len(lines), 2):
                key = lines[i].strip()
                value = lines[i + 1].strip() if i + 1 < len(lines) else ""

                if "Макс вес пользователя" in key:
                    weight = value
                elif "Кол-во уровней нагрузки" in key:
                    levels = value
                elif "Количество программ тренировок" in key:
                    programs = value

        else:
            for line in lines:
                if "Макс вес пользователя" in line:
                    weight = line.split(":")[-1].strip()
                elif "Кол-во уровней нагрузки" in line:
                    levels = line.split(":")[-1].strip()
                elif "Количество программ тренировок" in line:
                    programs = line.split(":")[-1].strip()

        print(f"Характеристики: {weight}, {levels}, {programs}")

    except Exception as e:
        print(f"Ошибка {e}")
        weight, levels, programs = "-", "-", "-"

    data.append([title, url, price, levels, weight, programs])

    print(f" {title} - {url} - {price}")

driver.quit()

df = pd.DataFrame(data, columns=["Название", "Ссылка", "Цена", "Уровни нагрузки", "Макс вес", "Программы тренировок"])
df.to_excel(output_file, index=False, engine="openpyxl")

print({output_file} )
