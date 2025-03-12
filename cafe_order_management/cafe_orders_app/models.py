# -*- coding: utf-8 -*-
"""
Модели для приложения cafe_orders_app.
Created on Tue Mar 11 07:30:51 2025
@author: sherp
"""
from django.db import models
from django.core.exceptions import ValidationError
from typing import List, Dict

class Dish(models.Model):
    """
    Модель для хранения информации о блюдах.
    
    Поля:
        name (str): Название блюда.
        price (Decimal): Цена блюда.
        available (bool): Доступно ли блюдо.
    """
    name = models.CharField(max_length=255, verbose_name="Название блюда")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Цена"
    )
    available = models.BooleanField(default=True, verbose_name="Доступно")

    def __str__(self) -> str:
        return f'{self.name} ({self.price})'

    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"
        ordering = ['name']

class Order(models.Model):
    """
    Модель заказа для кафе.
    
    Поля:
        table_number (int): Номер столика.
        dishes (ManyToManyField): Связь с блюдами.
        total_price (Decimal): Общая стоимость заказа.
        status (CharField): Статус заказа.
    """
    PENDING = 'В ожидании'
    READY = 'Готово'
    PAID = 'Оплачено'
    STATUS_CHOICES = [
        (PENDING, 'В ожидании'),
        (READY, 'Готово'),
        (PAID, 'Оплачено')
    ]

    table_number = models.IntegerField(verbose_name="Номер столика")
    dishes = models.ManyToManyField(
        Dish, 
        blank=True, 
        verbose_name="Блюда"
    )
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=0, 
        verbose_name="Общая стоимость"
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default=PENDING, 
        verbose_name="Статус заказа"
    )

    def __str__(self) -> str:
        return f'Заказ #{self.id}'

    def save(self, *args, **kwargs) -> None:
        """
        Переопределение метода save для автоматического расчета общей стоимости заказа.
        """
        # Сначала сохраняем объект без ManyToMany-отношений
        super().save(*args, **kwargs)
        
        # Теперь можно безопасно работать с ManyToMany-отношениями
        if self.dishes.exists():
            self.total_price = sum(
                dish.price for dish in self.dishes.filter(available=True)
            )
        else:
            self.total_price = 0
        
        # Сохраняем объект снова, чтобы обновить total_price
        super().save(*args, **kwargs)

    def clean(self) -> None:
        """
        Валидация данных перед сохранением.
        """
        if self.table_number <= 0:
            raise ValidationError("Номер столика должен быть положительным числом.")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-id']