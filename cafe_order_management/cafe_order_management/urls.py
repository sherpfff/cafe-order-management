# -*- coding: utf-8 -*-
"""
Основной файл маршрутизации для проекта cafe_order_management.
Created on Tue Mar 11 07:30:51 2025
@author: sherp
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('cafe_orders_app.urls')),  # Маршруты основного приложения
    path('api/', include('cafe_orders_app.api_urls')),  # Маршруты API
]