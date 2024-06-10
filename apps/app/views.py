from datetime import datetime

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.functions import Coalesce
from apps.finance.models import Payments, FinanceOutcome, Transaction
from apps.products.models import Product, Category
from apps.trade.models import Client, Trade, Addition_service
from django.utils.dateparse import parse_date
from django.db.models import Sum, F, Value
from rest_framework import status
from apps.users.models import Company
from .decorator import is_statistics_permission


class DynamicStatistics(APIView):
    @is_statistics_permission
    def get(self, request):
        company = Company.objects.get(id=request.user.company_id)

        if company.tariff == "Basic":
            return Response({"error": "This feature is not available for Basic tariff plans."}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve start_date and end_date from query parameters
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d') if start_date_str else None
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') if end_date_str else None

        if start_date and end_date:
            # Calculate total payment within the specified date range
            total_cash_payment = Coalesce(Sum('cash'), Value(0))
            total_card_payment = Coalesce(Sum('card'), Value(0))
            total_other_payment = Coalesce(Sum('other_pay'), Value(0))

            total_payment = Payments.objects.filter(added__range=[start_date, end_date]) \
                .aggregate(
                total_cash_payment=total_cash_payment,
                total_card_payment=total_card_payment,
                total_other_payment=total_other_payment
            )

            # Extract the individual payment totals
            total_cash = total_payment['total_cash_payment']
            total_card = total_payment['total_card_payment']
            total_other = total_payment['total_other_payment']
            total_payment_summa = total_cash + total_card + total_other

            # Calculate total finance outcome within the specified date range
            total_finance_outcome = FinanceOutcome.objects.filter(date__range=[start_date, end_date]) \
                .aggregate(total_outcome=Coalesce(Sum(F('cash') + F('other_pay') + F('card')), Value(0)))['total_outcome']

            # Calculate total trade sum within the specified date range
            total_trade_summa = 0
            trade_queryset = Trade.objects.filter(trade_details__trade__trade_date__date__range=[start_date, end_date])
            for trade in trade_queryset:
                total_trade_summa += trade.total_trade_summa

            addition_services = Addition_service.objects.filter(service_date__range=[start_date, end_date])
            addition_services_list = [{'name': service.service_type.name, 'price': service.service_price} for service in
                                      addition_services]
            total_addition_service = sum(service['price'] for service in addition_services_list)

            # Get transaction names and their total sums
            transaction_names = []
            for transaction in Transaction.objects.all():
                total_sum = FinanceOutcome.objects.filter(tranzaction_type=transaction, date__range=[start_date, end_date]) \
                    .aggregate(total_sum=Coalesce(Sum(F('cash') + F('other_pay') + F('card')), Value(0)))['total_sum']
                transaction_names.append({
                    'name': transaction.name,
                    'total_sum': total_sum
                })

            return Response({
                'total_payments': {
                    "total_cash_payment": total_cash,
                    "total_card_payment": total_card,
                    "total_other_payment": total_other,
                },
                "total_payment_summa": total_payment_summa,
                'total_finance_outcome': total_finance_outcome,
                'total_trade_summa': total_trade_summa,
                'total_addition_service': total_addition_service,
                'transaction_names': transaction_names,
                'addition_services': addition_services_list,
            })

        else:  # If start_date and end_date are not provided
            # Calculate total payment
            total_payment = Payments.objects.aggregate(
                total_payment=Coalesce(Sum('cash'), Value(0)) + Coalesce(Sum('other_pay'), Value(0)) + Coalesce(Sum('card'), Value(0)))['total_payment']

            # Calculate total finance outcome
            total_finance_outcome = FinanceOutcome.objects.aggregate(
                total_outcome=Coalesce(Sum(F('cash') + F('other_pay') + F('card')), Value(0)))['total_outcome']

            # Calculate total trade sum
            total_trade_summa = 0
            for trade in Trade.objects.all():
                total_trade_summa += trade.total_trade_summa

            return Response({
                'total_payment': total_payment,
                'total_finance_outcome': total_finance_outcome,
                'total_trade_summa': total_trade_summa,
                'total_debt_balance': total_trade_summa - total_payment,
            })



class StaticStatistics(APIView):
    @is_statistics_permission
    def get(self, request):
        company = Company.objects.get(id=request.user.company_id)

        if company.tariff == "Basic":
            return Response({"error": "This feature is not available for Basic tariff plans."}, status=status.HTTP_403_FORBIDDEN)

        # Retrieve start_date and end_date from query parameters
        start_date_str = request.query_params.get('start_date')
        end_date_str = request.query_params.get('end_date')

        # Parse start and end dates if provided and valid, default to today's date if not provided
        start_date = parse_date(start_date_str) if start_date_str else None
        end_date = parse_date(end_date_str) if end_date_str else None

        # Define queryset for each model
        product_queryset = Product.objects.all()
        client_queryset = Client.objects.all()
        trade_queryset = Trade.objects.all()
        category_queryset = Category.objects.all()

        # Filter trade_queryset and client_queryset based on start and end dates
        if start_date and end_date:
            trade_queryset = trade_queryset.filter(trade_date__date__range=[start_date, end_date])
            client_queryset = client_queryset.filter(added__range=[start_date, end_date])

        # Calculate totals for each model
        product_total = product_queryset.count()
        client_total = client_queryset.count()
        trade_total = trade_queryset.count()
        category_total = category_queryset.count()

        return Response({
            'product_total': product_total,
            'client_total': client_total,
            'trade_total': trade_total,
            'category_total': category_total,
        })