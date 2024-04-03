from django.shortcuts import render
from rest_framework import viewsets

from .filters import TransactionFilter
from .models import Transaction, Payments, FinanceOutcome
from .serializers import TransactionSerializer, PaymentsSerializer, FinanceOutcomeSerializer



class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filterset_class = TransactionFilter


class PaymentsViewSet(viewsets.ModelViewSet):
    queryset = Payments.objects.all()
    serializer_class = PaymentsSerializer

class FinanceOutcomeViewSet(viewsets.ModelViewSet):
    queryset = FinanceOutcome.objects.all()
    serializer_class = FinanceOutcomeSerializer
