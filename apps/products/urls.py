from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.products.views import CategoryViewSet, ProductViewSet, SupplierViewSet, StorageViewSet, \
    StorageProductViewSet, ProductDeleteManagerAPI, FormatViewSet, ProductCreateAPIView, StorageProductCreate, \
    StorageProductOffViewSet, ALlProductViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'products', ProductViewSet, basename='products')
router.register(r'all_products', ALlProductViewSet, basename='all_products')
router.register(r'formats', FormatViewSet, basename='formats')
router.register(r'suppliers', SupplierViewSet, basename='suppliers')
router.register(r'storages', StorageViewSet, basename='storages')
router.register(r'storage_products', StorageProductViewSet, basename='storage_products')
router.register(r'storage_products_off', StorageProductOffViewSet, basename='storage_products_off')

urlpatterns = [
    path('', include(router.urls)),
    path('storage_product_create/',StorageProductCreate.as_view()),
    path('delete_products/', ProductDeleteManagerAPI.as_view(), name='delete_products'), 
    path('product_create/', ProductCreateAPIView.as_view(), name='product_creates'),
]
