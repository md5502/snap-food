from django import forms

from .models import Food, FoodComment


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


class FoodCommentForm(forms.ModelForm):
    class Meta:
        model = FoodComment
        fields = ["text"]
