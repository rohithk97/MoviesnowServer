# Generated by Django 4.2.3 on 2023-09-06 07:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('filmapp', '0005_remove_movie_time_slots_delete_timeslot'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Theaterapp', '0016_delete_booking'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seats_booked', models.JSONField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='filmapp.movie')),
                ('theater', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Theaterapp.theater')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
