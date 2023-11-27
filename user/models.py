from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    shop = models.ForeignKey(
        'garancija.Shop',
        on_delete=models.DO_NOTHING,
        related_name="employees",
        null=True,
        default=None,
        blank=True
    )
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

    class Meta(AbstractUser.Meta):
        permissions = (
            ('can_create_warranty', 'can_create_warranty'),
            ('can_edit_warranty', 'can_edit_warranty'),
            ('can_delete_warranty', 'can_delete_warranty'),
            ("can_view_my_warranty", "can_view_my_warranty"),
            ("can_view_shop_warranty", "can_view_shop_warranty"),
            ("can_view_shop_employee", "can_view_shop_employee"),
            ("can_view_customer", "can_view_customer")
        )
