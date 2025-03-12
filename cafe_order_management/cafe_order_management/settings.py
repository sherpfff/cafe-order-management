# -*- coding: utf-8 -*-
"""
Настройки для проекта cafe_order_management.
Created on Tue Mar 11 07:30:51 2025
@author: sherp
"""
from pathlib import Path

# Основной путь к проекту
BASE_DIR = Path(__file__).resolve().parent.parent

# Быстрые настройки разработки - НЕ ПОДХОДЯТ ДЛЯ ПРОДАКШЕНА!
# https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# Секретный ключ (замените на реальный при развертывании)
SECRET_KEY = 'django-insecure-87!_%i#h(=c68f1c_m&u@@p5-qyy$e)*vk63#xc*8xg3yb0ofv'

# Режим отладки
DEBUG = True

# Разрешенные хосты (добавьте домены при развертывании)
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Сборка статических файлов для production
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Приложения
INSTALLED_APPS = [
    'cafe_orders_app',  # Приложение заказов
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',  # Поддержка DRF
]

# Промежуточное ПО
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Основной URL-конфигурационный файл
ROOT_URLCONF = 'cafe_order_management.urls'

# Настройки шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],  # Добавляем директорию для глобальных шаблонов
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI-приложение
WSGI_APPLICATION = 'cafe_order_management.wsgi.application'

# База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Валидация паролей
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Интернационализация
LANGUAGE_CODE = 'ru-ru'  # Русский язык
TIME_ZONE = 'Europe/Moscow'  # Московское время
USE_I18N = True
USE_TZ = True

# Статические файлы (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]  # Локальная директория для статических файлов

# Тип первичного ключа по умолчанию
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки REST Framework
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',  # Рендеринг JSON
        'rest_framework.renderers.BrowsableAPIRenderer',  # Включено для удобства разработки
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',  # Парсинг JSON
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [],  # Без аутентификации
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Разрешить доступ всем
    ],
}