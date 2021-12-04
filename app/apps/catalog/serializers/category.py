from rest_framework import serializers

from apps.catalog.models import Category


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(source='products__count')
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'title',
            'slug',
            'image',
            'available',
            'products_count',
            'parent',
            'children',
        ]
        lookup_field = "slug"

    def get_children(self, obj):
        children = self.Meta.model.objects.get_with_products_count(
            obj.get_children().filter(
                available=True
            )).filter(products__count__gt=0)
        return CategorySerializer(children, many=True).data
