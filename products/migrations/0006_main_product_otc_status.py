# Generated by Django 4.2.5 on 2023-11-13 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_orders_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='main_product',
            name='otc_status',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], default='yes', max_length=3),
        ),
    ]
