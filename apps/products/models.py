from django.db import models
from django.db.models import Sum
from django.conf import settings
from datetime import datetime
from apps.app.models import BaseModel
from apps.finance.models import FinanceOutcome


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
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPE)
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

    @property
    def current_total_count(self):
        total_current_count = 0
        for storage_product in self.storage_products.all():
            total_off_count = storage_product.storageproductoff_set.aggregate(total_off=Sum('count'))['total_off'] or 0
            total_current_count += storage_product.total_count - total_off_count
        return total_current_count

    def __str__(self):
        return f"{self.name} | {self.id}"


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
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True, related_name='storages')
    company_id = models.BigIntegerField(default=0)
    storage_type = models.CharField(max_length=20, choices=STORAGE_TYPE, default="Naqtga")
    size_type = models.CharField(max_length=20, choices=SIZE_TYPE, default="O'lchovsiz")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="storage_products")

    storage_count = models.FloatField(default=1)
    part_size = models.FloatField(null=True, blank=True, default=1)  # Set a default value
    height = models.FloatField(null=True, blank=True, default=1)  # Set a default value
    width = models.FloatField(null=True, blank=True, default=1)  # Set a default value
    price = models.FloatField(default=1)

    date = models.DateTimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)


    remind_count = models.FloatField(help_text='Eslatish miqdori ...', default=0)
    expiration = models.DateField(help_text='Yaroqlilik muddati ...', null=True, blank=True)
    # desc = models.TextField(null=True, blank=True)


    # deleted = models.DateField(null=True, blank=True)
    # objects = DelateManager()
    # all_objects = models.Manager()


    @property
    def total_count(self):
        if self.size_type == "O'lchovsiz":
            return self.storage_count
        elif self.size_type == "O'lchovli":
            return self.storage_count * self.part_size
        elif self.size_type == "Formatli":
            return self.storage_count*self.width*self.height
        else:
            return 0

    @property
    def total_summa(self):
        return self.price*self.total_count

    @property
    def current_total_count(self):
        total_off_count = self.storageproductoff_set.aggregate(total_off=Sum('count'))['total_off'] or 0
        return self.total_count - total_off_count


    # def delete(self):
    #     self.deleted = datetime.now().date()
    #     self.save()

    def delete(self, *args, **kwargs):
        # Delete related FinanceOutcome instances
        FinanceOutcome.objects.filter(
            user=self.user,
            supplier=self.supplier,
            storage_product=self
        ).delete()
        self.deleted = datetime.now().date()
        self.save()


    def __str__(self):
        return self.product.name




class StorageProductOff(models.Model):
    company_id = models.BigIntegerField(default=0)
    product = models.ForeignKey(StorageProduct, on_delete=models.CASCADE)
    count = models.FloatField()
    def __str__(self):
        return f"{self.count}"




