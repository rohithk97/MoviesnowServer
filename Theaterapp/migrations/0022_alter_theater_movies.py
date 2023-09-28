# Generated by Django 4.2.3 on 2023-09-14 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmapp', '0005_remove_movie_time_slots_delete_timeslot'),
        ('Theaterapp', '0021_alter_theater_movies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theater',
            name='movies',
            field=models.ManyToManyField(blank=True, related_name='theaters', to='filmapp.movie'),
        ),
    ]
