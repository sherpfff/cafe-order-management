# -*- coding: utf-8 -*-
"""
Сериализаторы для модели Order.
Created on Tue Mar 11 07:30:51 2025
@author: sherp
"""
from rest_framework import serializers
from .models import Order

def validate_items(value):
    """
    Валидация поля items.
    Args:
        value: Значение поля items.
    Returns:
        value: Валидное значение.
    Raises:
        serializers.ValidationError: Если данные невалидны.
    """
    if not isinstance(value, list):
        raise serializers.ValidationError("Должен быть список блюд.")
    
    for item in value:
        if not isinstance(item, dict):
            raise serializers.ValidationError("Каждое блюдо должно быть объектом.")
        
        if 'name' not in item or 'price' not in item:
            raise serializers.ValidationError("Каждое блюдо должно содержать 'name' и 'price'.")
        
        if not isinstance(item['price'], (int, float)):
            raise serializers.ValidationError("Цена должна быть числом.")
    
    return value

class OrderSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Order.
    Поля:
        items (JSONField): Список блюд с их названиями и ценами.
    """
    items = serializers.JSONField(
        validators=[validate_items],
        help_text="Список блюд в формате [{'name': 'Блюдо', 'price': 100}, ...]."
    )

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('total_price',)  # Поле total_price вычисляется автоматически

    def create(self, validated_data: dict) -> Order:
        """
        Создание нового заказа.
        Args:
            validated_data (dict): Валидированные данные.
        Returns:
            Order: Созданный заказ.
        """
        items = validated_data.pop('items', [])
        order = Order.objects.create(**validated_data)
        
        # Добавляем блюда к заказу
        for item in items:
            dish, created = Dish.objects.get_or_create(
                name=item['name'],
                defaults={'price': item['price'], 'available': True}
            )
            order.dishes.add(dish)
        
        # Сохраняем заказ для обновления total_price
        order.save()
        return order

    def update(self, instance: Order, validated_data: dict) -> Order:
        """
        Обновление существующего заказа.
        Args:
            instance (Order): Существующий заказ.
            validated_data (dict): Валидированные данные.
        Returns:
            Order: Обновленный заказ.
        """
        items = validated_data.pop('items', None)
        
        # Обновляем базовые поля заказа
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        if items is not None:
            instance.dishes.clear()  # Очищаем старые блюда
            for item in items:
                dish, created = Dish.objects.get_or_create(
                    name=item['name'],
                    defaults={'price': item['price'], 'available': True}
                )
                instance.dishes.add(dish)
        
        # Сохраняем заказ для обновления total_price
        instance.save()
        return instance