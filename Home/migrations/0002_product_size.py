# Generated by Django 5.0.3 on 2024-07-27 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]