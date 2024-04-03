from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from apps.app.models import Position, Worker
from apps.app.serializers import PositionSerializer, WorkerSerializer
from rest_framework.views import APIView
from django.utils import timezone
from apps.products.models import Product, Category
from apps.trade.models import Client, Trade
from django.utils.dateparse import parse_date
from django.db.models import Count, Sum

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer

class WorkerViewSet(viewsets.ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer





class DynamicStatistics(APIView):
    def get(self, request):
        # Get trade count by date
        trade_by_date = Trade.objects.values('trade_date__date').annotate(trade_count=Count('id'))
        # Get top products
        top_products = Product.objects.annotate(trade_count=Count('trade')).order_by('-trade_count')[:10]
        # Format trade_by_date to match desired output
        formatted_trade_by_date = [{'trade_date': item['trade_date__date'], 'trade_count': item['trade_count']} for item in trade_by_date]
        formatted_top_products = [{'product_name': item.name} for item in top_products]

        return Response({
            'trade_by_date': formatted_trade_by_date,
            'top_products': formatted_top_products,
        })







class StaticStatistics(APIView):
    def get(self, request):
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