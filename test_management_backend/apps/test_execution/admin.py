from django.contrib import admin

from .models import TestResult, TestRun


@admin.register(TestRun)
class TestRunAdmin(admin.ModelAdmin):
    list_display = ("id", "test_case", "board", "status", "started_at", "finished_at")
    list_filter = ("status", "board")
    search_fields = ("test_case__title",)


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ("test_run", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("message",)

