from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.products.views import CategoryViewSet, ProductViewSet, SupplierViewSet, StorageViewSet, \
    StorageProductViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'suppliers', SupplierViewSet, basename='suppliers')
router.register(r'storages', StorageViewSet, basename='storages')
router.register(r'storage-products', StorageProductViewSet, basename='storage-products')

urlpatterns = [
    path('', include(router.urls)),
]
