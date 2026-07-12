from django.contrib import admin

from .models import Label, TestCase, TestType


@admin.register(TestType)
class TestTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ("title", "test_type", "is_active", "created_by", "created_at", "updated_at")
    list_filter = ("is_active", "test_type", "tags")
    search_fields = ("title", "description")
    filter_horizontal = ("tags",)
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    raw_id_fields = ("created_by",)
