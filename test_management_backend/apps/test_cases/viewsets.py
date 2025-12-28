from rest_framework import permissions, viewsets

from .models import Tag, TestCase, TestType
from .serializers import TagSerializer, TestCaseSerializer, TestTypeSerializer


class TestCaseViewSet(viewsets.ModelViewSet):
    """CRUD endpoints for test cases."""

    serializer_class = TestCaseSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = TestCase.objects.all().order_by("title")
    search_fields = ["title", "description"]
    filterset_fields = ["test_type", "is_active"]
    ordering_fields = ["title", "created_at"]


class TestTypeViewSet(viewsets.ModelViewSet):
    serializer_class = TestTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = TestType.objects.all().order_by("name")


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Tag.objects.all().order_by("name")

