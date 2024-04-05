from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from datetime import datetime
from datetime import timedelta
from django.db.models import Sum
from apps.products.models import Product


class Client(models.Model):
    CLIENT_TYPE = (
        ('Tezkor', 'Tezkor'),
        ('Doimiy', 'Doimiy'),
    )
    client_type = models.CharField(max_length=20, choices=CLIENT_TYPE,default="Tezkor")
    name = models.CharField(max_length=400)
    phone = models.CharField(max_length=13)
    added = models.DateTimeField()
    desc = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name



class Trade(models.Model):
    TRADE_TYPE = (
        ('Naqtga', 'Naqtga'),
        ('Qarzga', 'Qarzga'),
    )
    DISCOUNT_TYPE = (
        ("Narx bo'yicha chegirma", "Narx bo'yicha chegirma"),
        ("Umumiy savdodan chegirma", "Umumiy savdodan chegirma"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    trade_type = models.CharField(max_length=20, choices=TRADE_TYPE, default="Naqtga")
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    discount_type = models.CharField(max_length=24, choices=DISCOUNT_TYPE, default="Umumiy savdodan chegirma",
                                     null=True)
    discount_summa = models.PositiveIntegerField(default=0)
    trade_date = models.DateTimeField()
    check_id = models.IntegerField(default=10000, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            last_trade = Trade.objects.order_by('-check_id').first()
            if last_trade and last_trade.check_id is not None:
                self.check_id = last_trade.check_id + 1
        super().save(*args, **kwargs)

    @property
    def total_trade_summa(self):
        trade_details_sum = sum(detail.total_summa for detail in self.trade_details.all())
        addition_services_sum = sum(service.service_price for service in self.addition_service.all())
        return trade_details_sum + addition_services_sum - self.discount_summa
        print(self.service_price)



    def __str__(self):
        return f"{self.trade_date.strftime('%Y-%m-%d %H:%M:%S')} | {self.client.name}"


class TradeDetail(models.Model):
    SIZE_TYPE = (
        ("O'lchovli", "O'lchovli"),
        ("O'lchovsiz", "O'lchovsiz"),
        ("Formatli", "Formatli"),
    )
    DETAIL_TYPE = (
        ("Narxida", "Narxida"),
        ("Chegirmada", "Chegirmada"),
    )
    detail_type = models.CharField(max_length=30, choices=DETAIL_TYPE, default="Narxida")
    size_type = models.CharField(max_length=20, choices=SIZE_TYPE, default="O'lchovsiz")
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name='trade_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')

    discount_price = models.PositiveIntegerField(default=1)

    size = models.FloatField(default=1)
    height = models.FloatField(default=1)
    width = models.FloatField(default=1)

    count = models.FloatField(default=1)

    @property
    def quantity(self):
        if self.size_type == "O'lchovli":
            return self.size * self.count
        elif self.size_type == "Formatli":
            return self.height * self.width * self.count
        elif self.size_type == "O'lchovsiz":
            return self.count
        else:
            return self.count

    @property
    def total_summa(self):
        if self.detail_type == "Narxida":
            return self.quantity * self.product.price
        elif self.detail_type == "Chegirmada":
            return self.quantity * self.discount_price
        else:
            return 0

    def __str__(self):
            return f"{self.trade.trade_date.strftime('%Y-%m-%d %H:%M:%S')}"


class ServiceType(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return f"{self.name}"

# Addition service class
class Addition_service(models.Model):
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name='addition_service')
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE,related_name='addition_service')
    service_price = models.PositiveBigIntegerField()
    service_date = models.DateTimeField()
    desc = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.service_type.name} - {self.service_price}"