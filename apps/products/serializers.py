from rest_framework import serializers

from apps.products.models import Category, Format, Product, Supplier, Storage, StorageProduct


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = '__all__'

class StorageProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageProduct
        fields = '__all__'
