from datetime import timezone

from django.db import models
from django.contrib.auth.models import AbstractUser


class Company(models.Model):
    comp_name = models.CharField(max_length=500,unique=True)
    phone = models.IntegerField(unique=True)
    email = models.EmailField(null=True,unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    sum = models.IntegerField(default=0)

    def __str__(self):
        return self.comp_name





class User(AbstractUser):
    company_id = models.BigIntegerField(default=0)
    class Role(models.TextChoices):
        COMPANY = "COMPANY" , "company"
        DIRECTOR = "DIRECTOR", "director"
        MANAGER = "MANAGER", "manager"
        KASSA  = 'KASSA' ,'kassa'
        STORAGE = 'STORAGE' ,'storage'

    is_user_create = models.BooleanField(default=False)
    is_trade = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_product = models.BooleanField(default=False)
    is_finance = models.BooleanField(default=False)
    is_statistics = models.BooleanField(default=False)
    is_storage = models.BooleanField(default=False)

    salary = models.PositiveIntegerField('maoshi',default=0)
    wallet = models.IntegerField('qarzi haqqi',default=0)
    description = models.TextField(verbose_name="Description", null=True, blank=True)
    role = models.CharField(max_length=15, choices=Role.choices)
    def __str__(self):
        return self.username
    class Meta:
        db_table = "User"



