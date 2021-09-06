from django.db.models import Count
from rest_framework import viewsets

from apps.catalog.models import Product, Category
from apps.catalog.serializers.category import CategorySerializer
from apps.catalog.serializers.product import ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.annotate(Count('products'))
    lookup_field = 'slug'
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    lookup_field = 'slug'
    serializer_class = ProductSerializer
