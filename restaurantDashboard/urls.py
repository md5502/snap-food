from django.urls import path

from .views.food import (
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
from .views.menu import (
    MenuCreateView,
    MenuDeleteView,
    MenuDetailView,
    MenuListView,
    MenuUpdateView,
)
from .views.restaurant import (
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

app_name = "restaurant_dashboard"

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

    path("menus/<uuid:restaurant_id>", MenuListView.as_view(), name="menu_list"),
    path("menu/create/<uuid:restaurant_id>", MenuCreateView.as_view(), name="menu_create"),
    path("menu/update/<uuid:pk>", MenuUpdateView.as_view(), name="menu_update"),
    path("menu/delete/<uuid:pk>", MenuDeleteView.as_view(), name="menu_delete"),
    path("menu/detail/<uuid:pk>", MenuDetailView.as_view(), name="menu_detail"),
]
