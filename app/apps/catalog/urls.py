from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.catalog.api import ProductViewSet, CategoryViewSet

app_name = 'catalog'

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'products', ProductViewSet, basename='products')


urlpatterns = [
    path('', include(router.urls)),
]
