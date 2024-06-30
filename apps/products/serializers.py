from rest_framework import serializers

from apps.products.models import Category, Product, Supplier, Storage, StorageProduct ,Format,StorageProductOff


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id","name"]


class StorageProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageProduct
        # fields = ["id","storage_count"]
        fields = "__all__"

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    format = FormatSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    format_id = serializers.PrimaryKeyRelatedField(queryset=Format.objects.all(), source='format', write_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'product_type', 'category', 'category_id', 'price', 'format', 'format_id', 'bar_code', 'storage_products', 'current_total_count']
        depth = 1

    def update(self, instance, validated_data):
        if 'category' in validated_data:
            instance.category = validated_data.pop('category')
        if 'format' in validated_data:
            instance.format = validated_data.pop('format')
        return super().update(instance, validated_data)

class ProductImportSerializer(serializers.Serializer):
    file = serializers.FileField()

class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = '__all__'

class  FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        fields = "__all__"

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = "__all__"


class StorageProductOffSerializer(serializers.ModelSerializer):
    class Meta:
        model = StorageProductOff
        fields = "__all__"
    
    