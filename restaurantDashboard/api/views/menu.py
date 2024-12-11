from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from restaurantDashboard.api.serializers import (
    MenuDetailSerializer,
    MenuListSerializer,
    MenuPostSerializer,
)
from restaurantDashboard.models import (
    Menu,
    Restaurant,
)


class ListCreateMenuView(APIView):
    """List and create menus for a given restaurant."""

    def get(self, request, restaurant_pk):
        menus = Menu.objects.filter(restaurant=restaurant_pk)
        serializer = MenuListSerializer(menus, many=True)
        return Response(serializer.data)

    def post(self, request, restaurant_pk):
        restaurant = Restaurant.objects.filter(pk=restaurant_pk).first()
        if not restaurant:
            return Response(
                {"error": "restaurant with given id not found"},
                status=403,
            )
        if restaurant.owner != request.user:
            return Response(
                {"error": "You must be the owner of the restaurant to add menu"},
                status=403,
            )

        serializer = MenuPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(restaurant=restaurant)
            return Response({"msg": "Menu created successfully"}, status=201)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UpdateDeleteRetrieveMenuView(APIView):
    """Retrieve, update or delete a single menu by primary key."""

    def get(self, request, menu_id):
        """Retrieve menu details by its primary key."""
        menu = Menu.objects.filter(Menu, pk=menu_id).first()
        if not menu:
            return Response(
                {"error": "menu with given id not found"},
                status=403,
            )
        serializer = MenuDetailSerializer(menu)
        return Response(serializer.data)

    def put(self, request, menu_id):
        """Update an existing menu if the user is the owner of the corresponding restaurant."""
        menu = Menu.objects.filter(Menu, pk=menu_id).first()
        if not menu:
            return Response(
                {"error": "menu with given id not found"},
                status=403,
            )
        # Check ownership
        if menu.restaurant.owner != request.user:
            return Response(
                {"error": "You must be the owner of the restaurant to update menu"},
                status=403,
            )

        # Deserialize data
        serializer = MenuPostSerializer(menu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, menu_id):
        """Delete a menu if the user is the owner of the corresponding restaurant."""
        menu = Menu.objects.filter(Menu, pk=menu_id).first()
        if not menu:
            return Response(
                {"error": "menu with given id not found"},
                status=403,
            )
        # Check ownership
        if menu.restaurant.owner != request.user:
            return Response(
                {"error": "You must be the owner of the restaurant to delete menu"},
                status=403,
            )

        # Perform delete
        menu.delete()
        return Response({"msg": "Menu deleted successfully"}, status=HTTP_204_NO_CONTENT)
