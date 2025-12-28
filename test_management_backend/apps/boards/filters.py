import django_filters

from .models import Board


class BoardFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status")
    name = django_filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Board
        fields = ["status", "name", "baud_rate"]

