from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from datetime import datetime
from datetime import timedelta
from django.db.models import Sum
from apps.products.models import Product
from django.core.exceptions import ValidationError
from apps.app.models import BaseModel


class DelateManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted__isnull=True)

class Client(BaseModel):
    CLIENT_TYPE = (
        ('Tezkor', 'Tezkor'),
        ('Doimiy', 'Doimiy'),
    )
    # company_id = models.BigIntegerField(default=0)
    client_type = models.CharField(max_length=20, choices=CLIENT_TYPE,default="Tezkor")
    # name = models.CharField(max_length=400, null=True, blank=True)
    phone = models.CharField(max_length=13, null=True, blank=True)
    added = models.DateTimeField()
    desc = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    # debt = models.FloatField(null=True, blank=True)

    deleted = models.DateField(null=True, blank=True)
    objects = DelateManager()
    all_objects = models.Manager()
    def delete(self):
        self.deleted = datetime.now().date()
        self.save()
    def restore(self):
        self.deleted = None
        self.save()
    def __str__(self):
        return self.name
    


class Trade(models.Model):
    TRADE_TYPE = (
        ('Naqtga', 'Naqtga'),
        ('Qarzga', 'Qarzga'),
    )
    # DISCOUNT_TYPE = (
    #     ("Narx bo'yicha chegirma", "Narx bo'yicha chegirma"),
    #     ("Umumiy savdodan chegirma", "Umumiy savdodan chegirma"),
    # )
    company_id = models.BigIntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    trade_type = models.CharField(max_length=20, choices=TRADE_TYPE, default="Naqtga")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=Client.client_type=="Tezkor")
    # discount_type = models.CharField(max_length=24, choices=DISCOUNT_TYPE, default="Umumiy savdodan chegirma",
    #                                  null=True)
    discount_summa = models.FloatField(default=0)
    trade_date = models.DateTimeField(null=True,blank=True)
    check_id = models.IntegerField(default=10000, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)


    # cash = models.FloatField(default=0)
    # card = models.FloatField(default=0)
    # other_pay = models.FloatField(default=0)
    # @property
    # def total(self):
    #     return self.cash+self.other_pay+self.card+self.discount_summa
    
    def save(self, *args, **kwargs):
        if not self.pk:
            last_trade = Trade.objects.order_by('-check_id').first()
            if last_trade and last_trade.check_id is not None:
                self.check_id = last_trade.check_id + 1
        super().save(*args, **kwargs)


    # Trade delete Basket
    
    def delete(self):
        self.deleted = datetime.now().date()
        self.save()
    def restore(self):
        self.deleted = None
        self.save()


    def __str__(self):
        return self.client.name


class ServiceType(BaseModel):
    # company_id = models.BigIntegerField(default=0)
    # name = models.CharField(max_length=200)
    def __str__(self):
        return f"{self.name}"

# Addition service class
class Addition_service(models.Model):
    company_id = models.BigIntegerField(default=0)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name='addition_service')
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE,related_name='addition_service')
    service_price = models.PositiveBigIntegerField()
    service_date = models.DateTimeField()
    desc = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.service_type.name} - {self.service_price}"