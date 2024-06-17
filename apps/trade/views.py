from datetime import datetime, timedelta
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .filters import ServiceTypeFilter
from .models import Client, ServiceType, Addition_service, Trade
from .serializers import ClientSerializer,ServiceTypeSerializer, AdditionServiceSerializer
from ..finance.models import Transaction, Payments
from ..finance.serializers import PaymentsSerializer
from ..products.models import Product, Category, StorageProduct
from ..products.serializers import CategorySerializer, ProductSerializer
from .decorator import is_client_permission, is_trade_permission
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly


# Pagination class
class BasePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50000
    def get_paginated_response(self, data):
        return Response({
            "page_size": self.page_size,
            "total_objects": self.page.paginator.count,
            "total_pages": self.page.paginator.num_pages,
            "current_page_number": self.page.number,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data,
        })
class CustomPaginationMixin:
    pagination_class = BasePagination
class BasePermissionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

# noqa
class ClientDeleteManagerAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        company_id = self.request.user.company_id
        all_delete = datetime.now().date() - timedelta(days=30)
        delete_clients = Client.all_objects.filter(company_id=company_id,deleted__lt=all_delete)
        if delete_clients.exists():
            delete_clients.delete()
        deleted = datetime.now().date() - timedelta(days=30)
        clients = Client.all_objects.filter(company_id=company_id,deleted__gte=deleted)
        serializer = ClientSerializer(clients, many=True)
        return Response(serializer.data)
    @is_client_permission
    def post(self,request):
        data = request.data
        try:
            id =  data['client']['id']
            client = Client.all_objects.get(id=id)
            client.restore()
        except: pass
        return Response({"status":'ok'})
    @is_client_permission
    def delete(self,request):
        company_id = self.request.user.company_id
        # print(request.user)
        # print(company_id)
        all_delete = datetime.now().date()
        client =  Client.all_objects.filter(company_id=company_id,deleted__lte=all_delete)
        # print(company_id)
        client.delete()
        return Response({"status":'ok'})
    
class ClientViewSet(CustomPaginationMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer
    def get_queryset(self):
        company_id = self.request.user.company_id
        queryset = Client.objects.filter(company_id=company_id).order_by('-id')
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

    @is_client_permission  # Apply your custom permission decorator
    def post(self, request, *args, **kwargs):
        if hasattr(request.user, 'company'):
            company = request.user.company
            client_count = Client.objects.filter(company_id=company.id).count()

            if (company.tariff == "BASIC" and client_count >= 10) or \
                    (company.tariff == "PREMIUM" and client_count >= 50):
                return Response({"error": "Client limit reached for your tariff plan."},
                                status=status.HTTP_403_FORBIDDEN)

            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(company_id=company.id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "User does not have company information."}, status=status.HTTP_400_BAD_REQUEST)


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

    def get(self, request):
        company_id = request.user.company_id

        # Delete storage products with zero count
        StorageProduct.objects.filter(company_id=company_id, storage_count=0).delete()

        # Fetch categories, clients, services, and products with available stock for the company
        categories = Category.objects.filter(company_id=company_id)
        clients = Client.objects.filter(company_id=company_id)
        services = ServiceType.objects.filter(company_id=company_id)
        products = Product.objects.select_related('format', 'category') \
            .filter(company_id=company_id) \
            .prefetch_related('storage_products') \
            .filter(storage_products__storage_count__gte=1) \
            .distinct()

        # Serialize data
        category_serializer = CategorySerializer(categories, many=True)
        client_serializer = ClientSerializer(clients, many=True)
        service_serializer = ServiceTypeSerializer(services, many=True)
        product_serializer = ProductSerializer(products, many=True)

        return Response({
            "client": client_serializer.data,
            "category": category_serializer.data,
            "product": product_serializer.data,
            'service': service_serializer.data,
            "company_id": company_id
        })

    @is_trade_permission
    def post(self, request):
        company_id = request.user.company_id

        try:
            data = request.data
            client_id = data.get('client_id')
            trade_type = data.get('trade_type')
            total_price = data.get('total_price')
            discount_summa = data.get('discount_summa', 0)
            service_id = data.get("service_id")
            service_price = data.get("service_price")
            products = data.get('products', [])

            if not client_id:
                return Response({"status": "error", "message": "Client ID is required"},
                                status=status.HTTP_400_BAD_REQUEST)

            client = Client.objects.get(id=client_id, company_id=company_id)

            # Validate products and update storage counts
            description_text = ''
            for product_data in products:
                storage_product_id = product_data['storage_product_id']
                count = product_data['count']

                # Fetch and update storage product
                storage_product = StorageProduct.objects.get(id=storage_product_id, company_id=company_id)
                if storage_product.storage_count < count:
                    return Response({"status": "error", "message": f"Insufficient stock for product {storage_product.product.name}"},
                                    status=status.HTTP_400_BAD_REQUEST)

                storage_product.storage_count -= count
                storage_product.save()

                # Build description text for the trade
                description_text += f'Product {storage_product.product.name}: {count} * {storage_product.price} = {count * storage_product.price}\n'

            # Create Trade record
            trade = Trade.objects.create(
                company_id=company_id,
                client=client,
                user=request.user,
                trade_type=trade_type,
                trade_date=datetime.now(),
                discount_summa=discount_summa,
                desc=description_text
            )

            # Fetch the transaction type
            transaction = Transaction.objects.get(company_id=company_id, action_type='kirim', name='savdo')

            # Create Payment record
            payment = Payments.objects.create(
                company_id=company_id,
                transaction=transaction,
                user=request.user,
                trade=trade,
                client=client,
                cash=int(total_price),
                added=datetime.now(),
            )

            # Optionally create additional service
            if service_id is not None:
                service_type = ServiceType.objects.get(company_id=company_id, id=service_id)
                Addition_service.objects.create(
                    company_id=company_id,
                    trade=trade,
                    service_type=service_type,
                    service_price=service_price,
                    desc=data.get("service_desc", "")
                )

            payment_serializer = PaymentsSerializer(payment)
            return Response({"payment": payment_serializer.data}, status=status.HTTP_201_CREATED)

        except Client.DoesNotExist:
            return Response({"status": "error", "message": "Client not found"}, status=status.HTTP_404_NOT_FOUND)

        except StorageProduct.DoesNotExist:
            return Response({"status": "error", "message": "Storage product not found"}, status=status.HTTP_404_NOT_FOUND)

        except Transaction.DoesNotExist:
            return Response({"status": "error", "message": "Transaction type 'kirim - savdo' not found"},
                            status=status.HTTP_404_NOT_FOUND)

        except ServiceType.DoesNotExist:
            return Response({"status": "error", "message": "Service type not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)






class ServiceTypeViewSet(viewsets.ModelViewSet):
    queryset = ServiceType.objects.all().order_by("-id")
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