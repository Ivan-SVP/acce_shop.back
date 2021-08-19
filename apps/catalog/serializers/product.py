from rest_framework import serializers

from apps.catalog.models import Product
from apps.catalog.serializers.product_image import ProductImageSerializer


class BaseProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        lookup_field = "slug"


class ProductSerializer(BaseProductSerializer):
    discount_price = serializers.DecimalField(decimal_places=0, max_digits=7)
    product_images = ProductImageSerializer(many=True)

    class Meta(BaseProductSerializer.Meta):
        fields = '__all__'
