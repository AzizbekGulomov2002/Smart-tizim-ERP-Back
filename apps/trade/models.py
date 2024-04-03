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

        if self.discount_type == "Umumiy savdodan chegirma":
            return self.discount_summa
        else:
            return trade_details_sum + addition_services_sum - self.discount_summa


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

    size_type = models.CharField(max_length=20, choices=SIZE_TYPE, default="O'lchovsiz")
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name='trade_details')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    discount_price = models.PositiveIntegerField(default=1)

    size = models.FloatField(default=1)
    height = models.FloatField(default=1)
    width = models.FloatField(default=1)
    quantity = models.FloatField(default=1)

    @property
    def total_summa(self):
        if self.discount_price > 1:
            return self.height * self.width * self.quantity * self.discount_price
        elif self.size > 1:
            return self.size * self.quantity * self.product.price
        else:
            return self.height * self.width * self.quantity * self.product.price

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