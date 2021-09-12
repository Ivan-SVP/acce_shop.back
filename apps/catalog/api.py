from django.db.models import Count, Min, Max
from rest_framework import viewsets, mixins
from rest_framework.viewsets import GenericViewSet

from apps.catalog.models import Product, Category
from apps.catalog.serializers.category import CategorySerializer
from apps.catalog.serializers.product import ProductSerializer


class CategoryViewSet(mixins.ListModelMixin,
                      GenericViewSet):
    queryset = Category.objects.annotate(Count('products'))
    lookup_field = 'slug'
    serializer_class = CategorySerializer
    pagination_class = None


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    lookup_field = 'slug'
    serializer_class = ProductSerializer

    filterset_fields = {
        'category__slug': ['exact'],
        'price': ['gte', 'lte'],
    }
    search_fields = [
        'title',
    ]
    ordering_fields = [
        'title',
        'price'
    ]

    def list(self, request, *args, **kwargs):
        if request.query_params.get('update_price_range'):
            self.clean_price_query_params(request)

        response = super().list(request, *args, **kwargs)
        self.add_price_range_to_response(response)
        return response

    def add_price_range_to_response(self, response):
        """Добавляет в ответ диапазон цен для текущей выборки."""
        if response.data.get('results'):
            price_range = self.filter_queryset(self.get_queryset()).aggregate(min_price=Min('price'), max_price=Max('price'))
            price_range_data = {'min_price': price_range['min_price'], 'max_price': price_range['max_price']}
            response.data.update(price_range_data)

    def clean_price_query_params(self, request):
        request.query_params._mutable = True
        for condition in self.filterset_fields['price']:
            request.query_params.pop(f'price__{condition}', None)
        request.query_params._mutable = False
