FROM python:3.12-slim
WORKDIR /app
# Установка зависимостей
COPY /requirements.txt /
RUN pip install -r /requirements.txt --no-cache-dir

# Копирование всех остальных файлов проекта
COPY . .

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]


