from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import BoardFilter
from .models import Board, BoardLog
from .serializers import BoardLogSerializer, BoardSerializer


class BoardViewSet(viewsets.ModelViewSet):
    """CRUD operations for boards."""

    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Board.objects.all().order_by("name")
    filterset_class = BoardFilter
    search_fields = ["name", "serial_number", "uart_port"]
    ordering_fields = ["name", "serial_number", "last_seen_at"]

    @action(detail=True, methods=["get"])
    def logs(self, request, pk=None):
        logs = BoardLog.objects.filter(board_id=pk).order_by("-created_at")[:50]
        data = BoardLogSerializer(logs, many=True).data
        return Response(data)

