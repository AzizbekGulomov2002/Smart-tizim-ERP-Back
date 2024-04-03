from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.finance.views import TransactionViewSet, PaymentsViewSet, FinanceOutcomeViewSet

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet)
router.register(r'payments', PaymentsViewSet)
router.register(r'finance-outcomes', FinanceOutcomeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
