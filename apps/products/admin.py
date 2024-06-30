from django.contrib import admin
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id','name','supplier_type')

@admin.register(Format)
class FormatAdmin(admin.ModelAdmin):
    list_display = ('id','name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id','storage','category', 'name', 'price', 'product_type','current_total_count')

@admin.register(StorageProduct)
class StorageProductAdmin(admin.ModelAdmin):
    list_display = ('id','storage','get_product_name', 'date',"storage_type","size_type",'price', "total_count",'total_summa')
    list_filter = ('date',)
    search_fields = ('product__name',)
    ordering = ('-date',)
    def get_product_name(self, obj):
        return obj.product.name
    get_product_name.short_description = 'Product Name'
    get_product_name.admin_order_field = 'product__name'


@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('id','name',)


@admin.register(StorageProductOff)
class StorageProductOffAdmin(admin.ModelAdmin):
    list_display = ('id',"count")



