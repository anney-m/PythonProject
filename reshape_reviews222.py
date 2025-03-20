from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service)

driver.get("https://yandex.ru/maps/org/reshape/152017623705/reviews/?ll=37.632233%2C55.767803&z=15")

time.sleep(5)

reviews_data = []


def scroll_page():
    scrollable_element = driver.find_element(By.TAG_NAME, "body")
    actions = ActionChains(driver)
    actions.move_to_element(scrollable_element).perform()
    actions.scroll_by_amount(0, 3000).perform()
    time.sleep(5)


def collect_reviews():
    reviews = driver.find_elements(By.CLASS_NAME, "business-review-view__info")
    return reviews


def get_review_text(review):
    review_text = ""
    try:
        expand_button = review.find_element(By.CLASS_NAME, "business-review-view__expand")
        expand_button.click()
        time.sleep(1)
    except Exception as e:
        pass
    try:
        review_text_element = review.find_element(By.CLASS_NAME, "business-review-view__body-text")
        review_text = review_text_element.text
    except Exception as e:
        print(f"Не удалось получить текст отзыва: {e}")

    return review_text


def process_reviews(reviews):
    for review in reviews:
        review_text = get_review_text(review)
        rating_stars = review.find_elements(By.CSS_SELECTOR, "div.business-rating-badge-view__stars span._full")
        rating = len(rating_stars)
        reviews_data.append({"review": review_text, "rating": rating})


WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "business-review-view__info"))
)

while len(reviews_data) < 212:
    reviews = collect_reviews()
    process_reviews(reviews[len(reviews_data):])
    scroll_page()


df = pd.DataFrame(reviews_data)
df.to_excel('reshape2.xlsx', index=False)
driver.quit()
