
import django_filters
from .models import Transaction

class TransactionFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields = {
            'name': ['exact', 'icontains'],
            'action_type': ['exact'],
            'transaction_type': ['exact'],
        }

