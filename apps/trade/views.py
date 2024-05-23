from datetime import datetime
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .filters import ServiceTypeFilter
from .models import Client, ServiceType, Addition_service, Trade
from .serializers import ClientSerializer,ServiceTypeSerializer, AdditionServiceSerializer
from ..products.models import Product, Category, StorageProduct
from ..products.serializers import CategorySerializer, ProductSerializer
from django.db import transaction
from django.db.models import F
from ..finance.models import Payments , Transaction
from ..finance.serializers import PaymentsSerializer
from .decorator import is_client_permission, is_trade_permission



class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer
    def get_queryset(self):
        company_id = self.request.user.company_id
        queryset = Client.objects.filter(company_id=company_id)
        return queryset
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    @is_client_permission
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    @is_client_permission
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company_id=request.user.company_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @is_client_permission
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @is_client_permission
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TradeApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        company_id = request.user.company_id
        product = Product.objects.filter(company_id=company_id).prefetch_related('storage_products').filter(storage_products__count__gte=1).distinct()
        category = Category.objects.filter(company_id=company_id)
        client = Client.objects.filter(company_id=company_id)
        category = CategorySerializer(category,many=True)
        client =  ClientSerializer(client,many=True)
        product = ProductSerializer(product,many=True)
        return Response({"client":client.data,"category":category.data,"product":product.data, "company_id":company_id})

        # bu savdo sahifasini ochganda  frontendga biz jonatadigan malumot

    @is_trade_permission
    def post(self, request):
        company_id = request.user.company_id
        try:
            data = request.data[0]
            client = None
            client_id = data.pop('id') # Default holatda doim 0 bilan jo'natadi
            if client_id != 0:
                try:
                    client = Client.objects.get(id=int(client_id))
                except Client.DoesNotExist:
                    return Response({"status": "error", "message": "Client not found"},
                                    status=status.HTTP_404_NOT_FOUND)
            products = data.pop('product')
            storage_product_updates = []
            for product in products:
                count = product['count']
                storage_product_id = product['storage_products']
                storage_product_updates.append((storage_product_id, count))

            for storage_product_id, count in storage_product_updates:
                updated_count = StorageProduct.objects.filter(id=storage_product_id).update(count=F('count') - count)
                if updated_count == 0:
                    return Response({"status": "error",
                                    "message": f"Storage product {storage_product_id} not found or insufficient stock"},
                                    status=status.HTTP_400_BAD_REQUEST)

            total_price = data.pop('total_price')
            trade = Trade.objects.create(
                company_id=company_id,
                client=client,
                user=request.user,
                # trade_type=TRADE_TYPE.Qarzga
                trade_date=datetime.now(),

            )

            transaction = Transaction.objects.filter(company_id=company_id)[0]

            payment = Payments.objects.create(
                company_id=company_id,
                transaction_id=transaction.id,
                user=request.user,
                trade=trade,
                client=client,
                cash=int(total_price),
                added = datetime.now(),

            )

            service_type = ServiceType.objects.filter(company_id=company_id)[0]
            Addition_service.objects.create(
                company_id=company_id,
                trade=trade,
                service_type=service_type,
                service_price = 50000,
            )
            serializers = PaymentsSerializer(payment)

            return Response(serializers.data)
        except KeyError as e:
            return Response({"status": "error", "message": f"Missing key: {e.args[0]}"},
                        status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ServiceTypeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceTypeSerializer
    filterset_class = ServiceTypeFilter
    def get_queryset(self):
        company_id = self.request.user.company_id
        queryset = ServiceType.objects.filter(company_id=company_id)
        return queryset
    def list(self, request, *args, **kwargs):
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


class AdditionServiceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AdditionServiceSerializer
    def get_queryset(self):
        company_id = self.request.user.company_id
        queryset = Addition_service.objects.filter(company_id=company_id)
        return queryset
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return serializer(serializer.data)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company_id=request.user.company_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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