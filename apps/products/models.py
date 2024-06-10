from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.conf import settings
from datetime import datetime
from datetime import timedelta
from apps.app.models import BaseModel

# Create your models here.
class Category(BaseModel):
    # company_id = models.BigIntegerField(default=0)
    # name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class Format(BaseModel):
    # company_id = models.BigIntegerField(default=0)
    # name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

class DelateManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted__isnull=True)



class Product(BaseModel):
    STORAGE_TYPES = [
        ('Sanaladigan', 'Sanaladigan'),
        ('Sanalmaydigan', 'Sanalmaydigan')
    ]
    # company_id = models.BigIntegerField(default=0)
    # name = models.CharField(max_length=100)
    storage_type = models.CharField(max_length=20, choices=STORAGE_TYPES , default='Sanaladigan')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    format = models.ForeignKey(Format, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    bar_code = models.TextField(blank=True, null=True)


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


    @property
    def total_storage_count(self):
        total_quantity = sum(product.quantity for product in self.storage_products.all())
        return total_quantity

    @property
    def current_storage_count(self):
        total_import = \
        self.storage_products.filter(storage__action_type='Kiritish').aggregate(total_import=Sum('count'))[
            'total_import'] or 0
        total_remove = \
        self.storage_products.filter(storage__action_type='Chiqarish').aggregate(total_remove=Sum('count'))[
            'total_remove'] or 0
        return total_import - total_remove

    def __str__(self):
        return self.name


class Supplier(BaseModel):
    SUPPLIER_TYPE = (
        ('Tezkor', 'Tezkor'),
        ('Doimiy', 'Doimiy'),
    )
    # company_id = models.BigIntegerField(default=0)
    supplier_type = models.CharField(max_length=20, choices=SUPPLIER_TYPE, default="Tezkor")
    # name = models.CharField(max_length=400, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    added = models.DateTimeField()
    desc = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.name


class Storage(BaseModel):
    # company_id = models.BigIntegerField(default=0)
    # name = models.CharField(max_length=300)
    def __str__(self):
        return self.name


class StorageProduct(models.Model):
    SIZE_TYPE = (
        ("O'lchovli", "O'lchovli"),
        ("O'lchovsiz", "O'lchovsiz"),
        ("Formatli", "Formatli"),
    )
    STORAGE_TYPE = (
        ('Naqtga', 'Naqtga'),
        ('Qarzga', 'Qarzga'),
    )
    company_id = models.BigIntegerField(default=0)
    size_type = models.CharField(max_length=20, choices=SIZE_TYPE, default="O'lchovsiz")
    # storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="storage_products")
    storage_count = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(null=True, blank=True)
    date = models.DateTimeField(null=True,blank=True) # noqa

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True) # StorageProductga
    storage_type = models.CharField(max_length=20, choices=STORAGE_TYPE, default="Naqtga") # StorageProductga
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True, related_name='storages') # StorageProductga

    remind_count = models.FloatField(help_text='Eslatish miqdori ...',default=0) # StorageProductga
    expiration = models.DateField(help_text='Yaroqlilik muddati ...',null=True,blank=True) # StorageProductga
    total_summa = models.PositiveIntegerField(default=0 ,null=True,blank=True)

    deleted = models.DateField(null=True, blank=True)
    objects = DelateManager()
    all_objects = models.Manager()
    def delete(self):
        self.deleted = datetime.now().date()
        self.save()
    def __str__(self):
        return self.product.name


# class CompanyId(models.Model):
#     company_id = models.BigIntegerField(default=0)

# # Create your models here.
# class Category(CompanyId):
#     name = models.CharField(max_length=100)
#     def str(self):
#         return self.name

