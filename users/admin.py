from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile, CustomUser

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
admin.site.register(CustomUser, CustomUserAdmin)
