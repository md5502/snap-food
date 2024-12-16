from django.contrib import admin

from .models import Food


class FoodAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "restaurant", "count", "rate", "discount")
    list_filter = ("rate",)
    search_fields = ("name", "restaurant__name")
    ordering = ("name",)

    fieldsets = (
        (
            None,
            {
                "fields": ("name", "price", "restaurant", "image", "rate", "count", "discount"),
            },
        ),
    )


class FoodCommentAdmin(admin.ModelAdmin):
    list_display = ("user", "food", "text", "like_count", "dislike_count", "parent", "created_at")
    list_filter = ("food", "user")
    search_fields = ("text", "user__username", "restaurant__name")
    ordering = ("-created_at",)
    readonly_fields = ("like_count", "dislike_count")


admin.site.register(Food, FoodAdmin)
