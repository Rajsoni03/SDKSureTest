from rest_framework import serializers

from .models import TestResult, TestRun


class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = ["id", "status", "message", "created_at"]
        read_only_fields = ["id", "created_at"]


class TestRunSerializer(serializers.ModelSerializer):
    results = TestResultSerializer(many=True, read_only=True)

    class Meta:
        model = TestRun
        fields = [
            "id",
            "test_case",
            "board",
            "initiated_by",
            "status",
            "started_at",
            "finished_at",
            "output_log",
            "results",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "started_at", "finished_at", "results", "created_at", "updated_at"]

