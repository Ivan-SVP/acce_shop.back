import logging

import django_filters
from django.db.models import Min, Max
from rest_framework import viewsets

from apps.catalog.models import Product, Category
from apps.catalog.serializers.product import ProductSerializer

logger = logging.getLogger(__name__)


class ProductFilter(django_filters.FilterSet):
    category__slug = django_filters.CharFilter(method='filter_category')

    class Meta:
        model = Product
        fields = {
            'category__slug': ['exact'],
            'price': ['gte', 'lte'],
            'slug': ['in'],
        }

    def filter_category(self, queryset, name, value):
        try:
            category = Category.objects.get(slug=value)
            descendant__slugs = category.get_descendants(include_self=True).values_list('slug', flat=True)
            return queryset.filter(**{
                f'{name}__in': descendant__slugs,
            })
        except Exception as ex:
            logger.exception(ex)
            return queryset


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all().order_by('id')
    lookup_field = 'slug'
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
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

    def get_queryset(self):
        qs = super(ProductViewSet, self).get_queryset()
        if self.action == 'list':
            qs = qs.available().photo_required()
        return qs

    def clean_price_query_params(self, request):
        request.query_params._mutable = True
        for condition in self.filterset_class.get_fields().get('price', []):
            request.query_params.pop(f'price__{condition}', None)
        request.query_params._mutable = False

    def add_price_range_to_response(self, response):
        """Добавляет в ответ диапазон цен для текущей выборки."""
        if response.data.get('results'):
            price_range = self.filter_queryset(self.get_queryset()).aggregate(min_price=Min('price'),
                                                                              max_price=Max('price'))
            price_range_data = {'min_price': price_range['min_price'], 'max_price': price_range['max_price']}
            response.data.update(price_range_data)
