from django.urls import path

from .views import (
    ListCreateFoodView,
    UpdateDeleteRetrieveFoodView,
)

urlpatterns = [
    path(
        "restaurants/<uuid:restaurant_id>/foods/",
        ListCreateFoodView.as_view(),
        name="food-list-create",
    ),
    path(
        "foods/<uuid:food_id>/",
        UpdateDeleteRetrieveFoodView.as_view(),
        name="food-detail",
    ),
]
