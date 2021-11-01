from rest_framework import serializers

from apps.catalog.models import Category


class CategorySerializer(serializers.ModelSerializer):  # TODO только нужные поля
    products_count = serializers.IntegerField(source='products__count')

    class Meta:
        model = Category
        fields = '__all__'
        lookup_field = "slug"
