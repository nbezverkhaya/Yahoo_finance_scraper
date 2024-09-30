from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import pandas as pd

def scrape_yahoo_finance():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    driver.get("https://finance.yahoo.com/")

    try:
        wait = WebDriverWait(driver, 15)
        reject_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//button[@name="reject" and contains(text(), "Alle ablehnen")]'))
        )
        reject_button.click()
        print("Cookies попап закрито, натиснуто 'Alle ablehnen'.")

        # Очікуємо, поки заголовки новин з'являться
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h3, div[data-test-id="news-article-title"]')))

        # Збір заголовків новин
        articles = driver.find_elements(By.CSS_SELECTOR, 'h3, div[data-test-id="news-article-title"]')
        titles = [article.text for article in articles if article.text.strip() != ""]

        # Створення DataFrame і збереження в CSV файл
        if titles:
            data = {'Title': titles}
            df = pd.DataFrame(data)
            df.to_csv('yahoo_finance_news.csv', index=False)
            print(f"Збережено {len(titles)} заголовків новин у файл yahoo_finance_news.csv")
        else:
            print("Не вдалося знайти новини на сторінці.")

    except TimeoutException:
        print("Не вдалося завантажити список новин.")
    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_yahoo_finance()
