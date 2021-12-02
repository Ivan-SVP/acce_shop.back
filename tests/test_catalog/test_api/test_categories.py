import pytest
from django.urls import NoReverseMatch
from pytest_drf import (
    ViewSetTest,
    UsesGetMethod,
    UsesListEndpoint,
    Returns200,
    UsesDetailEndpoint,
    UsesPostMethod,
    Returns405
)
from pytest_drf.util import url_for
from pytest_lambda import lambda_fixture

pytestmark = pytest.mark.django_db


class TestCategoryViewSet(ViewSetTest):
    list_url = lambda_fixture(lambda: url_for('catalog:categories-list'))

    class TestList(
        UsesGetMethod,
        UsesListEndpoint,
        Returns200,
    ):
        pass

    class TestCreate(
        UsesPostMethod,
        UsesListEndpoint,
        Returns405,
    ):
        pass

    class TestDetailEndpoints(UsesDetailEndpoint):
        detail_url = lambda_fixture(lambda: ('catalog:categories-detail', 'some_slug'))

        def test_endpoints_exists(self, detail_url):
            with pytest.raises(NoReverseMatch):
                url_for(*detail_url)
