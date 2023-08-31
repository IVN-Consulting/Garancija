from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} - {self.address}"

class Employee(models.Model):
    name = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=256)
    email = models.EmailField()
    shop = models.ForeignKey(Shop, on_delete=models.DO_NOTHING, related_name="employees")

    def __str__(self):
        return f"{self.name} - {self.email}"