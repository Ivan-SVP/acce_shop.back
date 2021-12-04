from django.db import transaction
from rest_framework import serializers

from apps.catalog.models import Product
from apps.orders.models import Order, OrderItem


class OrderItemsSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        queryset=Product.objects.available(),
        slug_field='slug',
    )

    class Meta:
        model = OrderItem
        fields = ['product', 'price', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemsSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'name', 'email', 'phone', 'address', 'comment', 'uuid', 'order_items']

    @transaction.atomic
    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')

        order = super(OrderSerializer, self).create(validated_data)
        OrderItem.objects.bulk_create(map(lambda item: OrderItem(order=order, **item), order_items_data))

        return order
