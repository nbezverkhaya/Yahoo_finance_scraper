#123
import unittest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class TestYahooFinance(unittest.TestCase):
    def setUp(self):
        # Налаштування опцій для ChromeDriver
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Опціонально: запуск у фоновому режимі
        service = Service(ChromeDriverManager().install())

        # Створюємо екземпляр драйвера
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.get("https://finance.yahoo.com/")

    def test_article_titles_present(self):
        try:
            wait = WebDriverWait(self.driver, 15)

            # Закриття попапа
            try:
                reject_button = wait.until(
                    EC.element_to_be_clickable((By.XPATH, '//button[@name="reject" and contains(text(), "Alle ablehnen")]'))
                )
                reject_button.click()
                print("Cookies попап закрито, натиснуто 'Alle ablehnen'.")
            except TimeoutException:
                print("Попап із cookies не з'явився.")

            # Очікування заголовків новин
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h3, div[data-test-id="news-article-title"]')))

            # Перевіряємо наявність заголовків новин
            articles = self.driver.find_elements(By.CSS_SELECTOR, 'h3, div[data-test-id="news-article-title"]')
            # Фільтрація порожніх заголовків
            titles = [article.text.strip() for article in articles if article.text.strip()]

            self.assertGreater(len(titles), 0, "Не знайдено заголовків новин на сторінці")

            # Перевірка, що заголовки не порожні
            for title in titles:
                self.assertTrue(title, "Заголовок новини не повинен бути порожнім")

        except TimeoutException:
            self.fail("Заголовки новин не завантажились у відведений час")

    def tearDown(self):
        # Закриття браузера після завершення тестів
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
