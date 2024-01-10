from django.db import models
from user.models import User


class Shop(models.Model):
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name}"


class Warranty(models.Model):
    product_name = models.CharField(max_length=256)
    start_date = models.DateField()
    end_date = models.DateField()
    salesperson = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="salesperson")
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="warranties", null=True, default=None)
    file = models.FileField(blank=True, null=True, upload_to='files/')

    def __str__(self):
        return f"{self.product_name} - {self.salesperson.shop} - {self.salesperson} - {self.customer}"
