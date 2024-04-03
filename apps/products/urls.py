from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.products.views import CategoryViewSet, FormatViewSet, ProductViewSet, SupplierViewSet, StorageViewSet, \
    StorageProductViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'formats', FormatViewSet)
router.register(r'products', ProductViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'storage', StorageViewSet)
router.register(r'storage-products', StorageProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
