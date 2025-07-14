Проект hw_drf

Клонируем репозиторий:
git clone git@github.com:skysaika/hw_drf.git
cd hw_drf

Создаём и активируем виртуальное окружение:
python -m venv .venv
source .venv/bin/activate

Устанавливаем зависимости:
pip install -r requirements.txt
Создаём файл .env в корне проекта на основе .env.example и заполняем параметры (секретные ключи, настройки базы и т.д.)

Запуск без Docker (локально)
Запускаем миграции:
python manage.py migrate

Запускаем сервер Django:
python manage.py runserver

Запускаем Celery worker (обработка фоновых задач):
celery -A config worker -l info

Запускаем Celery beat (планировщик периодических задач):
celery -A config beat -l info

Открываем в браузере:
http://localhost:8000/

Запуск с Docker и Docker Compose
Останавливаем локальный Redis (если он запущен), чтобы порт 6379 не был занят:
sudo systemctl stop redis

Запускаем проект с пересборкой образов:
sudo docker compose up --build

После успешного запуска сервисов проект будет доступен по адресу:
http://localhost:8000/

Чтобы создать суперпользователя, выполните:
sudo docker compose exec web python manage.py createsuperuser

Развёртывание на PythonAnywhere:
Загрузите проект на PythonAnywhere (например, через Git).

Создайте виртуальное окружение на PythonAnywhere с Python 3.10.

Активируйте виртуальное окружение и установите зависимости:

source /home/yourusername/yourproject/venv/bin/activate
pip install -r requirements.txt

Создайте или измените файл .env в корне проекта с актуальными настройками для сервера.

Настройка .env для PythonAnywhere:
⚠️ Важно: файл .env на PythonAnywhere отличается от локального, 
так как настройки базы данных, секретные ключи и другие параметры могут быть другими.

В файле .env необходимо указать:

SECRET_KEY — секретный ключ Django для продакшена.

Параметры базы данных: DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT.

Настройки Redis: REDIS_HOST, REDIS_PORT (если используете).

Параметры почтового сервера (если есть).

Другие секреты и ключи.

Пример .env для PythonAnywhere:

SECRET_KEY=your_production_secret_key_here
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host_or_127.0.0.1
DB_PORT=5432
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
EMAIL_HOST=smtp.your-email-provider.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-email-password

Как обновить .env на PythonAnywhere:
Зайдите в Bash-консоль на PythonAnywhere.

Перейдите в папку проекта:

cd /home/yourusername/hw_drf
Отредактируйте или создайте .env:

nano .env
Сохраните изменения.

Перезагрузите веб-приложение через вкладку Web → кнопка Reload.

