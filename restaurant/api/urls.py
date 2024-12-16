from django.urls import path

from restaurant.api.views import (
    ListCreateRestaurantView,
    UpdateDeleteRetrieveRestaurantView,
)

urlpatterns = [
    # Restaurant routes
    path(
        "restaurants/",
        ListCreateRestaurantView.as_view(),
        name="restaurant-list-create",
    ),
    path(
        "restaurants/<uuid:restaurant_id>/",
        UpdateDeleteRetrieveRestaurantView.as_view(),
        name="restaurant-detail",
    ),
]
