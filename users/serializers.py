from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer

from .models import CustomUser


class CustomLoginSerializer(LoginSerializer):
    username = None
    class Meta:
        model = CustomUser
        fields = ["email", "password"]


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    class Meta:
        model = CustomUser
        fields = ["email"]
