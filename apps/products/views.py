from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from datetime import datetime
from apps.trade.views import CustomPaginationMixin
from apps.users.models import Company
from .models import Category,Product, Supplier, Storage, StorageProduct ,Format
from .serializers import  *
from .decorator import is_storage_permission, is_product_permission
from datetime import datetime, timedelta
from rest_framework.views import APIView
import json

from ..finance.models import Transaction, FinanceOutcome


# Product Delete Manager
class ProductDeleteManagerAPI(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        company_id = self.request.user.company_id
        all_delete = datetime.now().date() - timedelta(days=30) # Auto delete in 30 days
        delete_products = Product.all_objects.filter(company_id=company_id,deleted__lt=all_delete)
        if delete_products.exists():
            delete_products.delete()
        deleted = datetime.now().date() - timedelta(days=30)
        clients = Product.all_objects.filter(company_id=company_id,deleted__gte=deleted)
        serializer = ProductSerializer(clients, many=True)
        return Response(serializer.data)
    @is_product_permission
    def post(self,request):
        data = request.data
        try:
            id =  data['product']['id']
            product = Product.all_objects.get(id=id)
            product.restore()
        except: pass
        return Response({"status":'ok'})
    @is_product_permission
    def delete(self,request):
        company_id = self.request.user.company_id
        # print(request.user)
        # print(company_id)
        all_delete = datetime.now().date()
        client =  Product.all_objects.filter(company_id=company_id,deleted__lte=all_delete)
        # print(company_id)
        client.delete()
        return Response({"status":'ok'})


class FormatViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = FormatSerializer
    def get_queryset(self):
        company_id = self.request.user.company_id
        queryset = Format.objects.filter(company_id=company_id)
        return queryset
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
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
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class CategoryViewSet(ModelViewSet):
    permission_classes= [IsAuthenticated]
    serializer_class = CategorySerializer
    def get_queryset(self):
        company_id = self.request.user.company_id
        queryset = Category.objects.filter(company_id=company_id)
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


class ProductViewSet(CustomPaginationMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProductSerializer

    def get_queryset(self):
        company_id = self.request.user.company_id
        queryset = Product.objects.filter(company_id=company_id).order_by('-id')
        return queryset
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    @is_product_permission
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @is_product_permission
    def create(self, request, *args, **kwargs):
        ### create function is located in ProductCreateAPIView class
        return Response(status=status.HTTP_400_BAD_REQUEST)

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


class ProductCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        company_id = request.user.company_id
        products = Product.objects.filter(company_id=company_id)
        categories = Category.objects.filter(company_id=company_id)
        formats = Format.objects.filter(company_id=company_id)
        product_serializer = ProductSerializer(products, many=True)
        category_serializer = CategorySerializer(categories, many=True)
        format_serializer = FormatSerializer(formats, many=True)
        return Response({
            "products": product_serializer.data,
            "categories": category_serializer.data,
            "formats": format_serializer.data
        })
    def post(self, request):
        company_id = request.user.company_id
        data = request.data
        if not isinstance(data, list):
            return Response({"error": "Expected a list of items."}, status=status.HTTP_400_BAD_REQUEST)
        created_products = []
        for item in data:
            name = item.get("name")
            price = item.get("price")
            category_id = item.get("category_id")
            format_id = item.get("format_id")
            product_type = item.get("product_type", 'Sanaladigan')
            bar_code = item.get("bar_code", "")
            if not name or not price or not category_id or not format_id:
                return Response(
                    {"error": "name, price, category_id, and format_id are required for each product."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                Category.objects.get(company_id=company_id, id=category_id)
            except Category.DoesNotExist:
                return Response(
                    {"error": f"Invalid category_id {category_id} for the given company."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            try:
                Format.objects.get(company_id=company_id, id=format_id)
            except Format.DoesNotExist:
                return Response(
                    {"error": f"Invalid format_id {format_id} for the given company."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            # Create the product
            product = Product.objects.create(
                name=name,
                company_id=company_id,
                product_type=product_type,
                category_id=category_id,
                format_id=format_id,
                price=price,
                bar_code=bar_code,
            )
            created_products.append(product)
        serializer = ProductSerializer(created_products, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SupplierViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SupplierSerializer
    def get_queryset(self):
        company_id = self.request.user.company_id
        queryset = Supplier.objects.filter(company_id=company_id).order_by('-id')
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
        return Response(serializer, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StorageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = StorageSerializer
    def get_queryset(self):
        company_id = self.request.user.company_id
        queryset = Storage.objects.filter(company_id=company_id)
        return queryset
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    @is_storage_permission
    def retrieve(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    @is_storage_permission
    # limit
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company_id=request.user.company_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @is_storage_permission
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @is_storage_permission
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class StorageProductViewSet(CustomPaginationMixin, viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = StorageProductSerializer
    def get_queryset(self):
        company_id = self.request.user.company_id
        queryset = StorageProduct.objects.filter(company_id=company_id).order_by('-id')
        return queryset
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @is_storage_permission
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @is_storage_permission
    def create(self, request, *args, **kwargs):
        # serialaizer = self.get_serializer(data=request.data)
        # if serialaizer.is_valid():
        #     serialaizer.save(company_id=request.user.company_id)
        #     return Response(serialaizer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @is_storage_permission
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @is_storage_permission
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def parse_datetime(date_str = None):
    try: return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except:return None

def parse_date(date_str = None):
    try:return datetime.strptime(date_str, "%Y-%m-%d").date()
    except:return None


class StorageProductCreate(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        company_id = request.user.company_id
        product = Product.objects.select_related('format', 'category').prefetch_related('storage_products').filter(
            company_id=company_id)
        category = Category.objects.filter(company_id=company_id)
        supplier = Supplier.objects.filter(company_id=company_id)
        format_ = Format.objects.filter(company_id=company_id)

        productSerializer = ProductSerializer(product, many=True)
        categorySerializer = CategorySerializer(category, many=True)
        supplierSerializer = SupplierSerializer(supplier, many=True)
        formatSerializer = FormatSerializer(format_, many=True)

        return Response({
            "supplier": supplierSerializer.data,
            "category": categorySerializer.data,
            "format": formatSerializer.data,
            "product": productSerializer.data
        })

    def post(self, request):
        company_id = request.user.company_id
        data = json.loads(request.body.decode('utf-8'))
        supplier = None

        try:
            for item in data:
                if "supplier" in item:
                    supplier_id = item.get("supplier")
                    supplier = Supplier.objects.get(id=supplier_id, company_id=company_id)
                    break

            if not supplier:
                return Response({"error": "Supplier not found"}, status=status.HTTP_400_BAD_REQUEST)

            storage_products = []
            for item in data:
                if "supplier" in item:
                    continue

                product_id = item.get("product")
                if product_id:
                    product = Product.objects.get(id=product_id, company_id=company_id)
                else:
                    # Handle creation of new product if product_id is not provided
                    name = item.get("name")
                    price = item.get("price")
                    category_id = item.get("category")
                    format_id = item.get("format")
                    product, created = Product.objects.get_or_create(
                        name=name,
                        company_id=company_id,
                        defaults={
                            'product_type': item.get("product_type"),
                            'category_id': category_id,
                            'format_id': format_id,
                            'price': price,
                        }
                    )
                    if not created and product.price != price:
                        product.price = price
                        product.save()

                date = parse_datetime(item.get("date"))
                expiration = parse_date(item.get("expiration"))
                remind_count = item.get("remind_count") or 0
                size_type = item.get("size_type") or "O'lchovsiz"
                storage_type = item.get("storage_type") or "Naqtga"
                storage_price = item.get("price")  # Ensure correct field name is used

                # Ensure price is provided
                if storage_price is None:
                    return Response({"error": "Price is required"}, status=status.HTTP_400_BAD_REQUEST)

                storage_product = StorageProduct(
                    company_id=company_id,
                    storage_type=storage_type,
                    size_type=size_type,
                    storage_count=item.get("storage_count"),
                    part_size=item.get("part_size"),
                    height=item.get("height"),
                    width=item.get("width"),
                    product=product,
                    price=storage_price,
                    date=date,
                    user=request.user,
                    supplier=supplier,
                    remind_count=remind_count,
                    expiration=expiration,
                )
                storage_products.append(storage_product)

                try:
                    transaction_type = Transaction.objects.get(transaction_type='ombor', action_type='chiqim')
                    finance_outcome_data = {
                        "user": request.user,
                        "tranzaction_type": transaction_type,
                        "supplier": supplier,
                        "cash": item.get('cash', 0),
                        "card": item.get('card', 0),
                        "other_pay": item.get('other_pay', 0),
                        "desc": item.get('desc', ''),
                    }
                    if storage_type == "Naqtga":
                        FinanceOutcome.objects.create(**finance_outcome_data)
                    elif storage_type == "Qarzga":
                        finance_outcome_data["deadline"] = parse_date(item.get("deadline"))
                        FinanceOutcome.objects.create(**finance_outcome_data)
                except ObjectDoesNotExist:
                    return Response({"error": "Transaction type 'ombor' with action 'chiqim' does not exist"},
                                    status=status.HTTP_400_BAD_REQUEST)

            StorageProduct.objects.bulk_create(storage_products)
            return Response({"status": "ok"}, status=status.HTTP_201_CREATED)

        except Supplier.DoesNotExist:
            return Response({"error": "Supplier not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)





