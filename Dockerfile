FROM selenium/standalone-chrome:latest

# Встановлюємо Python та pip
USER root
RUN apt-get update && apt-get install -y python3 python3-pip

# Встановлюємо залежності
COPY requirements.txt .
RUN pip3 install -r requirements.txt

USER seluser

