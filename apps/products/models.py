from django.db import models
from django.db.models import Sum
from django.conf import settings
from datetime import datetime
from apps.app.models import BaseModel

# Create your models here.
class Category(BaseModel):
    def __str__(self):
        return self.name

class Format(BaseModel):
    def __str__(self):
        return self.name

class DelateManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted__isnull=True)



class Product(BaseModel):
    PRODUCT_TYPE = [
        ('Sanaladigan', 'Sanaladigan'),
        ('Sanalmaydigan', 'Sanalmaydigan')
    ]
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE , default='Sanaladigan')
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
        return f"{self.name} | {self.id}"


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
    supplier_type = models.CharField(max_length=20, choices=SUPPLIER_TYPE, default="Tezkor")
    phone = models.CharField(max_length=11, null=True, blank=True)
    added = models.DateTimeField()
    desc = models.TextField(blank=True, null=True)

    # @property
    # def status:
    #     if total>0:
    #         return "Qarzdorlik"
    #     else:
    #         return "Aktiv"
    def __str__(self):
        return self.name


class Storage(BaseModel):
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
    storage_type = models.CharField(max_length=20, choices=STORAGE_TYPE, default="Naqtga")
    size_type = models.CharField(max_length=20, choices=SIZE_TYPE, default="O'lchovsiz")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="storage_products")

    storage_count = models.FloatField(default=1)
    part_size = models.FloatField(null=True, blank=True, default=1)  # Set a default value
    height = models.FloatField(null=True, blank=True, default=1)  # Set a default value
    width = models.FloatField(null=True, blank=True, default=1)  # Set a default value
    price = models.FloatField(default=1)

    date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True, related_name='storages')

    remind_count = models.FloatField(help_text='Eslatish miqdori ...', default=0)
    expiration = models.DateField(help_text='Yaroqlilik muddati ...', null=True, blank=True)
    # total_summa = models.FloatField(default=0)

    deleted = models.DateField(null=True, blank=True)
    objects = DelateManager()
    all_objects = models.Manager()

    @property
    def total_summa(self):
        if self.size_type == "O'lchovsiz":
            return self.storage_count * self.price
        elif self.size_type == "O'lchovli":
            return self.storage_count * self.part_size * self.price
        elif self.size_type == "Formatli":
            return self.storage_count * self.width * self.height * self.price
        else:
            return 0


    def delete(self):
        self.deleted = datetime.now().date()
        self.save()

    def __str__(self):
        return self.product.name




