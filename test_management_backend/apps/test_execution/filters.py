import django_filters

from .models import TestRun


class TestRunFilter(django_filters.FilterSet):
    status = django_filters.CharFilter(field_name="status")
    board = django_filters.NumberFilter(field_name="board_id")

    class Meta:
        model = TestRun
        fields = ["status", "board", "test_case"]

