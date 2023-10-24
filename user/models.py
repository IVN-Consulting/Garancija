from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    shop = models.ForeignKey('garancija.Shop', on_delete=models.DO_NOTHING, related_name="employees", null=True, default=None, blank=True)
    user_type = models.CharField(
        max_length=64,
        choices=(
            ("employee", "employee"),
            ("customer", "customer")
        )
    )
    phone_number = models.CharField(max_length=64, null=True)

    def clean(self):
        super().clean()
        if self.user_type == "employee" and self.shop is None:
            raise Exception("employee without a shop")