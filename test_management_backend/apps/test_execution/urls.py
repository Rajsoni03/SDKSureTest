from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import TestRunViewSet

router = DefaultRouter()
router.register(r"test-runs", TestRunViewSet, basename="test-run")

urlpatterns = [
    path("", include(router.urls)),
]

