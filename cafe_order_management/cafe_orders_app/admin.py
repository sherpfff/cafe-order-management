# -*- coding: utf-8 -*-
"""
Административный интерфейс для приложения cafe_orders_app.
Created on Tue Mar 11 08:23:11 2025
@author: sherp
"""
from django.contrib import admin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin
from .models import Order, Dish

class DishAdmin(ImportExportModelAdmin, SimpleHistoryAdmin, admin.ModelAdmin):
    """
    Настройки административного интерфейса для модели Dish.
    """
    list_display = ('name', 'price', 'available', 'formatted_price')
    list_filter = ('available',)
    search_fields = ('name',)
    list_editable = ('available',)  # Возможность редактировать доступность прямо в списке

    @admin.display(description="Цена (руб.)")
    def formatted_price(self, obj) -> str:
        """
        Форматирует цену для отображения в админке.
        
        Args:
            obj (Dish): Экземпляр модели Dish.
        
        Returns:
            str: Отформатированная цена.
        """
        return f"{obj.price:.2f} руб."

@admin.register(Order)
class OrderAdmin(ImportExportModelAdmin, SimpleHistoryAdmin, admin.ModelAdmin):
    """
    Настройки административного интерфейса для модели Order.
    """
    list_display = ('id', 'table_number', 'status', 'total_price', 'formatted_dishes')
    list_filter = ('status', 'table_number')
    search_fields = ('table_number',)
    readonly_fields = ('total_price',)  # Поле total_price только для чтения
    filter_horizontal = ('dishes',)  # Удобный виджет для выбора блюд
    actions = ['mark_as_paid']  # Действие для массового изменения статуса

    @admin.display(description="Блюда")
    def formatted_dishes(self, obj) -> str:
        """
        Форматирует список блюд для отображения в админке.
        
        Args:
            obj (Order): Экземпляр модели Order.
        
        Returns:
            str: Список блюд с их ценами.
        """
        dishes = obj.dishes.all()
        if not dishes:
            return "Нет блюд"
        return format_html(
            "<br>".join(f"{dish.name} ({dish.price:.2f} руб.)" for dish in dishes)
        )

    def mark_as_paid(self, request, queryset):
        """
        Отмечает выбранные заказы как оплаченные.
        """
        queryset.update(status='PAID')
    mark_as_paid.short_description = "Отметить выбранные заказы как оплаченные"

# Регистрация модели Dish
admin.site.register(Dish, DishAdmin)
