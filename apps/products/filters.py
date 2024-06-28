import django_filters
from apps.products.models import Product
from django.db.models import Q


class ProductFilter(django_filters.FilterSet):
    product_type = django_filters.CharFilter(method='filter_by_product_type')
    price__gte = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    price__lte = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    category__name = django_filters.CharFilter(field_name="category__name", lookup_expr='icontains')
    format__name = django_filters.CharFilter(field_name="format__name", lookup_expr='icontains')
    bar_code = django_filters.CharFilter(field_name="bar_code", lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['product_type', 'price__gte', 'price__lte', 'category__name', 'format__name', 'bar_code']

    def filter_by_product_type(self, queryset, name, value):
        product_types = value.split(',')
        query = Q()
        for product_type in product_types:
            query |= Q(product_type=product_type)
        return queryset.filter(query)