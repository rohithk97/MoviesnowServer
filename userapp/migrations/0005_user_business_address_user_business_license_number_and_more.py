# Generated by Django 4.2.3 on 2023-09-12 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0004_remove_user_is_blocked'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='business_address',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='business_license_number',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='business_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
