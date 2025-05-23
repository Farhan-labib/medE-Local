# Generated by Django 5.0.3 on 2025-03-26 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_main_product_inventory_alter_orders_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='main_product',
            name='Batch',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='main_product',
            name='EXP_Date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='main_product',
            name='MFG_Date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='main_product',
            name='Purchase_Price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='main_product',
            name='SKU',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='main_product',
            name='Stock',
            field=models.IntegerField(default=0),
        ),
    ]
