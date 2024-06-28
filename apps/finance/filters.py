
import django_filters
from .models import Transaction, Payments


class TransactionFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields = {
            'name': ['exact', 'icontains'],
            'action_type': ['exact'],
            'transaction_type': ['exact'],
        }



class PaymentsFilter(django_filters.FilterSet):
    min_cash = django_filters.NumberFilter(field_name="cash", lookup_expr='gte')
    max_cash = django_filters.NumberFilter(field_name="cash", lookup_expr='lte')
    min_card = django_filters.NumberFilter(field_name="card", lookup_expr='gte')
    max_card = django_filters.NumberFilter(field_name="card", lookup_expr='lte')
    min_other_pay = django_filters.NumberFilter(field_name="other_pay", lookup_expr='gte')
    max_other_pay = django_filters.NumberFilter(field_name="other_pay", lookup_expr='lte')
    start_date = django_filters.DateFilter(field_name="added", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="added", lookup_expr='lte')

    class Meta:
        model = Payments
        fields = ['client', 'transaction', 'min_cash', 'max_cash', 'min_card', 'max_card', 'min_other_pay', 'max_other_pay', 'start_date', 'end_date']
