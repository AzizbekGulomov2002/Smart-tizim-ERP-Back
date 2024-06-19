from rest_framework import serializers
from apps.finance.models import Payments
from apps.finance.serializers import PaymentsSerializer
from apps.trade.models import Trade,Client,ServiceType,Addition_service
from django.db.models import F, Sum, Q


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = "__all__"

class AdditionServiceSerializer(serializers.ModelSerializer):
    # service_type = ServiceTypeSerializer()
    class Meta:
        model = Addition_service
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"
        # read_only_fields = ['total_payments',]





class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trade
        fields = "__all__"

    # def to_representation(self, instance):
    #     data = super().to_representation(instance)
    #     user_data = {
    #         'id': instance.user.id,
    #         'username': instance.user.username,
    #         'first_name': instance.user.first_name,
    #         'last_name': instance.user.last_name,
    #         'role': instance.user.role,
    #     }
    #     service_data = []
    #     addition_services = Addition_service.objects.filter(trade=instance)
    #     for service in addition_services:
    #         service_type_data = service.service_type.name
    #         addition_service_data = {
    #             "id": service.id,
    #             "service_price": service.service_price,
    #             "service_date": service.service_date,
    #             "desc": service.desc
    #         }
    #         service_data.append({
    #             'service_type_name': service_type_data,
    #             **addition_service_data
    #         })
    #     data['user'] = user_data
    #     data['addition_services'] = service_data
    #     return data



