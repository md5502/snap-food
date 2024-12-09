from django.urls import path

from .views import edit_user_profile, user_profile

app_name = "users"

urlpatterns = [
    path("profile/", user_profile, name="user_profile"),
    path("profile/edit/",edit_user_profile, name="edit_profile" ),
]
