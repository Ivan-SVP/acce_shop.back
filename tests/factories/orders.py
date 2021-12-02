import factory
import uuid
from apps.orders.models import Order, OrderItem
from tests.factories.catalog import ProductFactory


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    name = 'Ivan'
    email = 'ivan@email.com'
    phone = '88003000600'
    uuid = factory.Sequence(lambda n: uuid.uuid4().hex)


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    price = 100
    quantity = 1
