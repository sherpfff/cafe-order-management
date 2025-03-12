# -*- coding: utf-8 -*-
"""
WSGI конфигурация для проекта cafe_order_management.
Этот модуль предоставляет вызываемый объект WSGI как переменную уровня модуля `application`.

Для получения дополнительной информации об этом файле см.:
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""
import os
from django.core.wsgi import get_wsgi_application

# Установка переменной окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafe_order_management.settings')

# Создание экземпляра WSGI-приложения
application = get_wsgi_application()