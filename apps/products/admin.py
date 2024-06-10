from django.contrib import admin
from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

# @admin.register(Format)
# class FormatAdmin(admin.ModelAdmin):
#     list_display = ('name',)

# @admin.register(Product)
# class ProductAdmin(admin.ModelAdmin):
#     list_display = ('name', 'storage_type', 'category', 'format', 'price', 'total_storage_count','current_storage_count')


# class ProductAdmin(ImportExportModelAdmin):
#     # resource_class = ProductResource
#     list_display = ['name', 'storage_type', 'category', 'format', 'price', 'bar_code']
#     search_fields = ['name', 'bar_code']
#     list_filter = ['storage_type', 'category', 'format']
#     list_editable = ['storage_type', 'category', 'format', 'price', 'bar_code']
#     list_per_page = 10

    # Optional: Customize form fields for foreign keys to show as dropdowns
    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     form.base_fields['category'].queryset = Category.objects.filter(company_id=request.user.company_id)
    #     form.base_fields['format'].queryset = Format.objects.filter(company_id=request.user.company_id)
    #     return form

admin.site.register(Product)
admin.site.register(Supplier)
admin.site.register(Format)
admin.site.register(StorageProduct)

# @admin.register(Supplier)
# class SupplierAdmin(admin.ModelAdmin):
#     list_display = ('name', 'supplier_type', 'phone', 'added', 'desc')

# @admin.register(StorageProduct)
# class StorageProductAdmin(admin.ModelAdmin):
#     list_display = ('storage', 'product',  'price','total_summa','quantity')
# class StorageProductInline(admin.TabularInline):
#     model = StorageProduct
#     extra = 1

# @admin.register(Storage)
# class StorageAdmin(admin.ModelAdmin):
#     list_display = ('user', 'storage_type', 'action_type', 'supplier', 'storage_date', 'desc')
#     inlines = [StorageProductInline]


