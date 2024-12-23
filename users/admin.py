from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Address, CustomUser, UserProfile


class AddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "title",
        "full_name",
        "city",
        "state",
        "postal_code",
        "is_default",
    )
    list_filter = ("is_default", "country", "state")
    search_fields = ("full_name", "city", "state", "postal_code", "user__email")
    list_editable = ("is_default",)
    ordering = ("-is_default", "user")



class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active"),
        }),
    )
    search_fields = ("email",)
    ordering = ("email",)


class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ("email","first_name", "last_name", "phone_number", "user")
    search_fields = ("first_name", "last_name", "email", "phone_number")
    list_filter = ("email",)
    fieldsets = (
        (None, {"fields": ("first_name", "last_name", "email", "phone_number", "profile_image", "user")}),
    )
    ordering = ("first_name",)


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
