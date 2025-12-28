"""Hardware board models."""
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone

from apps.core.validators import validate_uart_port


class Board(models.Model):
    """Hardware board (EVM) model."""

    STATUS_CHOICES = [
        ("CONNECTED", "Connected"),
        ("DISCONNECTED", "Disconnected"),
        ("OFFLINE", "Offline"),
        ("ERROR", "Error"),
    ]

    name = models.CharField(max_length=255, unique=True, db_index=True, validators=[MinLengthValidator(3)])
    serial_number = models.CharField(max_length=255, unique=True, db_index=True)
    description = models.TextField(blank=True)

    uart_port = models.CharField(max_length=50, validators=[validate_uart_port])
    baud_rate = models.IntegerField(
        default=115200,
        choices=[(9600, "9600"), (19200, "19200"), (38400, "38400"), (57600, "57600"), (115200, "115200")],
    )
    data_bits = models.IntegerField(default=8, choices=[(7, "7"), (8, "8")])
    stop_bits = models.IntegerField(default=1, choices=[(1, "1"), (2, "2")])
    parity = models.CharField(
        max_length=10,
        default="NONE",
        choices=[("NONE", "None"), ("EVEN", "Even"), ("ODD", "Odd")],
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OFFLINE", db_index=True)
    last_seen_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["serial_number"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.name

    def mark_seen(self):
        self.last_seen_at = timezone.now()
        self.save(update_fields=["last_seen_at"])


class BoardCapability(models.Model):
    """Capabilities supported by a board."""

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="capabilities")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("board", "name")
        ordering = ["name"]

    def __str__(self):
        return f"{self.board.name}: {self.name}"


class BoardLog(models.Model):
    """Log entries for board connectivity and execution events."""

    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="logs")
    message = models.TextField()
    level = models.CharField(
        max_length=10, choices=[("INFO", "INFO"), ("WARN", "WARN"), ("ERROR", "ERROR")], default="INFO"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

