from django.urls import path

from .views import (
    RestaurantCommentCreateView,
    RestaurantCommentDeleteView,
    RestaurantCommentUpdateView,
    RestaurantCreateView,
    RestaurantDeleteView,
    RestaurantDetailView,
    RestaurantListView,
    RestaurantUpdateView,
    restaurant_comment_dislike_view,
    restaurant_comment_like_view,
    restaurant_comment_reply_view,
)

app_name = "restaurant"

urlpatterns = [
    path("", RestaurantListView.as_view(), name="list_restaurant"),
    path("create/", RestaurantCreateView.as_view(), name="create_restaurant"),
    path("update/<uuid:pk>", RestaurantUpdateView.as_view(), name="update_restaurant"),
    path("delete/<uuid:pk>", RestaurantDeleteView.as_view(), name="delete_restaurant"),
    path("detail/<uuid:pk>", RestaurantDetailView.as_view(), name="detail_restaurant"),

    path("<uuid:pk>/comment/create/", RestaurantCommentCreateView.as_view(), name="restaurant_comment_create"),
    path("comment/<uuid:pk>/edit/", RestaurantCommentUpdateView.as_view(), name="restaurant_comment_update"),
    path("comment/<uuid:pk>/delete/", RestaurantCommentDeleteView.as_view(), name="restaurant_comment_delete"),
    path("comment/<uuid:comment_pk>/like/", restaurant_comment_like_view, name="restaurant_comment_like"),
    path("comment/<uuid:comment_pk>/dislike/", restaurant_comment_dislike_view, name="restaurant_comment_dislike"),
    path("comment/<uuid:parent_comment_pk>/replay/", restaurant_comment_reply_view, name="restaurant_comment_reply"),
]
