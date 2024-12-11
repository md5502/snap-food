from django.urls import path

from restaurant.api.views import (
    ListCreateRestaurantView,
    RestaurantCommentCreateDeleteUpdateView,
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
    path(
        "restaurants/<uuid:restaurant_id>/comments/",
        RestaurantCommentCreateDeleteUpdateView.as_view(),
        name="restaurant-comments",
    ),
    path(
        "restaurants/<uuid:restaurant_id>/comments/<uuid:comment_id>/",
        RestaurantCommentCreateDeleteUpdateView.as_view(),
        name="restaurant-comment-post-delete-update",
    ),
]
