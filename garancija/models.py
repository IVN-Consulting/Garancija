from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name}"


class Employee(models.Model):
    name = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=256)
    email = models.EmailField()
    shop = models.ForeignKey(Shop, on_delete=models.DO_NOTHING, related_name="employees")

    def __str__(self):
        return f"{self.name}"


class Warranty(models.Model):
    product_name = models.CharField(max_length=256)
    start_date = models.DateField()
    end_date = models.DateField()
    salesperson = models.ForeignKey(Employee, on_delete=models.DO_NOTHING, related_name="salesperson")

    def __str__(self):
        return f"{self.product_name} - {self.salesperson.shop} - {self.salesperson}"
