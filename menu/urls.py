from django.urls import path

from .views import (
    MenuCreateView,
    MenuDeleteView,
    MenuDetailView,
    MenuListView,
    MenuUpdateView,
)

app_name = "menu"

urlpatterns = [
    path("menus/<uuid:restaurant_id>", MenuListView.as_view(), name="menu_list"),
    path("menu/create/<uuid:restaurant_id>", MenuCreateView.as_view(), name="menu_create"),
    path("menu/update/<uuid:pk>", MenuUpdateView.as_view(), name="menu_update"),
    path("menu/delete/<uuid:pk>", MenuDeleteView.as_view(), name="menu_delete"),
    path("menu/detail/<uuid:pk>", MenuDetailView.as_view(), name="menu_detail"),
]
