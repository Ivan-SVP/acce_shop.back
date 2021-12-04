from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


def get_docs_schema_view():
    """Базовая конфигурация автодокументации API"""
    return get_schema_view(
        openapi.Info(
            title="AccE backend",
            default_version='v1',
            description="AccE backend API",
            contact=openapi.Contact(email="example@mail.com"),
        ),
        public=False,
        permission_classes=(permissions.IsAdminUser,),
    )
