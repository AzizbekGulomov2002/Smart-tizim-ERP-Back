from rest_framework import serializers, exceptions, status
from .models import *
from rest_framework import serializers


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password", "first_name", "last_name", "role")


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ("id", "username", "first_name", "last_name", "role")


class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manager
        fields = ("id", "username", "first_name", "last_name", "role")


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=223, required=True)
    password = serializers.CharField(max_length=68, required=True)

    @staticmethod
    def validate_username(username):
        if len(username) < 4 or len(username) > 30:
            raise exceptions.ValidationError(
                {"message": "username must be between 4 and 30 characters"},
                status.HTTP_400_BAD_REQUEST,
            )
        return username