from django.db import models
from django.conf import settings
from datetime import datetime
from apps.app.models import BaseModel


class DelateManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted__isnull=True)

class Client(BaseModel):
    CLIENT_TYPE = (
        ('Tezkor', 'Tezkor'),
        ('Doimiy', 'Doimiy'),
    )
    client_type = models.CharField(max_length=20, choices=CLIENT_TYPE,default="Tezkor")
    phone = models.CharField(max_length=13, null=True, blank=True)
    added = models.DateTimeField()
    desc = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)


    deleted = models.DateField(null=True, blank=True)
    objects = DelateManager()
    all_objects = models.Manager()
    def delete(self):
        self.deleted = datetime.now().date()
        self.save()
    def restore(self):
        self.deleted = None
        self.save()

    @property
    def status(self):
        return "Status"
    def __str__(self):
        return self.name
    


class Trade(models.Model):
    TRADE_TYPE = (
        ('Naqtga', 'Naqtga'),
        ('Qarzga', 'Qarzga'),
    )
    company_id = models.BigIntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    trade_type = models.CharField(max_length=20, choices=TRADE_TYPE, default="Naqtga")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, default=Client.client_type=="Tezkor")
    discount_summa = models.FloatField(default=0)
    trade_date = models.DateTimeField(null=True,blank=True)
    check_id = models.IntegerField(default=10000, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)

    
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
    def __str__(self):
        return f"{self.name}"

# Addition service class
class Addition_service(models.Model):
    company_id = models.BigIntegerField(default=0)
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name='addition_service')
    service_type = models.ForeignKey(ServiceType, on_delete=models.CASCADE,related_name='addition_service')
    service_price = models.PositiveBigIntegerField()
    # service_date = models.DateTimeField(null=True, blank=True) # noqa
    desc = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.service_type.name} - {self.service_price}"