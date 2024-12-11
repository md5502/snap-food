from django.urls import path

from .views import (
    DislikeFoodCommentView,
    FoodCommentCreateDeleteUpdateView,
    LikeFoodCommentView,
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
