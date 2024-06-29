import django_filters
from apps.products.models import Product, Category, Format
from django.db.models import Q


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    product_type = django_filters.CharFilter(method='filter_by_product_type')
    price__gte = django_filters.NumberFilter(field_name="price", lookup_expr='gte')
    price__lte = django_filters.NumberFilter(field_name="price", lookup_expr='lte')
    category_id = django_filters.CharFilter(method='filter_by_category_id')
    format_id = django_filters.NumberFilter(field_name="format_id", lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['name', 'product_type', 'price__gte', 'price__lte', 'category_id', 'format_id']

    def filter_by_product_type(self, queryset, name, value):
        product_types = value.split(',')
        query = Q()
        for product_type in product_types:
            query |= Q(product_type=product_type)
        return queryset.filter(query)

    def filter_by_category_id(self, queryset, name, value):
        category_ids = value.split(',')
        return queryset.filter(category_id__in=category_ids)


class CategoryFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains')
    class Meta:
        model = Category
        fields = ['name']


class FormatFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains')
    class Meta:
        model = Format
        fields = ['name']