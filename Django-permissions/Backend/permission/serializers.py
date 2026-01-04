from rest_framework import serializers
from .models import User


class AdminRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=["teacher", "student"])  # role is required

    class Meta:
        model = User
        fields = ["username", "email", "password", "first_name", "last_name", "role"]    