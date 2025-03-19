from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .api_views import OrderViewSet

# Настройка роутера
router = DefaultRouter()
router.register(r'orders', OrderViewSet)

# Генерация документации
schema_view = get_schema_view(
    openapi.Info(
        title="Orders API",
        default_version='v1',
        description="API для управления заказами",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

# Определение URL-маршрутов
urlpatterns = [
    path('api/v1/', include(router.urls)),  # Маршруты API
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # ReDoc
]
