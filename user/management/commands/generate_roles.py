from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model


User = get_user_model()


class Command(BaseCommand):

    def handle(self, *args, **options):
        employee, created = Group.objects.get_or_create(name="employee")
        customer, created = Group.objects.get_or_create(name="customer")

        employee_permissions = (
            'can_create_warranty',
            'can_edit_warranty',
            'can_delete_warranty',
            'can_view_shop_warranty',
        )

        customer_permissions = (
            'can_view_my_warranty',
        )

        employee.permissions.set(
            Permission.objects.filter(
                name__in=employee_permissions
            )
        )

        customer.permissions.set(
            Permission.objects.filter(
                name__in=customer_permissions
            )
        )

        for user in User.objects.filter(user_type='customer'):
            user.groups.add(customer)
            user.save()

        for user in User.objects.filter(user_type='employee'):
            user.groups.add(employee)
            user.save()
