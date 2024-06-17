from django.contrib import admin
from .models import User, Company,CompanyPayments

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'comp_name',"full_name", 'phone', 'email', 'is_active','tariff',"active_days")
    search_fields = ('comp_name', 'phone', 'email')
    list_filter = ('is_active', 'created')
    ordering = ('comp_name',)
admin.site.register(Company, CompanyAdmin)



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'company_id', 'role', 'is_user_create',
                    'is_trade', 'is_client', 'is_product', 'is_finance',
                    'is_statistics', 'is_storage')

    search_fields = ('username', 'email', 'company_id')



@admin.register(CompanyPayments)
class CompanyPaymentsAdmin(admin.ModelAdmin):
    list_display = ('company_id', 'sum', 'date', 'finish', 'description')
    search_fields = ('company_id',)
    list_filter = ('company_id', 'date', 'finish')
    ordering = ('-date',)