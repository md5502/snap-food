from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("users.urls")),
    path("restaurant-dashboard/", include("restaurantDashboard.urls")),

]
