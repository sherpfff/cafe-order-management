# -*- coding: utf-8 -*-
"""
Менеджер для управления блюдами.
Created on Wed Mar 12 01:14:44 2025
@author: sherp
"""
from typing import List, Dict, Optional
import json
import os

# Файл для хранения данных о блюдах
DATA_FILE = 'dishes.json'

def load_dishes() -> List[Dict[str, any]]:
    """
    Загружает список блюд из файла.
    
    Returns:
        List[Dict[str, any]]: Список блюд, где каждый элемент - словарь с данными о блюде.
    """
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_dishes(dishes: List[Dict[str, any]]) -> None:
    """
    Сохраняет список блюд в файл.
    
    Args:
        dishes (List[Dict[str, any]]): Список блюд для сохранения.
    """
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(dishes, f, ensure_ascii=False, indent=4)

def add_dish(name: str, price: float) -> bool:
    """
    Добавляет новое блюдо в список.
    
    Args:
        name (str): Название блюда.
        price (float): Цена блюда.
    
    Returns:
        bool: True если блюдо успешно добавлено, False если блюдо с таким именем уже существует.
    """
    dishes = load_dishes()
    if any(dish['name'] == name for dish in dishes):
        return False
    dishes.append({
        'name': name,
        'price': price,
        'available': True  # По умолчанию блюдо доступно
    })
    save_dishes(dishes)
    return True

def update_availability(name: str, available: bool) -> bool:
    """
    Обновляет статус наличия блюда.
    
    Args:
        name (str): Название блюда.
        available (bool): Новый статус наличия.
    
    Returns:
        bool: True если статус успешно обновлен, False если блюдо не найдено.
    """
    dishes = load_dishes()
    for dish in dishes:
        if dish['name'] == name:
            dish['available'] = available
            save_dishes(dishes)
            return True
    return False

def get_available_dishes() -> List[Dict[str, any]]:
    """
    Получает список доступных блюд.
    
    Returns:
        List[Dict[str, any]]: Список доступных блюд.
    """
    dishes = load_dishes()
    return [dish for dish in dishes if dish['available']]

def get_all_dishes() -> List[Dict[str, any]]:
    """
    Получает полный список блюд.
    
    Returns:
        List[Dict[str, any]]: Полный список блюд.
    """
    return load_dishes()

def delete_dish(name: str) -> bool:
    """
    Удаляет блюдо из списка.
    
    Args:
        name (str): Название блюда.
    
    Returns:
        bool: True если блюдо успешно удалено, False если блюдо не найдено.
    """
    dishes = load_dishes()
    initial_length = len(dishes)
    dishes = [dish for dish in dishes if dish['name'] != name]
    if len(dishes) == initial_length:
        return False
    save_dishes(dishes)
    return True