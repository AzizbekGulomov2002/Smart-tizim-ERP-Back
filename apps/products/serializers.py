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
    class Meta:
        model = Product
        fields = ['id','name','product_type', "category",'price','format','bar_code', 'storage_products','current_total_count'] # <  qoganlari ozgarsaham  storage_products   shu ozgarmasin
        depth = 1



class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = '__all__'

class  FormatSerializer (serializers.ModelSerializer):
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
    
    