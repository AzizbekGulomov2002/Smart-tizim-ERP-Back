from django.db import models

# Create your models here.


class Position(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
class Worker(models.Model):
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    name = models.CharField(max_length=400)
    phone = models.CharField(max_length=13)
    desc = models.TextField(blank=True, null=True)
    added = models.DateTimeField()
    def __str__(self):
        return self.name