from rest_framework import serializers

from .models import Tag, TestCase, TestType


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class TestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestType
        fields = ["id", "name", "description"]


class TestCaseSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, required=False, read_only=True)
    test_type = TestTypeSerializer(read_only=True)

    class Meta:
        model = TestCase
        fields = [
            "id",
            "title",
            "description",
            "test_type",
            "tags",
            "is_active",
            "created_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]

