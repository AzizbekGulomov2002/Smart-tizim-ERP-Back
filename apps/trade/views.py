from rest_framework import viewsets

from .filters import ClientFilter,TradeFilter,ServiceTypeFilter
from .models import Client, Trade, TradeDetail, ServiceType, Addition_service
from .serializers import ClientSerializer, TradeSerializer, TradeDetailSerializer, ServiceTypeSerializer, AdditionServiceSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filterset_class = ClientFilter

# class ClientTradeListAPIView(generics.RetrieveAPIView):
#     queryset = Client.objects.all()
#     serializer_class = ClientSerializer
#     lookup_field = 'pk'
#
#     def get_object(self):
#         queryset = self.get_queryset()
#         obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
#         return obj

class TradeViewSet(viewsets.ModelViewSet):
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
    filterset_class = TradeFilter

class TradeDetailViewSet(viewsets.ModelViewSet):
    queryset = TradeDetail.objects.all()
    serializer_class = TradeDetailSerializer

class ServiceTypeViewSet(viewsets.ModelViewSet):
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    filterset_class = ServiceTypeFilter

class AdditionServiceViewSet(viewsets.ModelViewSet):
    queryset = Addition_service.objects.all()
    serializer_class = AdditionServiceSerializer
