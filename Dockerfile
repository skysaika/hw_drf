FROM python:3.12-slim

WORKDIR /app


# Установка зависимостей
COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

# Копирование всех остальных файлов проекта
COPY . .
