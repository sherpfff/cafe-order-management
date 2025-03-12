# -*- coding: utf-8 -*-
"""
API представления для работы с заказами.
Created on Tue Mar 11 06:59:50 2025
@author: sherp
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Sum
from typing import List, Dict, Any
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
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]  # Разрешить доступ всем

    @action(detail=False, methods=['get'], url_path='calculate-revenue')
    def calculate_revenue(self, request) -> Response:
        """
        Расчет общей выручки по оплаченным заказам.
        
        Returns:
            Response: JSON с общей выручкой.
        """
        total_revenue = (
            Order.objects.filter(status=Order.PAID)
            .aggregate(total=Sum('total_price'))['total'] or 0
        )
        return Response({'total_revenue': total_revenue}, status=status.HTTP_200_OK)

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
        order = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(Order.STATUS_CHOICES):
            return Response(
                {'error': 'Недопустимый статус'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
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
        table_totals = (
            Order.objects.values('table_number')
            .annotate(total_price=Sum('total_price'))
            .order_by('table_number')
        )
        return Response(table_totals, status=status.HTTP_200_OK)