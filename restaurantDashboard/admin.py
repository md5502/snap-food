from django.contrib import admin

from .models import DayOfWeek, Food, FoodComment, Menu, Restaurant, RestaurantComment


class RestaurantCommentInline(admin.TabularInline):
    model = RestaurantComment
    extra = 1  # Number of empty forms to display
    fields = ("user", "text", "like_count", "dislike_count", "parent")
    readonly_fields = ("like_count", "dislike_count")


class FoodCommentInline(admin.TabularInline):
    model = FoodComment
    extra = 1  # Number of empty forms to display
    fields = ("user", "text", "like_count", "dislike_count", "parent")
    readonly_fields = ("like_count", "dislike_count")


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "rate", "address", "time_to_open", "time_to_close")
    list_filter = ("rate",)
    search_fields = ("name", "owner__username", "address")
    ordering = ("name",)
    inlines = [RestaurantCommentInline]  # Add RestaurantComment as inline

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "owner",
                    "logo",
                    "description",
                    "rate",
                    "call_number",
                    "address",
                ),
            },
        ),
        (
            "Operating Hours",
            {
                "fields": ("time_to_open", "time_to_close"),
            },
        ),
    )


class FoodAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "restaurant", "count", "rate", "discount")
    list_filter = ("rate",)
    search_fields = ("name", "restaurant__name")
    ordering = ("name",)
    inlines = [FoodCommentInline]

    fieldsets = (
        (
            None,
            {
                "fields": ("name", "price", "restaurant", "image", "rate", "count", "discount"),
            },
        ),
    )


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


class RestaurantCommentAdmin(admin.ModelAdmin):
    list_display = ("user", "restaurant", "text", "like_count", "dislike_count", "parent", "created_at")
    list_filter = ("restaurant", "user")
    search_fields = ("text", "user__username", "restaurant__name")
    ordering = ("-created_at",)
    readonly_fields = ("like_count", "dislike_count")


class FoodCommentAdmin(admin.ModelAdmin):
    list_display = ("user", "food", "text", "like_count", "dislike_count", "parent", "created_at")
    list_filter = ("food", "user")
    search_fields = ("text", "user__username", "restaurant__name")
    ordering = ("-created_at",)
    readonly_fields = ("like_count", "dislike_count")


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(DayOfWeek, DayOfWeekAdmin)
admin.site.register(FoodComment, FoodCommentAdmin)
admin.site.register(RestaurantComment, RestaurantCommentAdmin)
