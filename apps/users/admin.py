from django.contrib import admin
from .models import User, Company

class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'comp_name', 'phone', 'email', 'is_active', 'start_date', 'end_date', 'sum')
    search_fields = ('comp_name', 'phone', 'email')
    list_filter = ('is_active', 'start_date', 'end_date')
    fields = ('comp_name', 'phone', 'email', 'is_active', 'start_date', 'end_date', 'sum')
    ordering = ('comp_name',)
admin.site.register(Company, CompanyAdmin)



class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_active', 'company_id', 'role', 'is_user_create', 'is_trade', 'is_client', 'is_product', 'is_finance', 'is_statistics', 'is_storage')
    search_fields = ('username', 'is_active', 'company_id')  # Add more fields if needed

admin.site.register(User, CustomUserAdmin)

