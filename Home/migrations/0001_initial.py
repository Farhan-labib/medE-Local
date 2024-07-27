# Generated by Django 5.0.3 on 2024-07-27 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('p_name', models.CharField(max_length=255)),
                ('p_category', models.CharField(max_length=255)),
                ('p_image', models.ImageField(default='static\\cat-icons\\syringe.png', upload_to='media/')),
                ('p_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('p_discount', models.DecimalField(decimal_places=2, max_digits=5)),
                ('p_id', models.AutoField(primary_key=True, serialize=False)),
                ('p_type', models.CharField(blank=True, max_length=255)),
                ('p_Dosage', models.TextField(blank=True)),
                ('p_Dosage_Strength', models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]
