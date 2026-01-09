FROM python:3.10-slim

# Установка системных зависимостей (меняются редко - кэшируется)
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование requirements.txt и установка зависимостей
# Этот слой будет кэшироваться, пока requirements.txt не изменится
COPY Website/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Создание директории data (будет монтироваться как volume, но нужно создать структуру)
RUN mkdir -p /app/Website/data/databases /app/Website/data/downloads /app/Website/data/projects /app/Website/data/models

# Переменные окружения (несекретные значения по умолчанию)
# API_KEY должен передаваться через -e при запуске контейнера
ENV MODE="release"
ENV SERVER_PORT=80

# Открытие порта
EXPOSE 80

# Копирование кода в самом конце (меняется чаще всего)
# При изменении кода не будут пересобираться слои с зависимостями и настройками
COPY Website/ ./Website/

# Установка рабочей директории для приложения (после копирования)
WORKDIR /app/Website

# Команда запуска
CMD ["python3", "runserver.py"]

