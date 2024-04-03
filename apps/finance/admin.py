from django.contrib import admin
from apps.finance.models import Transaction, Payments, FinanceOutcome


# Register your models here.




@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('name', 'action_type', 'transaction_type')

@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('trade', 'transaction', 'cash', 'card', 'other_pay', 'dedline', 'added', 'check_id', 'total')

class FinanceOutcomeAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'tranzaction_type', 'client', 'worker', 'storage', 'cash', 'card', 'other_pay', 'total', 'date')
    list_filter = ('tranzaction_type', 'client', 'worker', 'storage', 'date')
    search_fields = ['name', 'client__name', 'worker__name', 'storage__name']
    date_hierarchy = 'date'

admin.site.register(FinanceOutcome, FinanceOutcomeAdmin)