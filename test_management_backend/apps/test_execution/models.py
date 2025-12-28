"""Models for managing test execution."""
from django.conf import settings
from django.db import models
from django.utils import timezone


class TestRun(models.Model):
    """Represents a single execution of a test case on a board."""

    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("RUNNING", "Running"),
        ("PAUSED", "Paused"),
        ("COMPLETED", "Completed"),
        ("FAILED", "Failed"),
        ("KILLED", "Killed"),
    ]

    test_case = models.ForeignKey("test_cases.TestCase", on_delete=models.CASCADE, related_name="test_runs")
    board = models.ForeignKey("boards.Board", on_delete=models.CASCADE, related_name="test_runs")
    initiated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="started_test_runs"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING", db_index=True)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    output_log = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["status"])]

    def __str__(self):
        return f"TestRun #{self.id} ({self.status})"

    def start(self):
        self.status = "RUNNING"
        self.started_at = timezone.now()
        self.save(update_fields=["status", "started_at"])

    def complete(self, success: bool = True):
        self.status = "COMPLETED" if success else "FAILED"
        self.finished_at = timezone.now()
        self.save(update_fields=["status", "finished_at"])

    def can_pause(self):
        return self.status == "RUNNING"

    def can_kill(self):
        return self.status in {"RUNNING", "PAUSED"}


class TestResult(models.Model):
    """Result log entries for a test run."""

    STATUS_CHOICES = [
        ("INFO", "Info"),
        ("WARN", "Warn"),
        ("ERROR", "Error"),
    ]

    test_run = models.ForeignKey(TestRun, on_delete=models.CASCADE, related_name="results")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="INFO")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

