from django.urls import path, include
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
from apps.users.views import *


urlpatterns = [
    path('create_user_company/', CreateCompanyUserAPIView.as_view()),
    path('create/', UserCreateAPIView.as_view()),

]