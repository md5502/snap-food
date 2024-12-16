from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from restaurant.api.serializers import (
    RestaurantDetailSerializer,
    RestaurantListSerializer,
    RestaurantPostSerializer,
)
from restaurant.models import (
    Restaurant,
)


class ListCreateRestaurantView(APIView):
    """List and create restaurants for the logged-in user."""

    def get(self, request):
        # Get all restaurants owned by the user.
        restaurants = Restaurant.objects.filter(owner=request.user)
        serializer = RestaurantListSerializer(restaurants, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RestaurantPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response({"msg": "Restaurant created successfully"}, status=201)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UpdateDeleteRetrieveRestaurantView(APIView):
    """Retrieve, update or delete a single restaurant."""

    def get(self, request, restaurant_id):
        restaurant = Restaurant.objects.filter(pk=restaurant_id).first()
        if not restaurant:
            return Response({"error": "restaurant not found"})

        serializer = RestaurantDetailSerializer(restaurant)
        return Response(serializer.data)

    def put(self, request, restaurant_id):
        restaurant = Restaurant.objects.filter(pk=restaurant_id).first()
        if not restaurant:
            return Response({"error": "restaurant not found"})

        if restaurant.owner != request.user:
            return Response({"error": "You can only edit your own restaurant"}, status=403)

        serializer = RestaurantDetailSerializer(restaurant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, restaurant_id):
        restaurant = Restaurant.objects.filter(pk=restaurant_id).first()
        if not restaurant:
            return Response({"error": "restaurant not found"})

        if restaurant.owner != request.user:
            return Response({"error": "You can only delete your own restaurant"}, status=403)
        restaurant.delete()
        return Response({"msg": "Restaurant deleted successfully"}, status=HTTP_204_NO_CONTENT)


