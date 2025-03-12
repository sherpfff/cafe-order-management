# -*- coding: utf-8 -*-
"""
ASGI конфигурация для проекта cafe_order_management.
Этот модуль предоставляет вызываемый объект ASGI как переменную уровня модуля `application`.

Для получения дополнительной информации об этом файле см.:
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import os
from django.core.asgi import get_asgi_application

# Установка переменной окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cafe_order_management.settings')

# Создание экземпляра ASGI-приложения
application = get_asgi_application()