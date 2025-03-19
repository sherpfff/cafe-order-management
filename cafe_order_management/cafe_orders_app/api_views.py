# -*- coding: utf-8 -*-
"""
API представления для работы с заказами.
Created on Tue Mar 11 06:59:50 2025
@author: sherp
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError
from django.db.models import Sum
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """
    API ViewSet для управления заказами.

    Предоставляет CRUD-операции для модели Order:
    - Получение списка заказов (GET /orders/)
    - Создание нового заказа (POST /orders/)
    - Обновление существующего заказа (PUT /orders/<id>/)
    - Удаление заказа (DELETE /orders/<id>/)

    Дополнительно:
    - Метод calculate_revenue для расчета общей выручки.
    - Метод change_status для изменения статуса заказа.
    - Метод table_summary для сводки по столам.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]  # Разрешить доступ только авторизованным пользователям

    # Пагинация
    pagination_class = None  # Можно настроить пагинацию через `rest_framework.pagination.PageNumberPagination`

    @action(detail=False, methods=['get'], url_path='calculate-revenue')
    def calculate_revenue(self, request) -> Response:
        """
        Расчет общей выручки по оплаченным заказам.

        Returns:
            Response: JSON с общей выручкой.
        """
        try:
            total_revenue = (
                Order.objects.filter(status=Order.PAID)
                .aggregate(total=Sum('total_price'))['total'] or 0
            )
            return Response({'total_revenue': total_revenue}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'], url_path='change-status')
    def change_status(self, request, pk=None) -> Response:
        """
        Изменение статуса заказа.

        Args:
            request: HTTP-запрос.
            pk (int): ID заказа.

        Returns:
            Response: JSON с новым статусом заказа.
        """
        try:
            order = self.get_object()  # Может вызвать NotFound, если объект не существует
        except Order.DoesNotExist:
            raise NotFound("Заказ не найден")

        new_status = request.data.get('status')
        if not new_status or new_status not in dict(Order.STATUS_CHOICES):
            raise ValidationError("Недопустимый статус")

        order.status = new_status
        order.save()
        return Response(
            {'message': f'Статус заказа изменен на {new_status}'},
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=['get'], url_path='table-summary')
    def table_summary(self, request) -> Response:
        """
        Сводка по столам: общая стоимость заказов для каждого стола.

        Returns:
            Response: JSON с данными о столах и их общей стоимости.
        """
        try:
            table_totals = (
                Order.objects.values('table_number')
                .annotate(total_price=Sum('total_price'))
                .order_by('table_number')
            )
            return Response(table_totals, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Добавляем документацию для методов
    calculate_revenue.__doc__ += """
    Responses:
        200 OK:
            {
                "total_revenue": 5000
            }
        500 Internal Server Error:
            {
                "error": "Ошибка сервера"
            }
    """

    change_status.__doc__ += """
    Parameters:
        status (str): Новый статус заказа (например, PAID, DELIVERED).

    Responses:
        200 OK:
            {
                "message": "Статус заказа изменен на DELIVERED"
            }
        400 Bad Request:
            {
                "error": "Недопустимый статус"
            }
        404 Not Found:
            {
                "error": "Заказ не найден"
            }
    """

    table_summary.__doc__ += """
    Responses:
        200 OK:
            [
                {
                    "table_number": 1,
                    "total_price": 1500
                },
                {
                    "table_number": 2,
                    "total_price": 3000
                }
            ]
        500 Internal Server Error:
            {
                "error": "Ошибка сервера"
            }
    """
