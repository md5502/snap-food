from django.urls import path

from menu.api.views import ListCreateMenuView, UpdateDeleteRetrieveMenuView

urlpatterns = [
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
]
