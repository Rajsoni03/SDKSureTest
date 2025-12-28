from rest_framework import permissions, viewsets

from .filters import TestRunFilter
from .models import TestRun
from .permissions import IsTestRunner
from .serializers import TestRunSerializer


class TestRunViewSet(viewsets.ModelViewSet):
    """Manage test run lifecycle."""

    serializer_class = TestRunSerializer
    permission_classes = [permissions.IsAuthenticated, IsTestRunner]
    queryset = TestRun.objects.select_related("test_case", "board", "initiated_by").order_by("-created_at")
    filterset_class = TestRunFilter
    search_fields = ["test_case__title"]
    ordering_fields = ["created_at", "status"]

