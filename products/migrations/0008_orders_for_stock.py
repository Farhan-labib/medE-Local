# Generated by Django 5.0.3 on 2025-03-28 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_remove_main_product_alert'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='for_stock',
            field=models.TextField(default='null'),
        ),
    ]
