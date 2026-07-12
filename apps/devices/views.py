import requests as http_requests
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .filters import BoardFilter
from .models import Capability, Relay, Workstation, Board
from .serializers import (
    CapabilitySerializer,
    RelaySerializer,
    WorkstationSerializer,
    BoardSerializer,
)

# Create your views here.
class CapabilityViewSet(viewsets.ModelViewSet):
    """CRUD operations for board capabilities."""

    serializer_class = CapabilitySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Capability.objects.all().order_by("name")
    search_fields = ["name"]
    ordering_fields = ["name", "created_at", "updated_at"]


class RelayViewSet(viewsets.ModelViewSet):
    """CRUD operations for relays."""

    serializer_class = RelaySerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Relay.objects.all().order_by("relay_name")
    search_fields = ["relay_name", "ip_address"]
    ordering_fields = ["relay_name", "status", "created_at", "updated_at", "last_checked_at"]



class WorkstationViewSet(viewsets.ModelViewSet):
    """CRUD operations for workstations."""

    serializer_class = WorkstationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Workstation.objects.all().order_by("hostname")
    search_fields = ["hostname", "ip_address", "domain_name"]
    ordering_fields = ["hostname", "status", "os_version", "created_at", "updated_at"]

    @action(detail=True, methods=["post"], url_path="ping")
    def ping(self, request, pk=None):
        """Hit the workstation's health endpoint and update its status."""
        workstation = self.get_object()
        host = workstation.domain_name or workstation.ip_address
        url = f"http://{host}:5500/health"
        try:
            resp = http_requests.get(url, timeout=5)
            health_data = resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
            is_ok = resp.status_code == 200 and health_data.get("status") == "ok"
            workstation.status = "ONLINE" if is_ok else "OFFLINE"
            workstation.last_heartbeat_at = timezone.now()
            workstation.save(update_fields=["status", "last_heartbeat_at"])
            return Response({
                "health": health_data,
                "workstation": WorkstationSerializer(workstation).data,
            })
        except Exception as exc:
            workstation.status = "OFFLINE"
            workstation.last_heartbeat_at = timezone.now()
            workstation.save(update_fields=["status", "last_heartbeat_at"])
            return Response(
                {"detail": f"Health check failed: {exc}",
                 "workstation": WorkstationSerializer(workstation).data},
                status=status.HTTP_502_BAD_GATEWAY,
            )


class BoardViewSet(viewsets.ModelViewSet):
    """CRUD operations for boards."""

    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = (
        Board.objects.select_related("workstation", "relay")
        .prefetch_related("capabilities")
        .all()
        .order_by("name")
    )
    filterset_class = BoardFilter
    search_fields = ["name", "hardware_serial_number", "project", "platform", "test_farm", "board_ip"]
    ordering_fields = [
        "name",
        "hardware_serial_number",
        "project",
        "platform",
        "status",
        "test_farm",
        "created_at",
        "updated_at",
        "last_heartbeat_at",
    ]