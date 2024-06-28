import django_filters
from apps.trade.models import Client, Trade, ServiceType


class ClientFilter(django_filters.FilterSet):
    client_type = django_filters.ChoiceFilter(choices=Client.CLIENT_TYPE)
    phone = django_filters.CharFilter(lookup_expr='icontains')
    is_active = django_filters.BooleanFilter()
    added = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Client
        fields = ['client_type', 'phone', 'is_active', 'added']


class TradeFilter(django_filters.FilterSet):
    trade_type = django_filters.ChoiceFilter(choices=Trade.TRADE_TYPE)
    client = django_filters.ModelChoiceFilter(queryset=Client.objects.all())
    trade_date = django_filters.DateFromToRangeFilter()
    class Meta:
        model = Trade
        fields = ['trade_type', 'client', 'trade_date']


class ServiceTypeFilter(django_filters.FilterSet):
    class Meta:
        model = ServiceType
        fields = {
            'name': ['exact', 'icontains'],
        }
