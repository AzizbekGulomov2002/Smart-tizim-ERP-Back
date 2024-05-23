import django_filters
from .models import Client, Trade, ServiceType

class ClientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    phone = django_filters.CharFilter(field_name='phone', lookup_expr='icontains')
    client_type = django_filters.ChoiceFilter(field_name='client_type', choices=Client.CLIENT_TYPE)
    added = django_filters.DateFilter(field_name='added', lookup_expr='date')
    debt_balance = django_filters.NumberFilter(method='filter_debt_balance')

    class Meta:
        model = Client
        fields = ['name', 'phone', 'client_type', 'added', 'debt_balance']

    def filter_debt_balance(self, queryset, name, value):
        if value == 'positive':
            return queryset.filter(debt_balance__gt=0)
        elif value == 'negative':
            return queryset.filter(debt_balance__lt=0)
        elif value == 'zero':
            return queryset.filter(debt_balance=0)
        return queryset

    def filter_status(self, queryset, name, value):
        if value == 'Qarzdor':
            return queryset.filter(debt_balance__gt=0)
        elif value == 'To\'langan':
            return queryset.filter(debt_balance__lte=0)
        return queryset

class TradeFilter(django_filters.FilterSet):
    class Meta:
        model = Trade
        fields = {
            'trade_type': ['exact'],
            'client': ['exact'],
        }

class ServiceTypeFilter(django_filters.FilterSet):
    class Meta:
        model = ServiceType
        fields = {
            'name': ['exact', 'icontains'],
        }
