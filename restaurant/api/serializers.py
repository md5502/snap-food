from rest_framework import serializers

from restaurant.models import Restaurant


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
