from django.contrib import admin
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Supplier)
admin.site.register(Format)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'product_type')

@admin.register(StorageProduct)
class StorageProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_product_name', 'date', 'storage_count','total_summa',"storage_type","size_type")
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




