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
        """Check health and pull system stats from the workstation agent."""
        workstation = self.get_object()
        host = workstation.domain_name or workstation.ip_address
        headers = {"Authorization": workstation.auth_token} if workstation.auth_token else {}
        now = timezone.now()

        # 1. Health check
        try:
            health_resp = http_requests.get(f"http://{host}:5500/health", timeout=5)
            is_ok = health_resp.status_code == 200 and health_resp.json().get("status") == "ok"
        except Exception:
            is_ok = False

        update_fields = ["status", "last_heartbeat_at"]
        workstation.status = "ONLINE" if is_ok else "OFFLINE"
        workstation.last_heartbeat_at = now

        # 2. Pull system stats and SysConn version (only if online and auth_token set)
        stats = {}
        if is_ok and workstation.auth_token:
            try:
                stats_resp = http_requests.get(
                    f"http://{host}:5500/api/v1/system/stats",
                    headers=headers,
                    timeout=5,
                )
                if stats_resp.status_code == 200:
                    stats = stats_resp.json()
                    workstation.cpu_utilization = stats.get("cpu", {}).get("percent", workstation.cpu_utilization)
                    workstation.ram_utilization = stats.get("memory", {}).get("percent", workstation.ram_utilization)
                    workstation.disk_utilization = stats.get("disk", {}).get("percent", workstation.disk_utilization)
                    workstation.docker_container_count = stats.get("docker", {}).get("total", workstation.docker_container_count)
                    update_fields += ["cpu_utilization", "ram_utilization", "disk_utilization", "docker_container_count"]
            except Exception:
                pass

            try:
                ver_resp = http_requests.get(
                    f"http://{host}:5500/version",
                    headers=headers,
                    timeout=5,
                )
                if ver_resp.status_code == 200:
                    data = ver_resp.json()
                    workstation.sysconn_version = data.get("version", workstation.sysconn_version)
                    workstation.sysconn_commit = data.get("commit", workstation.sysconn_commit)
                    update_fields += ["sysconn_version", "sysconn_commit"]
            except Exception:
                pass

        workstation.save(update_fields=update_fields)
        code = status.HTTP_200_OK if is_ok else status.HTTP_502_BAD_GATEWAY
        return Response(
            {"stats": stats, "workstation": WorkstationSerializer(workstation).data},
            status=code,
        )

    @action(detail=True, methods=["post"], url_path="update-agent")
    def update_agent(self, request, pk=None):
        """Trigger a SysConn self-update on the workstation."""
        workstation = self.get_object()
        if not workstation.auth_token:
            return Response({"detail": "No auth_token configured for this workstation."}, status=status.HTTP_400_BAD_REQUEST)
        host = workstation.domain_name or workstation.ip_address
        headers = {"Authorization": workstation.auth_token}
        try:
            resp = http_requests.post(f"http://{host}:5500/update", headers=headers, timeout=30)
            return Response({"detail": resp.text, "status_code": resp.status_code}, status=status.HTTP_200_OK)
        except http_requests.exceptions.ConnectionError:
            return Response({"detail": "Could not connect to workstation agent."}, status=status.HTTP_502_BAD_GATEWAY)
        except http_requests.exceptions.Timeout:
            return Response({"detail": "Update request timed out."}, status=status.HTTP_504_GATEWAY_TIMEOUT)
        except Exception as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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