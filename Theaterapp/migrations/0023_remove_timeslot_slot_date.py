# Generated by Django 4.2.3 on 2023-09-15 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Theaterapp', '0022_alter_theater_movies'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timeslot',
            name='slot_date',
        ),
    ]