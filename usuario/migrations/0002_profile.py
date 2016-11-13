# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-10-07 19:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(unique=True)),
                ('name', models.CharField(max_length=100)),
                ('photo', models.ImageField(null=True, upload_to='user')),
            ],
        ),
    ]
