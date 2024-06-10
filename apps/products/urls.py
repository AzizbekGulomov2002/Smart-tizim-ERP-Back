from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.products.views import CategoryViewSet, ProductViewSet, SupplierViewSet, StorageViewSet, \
    StorageProductViewSet,ProductDeleteManagerAPI, FormatViewSet, ProductCreateAPIView

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'formats', FormatViewSet, basename='formats')
router.register(r'suppliers', SupplierViewSet, basename='suppliers')
router.register(r'storages', StorageViewSet, basename='storages')
router.register(r'storage-products', StorageProductViewSet, basename='storage-products')

urlpatterns = [
    path('', include(router.urls)),
    path('delete_products/', ProductDeleteManagerAPI.as_view(), name='delete_products'), 
    path('product_creates/', ProductCreateAPIView.as_view(), name='product_creates'), 
]
