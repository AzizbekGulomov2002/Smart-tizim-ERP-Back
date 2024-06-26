from django.contrib import admin
from .models import Client, Trade,ServiceType, Addition_service

from apps.finance.models import Payments


# class TradeDetailInline(admin.TabularInline):
#     model = TradeDetail

class TradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'trade_date', 'trade_type', 'check_id')
    list_filter = ('trade_type', 'client')
    search_fields = ['client__name', 'desc']
    date_hierarchy = 'trade_date'

class ClientAdmin(admin.ModelAdmin):
    list_display = ("id",'name', 'phone', 'added',)
    search_fields = ['name', 'phone']
    date_hierarchy = 'added'

class AdditionServiceAdmin(admin.ModelAdmin):
    list_display = ('service_type', 'service_price', 'desc')
    search_fields = ['service_type__name', 'desc']

class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


admin.site.register(ServiceType, ServiceTypeAdmin)
admin.site.register(Addition_service, AdditionServiceAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Trade, TradeAdmin)
