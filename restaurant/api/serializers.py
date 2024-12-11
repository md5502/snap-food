from rest_framework import serializers

from restaurant.models import Restaurant, RestaurantComment


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
