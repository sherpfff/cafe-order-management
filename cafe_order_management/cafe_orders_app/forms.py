# -*- coding: utf-8 -*-
"""
Формы для приложения cafe_orders_app.
Created on Tue Mar 11 07:30:51 2025
@author: sherp
"""
from django import forms
from .models import Order, Dish
from typing import List, Dict

class OrderForm(forms.ModelForm):
    """
    Форма для создания и редактирования заказа.
    
    Поля:
        table_number (IntegerField): Номер столика.
        dishes (ModelMultipleChoiceField): Список доступных блюд.
    """
    dishes = forms.ModelMultipleChoiceField(
        queryset=Dish.objects.filter(available=True),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        required=False,
        label="Выберите блюда"
    )

    class Meta:
        model = Order
        fields = ['table_number', 'dishes']

    def clean_table_number(self) -> int:
        """
        Валидация поля table_number.
        Args:
            self: Экземпляр формы.
        Returns:
            int: Валидное значение номера столика.
        Raises:
            forms.ValidationError: Если номер столика недопустим.
        """
        table_number = self.cleaned_data.get('table_number')
        if table_number <= 0:
            raise forms.ValidationError("Номер столика должен быть положительным числом.")
        return table_number

    def clean_dishes(self) -> List[Dish]:
        """
        Валидация поля dishes.
        Args:
            self: Экземпляр формы.
        Returns:
            List[Dish]: Список выбранных блюд.
        Raises:
            forms.ValidationError: Если блюда не выбраны.
        """
        dishes = self.cleaned_data.get('dishes')
        if not dishes:
            raise forms.ValidationError("Пожалуйста, выберите хотя бы одно блюдо.")
        return dishes

    def clean(self) -> Dict:
        """
        Общая валидация формы.
        Args:
            self: Экземпляр формы.
        Returns:
            Dict: Очищенные данные формы.
        """
        cleaned_data = super().clean()
        return cleaned_data