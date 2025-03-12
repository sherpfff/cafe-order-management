from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.db.models import Sum
from typing import List, Dict
from .models import Order, Dish
from .forms import OrderForm

def index(request):
    """
    Главная страница со списком всех заказов.
    Поддерживает фильтрацию заказов по статусу.
    Args:
        request: HTTP-запрос.
    Returns:
        HttpResponse: HTML-страница со списком заказов.
    """
    # Получаем параметр status из GET-запроса
    status_filter = request.GET.get('status', None)
    
    # Базовый QuerySet
    orders = Order.objects.all()
    
    # Применяем фильтр, если параметр status указан
    if status_filter in dict(Order.STATUS_CHOICES):
        orders = orders.filter(status=status_filter)
    
    return render(request, 'cafe_orders_app/index.html', {
        'orders': orders,
        'status_filter': status_filter,  # Передаем текущий фильтр в шаблон
        'STATUS_CHOICES': Order.STATUS_CHOICES  # Передаем доступные статусы
    })

def add_order(request: HttpRequest) -> HttpResponse:
    """
    Добавление нового заказа.
    Args:
        request (HttpRequest): HTTP-запрос.
    Returns:
        HttpResponse: Перенаправление на главную страницу после успешного добавления.
    """
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cafe_orders_app:index')
    else:
        form = OrderForm()
    return render(request, 'cafe_orders_app/add_order.html', {'form': form})

def change_status(request: HttpRequest, id: int) -> HttpResponse:
    """
    Изменение статуса заказа.
    Args:
        request (HttpRequest): HTTP-запрос.
        id (int): ID заказа.
    Returns:
        HttpResponse: Перенаправление на главную страницу после изменения статуса.
    """
    order = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            return redirect('cafe_orders_app:index')
    return render(request, 'cafe_orders_app/change_status.html', {'order': order})

def delete_order(request: HttpRequest, id: int) -> HttpResponse:
    """
    Удаление заказа.
    Args:
        request (HttpRequest): HTTP-запрос.
        id (int): ID заказа.
    Returns:
        HttpResponse: Перенаправление на главную страницу после удаления заказа.
    """
    order = get_object_or_404(Order, id=id)
    if request.method == 'POST':
        order.delete()
        return redirect('cafe_orders_app:index')
    return render(request, 'cafe_orders_app/delete_order.html', {'order': order})

def search_orders(request: HttpRequest) -> HttpResponse:
    """
    Поиск заказов по номеру стола или названию блюда.
    Args:
        request (HttpRequest): HTTP-запрос.
    Returns:
        HttpResponse: HTML-страница с результатами поиска.
    """
    query = request.GET.get('search_query', '')
    if query.isdigit():
        orders = Order.objects.filter(table_number=int(query))
    else:
        orders = Order.objects.filter(dishes__name__icontains=query).distinct()
    return render(request, 'cafe_orders_app/search_orders.html', {'orders': orders, 'query': query})

def combined_view(request: HttpRequest) -> HttpResponse:
    """
    Объединенная страница с добавлением, поиском и отображением заказов.
    Args:
        request (HttpRequest): HTTP-запрос.
    Returns:
        HttpResponse: HTML-страница с объединенной функциональностью.
    """
    # Поиск заказов
    search_query = request.GET.get('search_query', '')
    if search_query.isdigit():
        orders = Order.objects.filter(table_number=int(search_query))
    else:
        orders = Order.objects.filter(dishes__name__icontains=search_query).distinct()

    # Добавление заказа
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cafe_orders_app:combined_view')
    else:
        form = OrderForm()

    # Все заказы
    all_orders = Order.objects.all()

    return render(request, 'cafe_orders_app/combined_view.html', {
        'orders': orders,
        'all_orders': all_orders,
        'form': form,
        'search_query': search_query,
    })

def table_summary(request: HttpRequest) -> HttpResponse:
    """
    Страница с общей стоимостью заказов для каждого стола.
    Args:
        request (HttpRequest): HTTP-запрос.
    Returns:
        HttpResponse: HTML-страница с общей стоимостью заказов.
    """
    # Группируем заказы по столам и рассчитываем общую стоимость
    table_totals = (
        Order.objects.values('table_number')
        .annotate(total_price=Sum('total_price'))
        .order_by('table_number')
    )

    # Получаем все заказы для отображения деталей
    orders = Order.objects.all()

    return render(request, 'cafe_orders_app/table_summary.html', {
        'table_totals': table_totals,
        'orders': orders,
    })