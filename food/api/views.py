from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from food.models import (
    Food,
)
from restaurant.models import Restaurant

from .serializers import (
    FoodDetailSerializer,
    FoodListSerializer,
    FoodPostSerializer,
)


class ListCreateFoodView(APIView):
    """List and create foods for a given restaurant."""

    def get(self, request, restaurant_pk):
        foods = Food.objects.filter(restaurant=restaurant_pk)
        serializer = FoodListSerializer(foods, many=True)
        return Response(serializer.data)

    def post(self, request, restaurant_pk):
        restaurant = Restaurant.objects.filter(pk=restaurant_pk).first()
        if restaurant.owner != request.user:
            return Response(
                {"error": "You must be the owner of the restaurant to add food"},
                status=403,
            )

        serializer = FoodPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(restaurant=restaurant)
            return Response({"msg": "Food created successfully"}, status=201)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class UpdateDeleteRetrieveFoodView(APIView):
    """Retrieve, update or delete a specific food."""

    def get(self, request, food_id):
        food = Food.objects.filter(pk=food_id).first()
        if not food:
            return Response({"error": "food not found"})

        serializer = FoodDetailSerializer(food)
        return Response(serializer.data)

    def put(self, request, food_id):
        food = Food.objects.filter(pk=food_id).first()
        if not food:
            return Response({"error": "food not found"})

        if food.restaurant.owner != request.user:
            return Response(
                {"error": "You must be the owner of the restaurant to update food"},
                status=403,
            )
        serializer = FoodPostSerializer(food, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, food_id):
        food = Food.objects.filter(pk=food_id).first()
        if not food:
            return Response({"error": "food not found"})

        if food.restaurant.owner != request.user:
            return Response(
                {"error": "You must be the owner of the restaurant to delete food"},
                status=403,
            )
        food.delete()
        return Response({"msg": "Food deleted successfully"}, status=HTTP_204_NO_CONTENT)
