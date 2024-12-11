from django.urls import path

from restaurantDashboard.api.views.food import (
    DislikeFoodCommentView,
    FoodCommentCreateDeleteUpdateView,
    LikeFoodCommentView,
    ListCreateFoodView,
    UpdateDeleteRetrieveFoodView,
)
from restaurantDashboard.api.views.menu import (
    ListCreateMenuView,
    UpdateDeleteRetrieveMenuView,
)
from restaurantDashboard.api.views.restaurant import (
    DislikeRestaurantCommentView,
    LikeRestaurantCommentView,
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
    # Food routes
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
    # Menu routes
    path(
        "restaurants/<uuid:restaurant_id>/menus/",
        ListCreateMenuView.as_view(),
        name="menu-list-create",
    ),
    path(
        "menus/<uuid:menu_id>/",
        UpdateDeleteRetrieveMenuView.as_view(),
        name="menu-detail",
    ),
    # Restaurant comments
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
    # Food comments
    path(
        "foods/<uuid:food_id>/comments/",
        FoodCommentCreateDeleteUpdateView.as_view(),
        name="food-comments",
    ),
    path(
        "foods/<uuid:food_id>/comments/<uuid:comment_id>/",
        FoodCommentCreateDeleteUpdateView.as_view(),
        name="food-comment-post-delete-update",
    ),
    path(
        "restaurant-comments/<uuid:comment_pk>/like/",
        LikeRestaurantCommentView.as_view(),
        name="like-restaurant-comment",
    ),
    path(
        "restaurant-comments/<uuid:comment_pk>/dislike/",
        DislikeRestaurantCommentView.as_view(),
        name="dislike-restaurant-comment",
    ),
    # Food comment like/dislike
    path(
        "food-comments/<uuid:comment_pk>/like/",
        LikeFoodCommentView.as_view(),
        name="like-food-comment",
    ),
    path(
        "food-comments/<uuid:comment_pk>/dislike/",
        DislikeFoodCommentView.as_view(),
        name="dislike-food-comment",
    ),
]
