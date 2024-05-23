from rest_framework import serializers
from .models import Transaction, Payments, FinanceOutcome

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class PaymentsSerializer(serializers.ModelSerializer):
    # def get_trade(self, obj):
    #     if obj.trade:
    #         return {
    #             'id': obj.trade.id,
    #             'trade_date': obj.trade.trade_date
    #             # Add more fields as needed
    #         }
    #     return None
    #
    # def get_client(self, obj):
    #     if obj.client:
    #         return {
    #             'id': obj.client.id,
    #             'name': obj.client.name,
    #             # Add more fields as needed
    #         }
    #     return None
    #
    # def get_transaction(self, obj):
    #     if obj.transaction:
    #         return {
    #             'id': obj.transaction.id,
    #             'name': obj.transaction.name,
    #         }
    #     return None
    #
    # def get_user(self, obj):
    #     if obj.user:
    #         return {
    #             'id': obj.user.id,
    #             'username': obj.user.username,
    #             'first_name': obj.user.first_name,
    #             'last_name': obj.user.last_name,
    #             # Add more fields as needed
    #         }
    #     return None

    class Meta:
        model = Payments
        fields = "__all__"

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     representation['trade'] = self.get_trade(instance)
    #     representation['client'] = self.get_client(instance)
    #     representation['transaction'] = self.get_transaction(instance)
    #     representation['user'] = self.get_user(instance)
    #     return representation




class FinanceOutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinanceOutcome
        fields = '__all__'
