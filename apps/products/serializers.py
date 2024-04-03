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

class StorageProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()  # Nested serialization of Product

    class Meta:
        model = StorageProduct
        fields = '__all__'


class StorageSerializer(serializers.ModelSerializer):
    storage_products = StorageProductSerializer(many=True, read_only=True)
    class Meta:
        model = Storage
        fields = ['user', 'action_type', 'storage_type', 'supplier', 'storage_date', 'desc', 'storage_products']

class SupplierSerializer(serializers.ModelSerializer):
    storage_products = serializers.SerializerMethodField()
    class Meta:
        model = Supplier
        fields = ['supplier_type','name','phone','added','desc','storage_products']
    def get_storage_products(self, obj):
        # Retrieve all related StorageProduct instances for the Supplier
        storage_products = StorageProduct.objects.filter(storage__supplier=obj)
        # Serialize the queryset
        serializer = StorageProductSerializer(instance=storage_products, many=True)
        return serializer.data