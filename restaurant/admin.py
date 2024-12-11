from django.contrib import admin

from .models import Restaurant, RestaurantComment


class RestaurantCommentInline(admin.TabularInline):
    model = RestaurantComment
    extra = 1
    fields = ("user", "text", "like_count", "dislike_count", "parent")
    readonly_fields = ("like_count", "dislike_count")


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "rate", "address", "time_to_open", "time_to_close")
    list_filter = ("rate",)
    search_fields = ("name", "owner__username", "address")
    ordering = ("name",)
    inlines = [RestaurantCommentInline]

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

class RestaurantCommentAdmin(admin.ModelAdmin):
    list_display = ("user", "restaurant", "text", "like_count", "dislike_count", "parent", "created_at")
    list_filter = ("restaurant", "user")
    search_fields = ("text", "user__username", "restaurant__name")
    ordering = ("-created_at",)
    readonly_fields = ("like_count", "dislike_count")

admin.site.register(RestaurantComment, RestaurantCommentAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
