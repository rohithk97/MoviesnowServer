# Generated by Django 4.2.3 on 2023-09-16 04:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmapp', '0005_remove_movie_time_slots_delete_timeslot'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
