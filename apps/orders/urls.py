from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.orders.api import OrderViewSet

app_name = 'orders'

router = DefaultRouter()
router.register(r'', OrderViewSet, basename='orders')


urlpatterns = [
    path('', include(router.urls)),
]
