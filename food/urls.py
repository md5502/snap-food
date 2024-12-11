from django.urls import path

from .views import (
    FoodCommentCreateView,
    FoodCommentDeleteView,
    FoodCommentUpdateView,
    FoodCreateView,
    FoodDeleteView,
    FoodDetailView,
    FoodListView,
    FoodUpdateView,
    food_comment_dislike_view,
    food_comment_like_view,
    food_comment_reply_view,
)

app_name = "food"

urlpatterns = [
    path("foods/<uuid:restaurant_id>", FoodListView.as_view(), name="food_list"),
    path("food/create/<uuid:restaurant_id>", FoodCreateView.as_view(), name="food_create"),
    path("food/update/<uuid:pk>", FoodUpdateView.as_view(), name="food_update"),
    path("food/delete/<uuid:pk>", FoodDeleteView.as_view(), name="food_delete"),
    path("food/detail/<uuid:pk>", FoodDetailView.as_view(), name="food_detail"),
    path("food/<uuid:pk>/comment/create/", FoodCommentCreateView.as_view(), name="food_comment_create"),
    path("food/comment/<uuid:pk>/update/", FoodCommentUpdateView.as_view(), name="food_comment_update"),
    path("food/comment/<uuid:pk>/delete/", FoodCommentDeleteView.as_view(), name="food_comment_delete"),
    path("food/comment/<uuid:comment_pk>/like/", food_comment_like_view, name="food_comment_like"),
    path("food/comment/<uuid:comment_pk>/dislike/", food_comment_dislike_view, name="food_comment_dislike"),
    path("food/comment/<uuid:parent_comment_pk>/replay/", food_comment_reply_view, name="food_comment_reply"),
]
