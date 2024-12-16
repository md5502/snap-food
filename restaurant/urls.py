from django.urls import path

from .views import (
    RestaurantCreateView,
    RestaurantDeleteView,
    RestaurantDetailView,
    RestaurantListView,
    RestaurantUpdateView,
)

app_name = "restaurant"

urlpatterns = [
    path("", RestaurantListView.as_view(), name="list_restaurant"),
    path("create/", RestaurantCreateView.as_view(), name="create_restaurant"),
    path("update/<uuid:pk>", RestaurantUpdateView.as_view(), name="update_restaurant"),
    path("delete/<uuid:pk>", RestaurantDeleteView.as_view(), name="delete_restaurant"),
    path("detail/<uuid:pk>", RestaurantDetailView.as_view(), name="detail_restaurant"),
]
