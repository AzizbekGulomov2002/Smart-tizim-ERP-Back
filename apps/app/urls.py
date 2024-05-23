from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.app.views import StaticStatistics,DynamicStatistics

router = DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('static_statistics/', StaticStatistics.as_view(), name='static_statistics'),
    path('dynamic_statistics/', DynamicStatistics.as_view(), name='dynamic_statistics'),
]