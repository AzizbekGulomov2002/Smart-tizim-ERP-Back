from django.contrib import admin
from .models import Client, Trade, TradeDetail, ServiceType, Addition_service

from apps.finance.models import Payments


class TradeDetailInline(admin.TabularInline):
    model = TradeDetail

class AdditionServiceInline(admin.TabularInline):
    model = Addition_service

class PaymentsInline(admin.TabularInline):
    model = Payments
class TradeAdmin(admin.ModelAdmin):
    inlines = [
        TradeDetailInline,
        AdditionServiceInline,
        PaymentsInline,
    ]
    list_display = ('id', 'client', 'trade_date', 'trade_type', 'check_id')
    list_filter = ('trade_type', 'discount_type', 'client')
    search_fields = ['client__name', 'desc']
    date_hierarchy = 'trade_date'

class TradeInline(admin.TabularInline):
    model = Trade
class ClientAdmin(admin.ModelAdmin):
    inlines = [TradeInline, ]
    list_display = ('name', 'phone', 'added',)
    search_fields = ['name', 'phone']
    date_hierarchy = 'added'

class TradeDetailAdmin(admin.ModelAdmin):
    list_display = ('id', 'trade', 'product', 'discount_price', 'size_type', 'size', 'height', 'width', 'quantity', 'total_summa')
    list_filter = ('size_type',)
    search_fields = ['trade__client__name', 'product__name']
    readonly_fields = ('total_summa',)


class AdditionServiceAdmin(admin.ModelAdmin):
    list_display = ('trade', 'service_type', 'service_price', 'service_date', 'desc')
    list_filter = ('trade__client', 'service_type', 'service_date')
    search_fields = ['trade__client__name', 'service_type__name', 'desc']
    date_hierarchy = 'service_date'

class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']


admin.site.register(ServiceType, ServiceTypeAdmin)
admin.site.register(Addition_service, AdditionServiceAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Trade, TradeAdmin)
admin.site.register(TradeDetail, TradeDetailAdmin)
