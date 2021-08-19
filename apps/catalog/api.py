from rest_framework import viewsets

from apps.catalog.models import Product
from apps.catalog.serializers.product import ProductSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    lookup_field = 'slug'
    serializer_class = ProductSerializer
