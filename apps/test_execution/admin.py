from django.contrib import admin

from .models import TestResult, TestRun, TestScenario


class TestResultInline(admin.TabularInline):
    model = TestResult
    extra = 0
    readonly_fields = ("status", "message", "created_at")
    can_delete = False


@admin.register(TestScenario)
class TestScenarioAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "updated_by", "created_at", "updated_at")
    list_filter = ("labels",)
    search_fields = ("name", "description")
    filter_horizontal = ("test_cases", "labels")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    raw_id_fields = ("created_by", "updated_by")


@admin.register(TestRun)
class TestRunAdmin(admin.ModelAdmin):
    list_display = ("name", "created_by", "updated_by", "created_at", "updated_at")
    list_filter = ("labels",)
    search_fields = ("name", "description")
    filter_horizontal = ("scenarios", "labels")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    raw_id_fields = ("created_by", "updated_by")
    inlines = [TestResultInline]


@admin.register(TestResult)
class TestResultAdmin(admin.ModelAdmin):
    list_display = ("test_run", "status", "message", "created_at")
    list_filter = ("status",)
    search_fields = ("message",)
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    raw_id_fields = ("test_run",)
