from django.contrib import admin

from .models import Board, BoardCapability, BoardLog


class BoardCapabilityInline(admin.TabularInline):
    model = BoardCapability
    extra = 1


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ("name", "serial_number", "status", "uart_port", "baud_rate", "last_seen_at")
    search_fields = ("name", "serial_number", "uart_port")
    list_filter = ("status", "baud_rate")
    inlines = [BoardCapabilityInline]


@admin.register(BoardLog)
class BoardLogAdmin(admin.ModelAdmin):
    list_display = ("board", "level", "created_at")
    list_filter = ("level",)
    search_fields = ("board__name", "message")

