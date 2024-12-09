from django import forms

from .models import UserProfile


class UpdateUserProfileFrom(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "profile_image",
        ]
