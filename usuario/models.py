from __future__ import unicode_literals

from django.db import models

# Create your models here.

class TypeUser(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name='Nombre')

class Profile(models.Model):
    user_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='user', null=True)
