from django import forms

from .models import Restaurant


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
