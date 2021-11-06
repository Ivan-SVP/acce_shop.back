from rest_framework import  mixins
from rest_framework.viewsets import GenericViewSet

from apps.catalog.models import Category
from apps.catalog.serializers.category import CategorySerializer


class CategoryViewSet(mixins.ListModelMixin,
                      GenericViewSet):
    queryset = Category.objects.get_with_products_count(
        Category.objects.root_nodes().filter(available=True),
    ).filter(products__count__gt=0)
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    pagination_class = None
