from rest_framework import viewsets, mixins

from apps.orders.models import Order
from apps.orders.serializers.order import OrderSerializer


class OrderViewSet(mixins.CreateModelMixin,
                   viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
