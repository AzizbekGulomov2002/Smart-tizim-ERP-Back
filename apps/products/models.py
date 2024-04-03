from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.conf import settings
from datetime import datetime
from datetime import timedelta


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Format(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Product(models.Model):
    STORAGE_TYPES = [
        ('Sanaladigan', 'Sanaladigan'),
        ('Sanalmaydigan', 'Sanalmaydigan')
    ]
    name = models.CharField(max_length=100)
    storage_type = models.CharField(max_length=20, choices=STORAGE_TYPES)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    format = models.ForeignKey(Format, on_delete=models.CASCADE)
    measure = models.FloatField(default=1)
    price = models.PositiveIntegerField()
    bar_code = models.TextField(blank=True, null=True)

    @property
    def total_storage_count(self):
        total_import = \
        self.storageproduct_set.filter(storage__action_type='Kiritish').aggregate(total_import=Sum('storage_count'))[
            'total_import'] or 0
        total_remove = \
        self.storageproduct_set.filter(storage__action_type='Chiqarish').aggregate(total_remove=Sum('storage_count'))[
            'total_remove'] or 0
        return total_import - total_remove

    # @property
    # def current_storage_count(self):
    #     return self.total_storage_count
    #
    # @property
    # def total_size(self):
    #     total_size = self.storageproduct_set.aggregate(
    #         total_size=Sum(models.F('height') * models.F('width') * models.F('quantity') * models.F('price')))[
    #         'total_size']
    #     return total_size or 0

    def __str__(self):
        return self.name

class Supplier(models.Model):
    SUPPLIER_TYPE = (
        ('Tezkor', 'Tezkor'),
        ('Doimiy', 'Doimiy'),
    )
    supplier_type = models.CharField(max_length=20, choices=SUPPLIER_TYPE, default="Tezkor")
    name = models.CharField(max_length=400)
    phone = models.CharField(max_length=11)
    added = models.DateTimeField()
    desc = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name


class Storage(models.Model):
    STORAGE_TYPE = (
        ('Naqtga', 'Naqtga'),
        ('Qarzga', 'Qarzga'),
    )
    ACTION_TYPE = (
        ('Kiritish', 'Kiritish'),
        ('Chiqarish', 'Chiqarish'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action_type = models.CharField(max_length=20, choices=ACTION_TYPE, default='Kiritish')
    storage_type = models.CharField(max_length=20, choices=STORAGE_TYPE, default="Naqtga")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    storage_date = models.DateTimeField()
    desc = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.storage_date.strftime('%Y-%m-%d %H:%M:%S')}"


class StorageProduct(models.Model):
    SIZE_TYPE = (
        ("O'lchovli", "O'lchovli"),
        ("O'lchovsiz", "O'lchovsiz"),
        ("Formatli", "Formatli"),
    )
    size_type = models.CharField(max_length=20, choices=SIZE_TYPE, default="O'lchovsiz")
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    storage_count = models.FloatField()
    price = models.PositiveIntegerField()
    # validation_date = models.DateField()
    # status = models.BooleanField(default=True)

    size = models.FloatField(default=1)
    height = models.FloatField(default=1)
    width = models.FloatField(default=1)
    quantity = models.FloatField(default=1)

    property
    def total_size(self):
        return self.height*self.width*self.quantity*self.price

    def __str__(self):
        return self.product.name

