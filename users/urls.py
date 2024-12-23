from django.urls import path

from .views import create_address, edit_user_profile, user_profile, update_address ,delete_address

app_name = "users"

urlpatterns = [
    path("profile/", user_profile, name="user_profile"),
    path("profile/address/create", create_address, name="create_address"),
    path("profile/address/update/<int:pk>", update_address, name="update_address"),
    path("profile/address/delete/<int:pk>", delete_address, name="delete_address"),
    path("profile/edit/", edit_user_profile, name="edit_profile"),
]
