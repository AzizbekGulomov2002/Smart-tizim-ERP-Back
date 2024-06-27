import django_filters
from apps.products.models import Product
class ProductFilter(django_filters.FilterSet):
    product_type = django_filters.ChoiceFilter(choices=Product.PRODUCT_TYPE)
    price__gte = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    price__lte = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    category__name = django_filters.CharFilter(field_name="category__name", lookup_expr='icontains')
    format__name = django_filters.CharFilter(field_name="format__name", lookup_expr='icontains')
    bar_code = django_filters.CharFilter(field_name="bar_code", lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['product_type', 'price__gte', 'price__lte', 'category__name', 'format__name', 'bar_code']