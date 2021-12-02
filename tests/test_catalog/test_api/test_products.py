import pytest
from pytest_drf import (
    ViewSetTest,
    UsesGetMethod,
    UsesListEndpoint,
    Returns200,
    UsesPostMethod,
    UsesDetailEndpoint,
    Returns405,
    UsesPatchMethod,
    UsesDeleteMethod,
    UsesPutMethod
)
from pytest_drf.util import url_for
from pytest_lambda import lambda_fixture

from tests.factories.catalog import ProductFactory

pytestmark = pytest.mark.django_db


class TestProductViewSet(ViewSetTest):
    list_url = lambda_fixture(lambda: url_for('catalog:products-list'))
    detail_url = lambda_fixture(lambda product: url_for('catalog:products-detail', product.slug))

    class TestList(
        UsesGetMethod,
        UsesListEndpoint,
        Returns200,
    ):
        pass

    class TestRetrieve(
        UsesGetMethod,
        UsesDetailEndpoint,
        Returns200,
    ):
        product = lambda_fixture(lambda: ProductFactory.create())

    class TestCreate(
        UsesPostMethod,
        UsesListEndpoint,
        Returns405,
    ):
        pass

    class TestUpdate(
        UsesPutMethod,
        UsesDetailEndpoint,
        Returns405,
    ):
        product = lambda_fixture(lambda: ProductFactory.create())

    class TestPartialUpdate(
        UsesPatchMethod,
        UsesDetailEndpoint,
        Returns405,
    ):
        product = lambda_fixture(lambda: ProductFactory.create())

    class TestDestroy(
        UsesDeleteMethod,
        UsesDetailEndpoint,
        Returns405,
    ):
        product = lambda_fixture(lambda: ProductFactory.create())
