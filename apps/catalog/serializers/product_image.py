from rest_framework import serializers

from apps.catalog.models import ProductImage


class BaseProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage


class ProductImageSerializer(BaseProductImageSerializer):

    class Meta(BaseProductImageSerializer.Meta):
        fields = ('image', )
