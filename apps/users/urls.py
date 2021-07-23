from django.conf import settings
from django.urls import path, include

urlpatterns = [
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]

if settings.DEBUG:
    urlpatterns.append(
        path('drf/', include('rest_framework.urls'))
    )
