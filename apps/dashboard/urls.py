from rest_framework.routers import DefaultRouter
from .viewsets import DashboardMetricViewSet

router = DefaultRouter()
router.register(r"dashboard-metrics", DashboardMetricViewSet, basename="dashboard-metrics")

urlpatterns = router.urls
