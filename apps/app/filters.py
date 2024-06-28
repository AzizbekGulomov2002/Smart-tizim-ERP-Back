# import django_filters
# from apps.a.models import Position, Worker

# class PositionFilter(django_filters.FilterSet):
#     class Meta:
#         model = Position
#         fields = {
#             'name': ['exact', 'icontains'],
#         }

# class WorkerFilter(django_filters.FilterSet):
#     class Meta:
#         model = Worker
#         fields = {
#             'position__name': ['exact', 'icontains'],
#             'name': ['exact', 'icontains'],
#             'phone': ['exact', 'icontains'],
#         }