from django.urls import path

from .views import (
    FoodCreateView,
    FoodDeleteView,
    FoodDetailView,
    FoodListView,
    FoodUpdateView,
)

app_name = "food"

urlpatterns = [
    path("foods/<uuid:restaurant_id>", FoodListView.as_view(), name="food_list"),
    path("food/create/<uuid:restaurant_id>", FoodCreateView.as_view(), name="food_create"),
    path("food/update/<uuid:pk>", FoodUpdateView.as_view(), name="food_update"),
    path("food/delete/<uuid:pk>", FoodDeleteView.as_view(), name="food_delete"),
    path("food/detail/<uuid:pk>", FoodDetailView.as_view(), name="food_detail"),

]
