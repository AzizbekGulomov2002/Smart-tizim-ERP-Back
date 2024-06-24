from django.db import models
from django.conf import settings
from apps.app.models import BaseModel
from apps.trade.models import Client


class Transaction(BaseModel):
    ACTION_TYPE = (
        ('kirim', "kirim"),
        ('chiqim', "chiqim"),
    )
    TRANSACTION_TYPE = (
        ('mijoz', "mijoz"),
        ('ombor', "ombor"),
        ('hodim', "hodim"),
        ('boshqa', "Boshqa")
    )
    action_type = models.CharField(max_length=100, choices=ACTION_TYPE, default='kirim')
    transaction_type = models.CharField(max_length=100, choices=TRANSACTION_TYPE)
    def __str__(self):
        return self.name


class Payments(models.Model):
    # PAYMENT_TYPE = (
    #     ("Savdoga to'lov", "Savdoga to'lov"),
    #     ("Mijozga to'lov", "Mijozga to'lov"),
    # )
    company_id = models.BigIntegerField(default=0)
    # payment_type = models.CharField(max_length=100, choices=PAYMENT_TYPE, default="Savdoga to'lov")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    # trade = models.ForeignKey(Trade, on_delete=models.CASCADE, null=True, blank=True, related_name="trade_set")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True, related_name="payments_set")
    # storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)

    cash = models.FloatField(default=0)
    card = models.FloatField(default=0)
    other_pay = models.FloatField(default=0)

    deadline = models.DateField(null=True, blank=True)
    added = models.DateTimeField()
    check_id =models.IntegerField(default=10000, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            last_payment = Payments.objects.order_by('-check_id').first()
            if last_payment and last_payment.check_id is not None:
                self.check_id = last_payment.check_id + 1
        super().save(*args, **kwargs)

    @property
    def total(self):
        return self.cash+self.other_pay+self.card
    def __str__(self):
        return str(self.total)
    class Meta:
        verbose_name_plural = 'Payments'
        verbose_name = 'Payment'



class FinanceOutcome(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    tranzaction_type = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey("products.Supplier", on_delete=models.CASCADE, null=True, blank=True)
    storage_product = models.ForeignKey("products.StorageProduct", on_delete=models.CASCADE, null=True, blank=True) # For delete StorageProduct related FinanceOutcome

    cash = models.FloatField(default=0)
    card = models.FloatField(default=0)
    other_pay = models.FloatField(default=0)

    date = models.DateTimeField(null=True, blank=True)
    desc = models.TextField(blank=True, null=True)

    deadline = models.DateField(null=True, blank=True)

    @property
    def total(self):
        return self.cash + self.other_pay + self.card

    def __str__(self):
        return self.name
