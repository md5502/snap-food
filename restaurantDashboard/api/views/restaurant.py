from rest_framework import status
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from restaurantDashboard.api.serializers import (
    RestaurantCommentPostSerializer,
    RestaurantCommentUpdateSerializer,
    RestaurantDetailSerializer,
    RestaurantListSerializer,
    RestaurantPostSerializer,
)
from restaurantDashboard.models import (
    Restaurant,
    RestaurantComment,
    RestaurantCommentDislike,
    RestaurantCommentLike,
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


class RestaurantCommentCreateDeleteUpdateView(APIView):
    """API endpoints for creating, updating, deleting restaurant comments."""

    def post(self, request, restaurant_pk):
        """Create a new restaurant comment."""
        restaurant = Restaurant.objects.filter(pk=restaurant_pk).first()
        if not restaurant:
            return Response(
                {"error": "restaurant with given id not found"},
                status=403,
            )
        serializer = RestaurantCommentPostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(restaurant=restaurant, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, restaurant_pk, comment_pk):
        """Update a restaurant comment."""
        restaurant = Restaurant.objects.filter(pk=restaurant_pk).first()
        if not restaurant:
            return Response(
                {"error": "restaurant with given id not found"},
                status=403,
            )
        comment = RestaurantComment.objects.filter(pk=comment_pk).first()
        if not comment:
            return Response(
                {"error": "comment with given id not found"},
                status=403,
            )
        if comment.user == request.user and comment.restaurant == restaurant:
            serializer = RestaurantCommentUpdateSerializer(
                comment,
                data=request.data,
                partial=True,
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            {"error": "You can only edit your own comments."},
            status=status.HTTP_403_FORBIDDEN,
        )

    def delete(self, request, restaurant_pk, comment_pk):
        """Delete a restaurant comment."""
        restaurant = Restaurant.objects.filter(pk=restaurant_pk).first()
        if not restaurant:
            return Response(
                {"error": "restaurant with given id not found"},
                status=403,
            )
        comment = RestaurantComment.objects.filter(pk=comment_pk).first()
        if not comment:
            return Response(
                {"error": "comment with given id not found"},
                status=403,
            )

        if comment.user == request.user and comment.restaurant == restaurant:
            comment.delete()
            return Response(
                {"msg": "Comment deleted successfully."},
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(
            {"error": "You can only delete your own comments."},
            status=status.HTTP_403_FORBIDDEN,
        )


class LikeRestaurantCommentView(APIView):
    def post(self, request, comment_pk):
        try:
            comment = RestaurantComment.objects.get(pk=comment_pk)
        except RestaurantComment.DoesNotExist:
            return Response({"error": "Comment not found."}, status=404)

        user = request.user
        like_comment = RestaurantCommentLike.objects.filter(comment=comment, user=user).exists()

        if like_comment:
            return Response({"msg": "You already liked this comment."}, status=400)

        RestaurantCommentLike.objects.create(user=user, comment=comment)
        comment.like_count += 1
        comment.save()
        return Response({"msg": "Liking was successful."}, status=200)


class DislikeRestaurantCommentView(APIView):
    def post(self, request, comment_pk):
        try:
            comment = RestaurantComment.objects.get(pk=comment_pk)
        except RestaurantComment.DoesNotExist:
            return Response({"error": "Comment not found."}, status=404)

        user = request.user
        dislike_comment = RestaurantCommentDislike.objects.filter(comment=comment, user=user).exists()

        if dislike_comment:
            return Response({"msg": "You already disliked this comment."}, status=400)

        RestaurantCommentDislike.objects.create(user=user, comment=comment)
        comment.dislike_count += 1
        comment.save()
        return Response({"msg": "Disliking was successful."}, status=200)
