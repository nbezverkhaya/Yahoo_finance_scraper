# Вибір базового образу
FROM selenium/standalone-chrome:latest

# Встановлення Python і pip
USER root
RUN apt-get update && apt-get install -y python3 python3-pip

# Копіювання requirements.txt
COPY requirements.txt .

# Встановлення залежностей
RUN pip3 install --no-cache-dir -r requirements.txt

# Повернення до користувача selenium
USER seluser
