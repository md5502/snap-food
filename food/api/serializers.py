from rest_framework import serializers

from food.models import Food


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

