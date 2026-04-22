from django.contrib import admin

from .models import PriceHistory


@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ("id", "symbol", "price", "created_at_utc")
    list_filter = ("symbol",)
    search_fields = ("symbol",)
