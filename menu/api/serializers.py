from rest_framework import serializers

from menu.models import Menu


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
