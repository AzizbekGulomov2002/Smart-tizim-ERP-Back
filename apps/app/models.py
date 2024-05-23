from django.db import models
from apps.users.models import User


# Create your models here.
# class Company(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     comp_name = models.CharField(max_length=500)
#     first_name = models.CharField(max_length=200)
#     family_name = models.CharField(max_length=200)
#     phone = models.IntegerField()
#     email = models.EmailField()
#
#     is_active = models.BooleanField(default=True)
#
#     start_date = models.DateTimeField(null=True,blank=True)
#     end_date = models.DateTimeField(null=True,blank=True)
#     sum = models.IntegerField(default=0)
#
#     def __str__(self):
#         return self.comp_name
