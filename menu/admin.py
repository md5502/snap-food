from django.contrib import admin

from .models import DayOfWeek, Menu


class MenuAdmin(admin.ModelAdmin):
    list_display = ("name", "restaurant", "available_from", "available_to", "is_active")
    list_filter = ("restaurant", "is_active", "available_days")
    search_fields = ("name", "restaurant__name")
    ordering = ("name",)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "restaurant",
                    "description",
                    "available_from",
                    "available_to",
                    "is_active",
                    "available_days",
                ),
            },
        ),
        (
            "Foods",
            {
                "fields": ("foods",),
            },
        ),
    )


class DayOfWeekAdmin(admin.ModelAdmin):
    list_display = ("day",)
    ordering = ("day",)

admin.site.register(Menu, MenuAdmin)
admin.site.register(DayOfWeek, DayOfWeekAdmin)

