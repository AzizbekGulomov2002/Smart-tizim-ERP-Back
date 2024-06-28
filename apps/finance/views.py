from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status,filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .filters import TransactionFilter, PaymentsFilter
from .models import Transaction, Payments, FinanceOutcome
from .serializers import TransactionSerializer, PaymentsSerializer, FinanceOutcomeSerializer
from .decorator import is_finance_permission
from ..app.views import BasePagination


class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    filterset_class = TransactionFilter
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        company_id = self.request.user.company_id
        queryset = Transaction.objects.filter(company_id=company_id)
        return queryset
    def list(self,request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company_id=request.user.company_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class PaymentsViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = BasePagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = PaymentsFilter
    search_fields = ['client__name', 'desc']
    def get_queryset(self):
        company_id = self.request.user.company_id
        queryset = Payments.objects.filter(company_id=company_id)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    @is_finance_permission
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serialiser = self.get_serializer(instance)
        return Response(serialiser.data)
    @is_finance_permission
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company_id = request.user.company_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @is_finance_permission
    def updata(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @is_finance_permission
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FinanceOutcomeViewSet(viewsets.ModelViewSet):
    serializer_class = FinanceOutcomeSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        company_id = self.request.user.company_id
        queryset = FinanceOutcome.objects.filter(company_id=company_id)
        return queryset
    @is_finance_permission
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    @is_finance_permission
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    @is_finance_permission
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company_id=request.user.company_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @is_finance_permission
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @is_finance_permission
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
