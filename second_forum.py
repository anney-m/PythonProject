from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

url = "https://www.woman.ru/health/health-fitness/thread/4895239/"
driver.get(url)
time.sleep(5)

review_data = []

def scroll_page():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def collect_comments():
    comments = driver.find_elements(By.CSS_SELECTOR, "div.card__text p.card__comment")
    for comment in comments:
        comment_text = comment.text.strip()
        if comment_text:
            review_data.append({"comment": comment_text})

scroll_page()
collect_comments()
driver.quit()

df = pd.DataFrame(review_data)
df.to_excel("second_forum.xlsx", index=False)

