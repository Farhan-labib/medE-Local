# Generated by Django 5.0.3 on 2025-03-26 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_presciption_order_payment_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presciption_order',
            name='Delivery_status',
        ),
        migrations.RemoveField(
            model_name='presciption_order',
            name='status',
        ),
        migrations.AddField(
            model_name='presciption_order',
            name='Order_status',
            field=models.CharField(blank=True, choices=[('Pending', 'Pending'), ('Created', 'Created'), ('Rejected', 'Rejected')], default='Pending', max_length=20),
        ),
    ]
