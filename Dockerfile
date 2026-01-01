FROM python:3.10-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Установка рабочей директории
WORKDIR /app

# Копирование requirements.txt и установка зависимостей
COPY Website/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всего проекта
COPY . .

# Установка рабочей директории для приложения
WORKDIR /app/Website

# Создание директории data (будет монтироваться как volume, но нужно создать структуру)
RUN mkdir -p data/databases data/downloads data/projects data/models

# Переменные окружения (несекретные значения по умолчанию)
# API_KEY должен передаваться через -e при запуске контейнера
ENV MODE="release"
ENV SERVER_PORT=80

# Открытие порта
EXPOSE 80

# Команда запуска
CMD ["python3", "runserver.py"]

