# Generated by Django 4.2.4 on 2023-11-25 22:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': (('can_create_warranty', 'can_create_warranty'), ('can_edit_warranty', 'can_edit_warranty'), ('can_delete_warranty', 'can_delete_warranty'), ('can_view_my_warranty', 'can_view_my_warranty'), ('can_view_shop_warranty', 'can_view_shop_warranty'), ('can_view_customer', 'can_view_customer')), 'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
    ]
