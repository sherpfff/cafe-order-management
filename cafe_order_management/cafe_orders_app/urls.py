from django.urls import path
from cafe_orders_app import views 

app_name = 'cafe_orders_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('add_order/', views.add_order, name='add_order'),
    path('change_status/<int:id>/', views.change_status, name='change_status'),
    path('delete_order/<int:id>/', views.delete_order, name='delete_order'),
    path('search_orders/', views.search_orders, name='search_orders'),
    path('table_summary/', views.table_summary, name='table_summary'),
]