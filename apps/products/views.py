from django.shortcuts import render
from rest_framework import viewsets
from .models import Category, Format, Product, Supplier, Storage, StorageProduct
from .serializers import CategorySerializer, FormatSerializer, ProductSerializer, SupplierSerializer, StorageSerializer, StorageProductSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class FormatViewSet(viewsets.ModelViewSet):
    queryset = Format.objects.all()
    serializer_class = FormatSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer

class StorageProductViewSet(viewsets.ModelViewSet):
    queryset = StorageProduct.objects.all()
    serializer_class = StorageProductSerializer
