# Generated by Django 4.2.3 on 2023-10-12 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_userprofile_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user_type',
            field=models.CharField(choices=[('quatity', 'quatity'), ('days', 'days')], default='days', max_length=10),
        ),
    ]
