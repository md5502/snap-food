from rest_framework import serializers

from food.models import Food, FoodComment


class FoodCommentGetSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email")

    class Meta:
        model = FoodComment
        fields = [
            "email",
            "text",
            "like_count",
            "dislike_count",
            "parent",
            "created_at",
            "updated_at",
            "pk",
        ]


class FoodCommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodComment
        fields = [
            "text",
            "user",
            "food",
        ]


class FoodCommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodComment
        fields = [
            "text",
        ]


class FoodListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = [
            "pk",
            "name",
            "image",
            "description",
        ]


class FoodDetailSerializer(serializers.ModelSerializer):
    comments = FoodCommentGetSerializer(many=True)

    class Meta:
        model = Food
        fields = [
            "name",
            "description",
            "image",
            "count",
            "rate",
            "discount",
            "price",
            "comments",
            "pk",
            "created_at",
            "updated_at",
        ]


class FoodPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = [
            "name",
            "description",
            "restaurant",
            "image",
            "count",
            "rate",
            "discount",
            "price",
        ]
        read_only_fields = ["restaurant"]

