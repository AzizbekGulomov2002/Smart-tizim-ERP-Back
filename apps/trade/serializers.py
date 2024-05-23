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
    service_type = ServiceTypeSerializer()
    class Meta:
        model = Addition_service
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    # total_payments = serializers.SerializerMethodField()
    #
    # def get_total_payments(self, obj):
    #     total_payments = Payments.objects.filter(
    #         client=obj
    #     ).aggregate(
    #         total=Sum(F('cash') + F('card') + F('other_pay'))
    #     )['total'] or 0
    #     return total_payments

    # def get_trades(self, obj):
    #     trades = Trade.objects.filter(client=obj)
    #     return TradeSerializer(trades, many=True).data
    # def get_debt_balance(self, obj):
    #     total_trade_summa = sum(trade.total_trade_summa for trade in obj.trade_set.all())
    #     total_payments_summa = self.get_total_payments(obj)
    #     return total_trade_summa - total_payments_summa
    # def get_status(self, obj):
    #     debt_balance = self.get_debt_balance(obj)
    #     if debt_balance > 0:
    #         return "Qarzdor"
    #     else:
    #         return "To'langan"

    class Meta:
        model = Client
        fields = "__all__"
        # read_only_fields = ['total_payments',]





class TradeSerializer(serializers.ModelSerializer):
    # payments = serializers.SerializerMethodField()
    # def get_payments(self, obj):
    #     # Retrieve payments associated with either the trade or the client
    #     payments = Payments.objects.filter(Q(trade=obj) | Q(client=obj.client))
    #     return PaymentsSerializer(payments, many=True).data
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



