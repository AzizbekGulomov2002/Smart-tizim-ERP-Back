from rest_framework import serializers

from apps.products.models import Category, Product, Supplier, Storage, StorageProduct


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class StorageProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageProduct
        fields = ["id","count"]

class ProductSerializer(serializers.ModelSerializer):
    # storage_products = StorageProductSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id','name','storage_type','price','format','bar_code','storage_products'] # <  qoganlari ozgarsaham  storage_products   shu ozgarmasin
        depth = 1



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
        fields = ["id",'supplier_type', 'name', 'phone', 'added', 'desc', 'storage_products']

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