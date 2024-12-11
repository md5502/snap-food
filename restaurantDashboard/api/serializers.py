from rest_framework import serializers

from restaurantDashboard.models import Food, FoodComment, Menu, Restaurant, RestaurantComment


class RestaurantCommentGetSerializer(serializers.ModelSerializer):
    email = serializers.CharField(source="user.email")

    class Meta:
        model = RestaurantComment
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


class RestaurantCommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantComment
        fields = [
            "text",
            "user",
            "restaurant",
        ]

        read_only_fields = [
            "restaurant",
            "user",
        ]

class RestaurantCommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantComment
        fields = [
            "text",

        ]

class RestaurantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            "pk",
            "name",
            "logo",
            "description",
        ]


class RestaurantDetailSerializer(serializers.ModelSerializer):
    comments = RestaurantCommentGetSerializer(many=True)

    class Meta:
        model = Restaurant
        fields = [
            "name",
            "logo",
            "description",
            "address",
            "call_number",
            "time_to_open",
            "time_to_close",
            "comments",
            "pk",
            "created_at",
            "updated_at",
        ]


class RestaurantPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            "name",
            "logo",
            "owner",
            "description",
            "address",
            "call_number",
            "time_to_open",
            "time_to_close",
        ]
        read_only_fields = ["owner"]


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


class MenuListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            "pk",
            "name",
            "description",
        ]


class MenuDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            "name",
            "description",
            "foods",
            "available_from",
            "available_to",
            "is_active",
            "available_days",
            "pk",
            "created_at",
            "updated_at",
        ]


class MenuPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            "name",
            "description",
            "foods",
            "available_from",
            "available_to",
            "is_active",
            "available_days",
            "restaurant",
            "pk",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["restaurant"]
