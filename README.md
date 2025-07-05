Проект hw_drf
Установка

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

