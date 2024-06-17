from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.finance.views import TransactionViewSet, PaymentsViewSet, FinanceOutcomeViewSet

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transactions')
router.register(r'payments', PaymentsViewSet, basename='payments')
router.register(r'finance_outcomes', FinanceOutcomeViewSet, basename='finance-outcomes')

urlpatterns = [
    path('', include(router.urls)),
]
