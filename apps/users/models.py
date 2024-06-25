from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser



class Company(models.Model):
    TARIFF = (
        ('BASIC', 'Basic'),
        ('STANDART', 'Standart'),
        ('BEST', 'Best'),
    )
    comp_name = models.CharField(max_length=500)
    # full_name = models.CharField(max_length=500) # noqa
    # phone = models.IntegerField(unique=True)
    # email = models.EmailField(null=True,unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    created = models.DateField() 

    active_days = models.DateField()
    # end_date = models.DateField(null=True,blank=True)
    # sum = models.IntegerField(default=0)
    tariff = models.CharField(max_length=20, choices=TARIFF, default="Best")
    currency_type = models.CharField(max_length=200, help_text="Valyuta turini bering: So'm, Rubl, Dollar ...")

    # @property
    # def status(self):
    #     today = timezone.now().date()
    #     difference = (today - self.created).days
    #     if difference >= self.days:
    #         return Company.is_active == False
    #     else:
    #         return Company.is_active == True
    def __str__(self):
        return self.comp_name




class User(AbstractUser):
    company_id = models.BigIntegerField(default=0)
    class Role(models.TextChoices):
        DIRECTOR = "DIRECTOR", "director"
        MANAGER = "MANAGER", "manager"

    is_user_create = models.BooleanField(default=False)
    is_trade = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_product = models.BooleanField(default=False)
    is_finance = models.BooleanField(default=False)
    is_statistics = models.BooleanField(default=False)
    is_storage = models.BooleanField(default=False)
    description = models.TextField(verbose_name="Description", null=True, blank=True)
    role = models.CharField(max_length=15, choices=Role.choices)
    def __str__(self):
        return self.username
    class Meta:
        db_table = "User"



class CompanyPayments(models.Model):
    company_id = models.BigIntegerField(default=0)
    sum = models.FloatField()
    date = models.DateTimeField()
    finish = models.DateField()
    description = models.TextField(null=True,blank=True)

    def __str__(self):
        return f"Company: {self.company_id} | Payment: {self.sum}"
    
    class Meta:
        verbose_name = "Company Payment"
        verbose_name_plural = "Company Payments"
    