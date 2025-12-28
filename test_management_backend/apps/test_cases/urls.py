from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .viewsets import TagViewSet, TestCaseViewSet, TestTypeViewSet

router = DefaultRouter()
router.register(r"test-cases", TestCaseViewSet, basename="test-case")
router.register(r"test-types", TestTypeViewSet, basename="test-type")
router.register(r"tags", TagViewSet, basename="tag")

urlpatterns = [
    path("", include(router.urls)),
]

