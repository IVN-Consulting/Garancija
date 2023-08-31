from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=256)
    address = models.CharField(max_length=256)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} - {self.address}"