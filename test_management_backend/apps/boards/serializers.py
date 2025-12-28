from rest_framework import serializers

from .models import Board, BoardCapability, BoardLog


class BoardCapabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardCapability
        fields = ["id", "name", "description"]


class BoardSerializer(serializers.ModelSerializer):
    capabilities = BoardCapabilitySerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = [
            "id",
            "name",
            "serial_number",
            "description",
            "uart_port",
            "baud_rate",
            "data_bits",
            "stop_bits",
            "parity",
            "status",
            "last_seen_at",
            "capabilities",
        ]
        read_only_fields = ["id", "status", "last_seen_at", "capabilities"]


class BoardLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardLog
        fields = ["id", "board", "message", "level", "created_at"]
        read_only_fields = ["id", "created_at"]

