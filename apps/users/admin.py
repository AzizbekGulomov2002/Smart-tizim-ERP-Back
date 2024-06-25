from django.contrib import admin
from .models import User, Company,CompanyPayments

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'comp_name', 'is_active','tariff','created',"active_days")
    search_fields = ('comp_name', )
    list_filter = ('is_active', 'created')
    ordering = ('comp_name',)
admin.site.register(Company, CompanyAdmin)



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'company_id', 'is_active','role', 'is_user_create')
    search_fields = ('username', 'email', 'company_id')


@admin.register(CompanyPayments)
class CompanyPaymentsAdmin(admin.ModelAdmin):
    list_display = ('company_id', 'sum', 'date', 'finish', 'description')
    search_fields = ('company_id',)
    list_filter = ('company_id', 'date', 'finish')
    ordering = ('-date',)