from django.db import models

# Create your models here.


class Product(models.Model):

    name = models.CharField(max_length=15)
    category = models.CharField(max_length=15)
    price = models.IntegerField()
