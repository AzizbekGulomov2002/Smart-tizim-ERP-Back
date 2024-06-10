from django.contrib import admin
from apps.users.status_admin import company_off_view, company_on_view
from apps.users.views import LoginApiView, CreateCompanyUserAPIView, UserCreateAPIView
from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
swagger_view = get_swagger_view(title='API')
router = routers.DefaultRouter()
schema_view = get_schema_view(
    openapi.Info(
        title="Smart-tizim ERP",
        default_version="v1",
        description="Your API description",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

from apps.products.views import StorageProductCreate
urlpatterns = [

    path('',StorageProductCreate.as_view()),
    path('company_off/',company_off_view),
    path('company_on/',company_on_view),

    path('create_user_company/', CreateCompanyUserAPIView.as_view()),
    path('create/', UserCreateAPIView.as_view()),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/', include_docs_urls(title='API Documentation')),
    path('swagger/', swagger_view),
    path('admin/', admin.site.urls),
    path('api/', include('apps.urls')),

    path('login/', LoginApiView.as_view(), name='login'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path("__debug__/", include("debug_toolbar.urls")),
]
