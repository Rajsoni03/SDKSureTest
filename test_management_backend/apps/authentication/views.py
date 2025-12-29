from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


@extend_schema(
    tags=["Authentication"],
    summary="Login to obtain access and refresh tokens",
)
class LoginView(TokenObtainPairView):
    """JWT login endpoint (email/username + password)."""


@extend_schema(
    tags=["Authentication"],
    summary="Refresh access token",
)
class RefreshView(TokenRefreshView):
    """JWT refresh endpoint."""

