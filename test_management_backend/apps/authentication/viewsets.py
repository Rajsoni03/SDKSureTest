from django.contrib.auth import get_user_model
from rest_framework import permissions, viewsets

from .permissions import IsAdmin
from .serializers import UserSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """User management endpoints."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    queryset = User.objects.all().order_by("-date_joined")

