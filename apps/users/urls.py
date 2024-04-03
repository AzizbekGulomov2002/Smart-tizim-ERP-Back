from django.urls import path, include
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
from apps.users.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('directors/', DirectorViewset.as_view(), name='director-list'),
    path('managers/', ManagerViewset.as_view(), name='manager-list'),
    path('users/', UserViewset.as_view(), name='user-list'),
    # Add other URL patterns as needed
]