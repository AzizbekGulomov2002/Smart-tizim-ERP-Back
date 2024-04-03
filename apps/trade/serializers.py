from rest_framework import serializers

from apps.finance.models import Payments
from apps.finance.serializers import PaymentsSerializer
from apps.products.models import Product
from apps.products.serializers import ProductSerializer
from apps.trade.models import Trade,TradeDetail,Client,ServiceType,Addition_service
from apps.users.serializers import UserSerializer
from django.db.models import F, Sum, Q


class ServiceTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceType
        fields = ['name']

class AdditionServiceSerializer(serializers.ModelSerializer):
    service_type = ServiceTypeSerializer()
    class Meta:
        model = Addition_service
        fields = ['id','service_type','service_price','service_date','desc']


class ClientSerializer(serializers.ModelSerializer):
    total_payments = serializers.SerializerMethodField()
    debt_balance = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    trades = serializers.SerializerMethodField()

    def get_total_payments(self, obj):
        # Aggregate payments for both client and trade associated with the client
        total_client_payments = Payments.objects.filter(client=obj).aggregate(
            total=Sum(F('cash') + F('card') + F('other_pay')))
        total_trade_payments = Payments.objects.filter(trade__client=obj).aggregate(
            total=Sum(F('cash') + F('card') + F('other_pay')))

        # Sum up the total payments for both client and trade
        total = (total_client_payments['total'] if total_client_payments['total'] else 0) + \
                (total_trade_payments['total'] if total_trade_payments['total'] else 0)

        return total
    def get_trades(self, obj):
        trades = Trade.objects.filter(client=obj)
        return TradeSerializer(trades, many=True).data
    def get_debt_balance(self, obj):
        total_trade_summa = sum(trade.total_trade_summa for trade in obj.trade_set.all())
        total_payments_summa = self.get_total_payments(obj)
        return total_trade_summa - total_payments_summa
    def get_status(self, obj):
        debt_balance = self.get_debt_balance(obj)
        if debt_balance > 0:
            return "Qarzdor"
        else:
            return "To'langan"

    class Meta:
        model = Client
        fields = ['id', 'client_type', 'name', 'phone', 'added', 'total_payments', 'debt_balance', 'status', 'trades']
        read_only_fields = ['total_payments', 'debt_balance', 'status', 'trades']





class TradeSerializer(serializers.ModelSerializer):
    payments = serializers.SerializerMethodField()
    trade_details = serializers.SerializerMethodField()
    def get_trade_details(self, obj):
        trade_details = TradeDetail.objects.filter(trade=obj)
        return TradeDetailSerializer(trade_details, many=True).data
    def get_payments(self, obj):
        # Retrieve payments associated with either the trade or the client
        payments = Payments.objects.filter(Q(trade=obj) | Q(client=obj.client))
        return PaymentsSerializer(payments, many=True).data
    class Meta:
        model = Trade
        fields = ['id', 'user', 'trade_type', 'client', 'discount_type', 'trade_date', 'check_id', 'desc', 'trade_details','payments','total_trade_summa']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        user_data = {
            'id': instance.user.id,
            'username': instance.user.username,
            'first_name': instance.user.first_name,
            'last_name': instance.user.last_name,
            'role': instance.user.role,
        }
        service_data = []
        addition_services = Addition_service.objects.filter(trade=instance)
        for service in addition_services:
            service_type_data = service.service_type.name
            addition_service_data = {
                "id": service.id,
                "service_price": service.service_price,
                "service_date": service.service_date,
                "desc": service.desc
            }
            service_data.append({
                'service_type_name': service_type_data,
                **addition_service_data
            })
        data['user'] = user_data
        data['addition_services'] = service_data
        return data




class TradeDetailSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField()
    class Meta:
        model = TradeDetail
        fields = ['id', 'size_type', 'trade', 'products', 'discount_price',
                  'size', 'height', 'width', 'quantity', 'total_summa']
    def get_products(self, obj):
        return {
            'id': obj.product.id,
            'name': obj.product.name,
            'category_name': obj.product.category.name,
            'format_name': obj.product.format.name,
            'price': obj.product.price,
            'storage_type': obj.product.storage_type
        }


