# Generated by Django 5.0.3 on 2025-04-22 19:57

import django.core.validators
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_admin', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='delivery_fee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
    ]
