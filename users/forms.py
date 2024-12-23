from django import forms

from .models import Address, UserProfile


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


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "title",
            "full_name",
            "phone_number",
            "address_line_1",
            "address_line_2",
            "city",
            "state",
            "street",
            "postal_code",
            "country",
            "is_default",
        ]
