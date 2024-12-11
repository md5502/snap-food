from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from food.models import (
    Food,
    FoodComment,
    FoodCommentDislike,
    FoodCommentLike,
)
from restaurant.models import Restaurant

from .serializers import (
    FoodCommentPostSerializer,
    FoodCommentUpdateSerializer,
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


class FoodCommentCreateDeleteUpdateView(APIView):
    """API endpoints for creating, updating, deleting food comments."""

    def post(self, request, food_pk):
        """Create a new food comment."""
        food = Food.objects.filter(pk=food_pk).first()
        if not food:
            return Response(
                {"error": "food with given id not found"},
                status=403,
            )
        serializer = FoodCommentPostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(food=food, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, food_pk, comment_pk):
        """Update a food comment."""
        food = Food.objects.filter(pk=food_pk).first()
        if not food:
            return Response(
                {"error": "food with given id not found"},
                status=403,
            )
        comment = FoodComment.objects.filter(pk=comment_pk).first()
        if not comment:
            return Response(
                {"error": "comment with given id not found"},
                status=403,
            )

        if comment.user == request.user and comment.food == food:
            serializer = FoodCommentUpdateSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"error": "You can only edit your own comments."},
            status=status.HTTP_403_FORBIDDEN,
        )

    def delete(self, request, food_pk, comment_pk):
        """Delete a food comment."""
        food = Food.objects.filter(pk=food_pk).first()
        if not food:
            return Response(
                {"error": "food with given id not found"},
                status=403,
            )
        comment = FoodComment.objects.filter(pk=comment_pk).first()
        if not comment:
            return Response(
                {"error": "comment with given id not found"},
                status=403,
            )

        if comment.user == request.user and comment.food == food:
            comment.delete()
            return Response(
                {"msg": "Comment deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(
            {"error": "You can only delete your own comments."},
            status=status.HTTP_403_FORBIDDEN,
        )


class LikeFoodCommentView(APIView):
    def post(self, request, comment_pk):
        try:
            comment = FoodComment.objects.get(pk=comment_pk)
        except FoodComment.DoesNotExist:
            return Response({"error": "Comment not found."}, status=404)

        user = request.user
        like_comment = FoodCommentLike.objects.filter(comment=comment, user=user).exists()

        if like_comment:
            return Response({"msg": "You already liked this comment."}, status=400)

        FoodCommentLike.objects.create(user=user, comment=comment)
        comment.like_count += 1
        comment.save()
        return Response({"msg": "Liking was successful."}, status=200)


class DislikeFoodCommentView(APIView):
    def post(self, request, comment_pk):
        try:
            comment = FoodComment.objects.get(pk=comment_pk)
        except FoodComment.DoesNotExist:
            return Response({"error": "Comment not found."}, status=404)

        user = request.user
        dislike_comment = FoodCommentDislike.objects.filter(comment=comment, user=user).exists()

        if dislike_comment:
            return Response({"msg": "You already disliked this comment."}, status=400)

        FoodCommentDislike.objects.create(user=user, comment=comment)
        comment.dislike_count += 1
        comment.save()
        return Response({"msg": "Disliking was successful."}, status=200)
