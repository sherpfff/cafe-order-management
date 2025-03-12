# -*- coding: utf-8 -*-
"""
Интерфейс для управления блюдами.
Created on Wed Mar 12 01:15:42 2025
@author: sherp
"""
from typing import Optional
from dish_manager import (
    add_dish,
    update_availability,
    get_available_dishes,
    get_all_dishes,
)

def show_menu() -> None:
    """
    Отображает главное меню программы.
    """
    print("\nМенеджер блюд:")
    print("1. Добавить новое блюдо")
    print("2. Изменить статус наличия блюда")
    print("3. Показать все блюда")
    print("4. Показать доступные блюда")
    print("5. Выход")

def add_dish_interface() -> None:
    """
    Интерфейс для добавления нового блюда.
    """
    name = input("Введите название блюда: ").strip()
    if not name:
        print("Название блюда не может быть пустым!")
        return

    try:
        price = float(input("Введите цену блюда: "))
        if price <= 0:
            raise ValueError
    except ValueError:
        print("Цена должна быть положительным числом!")
        return

    if add_dish(name, price):
        print(f"Блюдо '{name}' успешно добавлено!")
    else:
        print(f"Блюдо '{name}' уже существует!")

def update_availability_interface() -> None:
    """
    Интерфейс для обновления статуса наличия блюда.
    """
    name = input("Введите название блюда: ").strip()
    if not name:
        print("Название блюда не может быть пустым!")
        return

    status = input("Есть в наличии? (y/n): ").lower().strip()
    if status not in ['y', 'n']:
        print("Некорректный ввод! Введите 'y' или 'n'.")
        return

    available = status == 'y'
    if update_availability(name, available):
        print(f"Статус блюда '{name}' обновлен!")
    else:
        print(f"Блюдо '{name}' не найдено!")

def show_dishes(dishes: list, title: str) -> None:
    """
    Отображает список блюд.
    
    Args:
        dishes (list): Список блюд для отображения.
        title (str): Заголовок списка.
    """
    print(f"\n{title}:")
    if not dishes:
        print("Список пуст.")
        return

    for i, dish in enumerate(dishes, 1):
        availability = "✅" if dish['available'] else "❌"
        print(f"{i}. {dish['name']} - {dish['price']} руб. {availability}")

def main() -> None:
    """
    Основная функция для запуска интерфейса.
    """
    while True:
        show_menu()
        choice = input("Выберите действие: ").strip()

        if choice == '1':
            add_dish_interface()
        elif choice == '2':
            update_availability_interface()
        elif choice == '3':
            show_dishes(get_all_dishes(), "Все блюда")
        elif choice == '4':
            show_dishes(get_available_dishes(), "Доступные блюда")
        elif choice == '5':
            print("До свидания!")
            break
        else:
            print("Некорректный выбор! Пожалуйста, выберите число от 1 до 5.")

if __name__ == "__main__":
    main()