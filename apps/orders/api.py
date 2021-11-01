from rest_framework import viewsets
from apps.orders.models import Order
from apps.orders.serializers.order import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
