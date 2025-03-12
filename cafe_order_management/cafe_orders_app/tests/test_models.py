# -*- coding: utf-8 -*-
"""
Created on Wed Mar 12 22:53:06 2025

@author: sherp
"""

# tests/test_models.py
import pytest
from cafe_orders_app.models import Order, Dish

@pytest.mark.django_db
def test_order_creation():
    dish = Dish.objects.create(name="Чай", price=10.0)
    order = Order.objects.create(table_number=1)
    order.dishes.add(dish)
    order.save()
    assert order.total_price == 10.0