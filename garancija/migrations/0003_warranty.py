# Generated by Django 4.2.4 on 2023-09-07 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('garancija', '0002_employee'),
    ]

    operations = [
        migrations.CreateModel(
            name='Warranty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=256)),
                ('start_date', models.DateField(max_length=256)),
                ('end_date', models.DateField(max_length=256)),
                ('active', models.BooleanField(default=None)),
                ('salesperson', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='salesperson', to='garancija.employee')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='shops', to='garancija.shop')),
            ],
        ),
    ]