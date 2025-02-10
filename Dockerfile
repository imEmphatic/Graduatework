# Используем официальный базовый образ Python
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Устанавливаем Poetry
RUN pip install poetry

# Копируем файлы проекта, включая pyproject.toml и poetry.lock
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости с помощью Poetry
RUN poetry config virtualenvs.create false && poetry install --no-root

# Копируем весь код проекта
COPY . /app/