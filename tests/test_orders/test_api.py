import pytest
from django.urls import NoReverseMatch
from pytest_drf import (
    ViewSetTest,
    UsesGetMethod,
    UsesListEndpoint,
    UsesDetailEndpoint,
    UsesPostMethod,
    Returns405,
    Returns201
)
from pytest_drf.util import url_for
from pytest_lambda import lambda_fixture

from tests.factories.orders import OrderFactory, OrderItemFactory

pytestmark = pytest.mark.django_db


class TestOrderViewSet(ViewSetTest):
    list_url = lambda_fixture(lambda: url_for('orders:orders-list'))

    class TestCreate(
        UsesPostMethod,
        UsesListEndpoint,
        Returns201,
    ):
        @pytest.fixture
        def data(self):
            order = OrderFactory.stub().__dict__
            item = OrderItemFactory.create()
            order['order_items'] = [{
                'product': item.product.slug,
                'price': item.price,
                'quantity': item.quantity,
            }]
            return order

    class TestList(
        UsesGetMethod,
        UsesListEndpoint,
        Returns405,
    ):
        pass

    class TestDetailEndpoints(UsesDetailEndpoint):
        detail_url = lambda_fixture(lambda: ('orders:orders-detail', 1))

        def test_endpoints_exists(self, detail_url):
            with pytest.raises(NoReverseMatch):
                url_for(*detail_url)
