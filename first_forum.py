from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import pandas as pd


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
first_url = "https://mosday.ru/forum/viewtopic.php?t=4236&postdays=0&postorder=asc&start={}"
reviews_data = []

start = 0

while True:
    url = first_url.format(start)
    driver.get(url)
    time.sleep(3)
    reviews = driver.find_elements(By.CSS_SELECTOR, 'span.postbody')
    if not reviews or start > 15:
        print("отзывы загружены")
        break

    for review in reviews:
        review_text = review.text.strip()
        if review_text:
            reviews_data.append({"review": review_text})

    start += 15


driver.quit()
df = pd.DataFrame(reviews_data)
df.to_excel("reviews_data.xlsx", index=False)
