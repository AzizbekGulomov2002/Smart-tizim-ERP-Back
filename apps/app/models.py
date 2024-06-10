from django.db import models
from apps.users.models import User


class BaseModel(models.Model):
    company_id = models.BigIntegerField(default=0)
    name = models.CharField(max_length=500)
    class Meta:
        abstract = True  # Ensure this is an abstract base class

