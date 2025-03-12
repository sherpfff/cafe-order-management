# cafe_orders_app/tests.py

from django.test import TestCase, Client
from django.urls import reverse
from .models import Order
from .serializers import OrderSerializer
from django.core.exceptions import ValidationError
from typing import List, Dict
from django.db.models import Sum
class OrderModelTest(TestCase):
    """
    Тесты для модели Order.
    """

    def test_save_method_calculates_total_price(self) -> None:
        """
        Проверяет, что метод save() корректно рассчитывает общую стоимость заказа.
        """
        order = Order.objects.create(
            table_number=1,
            items=[
                {"name": "Кофе", "price": 150},
                {"name": "Пирожное", "price": 200}
            ]
        )
        self.assertEqual(order.total_price, 350)

    def test_invalid_items_raise_validation_error(self) -> None:
        """
        Проверяет, что невалидные данные в поле items вызывают ValidationError.
        """
        order_data = {
            'table_number': 1,
            'items': "invalid_data"  # Неправильные данные, ожидаем ошибку
        }
        
        serializer = OrderSerializer(data=order_data)
        self.assertFalse(serializer.is_valid())  # Проверка, что сериализатор не прошел валидацию
        self.assertIn('items', serializer.errors)  # Проверка, что ошибка связана с полем 'items'

    def test_empty_items_default_total_price(self) -> None:
        """
        Проверяет, что при пустом списке блюд total_price равен 0.
        """
        order = Order.objects.create(
            table_number=1,
            items=[]
        )
        self.assertEqual(order.total_price, 0)

class OrderViewsTest(TestCase):
    """
    Тесты для представлений (views).
    """

    def setUp(self) -> None:
        """
        Создает клиент и тестовый заказ перед каждым тестом.
        """
        self.client = Client()
        self.order = Order.objects.create(
            table_number=1,
            items=[{"name": "Чай", "price": 100}]  # Создаем заказ с чаем
        )

    def test_index_view(self) -> None:
        """
        Проверяет отображение списка заказов на главной странице.
        """
        response = self.client.get(reverse('cafe_orders_app:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Все заказы")

    def test_add_order_view(self) -> None:
        """
        Проверяет добавление нового заказа через форму.
        """
        data: Dict[str, str] = {
            'table_number': 2,
            'items': '[{"name": "Чай", "price": 100}]'
        }
        response = self.client.post(reverse('cafe_orders_app:add_order'), data)
        self.assertEqual(response.status_code, 302)  # Перенаправление после успешного создания
        self.assertEqual(Order.objects.count(), 2)

    def test_change_status_view(self) -> None:
        """
        Проверяет изменение статуса заказа.
        """
        url = reverse('cafe_orders_app:change_status', args=[self.order.id])
        response = self.client.post(url, {'status': 'ready'})
        self.assertEqual(response.status_code, 302)  # Перенаправление
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'ready')

    def test_delete_order_view(self) -> None:
        """
        Проверяет удаление заказа.
        """
        url = reverse('cafe_orders_app:delete_order', args=[self.order.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Перенаправление
        self.assertEqual(Order.objects.count(), 0)

    def test_search_orders_view(self):
        """
        Проверяет поиск заказов по номеру стола или статусу.
        """
        # Создаем заказ с блюдом "Чай"
        Order.objects.create(
            table_number=1,
            items=[{"name": "Чай", "price": 100}],
            status='pending'
        )
    
        # Ищем заказ по названию блюда
        search_query = "Чай"
        response = self.client.get(reverse('cafe_orders_app:search_orders'), {'search_query': search_query})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Чай")  # Проверяем, что найден заказ с чаем
    
    def test_calculate_revenue(self) -> None:
        """
        Проверяет расчет общей выручки по оплаченным заказам.
        """
        # Создаем оплаченный заказ
        Order.objects.create(
            table_number=1,
            items=[{"name": "Кофе", "price": 150}],
            status=Order.PAID
        )
        
        # Проверяем, что выручка корректно рассчитана
        total_revenue = Order.objects.filter(status=Order.PAID).aggregate(
            total=Sum('total_price')
        )['total'] or 0
        self.assertEqual(total_revenue, 150)