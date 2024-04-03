from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.trade.views import ClientViewSet, TradeViewSet, TradeDetailViewSet, ServiceTypeViewSet, \
    AdditionServiceViewSet

router = DefaultRouter()
router.register(r'clients', ClientViewSet)
router.register(r'trades', TradeViewSet)
router.register(r'trade-details', TradeDetailViewSet)
router.register(r'service-types', ServiceTypeViewSet)
router.register(r'addition-services', AdditionServiceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('clients/<int:pk>/trades/', ClientTradeListAPIView.as_view(), name='client-trade-list'),
]
