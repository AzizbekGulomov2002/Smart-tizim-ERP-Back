from django.contrib import admin
from .models import Category, Format, Product, Supplier, Storage, StorageProduct

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Format)
class FormatAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'storage_type', 'category', 'format', 'measure', 'price', 'total_storage_count')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'supplier_type', 'phone', 'added', 'desc')

@admin.register(StorageProduct)
class StorageProductAdmin(admin.ModelAdmin):
    list_display = ('storage', 'product', 'storage_count', 'price')
class StorageProductInline(admin.TabularInline):
    model = StorageProduct
    extra = 1

@admin.register(Storage)
class StorageAdmin(admin.ModelAdmin):
    list_display = ('user', 'storage_type', 'action_type', 'supplier', 'storage_date', 'desc')
    inlines = [StorageProductInline]


