from django.urls import path

from .views import detail_restaurant, home, list_restaurant

app_name = "front"

urlpatterns = [
    path("", home, name="home"),
    path("restaurants", list_restaurant, name="list_restaurant"),
    path("restaurants/detail/<str:restaurant_pk>", detail_restaurant, name="detail_restaurant"),
]
