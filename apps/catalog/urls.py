from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.catalog.api import ProductViewSet

app_name = 'catalog'

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')


urlpatterns = [
    path('', include(router.urls)),
]
