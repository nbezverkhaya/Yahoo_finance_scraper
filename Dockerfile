FROM python:3.9-slim  # Використовуємо базовий образ Python

# Встановлюємо потрібні пакунки
RUN apt-get update && apt-get install -y \
    python3-pip \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Встановлюємо Selenium і WebDriver Manager
RUN pip install selenium webdriver-manager

# Копіюємо ваш код у контейнер
WORKDIR /app
COPY . .

# Запускаємо тести
CMD ["python3", "-m", "unittest", "discover", "-s", "tests", "-p", "*_test.py"]

