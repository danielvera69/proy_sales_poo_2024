# Generated by Django 4.2 on 2024-07-05 21:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_product_expiration_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='expiration_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 8, 4, 21, 43, 32, 158061, tzinfo=datetime.timezone.utc), verbose_name='Caducidad'),
        ),
    ]
