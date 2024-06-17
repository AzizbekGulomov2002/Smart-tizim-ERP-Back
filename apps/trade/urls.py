from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.trade.views import ClientViewSet, TradeApiView, ServiceTypeViewSet, \
    AdditionServiceViewSet,ClientDeleteManagerAPI

router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='clients')

# router.register(r'trade-details', TradeDetailViewSet)
router.register(r'service_types', ServiceTypeViewSet, basename='service-types')
router.register(r'addition_services', AdditionServiceViewSet, basename='addition-services')

urlpatterns = [
    path('trades/', TradeApiView.as_view(), name='trades'), 
    path('delete_clients/', ClientDeleteManagerAPI.as_view(), name='delete_clients'), 
    path('', include(router.urls)),  # Include the router's URLs
]