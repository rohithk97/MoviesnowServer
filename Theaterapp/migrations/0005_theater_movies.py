# Generated by Django 4.2.3 on 2023-08-14 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('filmapp', '0002_movie_image'),
        ('Theaterapp', '0004_alter_theater_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='theater',
            name='movies',
            field=models.ManyToManyField(related_name='theaters', to='filmapp.movie'),
        ),
    ]
