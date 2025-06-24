Проект hw_drf

Установка
Клонируйте репозиторий на свой компьютер:
git@github.com:skysaika/hw_drf.git

Перейдите в директорию проекта:
- cd hw_drf
- 
Создайте и активируйте виртуальное окружение:
- python -m venv venv
- source .venv/bin/activate

Установите зависимости из файла requirements.txt:
- pip install -r requirements.txt

Настройка:
- Создайте файл .env в корневой директории проекта и скопируйте в него содержимое из .env.sample. 
- Заполните необходимые параметры, параметры подключения к базе данных и другие.

Запуск:
1) Запустите сервер Django:
    - python manage.py runserver
2) Запустите Celery worker для обработки задач:
    - celery -A config worker -l info
3) Запустите Celery beat для планирования задач:
    - celery -A config beat -l info
4) Откройте браузер и перейдите по адресу http://localhost:8000/ для проверки работоспособности сервера.
5) 