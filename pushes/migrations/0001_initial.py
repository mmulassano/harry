# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-06 14:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('active', models.BooleanField(default=True)),
                ('user_id', models.IntegerField()),
                ('device_id', models.IntegerField(unique=True)),
                ('key_firebase', models.CharField(max_length=500)),
                ('date_create', models.CharField(max_length=100)),
            ],
        ),
    ]
