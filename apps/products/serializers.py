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
    product = serializers.SerializerMethodField()
    format = serializers.SerializerMethodField()

    class Meta:
        model = StorageProduct
        fields = '__all__'

    def get_product(self, obj):
        product = obj.product
        return {
            'id': product.id,
            'name': product.name,
            'storage_type': product.storage_type,
            'price': product.measure,
        }

    def get_format(self, obj):
        product = obj.product
        format_obj = product.format
        return {
            'id': format_obj.id,
            'name': format_obj.name
        }


class StorageSerializer(serializers.ModelSerializer):
    storage_products = StorageProductSerializer(many=True, read_only=True)
    class Meta:
        model = Storage
        fields = ['user', 'action_type', 'storage_type', 'supplier', 'storage_date', 'desc', 'storage_products']
    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Include supplier details within the representation
        supplier_data = {
            'id': instance.supplier.id if instance.supplier else None,
            'type': instance.supplier.supplier_type if instance.supplier else None,
            'name': instance.supplier.name if instance.supplier else None
        }
        data['supplier'] = supplier_data
        # Include user details within the representation
        user_data = {
            'id': instance.user.id,
            'username': instance.user.username,
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
            'role': instance.user.role,
        }
        data['user'] = user_data
        return data

class SupplierSerializer(serializers.ModelSerializer):
    storage_products = serializers.SerializerMethodField()

    class Meta:
        model = Supplier
        fields = ['supplier_type', 'name', 'phone', 'added', 'desc', 'storage_products']

    def get_storage_products(self, obj):
        # Retrieve all related StorageProduct instances for the Supplier
        storage_products = StorageProduct.objects.filter(storage__supplier=obj)
        # Serialize the queryset
        serializer = StorageProductSerializer(instance=storage_products, many=True)
        return serializer.data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Include related Storage information within the representation
        storages = Storage.objects.filter(supplier=instance)
        storage_data = StorageSerializer(storages, many=True).data
        representation['storages'] = storage_data
        return representation