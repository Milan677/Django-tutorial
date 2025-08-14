from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'password', 'is_active', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True},  # Don't show password in GET responses
            'is_active': {'read_only': True},  # Optional: prevent changing via API
            'is_staff': {'read_only': True},   # Optional: prevent changing via API
        }

    def create(self, validated_data):
        # Hash password before saving
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Hash password if it's being updated
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().update(instance, validated_data)
