# Система управления заказами для кафе
Проект cafe_order_management

# Требования к системе
Python 3.9 или выше
pip менеджер пакетов Python
Git для клонирования репозитория
База данных SQLite встроенная в Python

# Установите зависимости:
pip install -r requirements.txt

# Файл requirements.txt содержит следующие зависимости:
Django==4.2
djangorestframework==3.14

# Настройка окружения
Создайте файл .env в корневой директории проекта и добавьте следующие переменные:
SECRET_KEY=ваш-секретный-ключ
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Замените ваш-секретный-ключ на уникальный секретный ключ.

# Миграции базы данных
Примените миграции для создания таблиц в базе данных:
python manage.py makemigrations
python manage.py migrate

# Запуск приложения
Запустите локальный сервер:
python manage.py runserver

Приложение будет доступно по адресу http://127.0.0.1:8000/

# Тестирование
Для запуска тестов выполните команду:
python manage.py test

# API документация
Доступны следующие эндпоинты API:

GET /api/orders/ Получение списка заказов
POST /api/orders/ Создание нового заказа
GET /api/orders/<id>/ Получение информации о конкретном заказе
PUT /api/orders/<id>/ Обновление информации о заказе
DELETE /api/orders/<id>/ Удаление заказа
GET /api/orders/calculate-revenue/ Расчет общей выручки
GET /api/orders/table-summary/ Сводка по столам

Структура проекта
cafe_order_management/
cafe_orders_app/ Основное приложение
admin.py Административный интерфейс
api_urls.py Маршруты API
api_views.py Представления API
dishes.json Данные о блюдах
dish_interface.py Интерфейс управления блюдами
dish_manager.py Менеджер блюд
forms.py Формы Django
models.py Модели данных
serializers.py Сериализаторы DRF
tests.py Модульные тесты
views.py Представления Django
templates/ HTML шаблоны
static/ Статические файлы
css/ Стили CSS
js/ JavaScript
# manage.py Управление проектом
# requirements.txt Зависимости
README.md Инструкция по развертыванию

# Безопасность
# Убедитесь что переменная DEBUG установлена в False в продакшене
# Для отслеживания ошибок рекомендуется настроить логирование в settings.py
# Для развертывания на сервере используйте WSGI сервер например Gunicorn и обратный прокси например Nginx
