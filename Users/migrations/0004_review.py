# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-29 10:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_genre_movie_moviegenre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('review', models.CharField(max_length=300)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.Movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Users.Users')),
            ],
        ),
    ]
