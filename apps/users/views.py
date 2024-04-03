from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework.decorators import renderer_classes

from rest_framework.viewsets import ModelViewSet

# from config.custom_renderers import CustomRenderer
from .models import *
from rest_framework import status
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate

from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.urls.exceptions import Resolver404
from rest_framework import generics, status, permissions
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework import generics, views

from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

from .serializers import (
    UserMeSerializer,
    DirectorSerializer,
    ManagerSerializer,
    UserSerializer,
    LoginSerializer,
)


class UserMeView(generics.RetrieveAPIView):
    serializer_class = UserMeSerializer
    object = User
    permission_classes = [IsAuthenticated]
    search_fields = ("username", "first_name", "last_name", "role")
    def get_object(self):
        return self.request.user


class DirectorViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    search_fields = ("username", "first_name", "last_name", "role")

    def perform_create(self, serializer):
        # Hash password if provided
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()

    def perform_update(self, serializer):
        # Hash password if provided
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()

class ManagerViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer
    search_fields = ("username", "first_name", "last_name", "role")

    def perform_create(self, serializer):
        # Hash password if provided
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()

    def perform_update(self, serializer):
        # Hash password if provided
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()


class UserViewset(ModelViewSet):
    # authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    search_fields = ("username", "first_name", "last_name", "role")

    def create(self, request, *args, **kwargs):
        data = request.data
        try:
            # Check if the role is "Superuser"
            if data["role"].lower() == "superuser":
                user = User.objects.create_superuser(
                    username=data["username"],
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    password=data["password"],
                )
            else:
                user = User.objects.create_user(
                    username=data["username"],
                    first_name=data["first_name"],
                    last_name=data["last_name"],
                    password=data["password"],
                    role=data["role"],
                )
            serializer = UserSerializer(user, partial=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"error": "Please be aware"})


class LoginView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if user:
            refresh = RefreshToken.for_user(user)
            response_data = {
                "user": {
                    "success": True,
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "role": user.role,
                },
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            raise AuthenticationFailed(
                {
                    "status": False,
                    "message": "Something went wrong during authentication",
                }
            )