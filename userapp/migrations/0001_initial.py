# Generated by Django 4.2.3 on 2023-07-30 15:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=100, unique=True)),
                ('password', models.CharField(max_length=250)),
                ('name', models.CharField(max_length=50, null=True)),
                ('phone', models.PositiveBigIntegerField(null=True, validators=[django.core.validators.RegexValidator(message='Mobile number should only contain digits', regex='^\\d+$')])),
                ('profile_image', models.ImageField(blank=True, null=True, upload_to='profile_image')),
                ('date_joined', models.DateField(auto_now_add=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
