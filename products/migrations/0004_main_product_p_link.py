# Generated by Django 5.0.3 on 2024-07-28 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_main_product_p_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='main_product',
            name='p_link',
            field=models.CharField(blank=True, max_length=765),
        ),
    ]
