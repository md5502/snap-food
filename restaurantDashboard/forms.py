from django import forms
from django.core.exceptions import ValidationError

from .models import Food, FoodComment, Menu, Restaurant, RestaurantComment


class RestaurantForm(forms.ModelForm):
    time_to_open = forms.TimeField(
        widget=forms.TimeInput(attrs={"type": "time"}),
        required=True,
    )
    time_to_close = forms.TimeField(
        widget=forms.TimeInput(attrs={"type": "time"}),
        required=True,
    )

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
        ]


class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = [
            "name",
            "price",
            "image",
            "count",
            "discount",
        ]


class MenuForm(forms.ModelForm):
    available_from = forms.TimeField(
        widget=forms.TimeInput(attrs={"type": "time"}),
        required=True,
    )
    available_to = forms.TimeField(
        widget=forms.TimeInput(attrs={"type": "time"}),
        required=True,
    )

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
        ]

    def clean(self):
        cleaned_data = super().clean()
        available_from = cleaned_data.get("available_from")
        available_to = cleaned_data.get("available_to")

        if available_from and available_to and available_from >= available_to:
            raise ValidationError(
                {
                    "available_to": "The end time must be after the start time.",
                },
            )

        return cleaned_data


class RestaurantCommentForm(forms.ModelForm):
    class Meta:
        model = RestaurantComment
        fields = ["text"]


class FoodCommentForm(forms.ModelForm):
    class Meta:
        model = FoodComment
        fields = ["text"]
