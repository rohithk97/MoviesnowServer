# Generated by Django 4.2.3 on 2023-08-07 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Theaterapp', '0003_alter_theater_contact_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theater',
            name='location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]