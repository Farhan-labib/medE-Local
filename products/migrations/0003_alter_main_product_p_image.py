# Generated by Django 5.0.3 on 2025-06-12 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_main_product_feature_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='main_product',
            name='p_image',
            field=models.ImageField(default='static\\cat-icons\\syringe.png', upload_to='media/'),
        ),
    ]
