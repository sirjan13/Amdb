# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-26 19:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('username', models.CharField(max_length=120, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('short_bio', models.CharField(max_length=350)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
