import django_filters
from apps.products.models import Product
class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'icontains'],
            'category': ['exact'],
            'format': ['exact'],
            'price': ['exact', 'gte', 'lte'],
        }
